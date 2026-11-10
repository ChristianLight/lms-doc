# Assessment acceptance scenarios

## ASM-001 — Lost draft update is rejected without partial bindings

Covers `SaveItemDraft`, `ItemVersion`, `ItemCriterionBinding`.

### Given

- Draft revision 7 contains response keys result and method.

### When

- Two authorized writers PUT against revision 7 with different criteria.

### Then

- First accepted creates version 8.
- Second returns DRAFT_CHANGED and neither its interaction nor its criterion is persisted.

### Fixture values

```json
{
  "start_revision": 7,
  "accepted_revision": 8,
  "rejected_status": 412,
  "rejected_code": "DRAFT_CHANGED"
}
```

## ASM-002 — Review binds exact item graph

Covers `ReviewItemVersion`, `PublishItemVersion`, `ItemReviewDecision`.

### Given

- Exam item has approved prompt asset at revision 3 and reviewed digest A.

### When

- Author changes source asset to revision 4 and republishes using approval A.

### Then

- Publication fails because graph digest B does not equal approval A.

### Fixture values

```json
{
  "reviewed_asset_revision": 3,
  "requested_asset_revision": 4,
  "same_approval_valid": false
}
```

## ASM-003 — A frozen item can resolve in history after withdrawal

Covers `WithdrawItemVersion`, `StartAssessmentAttempt`, `AttemptItem`.

### Given

- Attempt ordinal 1 realizes bank item revision 4.

### When

- Publisher withdraws item revision 4.

### Then

- New starts requiring that unavailable fixed item are blocked.
- Historical realized AttemptItem remains readable with exact content and marking rule.

### Fixture values

```json
{
  "item_revision": 4,
  "history_resolves": true,
  "new_start_available": false
}
```

## ASM-004 — Pool solver avoids greedy dead end

Covers `PublishAssessmentVersion`, `StartAssessmentAttempt`, `ItemPoolVersion`.

### Given

- Slot A permits items X and Y. Slot B permits X. Repeats forbidden.

### When

- Realize fixed seed form.

### Then

- B receives X first in constraint order and A receives Y. Presentation order remains A then B.

### Fixture values

```json
{
  "eligible": {
    "A": [
      "X",
      "Y"
    ],
    "B": [
      "X"
    ]
  },
  "resolved": {
    "A": "Y",
    "B": "X"
  },
  "display_order": [
    "A",
    "B"
  ]
}
```

## ASM-005 — Independent authored numeric tolerances compare with exact boundary

Covers `ApproveMarkingRule`, `CompleteEvaluationRun`, `MarkingRuleVersion`.

### Given

- Expected score response is 12.00 with absolute 0.05 and relative 0.01 tolerance, inclusive.

### When

- Evaluate 12.12 and 12.121 against same pinned rule.

### Then

- 12.12 is accepted and 12.121 is rejected.
- Criterion maximum and input precision remain unchanged.

### Fixture values

```json
{
  "expected": "12.00",
  "absolute_tolerance": "0.05",
  "relative_tolerance": "0.01",
  "responses": [
    {
      "input": "12.12",
      "accepted": true
    },
    {
      "input": "12.121",
      "accepted": false
    }
  ]
}
```

## ASM-006 — Affine units distinguish temperatures from differences

Covers `ApproveMarkingRule`, `CompleteEvaluationRun`.

### Given

- Rule pins approved dimensional registry and separate quantity/delta families.

### When

- Evaluate 25 Celsius under quantity and delta rules.

### Then

- Absolute quantity normalizes to 298.15 K.
- Temperature difference normalizes to 25 K.

### Fixture values

```json
{
  "quantity": {
    "input": "25",
    "unit": "Cel",
    "canonical": "298.15"
  },
  "difference": {
    "input": "25",
    "unit": "Cel",
    "canonical": "25"
  }
}
```

## ASM-007 — Correct symbolic value and domain hole are distinct

Covers `MarkingRuleVersion`, `CompleteEvaluationRun`.

### Given

- Expected x+1 and response (x^2-1)/(x-1).

### When

- Evaluate for all real x and for real x excluding 1.

### Then

- All-real comparison fails domain equality.
- Restricted-domain rational value equality succeeds.

### Fixture values

```json
{
  "expected": "x+1",
  "response": "(x^2-1)/(x-1)",
  "tests": [
    {
      "domain": "R",
      "accepted": false
    },
    {
      "domain": "R\\{1}",
      "accepted": true
    }
  ]
}
```

## ASM-008 — Technical scorer failure cannot record a zero

