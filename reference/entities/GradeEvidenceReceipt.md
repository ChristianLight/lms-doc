# GradeEvidenceReceipt

Records-side pointer to verified immutable evidence and source sequence.

Owned by **records**.

## Fields

### id

Stable globally unique GradeEvidenceReceipt identifier.

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

Mapped line in same offering.

Required. Null is rejected.

References [GradeItem](GradeItem.md). Mapped line in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evidence_id

Original accepted evidence with matching offering, item and enrollment.

Required. Null is rejected.

References [GradeEvidence](GradeEvidence.md). Original accepted evidence with matching offering, item and enrollment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### producer

Authorized producer identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### event_id

Stable original message ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_kind

Immutable originating source type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native",
    "manual",
    "package",
    "external"
  ]
}
```

### source_object_id

Opaque source stream identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_revision

Authoritative stream sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### evidence_digest

Verified source lineage digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### received_at

Records intake UTC timestamp.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### status

Intake disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "accepted",
    "quarantined",
    "reconciled"
  ],
  "default": "accepted"
}
```

## Integrity

- Conflicting duplicate source digest quarantines event in the platform inbox before accepted academic receipt.
- Later arrival does not replace a higher source sequence.

## Unique keys

- `id`
- `producer, event_id`
- `evidence_id`
- `grade_item_id, enrollment_id, source_kind, source_object_id, source_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, grade_item_id, source_object_id, source_revision | Select a scoped source head at cutoff. |
| offering_id, status, received_at | Locate intake gaps and exceptions. |

## Retention

Retain according to institution audit retention and hold. Keep source pointers while a retained official output requires them.
