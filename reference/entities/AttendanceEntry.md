# AttendanceEntry

One attendance subject in one occurrence and current published pointer.

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

### meeting_occurrence_id

Occurrence owner.

Required. Null is rejected.

References [MeetingOccurrence](MeetingOccurrence.md). Must resolve to an authorized MeetingOccurrence in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Learner in frozen audience or approved exception.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment must belong to the same offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### current_revision_id

Effective published decision.

Optional. Nullable.

References [AttendanceRevision](AttendanceRevision.md). Must resolve to an authorized AttendanceRevision in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Compare-and-swap token.

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

- Proposals never replace published pointer.

## Unique keys

- `id`
- `meeting_occurrence_id, enrollment_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| meeting_occurrence_id, current_revision_id | Scoped roster and unresolved decisions. |
| enrollment_id, meeting_occurrence_id | Learner attendance history. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
