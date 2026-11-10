# 11. Implementation verification and fixture strategy

Catalog scenarios describe required outcomes. The adjacent [golden vectors](golden-vectors.json) supply exact input bytes, digests, ASTs and score outputs for selected calculations. This chapter defines harness boundaries for reproducibility. A conforming implementation may use any language, database, queue or UI stack. Validation exercises both durable state and forbidden observations.

Run the reference fixture verifier with the Python standard library.

```sh
python3 specification/assessment/verify-golden-vectors.py
```

The verifier checks the canonical bytes and SHA-256 of the fixed manifest, the encoded inputs and outputs of pool and choice HMAC rankings, the exact values of supplied ASTs, diagnostic anchors in the original input, and the exact arithmetic for tolerance, unit conversion, partial selection and slot normalization. The parser and evaluator implementations must separately prove that they produce those ASTs, diagnostics and scores from the inputs.

## Fixture conventions

Use canonical timestamps with explicit UTC. Test clock has an externally controlled monotonic tick and authoritative wall instant. Use repeatable fixture IDs and producer keys. Treat UTC second precision and fractional milliseconds as supported input. A fixture can choose a smaller declared serialization resolution. Digests use exact UTF-8 canonicalized input bytes. Use binary HMAC for selection ranking and compare digests as unsigned byte sequences. Use [JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785) for version 1 manifest digests, with exact point values and large integers serialized as typed strings. Use a versioned deterministic serializer for each manifest. A serializer version change is a compatibility change and cannot recompute old digests without retaining its old rules.

A scoring golden vector contains scorer profile, typed input, protected reference, declared assumptions, response disposition, criterion points and maximum, safe diagnostic, and invariant assertions. For a math parser, include AST structure or parse error location. Compare numeric values as canonical exact decimal or rational. For private answers and diagnostics, use synthetic fixtures. Do not record real learner work in fixtures or normal trace captures.

A workflow golden vector specifies starting durable rows and heads, principal capabilities, authoritative instants, named command inputs, fault location, final durable state, expected events and withheld observations. Use transaction instrumentation to inject faults between logical steps and process restart. Test authorization independently with an unrelated offering and revoked assignment. Test duplicate logical operations with identical and changed idempotency payloads.

## Required evaluator vectors

| Vector | Inputs | Expected authoritative result |
| --- | --- | --- |
| AST associativity | `-2^2`, `(-2)^2`, `2^3^2` | Exact results −4, 4, 512 and distinct AST shapes |
| Rational exactness | `2/6` compared with `1/3` | Equality passes. Lowest-terms constraint fails on unreduced candidate spelling |
| Unicode locale | `−0,50` in configured decimal comma profile | Parse −1/2, retain two original decimal places |
| Inexact comparison edge | Expected 12, abs 0.05, relative 0.01, candidate 12.12 | Accepted inclusive edge, no premature rounding |
| Unit scale | 36 km/h compared with 10 m/s | Same dimensions, exact 10 in canonical m/s |
| Affine distinction | Quantity 25 Cel and difference 25 Cel | 298.15 K and 25 K respectively |
| Fractional exponent limits | Oversized exponential input | Bounded diagnostic and unresolved case if valid but out of profile. No resource-dependent mark |
| Domain singularity | `(x²−1)/(x−1)` and `x+1` | Restricted-domain match for x≠1. All-real function comparison fails |
| Sampling classification | `x²` and `x` at points {0,1} | Two matching samples, never a symbolic proof. Sample point 2 rejects |
| Ordered constraints | B,A,C for declared A,B,C | Position mode 1/3, pair mode 2/3 |
| Form criterion | `x²+2x+1` when factoring required | Equality criterion passes. Factoring criterion fails |
| Independent exact sets | `{3}` versus roots {−3,3} | Correctness criterion passes, completeness fails |
| Matrix dimensions | Vector [1,2] compared with matrix [[1,2]] | Shape mismatch under default semantics |
| Technical failure | Worker time budget exceeded after valid parse | Evaluation retry or manual review. No implicit zero |

## Concurrent workflow vectors

1. Start a formal exam with lease A. Use a second valid authenticated session to take over and mint B. Attempt to save with A and a current response version. Expect rejection. Save under B. Expect only B's revision. Replay the earlier acknowledged A save using its original key and verified authorized caller. Expect the historical receipt, not a new write.
2. Save a candidate field with expected revision 0, then attempt to clear with the same expected revision. Expect conflict and retained value. Retry clear against authoritative current revision. Expect explicit clear revision. Auto submit at deadline. Expect sealed blank disposition with clear history preserved.
3. Stage a file with digest H1. Change bytes to H2 before completing. Expect rejection and no eligible asset. Stage actual H2, let scan finish after deadline. Auto submit omits it and later approval cannot change the manifest.
4. Pause at 09:15, resume 09:22 with pause cap 10 minutes and close 10:05. Start at 09:00 and duration 60 minutes. Expect hard deadline 10:05, not 10:07. A stale pause callback cannot extend the same allowance twice.
5. Review the same blinded response with two distinct markers and open both candidate and staff queues. Before moderation, staff assigned independently cannot read each other's scores. Candidate cannot infer marks from accessible state, notification content, grades source or export. Moderator resolves only after both mark revisions exist.
6. Approve an assessment correction preview and then accept a conflicting independent review. Run the previewed correction. Expect conflict disposition and no overwrite. Abort remaining cases. A case already committed stays committed. Evidence consumer sees original and correction histories in causal order or retrieves missing revisions.
7. Import a question with same-looking HTML but differing case-fold, accepted options or numeric tolerance. Verify a source-target fixture mismatch prevents publication. Attempt import can preserve metadata and original payload without granting executable scoring.
8. Grant a retake allowance with end 12:00. Try at 12:00 exact. Expect no ordinal change. Try at 11:59 in a separate fixture state. Expect one new ordinal and one consumed allowance. Retrying with same request key returns same receipt.
9. Register a package-grade producer scoped to one offering. Send valid score for a learner in another offering. Expect denied intake, no record and no event. Send revision 3 before 2 for the correct learner. Expect revision gap and a recovery hint. Then send 2 and 3 in order.
10. Restore a durable backup between accepted submission and queued grading. Replay outbox while a stale worker also delivers an older lease callback. Expect one canonical receipt, one verified run result and no grade evidence duplicates.

## Candidate and staff UI acceptance

Use keyboard-only, screen reader, zoom/reflow and restricted bandwidth exercises. Test long labels and translated number input. Every visible question field must be named and every error associated. Reordering works with visible and programmatic buttons. The timer warns without forcing focus. Network outage shows last accepted save time and unsent state. Do not announce upload percent excessively. A reduced-motion preference suppresses nonessential feedback animation. Candidate feedback can be navigated by item and criterion. A staff mark form preserves typed draft comments across validation errors but restores assignment authorization after reauthentication. Candidate and staff can complete their tasks without hidden key events or pointer-only affordances.

Before production, dry-run a time-bound exam and one regrade under realistic roster size. Measure rate of time-authority disagreements, blocked form resolutions, concurrent save conflicts, queue wait and reconciliation mismatch. Review failures with reason categories. Capacity estimates must include bursts at the deadline and multiple schools using the same service. Set an explicit per-institution operational budget and fail with recoverable state where admission is unsafe.
