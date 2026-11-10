# ItemPoolVersion

Reviewed frozen selection inventory and item metadata.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemPoolVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution permitted to select items.

Required. Null is rejected.

References [Institution](Institution.md). Institution permitted to select items.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pool_key

Institution-scoped logical pool key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### revision

Monotonic pool revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### eligible_items

Pinned item revisions and reviewed coverage and variant metadata.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "item_version_id": {
        "type": "string",
        "format": "uuid"
      },
      "variant_profile_version_id": {
        "type": "string",
        "format": "uuid"
      },
      "difficulty": {
        "type": "integer",
        "minimum": 1,
        "maximum": 10
      },
      "tags": {
        "type": "array",
        "items": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
        },
        "minItems": 0,
        "maxItems": 32
      }
    },
    "required": [
      "item_version_id",
      "difficulty",
      "tags"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 25000
}
```

### digest

Digest over frozen item set and metadata.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### approved_by

Pool reviewer with all necessary bank read and reuse rights.

Required. Null is rejected.

References [Principal](Principal.md). Pool reviewer with all necessary bank read and reuse rights.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Pool approval time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Candidates are resolved from a frozen list rather than a current query.
- Item revision appears at most once per pool.

## Unique keys

- `id`
- `institution_id, pool_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, pool_key | Find versioned bank-derived pools. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
