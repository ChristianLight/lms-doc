# Announcement

Scoped instructional communication with separate dispatch results.

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

### offering_id

Owning delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### audience

Offering-local scoped recipients.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "kind": {
      "type": "string",
      "enum": [
        "offering",
        "section",
        "learning_group",
        "enrollment"
      ]
    },
    "id": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": [
    "kind",
    "id"
  ],
  "additionalProperties": false
}
```

### author_id

Authorized author.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### title

Notification title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### body

Sanitized visible announcement body.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 12000
}
```

### severity

Display and dispatch class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "information",
    "important",
    "urgent"
  ],
  "default": "information"
}
```

### state

Announcement lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "scheduled",
    "published",
    "withdrawn"
  ],
  "default": "draft"
}
```

### revision

Optimistic token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### publish_at

Scheduled or actual visibility start.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### withdraw_at

Optional exclusive withdrawal time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Notification payload excludes grades and sensitive accommodations.
- Dispatch is unique per recipient, channel and revision.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, publish_at | Scoped learner and staff announcement list. |

## Retention

Retain for the configured operational interval. Purge or de-identify after expiry when no academic reference or hold applies.
