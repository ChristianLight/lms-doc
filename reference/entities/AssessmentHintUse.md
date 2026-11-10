# AssessmentHintUse

Authorized durable use of one on-demand hint in an exact candidate scope.

Owned by **assessment**.

## Fields

### id

Stable durable hint receipt ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Item occurrence in the active candidate attempt.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Item occurrence in the active candidate attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### feedback_rule_id

On-demand rule in the exact realized item version.

Required. Null is rejected.

References [ItemFeedbackRule](ItemFeedbackRule.md). On-demand rule in the exact realized item version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### principal_id

Authorized candidate or active team editor who requested the hint.

Required. Null is rejected.

References [Principal](Principal.md). Authorized candidate or active team editor who requested the hint.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Monotonic disclosure sequence in the attempt-item scope.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 256
}
```

### requested_at

Authoritative disclosure time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A hint receipt is idempotent and does not mutate response or grade evidence.
- An item-scoped hint may be reviewed later only while candidate access and disclosure permit it.

## Unique keys

- `id`
- `attempt_item_id, ordinal`
- `attempt_item_id, feedback_rule_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_item_id, ordinal | Select next unrevealed authorized hint under attempt-item lock. |

## Retention

Retain with the scored activity evidence or until institutional formative evidence retention expires, subject to active holds.
