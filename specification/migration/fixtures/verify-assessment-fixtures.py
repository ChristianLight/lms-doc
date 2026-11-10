#!/usr/bin/env python3
"""Verify synthetic assessment extraction and compatibility witnesses."""

import json
import re
import sys
from collections import Counter
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path
from xml.etree import ElementTree


FIXTURES = Path(__file__).resolve().parent
RESPONSE_FAMILIES = {
    "multiplechoiceresponse": "single_choice",
    "choiceresponse": "multiple_choice",
    "optionresponse": "single_choice",
    "stringresponse": "short_text",
    "numericalresponse": "math",
    "formularesponse": "math",
}
PRIVATE_TAGS = {"solution", "choicehint", "demandhint", "additional_answer", "responseparam", "script"}


class FixtureError(ValueError):
    """A checked witness is malformed or disagrees with the frozen expected result."""


def equal(actual, expected, label):
    if actual != expected:
        raise FixtureError(f"{label}: expected {expected!r}, received {actual!r}")


def parse_fixture():
    source = (FIXTURES / "assessment-extraction.xml").read_bytes()
    if len(source) > 65536 or re.search(br"<!\s*(?:DOCTYPE|ENTITY)", source, re.IGNORECASE):
        raise FixtureError("unsafe synthetic fixture XML")
    return ElementTree.fromstring(source)


def public_text(node):
    """Drop protected child content while preserving each child's public tail."""
    pieces = [node.text or ""]
    for child in node:
        if child.tag not in PRIVATE_TAGS:
            pieces.append(public_text(child))
        pieces.append(child.tail or "")
    return "".join(pieces)


def choice_rows(group):
    return [
        {
            "key": f"choice_{ordinal:02d}",
            "label": " ".join(public_text(choice).split()),
            "fixed": choice.get("fixed", "false").lower() == "true",
        }
        for ordinal, choice in enumerate(group.findall("choice"), 1)
    ]


def rubric_projection(open_response):
    rubric = open_response.find("rubric")
    maxima = [
        max((Decimal(level.attrib["points"]) for level in criterion.findall("option")), default=Decimal(0))
        for criterion in rubric.findall("criterion")
    ]
    return {
        "text": open_response.get("text_response", "disabled"),
        "files": open_response.get("file_upload_response", "disabled"),
        "score_maximum": str(sum(maxima)),
        "steps": [step.attrib["name"] for step in open_response.findall("./assessments/assessment")],
        "rubric_visible_during_response": open_response.get("show_rubric_during_response", "false").lower() == "true",
    }


def verify_structure(root, expected):
    equal(len(root), expected["component_count"], "component count")
    composite = root.find("./problem[@url_name='synthetic-garden-gauge']")
    controls = [node for node in composite.iter() if node.tag in RESPONSE_FAMILIES]
    parents = {child: parent for parent in composite.iter() for child in parent}
    equal([RESPONSE_FAMILIES[node.tag] for node in controls], expected["composite_interactions"], "response/control order")
    equal([parents[node].tag for node in controls], expected["composite_control_context"], "response context")
    equal(choice_rows(controls[1].find("choicegroup")), expected["choices"], "choice identity and visible label")
    equal(controls[0].find("formulaequationinput").get("trailing_text"), expected["numeric_trailing_text"], "presentation suffix")
    partition = expected["public_private_partition"]
    equal(controls[0].tail.strip(), partition["public_after_control"], "public tail after control")
    equal(next(composite.iter("solution")).tail.strip(), partition["public_after_solution"], "public tail after protected solution")
    visible = public_text(composite)
    for tag in ("solution", "choicehint", "hint"):
        for node in composite.iter(tag):
            protected = " ".join("".join(node.itertext()).split())
            if protected and protected in " ".join(visible.split()):
                raise FixtureError(f"protected {tag} content leaked into candidate text")
    actual_counts = Counter(
        model_solution=len(list(composite.iter("solution"))),
        choice_selected=len(list(composite.iter("choicehint"))),
        on_demand=len(list(composite.iter("hint"))),
    )
    equal(dict(actual_counts), partition["private_rule_counts"], "private feedback classification")
    open_responses = root.findall("openassessment")
    equal([rubric_projection(node) for node in open_responses], expected["rubric_projections"], "inline rubric, requirements and workflows")
    missing = sum(
        node.tag == "drag-and-drop-v2" and not list(node) and bool(node.get("url_name"))
        for node in root
    )
    equal(missing, expected["missing_dependency_count"], "unresolved typed reference")
    return composite


