# CourseFollow

Learner preference for course discovery or notifications independent of enrollment.

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

### person_id

Preference owner.

Required. Null is rejected.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_id

Visible followed catalog identity.

Required. Null is rejected.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### active

Whether discovery notifications are enabled.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### revision

Optimistic preference token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### updated_at

Server preference time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Follow never grants learner or roster access.

## Unique keys

- `id`
- `person_id, course_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, active, updated_at | Personal followed-course list. |

## Retention

Retain active preference and minimal opted-out history through the notification suppression window.