Covers `EvaluationRun`, `RecoverEvaluationLease`, `CompleteEvaluationRun`, `GradeEvidence`.

### Given

- Three criteria have maxima 2, 3 and 5. First two completed 1.5 and 2 points.

### When

- Third criterion lease expires and retry budget remains.

### Then

- Run is requeued and item remains unresolved.
- No earned evidence and no official 3.5/10 score.

### Fixture values

```json
{
  "maxima": [
    "2",
    "3",
    "5"
  ],
  "provisional_points": [
    "1.5",
    "2"
  ],
  "third": "retry_wait",
  "earned_evidence": false
}
```

## ASM-009 — Exclusive hard close overrides extra time unless explicitly extended

Covers `ApproveAssessmentOverride`, `StartAssessmentAttempt`, `SaveAssessmentResponses`, `ExpireAssessmentAttempt`.

### Given

- Exam opens at 08:00 and closes at 10:00 with duration 90 minutes. Learner starts at 08:40 with 30% group extension and individual close 11:00.

### When

- Save at 10:36:59.900 then again at 10:37:00.000.

### Then

- First is admitted. Second is rejected.
- Auto finalization seals latest first-save revision.

### Fixture values

```json
{
  "effective_duration_seconds": 7020,
  "deadline": "2026-11-10T10:37:00Z",
  "admissions": [
    true,
    false
  ]
}
```

## ASM-010 — Independent collaborative fields merge without last-writer-wins

Covers `SaveAssessmentResponses`, `AttemptLease`, `ResponseRevision`.

### Given

- Two authorized team editors hold leases. Response heads A=3 and B=1.

### When

- Editor 1 changes A expected 3. Editor 2 changes B expected 1 and later sends stale A expected 3.

### Then

- A=4 and B=2 remain.
- Stale A gets RESPONSE_CONFLICT.

### Fixture values

```json
{
  "initial_heads": {
    "A": 3,
    "B": 1
  },
  "expected_heads": {
    "A": 4,
    "B": 2
  },
  "stale_error": "RESPONSE_CONFLICT"
}
```

## ASM-011 — Finalization crash is recovered by receipt replay

Covers `SubmitAssessmentAttempt`, `AttemptSubmission`, `AttemptSubmitted`.

### Given

- Candidate saves and finalizes acknowledged draft version 9.

### When

- Durable commit succeeds before HTTP disconnect. Candidate retries same command key.

### Then

- Exact same receipt returned.
- One submission row and one logical AttemptSubmitted event.

### Fixture values

```json
{
  "draft_version": 9,
  "durable_submissions": 1,
  "submission_events": 1,
  "same_receipt": true
}
```

## ASM-012 — Expired evaluator lease cannot commit a late result

Covers `ClaimEvaluationRun`, `CompleteEvaluationRun`, `RecoverEvaluationLease`.

### Given

- Worker A lease expires while computing. Worker B claims requeued run.

### When

- A and then B callback with valid matching inputs.

### Then

- A result rejected. B commits. Identical B retry replays canonical state.

### Fixture values

```json
{
  "accepted_worker": "B",
  "old_worker_response": 409,
  "accepted_result_count": 1
}
```

## ASM-013 — Pending upload missed deadline is excluded

Covers `CompleteAssessmentScan`, `ExpireAssessmentAttempt`, `AttemptSubmission`.

### Given

- Attachment bytes arrived at 10:59 but scan still pending at 11:00 deadline.

### When

- Expiry auto seals at 11:00. Scan succeeds at 11:00:03.

### Then

- Manifest records pending_asset disposition.
- Newly approved asset cannot retroactively enter sealed evidence.

### Fixture values

```json
{
  "deadline": "2026-11-10T11:00:00Z",
  "scan_at": "2026-11-10T11:00:03Z",
  "manifest_disposition": "pending_asset"
}
```

## ASM-014 — Frozen team mark emits one revision per eligible member

Covers `AcceptItemMark`, `TeamSnapshot`, `GradeEvidence`.

### Given

- Three eligible enrollments and an uncredited observer are in frozen team.

### When

- Accept team mark 80/100 and replay accepted event.

### Then

- Exactly three native evidence revisions exist.
- Observer receives none and replay emits no duplicate.

### Fixture values

```json
{
  "eligible": [
    "E1",
    "E2",
    "E3"
  ],
  "observer": "E4",
  "points": "80",
  "maximum": "100",
  "evidence_count": 3
}
```

## ASM-015 — Peer allocator fills constrained positions and handles withdrawal

Covers `AllocatePeerReviews`, `ReplacePeerReview`, `PeerReviewAssignment`.

