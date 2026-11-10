# AssessmentSectionVersion

Ordered section in one published assessment assembly.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentSectionVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Parent assessment assembly.

Required. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Parent assessment assembly.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Stable section key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### display_order

Unique section ordinal.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### label

Candidate section title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### navigation

Free or locked sequencing policy.

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

### duration_seconds

Optional independent section timer.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 604800
}
```

### coverage

Constrained item coverage by tags.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "tag": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "minimum": {
        "type": "integer",
        "minimum": 0,
        "maximum": 500
      },
      "maximum": {
        "type": "integer",
        "minimum": 0,
        "maximum": 500
      }
    },
    "required": [
      "tag",
      "minimum",
      "maximum"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 64
}
```

## Integrity

- Coverage minimum cannot exceed maximum.
- Section clock cannot extend the attempt deadline.

## Unique keys

- `id`
- `assessment_version_id, key`
- `assessment_version_id, display_order`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assessment_version_id, display_order | Realize ordered section navigation. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
