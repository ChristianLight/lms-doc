# SectionMembership

Effective-dated learner assignment to a section.

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

### section_id

Section in enrollment offering.

Required. Null is rejected.

References [Section](Section.md). Must resolve to an authorized Section in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effective_from

Inclusive assignment start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive assignment end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### primary

Primary section for default schedule.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### source

Assignment route.

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

Assignment actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Pair intervals must not overlap.
- At most one primary assignment covers any instant.

## Unique keys

- `id`
- `enrollment_id, section_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| section_id, effective_from, effective_to | Time-specific class roster. |
| enrollment_id, primary, effective_to | Effective primary section. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
