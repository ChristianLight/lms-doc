# StorageScanResult

Immutable evidence of a particular scanner decision on exact content.

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

### storage_object_id

Object evaluated.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_sha256

Digest of inspected bytes.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### engine_version

Scanner engine and ruleset identification.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### policy_version

Pinned file handling policy version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### verdict

Normalized evidence result.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "clean",
    "unsupported",
    "infected",
    "corrupt",
    "unsafe",
    "timeout"
  ]
}
```

### checked_at

Inspection time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### safe_reason_code

Safe failure detail code.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

## Integrity

- Verdict timeout is inconclusive and cannot enable serving.
- A changed digest requires a different object version or a rescan under matching provenance.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, storage_object_id, checked_at | Trace trust decisions and compare later scans |

## Retention

Default 365 days for ordinary operational records. Follow approved audit schedule and active holds. Academic version history has its own retention.