### Given

- R1 eligible A or B, R2 only A, R3 only C. Each needs one review.

### When

- Allocate then R3 loses eligibility before review.

### Then

- Allocation is R1→B, R2→A and R3→C.
- R3 access revoked and C routed to staff if no replacement.

### Fixture values

```json
{
  "eligible": {
    "R1": [
      "A",
      "B"
    ],
    "R2": [
      "A"
    ],
    "R3": [
      "C"
    ]
  },
  "initial": {
    "R1": "B",
    "R2": "A",
    "R3": "C"
  },
  "withdrawn_fallback": "C"
}
```

## ASM-016 — Moderator adjudicates without disclosing independent marks

Covers `SubmitItemMark`, `ModerateItemMark`, `ReleaseAssessmentFeedback`.

### Given

- Independent scores 7 and 9 on a 10-point item. Threshold is 1 point.

### When

- Submit both and moderator accepts 8 with per-criterion rationale.

### Then

- Candidates see neither provisional score.
- Accepted 8 becomes visible only after explicit feedback release.

### Fixture values

```json
{
  "scores": [
    "7",
    "9"
  ],
  "maximum": "10",
  "trigger_threshold": "1",
  "resolved": "8",
  "released_only_after_approval": true
}
```

## ASM-017 — Regrade respects intervening mark and disclosed decreases

Covers `PreviewAssessmentRegrade`, `ApproveAssessmentRegrade`, `ApplyAssessmentRegradeCase`.

### Given

- Dry run has 9 increases, 6 decreases, and 45 unchanged. Two decreases have manual overrides.

### When

- Approve preserve overrides and no decreases. One increased case receives a concurrent accepted mark before processing.

### Then

- Eight revisions applied.
- One conflict and six decrease exclusions.
- No unchanged record rewritten.

### Fixture values

```json
{
  "population": 60,
  "increases": 9,
  "decreases": 6,
  "manual_override_decreases": 2,
  "changed": 8,
  "conflicted": 1,
  "excluded": 6,
  "unchanged": 45
}
```

## ASM-018 — Unreleased marks are absent from candidate projection

Covers `GetAssessmentFeedback`, `ReleaseAssessmentFeedback`, `ItemMarkRevision`.

### Given

- Candidate has accepted mark and an open exam window. No release.

### When

- Read feedback and inspect notifications and HTML.

### Then

- No marks, answer keys or private comments exposed.
- After authorized close and release points-only returns points and maximum only.

### Fixture values

```json
{
  "before": "withheld",
  "released_fields": [
    "points"
  ],
  "forbidden_fields": [
    "answer_key",
    "private_comments",
    "model_solution"
  ]
}
```

## ASM-019 — External producer cannot target unrelated learner

Covers `AcceptExternalGradeEvidence`, `GradeEvidence`.

### Given

- Package producer is registered for offering A and line A1. Enrollment X belongs to offering B.

### When

- Producer submits score 70/100 for A1 and X.

### Then

- Authorization rejects cross-scope evidence and produces no event.

### Fixture values

```json
{
  "producer_scope": "A/A1",
  "target_enrollment_scope": "B",
  "durable_evidence_count": 0
}
```

## ASM-020 — Correction preserves official historical evidence

Covers `AcceptItemMark`, `GetGradeEvidence`, `GradeEvidenceAccepted`, `GradeEvidence`.

### Given

- Attempt has evidence revision 1 with 75/100 and an official record references it.

### When

- Accept authorized correction to 79/100.

### Then

- Revision 2 links to revision 1.
- Both exact revisions read independently.
- Previously issued academic record does not change automatically.

### Fixture values

```json
{
  "previous": "75",
  "new": "79",
  "current_source_revision": 2,
  "official_record_requires_separate_action": true
}
```

## ASM-021 — Precision requirement preserves original tokens

Covers `ApproveMarkingRule`, `CompleteEvaluationRun`, `ResponseRevision`.

### Given

- Input rule asks for three significant figures.

### When

- Compare original 1.20, 1.2, 0.00450 and ambiguous 1200.

### Then

- 1.20 and 0.00450 pass the precision test.
- 1.2 fails.
- Ambiguous integer notation requires explicit notation under this profile.

### Fixture values

```json
{
  "required_significant_figures": 3,
  "cases": [
    {
      "value": "1.20",
      "pass": true
    },
    {
      "value": "1.2",
      "pass": false
    },
    {
      "value": "0.00450",
      "pass": true
    },
    {
      "value": "1200",
      "pass": false
    }
  ]
}
```

