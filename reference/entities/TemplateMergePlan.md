# TemplateMergePlan

Reviewed three-way proposal and exact conflict choices for one destination.

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

### library_adoption_id

Existing managed distribution.

Required. Null is rejected.

References [LibraryAdoption](LibraryAdoption.md). Must resolve to an authorized LibraryAdoption in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_entry_version_id

New candidate source.

Required. Null is rejected.

References [LibraryEntryVersion](LibraryEntryVersion.md). Must resolve to an authorized LibraryEntryVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_draft_revision

Destination state at preview.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### plan_digest

Canonical diff, scope and rights digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### changes

Typed normalized paths, old and new digests and required conflict choices.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "maxProperties": 12
  },
  "maxItems": 20000,
  "minItems": 0
}
```

### state

Merge lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "previewed",
    "resolved",
    "applied",
    "superseded",
    "abandoned"
  ],
  "default": "previewed"
}
```

### created_at

Preview creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A merge plan applies only to its expected target revision and current rights.

## Unique keys

- `id`
- `library_adoption_id, plan_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| library_adoption_id, state, created_at | Resolve or report competing propagation plans. |

## Retention

Retain through the institutional draft and audit window. Purge only when abandoned, unreferenced and free of holds.
