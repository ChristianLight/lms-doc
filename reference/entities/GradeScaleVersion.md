# GradeScaleVersion

Published numeric, ordinal or completion scale with exact threshold and presentation policy.

Owned by **records**.

## Fields

### id

Stable globally unique GradeScaleVersion identifier.

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

### scale_key

Stable grade scale family identifier within institution.

Required. Null is rejected.

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

### name

Staff display name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### state

Current publication lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "superseded",
    "retired"
  ],
  "default": "draft"
}
```

### scale_type

Permitted interpretation of grade bands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "percentage",
    "ordinal",
    "completion"
  ],
  "default": "percentage"
}
```

### locale

Default approved label locale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9-]+$",
  "default": "en"
}
```

### cap_ratio

Maximum representable ratio, inclusive.

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

### bands

Ordered immutable bands with versioned GPA mapping.

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
      "lower": {
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
      },
      "upper": {
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
      },
      "gpa_points": {
        "oneOf": [
          {
            "type": "string",
            "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
          },
          {
            "type": "null"
          }
        ]
      },
      "passed": {
        "type": "boolean"
      },
      "sort_order": {
        "type": "integer",
        "minimum": 0,
        "maximum": 255
      }
    },
    "required": [
      "code",
      "label",
      "lower",
      "upper",
      "gpa_points",
      "passed",
      "sort_order"
    ],
    "additionalProperties": false
  },
  "maxItems": 256,
  "minItems": 1
}
```

### display_rounding

Decimal display rounding only by default.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "half_up",
    "half_even",
    "truncate"
  ],
  "default": "half_up"
}
```

### display_places

Number of displayed decimal percentage places.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 4,
  "default": 2
}
```

### threshold_basis

Threshold comparison basis.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "exact",
    "display_rounded"
  ],
  "default": "exact"
}
```

### published_at

Publication instant.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Published percentage bands have positive range, cannot overlap and cover zero through cap. Ordinal and completion bands have null numeric bounds and a unique ordered code.
- Final upper limit inclusive and remaining upper limits exclusive.
- Scale label changes require new revision.

## Unique keys

- `id`
- `institution_id, scale_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, scale_key | Find selectable scale families and approved versions. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishGradeScale | All bands, caps and scope valid Freeze revision and announce publication. |
