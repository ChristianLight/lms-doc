# NotificationDelivery

A retryable channel-specific delivery record for one committed purpose.

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

### person_id

Recipient of the logical message.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### connection_id

External delivery connector, if any.

Optional. Nullable.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_event_id

Causative authoritative event identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### purpose

Allowlisted purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### channel

Delivery channel.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "in_app",
    "email",
    "sms",
    "collaboration"
  ]
}
```

### template_key

Versioned localized message template family.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### template_version

Exact approved wording version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### locale

Resolved message language.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
}
```

### delivery_key

Per-recipient, channel, purpose and source deduplication key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### provider_message_id

Provider-issued opaque acknowledgement.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### next_delivery_at

Earliest eligible delivery time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### last_error_code

Safe delivery failure class.

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
    "planned",
    "sending",
    "sent",
    "suppressed",
    "bounced",
    "uncertain",
    "failed"
  ]
}
```

## Integrity

- External payload contains minimal generic notice and authenticated resource link, no official grades or sensitive learner information.
- Provider failure never reverses a committed academic change. Recheck current audience and contact before send.

## Unique keys

- `id`
- `institution_id, delivery_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, next_delivery_at | Find eligible notification deliveries |
| institution_id, person_id, created_at | Review recipient's notification history |

## Retention

Retain redacted completion and effect identifiers for 90 days by default. Retain pending jobs until terminal. A hold supersedes disposal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| planned | sending | ClaimPlatformJob | Purpose, audience, contact and preference are current Reserve provider effect identity. |
| planned | suppressed | RecordNotificationOutcome | Access, preference or policy prohibits delivery Record reason without sending. |
| sending | sent | RecordNotificationOutcome | Provider or local channel durably acknowledges Store reference without message contents. |
| sending | bounced | RecordNotificationOutcome | Authenticated provider bounce associated with this delivery Suppress failing contact until reverified. |
| sending | uncertain | RecordNotificationOutcome | Delivery acknowledgement lost and provider cannot yet reconcile Block blind send retry. |
| sending | failed | RecordNotificationOutcome | Permanent error or budget exhausted Display failure to authorized operators. |
| uncertain | sent | RecordNotificationOutcome | Provider lookup confirms delivery Complete the same logical effect. |
| uncertain | sending | RetryPlatformJob | Provider proves absence or accepts same deduplication key Retry the same logical delivery. |
