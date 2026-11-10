# AttemptItem

Realized pinned form occurrence and private scoring inputs.

Owned by **assessment**.

## Fields

### id

Stable globally unique AttemptItem identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Owning attempt.

Required. Null is rejected.

References [Attempt](Attempt.md). Owning attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_slot_id

Slot in captured assessment revision.

Required. Null is rejected.

References [AssessmentSlot](AssessmentSlot.md). Slot in captured assessment revision.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### occurrence

Positive occurrence within a slot.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### display_order

Distinct order across realized form.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### item_version_id

Pinned selected item content.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Pinned selected item content.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### variant_profile_version_id

Exact variant generator revision when used.

Optional. Nullable.

References [VariantProfileVersion](VariantProfileVersion.md). Exact variant generator revision when used.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resolved_parameters

Versioned private and public rendered parameter vector under scoped access.

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
      "value": {
        "type": "string",
        "minLength": 1,
        "maxLength": 2048
      },
      "kind": {
        "type": "string",
        "enum": [
          "rational",
          "decimal",
          "identifier",
          "text"
        ]
      }
    },
    "required": [
      "key",
      "value",
      "kind"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 64
}
```

### choice_order

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
  "maxItems": 64
}
```

### locale

Effective reviewed localization.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8}){0,6}$"
}
```

### maximum

Realized slot maximum.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### digest

Canonical realized rendering and scoring input digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

## Integrity

- Realized form is immutable.
- All choice keys and referenced content belong to the resolved revision.

## Unique keys

- `id`
- `attempt_id, assessment_slot_id, occurrence`
- `attempt_id, display_order`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_id, display_order | Render and reconstruct exact candidate form. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
