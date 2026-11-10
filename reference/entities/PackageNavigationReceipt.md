# PackageNavigationReceipt

Immutable result of one edition-specific navigation request.

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

Sequencing instance.

Required. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### from_occurrence_id

Current activity at input, when applicable.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_occurrence_id

Validated target for choice or jump when present.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_occurrence_id

New leaf selected by edition sequencing engine.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### request_key

Scoped idempotency identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### request_kind

Edition navigation request token.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### request_source

Which authenticated command source initiated navigation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "host_ui",
    "sco",
    "system"
  ]
}
```

### prior_sequence_revision

State revision compared before process execution.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### delivery_attempt_id

Attempt selected by successful delivery.

Optional. Null is rejected.

References [PackageActivityAttempt](PackageActivityAttempt.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### transition_trace

Bounded ordered normative process trace with protected values excluded.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "process_id": {
        "type": "string",
        "minLength": 1,
        "maxLength": 32
      },
      "outcome": {
        "type": "string",
        "minLength": 1,
        "maxLength": 64
      },
      "occurrence_id": {
        "type": "string",
        "format": "uuid"
      }
    },
    "required": [
      "process_id",
      "outcome"
    ],
    "additionalProperties": false
  },
  "maxItems": 256,
  "minItems": 0,
  "uniqueItems": false
}
```

### result

Authoritative outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "deliver",
    "no_delivery",
    "suspend",
    "end",
    "rejected"
  ]
}
```

### reason_code

Edition result or rejected prerequisite reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

### sequence_revision

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

- Each successful request serializes against authoritative sequencing revision.
- Replay never starts a duplicate activity attempt.

## Unique keys

- `id`
- `registration_id, request_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| registration_id, sequence_revision | Replay deterministic navigation and inspect selection order. |

## Retention

Retain with package progression evidence.
