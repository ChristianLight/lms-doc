#!/usr/bin/env python3
"""Pack and check the synthetic course, libraries and SCORM samples."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import tarfile
import tomllib
import zipfile
from decimal import Decimal
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
XML_BASE = "{http://www.w3.org/XML/1998/namespace}base"
PROFILES = {
    "fraction-course.tar.gz": ("olx/course", "tar"),
    "fraction-legacy-library.tar.gz": ("olx/legacy-library", "tar"),
    "fraction-versioned-library.zip": ("olx/versioned-library", "zip"),
    "fraction-scorm-12.zip": ("scorm/1.2", "zip"),
    "fraction-scorm-2004-4.zip": ("scorm/2004.4", "zip"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def entries(directory: Path) -> list[tuple[str, bytes]]:
    return [
        (path.relative_to(directory).as_posix(), path.read_bytes())
        for path in sorted(directory.rglob("*"))
        if path.is_file() and not path.is_symlink()
    ]


def archive(files: list[tuple[str, bytes]], kind: str) -> bytes:
    result = io.BytesIO()
    if kind == "zip":
        with zipfile.ZipFile(result, "w") as container:
            for path, content in files:
                metadata = zipfile.ZipInfo(path, date_time=(2020, 1, 1, 0, 0, 0))
                metadata.external_attr = 0o100644 << 16
                container.writestr(metadata, content, compress_type=zipfile.ZIP_DEFLATED)
    else:
        with gzip.GzipFile(filename="", fileobj=result, mode="wb", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w") as container:
                for path, content in files:
                    metadata = tarfile.TarInfo(path)
                    metadata.size = len(content)
                    container.addfile(metadata, io.BytesIO(content))
    return result.getvalue()


def unpack(payload: bytes, kind: str) -> dict[str, bytes]:
    source = io.BytesIO(payload)
    if kind == "zip":
        with zipfile.ZipFile(source) as container:
            return {path: container.read(path) for path in container.namelist()}
    with tarfile.open(fileobj=source, mode="r:gz") as container:
        result = {}
        for item in container:
            member = container.extractfile(item)
            require(member is not None, f"Expected a fixture file at {item.name}")
            result[item.name] = member.read()
        return result


def check_course(files: dict[str, bytes]) -> dict[str, object]:
    descriptor = ET.fromstring(files["course.xml"])
    key = descriptor.attrib["url_name"]
    root = ET.fromstring(files[f"course/{key}.xml"])
    order = []

    def visit(node: ET.Element) -> None:
        for child in node:
            item = child.attrib["url_name"]
            order.append(f"{child.tag}/{item}")
            if child.tag in {"chapter", "sequential", "vertical"}:
                visit(ET.fromstring(files[f"{child.tag}/{item}.xml"]))

    visit(root)
    require(
        order == ["chapter/fundamentals", "sequential/ratio", "vertical/equivalence", "html/intro", "problem/nearest"],
        "Course tree or order changed",
    )
    html = files["html/intro.html"].decode()
    units = {item.split("/", 1)[1] for item in order if item.startswith("vertical/")}
    links = set(re.findall(r'href="/jump_to_id/([^"]+)"', html))
    require(links - units == {"missing-page"}, "Expected exactly one unresolved unit reference")
    require("static/fraction.svg" in files, "Missing required shared asset")
    problem = ET.fromstring(files["problem/nearest.xml"]).find("numericalresponse")
    require(problem is not None, "Fixture needs numeric response")
    tolerance = Decimal(problem.find("responseparam").attrib["default"])
    target = Decimal(problem.attrib["answer"])
    probes = ["0.4899", "0.49", "0.50", "0.51", "0.5101"]
    outcomes = [abs(Decimal(probe) - target) <= tolerance for probe in probes]
    require(outcomes == [False, True, True, True, False], "Tolerance boundaries changed")
    draft = ET.fromstring(files["drafts/vertical/draft-only.xml"])
    require(draft.attrib["index_in_children_list"] == "1" and "vertical/draft-only" not in order, "Draft leaked into published order")
    return {"ordered_objects": order, "unresolved_units": sorted(links - units), "numeric_responses": dict(zip(probes, outcomes))}


def check_libraries(legacy: dict[str, bytes], versioned: dict[str, bytes]) -> dict[str, object]:
    library = ET.fromstring(legacy["library.xml"])
    members = [child.attrib["url_name"] for child in library.findall("problem")]
    require(members == ["half"] and "problem/half.xml" in legacy, "Legacy bank is not resolvable")
    header = tomllib.loads(versioned["package.toml"].decode())
    require(header["meta"]["format_version"] == 1, "Unexpected modern archive profile")
    component = "entities/xblock.v1/html/fractions"
    meta = tomllib.loads(versioned[component + ".toml"].decode())
    published = meta["entity"]["published"]["version_num"]
    draft = meta["entity"]["draft"]["version_num"]
    require((published, draft) == (1, 2), "Library version pointers changed")
    digests = []
    for version in (published, draft):
        directory = f"{component}/component_versions/v{version}"
        block = ET.fromstring(versioned[directory + "/block.xml"])
        require('/static/model.svg' in block.text, f"Version {version} should resolve a scoped asset")
        digests.append(hashlib.sha256(versioned[directory + "/static/model.svg"]).hexdigest())
    require(digests[0] != digests[1], "Asset paths in two versions must point to different fixture bytes")
    collection = tomllib.loads(versioned["collections/fractions.toml"].decode())["collection"]
    require(collection["entities"] == ["unit-sample", "xblock.v1:html:fractions"], "Collection membership changed")
    return {"legacy_members": members, "published_revision": published, "draft_revision": draft, "asset_digests": digests}


def check_scorm(files: dict[str, bytes], edition: str) -> dict[str, object]:
    root = ET.fromstring(files["imsmanifest.xml"])
    namespace = {"c": root.tag.partition("}")[0].removeprefix("{")}
    resources = root.find("c:resources", namespace)
    organizations = root.find("c:organizations", namespace)
    require(resources is not None and organizations is not None, "Missing CAM structures")
    organization = organizations.find("c:organization", namespace)
    require(organization is not None and organizations.get("default") == organization.get("identifier"), "Default organization must resolve")
    items = organization.findall("c:item", namespace)
    by_resource = {resource.attrib["identifier"]: resource for resource in resources}
    resource_ids = [item.attrib["identifierref"] for item in items]
    if edition == "2004.4":
        require(len(items) == 2 and len(set(resource_ids)) == 1, "Expected two distinct occurrences sharing one resource")
    for resource in resources:
        base = PurePosixPath(root.get(XML_BASE, ""), resources.get(XML_BASE, ""), resource.get(XML_BASE, ""))
        for file_ref in resource.findall("c:file", namespace):
            file_path = (base / file_ref.attrib["href"]).as_posix()
            require(file_path in files, f"Missing declared resource file {file_path}")
        for dependency in resource.findall("c:dependency", namespace):
            require(dependency.attrib["identifierref"] in by_resource, "Unresolved CAM dependency")
    return {"edition": edition, "items": [item.attrib["identifier"] for item in items], "resource_ids": resource_ids}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional directory for verified test archives.")
    options = parser.parse_args()
    packed = {}
    unpacked = {}
    for name, (directory, kind) in PROFILES.items():
        source = entries(ROOT / directory)
        blob = archive(source, kind)
        require(blob == archive(source, kind), f"Non-deterministic fixture archive: {name}")
        expanded = unpack(blob, kind)
        require(expanded == dict(source), f"Archive round-trip changed bytes: {name}")
        packed[name] = blob
        unpacked[name] = expanded
    report = {
        "course": check_course(unpacked["fraction-course.tar.gz"]),
        "libraries": check_libraries(unpacked["fraction-legacy-library.tar.gz"], unpacked["fraction-versioned-library.zip"]),
        "scorm": [
            check_scorm(unpacked["fraction-scorm-12.zip"], "1.2"),
            check_scorm(unpacked["fraction-scorm-2004-4.zip"], "2004.4"),
        ],
        "archive_sha256": {name: hashlib.sha256(blob).hexdigest() for name, blob in packed.items()},
    }
    if options.output:
        options.output.mkdir(parents=True, exist_ok=True)
        for name, blob in packed.items():
            (options.output / name).write_bytes(blob)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
