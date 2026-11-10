# LibraryEntry

Stable library item for a shared resource, activity or template.

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

### library_id

Owning library.

Required. Null is rejected.

References [Library](Library.md). Must resolve to an authorized Library in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_key

Normalized stable entry key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### entry_kind

Payload family.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "resource",
    "activity",
    "template"
  ]
}
```

### title

Discovery title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### tags

Approved search keywords.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
  },
  "maxItems": 40,
  "minItems": 0
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

- Archive does not remove authorized historic pinned versions.

## Unique keys

- `id`
- `library_id, item_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| library_id, entry_kind, archived, title | Filtered authorized library results. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
