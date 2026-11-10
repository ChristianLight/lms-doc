# Records acceptance scenarios

## REC-001 — Publish exact grade scale and draft gradebook

Covers `CreateGradeScaleDraft`, `PublishGradeScale`, `CreateGradePolicyDraft`, `PutGradeCategory`, `PutGradeItemRule`, `PreviewGradePolicy`, `PublishGradePolicy`.

### Given

- An approved offering needs Algebra grading with a 50 percent passing band and a points root.
- Teacher has no grade-read delegation but may design the draft.

### When

- Registrar drafts/publishes the scale. Instructor sets two grade lines, previews synthetic scores, and registrar publishes the same digest.

### Then

- 55/100 maps to Pass. Policy owns exactly one root and two leaf revisions.
- Actual learner examples require separate read permission. Duplicate sibling order or overlapping bands blocks publication.

### Fixture values

```json
{
  "items": [
    {
      "code": "quiz",
      "maximum": "10",
      "score": "8"
    },
    {
      "code": "exam",
      "maximum": "90",
      "score": "47"
    }
  ],
  "expected_percent": "55.00",
  "expected_state": "published"
}
```

## REC-002 — Policy assignment activates atomically

Covers `StageGradePolicyAssignments`, `ActivateGradePolicyAssignments`, `GradePolicyAssignment`, `GradePolicyAdoptionBatch`.

### Given

- Three active enrollments have policy revision 1. Two are in the approved adoption scope.

### When

- Stage revision 2 for two releases effective at 2026-08-01, then change one predecessor before activation.
- Recompute and activate a fresh preview.

### Then

- Stale batch changes neither enrollment. Fresh batch switches exactly two enrollments at the same boundary. Third remains on revision 1.

### Fixture values

```json
{
  "scope_count": 2,
  "outside_scope_count": 1,
  "effective_at": "2026-08-01T00:00:00Z",
  "expected_error": "PREVIEW_STALE"
}
```

## REC-003 — Source evidence retries and out-of-order accepted corrections

Covers `ConsumeGradeEvidence`, `RecordGradeCoverage`, `CalculateGradeResult`, `GradeEvidenceReceipt`, `GradeCoverageSnapshot`, `GradeResultRevision`, `GradeContribution`.

### Given

- Native attempt A earned 20/40 at sequence 2 and corrected 30/40 at sequence 3. Source checkpoints are complete.

### When

- Deliver E3 then E2 then repeat E3. Freeze coverage and calculate at a checkpoint including E3.

### Then

- One current attempt score 3/4. E2 remains historical. No duplicate calculation on equal fingerprint.
- Same tuple and conflicting lineage digest quarantines input and cannot change result.

### Fixture values

```json
{
  "source_order": [
    3,
    2,
    3
  ],
  "score_by_sequence": {
    "2": "20",
    "3": "30"
  },
  "maximum": "40",
  "expected_ratio": {
    "numerator": "3",
    "denominator": "4"
  }
}
```

## REC-004 — Confirmed missing stays distinct from submitted pending

Covers `RecordGradeCoverage`, `CalculateGradeResult`, `GetGradebook`, `GetGradeExplanation`.

### Given

- One visible scored item is 8/10, one is excused, another 10-point item submitted and pending.

### When

- Calculate current and final. Then reconcile authenticated absence evidence for another identical learner without a submission.

### Then

- First learner final pending, current 80 percent. Second learner final 8/20 after confirmed missing.
- Learner explanation does not reveal staff-only sources.

### Fixture values

```json
{
  "scored": {
    "points": "8",
    "maximum": "10"
  },
  "pending_maximum": "10",
  "excused_maximum": "20",
  "current_percent": "80.00",
  "confirmed_missing_final_percent": "40.00"
}
```

## REC-005 — Exact ratio and impact modes produce distinct drops

Covers `CalculateGradeResult`, `GetGradeExplanation`, `GradeCategoryVersion`.

### Given

- A 50/50, B 65/100 and C 12/24 are counted under equal source validity.

### When

- Apply one drop in ratio mode and then separately sequential points impact mode.

### Then

- Ratio drops C and computes 23/30. Impact drops B and computes 31/37. Neither rounds before threshold.

### Fixture values

