# AssessmentFeedbackRelease

Per-submission visible feedback fields pinned to mark revisions.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentFeedbackRelease identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Candidate scope for disclosure.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Candidate scope for disclosure.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic feedback release version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### mark_revision_ids

Exact accepted marks within submission.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). Exact accepted marks within submission.

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

### fields

Authorized candidate-visible content categories.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "response",
      "points",
      "rubric",
      "comments",
      "answer_key",
      "model_solution"
    ]
  },
  "minItems": 0,
  "maxItems": 6
}
```

### released_by

Actor with feedback disclosure authority.

Required. Null is rejected.

References [Principal](Principal.md). Actor with feedback disclosure authority.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### released_at

Effective disclosure instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### previous_release_id

Historical feedback release of same candidate submission.

Optional. Nullable.

References [AssessmentFeedbackRelease](AssessmentFeedbackRelease.md). Historical feedback release of same candidate submission.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Feedback release cannot advance official academic results.
- Released fields and provenance immutable.

## Unique keys

- `id`
- `submission_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| submission_id, released_at | Find candidate-visible approved feedback projection. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
