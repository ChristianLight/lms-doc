# CreditUnitSchemeVersion

Published credit precision and normalization scheme.

Owned by **records**.

## Fields

### id

Stable globally unique CreditUnitSchemeVersion identifier.

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

### scheme_key

Stable unit scheme family.

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

Credit unit system name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 120
}
```

### unit_code

Exact institutional credit unit.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### precision_places

Maximum allowed fractional credit precision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 6,
  "default": 2
}
```

### base_multiplier

Exact published scale conversion to institutional base unit.

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

### state

Version lifecycle.

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

- Never infer conversion from a percentage or title.
- Published multiplier positive and immutable.

## Unique keys

- `id`
- `institution_id, scheme_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, scheme_key | Resolve approved credit normalization. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishCreditScheme | Authorized unit and exact conversion validated Freeze credit conversion contract. |