def verify_decision_count(composite, rows):
    options = composite.find("choiceresponse/checkboxgroup").findall("choice")
    universe = {f"choice_{ordinal:02d}" for ordinal in range(1, len(options) + 1)}
    correct = {
        f"choice_{ordinal:02d}"
        for ordinal, choice in enumerate(options, 1)
        if choice.get("correct", "false").lower() == "true"
    }
    for row in rows:
        selected = set(row["selected"])
        if len(selected) != len(row["selected"]) or not selected <= universe:
            raise FixtureError("invalid selection keys")
        matches = len(selected & correct) + len((universe - correct) - selected) if selected else 0
        points = (Decimal(matches) / Decimal(len(universe))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        status = "correct" if matches == len(universe) else "partial" if matches else "incorrect"
        equal(points, Decimal(row["points"]), f"decision-count points for {sorted(selected)}")
        equal(status, row["status"], f"decision-count status for {sorted(selected)}")


def verify_numeric(composite, vectors):
    source = next(composite.iter("numericalresponse"))
    primary = Fraction(source.attrib["answer"])
    alternate = Fraction(source.find("additional_answer").attrib["answer"])
    tolerance = Fraction(source.find("responseparam").attrib["default"])
    for row in vectors["numeric"]:
        candidate = Fraction(row["candidate"])
        match = "primary" if abs(candidate - primary) <= tolerance else "alternate" if candidate == alternate else "none"
        equal(match, row["match"], f"numeric match for {candidate}")
        equal(match != "none", row["accepted"], f"numeric acceptance for {candidate}")
    for row in vectors["explicit_percentage"]:
        expected = Fraction(row["expected"])
        candidate = Fraction(row["candidate"])
        tolerance = Fraction(row["tolerance"]) * abs(expected) / 100
        equal(abs(candidate - expected) <= tolerance, row["accepted"], f"percent tolerance for {candidate}")


def parse_sample_profile(source):
    match = re.fullmatch(r"([A-Za-z,]+)@([0-9,]+):([0-9,]+)#([0-9]{1,2})", source)
    if not match:
        return None
    symbols, low_values, high_values, count = match.groups()
    names = symbols.split(",")
    low = low_values.split(",")
    high = high_values.split(",")
    if len(names) != len(set(names)) or len(names) != len(low) or len(names) != len(high):
        return None
    return names, low, high, int(count)


def verify_formula(root, expected):
    correct = root.find("./problem[@url_name='synthetic-expression-sampler']/formularesponse")
    profile = parse_sample_profile(correct.attrib["samples"])
    if profile is None:
        raise FixtureError("synthetic sample profile did not parse")
    names, low, high, count = profile
    equal(low, high, "fixed sample bounds")
    points = [dict(zip(names, low)) for _ in range(count)]
    equal(points, expected["fixed_valid_points"], "repeated fixed points")

    # The one synthetic fixture uses one bounded addition. This is an arithmetic witness,
    # not a general expression evaluator or a source RNG implementation.
    expression = re.fullmatch(r"([A-Za-z]{1,8})\+([0-9]{1,6})", correct.attrib["answer"])
    if expression is None:
        raise FixtureError("synthetic reference expression exceeds the fixture grammar")
    symbol, offset = expression.groups()
    constant = Fraction(expected["constant_candidate"])
    equal(
        all(Fraction(point[symbol]) + int(offset) == constant for point in points),
        expected["accepted_at_fixed_points"],
        "fixed-point witness",
    )
    equal(Fraction(points[0][symbol]) + 1 + int(offset) == constant, expected["matches_different_point"], "different point witness")
    invalid = root.find("./problem[@url_name='synthetic-invalid-sample-dimensions']/formularesponse")
    equal("blocked" if parse_sample_profile(invalid.attrib["samples"]) is None else "parsed", expected["bad_dimensions_disposition"], "malformed sample bounds")


def verify_text(root, expected):
    literal, alternate, unsafe = root.findall("./problem[@url_name='synthetic-text-checks']/stringresponse")
    for row in expected["literal_witnesses"]:
        actual = row["candidate"].strip().lower() == literal.attrib["answer"].strip().lower()
        equal(actual, row["source_match"], "literal lowercase comparison")
    alternatives = alternate.attrib["answer"].split("|")
    if len(alternatives) != 2 or not all(re.fullmatch(r"[A-Za-z]{1,32}", word) for word in alternatives):
        raise FixtureError("synthetic legacy-alternation witness exceeds the fixture grammar")
    first, last = alternatives
    witness = expected["legacy_alternation_witness"]
    candidate = witness["candidate"]
    equal(candidate.startswith(first) or candidate.endswith(last), witness["source_match"], "legacy alternate anchor")
    equal(candidate in alternatives, witness["whole_string_match"], "whole-string alternative")
    # Identify the unsupported syntax as data. Never compile or execute the source pattern.
    disposition = "blocked" if re.search(r"\\[1-9]", unsafe.attrib["answer"]) else "parsed"
    equal(disposition, expected["backreference_disposition"], "backreference quarantine")


def verify_contributions(composite, vectors):
    for row in vectors["contributions"]:
        raw_earned, raw_maximum = Fraction(row["raw_earned"]), Fraction(row["raw_maximum"])
        possible = raw_maximum if row["explicit_weight"] is None else Fraction(row["explicit_weight"])
        earned = raw_earned * possible / raw_maximum
        equal((earned, possible), (Fraction(row["earned"]), Fraction(row["possible"])), "raw-to-counted scale")
        equal(possible > 0, row["counted"], "zero-weight contribution")
    equal(Decimal(composite.attrib["weight"]), Decimal(0), "synthetic source explicit zero weight")
    equal(composite.attrib["showanswer"], "after_all_attempts_or_correct", "synthetic source answer policy")
    maximum_attempts = int(composite.attrib["max_attempts"])
    for row in vectors["release"]:
        reveal = row["admitted_attempts"] >= maximum_attempts or row["correct"]
        equal(reveal, row["reveal"], "answer key disclosure gate")


def main():
    try:
        root = parse_fixture()
        vectors = json.loads((FIXTURES / "assessment-parity.json").read_text(encoding="utf-8"))
        equal(vectors["fixture_version"], "1.0.0", "fixture version")
        composite = verify_structure(root, vectors["structure"])
        verify_decision_count(composite, vectors["decision_count"])
        verify_numeric(composite, vectors)
        verify_formula(root, vectors["formula_samples"])
        verify_text(root, vectors["text"])
        verify_contributions(composite, vectors)
    except (OSError, ValueError, TypeError, KeyError, AttributeError, ElementTree.ParseError) as error:
        print(f"Assessment migration fixture failed: {error}", file=sys.stderr)
        return 1
    print("Verified synthetic assessment layout, private feedback partition and rubric workflows.")
    print("Verified decision-count, tolerance, formula witnesses, text matching and unsafe pattern disposition.")
    print("Verified positive, absent and zero grade contribution and answer-release gates.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
