# GradeItemVersion

Exact gradebook line rule and source mapping in one policy.

Owned by **records**.

## Fields

### id

Stable globally unique GradeItemVersion identifier.

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

### grade_item_id

Stable grade line within same offering.

Required. Null is rejected.

References [GradeItem](GradeItem.md). Stable grade line within same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Owning policy version within offering.

Required. Null is rejected.

References [GradePolicyVersion](GradePolicyVersion.md). Owning policy version within offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### category_id

Parent category in the same policy.

Required. Null is rejected.

References [GradeCategoryVersion](GradeCategoryVersion.md). Parent category in the same policy.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_delivery_id

Native delivery in same offering, when used.

Required. Nullable.

References [AssessmentDelivery](AssessmentDelivery.md). Native delivery in same offering, when used.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_key

Pinned placement identity if required for curriculum linkage.

Required. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_kind

Authorized authoritative evidence family.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native",
    "manual",
    "package",
    "external",
    "completion"
  ]
}
```

### source_dimension

Approved named score dimension where a source has split outputs.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### position

Stable order among grade items within the category.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2047
}
```

### academic_period_id

Grading and reporting period within same institution.

Required. Nullable.

References [AcademicPeriod](AcademicPeriod.md). Grading and reporting period within same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### maximum

Points capacity for numeric item, positive when counted.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### weight_bps

Weight in weighted parent.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 10000
}
```

### counting_kind

Ordinary, optional credit or noncounting line.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "ordinary",
    "bonus",
    "formative"
  ],
  "default": "ordinary"
}
```

### required_for_final

Unresolved applicable evidence blocks final result.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### protected

Item cannot be dropped.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### allow_low_stakes_release

Eligible for separately enabled automatic release.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### late_policy

Exact grace, deduction and cap parameters.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "mode": {
      "type": "string",
      "enum": [
        "none",
        "fixed_max_fraction",
        "interval_max_fraction",
        "interval_points"
      ]
    },
    "grace_ms": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2592000000
    },
    "interval_ms": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2592000000
    },
    "deduction": {
      "type": "string",
      "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
    },
    "deduction_cap": {
      "type": "string",
      "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
    },
    "floor_points": {
      "type": "string",
      "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
    }
  },
  "required": [
    "mode",
    "grace_ms",
    "interval_ms",
    "deduction",
    "deduction_cap",
    "floor_points"
  ],
  "additionalProperties": false
}
```

### gate_policy

Required independent passing condition where configured.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "kind": {
      "type": "string",
      "enum": [
        "none",
        "minimum_ratio",
        "required_completion"
      ]
    },
    "threshold": {
      "oneOf": [
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
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "kind",
    "threshold"
  ],
  "additionalProperties": false
}
```

### attempt_selection

Optional item-specific attempt policy.

Required. Nullable.

```json
{
  "type": "string",
  "enum": [
    "latest",
    "first",
    "highest",
    "average",
    "manual_selection"
  ]
}
```

## Integrity

- Native requires scoped AssessmentDelivery and exact placement match.
- One counting binding per native delivery and version unless distinct source dimension has explicit approval.
- Bonus or formative work never blocks final.
- Grade maximum and source maximum match or use approved deterministic normalization.

## Unique keys

- `id`
- `grade_item_id, policy_version_id`
- `category_id, position`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| policy_version_id, category_id, position | Evaluate and explain category contributions. |
| policy_version_id, assessment_delivery_id, source_dimension | Validate authorized assessment grade binding. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
