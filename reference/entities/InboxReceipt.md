# InboxReceipt

Durable deduplication and result state for a consumer and one message.

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

Registered local consumer or external receiver key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### connection_id

External source connection or null for internal messages.

Optional. Nullable.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### message_id

Stable sender message ID, scoped to consumer and configured source.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### source_key

Non-null registered source partition distinguishing local and external origins.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### payload_digest

SHA-256 of verified canonical payload or signed byte representation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### received_at

First successful verification time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### handled_at

Time the authoritative outcome became durable.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### result_code

Safe classified handling result.

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
    "received",
    "processing",
    "applied",
    "rejected",
    "uncertain"
  ]
}
```

## Integrity

- Same key and same digest replays the stored result. Different digest rejects and signals a security incident.
- Commit application and applied receipt in the same write boundary where local. Remote effects require verified reconciliation.

## Unique keys

- `id`
- `institution_id, consumer_key, source_key, message_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, consumer_key, state, received_at | Find recoverable verified receipts |

## Retention

At least the replay and retention horizon of the source. Default 30 days for valid handled inputs.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| received | processing | ClaimPlatformJob | Current consumer worker fence and schema recognized Reserve this logical processing attempt. |
| processing | applied | RecordInboundOutcome | Effect committed or reconciled successfully Persist result and handled_at. |
| processing | rejected | RecordInboundOutcome | Payload permanently invalid or source not authorized for action Persist rejection and handled_at. |
| processing | uncertain | RecordInboundOutcome | Provider acknowledgement cannot be established Block automatic effect replay. |
| uncertain | processing | RetryPlatformJob | Operator verified safe retry or current provider supports deduplication Resume with same message identity. |
