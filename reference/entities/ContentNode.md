# ContentNode

Stable independently editable learning resource identity.

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

Responsible institution.

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

### type_key

Registered stable content type.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### created_by

Author or migration principal.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
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

- A detached copy creates a new identity.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, type_key | Author resource picker. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
