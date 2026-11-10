"""Synthetic tests for the read-only course ZIP inventory diagnostic."""

from __future__ import annotations

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
import stat
import struct
import tempfile
import unittest
import warnings
import zipfile

import audit_curriculum_archive as scanner


SYNTHETIC = "synthetic-provenance-marker"
BASE = {
    "course.xml": '<course org="garden-lab" course="growth" url_name="spring"/>',
    "course/spring.xml": '<course><chapter url_name="basics"/></course>',
    "course/trial.xml": '<course><chapter url_name="basics"/></course>',
    "chapter/basics.xml": '<chapter><sequential url_name="measure"/></chapter>',
    "sequential/measure.xml": '<sequential><vertical url_name="sample"/></sequential>',
    "vertical/sample.xml": (
        '<vertical><html url_name="notes"/><html url_name="notes"/>'
        '<openassessment url_name="review"><rubric><criterion/></rubric></openassessment>'
        '<drag-and-drop-v2 url_name="position" x-is-pointer-node="true"/>'
        '<video url_name="conflict" x-is-pointer-node="true"><source/></video>'
        '</vertical>'
    ),
    "vertical/detached.xml": "<vertical/>",
    "html/notes.xml": '<html filename="notes"/>',
    "html/notes.html": (
        '<a href="/jump_to_id/sample#diagram">Diagram</a>'
        '<a href="/jump_to_id/detached">Detached</a>'
        '<a href="/jump_to_id/draft-a">Draft</a>'
        '<a href="/jump_to_id/unknown">Unknown</a>'
        '<a href="https://external.example/jump_to_id/sample?secret=token-example#private-fragment">External</a>'
        '<a href="https://usr:pass@credentials.example/content">Credential URL</a>'
        '<img src="/static/chart/line.svg">'
        '<img src="/static/chart%2fline.svg">'
    ),
    "static/chart/line.svg": '<svg xmlns="http://www.w3.org/2000/svg"/>',
    "drafts/vertical/draft-a.xml": (
        '<vertical parent_url="block-v1:garden-lab+growth+spring+type@sequential+block@measure" '
        'index_in_children_list="1"><problem url_name="question"/></vertical>'
    ),
    "drafts/vertical/draft-b.xml": (
        '<vertical parent_url="block-v1:garden-lab+growth+spring+type@sequential+block@measure" '
        'index_in_children_list="1"/>'
    ),
    "drafts/problem/question.xml": "<problem><label>Measure the seedling.</label></problem>",
    "policies/spring/policy.json": '{"course/spring":{"language":"en"}}',
    "policies/spring/grading_policy.json": '{"GRADER":[{}],"GRADE_CUTOFFS":{"Pass":0.75}}',
    "policies/trial/grading_policy.json": '{"GRADER":[]}',
    "assets/assets.xml": "<assets/>",
}


class AuditTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="course-audit-test-")
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)
        self.archive = self.directory / (SYNTHETIC + ".zip")

    def make_archive(self, entries, wrapper=SYNTHETIC):
        prefix = f"{wrapper}/" if wrapper else ""
        with zipfile.ZipFile(self.archive, "w", compression=zipfile.ZIP_DEFLATED) as container:
            for path, body in entries:
                if isinstance(path, zipfile.ZipInfo):
                    container.writestr(path, body)
                else:
                    container.writestr(prefix + path, body)

    def run_cli(self, *options):
        stream = StringIO()
        with redirect_stdout(stream):
            code = scanner.main([str(self.archive), *map(str, options)])
        output = stream.getvalue()
        self.assertNotIn(SYNTHETIC, output)
        return code, json.loads(output)

    def test_graph_and_private_report(self):
        self.make_archive(BASE.items())
        private = self.directory / "report.json"
        code, report = self.run_cli("--private-details", private)
        self.assertEqual(code, 0)
        row = report["archives"][0]
        self.assertEqual(row["alternate_run_documents"], 1)
        self.assertEqual(row["published_definitions_by_kind"]["openassessment"], 1)
        self.assertEqual(row["missing_published_extension_edges_by_kind"], {"drag-and-drop-v2": 1})
        self.assertEqual(row["published_edges_by_status"]["ambiguous_pointer_and_body"], 1)
        self.assertEqual(row["reused_published_definition_count"], 1)
        self.assertEqual(row["draft_anchor_counts"], {"reachable_parent": 2})
        self.assertEqual(row["issues_by_code"]["DRAFT_ORDINAL_COLLISION"], 1)
        self.assertEqual(row["policies"]["selected_grading_categories"], 1)
        self.assertEqual(row["links_by_status"], {
            "absolute_unit_route_needs_authority": 1,
            "asset_present": 1,
            "credential_uri": 1,
            "unit_detached": 1,
            "unit_in_selected_draft_only": 1,
            "unit_in_selected_published": 1,
            "unit_missing": 1,
            "unsafe_asset_path": 1,
        })
        self.assertEqual(row["links_by_source_projection"]["selected_published"], row["links_by_status"])
        self.assertEqual(stat.S_IMODE(private.stat().st_mode), 0o600)
        text = private.read_text()
        self.assertIn(SYNTHETIC, text)
        for removed in ["token-example", "private-fragment", "usr:pass", "credentials.example"]:
            self.assertNotIn(removed, text)
        self.assertEqual(self.run_cli("--private-details", private)[0], 2)

    def test_determinism_across_archive_order(self):
        self.make_archive(BASE.items())
        first = self.run_cli()
        self.make_archive(reversed(list(BASE.items())))
        self.assertEqual(self.run_cli(), first)

    def test_direct_inline_descriptor(self):
        self.make_archive([
            ("course.xml", '<course org="garden-lab" course="growth" url_name="spring"><chapter url_name="a"><sequential><vertical/></sequential></chapter></course>'),
        ], wrapper=None)
        code, report = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(report["archives"][0]["published_edges_by_status"], {"inline": 3})
        self.assertEqual(report["archives"][0]["wrapper_depth"], 0)

    def test_course_run_named_course_is_not_a_second_root(self):
        self.make_archive([
            ("course.xml", '<course org="garden-lab" course="growth" url_name="course"/>'),
            ("course/course.xml", "<course/>"),
        ], wrapper=None)
        code, report = self.run_cli()
        self.assertEqual(code, 0)
        self.assertEqual(report["archives"][0]["published_definitions_by_kind"], {"course": 1})

    def test_unsafe_paths_and_case_collision(self):
        for member, expected in [
            ("static/../hidden.xml", "UNSAFE_MEMBER_PATH"),
            ("static/%2e%2e/hidden.xml", "UNSAFE_ENCODED_MEMBER_PATH"),
            ("STATIC/other.html", "CASE_COLLIDING_MEMBER"),
            ("static", "FILE_DIRECTORY_COLLISION"),
        ]:
            with self.subTest(member=member):
                self.make_archive([*BASE.items(), (member, "unused")])
                code, report = self.run_cli()
                self.assertEqual(code, 1)
                self.assertEqual(report["archives"][0]["error_code"], expected)

    def test_duplicate_and_nonregular_members(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            self.make_archive([*BASE.items(), ("course.xml", BASE["course.xml"])])
        self.assertEqual(self.run_cli()[1]["archives"][0]["error_code"], "DUPLICATE_OR_AMBIGUOUS_MEMBER")
        link = zipfile.ZipInfo(f"{SYNTHETIC}/static/link")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.make_archive([*BASE.items(), (link, "target")])
        self.assertEqual(self.run_cli()[1]["archives"][0]["error_code"], "NONREGULAR_MEMBER")

    def test_xml_dtd_and_duplicate_policy_key(self):
        descriptor = (
            '<!DOCTYPE course [<!ENTITY marker "garden-lab">]>'
            '<course org="&marker;" course="growth" url_name="spring"/>'
        ).encode("utf-16")
        self.make_archive((path, descriptor if path == "course.xml" else body) for path, body in BASE.items())
        self.assertEqual(self.run_cli()[1]["archives"][0]["error_code"], "XML_DTD_OR_EXTERNAL_ENTITY")
        members = dict(BASE, **{"policies/spring/policy.json": '{"a":1,"a":2}'})
        self.make_archive(members.items())
        self.assertEqual(self.run_cli()[1]["archives"][0]["issues_by_code"]["INVALID_POLICY_JSON"], 1)

    def test_false_central_directory_count_rejected(self):
        self.make_archive(BASE.items())
        payload = bytearray(self.archive.read_bytes())
        footer = payload.rfind(b"PK\x05\x06")
        struct.pack_into("<HH", payload, footer + 8, 1, 1)
        self.archive.write_bytes(payload)
        self.assertEqual(self.run_cli()[1]["archives"][0]["error_code"], "CENTRAL_DIRECTORY_ENTRY_COUNT_MISMATCH")

    def test_private_report_rejects_public_directory_and_checkout(self):
        self.make_archive(BASE.items())
        shared = self.directory / "shared"
        shared.mkdir(mode=0o755)
        public_destination = shared / "report.json"
        code, result = self.run_cli("--private-details", public_destination)
        self.assertEqual((code, result["error_code"]), (2, "PRIVATE_REPORT_REQUIRES_OWNER_ONLY_DIRECTORY"))
        self.assertFalse(public_destination.exists())
        repository_destination = Path(scanner.__file__).resolve().parents[1] / "private-fixture-report.json"
        code, result = self.run_cli("--private-details", repository_destination)
        self.assertEqual((code, result["error_code"]), (2, "PRIVATE_REPORT_PATH_IS_IN_CHECKOUT"))
        self.assertFalse(repository_destination.exists())


if __name__ == "__main__":
    unittest.main()
