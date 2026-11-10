# VariantProfileVersion

Pinned constrained parameter generation and expected value derivation.

Owned by **assessment**.

## Fields

### id

Stable globally unique VariantProfileVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution that owns the generator profile.

Required. Null is rejected.

References [Institution](Institution.md). Institution that owns the generator profile.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### profile_key

Stable profile key within institution.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### revision

Profile revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### generator_key

Registered bounded generator capability.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### parameters

Typed ordered parameter declarations and constraints.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "kind": {
        "type": "string",
        "enum": [
          "number",
          "rational",
          "text",
          "identifier",
          "boolean",
          "structured"
        ]
      },
      "value": {
        "type": "string",
        "minLength": 1,
        "maxLength": 16000
      }
    },
    "required": [
      "name",
      "kind",
      "value"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 128
}
```

### iteration_limit

Maximum sampled candidates before resolution fails.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### digest

Protected generator and schema digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### approved_at

Generation approval time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Default limit 64.
- No unregistered executable generator.
- Constraint and parameter dependencies are acyclic.

## Unique keys

- `id`
- `institution_id, profile_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, profile_key | Find approved generator series. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