```json
{
  "scores": [
    {
      "key": "A",
      "points": "50",
      "maximum": "50"
    },
    {
      "key": "B",
      "points": "65",
      "maximum": "100"
    },
    {
      "key": "C",
      "points": "12",
      "maximum": "24"
    }
  ],
  "ratio_drop": {
    "key": "C",
    "numerator": "23",
    "denominator": "30",
    "display": "76.67"
  },
  "impact_drop": {
    "key": "B",
    "numerator": "31",
    "denominator": "37",
    "display": "83.78"
  }
}
```

## REC-006 — Lateness and attempt choice keep raw evidence

Covers `CalculateGradeResult`, `GradeContribution`, `GradeItemVersion`.

### Given

- Item maximum 40, raw 33 submitted 71 minutes after due, grace 10 and one point per commenced hour, capped 8. A second on-time attempt earned 30.

### When

- Calculate under highest and average approved policies.

### Then

- First adjusts to 31 but raw source is unchanged. Highest is 31/40. Average is 61/80.

### Fixture values

```json
{
  "raw": "33",
  "max": "40",
  "late_minutes": 71,
  "grace_minutes": 10,
  "interval_minutes": 60,
  "deduction": "2",
  "highest": "77.50",
  "average": "76.25"
}
```

## REC-007 — Override conflict preserves released grade

Covers `RequestGradeOverride`, `DecideGradeOverride`, `GradeOverrideDecision`, `CalculateGradeResult`.

### Given

- Grade 74.20 was already released. New request proposes 77.00 against its base.

### When

- Accept a source correction to 76.00 before the override reviewer approves. Refresh request and approve.

### Then

- Old request stale, fresh override computes 77.00 with 76.00 as computed lineage. Learner still sees 74.20 until correction release.

### Fixture values

```json
{
  "released": "74.20",
  "new_computed": "76.00",
  "approved_effective": "77.00",
  "approval_role": "registrar"
}
```

## REC-008 — Leased regrade preview has no partial official changes

Covers `StartRecalculationRun`, `ProcessRecalculationTarget`, `ApplyRecalculationRun`, `RecalculationTarget`.

### Given

- Registrar selects 2 targets and new algorithm grade-calc-v2. One worker crashes after staging.

### When

- Retry expired lease with same input and complete preview. Change one target source before all-or-nothing apply.

### Then

- No duplicate candidate. Apply rejects stale digest and neither pointer changes. Existing releases unaffected.

### Fixture values

```json
{
  "targets": 2,
  "stale_targets": 1,
  "all_or_nothing": true,
  "expected_changed_pointers": 0
}
```

## REC-009 — Final release is atomic and can be withdrawn with audit

Covers `StageGradeRelease`, `ActivateGradeRelease`, `WithdrawGradeRelease`, `GradeRelease`, `GradeReleaseEntry`.

### Given

- Two authorized overlapping staged manifests refer to same prior learner visibility pointer.

### When

- Activate A and then B. Withdraw A with recorded exposure reason.

### Then

- A activates once, B rejects stale. Withdrawal revokes future learner access and leaves audit.

### Fixture values

```json
{
  "eligible": 1,
  "blocking": 0,
  "manifest_a_result": "active",
  "manifest_b_error": "PREVIEW_STALE",
  "withdrawn_pointer_visible": false
}
```

## REC-010 — Period closure and narrow correction window

Covers `BeginGradePeriodClosure`, `CloseGradePeriod`, `OpenGradeCorrectionWindow`, `ResealGradePeriod`, `GradeCorrectionWindow`.

### Given

- 30 expected enrollments, 28 graded, 1 incomplete approved, 1 pending required.

### When

- Prepare close, approve remaining recognized disposition, close. Open a named correction window for one result, correct and reseal.

### Then

- Initial close blocked. Final close keeps 30 dispositions. A different target fails authorization during correction.

### Fixture values

```json
{
  "roster": 30,
  "pre_close_blockers": 1,
  "allowed_correction_targets": 1,
  "outside_scope_targets": 29,
  "final_state": "resealed"
}
```

## REC-011 — Appeal follows ownership boundaries

Covers `SubmitGradeAppeal`, `AssignGradeAppeal`, `ResolveGradeAppeal`, `GradeAppeal`.

### Given

- Learner released grade on May 4 and submits appeal May 12 under 14-day policy.

### When

- Assign independent reviewer and resolve changed only after approved correction release.

### Then

- Original appeal pins first release. Item error corrected at source. Only public outcome text visible to learner.

### Fixture values

```json
{
  "release_at": "2026-05-04T10:00:00Z",
  "appeal_at": "2026-05-12T10:00:00Z",
  "days_allowed": 14,
  "outcome": "changed"
}
```

