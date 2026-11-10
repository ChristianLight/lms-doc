# MarkDraftRevision

Private marker draft snapshot retained for attribution and reassignment audit.

Owned by **assessment**.

## Fields

### id

Stable globally unique MarkDraftRevision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assignment_id

The exact scoped marking task.

Required. Null is rejected.

References [MarkingAssignment](MarkingAssignment.md). The exact scoped marking task.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic draft snapshot revision within assignment.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### marker_id

Authenticated assigned writer at time of save.

Required. Null is rejected.

References [Principal](Principal.md). Authenticated assigned writer at time of save.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_version_id

Pinned same-item scoring guide.

Required. Null is rejected.

References [RubricVersion](RubricVersion.md). Pinned same-item scoring guide.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### criteria

Typed private rubric score draft.

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

Scoped draft comments with declared visibility.

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

### digest

Exact draft values and attribution digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### saved_at

Authoritative save time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A subsequent marker cannot submit a draft authored under former marker assignment.
- Candidate projection has no access.

## Unique keys

- `id`
- `assignment_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assignment_id, marker_id, revision | Retrieve drafts for current authorized reviewer and protected audit. |

## Retention

Delete superseded drafts after institutional moderation and appeal policy, subject to retention holds.
