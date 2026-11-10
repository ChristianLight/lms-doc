#!/usr/bin/env python3
"""Inventory ZIP course archives without extracting or evaluating course content."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from decimal import Decimal, InvalidOperation
from html.parser import HTMLParser
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import sys
import tempfile
import unicodedata
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree as ET
from xml.parsers import expat
import zipfile


FILE_LIMIT = 50_000
ARCHIVE_BYTES = 512 * 1024 * 1024
DIRECTORY_BYTES = 16 * 1024 * 1024
EXPANDED_BYTES = 512 * 1024 * 1024
MEMBER_BYTES = 128 * 1024 * 1024
TEXT_BYTES = 16 * 1024 * 1024
TOTAL_TEXT_BYTES = 128 * 1024 * 1024
TREE_DEPTH = 128
TREE_NODES = 150_000
TOTAL_XML_NODES = 1_000_000
MAX_EDGES = 250_000
MAX_URLS = 250_000
MAX_URL_LENGTH = 8192
ZIP_METHODS = {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
CORE = {"course", "chapter", "sequential", "vertical", "html", "problem", "video"}
EXTENSIONS = {"openassessment", "drag-and-drop-v2", "library_content", "scorm", "lti", "lti_consumer"}
CHILDREN = {
    "course": {"chapter"},
    "chapter": {"sequential"},
    "sequential": {"vertical"},
    "vertical": {"html", "problem", "video"} | EXTENSIONS,
}
KNOWN_ROOTS = CORE | EXTENSIONS | {"assets"}
HEX_KEY = re.compile(r"[0-9A-Fa-f]{32}\Z")
UUID_KEY = re.compile(r"[0-9A-Fa-f]{8}(?:-[0-9A-Fa-f]{4}){3}-[0-9A-Fa-f]{12}\Z")
BLOCK_KEY = re.compile(r"block-v1:([^+]+)\+([^+]+)\+([^+]+)\+type@([^+]+)\+block@([^+]+)\Z")
URL_FIELDS = {"href", "src", "data", "poster", "action", "xlink:href"}


class AuditError(Exception):
    """A stable diagnostic whose text is safe to emit without private evidence."""


def member_path(raw: str) -> str:
    path = raw[:-1] if raw.endswith("/") else raw
    parts = path.split("/")
    if (
        not path or len(path) > 2048 or len(parts) > 24
        or re.search(r"[\\:\x00-\x1f\x7f]", path)
        or any(part in {"", ".", ".."} for part in parts)
        or unicodedata.normalize("NFC", path) != path
    ):
        raise AuditError("UNSAFE_MEMBER_PATH")
    decoded = unquote(path)
    if re.search(r"%[a-fA-F0-9]{2}", decoded) or (
        decoded != path
        and (decoded.count("/") != path.count("/") or "\\" in decoded
             or any(part in {".", ".."} for part in decoded.split("/"))
             or re.search(r"[\x00-\x1f\x7f]", decoded))
    ):
        raise AuditError("UNSAFE_ENCODED_MEMBER_PATH")
    return path



def check_central_directory(source, size: int) -> None:
    """Bound the ordinary ZIP directory before ZipFile allocates member metadata."""
    tail_start = max(0, size - 65_557)
    source.seek(tail_start)
    tail = source.read()
    footer = tail.rfind(b"PK\x05\x06")
    while footer >= 0:
        if footer + 22 <= len(tail):
            _, disk, directory_disk, here, total, length, offset, comment = struct.unpack_from(
                "<4s4H2LH", tail, footer
            )
            if footer + 22 + comment == len(tail):
                break
        footer = tail.rfind(b"PK\x05\x06", 0, footer)
    if footer < 0:
        raise AuditError("ZIP_DIRECTORY_FOOTER_MISSING")
    if disk or directory_disk or here != total or total > FILE_LIMIT:
        raise AuditError("ZIP_DIRECTORY_LAYOUT_REJECTED")
    if length > DIRECTORY_BYTES or offset + length != tail_start + footer:
        raise AuditError("ZIP_DIRECTORY_RANGE_REJECTED")
    source.seek(offset)
    directory = source.read(length)
    position = 0
    found = 0
    while position < length:
        if position + 46 > length or directory[position:position + 4] != b"PK\x01\x02":
            raise AuditError("INVALID_CENTRAL_DIRECTORY_ENTRY")
        name_length, extra_length, comment_length = struct.unpack_from("<3H", directory, position + 28)
        position += 46 + name_length + extra_length + comment_length
        found += 1
        if found > FILE_LIMIT or position > length:
            raise AuditError("CENTRAL_DIRECTORY_ENTRY_LIMIT")
    if found != total:
        raise AuditError("CENTRAL_DIRECTORY_ENTRY_COUNT_MISMATCH")


def decode_member_uri(path: str) -> str:
    parts = []
    for segment in path.split("/"):
        decoded = unquote(segment, errors="strict")
        if any(mark in decoded for mark in ("/", "\\", "?", "#", "%")):
            raise AuditError("UNSAFE_URI_PATH_SEGMENT")
        parts.append(decoded)
    return member_path("/".join(parts))

def index_members(container: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    files = {}
    exact = set()
    folded: dict[str, str] = {}
    directories = set()
    expanded = 0
    members = container.infolist()
    if len(members) > FILE_LIMIT:
        raise AuditError("ARCHIVE_ENTRY_LIMIT")
    for info in members:
        original = info.orig_filename
        path = member_path(original)
        if path in exact or original != info.filename:
            raise AuditError("DUPLICATE_OR_AMBIGUOUS_MEMBER")
        exact.add(path)
        parts = path.split("/")
        prefixes = ["/".join(parts[:i]) for i in range(1, len(parts) + 1)]
        for prefix in prefixes:
            existing = folded.setdefault(prefix.casefold(), prefix)
            if existing != prefix:
                raise AuditError("CASE_COLLIDING_MEMBER")
        directories.update(prefixes[:-1])
        mode = stat.S_IFMT(info.external_attr >> 16) if info.create_system == 3 else 0
        if mode not in (0, stat.S_IFREG, stat.S_IFDIR):
            raise AuditError("NONREGULAR_MEMBER")
        if (info.flag_bits & 1) or info.compress_type not in ZIP_METHODS:
            raise AuditError("UNSUPPORTED_MEMBER_ENCODING")
        if info.is_dir():
            if info.file_size or mode == stat.S_IFREG:
                raise AuditError("INVALID_DIRECTORY_ENTRY")
            directories.add(path)
            continue
        if mode == stat.S_IFDIR or info.file_size > MEMBER_BYTES:
            raise AuditError("MEMBER_SIZE_OR_KIND_REJECTED")
        if info.file_size > max(1024 * 1024, info.compress_size * 500):
            raise AuditError("MEMBER_EXPANSION_LIMIT")
        expanded += info.file_size
        if expanded > EXPANDED_BYTES:
            raise AuditError("ARCHIVE_EXPANSION_LIMIT")
        files[path] = info
    if files.keys() & directories:
        raise AuditError("FILE_DIRECTORY_COLLISION")
    return files


def xml_tree(data: bytes, remaining_nodes: list[int]) -> ET.Element:
    """Build an XML tree with no DTDs, entity declarations or network resolution."""
    builder = ET.TreeBuilder()
    parser = expat.ParserCreate(namespace_separator="}")
    depth = 0
    nodes = 0

    def reject(*_):
        raise AuditError("XML_DTD_OR_EXTERNAL_ENTITY")

    def qualify(name):
        return "{" + name if "}" in name else name

    def start(name, attributes):
        nonlocal depth, nodes
        depth += 1
        nodes += 1
        remaining_nodes[0] -= 1
        if depth > TREE_DEPTH or nodes > TREE_NODES or remaining_nodes[0] < 0 or len(attributes) > 256:
            raise AuditError("XML_STRUCTURE_LIMIT")
        builder.start(qualify(name), {qualify(key): value for key, value in attributes.items()})

    def end(name):
        nonlocal depth
        builder.end(qualify(name))
        depth -= 1

    parser.StartDoctypeDeclHandler = reject
    parser.EntityDeclHandler = reject
    parser.ExternalEntityRefHandler = reject
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = builder.data
    try:
        parser.Parse(data, True)
        return builder.close()
    except (expat.ExpatError, ET.ParseError, ValueError) as error:
        raise AuditError("INVALID_XML") from error


def safe_key(value: str | None) -> bool:
    if not value:
        return False
    try:
        return member_path(value) == value and "/" not in value and "%" not in value
    except AuditError:
        return False


def known(tag: str) -> str:
    return tag if tag in KNOWN_ROOTS else "other"


def counts(rows) -> dict:
    return dict(sorted(Counter(rows).items()))


class LinkParser(HTMLParser):
    def __init__(self, emit):
        super().__init__(convert_charrefs=True)
        self.emit = emit

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in URL_FIELDS and value:
                self.emit(value, self.getpos()[0])


class CourseAudit:
    def __init__(self, container: zipfile.ZipFile):
        raw_files = index_members(container)
        candidates = [path for path in raw_files if PurePosixPath(path).name == "course.xml" and path.count("/") <= 1
                      and not (path == "course/course.xml" and "course.xml" in raw_files)]
        if len(candidates) != 1:
            raise AuditError("COURSE_DESCRIPTOR_MISSING_OR_AMBIGUOUS")
        entry = candidates[0]
        prefix = entry.removesuffix("course.xml")
        if prefix and any(not path.startswith(prefix) for path in raw_files):
            raise AuditError("MIXED_ARCHIVE_ROOTS")
        self.files = {path[len(prefix):]: info for path, info in raw_files.items()}
        self.container = container
        self.prefix = prefix
        self.read_bytes = 0
        self.remaining_xml_nodes = [TOTAL_XML_NODES]
        self.xml = {}
        self.issues = []
        self.links = []
        self.edges = []
        self.draft_anchors = []
        self.structural_keys = set()
        self.block_key_locations = defaultdict(set)
        self.visited = {}
        self.document_layers = defaultdict(set)
        self.selected = set()
        self.active = set()
        for path in sorted(self.files):
            if path.endswith(".xml"):
                try:
                    node = xml_tree(self.read_text(path), self.remaining_xml_nodes)
                except AuditError as error:
                    if str(error) not in {"INVALID_XML", "XML_DTD_OR_EXTERNAL_ENTITY"} or path == "course.xml":
                        raise
                    self.issue(str(error), path)
                    continue
                self.xml[path] = node
                if node.tag in CORE | EXTENSIONS and path != "course.xml":
                    key = PurePosixPath(path).stem
                    self.structural_keys.add((node.tag, key))
                    self.block_key_locations[key].add((node.tag, path.startswith("drafts/")))
        descriptor = self.xml["course.xml"]
        if descriptor.tag != "course":
            raise AuditError("INVALID_COURSE_DESCRIPTOR")
        self.scope = tuple(descriptor.get(key) for key in ("org", "course", "url_name"))
        if not all(safe_key(value) for value in self.scope):
            raise AuditError("INCOMPLETE_OR_UNSAFE_COURSE_SCOPE")
        has_inline_outline = any(child.tag in CHILDREN["course"] for child in descriptor)
        self.run_root = "course.xml" if has_inline_outline else f"course/{self.scope[2]}.xml"
        if self.run_root not in self.xml or self.xml[self.run_root].tag != "course":
            raise AuditError("SELECTED_RUN_DEFINITION_MISSING")
        if any(self.xml[self.run_root].get(key) not in (None, value) for key, value in zip(("org", "course", "url_name"), self.scope)):
            raise AuditError("COURSE_SCOPE_MISMATCH")

    def read_text(self, path):
        info = self.files[path]
        if info.file_size > TEXT_BYTES:
            raise AuditError("TEXT_MEMBER_LIMIT")
        with self.container.open(info) as stream:
            data = stream.read(TEXT_BYTES + 1)
        self.read_bytes += len(data)
        if len(data) != info.file_size or self.read_bytes > TOTAL_TEXT_BYTES:
            raise AuditError("TEXT_SIZE_OR_TOTAL_LIMIT")
        return data

    def issue(self, code, path, **details):
        if len(self.issues) >= MAX_EDGES:
            raise AuditError("GRAPH_ISSUE_LIMIT")
        self.issues.append({"code": code, "source": path, **details})

    def add_edge(self, row):
        if len(self.edges) >= MAX_EDGES:
            raise AuditError("GRAPH_EDGE_LIMIT")
        self.edges.append(row)

    def find_definition(self, kind, key, layer):
        if not safe_key(key):
            return None, "unsafe_key"
        plain = f"{kind}/{key}.xml"
        candidates = [f"drafts/{plain}", plain] if layer == "draft" else [plain]
        for path in candidates:
            if path in self.files:
                node = self.xml.get(path)
                if node is None or node.tag != kind or node.get("url_name") not in (None, key):
                    return None, "invalid_definition"
                return path, "resolved"
        return None, "missing_extension_definition" if kind in EXTENSIONS else "missing_definition"

    def walk(self, path, node, layer, depth=0, document=None):
        if depth >= TREE_DEPTH:
            raise AuditError("GRAPH_DEPTH_LIMIT")
        identity = (layer, path)
        if identity in self.active:
            self.issue("POINTER_CYCLE", path, layer=layer)
            return
        if identity in self.visited:
            return
        document = document or path
        self.visited[identity] = node.tag
        self.document_layers[document].add(layer)
        self.active.add(identity)
        if layer == "published":
            self.selected.add(path)
        if node.tag in CHILDREN:
            for ordinal, child in enumerate(node):
                kind = child.tag
                if kind not in CHILDREN[node.tag]:
                    if node.tag == "vertical":
                        self.issue("UNSUPPORTED_COMPONENT_KIND", path, kind=kind, ordinal=ordinal)
                    continue
                key = child.get("url_name")
                marker = child.get("x-is-pointer-node") == "true"
                has_body = bool(len(child) or (child.text or "").strip())
                is_pointer = marker or (key is not None and not has_body)
                if marker and has_body:
                    target, status = None, "ambiguous_pointer_and_body"
                elif is_pointer:
                    target, status = self.find_definition(kind, key, layer)
                else:
                    target, status = f"{path}#child[{ordinal}]", "inline"
                if target and (layer, target) in self.active:
                    status = "cycle"
                self.add_edge({"layer": layer, "source": path, "ordinal": ordinal, "kind": kind,
                               "key": key, "target": target, "status": status})
                if status == "inline":
                    self.walk(target, child, layer, depth + 1, document)
                elif status == "resolved":
                    self.walk(target, self.xml[target], layer, depth + 1)
                else:
                    self.issue(status.upper(), path, kind=kind, key=key, ordinal=ordinal, layer=layer)
        self.active.remove(identity)

    def index_drafts(self):
        slots = Counter()
        for path, node in self.xml.items():
            if not path.startswith("drafts/") or node.tag not in CORE | EXTENSIONS:
                continue
            parent = node.get("parent_url")
            ordinal = node.get("index_in_children_list")
            if parent is None and ordinal is None:
                continue
            match = BLOCK_KEY.fullmatch(parent or "")
            if not match or ordinal is None or not re.fullmatch(r"[0-9]{1,9}", ordinal):
                status, resolved, index = "unparsed_parent_or_index", None, None
            else:
                organization, course, run, kind, key = match.groups()
                index = int(ordinal)
                resolved, _ = self.find_definition(kind, key, "published") if kind in CORE else (None, None)
                if (organization, course, run) != self.scope:
                    status = "other_run_parent"
                elif not resolved:
                    status = "missing_parent"
                elif resolved not in self.selected:
                    status = "detached_parent"
                elif node.tag not in CHILDREN.get(kind, set()):
                    status = "invalid_parent_kind"
                else:
                    status = "reachable_parent"
                    slots[(resolved, index)] += 1
                    self.walk(path, node, "draft")
            self.draft_anchors.append({"source": path, "parent": parent, "target": resolved, "ordinal": index, "status": status})
            if status != "reachable_parent":
                self.issue("DRAFT_ANCHOR_REVIEW", path, status=status)
        for (target, index), count in sorted(slots.items()):
            if count > 1:
                self.issue("DRAFT_ORDINAL_COLLISION", target, ordinal=index, candidates=count)

    def inspect_html(self):
        result = Counter()
        for path, node in self.xml.items():
            if node.tag == "html":
                name = node.get("filename")
                if name is None:
                    result["inline_or_unspecified"] += 1
                elif not safe_key(name):
                    result["unsafe_companion"] += 1
                    self.issue("UNSAFE_HTML_COMPANION", path)
                else:
                    companion = str(PurePosixPath(path).parent / (name + ".html"))
                    if companion in self.files:
                        result["present_companion"] += 1
                        self.document_layers[companion].update(self.document_layers.get(path, ()))
                    else:
                        result["missing_companion"] += 1
                        self.issue("MISSING_HTML_COMPANION", path, candidate=companion)
            for element in node.iter():
                for key, value in element.attrib.items():
                    if (key in URL_FIELDS or key == "{http://www.w3.org/1999/xlink}href") and value:
                        self.audit_url(path, value, None)
                if element.tag == "html" and element.text and "<" in element.text:
                    self.scan_html(path, element.text)
        for path in sorted(self.files):
            if path.endswith(".html"):
                try:
                    value = self.read_text(path).decode("utf-8-sig")
                except UnicodeDecodeError:
                    self.issue("HTML_ENCODING_REVIEW", path)
                    continue
                self.scan_html(path, value)
        return dict(sorted(result.items()))

    def scan_html(self, path, text):
        parser = LinkParser(lambda value, line: self.audit_url(path, value, line))
        try:
            parser.feed(text)
            parser.close()
        except (ValueError, AssertionError):
            self.issue("HTML_PARSE_REVIEW", path)

    def audit_url(self, source, value, line):
        if len(self.links) >= MAX_URLS:
            raise AuditError("LINK_COUNT_LIMIT")
        target = None
        if len(value) > MAX_URL_LENGTH or re.search(r"[\x00-\x1f\x7f]", value):
            status = "unsafe_or_oversize_uri"
        else:
            try:
                uri = urlsplit(value.strip())
                _ = uri.port
                if uri.username or uri.password:
                    status = "credential_uri"
                elif value.strip().startswith("#"):
                    status = "fragment"
                elif uri.scheme not in ("", "http", "https"):
                    status = "opaque_source_route" if uri.scheme in ("i4x", "asset-v1", "block-v1") else "non_http_uri"
                elif uri.netloc or uri.scheme:
                    status = "absolute_unit_route_needs_authority" if "/jump_to_id/" in uri.path else "external_authority"
                elif uri.path.startswith("/jump_to_id/"):
                    key = unquote(uri.path.removeprefix("/jump_to_id/"), errors="strict")
                    if not safe_key(key):
                        status = "unsafe_unit_key"
                    else:
                        published, _ = self.find_definition("vertical", key, "published")
                        draft, _ = self.find_definition("vertical", key, "draft")
                        if published in self.selected:
                            target, status = published, "unit_in_selected_published"
                        elif ("draft", draft) in self.visited:
                            target, status = draft, "unit_in_selected_draft_only"
                        elif published or draft:
                            target, status = published or draft, "unit_detached"
                        else:
                            status = "unit_missing"
                elif uri.path.startswith("/static/"):
                    try:
                        candidate = decode_member_uri(uri.path.removeprefix("/"))
                    except AuditError:
                        status = "unsafe_asset_path"
                    else:
                        status = "asset_present" if candidate in self.files else "asset_missing"
                        target = candidate if candidate in self.files else None
                elif uri.path.startswith("/"):
                    status = "root_route_needs_profile"
                else:
                    status = "relative_route_needs_base"
            except (ValueError, UnicodeError):
                status = "invalid_uri"

        sanitized = None
        if status not in {"credential_uri", "invalid_uri", "unsafe_or_oversize_uri", "non_http_uri"}:
            sanitized = value.strip().split("?", 1)[0].split("#", 1)[0] or None
        self.links.append({"source": source, "value_without_query_fragment": sanitized,
                           "line": line, "status": status, "target": target})

    def inspect_policies(self):
        categories = Counter()

        def unique(pairs):
            fields = {}
            for key, value in pairs:
                if key in fields:
                    raise ValueError("duplicate key")
                fields[key] = value
            return fields

        def no_nonfinite(_):
            raise ValueError("nonfinite number")

        for path in sorted(self.files):
            if not path.startswith("policies/") or not path.endswith(".json"):
                continue
            try:
                data = json.loads(self.read_text(path), object_pairs_hook=unique, parse_float=Decimal, parse_constant=no_nonfinite)
                if not isinstance(data, dict):
                    raise ValueError("expected object")
            except (ValueError, RecursionError, InvalidOperation):
                self.issue("INVALID_POLICY_JSON", path)
                continue
            parts = path.split("/")
            if len(parts) == 3 and parts[1] == self.scope[2]:
                categories["selected_run_policy_documents"] += 1
                if parts[-1] == "grading_policy.json":
                    categories["selected_grading_categories"] += len(data["GRADER"]) if isinstance(data.get("GRADER"), list) else 0
            elif len(parts) == 3:
                categories["alternate_run_policy_documents"] += 1
            elif path == "policies/assets.json":
                categories["asset_policy_entries"] += len(data)
            else:
                categories["other_policy_documents"] += 1
        return dict(sorted(categories.items()))

    def run(self):
        self.walk(self.run_root, self.xml[self.run_root], "published")
        self.index_drafts()
        html = self.inspect_html()
        policies = self.inspect_policies()
        published_edges = [e for e in self.edges if e["layer"] == "published"]
        draft_edges = [e for e in self.edges if e["layer"] == "draft"]
        repeated = Counter(e["target"] for e in published_edges if e["status"] == "resolved")
        key_formats = Counter()
        detached = Counter()
        for path, node in self.xml.items():
            if path == "course.xml" or node.tag not in CORE | EXTENSIONS:
                continue
            stem = PurePosixPath(path).stem
            key_formats["opaque_32hex" if HEX_KEY.fullmatch(stem) else "uuid_shaped" if UUID_KEY.fullmatch(stem) else "other"] += 1
            if path not in self.selected and not path.startswith("drafts/"):
                detached[known(node.tag)] += 1
        links_by_projection = defaultdict(Counter)
        for row in self.links:
            layers = self.document_layers.get(row["source"], set())
            projection = (
                "selected_both_layers" if layers == {"published", "draft"}
                else "selected_published" if "published" in layers
                else "selected_draft" if "draft" in layers
                else "ancillary_or_detached"
            )
            row["source_projection"] = projection
            links_by_projection[projection][row["status"]] += 1
        summary = {
            "wrapper_depth": int(bool(self.prefix)),
            "regular_files": len(self.files),
            "parsed_xml_documents": len(self.xml),
            "alternate_run_documents": sum(path.startswith("course/") and node.tag == "course" and path != self.run_root
                                           for path, node in self.xml.items()),
            "published_definitions_by_kind": counts(known(kind) for (layer, _), kind in self.visited.items() if layer == "published"),
            "published_edges_by_status": counts(e["status"] for e in published_edges),
            "missing_published_extension_edges_by_kind": counts(e["kind"] for e in published_edges if e["status"] == "missing_extension_definition"),
            "reused_published_definition_count": sum(count > 1 for count in repeated.values()),
            "detached_published_documents_by_kind": dict(sorted(detached.items())),
            "draft_anchor_counts": counts(row["status"] for row in self.draft_anchors),
            "draft_definitions_by_kind": counts(known(kind) for (layer, _), kind in self.visited.items() if layer == "draft"),
            "draft_edges_by_status": counts(e["status"] for e in draft_edges),
            "draft_missing_extension_edges_by_kind": counts(e["kind"] for e in draft_edges if e["status"] == "missing_extension_definition"),
            "key_shapes": dict(sorted(key_formats.items())),
            "raw_key_count_multiple_kinds": sum(len({kind for kind, _ in owners}) > 1 for owners in self.block_key_locations.values()),
            "raw_key_count_multiple_layers": sum(len({layer for _, layer in owners}) > 1 for owners in self.block_key_locations.values()),
            "html_companions": html,
            "policies": policies,
            "static_files": sum(path.startswith("static/") for path in self.files),
            "nonmarkup_entries_not_read": sum(not path.endswith((".xml", ".html")) and not (path.startswith("policies/") and path.endswith(".json")) for path in self.files),
            "links_by_status": counts(row["status"] for row in self.links),
            "links_by_source_projection": {scope: dict(sorted(stats.items())) for scope, stats in sorted(links_by_projection.items())},
            "issues_by_code": counts(row["code"] for row in self.issues),
        }
        detail = {
            "source_scope": self.scope,
            "archive_wrapper": self.prefix,
            "selected_course_document": self.run_root,
            "selected_documents": sorted(self.selected),
            "edges": self.edges,
            "draft_anchors": self.draft_anchors,
            "links": self.links,
            "issues": self.issues,
        }
        return summary, detail


def private_report_path(output: Path, checkout: Path) -> Path:
    if not output.is_absolute() or output.is_symlink():
        raise AuditError("PRIVATE_REPORT_REQUIRES_SAFE_ABSOLUTE_PATH")
    destination = output.resolve()
    if destination.is_relative_to(checkout) or any((ancestor / ".git").exists() for ancestor in destination.parents):
        raise AuditError("PRIVATE_REPORT_PATH_IS_IN_CHECKOUT")
    if not destination.is_relative_to(Path(tempfile.gettempdir()).resolve()):
        raise AuditError("PRIVATE_REPORT_REQUIRES_TEMP_DIRECTORY")
    return destination


def write_private_report(destination: Path, details) -> None:
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    directory = os.open(destination.parent, flags)
    try:
        metadata = os.fstat(directory)
        if not stat.S_ISDIR(metadata.st_mode) or metadata.st_uid != os.geteuid() or metadata.st_mode & 0o077:
            raise AuditError("PRIVATE_REPORT_REQUIRES_OWNER_ONLY_DIRECTORY")
        output_flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(destination.name, output_flags, 0o600, dir_fd=directory), "w", encoding="utf-8") as output:
            json.dump({"archives": details}, output, indent=2, sort_keys=True)
            output.write("\n")
    finally:
        os.close(directory)


def audit(path: Path):
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0)
    with os.fdopen(os.open(path, flags), "rb") as source:
        metadata = os.fstat(source.fileno())
        if not stat.S_ISREG(metadata.st_mode) or metadata.st_size > ARCHIVE_BYTES:
            raise AuditError("ARCHIVE_MISSING_OR_SIZE_LIMIT")
        check_central_directory(source, metadata.st_size)
        with zipfile.ZipFile(source) as container:
            scanner = CourseAudit(container)
            summary, detail = scanner.run()
            return summary, detail, scanner.structural_keys


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archives", metavar="ARCHIVE", type=Path, nargs="+")
    parser.add_argument("--private-details", metavar="ABSOLUTE_TEMP_PATH", type=Path,
                        help="Write sensitive locators to a new mode 0600 file outside all detected Git checkouts.")
    options = parser.parse_args(argv)
    checkout = Path(__file__).resolve().parents[1]
    report, details, identities = [], [], Counter()
    try:
        destination = private_report_path(options.private_details, checkout) if options.private_details else None
        for index, path in enumerate(options.archives, start=1):
            try:
                summary, detail, keys = audit(path)
            except AuditError as error:
                report.append({"archive_index": index, "error_code": str(error)})
                continue
            except (OSError, zipfile.BadZipFile, RuntimeError, NotImplementedError, UnicodeError, EOFError):
                report.append({"archive_index": index, "error_code": "ARCHIVE_READ_REJECTED"})
                continue
            report.append({"archive_index": index, **summary})
            if destination:
                details.append({"archive_index": index, "archive_path": str(path), **detail})
            identities.update(keys)
        if destination:
            write_private_report(destination, details)
    except (AuditError, OSError) as error:
        code = str(error) if isinstance(error, AuditError) else "PRIVATE_REPORT_WRITE_REJECTED"
        print(json.dumps({"error_code": code}))
        return 2
    print(json.dumps({"archives": report, "shared_raw_kind_key_pairs": sum(n > 1 for n in identities.values())},
                     indent=2, sort_keys=True))
    return int(any("error_code" in row for row in report))


if __name__ == "__main__":
    sys.exit(main())
