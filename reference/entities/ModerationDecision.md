# ModerationDecision

Adjudication of independent marking and correction disposition.

Owned by **assessment**.

## Fields

### id

Stable globally unique ModerationDecision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Same offering-scoped item being moderated.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Same offering-scoped item being moderated.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### input_mark_ids

Frozen independent provisional or accepted inputs.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). Frozen independent provisional or accepted inputs.

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

### reviewer_id

Authorized independent moderator.

Required. Null is rejected.

References [Principal](Principal.md). Authorized independent moderator.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### action

Choose, adjust, request third, void or excuse.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "choose_mark",
    "adjust_criteria",
    "assign_third",
    "void",
    "excuse"
  ]
}
```

### reason

Protected factual justification.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### output_mark_id

Result revision in same item scope when created.

Optional. Nullable.

References [ItemMarkRevision](ItemMarkRevision.md). Result revision in same item scope when created.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decided_at

Effective approval instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Independent review capabilities and score bounds enforced.
- Reason and inputs remain immutable.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_item_id, decided_at | Historical moderation and appeal trail. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
