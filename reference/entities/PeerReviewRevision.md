# PeerReviewRevision

Sealed external peer rubric and feedback scoped to one assigned review.

Owned by **assessment**.

## Fields

### id

Stable globally unique PeerReviewRevision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assignment_id

Exact peer review edge and eligible evaluator.

Required. Null is rejected.

References [PeerReviewAssignment](PeerReviewAssignment.md). Exact peer review edge and eligible evaluator.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Positive assignment-level revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### rubric_version_id

Pinned approved criterion definitions.

Required. Null is rejected.

References [RubricVersion](RubricVersion.md). Pinned approved criterion definitions.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### criteria

Typed criterion marks, states and safe codes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "criterion_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "points": {
        "type": "string",
        "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
      },
      "maximum": {
        "type": "string",
        "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
      },
      "disposition": {
        "type": "string",
        "enum": [
          "scored",
          "blank",
          "invalid",
          "manual_review",
          "excused"
        ]
      },
      "feedback_code": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "level_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      }
    },
    "required": [
      "criterion_key",
      "maximum",
      "disposition"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 128
}
```

### comments

Private and candidate-facing feedback.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "criterion_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "text": {
        "type": "string",
        "minLength": 1,
        "maxLength": 4000
      },
      "visibility": {
        "type": "string",
        "enum": [
          "candidate",
          "marker_only"
        ]
      }
    },
    "required": [
      "criterion_key",
      "text",
      "visibility"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 128
}
```

### evidence_digest

Exact assessed immutable work digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### submitted_at

Authoritative accepted review time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A submitted revision is immutable.
- Publication requires the configured moderation gate.

## Unique keys

- `id`
- `assignment_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assignment_id, revision | Resolve submitted review and revisions. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
