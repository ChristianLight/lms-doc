# 09 Analytics, intervention and lineage

## Authoritative versus analytic

An analytics event is evidence of system activity. It can support intervention or aggregate reporting. It does not post grades, establish mastery, infer attendance or trigger a high-stakes outcome without an approved educational rule and decision. A learner viewing a page for two seconds does not establish that the material was understood. Gradebook, credit and award decisions remain with their owning records.

Use event envelopes with institution, producer, source event ID, purpose, schema version, occurred and received instants, data minimization and scope. Collect enrollment, delivery progression, released grades, official attendance and support interactions as separately authorized sources. Maintain checkpoint and source lineage. Pseudonymize analytic IDs with institution-scoped mapping where feasible. Access to mapping and direct identifiers is restricted. Store corrections and privacy tombstones so replay cannot reintroduce withdrawn content.

## Metric definitions

| Metric | Numerator | Denominator and exclusions | Default |
| --- | --- | --- | --- |
| Offering completion | Enrollments with approved CompletionRecord by cutoff | Active or completed eligible enrollments at cutoff, excluding cancelled or test | Show counts and ratio. Track withdrawals separately. |
| Pass rate | Learners with released passing final outcome | Enrollments with released final pass/fail outcome. Exclude incomplete, pending, withdrawn and transfer-only. | Include coverage count and incomplete count. |
| Submissions on time | Valid submitted assessment deliveries received at or before effective due after grace | Applicable submitted graded deliveries with defined due. Count one configured first valid submission per learner and delivery. | Do not infer timely from worker receipt. |
| Attendance rate | Present or late minutes where policy credits them | Scheduled eligible minutes, excluding cancelled and excused when policy excludes. | Unknown minutes are separate data gaps. |
| Median published course ratio | Median of released final numeric ratios | Eligible released numeric records only, one effective revision per learner/offering | Exact ratio median, average middle two if even. |
| Programme attainment | Approved qualifications by cutoff | Programme enrollments eligible for audit according to fixed reporting cohort | Require cohort definition and cohort cutoff. |

MetricDefinitionVersion records ordered dataset inputs, population inclusion, authorized grouping dimensions, aggregate function, cutoff interpretation, output type, suppression and version. Every report includes count, denominator, suppressed status and coverage. Zero denominator returns unavailable. Missing feeds produce an incomplete coverage label or failed official report rather than silently lowering a numerator. Lock dataset revision for paginated export. A correction event rebuilds affected partitions and preserves original delivered report version.

**Worked example.** An offering has 40 active or completed eligible enrollments, 32 published final pass/fail grades, 28 pass, 4 fail, 3 incomplete and 5 with unresolved grading. Report pass rate 28/32 or 87.50 percent, finalized coverage 32/40 or 80.00 percent and unresolved 5. Do not divide 28 by 40 for the pass-rate metric. If an approved correction changes one pass to fail, revised pass rate is 27/32 or 84.38 percent, while the original report retains its published cutoff.

## Early intervention

Start with transparent criteria. A product default example flags a learner after two confirmed overdue required tasks within 14 calendar days, provided the learner is active, the feeds are complete, the tasks are not excused and the learner does not already have an open case for the same condition and window. The institution enables the rule explicitly. Do not score a learner from optional activity, unreported activity or a disabled tracking source. A learner new to an offering gets a grace period of seven calendar days by default for inactivity-related triggers.

InterventionRuleVersion stores population, predicates, thresholds, lookback, excluded events, cooldown, routing role, note retention and permitted disclosure. InterventionCase stores Enrollment, rule, evidence pointers, reason codes, scope, triage state and assignment. An InterventionAction records assigned reviewer, contact action, appropriate channel, reason, time and resulting status. Authoritative education records are unchanged. Avoid embedding sensitive explanations in notifications or exporting case notes in standard cohort reports.

1. On a schedule, compute using stable event cutoff and rule version. Deduplicate by enrollment, rule and trigger window. Store observed evidence links and evaluated exclusions.
2. Assigned teacher/adviser sees a queue with reason and completeness. They can dismiss data error, request information, assign follow-up or mark resolved. The default is human review before any student-facing notification.
3. Refresh the case with corrections. If the source problem no longer applies, add a resolution event. Reopening requires a new authorized signal or explicit staff action with reason. Avoid repeated alerts during cooldown.
4. Allow learner access and correction request through approved institutional channels. Restrict sensitive staff notes by purpose. Monitor whether case rules produce uneven or misleading results without collecting unnecessary sensitive attributes.

## Privacy and access controls

The default aggregate suppression threshold is 10 distinct people in institution-configurable staff reports outside a directly assigned classroom. Apply complementary suppression when totals, adjacent filters or export joins could reconstruct suppressed cells. Limit overlapping arbitrary groupings, queries and exports. Small assigned classes can view their own authorized person-level records through the teaching workflow. They do not bypass institutional report suppression for unrelated data. Separate purpose permissions for individual grades, intervention notes, analyst reports, cross-offering reports and data exports.

Scope report generation at the time of request and at download. A revoked analyst role must invalidate active download authorization even when a file already exists. Include scope, source cutoffs, metric revision, render version, output digest, issuer and retention on export records. Use protected artifacts, redacted operational logs and access audit. Restore a reporting projection from source events after rollback without modifying official grades.

## Interchange

Use internal records for authoritative lineage and a separate adapter when publishing an analytics profile. Map only fields permitted for that purpose, record profile version and mappings and expose counts of rejected/unknown event types. Backfill/retry events with idempotent IDs. A receiver acknowledgment is delivery evidence and does not make an analytic statement academically official.

- [Caliper Analytics](https://www.1edtech.org/standards/caliper)
