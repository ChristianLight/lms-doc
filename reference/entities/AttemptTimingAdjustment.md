# AttemptTimingAdjustment

Append-only timing intervention or permitted pause record.

Owned by **assessment**.

## Fields

### id

Stable globally unique AttemptTimingAdjustment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Affected active sitting.

Required. Null is rejected.

References [Attempt](Attempt.md). Affected active sitting.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sequence

Monotonic timing decision sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### actor_id

Authorized accommodation coordinator or permitted candidate.

Required. Null is rejected.

References [Principal](Principal.md). Authorized accommodation coordinator or permitted candidate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### kind

Extension, pause start, pause end or reviewed correction.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### prior_deadline_at

Effective prior exclusive cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### new_deadline_at

Computed replacement cutoff when applicable.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_at

Authoritative time of action.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason_code

Non-sensitive reason classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### incident_id

Restricted linked incident only where applicable.

Optional. Nullable.

References [ExamIncident](ExamIncident.md). Restricted linked incident only where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Changing timer policy does not mutate original start snapshot.
- Pause seconds counted at most once.
- Existing sealed evidence is immutable.

## Unique keys

- `id`
- `attempt_id, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_id, sequence | Reconstruct each effective deadline and audit timeline. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