## ASM-022 — Symbolic form criterion depends on equality

Covers `ItemCriterionBinding`, `CompleteEvaluationRun`.

### Given

- Expected x^2+2x+1. Equality worth 3, factored form worth 2 and depends on equality.

### When

- Evaluate expanded correct, factored correct and factored wrong.

### Then

- Return 3, 5 and 0 respectively.

### Fixture values

```json
{
  "cases": [
    {
      "value": "x^2+2x+1",
      "points": "3"
    },
    {
      "value": "(x+1)^2",
      "points": "5"
    },
    {
      "value": "(x+2)^2",
      "points": "0"
    }
  ]
}
```

## ASM-023 — Marker loses evidence access on revocation

Covers `ClaimMarkingAssignment`, `SubmitItemMark`, `MarkingAssignment`.

### Given

- Staff marker was assigned and loaded a scoped evidence view.

### When

- Role revoked before saving mark and opening fresh asset link.

### Then

- Both new protected actions denied.
- Assignment history remains auditable.

### Fixture values

```json
{
  "new_mark_saved": false,
  "new_asset_access": false,
  "existing_assignment_audit": true
}
```

## ASM-024 — Appeal binds actual disclosed revision

Covers `FileAssessmentAppeal`, `DecideAssessmentAppeal`, `AssessmentAppeal`.

### Given

- Candidate has disclosed mark revision 2 and unreleased correction revision 3.

### When

- Candidate files appeal against 3 and then against disclosed revision 2.

### Then

- First is denied without revealing revision 3 status.
- Second creates protected case linked to revision 2.

### Fixture values

```json
{
  "disclosed_revision": 2,
  "held_revision": 3,
  "accepted_target_revision": 2
}
```

## ASM-025 — Negative mapped selections respect published bounds

Covers `InteractionDefinition`, `CompleteEvaluationRun`.

### Given

- A,C correct at +2 each and B,D distract at −1 each with floor 0 and cap 4.

### When

- Evaluate A,C,D and B,D.

### Then

- Points are 3 and 0.
- Reordered selections of same keys yield identical score.

### Fixture values

```json
{
  "weights": {
    "A": 2,
    "B": -1,
    "C": 2,
    "D": -1
  },
  "floor": 0,
  "cap": 4,
  "cases": [
    {
      "selected": [
        "A",
        "C",
        "D"
      ],
      "points": "3"
    },
    {
      "selected": [
        "B",
        "D"
      ],
      "points": "0"
    }
  ]
}
```

## ASM-026 — Agent drafts under bank delegation and cannot publish

Covers `CreateItemBank`, `GrantItemBankAccess`, `CreateItemDraft`, `SubmitItemForReview`, `PublishItemVersion`, `ItemBankGrant`.

### Given

- Institution A administrator creates bank algebra. Principal robot has no bank capabilities.

### When

- Grant robot draft and preview. Robot creates item and submits complete reviewed graph. Robot then requests publication.

### Then

- Draft and review request are attributable to robot.
- Publication denied to robot without an independently granted publisher and review decision.

### Fixture values

```json
{
  "bank_key": "algebra",
  "delegated": [
    "draft",
    "preview"
  ],
  "draft_version": 1,
  "publication_status": 403,
  "independent_publication_required": true
}
```

## ASM-027 — Clone retains meaning while translation retains option identity

Covers `CloneItemDraft`, `SaveItemTranslation`, `PreviewItemAsCandidate`, `ItemTranslation`.

### Given

- Published item revision 2 has interaction choice with options a and b.

### When

- Clone to revision 3, save approved candidate locale with display b then a, and preview exact locale.

### Then

- Both canonical keys resolve under one interaction.
- Display order changes while scoring keys remain unchanged.
- Candidate preview creates zero attempt ordinals.

### Fixture values

```json
{
  "base_revision": 2,
  "draft_revision": 3,
  "locale": "af-NA",
  "displayed_options": [
    "b",
    "a"
  ],
  "preview_attempts": 0
}
```

## ASM-028 — Rubric maximum and free point policy are validated

Covers `PublishRubricVersion`, `RubricCriterion`.

### Given

- Rubric for reasoning has criteria maxima 3 and 2 and two level labels for each.

### When

- Publish declared maximum 4 and then corrected maximum 5 under same newly issued request.

### Then

- First returns INVALID_RUBRIC and commits no revision.
- Corrected rubric publishes at maximum 5 with canonical ordered criteria.

### Fixture values

```json
{
  "criteria_maxima": [
    "3",
    "2"
  ],
  "invalid_total": "4",
  "valid_total": "5",
  "invalid_status": 422
}
```

