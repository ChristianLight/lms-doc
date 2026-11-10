# DeliveryPolicyVersion

Immutable effective access, time, submission and disclosure settings.

Owned by **assessment**.

## Fields

### id

Stable globally unique DeliveryPolicyVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Target delivery that owns this policy.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Target delivery that owns this policy.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic policy version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### opens_at

Earliest admissible candidate action.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### due_at

Instant after which admissible submissions are classified late.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### closes_at

Exclusive candidate mutation cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### time_zone

IANA zone used to interpret authored local schedule.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### duration_seconds

Optional elapsed sitting limit.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 604800
}
```

### attempt_limit

Allowed formal starts, with null meaning unlimited.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### navigation

Default navigation control.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "free",
    "section_linear",
    "item_linear"
  ]
}
```

### expiry

Automatic submit or expire disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "auto_submit",
    "expire"
  ]
}
```

### review

Field-by-field disclosure model and timing.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "mode": {
      "type": "string",
      "enum": [
        "immediate",
        "after_close",
        "staff_release",
        "never"
      ]
    },
    "fields": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "response",
          "points",
          "rubric",
          "comments",
          "answer_key",
          "model_solution"
        ]
      },
      "minItems": 0,
      "maxItems": 6
    },
    "delay_seconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2592000
    }
  },
  "required": [
    "mode",
    "fields"
  ],
  "additionalProperties": false
}
```

### pause_total_seconds

Maximum approved pause time, zero by default.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### requires_blank_acknowledgement

Require candidate confirmation for unanswered entries.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### published_at

Effective version release time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### require_exam_grant

Whether to consume an independent authorized one-use grant at start. Defaults false.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### practice

Optional formative check and hint behavior.

Optional. Nullable.

```json
{
  "type": "object",
  "properties": {
    "check_limit": {
      "type": "integer",
      "minimum": 0,
      "maximum": 1000
    },
    "allow_hints": {
      "type": "boolean"
    },
    "delay_answer_until_exhaustion": {
      "type": "boolean"
    },
    "same_response_repeat": {
      "type": "boolean"
    }
  },
  "required": [
    "check_limit",
    "allow_hints",
    "delay_answer_until_exhaustion",
    "same_response_repeat"
  ],
  "additionalProperties": false
}
```

### self_review

Optional candidate-only self-reflection profile and frozen rubric.

Optional. Nullable.

```json
{
  "type": "object",
  "properties": {
    "rubric_version_id": {
      "type": "string",
      "format": "uuid"
    },
    "opens_at": {
      "type": "string",
      "format": "date-time"
    },
    "closes_at": {
      "type": "string",
      "format": "date-time"
    },
    "required": {
      "type": "boolean"
    }
  },
  "required": [
    "rubric_version_id",
    "required"
  ],
  "additionalProperties": false
}
```

## Integrity

- When both present due is on or before close.
- Admission window is half-open.
- Exam requires explicit close and bounded duration by default.

## Unique keys

- `id`
- `delivery_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, revision | Locate captured policy version. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
