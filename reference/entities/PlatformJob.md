# PlatformJob

Durable operation with classification, a per-job lease and a stable logical effect identity.

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

### job_kind

Declared processing family and permitted worker profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "exam_marking",
    "release_dispatch",
    "asset_scan",
    "privacy_disposition",
    "sync",
    "notification",
    "bulk_report",
    "regrade",
    "course_import",
    "recovery_verification"
  ]
}
```

### effect_key

Canonical logical deduplication key for this kind and scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### target_type

Canonical target kind.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### target_id

Canonical target UUID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expected_target_version

Resource version to revalidate before effect.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### payload_ref

Protected schema-validated job parameters.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requested_by_id

Initiating Principal, when human or on behalf of a human.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### authority_mode

User rights rechecked for delegated work. Durable system work uses an explicitly registered policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "user_delegated",
    "durable_system"
  ]
}
```

### priority

Within-family priority, larger first.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100,
  "default": 50
}
```

### available_at

Earliest next claim instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### attempt_count

Number of leases started. Begins at zero.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 16
}
```

### max_attempts

Maximum automatically retriable attempts for this job.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 16,
  "default": 6
}
```

### active_fence

Current lease fence. Absent outside running state.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### checkpoint_ref

Last durable progress boundary.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### last_error_code

Normalized outcome category without content.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "running",
    "retry_wait",
    "succeeded",
    "blocked",
    "dead",
    "canceled"
  ]
}
```

## Integrity

- Each claim uses a monotonically increasing fence. Compare current fence before changing outcomes.
- Leases are coordination only. Remote effect keys, local version checks and effect records provide correctness.

## Unique keys

- `id`
- `institution_id, job_kind, effect_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_kind, state, available_at, priority, created_at | Claim work by authorized worker pool |
| institution_id, target_type, target_id, state | Detect active work and prevent inappropriate revocation bypass |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| queued | running | ClaimPlatformJob | Target is current and pool has capacity Allocate next fence and active lease. |
| retry_wait | running | ClaimPlatformJob | Backoff elapsed and attempt budget remains Allocate next fence. |
| running | succeeded | CompletePlatformJob | Effect or safe no-op committed under current fence Save terminal outcome and clear lease. |
| running | retry_wait | FailPlatformJob | Transient error and repeat is safe under same effect key Schedule bounded backoff and clear lease. |
| running | blocked | FailPlatformJob | Authorization changed or external outcome is uncertain Require scoped reconciliation or approval. |
| running | dead | FailPlatformJob | Permanent invalid work or retry budget exhausted Persist failure for operator review. |
| running | retry_wait | ReapExpiredJobLease | Lease expired and task is repeat-safe Invalidate old fence before making job claimable. |
| running | blocked | ReapExpiredJobLease | Lease expired and external effect is uncertain Require reconciliation before retry. |
| blocked | queued | RetryPlatformJob | Scope verified and retry justified Retain effect key and prior lease evidence. |
| dead | queued | RetryPlatformJob | Authorized explicit repair and updated version prove safe execution Record operator decision and preserve prior attempts. |
| queued | canceled | CancelPlatformJob | Authorized owner confirms cancellation Prevent future effects. |
| running | canceled | CancelPlatformJob | Current operation supports cancellation before effect commitment Advance fence and suppress stale workers. |
| retry_wait | canceled | CancelPlatformJob | Authorized owner confirms cancellation Prevent future effects. |
