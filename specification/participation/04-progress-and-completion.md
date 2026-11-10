# 04. Progress evidence, completion and recalculation

## Authoritative records

| Record | Identity and fields | Invariants |
| --- | --- | --- |
| LearningEvidence | Institution, enrollment release, exact placement, source kind, source event ID, evidence version, occurred and received instants, actor, typed payload and accepted disposition | Unique institution, authenticated producer namespace and source event ID. Same event key with changed payload is a conflict. Event is append-only |
| LearningProgress | Enrollment release, exact placement, state, first evidence instant, most recent accepted instant, accepted count, projected sequence and revision | Unique release and placement. Rebuildable. Progress states not_started, in_progress, completed and exempt |
| CompletionRecord | Enrollment release, placement or offering scope, rule version, decision type, earned instant, evidence links, approval and optional supersedes | Append-only. Only approved withdrawal or supersession replaces effective completion |
| ProgressResume | Enrollment release, selected placement, block or media anchor, learner session sequence, revision and received instant | One current per release. Kept separate from authoritative completion |
| LearnerBookmark | Person, offering, stable placement key, optional anchor, private label and created instant | Unique person, offering, key and normalized anchor. Personal data excluded from grade evidence |

Evidence source kinds include explicit acknowledgment, authenticated view, video coverage, accepted assessment submission, released assessment outcome, approved attendance, package evidence, equivalent accessibility task, waiver and carry. The client sends intents or telemetry. The authorized source adapter emits the accepted evidence. Only permissioned source adapters can represent an assessment result, package result or attendance correction. Checks bind actor, enrollment release, placement and compatible activity version.

Validate incoming kind and payload against the [version 1 evidence schema](learning-evidence.schema.json). Verify same-institution references, trusted source authority and source sequence outside JSON Schema.

## Acceptance and projection algorithm

1. Validate schema and source signature or server identity. Check action permission, exact release/placement relationship and evidence type permitted by the pinned activity. A delayed assessment or package callback may refer to a prior release if its corresponding authoritative attempt or registration is valid.
2. Derive institution from the exact enrollment release and deduplicate by institution, authenticated producer namespace, source key and canonical payload digest. Team or other multi-learner fanout derives a deterministic event key for each enrollment release and placement from the originating accepted event identity. Return original receipt for an exact replay. Reject mismatched replay and log the diagnostic without storing a second accepted event.
3. Append event with monotonic local sequence. Publish an idempotent projection job in the same transaction. Out-of-order timestamps remain observable. For replaceable source states, use trusted source revision and scope. For cumulative evidence combine valid sets. Keep chronological event time separate from ingestion order.
4. Compute state by exact rule version and effective policy. A nonterminal accepted action moves not_started to in_progress. Satisfying rule emits a CompletionRecord. Exemption is an independent approved decision and can supersede normal progress display. A late event does not undo an earned completion automatically.
5. Persist projection with its last source sequence and command version. Compare-and-swap updates. A failed projector can resume from the last committed sequence. Provide queue age in staff diagnostics and label stale reads. Rebuild uses the same deterministic rules and compares output digests.
6. Link evidence after approved release rollout using old and new release IDs, mapping type and rule evidence filters. Preserve original evidence and issued academic history. Any revoked evidence triggers impact analysis, then an authorized corrective completion supersession if necessary.

Viewed evidence defaults to optional reading acknowledgment. Raw page-open signals may satisfy an explicitly configured engagement rule after a minimum client-visible threshold of 5 seconds and authorized session receipt, with clearly documented assurance. They do not demonstrate mastery. Grades and mastery require approved records or evidence rules.

### Video coverage calculation

Each accepted report includes media version, player session, inclusive start milliseconds, exclusive end milliseconds and increasing session sequence. Validate range, reasonable elapsed time and rate limits. Merge overlapping or adjacent intervals into a canonical interval set. Sum distinct coverage and divide by declared effective media duration. Coverage defaults to 90 percent when explicitly required and can be replaced by an approved accessible equivalent. A resume position is last accepted position, independent of cumulative coverage.

For a 100,000 ms video, reports [0, 40,000), [30,000, 70,000) and [80,000, 99,000) cover 89,000 ms or 89 percent. A repeated [0, 40,000) changes nothing. A later [70,000, 80,000) brings coverage to 99 percent. Seeking directly to 99,000 gives a resume position but no extra coverage.

### Progress denominator and formal completion

Use required eligible leaf placements for the current enrollment release by default. Exclude optional and exempt placements. Include future scheduled requirements if assigned and safe to disclose. Omit hidden audience-specific branches entirely. For alternates, include one required slot per choice policy rather than every possible branch. Display completed count, assigned count and remaining or pending state. Use a whole percentage rounded half-up for display only. For no required activities show no required activities and an empty percentage. Do not award formal course completion automatically from a zero denominator unless an explicit catalog-only completion policy applies.

A learner has eight required eligible activities, one excused and five completed. Denominator is seven and displayed progress is 71 percent. A scheduled future eighth activity remains counted if assigned and visible as upcoming. If policy hides it entirely from the learner, report percentage as of visible assigned path and indicate there may be later requirements without revealing the hidden activity.

Award offering completion only when every applicable required criterion, grade threshold if configured, and attendance requirement is satisfied and the authoritative sources are ready. Store rule version, denominator basis and exact evidence. Show complete and pass or fail independently when policy distinguishes them. An appeal or corrected result creates an authorized superseding record rather than erasing earlier completion.

## Fixture set

| Replay or change | Expected outcome |
| --- | --- |
| Two browser tabs acknowledge the same resource with the same intent | One accepted evidence receipt and one effective completion |
| A package callback arrives after rollout | Historical release accepts it if registration still valid. Current projection changes only through an approved carry |
| Instructor exempts inaccessible required media | Completion view records exemption and removes item from required denominator under default policy |
| Earlier video report arrives after a newer report | Interval set grows idempotently. Resume anchor follows accepted current-session sequence |
| Official attendance correction invalidates required evidence | Staff see impact and can issue reviewed completion supersession. Original award stays auditable |
