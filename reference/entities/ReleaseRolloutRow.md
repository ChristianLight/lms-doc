# ReleaseRolloutRow

Idempotent rollout work and exact per-enrollment result.

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

### rollout_id

Frozen rollout plan.

Required. Null is rejected.

References [ReleaseRollout](ReleaseRollout.md). Must resolve to an authorized ReleaseRollout in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Frozen audience learner.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment must belong to the same offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_release_id

Compare-and-swap source release.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_release_id

Committed target release.

Optional. Nullable.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Per-participant outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pending",
    "deferred",
    "applied",
    "superseded",
    "failed"
  ],
  "default": "pending"
}
```

### reason_code

Optional status reason.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

## Integrity

- Retry can create only one target assignment.
- Superseded is terminal unless an independent rollout is approved.

## Unique keys

- `id`
- `rollout_id, enrollment_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| rollout_id, state | Retry work and aggregate plan progress. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
