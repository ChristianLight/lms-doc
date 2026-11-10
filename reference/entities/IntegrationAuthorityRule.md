# IntegrationAuthorityRule

Pinned field authority and permitted direction for one connector model attribute.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### connection_id

Connector installation.

Required. Null is rejected.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### connection_version

Exact configuration version owning this immutable rule.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### resource_type

Mapped connector model.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### field_key

Allowlisted field or action name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### authority

Source of truth for this field. Review queues conflicts.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "local",
    "provider",
    "review"
  ]
}
```

### direction

Permitted transport direction.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "inbound",
    "outbound",
    "both"
  ]
}
```

### allow_clear

Whether an explicit authorized clear is accepted for this field.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

## Integrity

- Undefined fields are denied by default. Incoming null and absent keys are different.
- Official grade release remains local. A provider result can supply evidence through a declared adapter only.

## Unique keys

- `id`
- `institution_id, connection_id, connection_version, resource_type, field_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, connection_id, connection_version, resource_type | Resolve policy for incoming field diffs |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
