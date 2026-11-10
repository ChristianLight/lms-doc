# PackageScoState

Current confirmed run-time state for one registration and activity occurrence.

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

Owning learner attempt.

Required. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### occurrence_id

SCO occurrence within registered organization.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### launch_count

Count of activated sessions for this occurrence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### total_time_ms

Exact fixed-unit millisecond projection only when duration has no unresolved calendar components.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### last_exit

Edition-specific prior exit token.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 32
}
```

### completion_status

Last accepted raw completion token, when supported.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### success_status

Last accepted raw success token, when supported.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### state_revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### updated_at

UTC time of last durably accepted mutation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### activity_attempt_id

Activity attempt whose RTE model this is.

Required. Null is rejected.

References [PackageActivityAttempt](PackageActivityAttempt.md). Same registration and exact occurrence.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### duration_total

Lossless duration sum. Preserve calendar components separately from fixed elapsed units.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "years": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "months": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "fixed_milliseconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    }
  },
  "required": [
    "years",
    "months",
    "fixed_milliseconds"
  ],
  "additionalProperties": false
}
```

## Integrity

- Raw status values remain edition-specific.
- A read of cached values is not evidence of commit.
- Only the runtime owner can write after valid edition checks.
- A new attempt within an existing registration starts from edition defaults. A resumed attempt reuses its own state. Preview, browse and review state never replaces official attempt evidence.

## Unique keys

- `id`
- `activity_attempt_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| registration_id, occurrence_id, state_revision | Read this registration occurrence history using the selected attempt pointer. |

## Retention

Retain under registration policy. Apply additional restricted handling for sensitive elements.