## REC-012 — Report card staged, rendered, issued and corrected

Covers `CreateReportTemplateDraft`, `PublishReportTemplate`, `ApproveAcademicComment`, `StageReportCard`, `RenderAcademicDocument`, `IssueReportCard`, `GetAcademicDocument`, `VoidAcademicDocument`, `ReportCardRevision`.

### Given

- A learner has two published interim grades and an approved comment, one additional staff-only comment.

### When

- Publish accessible template, stage and render report, issue, download, then void due to discovered source error.

### Then

- Issued report includes only permitted comment, artifact hash stable after void, active verification reports void.

### Fixture values

```json
{
  "published_grade_count": 2,
  "visible_comment_count": 1,
  "private_comment_count": 1,
  "mime_type": "application/pdf",
  "expected_state": "void"
}
```

## REC-013 — Transcript captures GPA and supports restricted external disclosure

Covers `CreateTranscriptTemplateDraft`, `PublishTranscriptTemplate`, `StageTranscript`, `RenderAcademicDocument`, `IssueTranscript`, `RequestRecordDisclosure`, `DecideRecordDisclosure`, `DeliverRecordDisclosure`, `TranscriptRevision`.

### Given

- Algebra 3x4, History 4x3, Lab 2 pass/fail and Biology 3x0.

### When

- Issue transcript at cutoff, approve purpose-scoped destination and deliver. Later revoke future disclosure.

### Then

- GPA 24/10 equals 2.40. Earned credits 9. No Lab GPA denominator. Retain earlier byte digest and deny future recipient download after revoke.

### Fixture values

```json
{
  "quality_points": "24",
  "gpa_units": "10",
  "gpa": "2.40",
  "earned_units": "9",
  "destination_purpose": "admission"
}
```

## REC-014 — Build versioned programme and admit a learner

Covers `CreateProgram`, `CreateCreditSchemeDraft`, `PublishCreditScheme`, `CreateProgramRequirementDraft`, `PutProgramRequirement`, `PublishProgramRequirements`, `EnrollInProgram`.

### Given

- Institutional unit conversion 1:1 and programme needs 12 total and 6 resident units.

### When

- Draft and publish credit scheme and exact programme rule graph, then admit learner under version 1.

### Then

- Learner remains pinned to version 1 after version 2 is drafted. Duplicate active admission is blocked.

### Fixture values

```json
{
  "programme": "SCI",
  "credits_min": "12",
  "residency_min": "6",
  "version": 1
}
```

## REC-015 — Review recognized credit and separate waiver from award

Covers `RequestRecognition`, `ReviewRecognition`, `DecideRecognition`, `RecordCreditDecision`, `DecideProgramRequirement`, `CreditDecision`, `RequirementDecision`.

### Given

- Learner requests transfer Chemistry worth 3 units and a zero-credit prerequisite waiver.

### When

- Verify issuer and person. Independent registrar approves credit and exact waiver. Replay request.

### Then

- Only one 3-unit transfer award, no GPA impact. Waived prerequisite grants zero credit.

### Fixture values

```json
{
  "transfer_units": "3",
  "waiver_credit": "0",
  "gpa_eligible": false,
  "approved_awards": 1
}
```

## REC-016 — Overlapping elective pools need deterministic allocation

Covers `RunProgramAudit`, `GetProgramAudit`, `ProgramAuditResult`, `ProgramAuditRuleResult`.

### Given

- Group A accepts Astronomy or Chemistry. Group B accepts only Chemistry. Both need 3.

### When

- Evaluate same evidence twice and check search bounds.

### Then

- Use Astronomy for A and Chemistry for B. 6 distinct units. Exact replay same fingerprint. Bound exhaustion returns needs_review without award.

### Fixture values

```json
{
  "group_a": [
    "Astronomy",
    "Chemistry"
  ],
  "group_b": [
    "Chemistry"
  ],
  "credits_each": "3",
  "expected_total": "6",
  "expected_state": "satisfied"
}
```

## REC-017 — Competency corrected observation and renewal evidence

Covers `CreateCompetencyFrameworkDraft`, `PutCompetencyDefinition`, `PublishCompetencyFramework`, `CreateCompetencyAlignment`, `RecordCompetencyEvidence`, `EvaluateCompetency`, `CompetencyDecision`.

### Given

- A level 3 day 10, B level 4 day 30. Two independent current level 3 observations required.

### When

- Correct B to level 2. Add independent C level 3 at day 40. Evaluate at day 40 and day 221.

