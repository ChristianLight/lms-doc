# AssessmentOverride

Approved policy delta for one learner, section or learning group.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentOverride identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Delivery subject to accommodation.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Delivery subject to accommodation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scope_kind

Enrollment, Section or LearningGroup.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "Enrollment",
    "Section",
    "LearningGroup"
  ]
}
```

### scope_id

UUID of applicable scope in same offering.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Override record version in scope.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### effective_from

Inclusive approval effect.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_until

Exclusive interval end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### deltas

Only approved field values with explicit types.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "opens_at": {
      "type": "string",
      "format": "date-time"
    },
    "due_at": {
      "type": "string",
      "format": "date-time"
    },
    "closes_at": {
      "type": "string",
      "format": "date-time"
    },
    "duration_seconds": {
      "type": "integer",
      "minimum": 1,
      "maximum": 604800
    },
    "attempt_limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 1000
    },
    "duration_factor_numerator": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100
    },
    "duration_factor_denominator": {
      "type": "integer",
      "minimum": 1,
      "maximum": 100
    },
    "alternate_assessment_version_id": {
      "type": "string",
      "format": "uuid"
    },
    "pause_total_seconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 3600
    },
    "alternate_presentation_profile": {
      "type": "string",
      "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
    }
  },
  "required": [],
  "additionalProperties": false
}
```

### reason_code

Non-sensitive reason category.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### approved_by

Accommodation approver for the delivery.

Required. Null is rejected.

References [Principal](Principal.md). Accommodation approver for the delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### protected_reference

Opaque protected support document link.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Enrollment takes precedence over group fields.
- Reject same-priority conflicts.
- Support information is separate and access-restricted.

## Unique keys

- `id`
- `delivery_id, scope_kind, scope_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, scope_kind, scope_id, effective_from | Resolve applicable per-field accommodation. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
