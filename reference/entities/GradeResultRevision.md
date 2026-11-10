# GradeResultRevision

Immutable official candidate or computed grade output with exact lineage.

Owned by **records**.

## Fields

### id

Stable globally unique GradeResultRevision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_result_id

Stable target within same offering and enrollment.

Required. Null is rejected.

References [GradeResult](GradeResult.md). Stable target within same offering and enrollment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Enrollment in the named offering and institution.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment in the named offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assignment_id

Exact applicable policy assignment at this result cutoff.

Required. Null is rejected.

References [GradePolicyAssignment](GradePolicyAssignment.md). Exact applicable policy assignment at this result cutoff.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scale_version_id

Exact mapping and presentation scale.

Required. Null is rejected.

References [GradeScaleVersion](GradeScaleVersion.md). Exact mapping and presentation scale.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Prior result revision in same target.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). Prior result revision in same target.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### override_decision_id

Approved effective decision, if any.

Required. Nullable.

References [GradeOverrideDecision](GradeOverrideDecision.md). Approved effective decision, if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic immutable revision number within its stable identity.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### status

Academic result state for this revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "graded",
    "missing_zero",
    "pending",
    "excused",
    "not_applicable",
    "not_due",
    "incomplete",
    "withdrawn",
    "transfer",
    "failed_calculation"
  ]
}
```

### ratio

Exact computed effective ratio. Null for nonnumeric disposition.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### computed_ratio

Unmodified calculated ratio for an approved override, otherwise same as ratio.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### band_code

Exact published scale band. Null for nonnumeric disposition.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### outcome

Separate academic outcome from measured numeric ratio.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pass",
    "fail",
    "incomplete",
    "withdrawn",
    "exempt",
    "pending",
    "not_applicable"
  ]
}
```

### display_percent

Rendered canonical percentage decimal for display.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 24
}
```

### threshold_failed

Independent required gate did not pass.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### algorithm_version

Reference calculation algorithm version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### cutoff_at

Academic as-of cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### source_vector

Ordered producer sequence bounds and fingerprints.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "producer": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9._-]{0,63}$"
      },
      "partition": {
        "type": "string",
        "minLength": 1,
        "maxLength": 128
      },
      "sequence": {
        "type": "integer",
        "minimum": 0,
        "maximum": 9007199254740991
      },
      "digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      }
    },
    "required": [
      "producer",
      "partition",
      "sequence",
      "digest"
    ],
    "additionalProperties": false
  },
  "maxItems": 4096,
  "minItems": 0
}
```

### fingerprint

Canonical deterministic lineage and result fingerprint.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### calculation_kind

Purpose and eligibility rules applied.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "current_staff",
    "final",
    "correction"
  ]
}
```

## Integrity

- Numeric score exists only for numeric status.
- Result score is reduced rational with bounded integer size.
- Exact pre-display threshold evaluated under pinned scale.
- Row remains immutable after release or supersession.

## Unique keys

- `id`
- `grade_result_id, revision`
- `grade_result_id, fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, enrollment_id, created_at | Resolve result timeline and stage releases. |
| grade_result_id, created_at | Explain revision history. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
