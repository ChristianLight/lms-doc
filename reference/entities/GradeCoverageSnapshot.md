# GradeCoverageSnapshot

Authoritative source coverage and missing decisions frozen for a calculation or final close.

Owned by **records**.

## Fields

### id

Stable globally unique GradeCoverageSnapshot identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Enrollment in the named offering and institution.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment in the named offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_item_id

Expected same-offering gradebook line.

Required. Null is rejected.

References [GradeItem](GradeItem.md). Expected same-offering gradebook line.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_release_id

Exact participation release for applicability.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Exact participation release for applicability.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### schedule_override_id

Approved effective deadline override if applicable.

Required. Nullable.

References [ScheduleOverride](ScheduleOverride.md). Approved effective deadline override if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### cutoff_at

As-of cutoff used to reconcile applicability and evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### due_at

Effective UTC deadline when assigned.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Distinct scoped finality status.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "not_applicable",
    "not_due",
    "confirmed_missing",
    "pending_mark",
    "scored",
    "excused",
    "unknown"
  ]
}
```

### source_vector

Reviewed producer checkpoint set.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "producer": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9._-]{0,63}$"
      },
      "partition": {
        "type": "string",
        "minLength": 1,
        "maxLength": 128
      },
      "sequence": {
        "type": "integer",
        "minimum": 0,
        "maximum": 9007199254740991
      },
      "digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      }
    },
    "required": [
      "producer",
      "partition",
      "sequence",
      "digest"
    ],
    "additionalProperties": false
  },
  "maxItems": 64,
  "minItems": 1
}
```

### fingerprint

Exact frozen source, due and applicability snapshot digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Confirmed missing requires approved applicability, elapsed due and complete authoritative submission source.
- Unknown coverage cannot be scored as zero.

## Unique keys

- `id`
- `enrollment_id, grade_item_id, fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, cutoff_at, state | Identify missing and pending blockers before final release. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
