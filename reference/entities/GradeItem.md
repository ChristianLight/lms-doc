# GradeItem

Stable offering-scoped gradebook line across policy revisions.

Owned by **records**.

## Fields

### id

Stable globally unique GradeItem identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_code

Stable unique offering-local code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### placement_key

Stable curriculum placement when linked.

Required. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### title

Default staff and learner label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### archived

Exclude from new policy assignment when true.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- One stable line does not change meaning across incompatible score or identity bindings.
- Archive never deletes used policy versions.

## Unique keys

- `id`
- `offering_id, item_code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, archived, item_code | List live gradebook lines. |
| offering_id, placement_key | Find lines tied to a placement. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
