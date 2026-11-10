# GroupMembership

Effective-dated learner membership in an offering group.

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

Learner participation.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment must belong to the same offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learning_group_id

Owning group.

Required. Null is rejected.

References [LearningGroup](LearningGroup.md). Must resolve to an authorized LearningGroup in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
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

### source

Membership route.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "manual",
    "self",
    "invitation",
    "cohort",
    "roster",
    "rule",
    "transfer"
  ]
}
```

### assigned_by

Actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- No overlapping pair intervals.
- Section restriction must hold throughout active membership.

## Unique keys

- `id`
- `enrollment_id, learning_group_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| learning_group_id, effective_from, effective_to | Scoped active group roster. |
| enrollment_id, effective_to | Effective group gates and schedule overrides. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