## ASM-029 — Revoking an evaluator stops work without losing sealed responses

Covers `RegisterEvaluatorRelease`, `ClaimEvaluationRun`, `RevokeEvaluatorRelease`, `CompleteEvaluationRun`, `EvaluatorRelease`.

### Given

- Verified rational evaluator release 4 handles two queued items and one active worker.

### When

- Register release 4, worker claims one item, then security revokes that exact digest before callback.

### Then

- New claims and old callbacks using revoked build fail.
- Both candidate submissions remain sealed and staff can arrange reviewed remediation.

### Fixture values

```json
{
  "release": 4,
  "claims_after_revocation": 0,
  "accepted_callbacks_after_revocation": 0,
  "sealed_submissions_preserved": 2
}
```

## ASM-030 — Reviewed pool and generator survive a later draft edit

Covers `PublishItemPool`, `PublishVariantProfile`, `CreateAssessmentDraft`, `SaveAssessmentDraft`, `PublishAssessmentVersion`.

### Given

- Authorized pool includes algebra items A,B,C, each 2 points. Variant excludes a=0.

### When

- Publish pool and profile, create assessment selecting two items and approve maximum 4. Then author drafts future variant including a=0.

### Then

- Published assembly uses only approved older profile and frozen eligible list.
- New invalid draft remains separate and cannot alter existing assembly.

### Fixture values

```json
{
  "eligible": [
    "A",
    "B",
    "C"
  ],
  "sample_count": 2,
  "max_points": "4",
  "forbidden_a": [
    0
  ],
  "published_profile_revision": 1
}
```

## ASM-031 — Delivery suspension and close block starts while receipts remain

Covers `CreateAssessmentDelivery`, `PublishAssessmentDelivery`, `SuspendAssessmentDelivery`, `ResumeAssessmentDelivery`, `CloseAssessmentDelivery`, `GetAssessmentAvailability`, `GetAssessmentReceipt`.

### Given

- Offering course placement and approved grade item resolve. Formal exam window is open.

### When

- Create and publish delivery. Start and submit A. Suspend and check B. Resume and check B. Close and read A receipt.

### Then

- B sees suspended then can_start before close and closed after.
- A retains the same historical receipt.
- No session starts under suspended or closed state.

### Fixture values

```json
{
  "availability_sequence": [
    "suspended",
    "can_start",
    "closed"
  ],
  "receipt_retained": true,
  "delivered_version": 1
}
```

## ASM-032 — Device takeover revokes writer but preserves localized form

Covers `GetAssessmentAttemptForm`, `TakeOverAssessmentLease`, `SaveAssessmentResponses`, `AttemptLease`.

### Given

- Exam candidate started with old lease A and French Canadian decimal profile. A save committed one accepted response.

### When

- Fetch form on second device, complete fresh authentication, take over with lease B and attempt new saves with A and B.

### Then

- Both authorized reads use same resolved form and saved value.
- Old lease cannot create new revision.
- B can save against exact expected revision.

### Fixture values

```json
{
  "locale": "fr-CA",
  "old_lease": "A",
  "new_lease": "B",
  "initial_response_version": 1,
  "final_response_version": 2
}
```

## ASM-033 — Authorized pause resumes under hard close and abandon preserves quota

Covers `PauseAssessmentAttempt`, `ResumeAssessmentAttempt`, `AbandonAssessmentAttempt`, `AttemptTimingAdjustment`.

### Given

- Formal sitting starts 09:00, duration 60 minutes, close 10:05 and permitted pause 10 minutes. Policy permits abandonment.

### When

- Pause 09:15, resume 09:22 and later abandon before cutoff.

### Then

- Effective deadline is 10:05, not 10:07.
- Pause timeline is preserved.
- Abandoned attempt still consumes original ordinal.

### Fixture values

```json
{
  "pause_seconds": 420,
  "uncapped_deadline": "10:07",
  "effective_deadline": "10:05",
  "terminal_state": "abandoned",
  "ordinal_remains_consumed": true
}
```

## ASM-034 — Exam incident allows extension and reviewed void under exact scope

Covers `OpenExamIncident`, `AdjustAttemptTiming`, `VoidAssessmentAttempt`, `GradeEvidence`.

### Given

- Learner active and network outage verified in own delivery. Deadline 11:00 and staff incident approval permits 15 more minutes.

### When

- Open incident, authorize extension, candidate submits at 11:10, then independent review voids under recorded eligibility decision.

### Then

