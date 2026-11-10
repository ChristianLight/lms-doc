# NotificationPreference

An allowed optional channel selection for a person and purpose.

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

Person choosing delivery preference.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### purpose

Notification purpose class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "learning_reminder",
    "announcement",
    "progress_summary",
    "security",
    "privacy_case",
    "exam_receipt"
  ]
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

### enabled

Whether optional delivery is permitted.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### quiet_start_minute

Local quiet hours start minute since midnight.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1439,
  "default": 1260
}
```

### quiet_end_minute

Local quiet hours end minute since midnight.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1439,
  "default": 420
}
```

### timezone

Pinned presentation timezone used for quiet hours.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^(UTC|[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+)+)$"
}
```

## Integrity

- User preference cannot suppress required in-app receipts or authorized security notices. Optional external channels are off absent preference.
- Quiet hours use the recipient zone. If endpoints equal, no quiet window.

## Unique keys

- `id`
- `institution_id, person_id, purpose, channel`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, person_id, purpose | Resolve user-level channel preference |

## Retention

Retain live and historic references while required by enrollment or records. Apply identity_contact policy to separately protected contact data.
