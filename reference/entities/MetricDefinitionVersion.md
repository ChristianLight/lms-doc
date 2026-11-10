# MetricDefinitionVersion

Published report metric population, grouping, algorithm and suppression.

Owned by **records**.

## Fields

### id

Stable globally unique MetricDefinitionVersion identifier.

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

### metric_key

Stable reporting metric code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
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

### title

Approved report display label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### aggregation

Exact aggregate function.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "ratio",
    "sum",
    "median",
    "count"
  ]
}
```

### source_profile

Versioned canonical source and eligible population rules.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### group_dimensions

Approved grouping dimensions.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "offering",
      "section",
      "academic_period",
      "organization_unit",
      "program"
    ]
  },
  "maxItems": 5,
  "minItems": 0,
  "uniqueItems": true
}
```

### minimum_group_size

Primary privacy suppression population threshold.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000,
  "default": 10
}
```

### complementary_suppression

Prevent reconstruction from totals and related cells.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### state

Published metric lifecycle.

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

- Denominator and source coverage required for ratios.
- Metric version never changes released academic records.

## Unique keys

- `id`
- `institution_id, metric_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, metric_key | Select authorized report definition. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishMetricDefinition | Population, privacy and grouping validated Freeze metric definition. |
