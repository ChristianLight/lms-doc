# AttemptAllowance

Reviewed bounded extra sitting capacity or resubmission grant.

Owned by **assessment**.

## Fields

### id

Stable globally unique AttemptAllowance identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Scoped delivery whose base quota may be extended.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Scoped delivery whose base quota may be extended.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Individual eligible enrollment if not a team grant.

Optional. Nullable.

References [Enrollment](Enrollment.md). Individual eligible enrollment if not a team grant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learning_group_id

Stable same-offering team recipient when not an individual grant.

Optional. Nullable.

References [LearningGroup](LearningGroup.md). Stable same-offering team recipient when not an individual grant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### previous_attempt_id

Prior linked attempt for retake or remediation.

Optional. Nullable.

References [Attempt](Attempt.md). Prior linked attempt for retake or remediation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason_kind

Distinguishes sanctioned retake and resubmission purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "retake",
    "resubmission",
    "alternate_sitting",
    "remediation"
  ]
}
```

### count

Maximum extra starts under this allowance.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### consumed_count

Committed extra starts count.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### valid_from

Inclusive validity start.

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

Authorized instructor or coordinator.

Required. Null is rejected.

References [Principal](Principal.md). Authorized instructor or coordinator.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Audited instructional or incident reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### revoked_at

Optional unused allowance cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Exactly one candidate identity.
- Count positive and consumed count cannot exceed count.
- Ordinal never resets.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, enrollment_id, valid_until | Find available individual grants. |
| delivery_id, learning_group_id, valid_until | Find team resubmission grants. |

## Retention

Retain through all linked attempts and approved appeal retention.
