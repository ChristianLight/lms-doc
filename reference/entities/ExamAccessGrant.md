# ExamAccessGrant

Single-use institutional admission approval scoped to a candidate delivery.

Owned by **assessment**.

## Fields

### id

Stable globally unique ExamAccessGrant identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Only the authorized delivery can consume this grant.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Only the authorized delivery can consume this grant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Candidate enrollment scoped to the same offering.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Candidate enrollment scoped to the same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### method

Approved institutional verification method.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "institutional_identity",
    "supervisor",
    "external_verified",
    "short_passcode"
  ]
}
```

### state

Available, consumed or revoked authority. Expired is derived when an available grant reaches valid_until.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "available",
    "consumed",
    "revoked",
    "expired"
  ]
}
```

### valid_from

Inclusive start of grant validity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### valid_until

Exclusive validity end.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approved_by

Authorized examiner or verifier.

Required. Null is rejected.

References [Principal](Principal.md). Authorized examiner or verifier.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### consumed_by_attempt_id

Durable attempt consuming this grant.

Optional. Nullable.

References [Attempt](Attempt.md). Durable attempt consuming this grant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- One use per grant.
- Grant is consumed only after valid attempt creation.
- Never hold identity documents in grant record.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, enrollment_id, state, valid_until | Find scoped currently eligible grants. |

## Retention

Retain grant and review events through assessment retention, then purge token and unnecessary method details.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| available | consumed | StartAssessmentAttempt | Candidate meets all admission requirements. Bind grant to committed sitting. |
| available | revoked | RevokeExamAccessGrant | Authorized exam supervisor records reason. Block all future use. |
