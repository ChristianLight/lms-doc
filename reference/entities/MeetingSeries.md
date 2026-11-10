# MeetingSeries

Scoped recurring or single live learning plan.

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

Authorized offering-local participants.

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

### organizer_id

Authorized teacher or organizer.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### title

Learner-visible meeting title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### timezone

Named recurrence zone.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### first_local_datetime

Validated local civil date and time with explicit DST resolution.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### rrule

Approved recurrence subset.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 400
}
```

### duration_minutes

Planned duration.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1440
}
```

### venue_kind

Delivery venue classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "physical",
    "online",
    "hybrid"
  ]
}
```

### alternative_placement_key

Approved alternative participation.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Series state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "active",
    "ended",
    "cancelled"
  ],
  "default": "draft"
}
```

### revision

Calendar mutation token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

## Integrity

- Default horizon is 120 days.
- Occurrence identity survives exception.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state | Calendar materialization and staff views. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
