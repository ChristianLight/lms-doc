# CompetencyEvidence

Accepted observed outcome level with exact educational source revision.

Owned by **records**.

## Fields

### id

Stable globally unique CompetencyEvidence identifier.

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

### person_id

Educational identity within the same institution.

Required. Null is rejected.

References [Person](Person.md). Educational identity within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### competency_version_id

Pinned outcome and ordered scale.

Required. Null is rejected.

References [CompetencyVersion](CompetencyVersion.md). Pinned outcome and ordered scale.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### alignment_id

Approved source mapping if used.

Required. Nullable.

References [CompetencyAlignment](CompetencyAlignment.md). Approved source mapping if used.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Optional same-person course evidence scope.

Required. Nullable.

References [Enrollment](Enrollment.md). Optional same-person course evidence scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_release_entry_id

Released grade source if applicable.

Required. Nullable.

References [GradeReleaseEntry](GradeReleaseEntry.md). Released grade source if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_mark_revision_id

Verified rubric or item mark if applicable.

Required. Nullable.

References [ItemMarkRevision](ItemMarkRevision.md). Verified rubric or item mark if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### recognition_decision_id

Accepted prior evidence if applicable.

Required. Nullable.

References [RecognitionDecision](RecognitionDecision.md). Accepted prior evidence if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Corrected source revision within same observation.

Required. Nullable.

References [CompetencyEvidence](CompetencyEvidence.md). Corrected source revision within same observation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_key

Stable identity of the observation source.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_revision

Monotonic source revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### level_code

Approved observed competency level.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### state

Eligibility disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "accepted",
    "revoked",
    "unverified"
  ]
}
```

### observed_at

Effective observation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Optional exclusive evidence cutoff.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
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

- One effective evidence revision per observation source.
- Observed source and learner association verified.

## Unique keys

- `id`
- `person_id, competency_version_id, source_key, source_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, competency_version_id, observed_at | Resolve effective outcome evidence chronology. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
