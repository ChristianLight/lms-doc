# SyncChange

One staged reconciliation decision for an exact provider record and canonical local identity.

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

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### sync_run_id

Run owning this proposed effect.

Required. Null is rejected.

References [SyncRun](SyncRun.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### local_id

Current local record, if mapped.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_type

Provider model type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### external_id

Stable provider identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### input_digest

Digest of normalized mapped input.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### decision

Proposed connector outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "noop",
    "upsert",
    "explicit_remove",
    "absence_review",
    "conflict",
    "invalid"
  ]
}
```

### protected_diff_ref

Reviewed restricted diff evidence.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### applied_version

Committed local record revision, if applied.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "applied",
    "skipped",
    "review"
  ]
}
```

## Integrity

- Same external key with changed digest during one snapshot is a conflict, not last-write-wins.
- Explicit removal uses the canonical domain's transition, including access revocation and retention.

## Unique keys

- `id`
- `institution_id, sync_run_id, external_type, external_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, sync_run_id, state, decision | Enumerate conflict and removal review queue |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | applied | ApplySyncPage | Authority and resource version validated Execute canonical domain command and record evidence. |
| staged | skipped | ApplySyncPage | Dry run, identical value or policy blocks this change Record reason without domain mutation. |
| staged | review | ApplySyncPage | Conflict or absence-derived removal requires approval Keep source digest and current local version. |
| review | applied | ApproveSyncRun | Reviewer approves this exact digest and local version still matches Apply the authorized effect. |
