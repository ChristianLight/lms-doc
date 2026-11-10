# ExamIncident

Protected operational event and reviewed intervention record.

Owned by **assessment**.

## Fields

### id

Stable globally unique ExamIncident identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Exam context.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Exam context.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Optional affected attempt within same delivery.

Optional. Nullable.

References [Attempt](Attempt.md). Optional affected attempt within same delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### category

Controlled operational incident type.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### status

Restricted investigation status.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "under_review",
    "resolved"
  ]
}
```

### opened_by

Authorized supervisor or service actor.

Required. Null is rejected.

References [Principal](Principal.md). Authorized supervisor or service actor.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### opened_at

Authoritative discovery time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### protected_evidence_ids

Private incident evidence approved for review.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Private incident evidence approved for review.

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

### resolution

Authorized disposition rationale.

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

### disposition

Scoped reviewed action authorized by the decision.

Optional. Nullable.

```json
{
  "type": "string",
  "enum": [
    "no_action",
    "extension_approved",
    "retake_approved",
    "void_approved",
    "escalated"
  ]
}
```

### reviewer_id

Authorized independent reviewer who closed the incident.

Optional. Nullable.

References [Principal](Principal.md). Authorized independent reviewer who closed the incident.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### write_version

CAS token for workflow and protected evidence changes.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

## Integrity

- Proctoring signals do not automatically change a mark.
- Corrections require authorized separate commands.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, status, opened_at | Authorized exam support queue. |

## Retention

Retain independently of ordinary telemetry and under active hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| open | under_review | ClaimExamIncident | Authorized independent reviewer claims open incident. Record protected review authority. |
| under_review | resolved | ResolveExamIncident | Assigned reviewer submits authorized disposition. Freeze reviewed action and reasoning. |
