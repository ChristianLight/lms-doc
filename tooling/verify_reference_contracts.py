#!/usr/bin/env python3
"""Verify original reference-index schema and complete-generation contract vectors.

This does not exercise a database, authorization provider or concurrent application.
"""

import copy
import hashlib
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from specification import load_catalogs, schema_for_entity

ROOT = Path(__file__).resolve().parents[1]
TARGET_COLUMNS = {
    "asset": "asset_version_id",
    "content_definition": "content_node_version_id",
    "activity_definition": "activity_version_id",
    "assessment": "assessment_version_id",
    "package": "package_version_id",
    "external_resource": "external_resource_map_id",
    "placement": "target_placement_id",
    "placement_selector": "target_selector",
}


def entries_digest(entries):
    rows = []
    for entry in sorted(entries, key=lambda item: item["reference_key"]):
        target = entry[TARGET_COLUMNS[entry["relation"]]]
        if entry["relation"] == "placement_selector":
            target = [target["placement_key"], target["context"]]
        rows.append([
            entry["reference_key"], entry["relation"], target,
            entry.get("anchor", ""), entry["required_for_publication"],
        ])
    payload = json.dumps(rows, separators=(",", ":"), ensure_ascii=False).encode()
    return hashlib.sha256(payload).hexdigest()


def validate_bundle(reference_set, entries, validators):
    validators["ContentReferenceSet"].validate(reference_set)
    if reference_set["state"] != "ready":
        raise ValueError("coverage is not ready")
    keys = set()
    for entry in entries:
        validators["ContentReference"].validate(entry)
        if entry["set_id"] != reference_set["id"]:
            raise ValueError("entry belongs to another set")
        if entry["generation"] != reference_set["generation"]:
            raise ValueError("entry generation differs from ready set")
        key = entry["reference_key"]
        if key in keys:
            raise ValueError("duplicate semantic key")
        keys.add(key)
        if hashlib.sha256(key.encode()).hexdigest() != entry["reference_key_digest"]:
            raise ValueError("semantic key digest differs")
        if reference_set["context_kind"] == "placement" and entry["relation"] == "placement_selector":
            raise ValueError("unresolved selector in placement binding")
        if reference_set["context_kind"] == "definition" and entry["relation"] == "placement":
            raise ValueError("exact placement substituted into reusable definition")
    if reference_set["context_kind"] == "placement":
        if reference_set["context_key"] != reference_set["source_placement_id"]:
            raise ValueError("placement context key differs")
    if len(entries) != reference_set["entry_count"]:
        raise ValueError("incomplete reference generation")
    if entries_digest(entries) != reference_set["entries_digest"]:
        raise ValueError("semantic entries digest differs")


def main():
    entities = {
        entity["name"]: entity
        for _, catalog in load_catalogs()
        for entity in catalog["entities"]
    }
    validators = {
        name: Draft202012Validator(schema_for_entity(entities[name]), format_checker=FormatChecker())
        for name in ("ContentReferenceSet", "ContentReference")
    }
    vectors = json.loads((ROOT / "specification/persistence/reference-contract-vectors.json").read_text())
    valid = invalid = 0
    for vector in vectors["cases"]:
        try:
            validate_bundle(copy.deepcopy(vector["set"]), copy.deepcopy(vector["entries"]), validators)
        except (ValidationError, ValueError) as exc:
            if vector["valid"]:
                raise AssertionError(f"Valid fixture {vector['name']} rejected: {exc}") from exc
            invalid += 1
        else:
            if not vector["valid"]:
                raise AssertionError(f"Invalid fixture {vector['name']} accepted")
            valid += 1
    print(f"Verified {valid} valid and {invalid} invalid original relationship contract vectors.")
    print("Scope: schemas, typed targets, semantic digests and complete generations; database races require implementation tests.")


if __name__ == "__main__":
    main()
