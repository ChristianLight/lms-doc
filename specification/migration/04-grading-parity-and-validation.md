# 04. Grading parity and migration validation

A parser can establish structure and still change a learner's result. Verify each accepted migration against a pinned compatibility profile and the candidate-visible workflow. Compare the exact input presented, accepted response, criterion points, item maximum, attempt consumption, feedback availability and academic contribution. A normalized result of “correct” is insufficient when one of these differs.

## Declare the comparison target

Record the source format, runtime family and available release evidence privately. Archive values alone may omit defaults and tenant overrides. Use a release-pinned upstream implementation or an authorized source instance where available to establish behavior. A current upstream release is evidence for that release. It does not prove an undated export was executed under it. Distinguish explicit source values, inherited policies, profile defaults and missing evidence. Match source scope from leaf, section and course metadata using declared field-specific inheritance rules. Absent, zero, false and empty are distinct inputs.

Assign a result to every staged component.

| Result | Meaning | Activation |
| --- | --- | --- |
| Exact by supported profile | All applicable fields mapped, executable representative vectors agree and no unresolved dependencies | Eligible for ordinary review |
| Approved behavioral change | Target behavior differs and an authorized reviewer approved the named difference and candidate impact | Eligible only after the approved repair |
| Preserved without grading | Candidate prose can be rendered and the original protected definition remains available | Separate ungraded publication decision. It never replaces a graded item implicitly |
| Blocked | An unsupported scorer, malformed rule, missing renderer or unresolved policy can alter results | Repair or keep inactive |
| Unverified | Source release or test oracle does not establish required behavior | Review required. No exact parity claim |

Measure denominators for published reachable material and for selected draft overlays separately. Count scored controls, constructed responses, attachment channels, assets and unhandled extension references in addition to definitions. Record every observed difference by affected private locator, symptom, target owner and remediation. Reports exposed to a repository or public log contain only synthetic cases and design rules.

## Discrete choices and partial credit

For a single-choice interaction store one selected key. A verified exact rule returns maximum when that key belongs to the accepted set. A declared partial choice has a private decimal fraction and the remainder of the rubric rules determine overall status. Do not use a numeric suffix or display label to infer marks. For a dropdown, verify whether the source stores raw option values or generated identities. The compatibility parser for a legacy quoted option list accepts only its declared quoting and delimiter grammar. It never uses a language evaluator. Reject ambiguous values that collide after source normalization.

For multi-select, define the known displayed option universe U, correct keys C and selected set S. Reject duplicates, unknown keys and out-of-scope answers at the response boundary. Grade exact-set mode by S = C. An explicit source profile may treat an empty selection as incorrect before applying partial credit. Preserve absence, candidate-cleared input and deliberately submitted empty set as separate evidence states. The decision-count profile computes the number of correct selections plus correct rejections, or `|S ∩ C| + |(U \ C) \ S|`, and divides by `|U|`. Apply source rounding at the response criterion boundary when verified. One known profile rounds points to two decimal places with midpoint away from zero and determines correct, partial or incorrect from the pre-rounding count. Default native mapped weights and this compatibility rule differ because the latter awards credit for correct omissions.

In a synthetic response with six options, correct keys A and B, and a 1-point maximum, selecting A and C gives one correct selection and three correct rejections. The verified decision-count profile yields 0.67 and partial. Selecting A and B yields 1 and correct. Submitting an empty set yields 0 when the source profile applies its empty-response guard, even though four distractors are unselected. For the halves profile, one mismatch earns one-half only with at least three available choices, and two mismatches earn one-quarter only with at least five. Other nonzero error counts yield zero under that profile. Confirm exact behavior for supplied scope before using any partial mode.

Snapshot actual option identities, placement and fixed-position flags. A shuffle changes display order, never the identity submitted or scored. Preserve source question layout and option count even if two entries look alike. Targeted feedback and compound hints match known keys or sets and use their own disclosure gates.

## Short text and expression-looking answers

