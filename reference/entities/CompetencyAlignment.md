# CompetencyAlignment

Approved typed mapping from academic evidence to one competency version.

Owned by **records**.

## Fields

### id

Stable globally unique CompetencyAlignment identifier.

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

### competency_version_id

Target competency in same institution.

Required. Null is rejected.

References [CompetencyVersion](CompetencyVersion.md). Target competency in same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Approved activity source where applicable.

Required. Nullable.

References [ActivityVersion](ActivityVersion.md). Approved activity source where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Exact assessment item where applicable.

Required. Nullable.

References [ItemVersion](ItemVersion.md). Exact assessment item where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_criterion_id

Exact criterion where applicable.

Required. Nullable.

References [RubricCriterion](RubricCriterion.md). Exact criterion where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_item_id

Approved grade line where applicable.

Required. Nullable.

References [GradeItem](GradeItem.md). Approved grade line where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_kind

Which authoritative evidence type can map.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "activity",
    "item",
    "rubric",
    "grade",
    "recognition",
    "observed"
  ]
}
```

### relation

Semantic alignment type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "demonstrates",
    "supports",
    "prerequisite"
  ]
}
```

### conversion

Explicit code conversion when applicable.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "source_code": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
      },
      "level_code": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
      }
    },
    "required": [
      "source_code",
      "level_code"
    ],
    "additionalProperties": false
  },
  "maxItems": 64,
  "minItems": 0
}
```

### source_family

Independence family used during evidence aggregation.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### active_from

Inclusive approved alignment validity start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### active_to

Exclusive end, null for ongoing.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Exactly one applicable source reference when kind requires it.
- Labeling an activity alone never grants mastery.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| competency_version_id, source_kind, active_from | Find eligible mappings for exact skill and source. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
