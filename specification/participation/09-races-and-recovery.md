# 09. Cross-domain races, retries and reconciliation

Institutional policies apply through owning domains. A workflow crossing domains uses an exact source version, a durable command or event, and a destination authorization check. An event notification is not a permission grant. A foreign database row never becomes mutable merely because a component has its identifier.

## Short start and rollout reservation

Use a platform coordination primitive scoped by institution and enrollment. A single-person start and a release rollout lock the same enrollment key. A team start locks every intended member in ascending UUID order with a bounded total wait. The default acquisition wait is two seconds and the fenced lease limit is 15 seconds. The critical section consists of re-reading authorization, source release and applicable policy, then committing the owning start or release assignment. Do expensive rendering and problem selection preparation outside the critical section. An expired fencing token cannot commit. A contention failure returns retryable 409 START_ROLLOUT_CONFLICT and releases all held reservations. The caller retries with the same idempotency key.

An assessment that wins the reservation pins the exact prior release and permits reviewed rollout policy to defer the learner. A rollout that wins changes the effective release before the assessment start recheck. A stale launch then fails with release changed and returns the current learner-safe route. Team start applies the same rule for every frozen member and refuses mixed incompatible release or delivery contexts by default. Late authoritative callbacks still use the exact originally accepted release.

## Recovery by boundary

| Boundary | Stable key or cursor | Commit and retry rule | Invalidated outputs |
| --- | --- | --- | --- |
| Curriculum publication to offering defaults | CourseVersion ID plus manifest digest | Publication commits independently. Default setting requires the current offering revision and exact version. A missing index record does not invalidate the manifest | Staff catalog search |
| Offering default selection versus new admission | Offering revision locked with admission | Commit determines which release is used. New enrollment receives one initial release. Earlier admissions remain pinned | Learner course navigation |
| Enrollment section transfer versus attendance publication | Enrollment and exact occurrence roster snapshot | Verify both occurrence audience and current operator authority. Historical captured membership can still support a reviewed decision | Workspace counts and future schedules |
| Grade release versus learning prerequisite check | GradeResultRevision ID plus grade release version | Allowed gate reads released or approved certified result. A pending or newer unpublished revision does not replace the earlier effective released result | Access cache, next action |
| Package commit after course rollout | PackageRegistration ID plus committed runtime revision | Commit maps exact prior release evidence. Any current carry uses an explicit approved mapping | Historical placement progress |
| Asset safety block while learner opens file | AssetVersion ID, StorageObject version, scoped authorization epoch | Recheck at issue and redemption. Withdrawal prevents new authorized retrieval or range requests | Asset token, renderer cache |
| Group membership revocation and provider add receipt | Local space link, member scope, desired revision and effect key | Stale add receipt cannot restore LMS access. Reconcile removal against current desired provider state | Provider access route |
| Deadline adjustment while learner is submitting | Attempt ID and pinned attempt policy | Existing attempt acceptance uses authoritative policy at start or later approved intervention. Ordinary future schedule edits do not rewrite it | Future actions and calendar display |
| Evidence projector rebuild with live ingest | Release-local source sequence | Rebuild through frozen high-water mark, apply tail under compare-and-swap, then publish the projection | Progress cache and counts |
| Existing completion versus corrected evidence | Exact completion record, source correction revision and reviewed decision | Append correction first. Impact review issues an authorized superseding completion only where policy requires | Affected progress and downstream academic review |

## Worked chronology

At 10:00:00 UTC a teacher approves rollout 20 for learner P from R4 to R5. At 10:00:01 the learner starts a quiz while a rollout worker acquires the same coordination reservation.

| Start wins | Rollout wins |
| --- | --- |
| Attempt A receives R4. Rollout rechecks, sees A active and marks P deferred. Submission S pins R4. After terminal attempt, retry rollout records R5 and the declared carry mapping | R5 becomes effective. Start rechecks and sees stale R4 in the client's access revision. It returns release changed without creating A. The learner refreshes and starts on the authorized R5 activity |

A captured grade or completion event has the authoritative release, delivery, placement and evidence identity. If A's result arrives while R5 is already effective, R4 receives its historical evidence. R5 changes only through an explicit carry decision. Even if learners resume on the same stable placement key, its exact version and rule are recorded independently.

## Monitoring and operator controls

Expose pending, retrying, blocked, stale and settled states on the owning workspace. Show correlation IDs, expected revisions and next scheduled attempt. Do not include raw invitation, collaboration or storage tokens in status. Replays require the same event key and payload digest. An operator bypass uses an authorized corrective command, never manual mutation of a source event. Default retries use capped exponential delays with jitter. Escalate a cross-domain command stuck past its workflow-specific acceptance window to the responsible owner. Continue native operations where provider side effects are independently recoverable.
