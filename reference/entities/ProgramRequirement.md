# ProgramRequirement

Typed requirement node in a published programme version.

Owned by **records**.

## Fields

### id

Stable globally unique ProgramRequirement identifier.

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

### requirement_version_id

Owning programme requirement version.

Required. Null is rejected.

References [ProgramRequirementVersion](ProgramRequirementVersion.md). Owning programme requirement version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_id

Parent in same version or null root.

Required. Nullable.

References [ProgramRequirement](ProgramRequirement.md). Parent in same version or null root.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_key

Stable rule code in version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### priority

Order for deterministic group satisfaction.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 255
}
```

### rule_kind

Typed logic expression kind.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "all",
    "any_count",
    "course",
    "credit_pool",
    "residency",
    "gpa",
    "competency"
  ]
}
```

### eligible_course_ids

Approved institutional courses for selected leaf or pool.

Required. Null is rejected.

References [Course](Course.md). Approved institutional courses for selected leaf or pool.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 1000,
  "minItems": 0,
  "uniqueItems": true
}
```

### competency_version_id

Exact required competency definition if applicable.

Required. Nullable.

References [CompetencyVersion](CompetencyVersion.md). Exact required competency definition if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### minimum_credit

Minimum credit for credit pool or residency.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### minimum_count

Required child outcome count for any-count group.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 256
}
```

### minimum_ratio

Required exact grade ratio when applicable.

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

### currency_days

Maximum age at audit when configured.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 36500
}
```

### allow_double_use

Allow explicitly reviewed credit reuse across local requirements.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

## Integrity

- Parameters match rule kind.
- All references within same institution.
- Double use does not increase overall distinct credit total.

## Unique keys

- `id`
- `requirement_version_id, rule_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| requirement_version_id, parent_id, priority | Traverse deterministic requirement graph. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
