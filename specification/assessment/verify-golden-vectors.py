#!/usr/bin/env python3
"""Check the assessment fixture bytes, hashes, rank orders and exact arithmetic."""

import argparse
import hashlib
import hmac
import json
import re
import struct
import sys
import uuid
from collections import Counter
from fractions import Fraction
from pathlib import Path


class FixtureError(ValueError):
    """A checked fixture is invalid or disagrees with its expected result."""


def require(condition, label):
    if not condition:
        raise FixtureError(label)


def equal(actual, expected, label):
    if actual != expected:
        raise FixtureError(f"{label}: expected {expected!r}, received {actual!r}")


def length_prefixed(value):
    encoded = value.encode("utf-8")
    return struct.pack(">I", len(encoded)) + encoded


def verify_manifest(vector):
    manifest = vector["logical_input"]
    equal(set(manifest), {"attempt", "choices", "points", "revision"}, "manifest shape")
    equal(str(uuid.UUID(manifest["attempt"])), manifest["attempt"], "manifest attempt UUID")
    require(
        isinstance(manifest["choices"], list)
        and all(isinstance(choice, str) and choice.isascii() for choice in manifest["choices"]),
        "manifest choices must be a list of ASCII strings",
    )
    decimal(manifest["points"])
    require(type(manifest["revision"]) is int and 0 < manifest["revision"] < 2**53, "manifest revision is outside the exact integer range")
    # This fixed schema uses ASCII property names, exact integers and decimal strings.
    # Sorted compact JSON has the JCS bytes for that restricted input shape.
    encoded = json.dumps(manifest, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    equal(encoded.hex(), vector["expected_utf8_hex"], "canonical manifest bytes")
    equal(hashlib.sha256(encoded).hexdigest(), vector["expected_sha256_hex"], "canonical manifest SHA-256")


def verify_rank(seed, message, row, label):
    equal(message.hex(), row["message_hex"], f"{label} message bytes")
    digest = hmac.digest(seed, message, "sha256")
    equal(digest.hex(), row["hmac_sha256_hex"], f"{label} HMAC-SHA256")
    return digest


def verify_pool(seed, vector):
    candidates = {name: uuid.UUID(value).bytes for name, value in vector["candidate_ids"].items()}
    slots = vector["ordered_candidates"]
    rows = vector["rank_inputs"]
    require(candidates and slots, "pool requires candidates and slots")
    equal(len(set(candidates.values())), len(candidates), "distinct pool candidate identities")
    equal(set(rows), {f"{slot}/{candidate}" for slot in slots for candidate in candidates}, "pool rank coverage")
    occurrence = struct.pack(">I", vector["occurrence"])
    for slot, expected_order in slots.items():
        prefix = length_prefixed("item-pool-v1") + length_prefixed(slot) + occurrence
        ranks = {
            candidate: verify_rank(seed, prefix + candidate_id, rows[f"{slot}/{candidate}"], f"pool {slot}/{candidate}")
            for candidate, candidate_id in candidates.items()
        }
        actual_order = sorted(candidates, key=lambda candidate: (ranks[candidate], candidates[candidate]))
        equal(actual_order, expected_order, f"pool {slot} order")
    return len(rows)


def verify_choices(seed, vector):
    rows = vector["rank_inputs"]
    require(rows, "choice order requires candidates")
    prefix = (
        length_prefixed("choice-order-v1")
        + uuid.UUID(vector["attempt_item_id"]).bytes
        + length_prefixed(vector["interaction_key"])
    )
    ranks = {
        key: verify_rank(seed, prefix + length_prefixed(key), row, f"choice {key}")
        for key, row in rows.items()
    }
    equal(sorted(ranks, key=lambda key: (ranks[key], key)), vector["expected_order"], "choice order")
    return len(rows)


def decimal(value):
    require(
        isinstance(value, str) and re.fullmatch(r"-?[0-9]{1,64}(\.[0-9]{1,64})?", value),
        "expected a bounded decimal literal",
    )
    return Fraction(value)


def rational(pair):
    require(
        isinstance(pair, list)
        and len(pair) == 2
        and all(isinstance(part, str) and re.fullmatch(r"-?[0-9]{1,64}", part) for part in pair),
        "expected a bounded rational pair",
    )
    numerator, denominator = map(int, pair)
    require(denominator > 0, "rational denominator must be positive")
    value = Fraction(numerator, denominator)
    equal((value.numerator, value.denominator), (numerator, denominator), "reduced rational pair")
    return value


def ast_value(tree, depth=0):
    require(depth < 32 and isinstance(tree, list) and tree, "invalid or over-deep fixture AST")
    operation, *operands = tree
    if operation in {"integer", "decimal"} and len(operands) == 1:
        value = decimal(operands[0])
        if operation == "integer":
            require("." not in operands[0], "integer AST literal contains decimal punctuation")
        return value
    if operation == "neg" and len(operands) == 1:
        return -ast_value(operands[0], depth + 1)
    if operation == "pow" and len(operands) == 2:
        base, exponent = (ast_value(operand, depth + 1) for operand in operands)
        require(exponent.denominator == 1 and abs(exponent) <= 64, "fixture exponent outside integer bounds")
        bits = max(base.numerator.bit_length(), base.denominator.bit_length())
        require(bits * abs(exponent) <= 4096, "fixture exponentiation exceeds the arithmetic budget")
        return base ** int(exponent)
    raise FixtureError(f"unsupported fixture AST node {operation!r} or arity")


def verify_parser_expectations(rows):
    ast_count = diagnostic_count = 0
    for row in rows:
        source = row["input"]
        require(isinstance(source, str) and 0 < len(source) <= 2048, "parser fixture input length")
        if "expected_ast" in row:
            equal(ast_value(row["expected_ast"]), rational(row["value_rational"]), f"fixture AST value for {source!r}")
            if "original_decimal_places" in row:
                require(row["profile"] == "math-decimal-comma-v1" and "," in source, "precision fixture requires decimal-comma profile")
                equal(len(source.rsplit(",", 1)[1]), row["original_decimal_places"], "original decimal places")
            ast_count += 1
        else:
            offset = row["expected_error_start_scalar"]
            require(type(offset) is int and 0 <= offset < len(source), "diagnostic offset outside original Unicode input")
            anchors = {
                "FUNCTION_ARITY_UNSUPPORTED": "log",
                "UNSUPPORTED_TOKEN": ".",
                "UNEXPECTED_SEPARATOR": ",",
            }
            token = anchors.get(row["expected_error"])
            require(token is not None and source.startswith(token, offset), f"diagnostic anchor for {source!r}")
            diagnostic_count += 1
    require(ast_count and diagnostic_count, "parser fixtures require AST and diagnostic vectors")
    return ast_count, diagnostic_count


def verify_scores(rows):
    counts = Counter()
    for number, row in enumerate(rows, 1):
        kind = row["kind"]
        label = f"score vector {number} ({kind})"
        if kind == "numerical_tolerance":
            expected = decimal(row["expected"])
            difference = abs(decimal(row["candidate"]) - expected)
            tolerance = max(decimal(row["abs_tol"]), decimal(row["rel_tol"]) * abs(expected))
            actual = difference <= tolerance if row["inclusive"] else difference < tolerance
            equal(actual, row["expected_acceptance"], label)
        elif kind == "unit_conversion":
            equal((row["from_unit"], row["to_unit"]), ("km/h", "m/s"), f"{label} unit profile")
            equal(decimal(row["candidate"]) * 1000 / 3600, rational(row["exact_rational"]), label)
        elif kind == "affine_conversion":
            equal((row["from_unit"], row["to_unit"]), ("Cel", "K"), f"{label} unit profile")
            offset = {"quantity": Fraction(27315, 100), "difference": Fraction(0)}[row["temperature_mode"]]
            equal(decimal(row["candidate"]) + offset, rational(row["exact_rational"]), label)
        elif kind == "partial_select":
            selected = row["selected"]
            equal(len(selected), len(set(selected)), f"{label} unique choices")
            awarded = sum(decimal(row["choice_weights"][choice]) for choice in selected)
            bounded = max(decimal(row["floor"]), min(decimal(row["cap"]), awarded))
            equal(bounded, decimal(row["expected_points"]), label)
        elif kind == "normalized_slot":
            maximum = decimal(row["item_maximum"])
            require(maximum > 0, f"{label} requires a positive item maximum")
            awarded = decimal(row["item_earned"]) * decimal(row["slot_maximum"]) / maximum
            equal(awarded, decimal(row["expected_points"]), label)
        else:
            raise FixtureError(f"unknown score vector family {kind!r}")
        counts[kind] += 1
    equal(
        set(counts),
        {"numerical_tolerance", "unit_conversion", "affine_conversion", "partial_select", "normalized_slot"},
        "score vector families",
    )
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixture", type=Path, nargs="?", default=Path(__file__).with_name("golden-vectors.json"))
    args = parser.parse_args()
    try:
        require(args.fixture.stat().st_size <= 1024 * 1024, "fixture exceeds 1 MiB")
        vectors = json.loads(args.fixture.read_text(encoding="utf-8"))
        equal(vectors["fixture_version"], "1.0.0", "fixture version")
        seed = bytes.fromhex(vectors["test_seed_hex"])
        equal(len(seed), 32, "HMAC test seed length")
        verify_manifest(vectors["canonical_manifest"])
        pool_count = verify_pool(seed, vectors["pool"])
        choice_count = verify_choices(seed, vectors["choice_order"])
        ast_count, diagnostic_count = verify_parser_expectations(vectors["math_parser"])
        counts = verify_scores(vectors["exact_score_vectors"])
    except (OSError, ValueError, TypeError, KeyError, ZeroDivisionError, struct.error) as error:
        print(f"Assessment fixture verification failed: {error}", file=sys.stderr)
        return 1
    print("Verified canonical manifest bytes and SHA-256.")
    print(f"Verified {pool_count} pool and {choice_count} choice HMAC-SHA256 rankings.")
    print(f"Verified {ast_count} supplied AST values and {diagnostic_count} diagnostic anchors.")
    score_summary = ", ".join(f"{kind}={count}" for kind, count in sorted(counts.items()))
    print(f"Verified exact scoring vectors: {score_summary}.")
    print("Scope: these fixtures cover arithmetic and encoded expectations. Evaluator and parser conformance requires a separate implementation test suite.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
