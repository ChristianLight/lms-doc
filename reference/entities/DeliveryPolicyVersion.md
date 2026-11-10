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
          "model_solution",
          "correctness",
          "hints",
          "targeted_feedback"
        ]
      },
      "maxItems": 9,
      "minItems": 0
    },
    "delay_seconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2592000
    },
    "field_rules": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "field": {
            "type": "string",
            "enum": [
              "response",
              "points",
              "rubric",
              "comments",
              "answer_key",
              "model_solution",
              "correctness",
              "hints",
              "targeted_feedback"
            ]
          },
          "mode": {
            "type": "string",
            "enum": [
              "immediate",
              "after_close",
              "staff_release",
              "never",
              "on_demand",
              "after_due",
              "after_attempt",
              "after_attempt_or_due",
              "after_attempt_count",
              "after_exhaustion",
              "after_correct",
              "after_exhaustion_or_correct",
              "after_exhaustion_or_due",
              "after_correct_or_due"
            ]
          },
          "attempt_threshold": {
            "type": "integer",
            "minimum": 1,
            "maximum": 1000
          },
          "boundary": {
            "type": "string",
            "enum": [
              "at_or_after",
              "strictly_after"
            ]
          },
          "deadline_basis": {
            "type": "string",
            "enum": [
              "due_at",
              "closes_at"
            ]
          }
        },
        "required": [
          "field",
          "mode"
        ],
        "additionalProperties": false
      },
      "maxItems": 9,
      "minItems": 0
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
    },
    "allow_staff_bypass": {
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

### submission_validation

Configured candidate finalization precondition. Omission retains existing blank acknowledgement behavior.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "acknowledge_blanks",
    "enforce_required",
    "require_any"
  ]
}
```

### submission_wait_seconds

Minimum delay between admitted scored submissions for the same candidate and delivery. Omission means no configured delay. Draft saving remains available during the wait.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2592000
}
```

### show_rubric_during_response

Explicit reviewed visibility of permitted rubric descriptors before candidate submission. Omission withholds.

Optional. Null is rejected.

```json
{
  "type": "boolean"
}
```

### retry_form_mode

Preserve original immutable form for subsequent eligible attempts under the same compatible assessment version when configured. Omission draws a new form.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "new_form",
    "retain_first_form"
  ]
}
```

## Integrity

- When both present due is on or before close.
- Admission window is half-open.
- Exam requires explicit close and bounded duration by default.
- A field-specific disclosure mode applies only to its unique named field. Missing field-specific modes fall back to the published legacy review mode for authorized fields.
- An attempt threshold is required only for after_attempt_count. A due rule declares its boundary semantics when a compatibility profile differs from the default.
- Staff bypass of required self review is disabled by default. If enabled, an authorized explicit moderation disposition must record the reason and source policy.
- A required or require-any submission must meet all named channel requirements before ordinary finalization. Expiry without qualifying evidence cannot fabricate a submission.
- Retain-first-form requires compatible course placement and assessment version, authorized current dependencies and a new independent attempt/evidence identity.

## Unique keys

- `id`
- `delivery_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, revision | Locate captured policy version. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
