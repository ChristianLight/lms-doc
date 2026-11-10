# EnrollmentRelease

Effective exact curriculum assignment for one enrollment.

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

### enrollment_id

Stable participation.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Must resolve to an authorized Enrollment in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_version_id

Exact immutable course version.

Required. Null is rejected.

References [CourseVersion](CourseVersion.md). Must belong to this enrollment offering course.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### predecessor_id

Previous assignment in same enrollment.

Optional. Nullable.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rollout_id

Approved rollout where applicable.

Optional. Nullable.

References [ReleaseRollout](ReleaseRollout.md). Must resolve to an authorized ReleaseRollout in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Assignment reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "initial",
    "rollout",
    "rollback",
    "reactivation"
  ]
}
```

### effective_from

Inclusive start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Intervals cannot overlap.
- At most one current assignment.
- Historical academic records retain exact release ID.

## Unique keys

- `id`
- `enrollment_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, effective_from, effective_to | Resolve exact release at action instant. |
| course_version_id | Impact and historical query. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
