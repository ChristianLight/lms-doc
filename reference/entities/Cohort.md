# Cohort

Institutional grouping reused across offerings.

Owned by **participation**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_unit_id

Delegated owner.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Normalized cohort code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Cohort title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### state

Membership lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "closed"
  ],
  "default": "active"
}
```

### revision

Compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

## Integrity

- No direct learning authority without explicit roster grant.

## Unique keys

- `id`
- `institution_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, state | Delegated cohort list. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
