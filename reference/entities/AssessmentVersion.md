# AssessmentVersion

Versioned assembly, marking and navigation plan.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_id

Stable definition and course scope.

Required. Null is rejected.

References [Assessment](Assessment.md). Stable definition and course scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic revision in the assessment.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### state

Editable draft or immutable publication. Review approval is a separate AssessmentAssemblyReview record.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published"
  ]
}
```

### draft_version

Authoring optimistic lock sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### purpose

Candidate use and default delivery policy category.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "practice",
    "survey",
    "coursework",
    "quiz",
    "formal_exam"
  ]
}
```

### maximum

Total maximum for the resolved form.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### content_digest

Digest over published form assembly rules.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### published_by

Approved publisher for this version.

Optional. Nullable.

References [Principal](Principal.md). Approved publisher for this version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_at

Release time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Validate feasible variants and total scale before publication.
- Bind immutable section, pool and scoring references.

## Unique keys

- `id`
- `assessment_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assessment_id, state, revision | Resolve active eligible assessment publications. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishAssessmentVersion | Assembly gate and independent review pass. Publish exact draft digest and version. |
