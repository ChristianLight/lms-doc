# LearningEvidence

Append-only validated event that can contribute to participation.

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

### institution_id

Evidence deduplication and ownership boundary.

Required. Null is rejected.

References [Institution](Institution.md). Same as the cited enrollment release and authenticated producer namespace.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_release_id

Exact assignment.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Exact delivered occurrence.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the course version in the cited EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Authenticated trusted producer.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### source_event_id

Stable producer event key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### source_revision

Version for replaceable state.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### sequence

Monotonic release-local ingestion sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### kind

Typed event class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "acknowledgment",
    "view",
    "video_coverage",
    "assessment_submission",
    "assessment_result",
    "attendance",
    "package",
    "accessible_equivalent",
    "waiver",
    "carry"
  ]
}
```

### payload

Validated source-kind payload and evidence references.

Required. Null is rejected.

```json
{
  "type": "object",
  "maxProperties": 20
}
```

### digest

Canonical replay comparison.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### occurred_at

Source instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### received_at

Authoritative accepted instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Same source key with changed digest conflicts.
- Client telemetry cannot stand in for trusted assessment or attendance.
- For multi-learner evidence fanout, each authoritative event uses one deterministic child event key per exact member release and placement. Cross-institution evidence cannot collide or disclose an existing key.

## Unique keys

- `id`
- `institution_id, source_namespace, source_event_id`
- `enrollment_release_id, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, content_placement_id, sequence | Deterministic placement rebuild. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
