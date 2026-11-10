# OutboxEvent

Immutable event committed atomically with an authoritative domain change.

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

### aggregate_type

Stable domain aggregate type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### aggregate_id

Owner aggregate UUID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### aggregate_version

Version of aggregate after the change.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### ordinal

Zero-based stable order for events emitted by one version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 65535
}
```

### event_name

Registered event contract name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### schema_version

Registered payload schema version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### occurred_at

UTC commit-side occurrence time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### correlation_id

Originating workflow identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### causation_id

Event or command ID that caused this event.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### payload_ref

Canonical allowlisted payload or protected record pointer.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- An outbox event is insert-only and never gains new effects through replay.
- Only selected declared payload fields cross subsystem boundaries. Do not send PII or learner responses in generic messages.

## Unique keys

- `id`
- `institution_id, aggregate_type, aggregate_id, aggregate_version, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, aggregate_type, aggregate_id, aggregate_version, ordinal | Read aggregate ordering stream |

## Retention

Default 30 days after every required consumer checkpoint. Never discard unhandled retained events.
