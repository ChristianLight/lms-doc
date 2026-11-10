#!/usr/bin/env python3
"""Verify numeric examples for the academic records grade-calc-v1 profile.

This executable reference covers only the declared vectors. Authorization,
authoritative evidence loading and transaction rules are outside its scope.
"""

import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path


def weighted_ratio(children):
    weight = sum(row["weight"] for row in children)
    if not weight:
        return None
    return sum(row["ratio"] * row["weight"] for row in children) / weight


def remove_drops(children, drop, count):
    if drop == "none":
        return []
    removed = []
    eligible = [row for row in children if not row["protected"]]
    if drop == "keep_highest":
        keep = sorted(eligible, key=lambda row: (-row["ratio"], row["key"]))[:count]
        eligible = [row for row in eligible if row not in keep]
        count = len(eligible)
    for _ in range(min(count, len(eligible), max(0, len(children) - 1))):
        if drop.endswith("_impact"):
            choices = []
            for row in eligible:
                remaining = [child for child in children if child is not row]
                impact = weighted_ratio(remaining)
                sort_ratio = -impact if "lowest" in drop else impact
                choices.append((sort_ratio, row["key"], row))
            selected = min(choices, key=lambda choice: choice[:2])[2]
        else:
            descending = drop == "drop_highest_ratio"
            selected = min(
                eligible,
                key=lambda row: (-row["ratio"] if descending else row["ratio"], row["key"]),
            )
        eligible.remove(selected)
        children.remove(selected)
        removed.append(selected["key"])
    return removed


def evaluate_category(args):
    mode = args["mode"]
    is_final = args.get("purpose", "current") == "final"
    ordinary = []
    bonus_points = Fraction(0)
    bonus_ratio = Fraction(0)
    for child in args["children"]:
        status = child.get("status", "graded")
        kind = child.get("kind", "ordinary")
        if kind == "formative":
            continue
        if status == "pending" and is_final and child.get("required", True) and kind == "ordinary":
            return {"status": "pending", "ratio": None, "dropped": []}
        if status != "graded" and (status != "missing_zero" or not is_final):
            continue
        earned = Fraction(child["earned"]) if status == "graded" else Fraction(0)
        maximum = Fraction(child["maximum"])
        ratio = earned / maximum
        if kind == "bonus":
            bonus_points += earned
            bonus_ratio += ratio
            continue
        if mode == "points":
            weight = maximum
        elif mode == "equal":
            weight = Fraction(1)
        elif mode == "weighted":
            weight = Fraction(child["weight"])
        else:
            raise ValueError(f"Unsupported category fixture mode {mode}")
        ordinary.append(
            {"key": child["key"], "ratio": ratio, "weight": weight, "protected": child.get("protected", False)}
        )
    dropped = remove_drops(ordinary, args.get("drop", "none"), args.get("drop_count", 0))
    ratio = weighted_ratio(ordinary)
    if ratio is None:
        return {"status": "not_applicable", "ratio": None, "dropped": dropped}
    bonus_mode = args.get("bonus_mode", "none")
    bonus = Fraction(0)
    if bonus_mode == "points":
        if mode != "points":
            raise ValueError("Points bonus requires a points category")
        bonus = bonus_points / sum(row["weight"] for row in ordinary)
    elif bonus_mode == "ratio_bonus":
        bonus = bonus_ratio
    if "bonus_cap" in args:
        bonus = min(bonus, Fraction(args["bonus_cap"]))
    capped = min(ratio + bonus, Fraction(args.get("cap", "1")))
    return {"status": "graded", "ratio": str(capped), "dropped": dropped}


def evaluate_late(args):
    raw = Fraction(args["earned"])
    maximum = Fraction(args["maximum"])
    elapsed = max(0, args["elapsed_ms"] - args["grace_ms"])
    mode = args["mode"]
    units = 0
    if elapsed and mode != "none":
        units = 1 if mode == "fixed_max_fraction" else (
            elapsed + args["interval_ms"] - 1
        ) // args["interval_ms"]
    deduction = units * Fraction(args["deduction"])
    if mode in {"fixed_max_fraction", "interval_max_fraction"}:
        deduction *= maximum
    deduction = min(deduction, Fraction(args["cap"]))
    adjusted = min(maximum, raw, max(Fraction(args["floor"]), raw - deduction))
    return {"units": units, "deducted": str(raw - adjusted), "adjusted": str(adjusted)}


def round_decimal_units(value, rule):
    floor, remainder = divmod(value.numerator, value.denominator)
    doubled = 2 * remainder
    if rule == "truncate":
        return floor
    if rule == "half_up":
        return floor + (doubled >= value.denominator)
    if rule == "half_even":
        return floor + (doubled > value.denominator or (doubled == value.denominator and floor % 2))
    raise ValueError(f"Unsupported rounding mode {rule}")


def evaluate_band(args):
    ratio = Fraction(args["ratio"])
    places = args["places"]
    multiplier = 10 ** places
    display = round_decimal_units(ratio * 100 * multiplier, args["rounding"])
    basis = Fraction(display, 100 * multiplier) if args["basis"] == "display_rounded" else ratio
    whole, rest = divmod(display, multiplier)
    text = f"{whole}.{rest:0{places}d}" if places else str(whole)
    return {"display_percent": text, "passed": basis >= Fraction(args["threshold"]) and args["required_gate_met"]}


def evaluate_attempts(args):
    def time_key(row):
        return datetime.fromisoformat(row["submitted"]), row["ordinal"], row["key"]

    allowed = [row for row in args["attempts"] if row.get("status", "graded") in {"pending", "graded"}]
    allowed.sort(key=time_key)
    if not allowed:
        return {"status": "not_applicable", "ratio": None, "selected": []}
    mode = args["mode"]
    selected = allowed
    if mode == "first":
        selected = allowed[:1]
    elif mode == "latest":
        selected = allowed[-1:]
    if any(row.get("status") == "pending" for row in selected):
        return {"status": "pending", "ratio": None, "selected": []}
    if mode == "highest":
        selected = [min(selected, key=lambda row: (-Fraction(row["adjusted_ratio"]), time_key(row)))]
    ratios = [Fraction(row["adjusted_ratio"]) for row in selected]
    return {"status": "graded", "ratio": str(sum(ratios) / len(ratios)), "selected": [row["key"] for row in selected]}


def main():
    evaluators = {
        "category": evaluate_category,
        "late": evaluate_late,
        "band": evaluate_band,
        "attempt": evaluate_attempts,
    }
    payload = json.loads(Path(__file__).with_name("grade-calculation-vectors.json").read_text())
    failures = []
    for vector in payload["vectors"]:
        actual = evaluators[vector["kind"]](vector["input"])
        if actual != vector["expected"]:
            failures.append(f"{vector['id']} expected {vector['expected']}, got {actual}")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"Verified {len(payload['vectors'])} {payload['algorithm']} vectors")


if __name__ == "__main__":
    main()
