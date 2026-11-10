# SelfReviewRevision

Candidate self-reflection against own sealed coursework and pinned rubric.

Owned by **assessment**.

## Fields

### id

Stable globally unique SelfReviewRevision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Sealed candidate submission under configured self review policy.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Sealed candidate submission under configured self review policy.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

The same candidate or eligible captured team member.

Required. Null is rejected.

References [Enrollment](Enrollment.md). The same candidate or eligible captured team member.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic self review revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### rubric_version_id

Immutable approved guide.

Required. Null is rejected.

References [RubricVersion](RubricVersion.md). Immutable approved guide.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### criteria

Candidate self-evaluation stored independently of staff marking.

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
  "maxItems": 64
}
```

### comments

Optional candidate notes and reflections.

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
  "maxItems": 64
}
```

### submitted_at

Authoritative self review acceptance time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- No self evaluation updates ItemMarkRevision or GradeEvidence.
- Separate from anonymous peer allocations.

## Unique keys

- `id`
- `submission_id, enrollment_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| submission_id, enrollment_id, revision | Read own self-review history and staff-approved visibility. |

## Retention

Retain under delivery feedback policy and any evidentiary holds.
