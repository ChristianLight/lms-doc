# AssessmentAppeal

Challenge to a disclosed assessment mark and its evidence.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentAppeal identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Disclosed candidate attempt.

Required. Null is rejected.

References [Attempt](Attempt.md). Disclosed candidate attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Candidate beneficiary within scope.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Candidate beneficiary within scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### mark_revision_id

Exact disclosed mark challenged.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). Exact disclosed mark challenged.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### category

Reason classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### reason

Protected learner explanation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### filed_at

Authoritative intake time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Case review lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "filed",
    "screening",
    "assigned",
    "decided",
    "closed",
    "withdrawn"
  ]
}
```

### reviewer_id

Scope-authorized independent adjudicator.

Optional. Nullable.

References [Principal](Principal.md). Scope-authorized independent adjudicator.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision

Resolution when decided.

Optional. Nullable.

```json
{
  "type": "string",
  "enum": [
    "uphold",
    "correct",
    "dismiss",
    "escalate"
  ]
}
```

### decision_reason

Protected adjudication rationale.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### resolved_at

Decision time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### protected_evidence_ids

Protected appeal evidence stored under this case and institutional retention.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Protected appeal evidence stored under this case and institutional retention.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

## Integrity

- One active appeal per learner and challenged revision.
- Appeal cannot overwrite a submitted response or official academic result.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, state, filed_at | Candidate case tracking. |
| reviewer_id, state, filed_at | Independent review queue. |

## Retention

Retain under appeal policy and legal holds. Keep evidentiary references until closure and retention expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| filed | assigned | AssignAssessmentAppeal | Authorized coordinator selects eligible reviewer. Assign independent case reviewer. |
| assigned | decided | DecideAssessmentAppeal | Assigned reviewer records decision and scope. Freeze appeal resolution and permitted follow-up. |
| filed | withdrawn | WithdrawAssessmentAppeal | Appealing learner requests withdrawal before decision. Close active case without altering evidence. |
| decided | closed | CloseAssessmentAppeal | Notification and decision reconciliation complete. Seal workflow closure. |
