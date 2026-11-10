# Asset

Durable resource and rights scope independent of storage bytes.

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

Responsible owner.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_unit_id

Scope for editing.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### title

Logical asset title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### kind

Asset class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "image",
    "document",
    "video",
    "audio",
    "caption",
    "transcript",
    "archive"
  ]
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

- Asset can own many exact versions.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, kind, title | Scoped asset catalog. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
