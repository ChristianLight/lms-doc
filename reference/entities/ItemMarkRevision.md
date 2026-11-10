# ItemMarkRevision

Immutable provisional or accepted judgment on an attempt item.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemMarkRevision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Realized item being judged.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Realized item being judged.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Exact submitted evidence for this item.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Exact submitted evidence for this item.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic item mark revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### assignment_id

Assigned reviewer workflow where human scoring contributes.

Optional. Nullable.

References [MarkingAssignment](MarkingAssignment.md). Assigned reviewer workflow where human scoring contributes.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evaluation_run_ids

Verified exact-scope evaluation run inputs.

Required. Null is rejected.

References [EvaluationRun](EvaluationRun.md). Verified exact-scope evaluation run inputs.

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

### marker_id

Authorized marker, moderator or service principal.

Required. Null is rejected.

References [Principal](Principal.md). Authorized marker, moderator or service principal.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source

Source class used for audit and review.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "deterministic",
    "human",
    "moderated",
    "manual_correction"
  ]
}
```

### criteria

Individual criterion values and dispositions.

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

### private_comments

Scoped comments with declared visibility.

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

### points

Total raw awarded points in this item mark.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### maximum

Actual scored maximum under pinned item rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### state

Provisional or accepted lifecycle projection.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "provisional",
    "accepted",
    "rejected",
    "superseded"
  ]
}
```

### accepted_at

Approval time for contributing revision.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### supersedes_id

Earlier authoritative mark for same attempt item if corrected.

Optional. Nullable.

References [ItemMarkRevision](ItemMarkRevision.md). Earlier authoritative mark for same attempt item if corrected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- One accepted current head per attempt item.
- A correction appends rather than edits scored evidence.
- Independent provisional marks remain inspectable by authorized staff.

## Unique keys

- `id`
- `attempt_item_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_item_id, state, revision | Find accepted mark head and immutable provenance. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
