# GradeReleaseEntry

Learner/result row and immutable revision within an approved release.

Owned by **records**.

## Fields

### id

Stable globally unique GradeReleaseEntry identifier.

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

### release_id

Parent release in same offering.

Required. Null is rejected.

References [GradeRelease](GradeRelease.md). Parent release in same offering.

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

### grade_result_id

Stable target for learner and scope.

Required. Null is rejected.

References [GradeResult](GradeResult.md). Stable target for learner and scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### result_revision_id

Pinned immutable revision of exact result.

Required. Null is rejected.

References [GradeResultRevision](GradeResultRevision.md). Pinned immutable revision of exact result.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_entry_id

Previous same target and purpose visibility pointer.

Required. Nullable.

References [GradeReleaseEntry](GradeReleaseEntry.md). Previous same target and purpose visibility pointer.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### audience_kind

Maximum approved disclosure audience.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "learner",
    "approved_delegate",
    "staff_only"
  ]
}
```

### visible_from

Earliest instant at which active manifest grants visibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### prior_pointer_version

Visibility guard version staged for compare and swap.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

## Integrity

- Activation publishes one active effective pointer per target and purpose group.
- Current authorization is checked in addition to historical audience.

## Unique keys

- `id`
- `release_id, grade_result_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, grade_result_id, visible_from | Find effective released grades without private computation. |
| result_revision_id, release_id | Find documents and notifications sourced from a revision. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