Treat literal, case-insensitive literal and pattern match as distinct evaluator profiles. Under a verified source string profile, strip leading and trailing Unicode whitespace from expected and submitted values for scoring. The case-insensitive literal profile uses Unicode lowercase comparison. It does not introduce Unicode normalization, accent folding or full case folding unless verified for the actual source. For example, an invented acceptance rule for “straße” under lowercase matching does not also accept “STRASSE”. A destination full case-fold profile would accept it and requires a reviewed change. Preserve ordered primary and alternate answers, deduplicate only when grading and feedback precedence both remain identical, and retain input representations privately. Punctuation and spaces inside a response remain significant unless declared otherwise.

Read `type` as tokens according to the source profile. Trailing whitespace can be irrelevant while unknown punctuation may affect tokenization. Retain source configuration privately and record parsed mode. A response that displays algebraic-looking text but uses the short text family must keep literal or pattern semantics unless the owner authorizes a math conversion. Explicit legacy alternate delimiters need their declared parser and tests. A candidate submit with no answer and a value that trims to empty use the profile's blank outcome.

For regex, record the runtime's engine family, matching method, anchoring, case behavior, alternate-combination rule, and its time and memory risk. The compatibility profile can only translate constructs whose behavior is expressible by the bounded target engine. Examine top-level alternation, anchoring, escapes, character classes, flags, lookaround and backreferences. Pattern compilation failure is a definition error. It does not mark learners wrong or silently turn the pattern into a literal. Do not run unchecked imported patterns in the web request or use the general-purpose runtime to test attacker-provided pathological expressions.

A known legacy profile builds an anchored expression by concatenating alternatives without surrounding the entire alternation in a group and then searches. A synthetic pattern `^sky|river$` may therefore accept “skyward”. A safe whole-string match of `(?:sky|river)` rejects it. The parity decision either uses an approved equivalent bounded matcher or presents the difference to an authorized reviewer. Keep expected and candidate strings in the protected fixture store. A regex feedback trigger can differ from scoring because it has separate trimming, mode and matching precedence. Test the expected winning feedback rule as well as correctness.

## Numerical scoring

Use the control declared by the renderer and the parser declared by the scoring rule. A numerical answer may be a decimal literal, fraction or bounded constant expression. Candidate formatting such as a unit suffix outside the text field has no grading effect by itself. Protect original text, evaluated value and parser status separately. Compare parsed values only after validation. Do not replace all numerical inputs by an exact-text matcher or infer a unit requirement from presentation.

For a confirmed compatibility profile, use the following finite comparisons.

| Tolerance declaration | Expected evaluation |
| --- | --- |
| Plain numeric tolerance t | Accept when absolute difference is at most t, inclusive |
| Explicit percentage p% | Compute `p/100 × abs(expected)`, then compare absolute difference, unless the pinned profile gives that exact tolerance token special treatment |
| Verified historical default `0.001%` | In the reference profile this exact default token uses `0.00001 × max(abs(candidate), abs(expected))`. Keep absent-versus-explicit provenance even if both use the same comparison |
| Numeric interval | Preserve endpoint expressions and open/closed boundaries. Validate range grammar rather than guessing when a wrapped expression resembles an interval |
| Additional numeric reference | In the checked reference profile, the primary comparison uses tolerance. An alternate is checked by exact numeric equality only after primary incorrectness. Preserve that order |
| Partial band or list | Store declared method, threshold, accepted values, precedence and point fraction. If any marker is unsupported, hold the definition for compatibility review |

For synthetic expected 50 and tolerance 2%, candidate 51 passes and 51.0001 fails. At expected zero, a relative-only tolerance need not admit any nonzero candidate. An explicit absolute tolerance can behave differently. If the primary reference is 8 with absolute tolerance 0.1 and an exact alternate is 11, the primary accepts 8.09 and the alternate accepts 11. A candidate response of 11.05 fails that compatibility rule. Native profiles may apply tolerance to all alternates if deliberately authored.

Test exact boundaries and runtime floating behavior using finite input witnesses. The source parser can evaluate arithmetic into floating values before the tolerance comparison. Converting the intended values to rational arithmetic can produce different edge results. A verified parity adapter declares how it reproduces the source numeric representation or publishes the reviewed difference. Complex values, nonfinite results, functions outside the registry, unknown symbols and malformed expressions have explicit incompatible or invalid dispositions. Do not silently coerce them to zero.

## Formula sampling and variants

