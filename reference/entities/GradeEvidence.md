# GradeEvidence

Immutable observed scoring revision accepted from an authorized producer.

Owned by **assessment**.

## Fields

### id

Stable globally unique GradeEvidence identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Institution and offering boundary checked against enrollment and grade item.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Institution and offering boundary checked against enrollment and grade item.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Beneficiary who owns relevant academic enrollment.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Beneficiary who owns relevant academic enrollment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_item_id

Approved gradebook line in same offering.

Required. Null is rejected.

References [GradeItem](GradeItem.md). Approved gradebook line in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_kind

Native, manual, package or external source class.

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

Opaque stable source identity verified against trusted registration.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_revision

Monotonic source revision within evidence tuple.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### delivery_id

Required native activity scope only.

Optional. Nullable.

References [AssessmentDelivery](AssessmentDelivery.md). Required native activity scope only.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Required native source evidence only.

Optional. Nullable.

References [Attempt](Attempt.md). Required native source evidence only.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_ordinal

Native candidate attempt number, absent for non-native evidence.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### submitted_at

Effective native submission time used by the academic lateness policy.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### assessment_version_id

Native assessment revision pinned at start.

Optional. Nullable.

References [AssessmentVersion](AssessmentVersion.md). Native assessment revision pinned at start.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Native delivery policy revision pinned at start.

Optional. Nullable.

References [DeliveryPolicyVersion](DeliveryPolicyVersion.md). Native delivery policy revision pinned at start.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### late

Whether the native submission met the captured published due classification.

Optional. Nullable.

```json
{
  "type": "boolean"
}
```

### status

Earned, excused, voided or technical exception.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "earned",
    "excused",
    "voided",
    "technical_exception"
  ]
}
```

### points

Canonical earned points, null for non-earned status.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### maximum

Canonical positive maximum, null for non-earned status.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### mark_revision_ids

Exact source mark lineage for native evidence, empty for other sources.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). Exact source mark lineage for native evidence, empty for other sources.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### lineage_digest

Source authorization, scoring revision and input lineage fingerprint.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### accepted_at

Authoritative evidence acceptance time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### supersedes_id

Previous revision for same tuple, null for first.

Required. Nullable.

References [GradeEvidence](GradeEvidence.md). Previous revision for same tuple, null for first.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approval_reference

Verified authorized producer approval for non-native evidence.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_release_id

Native beneficiary release pinned at sitting start, including an individual member of team work.

Optional. Nullable.

References [EnrollmentRelease](EnrollmentRelease.md). Native beneficiary release pinned at sitting start, including an individual member of team work.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Authorized producers cannot bind unrelated enrollment or grade item.
- Native source object ID equals attempt ID.
- Earned values must lie in grade item approved range.
- Missing is derived by academic policy, not emitted.
- Native enrollment_release_id must belong to the beneficiary Enrollment and point to the exact captured individual or team member release.

## Unique keys

- `id`
- `grade_item_id, enrollment_id, source_kind, source_object_id, source_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, enrollment_id, grade_item_id | Read verified evidence for academic projection. |
| grade_item_id, enrollment_id, source_kind, source_object_id, source_revision | Resolve monotonic evidence head and gaps. |

## Retention

Retain to satisfy referenced official results and audit obligations. Delete only through approved evidence retention process.