### Then

- Before C only one qualifying. Day 40 demonstrated, day 221 expired. Prior decisions preserved.

### Fixture values

```json
{
  "minimum_level": 3,
  "minimum_independent_count": 2,
  "lookback_days": 180,
  "A": {
    "day": 10,
    "level": 3
  },
  "B": {
    "day": 30,
    "revised_level": 2
  },
  "C": {
    "day": 40,
    "level": 3
  }
}
```

## REC-018 — Issue verifiable credential, then record revocation and renewal separately

Covers `ApproveQualification`, `CorrectQualification`, `CreateCredentialDefinitionDraft`, `PublishCredentialDefinition`, `IssueCredential`, `TransitionCredential`, `VerifyCredential`, `CredentialStatusEvent`.

### Given

- Satisfied exact programme audit, approved opaque verification definition with only issuer and status visible.

### When

- Approve award, issue once despite retry, verify, revoke with authorized reason and try to reinstate revoked record.

### Then

- Verification valid then revoked. Same issue retry returns same credential. Terminal revocation prevents reinstatement. New renewal may issue different ID.

### Fixture values

```json
{
  "approved_audit": "satisfied",
  "verification_mode": "opaque_link",
  "issue_retries": 2,
  "expected_issued_credentials": 1,
  "revocation_terminal": true
}
```

## REC-019 — Analytics uses correct denominators and protected export

Covers `CreateMetricDefinitionDraft`, `PublishMetricDefinition`, `BuildAcademicMetricSnapshot`, `GetAcademicMetricSnapshot`, `RequestAcademicReportExport`, `GetAcademicReportExport`, `MetricSnapshot`, `AcademicReportExport`.

### Given

- 40 eligible enrollments, 32 final pass/fail, 28 pass, 4 fail, 3 incomplete and 5 unresolved. One group contains 7 distinct persons.

### When

- Publish metric, generate cutoff snapshot and export, then revoke caller scope.

### Then

- Pass rate 87.50 percent, finalized coverage 80.00 percent. Suppress small cell and companion cells as needed. Download after scope revocation denied.

### Fixture values

```json
{
  "eligible": 40,
  "passed": 28,
  "failed": 4,
  "incomplete": 3,
  "unresolved": 5,
  "small_group": 7,
  "suppression_threshold": 10,
  "expected_pass_percent": "87.50"
}
```

## REC-020 — Early intervention uses complete source and human review

Covers `CreateInterventionRuleDraft`, `PublishInterventionRule`, `EvaluateInterventionRules`, `RecordInterventionAction`, `GetInterventionQueue`, `InterventionCase`.

### Given

- Learner has 2 confirmed overdue required tasks within 14 days and one optional task. Another learner has missing source checkpoint.

### When

- Run rule twice, assign case and dismiss after corrected due date.

### Then

- Exactly one case. No case for incomplete data. No automatic learner notification or grade changes.

### Fixture values

```json
{
  "required_overdue": 2,
  "optional_overdue": 1,
  "lookback_days": 14,
  "same_window_retries": 2,
  "cases_created": 1,
  "final_state": "dismissed"
}
```

## REC-021 — Hidden grades do not leak through totals

Covers `GetGradebook`, `GetGradeExplanation`, `GradeReleaseEntry`.

### Given

- Two 10-point grades exist, 9/10 released and 1/10 withheld.

### When

- Learner queries gradebook and requests staff-only revision explanation by ID.

### Then

- Visible learner aggregate 90 percent, staff preview 50 percent. Private revision returns 404 and no evidence IDs.

### Fixture values

```json
{
  "released_points": "9",
  "unreleased_points": "1",
  "item_maximum": "10",
  "learner_percent": "90.00",
  "staff_percent": "50.00",
  "private_revision_status": 404
}
```

## REC-022 — Substituted initial evidence cannot grant duplicate credits

Covers `RecordCreditDecision`, `RunProgramAudit`, `StageTranscript`.

### Given

- Same equivalent local course passed twice at 3 units, grades 4.0 and 3.0. Default credits earliest pass and GPA all.

### When

- Audit and issue transcript snapshot from both approved sources.

### Then

- Earned credits 3, GPA 3.50 with denominator 6. Both attempts visible according to profile.

### Fixture values

```json
{
  "credit_each": "3",
  "grade_points": [
    "4",
    "3"
  ],
  "expected_earned": "3",
  "expected_gpa": "3.50",
  "expected_gpa_credits": "6"
}
```
