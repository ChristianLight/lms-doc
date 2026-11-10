# Activity

Stable reusable interaction definition.

Owned by **curriculum**.

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

### institution_id

Owning institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_unit_id

Owning curriculum unit.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_kind

Registered interaction.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "acknowledgment",
    "self_check",
    "quiz",
    "exam",
    "assignment",
    "survey",
    "live_session",
    "collaboration",
    "package",
    "external_tool"
  ]
}
```

### created_by

Creator.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Grade evidence and learner state are excluded.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, activity_kind | Browse authorized activities. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
