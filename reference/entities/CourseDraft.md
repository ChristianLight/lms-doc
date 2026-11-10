# CourseDraft

Mutable outline workspace with a versioned review boundary.

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

Course being edited.

Required. Null is rejected.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### base_course_version_id

Optional prior publication.

Optional. Nullable.

References [CourseVersion](CourseVersion.md). Must resolve to an authorized CourseVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_principal_id

Responsible author.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Draft compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### state

Authoring state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "in_review",
    "changes_requested",
    "approved",
    "published",
    "abandoned"
  ],
  "default": "draft"
}
```

### digest

Current canonical manifest input digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### approved_digest

Exact independently approved digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### updated_at

Last authoritative mutation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### name

Author-facing workspace name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### default_locale

Draft-specific default locale pinned by manifest at publication.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
}
```

## Integrity

- All accepted draft edits invalidate earlier approvals.
- Base publication belongs to same course.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_id, state, updated_at | List active and abandoned drafts. |
| course_id, approved_digest | Locate a reviewable digest. |

## Retention

Retain through the institutional draft and audit window. Purge only when abandoned, unreferenced and free of holds.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | in_review | SubmitCourseDraft | Current digest validates. Pin review inputs. |
| in_review | approved | DecideCourseDraft | Approval authority and same digest. Record reviewer and approval digest. |
| in_review | changes_requested | DecideCourseDraft | Reviewer supplied at least one issue. Return to author. |
| changes_requested | draft | MutateDraftOutline | Authorized edit uses current revision. Invalidate prior validation. |
| approved | draft | MutateDraftOutline | Authorized changed edit. Invalidate exact approval. |
| approved | published | PublishCourseVersion | Manifest validated and exact approved digest. Seal publication. |
| draft | abandoned | AbandonCourseDraft | No active publication transaction. Remove from ordinary author workspace. |
| in_review | abandoned | AbandonCourseDraft | Actor can abandon and draft has no committed publication. End ordinary editing and retain review and audit history. |
| changes_requested | abandoned | AbandonCourseDraft | Actor can abandon and draft has no committed publication. End ordinary editing and retain review and audit history. |
| approved | abandoned | AbandonCourseDraft | Actor can abandon and draft has no committed publication. End ordinary editing and retain review and audit history. |
