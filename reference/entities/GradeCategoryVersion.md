# GradeCategoryVersion

Calculation group node pinned to one policy version.

Owned by **records**.

## Fields

### id

Stable globally unique GradeCategoryVersion identifier.

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

### policy_version_id

Parent grade policy in the same offering.

Required. Null is rejected.

References [GradePolicyVersion](GradePolicyVersion.md). Parent grade policy in the same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### category_key

Stable group identity reused across compatible policy versions.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_id

Parent in same policy or null for sole root.

Required. Nullable.

References [GradeCategoryVersion](GradeCategoryVersion.md). Parent in same policy or null for sole root.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### label

Localized category label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### position

Deterministic sibling order.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2047
}
```

### mode

Aggregation method.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "points",
    "equal",
    "weighted",
    "weighted_periods",
    "completion"
  ],
  "default": "points"
}
```

### parent_points

Declared points capacity when parent uses points.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### parent_weight_bps

Contribution weight when parent uses explicit weights.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 10000
}
```

### drop_mode

Candidate limit rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "none",
    "drop_lowest_ratio",
    "drop_highest_ratio",
    "keep_highest",
    "drop_lowest_impact",
    "drop_highest_impact"
  ],
  "default": "none"
}
```

### drop_count

Count required by selected drop or keep mode.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 128,
  "default": 0
}
```

### bonus_mode

Exclusive optional credit rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "none",
    "points",
    "ratio_bonus"
  ],
  "default": "none"
}
```

### bonus_cap_ratio

Maximum ratio of optional bonus contribution.

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

### result_cap_ratio

Maximum normalized result before parent aggregation.

Required. Null is rejected.

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

### propagate_bonus

Permit normalized category above one to parent.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### protected

Prevent category dropping under parent policy.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
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

## Integrity

- Unique root enforced despite nullable parent semantics.
- Depth at most 8 and sibling count at most 128.
- Parent capacities and category weights are required only in corresponding modes.
- Protected unresolved children cannot be dropped.

## Unique keys

- `id`
- `policy_version_id, category_key`
- `policy_version_id, parent_id, position`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| policy_version_id, parent_id, position | Traverse deterministic category graph. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
