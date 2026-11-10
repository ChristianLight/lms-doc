#!/usr/bin/env python3
"""Check independently invented protected export artifact and command shapes."""

from copy import deepcopy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


def identifier(number):
    return f"00000000-0000-4000-8000-{number:012d}"


def test_export_projections():
    base = Path(__file__).resolve().parent.parent
    schema = json.loads((base / "export-projection.schema.json").read_text(encoding="utf-8"))
    catalog = json.loads((base / "catalog.json").read_text(encoding="utf-8"))
    commands = {item["name"]: item for item in catalog["commands"]}
    queue = commands["QueueCurriculumExport"]
    choice = queue["request_examples"][0]
    digest = "a" * 64
    root = choice["root_version_ids"][0]
    common = {"schema_version": 1, "job_id": identifier(40), "institution_id": identifier(41)}
    docs = {
        "selection": {
            **common,
            "document_type": "selection",
            "selection": {
                **choice,
                "roots": [{"owner_kind": "CourseVersion", "revision_id": root, "projection_digest": digest}],
                "dependencies": [],
                "rights_decision_refs": [identifier(42)],
                "policy_snapshot_refs": [identifier(43)],
                "generator_build": "portable-4ed-v1",
            },
        },
        "capability_report": {
            **common,
            "document_type": "capability_report",
            "selection_digest": digest,
            "profile_revision": 1,
            "generator_build": "portable-4ed-v1",
            "coverage": [{
                "capability_key": "scorm.resume/1",
                "root_revision_id": root,
                "required": True,
                "status": "equivalent_projection",
            }],
        },
        "loss_report": {
            **common,
            "document_type": "loss_report",
            "selection_digest": digest,
            "capability_report_digest": "b" * 64,
            "losses": [],
        },
        "output_validation": {
            **common,
            "document_type": "output_validation",
            "selection_digest": digest,
            "profile_revision": 1,
            "generator_build": "portable-4ed-v1",
            "format": "scorm_2004_4",
            "edition": "scorm_2004_4",
            "output_sha256": "c" * 64,
            "output_byte_length": 48000,
            "checked_at": "2027-04-15T10:00:00Z",
            "checks": [{
                "check_key": "rte.resume",
                "runner_build": "independent-reference-v1",
                "status": "passed",
                "evidence_ref": identifier(44),
            }],
        },
    }
    Draft202012Validator.check_schema(schema)
    verify = Draft202012Validator(schema, format_checker=FormatChecker())
    for document in docs.values():
        verify.validate(document)
    wrong_edition = {**docs["output_validation"], "edition": "scorm_1_2"}
    assert not verify.is_valid(wrong_edition)
    contradicting_disclosure = deepcopy(docs["selection"])
    contradicting_disclosure["selection"]["include_answers"] = True
    assert not verify.is_valid(contradicting_disclosure)
    leaking_manifest = deepcopy(docs["loss_report"])
    leaking_manifest["source_answer_key"] = "synthetic forbidden field"
    assert not verify.is_valid(leaking_manifest)

    queue_verify = Draft202012Validator(queue["request_schema"], format_checker=FormatChecker())
    assert not queue_verify.is_valid({**choice, "format": "scorm_2004_unverified"})
    assert not queue_verify.is_valid({**choice, "edition": "scorm_1_2"})
    build = commands["BuildTransferPlan"]
    plan = {**build["request_examples"][0], "selected_root_keys": ["training-a", "training-b"]}
    plan_verify = Draft202012Validator(build["request_schema"], format_checker=FormatChecker())
    assert not plan_verify.is_valid(plan)
    plan_verify.validate({**plan, "root_commit_policy": "atomic_selected_closure"})
    print("Protected export projection and atomic root-selection fixtures passed.")


if __name__ == "__main__":
    test_export_projections()
