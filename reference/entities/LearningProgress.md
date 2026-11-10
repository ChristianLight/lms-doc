# LearningProgress

Rebuildable projection for one exact enrollment release and placement.

Owned by **participation**.

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

### enrollment_release_id

Exact participation release.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Exact placement.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the course version in the cited EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Evaluated rule.

Optional. Nullable.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Display lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "not_started",
    "in_progress",
    "completed",
    "exempt"
  ],
  "default": "not_started"
}
```

### first_evidence_at

First accepted relevant instant.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### last_evidence_at

Most recent accepted relevant instant.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### evidence_count

Accepted distinct count.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991,
  "default": 0
}
```

### projected_sequence

Last processed sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991,
  "default": 0
}
```

### revision

Projection compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

## Integrity

- Projection cannot mutate a CompletionRecord.
- Historical releases remain separately addressable.

## Unique keys

- `id`
- `enrollment_release_id, content_placement_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, state | Learner progress summary. |
| content_placement_id, state | Scoped staff aggregation after ACL. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
