# 03. Course publication and release rollout

## States and actors

| State | Entry command and actor | Allowed successor | Visible effect |
| --- | --- | --- | --- |
| draft | Author opens, clones or edits a draft | in_review, abandoned | Editors can preview |
| in_review | Author submits a validated revision and digest | changes_requested, approved, abandoned | Reviewer receives pinned diff |
| changes_requested | Reviewer returns with structured issues | draft, abandoned | Authors can edit and respond |
| approved | Publisher-authorized reviewer approves exact digest | published, draft, abandoned | Same digest can proceed through publication |
| published | Publisher commits a complete manifest | terminal draft state | New immutable version is selectable for offerings |
| abandoned | Owner withdraws with reason and expected revision | terminal draft state | Retained for audit and scheduled removal after holds |

Review approval defaults to independent for assessment-bearing changes and any active-learner rollout. A simple ungraded publication may use self-approval where institutional policy permits. Approval always names exact draft revision, canonical digest, reviewer, timestamp, decision code and required exception sign-offs.

## Publication algorithm

1. Author or import adapter creates a validated draft. Server computes an ordered validation report with machine codes, field paths, blocking flags and named author actions. Drafts can retain open import issues. Required published content cannot.
2. Review pins the canonical manifest inputs. Sign-off records the review policy revision, approved exception codes and digest. A subsequent edit invalidates approval and increments the draft revision.
3. In one curriculum transaction acquire draft and course locks, compare expected draft revision and approved digest, verify idempotency key and permission, and rerun scope, access rights, reference and dependency validation.
4. Assign the next monotonic publication number, materialize exact placement IDs, write the content-addressed manifest, and mark the draft published. The manifest must exist durably before the version becomes visible. An object storage workflow may stage the blob before this transaction and garbage collect unreferenced blobs after a grace window.
5. Append the publication audit and outbox event. Invalidation, indexing and staff notifications follow asynchronously. A retry returns the same publication. A different idempotency key with the same draft digest returns the prior publication link without creating a second version.
6. A publishing request cannot activate an offering. Participation separately schedules or selects the new default publication and creates release assignments using authorized commands.

Freeze ordered placements and exact node, activity, asset, rule and renderer versions plus license and localization inputs. Record the draft and renderer version. Hash canonical JSON with SHA-256 and a declared serialization algorithm such as [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785). Archive a publication by changing availability metadata. Its manifest, academic history and pinned references remain immutable. A withdrawn asset can be excluded from delivery immediately through a safety block independent of manifest integrity.

## Rollout plan and release assignments

A rollout has an offering, one source and target course version, an audience snapshot, state, expected offering revision, planned apply time, author, approver and immutable mapping. Participation owns applying the plan. Curriculum supplies the exact version diff and validates map shape. Plan states are draft, approved, applying, completed, partial and cancelled. Each enrollment has a release row with a half-open effective interval. The same transaction ends the former release and creates the new one. Keep every attempt on the release captured at attempt start.

| Mapping field | Type and meaning |
| --- | --- |
| source_placement_id | UUID of exact prior occurrence |
| target_placement_id | UUID of exact target occurrence, nullable only for removed |
| action | unchanged, equivalent, reset, removed |
| evidence_types | Supported progress evidence carry categories, empty for reset and removed |
| target_anchor_map | Optional reviewed prior block anchor to new block anchor mapping for resume |
| equivalence_basis | Stable reason code and human rationale. Mandatory when content, gate or completion rule differs and carry is requested |
| reviewed_by | Authorized principal for any equivalent or exceptional mapping |

Default automatic mapping uses the stable key and equal canonical payload digest, requiredness, gate version, rule version and relevant media duration. Target positions and locale text can change without invalidating completion only when reviewed under a named equivalence decision. A newly introduced target starts with no progress. A removed source remains in prior history. For changed keys, explicit equivalent mapping must identify the one intended target. Default rejects multiple sources to one target and one source to multiple targets. For split or merged teaching design, retain original evidence and use authorized target completion decisions under the institution's recorded policy.

### Apply and recovery

1. Preview affected enrollments, active attempts, package sessions, prior completions, open deadlines and missing target mappings. Require authorized sign-off for any reset that affects completed or in-progress work.
2. Freeze IDs of target enrollments rather than evaluating a moving roster during execution. Enrollments created later use the offering default, as independently configured.
3. Apply one enrollment per transaction, checking the source release ID and rollout idempotency. If it already applied, return the original new release. If another rollout changed the source, mark this row superseded with the observed release ID. If an assessment or package runtime owns an active attempt, defer by default and retry when the runtime reports terminal state. Assessment start and release rollout acquire the same short per-enrollment coordination reservation, using deterministic UUID order for team members. Both recheck effective release while holding the reservation and release it after their owner transaction. The first operation to commit establishes whether the attempt pins the former release or starts after the switch. An expired or unavailable reservation returns a retryable conflict. It never transfers authority over another domain’s writes.
4. End the prior release and create the target release. Emit a release change and a mapped-progress work item. The next authorization decision reads the new release immediately. A progress read before the projector completes displays updating and may apply the validated map to the old snapshot for a provisional view.
5. Progress projection links permitted source evidence or prior completion decisions to the new release through lineage records. It preserves earned dates and records the carry decision at rollout time. It rechecks any applicable target rule before awarding new completion.
6. Report per-enrollment success, deferral and conflict. A deferred enrollment retains its source release. Retrying updates only pending or deferred rows. A rollback makes a new rollout targeting the old version and follows the same review procedure. Earlier release IDs and awarded records remain readable to authorized staff.

## Example

Thirty learners use version 4. Version 5 moves lesson A, corrects a typo in lesson B and replaces exam X. A has equal delivery semantics and carries accepted completion by default. B carries completion after an independent review confirms equivalent work. X receives a new assessment version and is reset for version 5. A learner in an open X attempt stays on version 4 until submission or expiration. Twenty-nine assignments move on the first pass. A late course enrollment uses version 5 if the offering default already changed. It never appears in the earlier rollout snapshot. Completion generated by X in version 4 remains an academic record even if X is replaced in the curriculum.

| Test | Expected outcome |
| --- | --- |
| Object storage fails between manifest staging and transaction | Publication remains invisible and retry can resume safely |
| Reviewer approves a digest and an author edits a caption before publication | 409 DRAFT_CHANGED, return to review |
| Two workers run the same enrollment rollout concurrently | One target release is written. Both workers report the same release identity |
| A teacher removes the course after previewing a rollout | Applying rechecks current offering state and returns a conflict before assignment |
| Emergency video withdrawal affects a locked prior exam | The compromised asset is inaccessible. The pinned historical attempt survives and authorized staff see the withdrawal reason |
