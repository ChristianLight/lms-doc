# GradeAppeal

Records review request for a released grade, separate from item marking appeal.

Owned by **records**.

## Fields

### id

Stable globally unique GradeAppeal identifier.

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

### release_entry_id

Appealed visible release entry for this learner.

Required. Null is rejected.

References [GradeReleaseEntry](GradeReleaseEntry.md). Appealed visible release entry for this learner.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Review lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "received",
    "assigned",
    "evidence_requested",
    "upheld",
    "changed",
    "withdrawn"
  ],
  "default": "received"
}
```

### request_text

Learner or delegate statement.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### supporting_asset_ids

Protected and validated supporting material for this exact appeal.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Protected and validated supporting material for this exact appeal.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 10,
  "minItems": 0,
  "uniqueItems": true
}
```

### received_at

Trusted receipt timestamp.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### deadline_at

Appeal eligibility cutoff pinned at receipt.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### assigned_to

Authorized reviewer in offering.

Required. Nullable.

References [Principal](Principal.md). Authorized reviewer in offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### public_outcome

Approved outcome text if released.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### internal_reason

Restricted reviewer rationale.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### correction_release_id

Optional replacement release resolving the appeal.

Required. Nullable.

References [GradeRelease](GradeRelease.md). Optional replacement release resolving the appeal.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Review does not mutate evidence, grade or release directly.
- Duplicate open appeal for same release and scope requires merge or explicit distinct claim.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, received_at | Find scoped appeal cases. |
| enrollment_id, received_at | Display learner appeal history. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| received | assigned | AssignGradeAppeal | Reviewer authorized in offering Assign and audit review. |
| assigned | changed | ResolveGradeAppeal | Outcome accepted and correction linked Release permitted decision text. |
