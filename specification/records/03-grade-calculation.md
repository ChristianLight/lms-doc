# 03 Grade calculation and worked cases

## Numeric representation

Wire scores use a canonical decimal string with an optional fractional part up to six places and no exponent. Remove trailing zeroes on normalization. Disallow negative marks and negative zero. Input range is zero through 1,000,000 points per grade line and policy maximum must be positive for a counting numeric item. Convert each score and maximum to integers in common millionths. Divide using reduced arbitrary precision rational arithmetic. Compare thresholds by cross multiplication. Persist result rationals as nonnegative numerator and positive denominator strings, reduced by greatest common divisor. Exact processing has a 65,536-bit limit per integer. Reject source graph or computation that exceeds the limit and expose a repairable policy error. Round only display values unless a previously published policy explicitly requests round-before-map.

## Processing order

1. Load the assigned policy, offering release, enrollment applicability, authorized grade source bindings and consistent cutoff. A tombstoned source is excluded through its explicit revocation event rather than record deletion.
2. Resolve the applicable grade item and effective deadline for each learner. Exclude unassigned path items and excused work from all denominators. Count a confirmed missing item as zero at final only when its policy permits it. Never use absence of any source event as proof of non-submission when a reconciliation is pending.
3. For each applicable item, find accepted evidence per attempt, take the latest eligible sequence for each attempt at the cutoff and apply eligibility and late deductions. Select or average attempts. Apply any approved item override. An approved direct final override is a separate revision above the computed total.
4. Traverse child categories bottom up. Select counted, dropped and bonus contributors. Return a normalized rational and list of contribution decisions. If an included required child is pending under final policy, return a pending summary.
5. Apply category weights, bonus and cap. Apply independent required assessment or competency gates after arithmetic. Map the exact result to its grade scale. Apply a final override only where an approved scope allows changing each affected field.
6. Persist revisions and source lines. Stage release eligibility. Never render a private calculation to a learner before the matching release activates.

## Grade states

| Input state | Provisional treatment | Official treatment |
| --- | --- | --- |
| Not assigned or inapplicable | Exclude | Exclude |
| Excused | Exclude and show approved status | Exclude or require alternate evidence if protected |
| Assigned and not yet due | Display upcoming, exclude from current ratio | Pending if final cutoff precedes required deadline |
| Overdue with confirmed no valid submission | Show missing. Default current ratio excludes. | Count zero when authorized policy allows. |
| Submitted and unmarked | Show pending | Blocks final calculation for required line |
| Mark incomplete or evaluator failed | Show pending review | Blocks final until resolved or official incomplete |
| Valid scored zero | Include zero and full denominator | Include zero and full denominator |
| Graded and staff-only | Omit from learner aggregate | Include in staff calculation, release through authorized action |
| Voided attempt | Ignore and use permitted alternate | Require official reason and source lineage |
| Formative or zero weight | No aggregate contribution | No aggregate contribution |
| Explicit incomplete, withdrawal or transfer-only | Distinct outcome | Non-numeric disposition with policy consequence |

## Leaf attempts and deductions

For eligible attempt a, let raw ratio be earned divided by maximum. Extra credit at item level is separate from an ordinary item earned/maximum ratio. An ordinary evidence maximum must match its pinned source range or an approved normalization map. Raw fractional marks are retained as received.

When late policy is active, let t be max of zero and received-at minus effective due time minus grace, measured in integer milliseconds. Interval count is ceiling of t divided by interval duration. A fixed late amount applies once when t is positive. A per-interval percentage deduction is min of configured deduction cap and units times the configured ratio of maximum. Compute adjusted earned as max of configured floor and raw earned minus deduction points, then clamp to min of raw earned and item maximum so a floor cannot improve a score. Apply an item override after deductions only when approved. In the absence of an override, select latest/first by official submission instant and attempt ordinal, using UUID as last stable tie-break. Highest compares adjusted normalized ratios first and favors earliest official submission then lowest ordinal and UUID at a tie. Average uses arithmetic mean of eligible adjusted ratios and maps to the item maximum. A mean can include a zero submitted attempt. It never includes an abandoned draft. Pending attempts block official highest or average when they could change the selected result. Under latest or first, a pending attempt blocks if it is the current selected candidate by time/order.

A policy may cap or disallow early or late attempts. Compare official persisted received-at and effective deadline, never browser clock. Compute with the due snapshot bound to the attempt. If a later accommodation is approved retroactive to an existing submission, record the new deadline decision separately and recalculate through a correction request.

