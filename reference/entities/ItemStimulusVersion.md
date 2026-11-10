# ItemStimulusVersion

Immutable shared stimulus independently reusable across assessment items.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemStimulusVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution that owns this content.

Required. Null is rejected.

References [Institution](Institution.md). Institution that owns this content.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### stimulus_key

Institution-scoped reusable stimulus series key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### revision

Monotonic revision for the series.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### locale

Canonical stimulus language.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8}){0,6}$"
}
```

### content

Safe rich media or text blocks.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "format": {
        "type": "string",
        "enum": [
          "sanitized_html",
          "text",
          "asset",
          "math"
        ]
      },
      "value": {
        "type": "string",
        "minLength": 1,
        "maxLength": 50000
      }
    },
    "required": [
      "key",
      "format",
      "value"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 256
}
```

### asset_version_ids

Permitted immutable asset references.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Permitted immutable asset references.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### digest

Canonical stimulus content and accessibility manifest digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### published_at

Release time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Only published stimuli may be pinned to published items.

## Unique keys

- `id`
- `institution_id, stimulus_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, stimulus_key | Resolve stimulus reuse and revision lineage. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
