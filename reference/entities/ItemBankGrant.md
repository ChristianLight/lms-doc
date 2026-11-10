# ItemBankGrant

Explicit access operations delegated within one bank.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemBankGrant identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### bank_id

Bank whose authority is delegated.

Required. Null is rejected.

References [ItemBank](ItemBank.md). Bank whose authority is delegated.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### principal_id

Authorized institutional user or service.

Required. Null is rejected.

References [Principal](Principal.md). Authorized institutional user or service.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### operations

Allowed bank operations delegated to the recorded recipient.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "draft",
      "preview",
      "review",
      "publish",
      "reuse",
      "copy",
      "read_keys"
    ]
  },
  "minItems": 1,
  "maxItems": 7
}
```

### granted_by

Manager authorized to delegate all listed operations.

Required. Null is rejected.

References [Principal](Principal.md). Manager authorized to delegate all listed operations.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### granted_at

Authoritative start time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revoked_at

Optional explicit revocation cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Operations cannot widen beyond grantor authority.
- Current principal eligibility required for access.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| bank_id, principal_id, revoked_at | Check current explicit bank access. |

## Retention

Retain while a historical bank action cites grant authority.