- Extension admits candidate and leaves original snapshot.
- Void preserves receipt, appends voided evidence if earlier earned evidence existed, and does not erase marks.

### Fixture values

```json
{
  "old_deadline": "11:00",
  "new_deadline": "11:15",
  "submitted_at": "11:10",
  "evidence_disposition": "voided",
  "receipt_preserved": true
}
```

## ASM-035 — Upload verifies scoped digest before scan and preserves earlier answers

Covers `InitiateAssessmentUpload`, `CompleteAssessmentUpload`, `CompleteAssessmentScan`, `AssessmentUpload`.

### Given

- Candidate authorized for a 5 MiB file interaction and previously has accepted text responses.

### When

- Initiate approved 1 MiB PDF with digest H1. Submit completion against staged H2. Retry with new staged target H2 and clean scan.

### Then

- First completion rejects digest mismatch and attaches no file.
- New file becomes approved only after scan.
- Previous text response versions are unchanged.

### Fixture values

```json
{
  "staged_bytes": 1048576,
  "first_result": "UPLOAD_DIGEST_MISMATCH",
  "eligible_files_before_scan": 0,
  "eligible_files_after_scan": 1
}
```

## ASM-036 — Anonymous peer submission exposes sanitized evidence and one immutable review

Covers `PublishPeerReviewPolicy`, `AllocatePeerReviews`, `OpenPeerReview`, `SubmitPeerReview`, `PeerReviewRevision`.

### Given

- Policy requires blinded formative rubric review within offering. Submission includes private author metadata.

### When

- Publish policy, allocate reviewer R1, open and submit completed rubric twice using same key.

### Then

- Reviewer sees pseudonym and sanitized evidence only.
- Exactly one review exists and no official grade evidence emitted.

### Fixture values

```json
{
  "policy_mode": "formative",
  "anonymous": true,
  "incoming_required": 2,
  "review_count_after_retry": 1,
  "native_grade_evidence_count": 0
}
```

## ASM-037 — Reassigned marker cannot submit retained private draft

Covers `ClaimMarkingAssignment`, `SaveItemMarkDraft`, `ReassignMarkingAssignment`, `SubmitItemMark`.

### Given

- Marker M1 claims assignment version 1 with valid evidence.

### When

- M1 saves rubric draft. Coordinator reassigns to M2. M1 attempts submit using stale marker context and M2 saves new draft.

### Then

- M1 draft kept with original author.
- M1 cannot mark after reassignment.
- M2 creates distinct draft and cannot submit M1 work as their own.

### Fixture values

```json
{
  "former_marker": "M1",
  "new_marker": "M2",
  "old_draft_preserved": true,
  "old_marker_submission_status": 403
}
```

## ASM-038 — Stopping correction batch leaves committed cases and exact reconciliation

Covers `PlanAssessmentRegrade`, `RunAssessmentRegrade`, `ApplyAssessmentRegradeCase`, `StopAssessmentRegrade`, `GetAssessmentRegrade`.

### Given

- Approved batch contains four native evidence cases.

### When

- Plan, preview and approve. Run batch with limit one, apply its correction, stop batch and read status.

### Then

- Exactly one case updated.
- No additional case admitted after stop.
- Protected reconciliation shows one changed and outstanding cases without rolling back.

### Fixture values

```json
{
  "planned": 4,
  "batch_limit": 1,
  "changed": 1,
  "unprocessed": 3,
  "state": "stopped"
}
```

## ASM-039 — Finish requires terminal disposition for every case

Covers `RunAssessmentRegrade`, `FinishAssessmentRegrade`, `GetAssessmentRegrade`.

### Given

- Correction batch has three planned cases, two terminal and one awaiting worker.

### When

- Request completion, finish pending work and request completion again.

### Then

- First fails with no completed event.
- Second finalizes counters and emits one completion.

### Fixture values

```json
{
  "planned": 3,
  "terminal_at_first_request": 2,
  "changed": 1,
  "conflicted": 1,
  "unchanged": 1,
  "final_event_count": 1
}
```

## ASM-040 — Appeal reassignment, closure and candidate withdrawal preserve history

Covers `FileAssessmentAppeal`, `AssignAssessmentAppeal`, `DecideAssessmentAppeal`, `CloseAssessmentAppeal`, `WithdrawAssessmentAppeal`.

### Given

- Disclosed mark revision 2 belongs to learner and previous marker is not independent.

### When

- File and assign distinct reviewer, decide and close after notification. File a different disclosed revision appeal and withdraw before decision.

### Then

- First case closes with independent rationale and evidence hold history.
- Second records withdrawal and changes no mark.