A source sampled formula rule declares symbols, lower and upper bounds and sample count. Parse the field into a typed bounded structure. Reject duplicate symbols, missing endpoints, invalid numbers, unmatched dimension count, unsafe expressions and undefined behavior. Record case and supported symbol rules. A legacy range with equal endpoints supplies a fixed point for that variable. A reversed range or ambiguous delimiter sequence follows only a declared verified compatibility rule. Treat all-equal ranges as valid only where they preserve intended point comparison. Display a warning that repeated comparison at one point cannot prove algebraic equality.

Build candidate and reference evaluation from the same point vector. Apply the configured comparator to all required samples and record point values, scorer build, diagnostic and comparison outcome in protected evaluation evidence. A witness counterexample rejects. A service fault, parse discrepancy or insufficient supported points produces an indeterminate state or compatible invalid-response result. Never label a finite sample as proof of symbolic equivalence. Preserve singularity policy. If the source cannot resolve a point and the target silently resamples, the behaviors differ.

Separate sampling of test points from candidate variant generation. An assessment setting that disables problem rerandomization does not remove a formula comparator's sample profile. Conversely, a choice shuffle does not imply that question constants are randomized. A pinned source may draw different floating sample points on separate evaluations. The export may contain only its configuration. To claim exact test-point replay, obtain the original points or a verified algorithm and seed with compatible numeric semantics. Otherwise report “structural mapping” or “approved deterministic replacement”. Never generate an identical set of witnesses after the fact and claim they were observed in the source.

For a synthetic rule evaluated at x = 2, expressions `x+1` and `3` both evaluate to 3 at the same point. A mathematically different target rule may reject the constant over a full interval. Testing also at x = 3 distinguishes them. A degenerate-range migration keeps the original comparison purpose unless an authorized educator changes it. Source configuration that generates actual public parameters is separately mapped to VariantProfileVersion with reproducible realized parameters. Computed answers or executable grader dependencies require a registered scorer replacement and independent examples. Only an approved inert transfer artifact retains unhandled source code.

## Item points, assignment weight and completion

For a problem with several separately scored responses, record each response's point maximum and scoring state, then aggregate earned and possible independently. Source default is profile-specific and can be one point per scored response. The item-level delivery weight is a separate policy value. Missing weight uses the verified source raw possible maximum or inherited setting. A positive explicit weight W uses the raw score ratio times W when that is the declared source rule. Bind this range conversion to the approved grade item policy, without changing the assessment's raw marks.

For example, raw result 3/4 and positive weight 6 contribute 4.5 of 6. Missing explicit weight contributes 3 of 4 under the assumed default. An explicit zero contributes neither numerator nor denominator, but the candidate can still attempt the activity and receive approved correctness, raw marks, completion or rubric feedback. Use AssessmentDelivery's noncounting or formative contribution mode and retain AttemptSubmission and ItemMarkRevision. If a noncounting GradeItem exists, its GradeItemVersion has `counting_kind=formative` and a compatible observation range. A scored definition with weight zero does not acquire a zero scorer maximum. A comment-only rubric with genuine maximum zero is a different case and has no numeric GradeEvidence. Such a task can still require staff review and contribute completion or authorized comments.

Compute item pass/fail, completion, record aggregation and retake selection independently. A zero weight does not imply optional course participation. Positive source weight may normalize an individual point range while categories independently use a weighting formula. Check both. Unknown inherited category configuration creates a records issue, not a default equal-weight grade line.

## Attempt and answer release parity

Preserve the source operation boundary when one Check/Submit grades several fields together. A draft save, explicit formative check, scored submit, reset and next attempt are different actions. Discover which action consumes an attempt, whether it resets controls or variants, which evidence it preserves and which attempt supplies the grade. Carry source attempts, delays and maximum settings into a versioned DeliveryPolicyVersion and let academic policy select the approved mark. A delay between scored submissions may leave the draft writable. Use a compatible retain-first-form profile when repeated source submissions preserve realized parameters and option order. Treat reset-dependent changes as a separate compatibility check. A blank, parser error or scorer outage consumes an attempt only if the verified policy does so. Do not infer unlimited attempts from an absent field until the inherited or default value is resolved.

