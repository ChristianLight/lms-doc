# LibraryAdoption

Provenance and update baseline for a target draft placement.

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

### source_entry_version_id

Pinned adopted source baseline.

Required. Null is rejected.

References [LibraryEntryVersion](LibraryEntryVersion.md). Must resolve to an authorized LibraryEntryVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_draft_id

Current editable destination.

Required. Null is rejected.

References [CourseDraft](CourseDraft.md). Must resolve to an authorized CourseDraft in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_placement_key

Owning destination occurrence.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### mode

Adoption policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "linked",
    "independent",
    "managed_template"
  ]
}
```

### source_map

Reviewed occurrence identity mapping.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "source_key": {
        "type": "string",
        "format": "uuid"
      },
      "target_key": {
        "type": "string",
        "format": "uuid"
      }
    },
    "required": [
      "source_key",
      "target_key"
    ],
    "additionalProperties": false
  },
  "maxItems": 20000,
  "minItems": 1
}
```

### revision

Baseline compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### active

Eligible for future update proposals.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

## Integrity

- One active managed parent for each destination placement.
- Independent copy cannot auto-sync.

## Unique keys

- `id`
- `target_draft_id, target_placement_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| source_entry_version_id, active | Find consumers requiring update. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
