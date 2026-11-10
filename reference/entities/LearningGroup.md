# LearningGroup

Offering-local team, audience or collaboration group.

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

### section_id

Optional restricting section.

Optional. Nullable.

References [Section](Section.md). Section must belong to offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Normalized group code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### purpose

Group behavior classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "team",
    "discussion",
    "instruction",
    "collaboration"
  ]
}
```

### membership_mode

Admission mode.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "manual",
    "self_join",
    "rule"
  ],
  "default": "manual"
}
```

### capacity

Optional lower cap.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000000
}
```

### state

Membership availability.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "closed"
  ],
  "default": "active"
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

- Section-limited members must be in the effective section.

## Unique keys

- `id`
- `offering_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, section_id, state | Scoped group listing. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