### Fixture values

```json
{
  "disclosed_mark_revision": 2,
  "original_marker": "M1",
  "independent_reviewer": "M2",
  "first_final_state": "closed",
  "second_final_state": "withdrawn"
}
```

## ASM-041 — One-use exam approval survives idempotent retry and prevents revoked admission

Covers `IssueExamAccessGrant`, `RevokeExamAccessGrant`, `StartAssessmentAttempt`, `ExamAccessGrant`.

### Given

- Delivery D requires independent exam approval. Learner E holds available valid grant G1 and another unused G2.

### When

- Revoke G2 then attempt start with it. Start with G1 and retry identical key.

### Then

- G2 creates no ordinal.
- G1 consumed exactly once with attempt 1 and retry returns same ID.

### Fixture values

```json
{
  "delivery": "D",
  "grants": {
    "G1": "consumed",
    "G2": "revoked"
  },
  "attempt_count": 1,
  "same_start_receipt": true
}
```

## ASM-042 — An expiring retake grant cannot reset attempt ordinal

Covers `GrantAttemptAllowance`, `StartAssessmentAttempt`, `AttemptAllowance`.

### Given

- Base quota one used. Reviewed allowance adds one start before 12:00.

### When

- Start at 11:59 then retry. In isolated initial state try exactly at 12:00.

### Then

- First creates ordinal 2 and consumes one allowance.
- Retry replays ordinal 2.
- Exact expiry creates no attempt and consumes no grant.

### Fixture values

```json
{
  "base_limit": 1,
  "old_ordinal": 1,
  "new_ordinal": 2,
  "new_consumed_count": 1,
  "inclusive_expiry_allowed": false
}
```

## ASM-043 — Practice check infrastructure error consumes no tries

Covers `CheckPracticeResponse`, `PracticeCheck`.

### Given

- Practice attempts allow two explicit checks and candidate has saved response revision 5.

### When

- First request gets worker outage. Recover worker and evaluate accepted revision. Replay same successful key.

### Then

- Outage records no counted check.
- Successful evaluation creates sequence 1 and safe feedback.
- Replay does not increase count or emit grade evidence.

### Fixture values

```json
{
  "check_limit": 2,
  "response_revision": 5,
  "after_outage": 0,
  "after_retry": 1,
  "evidence_emitted": false
}
```

## ASM-044 — Branch decision persists exact threshold and refuses unsafe outage shortcut

Covers `ResolveAssessmentBranch`, `AssessmentBranchDecision`.

### Given

- Formative section routes less than 2 to R, 2 to less than 4 to S and 4 to T.

### When

- Run boundary case score 2 and an independent worker-outage case. Reload each attempt.

### Then

- 2 routes S and remains S after reload.
- Outage remains pending and does not select remediation as though answer incorrect.

### Fixture values

```json
{
  "thresholds": [
    "2",
    "4"
  ],
  "exact_score": "2",
  "target": "S",
  "outage_route": "pending"
}
```

## ASM-045 — Worker input projection is bound to lease and assigned item only

Covers `ClaimEvaluationRun`, `GetEvaluationInputs`, `CompleteEvaluationRun`.

### Given

- Approved worker W1 owns run for item Q1 on submission S. Other scorer W2 has lease for Q2.

### When

- Fetch Q1 inputs with valid W1 lease, then with W2 lease and after revoking W1.

### Then

- W1 receives only Q1 scoped responses and necessary rule values.
- Both foreign or revoked attempts denied. No input from Q2 or unrelated learners disclosed.

### Fixture values

```json
{
  "allowed_item": "Q1",
  "foreign_item": "Q2",
  "foreign_access_status": 403,
  "after_revocation_status": 403
}
```

## ASM-046 — Course rollout cannot retarget an active or concurrently starting assessment

Covers `GetAssessmentAvailability`, `StartAssessmentAttempt`, `GetAssessmentAttemptForm`, `Attempt`, `TeamSnapshot`, `GradeEvidence`.

### Given

- Enrollment E current release R4 maps to P4 and offering now has R5 placement P5 available for rollout. Team candidates likewise each carry an exact release.

### When

- Race start for R4 against approved rollout to R5. In isolated states make each owner win. Submit a started R4 attempt after later approved rollout.

### Then

- If start reservation wins, attempt pins R4/P4 and rollout defers.
- If rollout wins, stale start gets ENROLLMENT_RELEASE_CHANGED and consumes no ordinal.
- Historical form and native grade evidence retain R4.
- Mixed-release team cannot bind P4.

