# CompetencyVersion

Exact competency text, scale and typed edges within one framework version.

Owned by **records**.

## Fields

### id

Stable globally unique CompetencyVersion identifier.

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

### competency_id

Stable competency within same institution and framework.

Required. Null is rejected.

References [Competency](Competency.md). Stable competency within same institution and framework.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### framework_version_id

Exact framework version.

Required. Null is rejected.

References [CompetencyFrameworkVersion](CompetencyFrameworkVersion.md). Exact framework version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_id

Parent inside same framework version if hierarchical.

Required. Nullable.

References [CompetencyVersion](CompetencyVersion.md). Parent inside same framework version if hierarchical.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### prerequisite_ids

Required prior mastery nodes in same version.

Required. Null is rejected.

References [CompetencyVersion](CompetencyVersion.md). Required prior mastery nodes in same version.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 64,
  "minItems": 0,
  "uniqueItems": true
}
```

### title

Approved display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 250
}
```

### description

Definition of expected demonstration.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 6000
}
```

### levels

Ordered declared ordinal levels and optional normalized mapping.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
      },
      "label": {
        "type": "string",
        "minLength": 1,
        "maxLength": 100
      },
      "rank": {
        "type": "integer",
        "minimum": 0,
        "maximum": 100
      },
      "normalized_ratio": {
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
      "code",
      "label",
      "rank",
      "normalized_ratio"
    ],
    "additionalProperties": false
  },
  "maxItems": 32,
  "minItems": 2
}
```

### mastery_level_code

Exact threshold level.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### aggregation_mode

Approved evidence reduction algorithm.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "most_recent",
    "minimum_independent",
    "consecutive",
    "all_criteria"
  ],
  "default": "most_recent"
}
```

### lookback_days

Maximum age of observed evidence, null means no age exclusion.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 36500
}
```

### minimum_count

Number of qualifying observations required.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100,
  "default": 1
}
```

## Integrity

- Level codes and ranks unique.
- Ordinal arithmetic requires explicit numeric mapping.
- No cyclic dependency edge.

## Unique keys

- `id`
- `competency_id, framework_version_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| framework_version_id, parent_id | Traverse versioned competency framework. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
