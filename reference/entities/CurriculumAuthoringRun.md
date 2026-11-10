# CurriculumAuthoringRun

Idempotent staged agent curriculum workflow for a specific draft and exact accepted source versions.

Owned by **curriculum**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_course_draft_id

Exact authorized draft.

Required. Null is rejected.

References [CourseDraft](CourseDraft.md). Must resolve to an authorized CourseDraft in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expected_draft_revision

Draft compare-and-swap revision from approved plan.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### platform_job_id

Coordinator lease and checkpoint job.

Required. Null is rejected.

References [PlatformJob](PlatformJob.md). Same institution, job_kind course_import and target type CurriculumAuthoringRun.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requested_by_id

Accountable authoring requester.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### agent_principal_id

Scoped authoring service identity.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_extraction_run_ids

Exact sealed source evidence versions.

Required. Null is rejected.

References [SourceExtractionRun](SourceExtractionRun.md). Every source is sealed, authorized and belongs to same institution.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 20,
  "minItems": 1,
  "uniqueItems": true
}
```

### request_fingerprint

Canonical authorized brief, exact extraction set, target and expected revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### brief_object_id

Sealed purpose, teaching brief, allowed provider and privacy constraints.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Same institution and Platform evidence purpose. Input brief is exact and owned by target CourseDraft; an immutable scoped run copy may be linked once the run exists.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### stage

Current pipeline stage.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "coverage_plan",
    "course_plan",
    "learning_blocks",
    "assessment_candidates",
    "verification",
    "apply_plan",
    "owner_apply"
  ],
  "default": "coverage_plan"
}
```

### stage_manifest_object_id

Latest sealed candidate or apply checkpoint manifest.

Optional. Nullable.

References [StorageObject](StorageObject.md). Same institution. Platform purpose evidence and exact owner CurriculumAuthoringRun. Resolve actual object version and digest before use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### stage_manifest_digest

Exact stage artifact digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### approved_plan_digest

Exact reviewed candidate selection and target draft fingerprint.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### approved_by_id

Independent human apply approver.

Optional. Nullable.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Exact review instant.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Authoring run lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "planned",
    "generating",
    "ready_for_review",
    "changes_requested",
    "approved",
    "applying",
    "applied",
    "blocked",
    "canceled"
  ],
  "default": "planned"
}
```

### revision

Expected run revision used by stage and approval commands.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### created_at

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Every selected source and owner effect rechecks current rights and scope.
- Candidate and approved plan manifests are protected immutable StorageObjects.
- The authoring run cannot publish courses or create offerings, attempts, learner evidence or official grades.
- Apply must be selection-closed and bound to exact sealed inputs and draft revision.

## Unique keys

- `id`
- `institution_id, requested_by_id, target_course_draft_id, request_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| target_course_draft_id, state, created_at | Draft authoring history and pending work. |
| platform_job_id, state | Reconcile owner effects and job outcomes. |

## Retention

Retain protected decisions while needed for reviewed source derivation and retention policy or hold. Retain authorized academic lineage tombstone after eligible source disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| planned | generating | RecordCurriculumAuthoringStage | First coverage output and authorized job fence. Seal stage candidate manifest. |
| generating | ready_for_review | RecordCurriculumAuthoringStage | Validated apply plan and candidate dependency closure. Expose exact candidate digest to human reviewer. |
| ready_for_review | changes_requested | ReviewCurriculumAuthoringRun | Human reviewer recorded needed corrections. Invalidate old apply digest. |
| ready_for_review | approved | ReviewCurriculumAuthoringRun | Independent approval and unchanged exact candidate and draft inputs. Pin approval and candidate selection. |
| changes_requested | generating | RecordCurriculumAuthoringStage | Authorized new candidate revision with corrections. Preserve old decision and seal new stage output. |
| approved | applying | ApplyCurriculumAuthoringSelection | Reviewed exact plan and current target revisions. Schedule bounded owner writes. |
| applying | applied | RecordCurriculumAuthoringStage | All selected owner receipts reconciled. Record exact applied draft revision and lineage receipts. |
| applying | blocked | RecordCurriculumAuthoringStage | Owner conflict or mandatory dependency unresolved. Retain completed draft outputs and record blockers. |
| blocked | generating | RecordCurriculumAuthoringStage | Replanned authorized input digest and refreshed target. Revalidate candidate selection and require new approval. |
| planned | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| generating | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| ready_for_review | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| changes_requested | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| approved | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| applying | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
| blocked | canceled | CancelCurriculumAuthoringRun | Authorized actor and current run revision. Fence pending effects and retain committed owner receipts. |
