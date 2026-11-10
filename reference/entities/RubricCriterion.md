# RubricCriterion

Stable rubric criterion and approved levels or free points.

Owned by **assessment**.

## Fields

### id

Stable globally unique RubricCriterion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_version_id

Rubric revision defining marks and descriptors.

Required. Null is rejected.

References [RubricVersion](RubricVersion.md). Rubric revision defining marks and descriptors.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Stable criterion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### display_order

Distinct ordinal within rubric.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### description

Candidate-safe marking description.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### maximum

Maximum criterion points.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### point_step

Positive increment for authorized free-point scoring.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### levels

Available stable level keys and point values.

Optional. Nullable.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "level_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "label": {
        "type": "string",
        "minLength": 1,
        "maxLength": 160
      },
      "descriptor": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2000
      },
      "points": {
        "type": "string",
        "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
      }
    },
    "required": [
      "level_key",
      "label",
      "descriptor",
      "points"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 30
}
```

### scoring_mode

Explicit scoring mode. Without it, infer levels or free points from the existing payload.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "levels",
    "free_points",
    "feedback_only"
  ]
}
```

### feedback_mode

Configured marker comment requirement for this criterion. Omission uses existing workflow.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "none",
    "optional",
    "required"
  ]
}
```

### label

Optional reviewed display heading separate from the detailed criterion description.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

## Integrity

- Exactly one of level mode and free-point step applies.
- Score and level must agree within published bounds.
- Feedback-only criterion has maximum zero, no free-point step and at most one explicit zero level. A required comment must be present when marked.

## Unique keys

- `id`
- `rubric_version_id, key`
- `rubric_version_id, display_order`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| rubric_version_id, display_order | Build consistent rubric form. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
