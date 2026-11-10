# AttendanceRevision

Immutable proposed, published or corrected attendance decision.

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

### attendance_entry_id

Stable learner-occurrence record.

Required. Null is rejected.

References [AttendanceEntry](AttendanceEntry.md). Must resolve to an authorized AttendanceEntry in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### version

Monotonic decision version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### status

Learning attendance classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "present",
    "late",
    "absent",
    "excused",
    "unrecorded"
  ]
}
```

### source

Authorized decision route.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "teacher",
    "check_in",
    "provider",
    "correction"
  ]
}
```

### source_evidence_key

Optional proposal or provider reference.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### publication

Whether decision is authoritative.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "proposed",
    "published"
  ]
}
```

### actor_id

Accountable actor or verified integration.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### prior_revision_id

Superseded prior decision.

Optional. Nullable.

References [AttendanceRevision](AttendanceRevision.md). Must resolve to an authorized AttendanceRevision in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Reason required for correction.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1200
}
```

### recorded_at

Append instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Corrections append and may require academic impact review.

## Unique keys

- `id`
- `attendance_entry_id, version`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attendance_entry_id, publication, version | Current proposal and decision history. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
