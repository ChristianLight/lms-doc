# ParticipationIntervention

Purpose-limited instructor support action or follow-up with exact learner scope.

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

Teaching workspace scope.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Learner subject.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment belongs to offering and teacher current authority.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### recorded_by

Accountable support actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### kind

Support action class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "reminder",
    "support_request",
    "meeting_request",
    "review_referral"
  ]
}
```

### basis_codes

Safe coded basis such as required work overdue or unavailable result.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
  },
  "maxItems": 12,
  "minItems": 1
}
```

### restricted_note_ref

Access-controlled note resource reference.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### follow_up_at

Optional assigned follow-up.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Support lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "completed",
    "cancelled"
  ],
  "default": "open"
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

### recorded_at

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- No grade, enrollment, deadline or completion is altered by a support record.
- Sensitive notes follow separate capability and retention policy.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, enrollment_id, state, follow_up_at | Scoped instructor intervention queue. |

## Retention

Retain through documented support window and any active hold. Remove unnecessary notes after close.
