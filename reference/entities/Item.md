# Item

Stable identity for a reusable prompt and its publication series.

Owned by **assessment**.

## Fields

### id

Stable globally unique Item identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### bank_id

Owning bank, immutable after publication.

Required. Null is rejected.

References [ItemBank](ItemBank.md). Owning bank, immutable after publication.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Bank-local stable lookup key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### created_by

Creator authorized in the bank.

Required. Null is rejected.

References [Principal](Principal.md). Creator authorized in the bank.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Authoritative creation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### published_version_id

Current published version belonging to this item.

Optional. Nullable.

References [ItemVersion](ItemVersion.md). Current published version belonging to this item.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### archived_at

Item retirement time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Published version must refer to this item.
- Retirement prevents new selection without losing pinned history.

## Unique keys

- `id`
- `bank_id, key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| bank_id, archived_at | Active and retired item list. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
