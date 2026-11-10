# JobLease

A fenced claim by one worker over one platform job.

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

### job_id

Claimed logical job.

Required. Null is rejected.

References [PlatformJob](PlatformJob.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### worker_principal_id

Authorized service worker.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### fence

Monotonic per-job claim generation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### lease_started_at

Server database time when the job was claimed.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### lease_until

Exclusive expiry. Default start plus 120 seconds.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### last_heartbeat_at

Most recent valid renewal time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "completed",
    "expired",
    "revoked"
  ]
}
```

## Integrity

- Only current worker with matching fence may heartbeat or write job outcome.
- Heartbeat changes lease deadline within configured ceiling but cannot resurrect an expired lease.

## Unique keys

- `id`
- `institution_id, job_id, fence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| state, lease_until | Reap expired worker claims |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | completed | CompletePlatformJob | Current unexpired fence Commit outcome and close lease. |
| active | completed | FailPlatformJob | Current unexpired fence Commit failure classification and close lease. |
| active | expired | ReapExpiredJobLease | Database time reached expiry Fence stale worker before applying retry policy. |
| active | revoked | CancelPlatformJob | Authorized cancellation and effect has not committed Invalidate future completion for this claim. |