| Source outcome condition | Target review policy |
| --- | --- |
| Never | Withhold answer key and model solution |
| Always | A disclosure gate permits the specific fields. Protected exam policy may require an approved incompatibility resolution |
| Past due | Compare the verified effective close or due-with-grace instant with its source boundary semantics |
| Closed | Compute exhaustion OR verified due/grace condition when required by the profile |
| After N attempts | Count admitted scored attempts and apply the source threshold and configured maximum cap |
| After all attempts or correct | Permit only when quota exhausted or defined correctness condition attained. A threshold attribute for another mode does not modify this mode |
| Results visibility | Resolve separately for correctness, score and submission feedback. An answer-key rule does not grant every field |

A source may use a strict “now greater than deadline” disclosure check while the destination uses a half-open time window. Write an exact-boundary test and approve any difference. An exhausted attempt counter stays exhausted across reset where verified. Answer-key predicates use accepted marking evidence and do not infer correctness from a queued or errored run. Keep availability, check/submit authorization, score display and answer disclosure distinct. Prevent a current learner from discovering any private configuration by altering the client projection or requesting a hidden field directly.

## Constructed-response scoring parity

Compare written and attachment requiredness, file policy, prompt grouping, sealed evidence, the required workflow steps and release. Use the same ordered rubric for all mapped prompts. Validate one criterion mark against a canonical level or permitted free point step and preserve separate per-criterion feedback. A disabled criterion feedback field cannot become required. A missing point option is a rubric integrity issue. A one-level zero-point criterion collects the configured feedback without changing total score. Explicit single-level zero can be presented under its approved level contract or as a reviewed feedback-only form.

Test these conditions separately. A required written-only task rejects a blank seal. A file-only task rejects missing or pending files. With both enabled and required, both must pass validation. For an authorized choice of either channel, one valid response is sufficient. An uploaded file completing after the hard deadline cannot enter a prior sealed manifest. Preserve original files and safe working copies under scoped permissions.

For ordered staff and self-review steps, record exactly which are required and when. A learner self-score is retained as SelfReviewRevision, separate from official evidence. A staff-override mode can be reproduced only with explicit reviewed policy, auditable actor and preserved reason. Verify whether authoritative staff grading can bypass self-review completion in the selected source release. A missing or cancelled review step must not be converted to a failing mark. If a target cannot represent the release or completion interaction, stop active migration until the institution approves a replacement.

## Required validation stages

1. Build a normalized assessment projection twice from immutable staged bytes and compare digests and mapping outputs. The grader inputs, choice ID map, public node order and private feedback order must be stable.
2. Verify the public/private boundary by scanning every candidate projection, including accessible labels, asset references, markup, safe renderer props, notifications and preview endpoints. Exact answer values may appear in public question prose if deliberately authored. Classify whether a secret comes from a protected grading or feedback field before asserting a leak.
3. Run source-profile and destination vectors for every applicable rule family and rendering combination. Include correct, incorrect, alternate, malformed, blank, partial and boundary responses, plus common candidate variants. Mark unsupported input or scorer failures by reason.
4. Compare the whole compound item. Use the same response key set, submission boundary, criterion marks, raw and weighted possible values, release fields, attempt counter and selected academic evidence revision.
5. Test actual authored rendering with keyboard, accessible names, equation previews, table headers, unknown control errors and narrow viewports. Confirm that item position, stem context and attachment expectations remain usable.
6. Reconcile outcomes by authorized definition and placement. Only activate an exact version or reviewed behavior change. Finalize the private transfer receipt and retain source bytes and key maps under institution policy. A later correction creates another approved version and preserves earlier evidence.

Keep a regression fixture suite of wholly synthetic XML and expected logical records. It must include rich table/prose interleaving, duplicate visible choices, accessible fallback labels, absent text channel, both text and file requirements, a zero-point feedback rubric, fixed choices, decision-count scoring, literal normalization, tolerance boundaries, unresolved regex constructs, malformed and degenerate sample profiles, score-versus-weight separation, and an unresolvable plugin reference. A single source example does not establish a scoring algorithm. Validate difficult cases against more than one hand-calculated or independently verified expected result.

The [synthetic XML](fixtures/assessment-extraction.xml) and [frozen expectations](fixtures/assessment-parity.json) can be checked with the standard-library reference verifier. It checks the listed witnesses and does not implement a general importer or grader.

```sh
python3 specification/migration/fixtures/verify-assessment-fixtures.py
```