**Worked example.** An item is out of 40 with one point per commenced hour after a 10-minute grace, a maximum 8-point deduction and a 0-point floor. An attempt marked 33/40 arrives 71 minutes after due. Elapsed after grace is 61 minutes and units are two. The adjusted mark is 31/40. A second on-time attempt scored 30/40. Under highest, 31/40 wins. Under average, the result is 61/80 or 76.25 percent. Under latest, the persisted times identify which 30/40 or 31/40 wins.

## Aggregating a category

For ordinary counted child j, determine ratio r(j) and positive contribution w(j). For points mode w is the item maximum or child group declared points. In equal mode w is one. In weighted mode w is the configured basis-point integer. Base ratio is sum of w(j) times r(j) divided by sum of w(j). Renormalize across the set of eligible counted children after exclusions. Record original weight and used effective weight. An official group with zero eligible ordinary denominator returns not-applicable unless a required child remains unresolved. It cannot manufacture a passing result. A learner-facing current view can use available released evidence, explicitly labelled partial.

At most one drop operation mode applies per group. Candidates exclude bonus, protected and unresolved children. For drop-lowest and drop-highest ratio modes, sort by exact normalized ratio ascending or descending then stable placement key ascending. Drop min of requested count, available candidate count and count preserving at least one included ordinary child. Keep-highest retains the specified count of eligible unprotected candidates plus all protected children. If protected children exist, zero allowed unprotected children still preserves the required denominator. A required protected child's status remains unresolved rather than dropped. Configurable optional impact mode removes one candidate at a time by recalculating the ratio with it excluded. For low-drop choose the greatest remaining ratio and for high-drop choose the least, ties by stable key. This is explicitly a sequential policy. It is not an optimizer across all combinations. Bound impact candidates to 128 and drops to 16 per category.

Bonus credits never expand the ordinary denominator. In points mode the policy may add awarded bonus points divided by the remaining ordinary denominator. In any mode a separate named ratio-bonus entry can add capped percentage points against the group ratio. Each group chooses at most one bonus mode. Explicit maximum earned bonus, group cap and offering cap apply after bonus. If all ordinary work is excluded, bonus remains uncounted and appears separately. Nested child ratios may pass a bonus amount to a parent only under explicit propagation, default disabled above 100 percent.

| Case | Inputs and calculation | Expected |
| --- | --- | --- |
| Points | 8/10 and 45/90. Sum 53/100. | 53 percent |
| Equal | Same values. Mean of 0.8 and 0.5. | 65 percent |
| Weighted | 8/10 at 25 percent and 45/90 at 75 percent. | 57.5 percent |
| Renormalized | Homework 80 percent weight 40, exam excused weight 60. | 80 percent if no mandatory exam gate |
| Ratio drop | A is 50/50, B 65/100, C 12/24. C is lowest ratio. | 115/150 or 76.67 percent displayed |
| Impact drop | Same values, exclude B for 62/74. | 83.78 percent displayed |
| Confirmed missing | 8/10, excused 20-point work, 10-point missing. | 8/20 or 40 percent final |
| Submitted pending | Same as missing case but 10-point work was submitted and unmarked. | 80 percent current, final pending |
| Zero distinction | 8/10 and 0/10 scored. | 40 percent in both current and final |
| Points bonus | 90/100 ordinary and 12 optional bonus points, cap 1.05. | 102 percent |
| No denominator | All ordinary work excused and bonus 12. | Not applicable |
| Exact threshold | 4,999/10,000 with 50 percent passing and display 1 decimal. | 50.0 displayed, fail under exact threshold |
| Protected requirement | 92 percent aggregate, required practical score 45 percent against 50 percent gate. | 92 percent academic score, failing outcome code |
| Period weighted | 72 percent at 40 percent and 86 percent at 60 percent. | 80.4 percent |

A status-based pass requires an exact immutable CompletionRecord owned by Delivery and accepted at the cutoff for the same enrollment, course release and placement. Store that record identity on the GradeContribution. A pending or superseded completion remains pending or excluded according to its approved source status. A completion source must be independent of the grade it supports. Reject a circular policy where a course grade requires offering completion and that offering completion requires the same released grade. A minimum item threshold is an independent gate. Excused required items need an approved substitute or exception before awarding a pass. Render both computed score and course outcome to prevent ambiguity. In UI copy use status labels, not colored cells alone.

## Executable arithmetic examples

The [calculation vectors](grade-calculation-vectors.json) cover exact ratios, policy-dependent exclusions, score selection, late deductions, protected entries, bonus ceilings and independent grade gates. Run the [reference verifier](verify-grade-vectors.py) with Python 3.11 or later. Production implementations in any language can consume the same fixture data. Authorization and persistence are tested separately through the catalog scenarios.
