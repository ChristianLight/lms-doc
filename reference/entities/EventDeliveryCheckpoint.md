# EventDeliveryCheckpoint

Progress of an ordered subscriber stream whose offsets are transport-local.

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

### consumer_key

Registered consumer.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### stream_key

Provider or application partition identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### last_committed_offset

Opaque transport cursor observed after durably applied effects.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### last_event_id

Most recent committed event when checkpoint is from the local outbox.

Optional. Nullable.

References [OutboxEvent](OutboxEvent.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### checkpoint_at

Server instant at which the cursor became durable.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Advance by transport order and apply or recognize corresponding receipt first. Sparse events use the explicitly subscribed sequence.
- A consumer reset requires reviewed replay plan and cannot erase deduplication state.

## Unique keys

- `id`
- `institution_id, consumer_key, stream_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, consumer_key, checkpoint_at | Find stale consumers and safe stream retention floor |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
