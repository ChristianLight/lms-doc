# PracticeCheck

Non-submission formative check over acknowledged response revisions.

Owned by **assessment**.

## Fields

### id

Stable globally unique PracticeCheck identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Eligible practice occurrence.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Eligible practice occurrence.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sequence

Monotonic accepted check ordinal.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### response_heads

Exact acknowledged response set.

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
      "response_revision_id": {
        "type": "string",
        "format": "uuid"
      }
    },
    "required": [
      "interaction_key",
      "response_revision_id"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 64
}
```

### input_digest

Pinned response and rule contract digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### result

Candidate-safe outcome without exposing private keys.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "correct",
    "partial",
    "incorrect",
    "unresolved"
  ]
}
```

### feedback_code

Approved feedback code under practice visibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### checked_at

Authoritative acceptance instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Never emits grade evidence or seals assessment.
- Parsing and infrastructure failure do not consume a check.

## Unique keys

- `id`
- `attempt_item_id, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_item_id, sequence | Enforce formative check count and response replay. |

## Retention

Retain while practice evidence, learner review or operational hold is applicable.
