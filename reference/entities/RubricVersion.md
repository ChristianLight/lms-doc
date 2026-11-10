# RubricVersion

Immutable scoring rubric with criterion and point policy.

Owned by **assessment**.

## Fields

### id

Stable globally unique RubricVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution within which the rubric can be shared.

Required. Null is rejected.

References [Institution](Institution.md). Institution within which the rubric can be shared.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_key

Institution-scoped rubric series key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### revision

Positive version ordinal.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### label

Human-readable rubric title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### maximum

Published total maximum before combining with other criteria.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### digest

Digest over ordered criteria, level and display settings.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### published_by

Rubric publisher.

Required. Null is rejected.

References [Principal](Principal.md). Rubric publisher.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_at

Release instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### overall_feedback_prompt

Protected authorized reviewer guidance for overall feedback.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "format": {
        "type": "string",
        "enum": [
          "sanitized_html",
          "text",
          "asset",
          "math"
        ]
      },
      "value": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50000
      },
      "asset_version_id": {
        "type": "string",
        "format": "uuid"
      },
      "accessible_text": {
        "type": "string",
        "minLength": 1,
        "maxLength": 4000
      }
    },
    "required": [
      "key",
      "format",
      "value"
    ],
    "additionalProperties": false
  },
  "maxItems": 16,
  "minItems": 1
}
```

### overall_feedback_default

Protected default overall reviewer feedback text subject to ordinary validation.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

## Integrity

- Sum criterion maxima to rubric total.
- Published rubric graph immutable.
- A zero maximum rubric may be completed and reviewed without emitting earned numeric GradeEvidence.

## Unique keys

- `id`
- `institution_id, rubric_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, rubric_key | Rubric series browsing. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
