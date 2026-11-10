# ProgressResume

Private current navigation checkpoint, independent of evidence.

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

Current release.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Selected authorized exact placement.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the course version in the cited EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### anchor

Optional content block anchor.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### media_position_ms

Optional current playback position.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 86400000
}
```

### session_id

Client session token.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### session_sequence

Increasing per session.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### revision

Server compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### updated_at

Authoritative accepted instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Stale browser session cannot silently overwrite newer resume.
- Never records learning completion.

## Unique keys

- `id`
- `enrollment_release_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, updated_at | Personal resume view. |

## Retention

Retain for the configured operational interval. Purge or de-identify after expiry when no academic reference or hold applies.
