# ItemTranslation

Candidate-facing locale overlay for one item version.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemTranslation identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Item version in the same bank and revision.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Item version in the same bank and revision.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### locale

Distinct requested localization.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8}){0,6}$"
}
```

### prompt

Translated rich content with stable block keys.

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

### interaction_keys

Canonical key coverage in actual displayed order.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### option_keys

Versioned ordered keys grouped by interaction, where local option keys retain their original meaning.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "interaction_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "keys": {
        "type": "array",
        "items": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
        },
        "minItems": 0,
        "maxItems": 100
      }
    },
    "required": [
      "interaction_key",
      "keys"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 32
}
```

### reviewed_by

Reviewer with bank and locale capability.

Optional. Nullable.

References [Principal](Principal.md). Reviewer with bank and locale capability.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Independent language approval time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Every canonical interaction and option key appears exactly once within its proper interaction.
- Translation does not alter expected values.

## Unique keys

- `id`
- `item_version_id, locale`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, locale | Resolve approved locale fallback. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
