# DraftReview

Append-only reviewer decision bound to one exact draft input.

Owned by **curriculum**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_draft_id

Reviewed draft.

Required. Null is rejected.

References [CourseDraft](CourseDraft.md). Must resolve to an authorized CourseDraft in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### draft_revision

Reviewed draft revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### digest

Reviewed canonical digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### reviewer_id

Accountable review actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision

Review disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "approved",
    "changes_requested"
  ]
}
```

### issues

Structured review findings.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "code": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
      },
      "path": {
        "type": "string",
        "minLength": 1,
        "maxLength": 500
      },
      "message": {
        "type": "string",
        "minLength": 1,
        "maxLength": 1200
      },
      "blocking": {
        "type": "boolean"
      }
    },
    "required": [
      "code",
      "path",
      "message",
      "blocking"
    ],
    "additionalProperties": false
  },
  "maxItems": 250,
  "minItems": 0
}
```

### decided_at

Authoritative decision time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Publish approval uses this exact digest.
- Reviewed findings contain no answer key values.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_draft_id, draft_revision, decided_at | Show historical decisions and sign-off. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
