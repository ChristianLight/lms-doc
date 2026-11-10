# SyncRun

A resumable dry run, incremental feed, or full reconciliation against a configured connector.

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

Exact connector configuration pinned at start.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### mode

Run semantics and removal eligibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "dry_run",
    "incremental",
    "complete_snapshot"
  ]
}
```

### direction

Planned transfer direction.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "inbound",
    "outbound"
  ]
}
```

### initial_cursor

Provider cursor at start, treated as opaque.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### committed_cursor

Last completely applied checkpoint.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### pages_applied

Number of committed pages. Starts at zero.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647
}
```

### records_seen

Number of validated unique records observed. Starts at zero.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647
}
```

### conflicts

Number of records requiring review. Starts at zero.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647
}
```

### snapshot_marker

Provider proof of a complete consistent snapshot, required for absence review.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pending",
    "running",
    "review",
    "succeeded",
    "failed",
    "canceled"
  ]
}
```

## Integrity

- Dry run never changes local domain records, persisted connector cursor, or provider.
- No absence-based removals from partial data. Complete snapshots stage diffs and require explicit approval before applying removals.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, connection_id, state, created_at | Enforce one applying run per connection and direction |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | running | ClaimPlatformJob | Authorized worker and pinned connector version current Start guarded provider work. |
| running | review | FinishSyncRun | Conflict exists or complete snapshot proposes removals Persist candidate diffs and wait for reviewer. |
| running | succeeded | FinishSyncRun | All pages committed and required provider completion proof present Advance connection cursor for non-dry run. |
| running | failed | FinishSyncRun | Unrecoverable provider error or configuration version changed Keep last safe checkpoint without inferring omissions. |
| review | succeeded | ApproveSyncRun | Independent reviewer accepts specific removals or conflicts are resolved Apply current approved effects and advance cursor. |
| pending | canceled | CancelSyncRun | Authorized operator cancels before application Retain run evidence. |
| running | canceled | CancelSyncRun | Fence advances and an active worker cannot continue Keep committed effects and checkpoint. |
