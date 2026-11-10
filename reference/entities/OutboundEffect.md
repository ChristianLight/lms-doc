# OutboundEffect

Durable and reconcilable intent for one remote side effect.

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

Remote connector installation.

Required. Null is rejected.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### connection_version

Configuration pinned when intent was prepared.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### job_id

Logical job responsible for initiating or reconciling this effect.

Required. Null is rejected.

References [PlatformJob](PlatformJob.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### action_key

Approved provider action.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### resource_scope_id

Canonical authorized target.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effect_key

Stable provider deduplication identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### request_digest

Hash of the authorized normalized payload and recipient.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### provider_receipt_ref

Verified remote outcome evidence under custody.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### dispatched_at

First guarded send time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### confirmed_at

Verified outcome confirmation time.

Optional. Nullable.

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
    "prepared",
    "dispatched",
    "confirmed",
    "uncertain",
    "suppressed"
  ]
}
```

## Integrity

- Persist prepared intent before any network send. Never change recipient or body under a previously used effect key.
- An effect marked dispatched with no verified result is treated as possibly accepted after worker failure.

## Unique keys

- `id`
- `institution_id, connection_id, effect_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, connection_id, state, created_at | Reconcile dispatched and uncertain effects |

## Retention

Retain evidence through provider replay horizon, default 90 days after terminal status. Keep uncertain effects until reconciled.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| prepared | dispatched | AuthorizeOutboundDispatch | Current fence, authority, connector and exact request digest verified Durably record dispatch intent before allowing network send. |
| prepared | suppressed | RecordOutboundOutcome | Capability revoked or obsolete desired version prevents dispatch Prevent external send and record local reason. |
| dispatched | confirmed | RecordOutboundOutcome | Provider returned or lookup verified exact effect receipt Pin remote evidence and close logical effect. |
| dispatched | uncertain | RecordOutboundOutcome | Request can have reached provider without verified acknowledgement Block duplicate dispatch. |
| uncertain | confirmed | RecordOutboundOutcome | Authorized reconciliation found verified provider outcome Resolve same effect. |
| uncertain | dispatched | AuthorizeOutboundDispatch | Verified absence or provider accepts same idempotency identity Retry only unchanged logical intent. |
