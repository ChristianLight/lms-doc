# Course

Durable course catalog identity and owner scope.

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

Owning unit.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Display catalog code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### normalized_code

Canonical case-folded code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Catalog title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### summary

Plain catalog description.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 6000,
  "default": ""
}
```

### default_locale

Default published locale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
}
```

### visibility

Catalog discoverability.

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

### state

Catalog lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "archived"
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

- Business code normalization is invariant within an institution.
- Archive does not revoke academic evidence.

## Unique keys

- `id`
- `institution_id, normalized_code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, state, title | Scoped catalog lists and search. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | archived | ArchiveCourse | No outstanding authorization blocker. Remove from ordinary catalog and retain versions. |
