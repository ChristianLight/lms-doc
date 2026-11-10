# MeetingOccurrence

Materialized scheduled meeting with stable recurrence identity.

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

### meeting_series_id

Series owner.

Required. Null is rejected.

References [MeetingSeries](MeetingSeries.md). Must resolve to an authorized MeetingSeries in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Scoped calendar read and filtering.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### recurrence_id

Stable original civil recurrence identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 48
}
```

### starts_at

Canonical scheduled instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### ends_at

Canonical end instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### check_in_open_at

Inclusive check-in start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### check_in_close_at

Exclusive learner check-in end.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### roster_frozen_at

Attendance roster snapshot anchor.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Occurrence state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "scheduled",
    "open",
    "closed",
    "cancelled"
  ],
  "default": "scheduled"
}
```

### revision

Calendar and check-in mutation revision.

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

- End is after start.
- Completed meeting and attendance remain auditable on cancellation.

## Unique keys

- `id`
- `meeting_series_id, recurrence_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, starts_at | Authorized course calendar. |
| state, starts_at | Attendance scheduler. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
