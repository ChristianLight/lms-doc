# 04 Evidence intake, corrections and regrade

## Importing authoritative grade evidence

Subscribe to GradeEvidenceAccepted. Verify producer identity, schema and event envelope. Persist the receipt in an inbox with unique producer and event identifier. Resolve the pointer to GradeEvidence through a scoped read. Validate tenant, offering, enrollment, stable grade item and permitted source-kind. For native evidence verify the AssessmentDelivery relationship and exact AssessmentVersion. For a package or external provider, verify approved identity, attempt mapping, declared score and policy. Store the consumed source sequence and accepted pointer in GradeEvidenceReceipt. A result calculation references the original evidence revision through GradeContribution. Do not copy answers, protected exam content or grader notes into academic records.

Each source object has a sequence ordered by its owner. Each grade item can have multiple source objects for eligible attempts. Receiving sequence 3 and then 2 keeps both valid historical pointers but only 3 can be current at a later source cutoff. A duplicate by source identity and revision with the same digest is harmless. A conflicting digest is a quarantine incident. Unknown grade item or unmapped person yields an operator queue entry without a grade mutation. Reconciliation detects expected source streams whose checkpoints stopped before an active cutoff. A pending source with no accepted evidence cannot become an automatic missing zero.

When a source event and enrollment release or grade policy activation race, acknowledge the immutable event and resolve it at the pinned calculation cutoff. Do not drop evidence merely because the current policy changed. If no policy ever authorizes the source, quarantine. If a source event arrives after official release, compute a proposed difference and record a late evidence task. Leave the released pointer intact.

An offline grade entry goes through Assessment's AcceptExternalGradeEvidence command with source_kind manual. The assessment evidence remains the source for Academic Records. The staff member must be authorized for the learner and grade item. The UI must confirm a range, source time and reason when editing earlier evidence. A teacher entering valid offline evidence is supplying a new source mark. A teacher changing a policy-derived output without changing its source is requesting an override.

## Corrections by ownership

| Situation | Correct route | Result |
| --- | --- | --- |
| Wrong answer key, rubric decision or grading script | Assessment regrade | New Assessment evidence revision, followed by Records recalculation |
| Correct source score associated with wrong learner | Owning source correction with identity review | Source void and valid reattribution. No direct Records reassignment. |
| Valid assessment score but wrong applicability, due date or accommodation | Delivery or Assessment policy owner | New authorized eligibility evidence. Recalculate affected results. |
| Gradebook arithmetic defect | Records calculation engine correction | New algorithm version, dry run and reviewed replay |
| Grade scale or weighting policy needs changing | Records policy revision and adoption plan | Prospective by default, explicit retroactive review if authorized |
| Exceptional staff judgment on a computed item or final grade | Records override | Approved GradeOverrideDecision, separate visible effective result |
| Mistaken release to audience | Records exposure incident and authorized withdrawal | Superseding visibility event plus privacy handling. Earlier downloads cannot be recalled. |
| Incorrect issued report or transcript | Registrar replacement issuance | New immutable document, with previous version marked superseded |

## Official override

An instructor submits an override request scoped to one GradeResult and anchored to its current computed revision. Provide kind, requested numeric result or disposition, rationale, supporting references, effective instant and optional expiry for provisional overrides. Types are numeric item result, outcome code, incomplete, withdrawal, authorized credit-related correction and full computed course mark. A gradebook override cannot grant programme credit directly. Credit remains an independent decision.

Validate numeric overrides against the relevant maximum and permitted scale. Block a pass that contradicts a mandatory grade gate unless the request also has a separately authorized gate exception. A final outcome without numeric adjustment preserves the computed numeric ratio. A full numeric correction records before/after numbers and explains the threshold or basis. Store staff-only reason separately from a learner-facing explanation.

A different authorized reviewer approves official overrides. Approval rechecks the target result, current policy, evidence cutoff and period state. If any material input changed, mark the request stale and ask for a new preview. Rejection leaves earlier state unchanged. Approval appends a GradeOverrideDecision and a new GradeResultRevision, and queues affected ancestor calculations. Approval alone does not release either result or reason. Revoke by new decision and calculate again from underlying sources. A new raw evidence revision never silently removes an override. Recalculate and flag the override for review if the approved source fingerprint changed.

**Example.** A released course grade is 74.20 percent from revision R7. Staff request an academic judgment result of 77.00 with approved justification. Before approval, Assessment regrades the last item, producing R8 at 76.00. The R7 request becomes stale. Approval of a renewed R8 request creates an effective 77.00 revision and keeps 76.00 as computed lineage. The previously released 74.20 remains visible until the correction release. Cancelling the override returns the effective calculation to the newest approved computed result, subject to another release.

## Recalculation

An authorized RecalculationRun has scope, mode, pinned old/new policy and algorithm, selected target set, input checkpoint, reason and report digest. Default mode is preview. Capture all learner identifiers before work starts. Each RecalculationTarget references a GradeResult and current revision. Order batches by stable key. A worker claims one target with a short lease, replays immutable sources, records the candidate and a difference, and acknowledges the lease. Retries are idempotent using run plus result plus input fingerprint.

Display categorized deltas for score, pass state, eligibility, visibility, credit consequence and award consequence. Include unchanged counts and exact reasons. Approval compares the review digest and permitted scope. If the candidate was computed against stale evidence, do not silently recompute during apply. Reject or remove that target from the approved subset and require another preview. A whole-period retroactive change defaults to all-or-nothing activation. Store candidate rows and atomically switch an approved policy/publication guard after all candidates have passed validation. A preview can finish with quarantined or failed targets, but a final release never treats those as complete.

The worker may compute and stage independent revisions without affecting audience. Record committed official releases separately. A crash while committing a target may only leave either both revision and outbox or neither. Duplicate or timeout recovery repeats the same stable key. Result pointers use compare-and-swap. Historical documents remain available to authorized readers and explicitly marked superseded after a replacement.

## Appeals and explainability

The learner can request review of a released grade, within institution-configured deadline. Product default is 14 calendar days from the release timestamp in the relevant time zone. A registrar can accept a late appeal with a reason. The appeal pins the release entry and scope. A reviewer records received, assigned, evidence requested, upheld, changed or withdrawn. A change invokes the appropriate source correction or override path. Outcome text is released separately from internal notes. Appeal record remains even if the grade correction is later superseded.

Show learners the exact contributing released evidence allowed for that audience, effective weights, drop and excusal rationale, whether results are provisional or final and when decisions were released. Do not reveal alternate learner identities, hidden sources, moderation notes or unreleased questions. Provide an accessible explanation table and screen-reader status announcements, with separate staff-only lineage.
