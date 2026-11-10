# CourseVersion

Immutable published outline manifest.

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

### course_id

Logical owner.

Required. Null is rejected.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_draft_id

Published draft audit pointer.

Required. Null is rejected.

References [CourseDraft](CourseDraft.md). Must resolve to an authorized CourseDraft in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### version

Monotonic publication ordinal within course.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### draft_digest

Approved canonical inputs.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### manifest_digest

Final canonical published manifest SHA-256.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### manifest_locator

Private verified object locator.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 500
}
```

### published_by

Accountable publisher.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_at

Atomic visibility time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Availability status separate from manifest.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "published",
    "archived",
    "withdrawn"
  ],
  "default": "published"
}
```

## Integrity

- Manifest must be durably present before transaction commits.
- Archived publication cannot become a new offering default without reviewed reactivation.

## Unique keys

- `id`
- `course_id, version`
- `course_id, draft_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_id, published_at | Version history. |
| manifest_digest | Integrity and deduplication audit. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| published | archived | ArchiveCourseVersion | Authorized and actual uses acknowledged. Exclude from ordinary future release selection without altering manifest. |
