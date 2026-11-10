# LearningRecordDelivery

Outbox receipt for an immutable learning statement sent to an approved record store.

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

### institution_id

Institution owning these data and their access policy.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### profile_id

Approved xAPI or cmi5 output profile.

Required. Null is rejected.

References [ExchangeProfile](ExchangeProfile.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### statement_id

Stable xAPI statement ID allocated once.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_event_id

Immutable source evidence event ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### destination_key

Approved learning record store route key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### payload_digest

Digest of canonical outbound statement bytes.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### attempt_count

Number of delivery attempts.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100
}
```

### next_attempt_at

Next permitted retry time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### delivered_at

Verified remote acceptance time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "sending",
    "delivered",
    "rejected",
    "dead_letter"
  ]
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
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

## Integrity

- Replays must use the same statement ID and content digest.
- LRS delivery never substitutes for native grade or completion authority.

## Unique keys

- `id`
- `institution_id, destination_key, statement_id`
- `institution_id, destination_key, source_event_id, profile_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| state, next_attempt_at | Lease ready statement delivery and enforce bounded retries. |

## Retention

Retain delivery digest and outcomes by audit policy. Purge sensitive statement bytes separately after destination and privacy checks.
