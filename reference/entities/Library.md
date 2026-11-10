# Library

Scoped content and template collection.

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

Owner institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_unit_id

Owner unit.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Normalized library business code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Library display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### sharing_mode

Discovery scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "public",
    "institution",
    "restricted"
  ],
  "default": "restricted"
}
```

### license_key

Registered permitted use policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### revision

Metadata revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### archived

Retired from new use.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

## Integrity

- Discovery and reuse authorization are independent.

## Unique keys

- `id`
- `institution_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, archived, title | Library selection. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
