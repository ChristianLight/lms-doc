# LearnerBookmark

Private placement or anchor marker for one person.

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

Bookmark owner.

Required. Null is rejected.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Navigation context.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_key

Stable occurrence key.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### anchor_key

Normalized anchor or empty string.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 160,
  "default": ""
}
```

### label

Optional learner-private name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 240,
  "default": ""
}
```

### created_at

Creation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Unresolved or inaccessible placement never leaks a hidden title.

## Unique keys

- `id`
- `person_id, offering_id, placement_key, anchor_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, offering_id, created_at | Personal bookmark list. |

## Retention

Retain for the configured operational interval. Purge or de-identify after expiry when no academic reference or hold applies.
