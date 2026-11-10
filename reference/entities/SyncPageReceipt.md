# SyncPageReceipt

Commit proof for an exact cursor and page in one reconciliation run.

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

### sync_run_id

Owning run.

Required. Null is rejected.

References [SyncRun](SyncRun.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### cursor_key

Hash of connection-bound opaque current cursor or designated first-page sentinel.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### page_digest

Hash of validated normalized provider page.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### next_cursor

Provider next cursor as delivered, if any.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### record_count

Bounded validated record count.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 500
}
```

### committed_at

UTC time page outcomes and checkpoint committed.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Same run and cursor with a different page digest triggers review. Do not advance the checkpoint after a partial local page mutation.

## Unique keys

- `id`
- `institution_id, sync_run_id, cursor_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, sync_run_id, committed_at | Enumerate durable run pages and identify incomplete checkpoints |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.
