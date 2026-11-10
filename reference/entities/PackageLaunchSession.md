# PackageLaunchSession

Scoped learner launch lease for a single package activity occurrence.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### registration_id

Owning attempt.

Required. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### occurrence_id

Launchable occurrence in the registered organization.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### epoch

Fencing epoch pinned to registration writer lease.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### origin

Approved content origin with no application cookie scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### bootstrap_digest

Hash of short-lived bootstrap nonce, never raw token.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### lease_expires_at

Server deadline for writing under this epoch.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### activated_at

One-time bootstrap exchange time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### closed_at

Authoritative close or lease expiry time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### credited_time_ms

Exact fixed-unit millisecond projection only when duration has no unresolved calendar components.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### accepted_through_sequence

Contiguous confirmed client mutation sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "bootstrap",
    "active",
    "finished",
    "interrupted",
    "revoked"
  ]
}
```

### activity_attempt_id

Exact occurrence attempt, including distinct browse and review working states.

Required. Null is rejected.

References [PackageActivityAttempt](PackageActivityAttempt.md). Matches this registration and occurrence.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sco_state_id

Authoritative RTE state owned by this exact occurrence attempt.

Required. Null is rejected.

References [PackageScoState](PackageScoState.md). State belongs to the exact selected activity attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pending_navigation_request

Last valid 2004 session-scoped navigation request. Consumed only when its successful terminal transition permits it.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4096
}
```

### credited_duration

Lossless duration sum. Preserve calendar components separately from fixed elapsed units.

Optional. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "years": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "months": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "fixed_milliseconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    }
  },
  "required": [
    "years",
    "months",
    "fixed_milliseconds"
  ],
  "additionalProperties": false
}
```

### reported_duration_lexeme

Last valid edition-formatted duration, preserved exactly for traceability.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

## Integrity

- The grant is limited to one occurrence, learner attempt and epoch.
- Time is credited at most once per closed session.
- Only hashed bootstrap provenance is stored.
- SCO-written adl.nav.request never becomes a cross-launch CMI element. A new launch starts with the edition default request and cannot replay an old suspended or consumed request.

## Unique keys

- `id`
- `registration_id, epoch`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| state, lease_expires_at | Expire abandoned runtime leases. |

## Retention

Retain lifecycle evidence with registration. Purge transient secrets after redemption or expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| bootstrap | active | RedeemPackageLaunch | Bootstrap digest, actor, origin, audience and epoch match. Consume one-time credential and provide server snapshot. |
| active | finished | CommitPackageRuntime | Finalization and all validated writes are durably accepted. Credit time once and close runtime lease. |
| active | revoked | TakeOverPackageLaunch | Authorized learner approves takeover of current writer. Fence prior epoch. |
| active | interrupted | ExpirePackageLaunch | Lease expired without confirmed termination. Retain accepted prefix and mark interrupted. |
| bootstrap | revoked | TakeOverPackageLaunch | Owning learner verifies lost or unusable bootstrap at the exact current writer epoch. Fence the unavailable writer and issue a fresh launch for the same activity attempt. |
