# PackageActivityAttempt

Internal sequencing state for one occurrence attempt within a package registration.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### registration_id

Package attempt owner.

Required. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### occurrence_id

Tracked activity occurrence.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_attempt_id

Owning cluster attempt, absent only for the root.

Optional. Null is rejected.

References [PackageActivityAttempt](PackageActivityAttempt.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sco_state_id

Associated current SCO state, when applicable.

Optional. Null is rejected.

References [PackageScoState](PackageScoState.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Activity attempt counter scoped to registration and occurrence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 10000
}
```

### status

Internal sequencing lifecycle state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "ended",
    "abandoned"
  ]
}
```

### attempt_progress_known

Whether progress measures are authoritative.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### attempt_completion_known

Whether completion tracking is initialized.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### completed

Completion result interpreted only when known.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### duration_ms

Credited activity attempt duration.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### experienced_duration_ms

Time spent actively experiencing this activity, excluding suspension.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### progress_measure

Known normalized progress measure in [0,1] or omitted when unknown.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:0|[1-9][0-9]{0,11})(?:\\.[0-9]{1,6})?$"
}
```

### suspended_at

Most recent authoritative suspension time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### resumed_at

Most recent authoritative resume time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### selected_child_ids

Frozen selected and ordered child occurrence IDs when selection applies.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Each child is under this exact occurrence.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 10000,
  "minItems": 0,
  "uniqueItems": true
}
```

### start_time

Attempt start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### end_time

Attempt close.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### attempt_mode

Authorized creation scope. Only eligible credit attempts contribute official evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "normal_credit",
    "browse_no_credit",
    "review_no_credit",
    "preview"
  ]
}
```

## Integrity

- Knownness and Boolean result are independent.
- Frozen child order is reused on resume.
- An ungraded or preview context uses a distinct attempt-mode namespace and does not consume the official attempt count.

## Unique keys

- `id`
- `registration_id, occurrence_id, attempt_mode, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| registration_id, status | Find current and suspended sequencing path. |

## Retention

Retain as package progression evidence with registration.