### Fixture values

```json
{
  "initial_release": "R4",
  "target_release": "R5",
  "old_placement": "P4",
  "new_placement": "P5",
  "stale_error": "ENROLLMENT_RELEASE_CHANGED",
  "start_wins_evidence_release": "R4",
  "mixed_release_team_allowed": false
}
```

## ASM-047 — Team membership edit does not reset attempt limit

Covers `StartAssessmentAttempt`, `GetAssessmentAvailability`, `TeamSnapshot`, `AttemptAllowance`.

### Given

- Group G at roster revision 2 starts and submits its only default attempt. Staff changes membership to revision 3.

### When

- Try starting G without allowance, then issue one reviewed allowance and try again with eligible aligned releases.

### Then

- New roster alone cannot reset quota.
- Approved retake commits ordinal 2 with a new TeamSnapshot and keeps original ordinal 1 and its membership intact.

### Fixture values

```json
{
  "group": "G",
  "old_roster_revision": 2,
  "new_roster_revision": 3,
  "new_roster_without_allowance": "limit_exceeded",
  "retake_ordinal": 2
}
```

## ASM-048 — Incident approval cannot be inferred from a proctoring alert

Covers `OpenExamIncident`, `ClaimExamIncident`, `ResolveExamIncident`, `VoidAssessmentAttempt`, `ExamIncident`.

### Given

- Supervisor reports activity on a submitted exam and opens a restricted incident.

### When

- Attempt void before resolution. Independent reviewer claims and resolves no_action. Try void again.

### Then

- Both void requests denied.
- Receipt and earned evidence remain intact.
- Audit shows independent evidence reviewed.

### Fixture values

```json
{
  "disposition": "no_action",
  "allowed_voids": 0,
  "receipt_remains_authoritative": true
}
```

## ASM-049 — Revocation races a pending unused retake allowance

Covers `GrantAttemptAllowance`, `RevokeAttemptAllowance`, `StartAssessmentAttempt`, `AttemptAllowance`.

### Given

- Reviewed allowance has two remaining starts and previous attempts preserved.

### When

- Race next start against allowance revocation under same authorization guard.

### Then

- If start wins exactly one start remains recorded and coordinator must retry against new count.
- If revocation wins no new start consumes the grant.

### Fixture values

```json
{
  "original_available": 2,
  "start_wins_consumed": 1,
  "revocation_wins_consumed": 0,
  "prior_attempts_removed": 0
}
```

## ASM-050 — Assembly review becomes invalid after the pool revision changes

Covers `ReviewAssessmentAssembly`, `SaveAssessmentDraft`, `PublishAssessmentVersion`, `AssessmentAssemblyReview`.

### Given

- Review R approves digest A with pinned pool P2.

### When

- Draft changes to reviewed candidate pool P3. Publish digest B with R.

### Then

- Publication denies stale approval.
- Fresh approved digest B required even if P2 and P3 have same item count.

### Fixture values

```json
{
  "old_pool_revision": 2,
  "new_pool_revision": 3,
  "old_approval_still_applies": false
}
```

## ASM-051 — A self-reflection is separate from anonymous peer marks and official grades

Covers `SubmitAssessmentSelfReview`, `SelfReviewRevision`, `GradeEvidence`.

### Given

- Individual candidate has sealed coursework and policy enables self review under rubric R.

### When

- Candidate submits self score 8/10. A different enrolled candidate tries same endpoint.

### Then

- Owner has one immutable private reflection.
- Other candidate denied.
- Official grade evidence unchanged.

### Fixture values

```json
{
  "self_points": "8",
  "maximum": "10",
  "foreign_candidate_status": 403,
  "grade_evidence_delta": 0
}
```

## ASM-052 — A distinct concurrent team start cannot obtain another editor lease

Covers `StartAssessmentAttempt`, `GetAssessmentAvailability`, `AttemptLease`, `TakeOverAssessmentLease`.

### Given

- Eligible team editors E1 and E2 are authorized for the same stable group. E1 commits its active attempt first.

### When

- E2 sends a distinct start request against the same membership revision. E1 retries its exact committed request.

### Then

- E2 receives ATTEMPT_ALREADY_ACTIVE and can fetch the candidate-owned attempt pointer through availability without a lease token.
- E1 receives its original start receipt. A valid separate lease or takeover follows the published access policy.

### Fixture values

```json
{
  "original_writer": "E1",
  "distinct_caller": "E2",
  "distinct_start_status": 409,
  "distinct_start_lease_disclosed": false,
  "exact_replay_same_receipt": true
}
```
