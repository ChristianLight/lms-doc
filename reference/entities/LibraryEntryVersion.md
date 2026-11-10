# LibraryEntryVersion

Published immutable entry or template baseline.

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

### library_entry_id

Stable library item.

Required. Null is rejected.

References [LibraryEntry](LibraryEntry.md). Must resolve to an authorized LibraryEntry in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic publication number.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### content_node_version_id

Exact resource payload.

Optional. Nullable.

References [ContentNodeVersion](ContentNodeVersion.md). Must resolve to an authorized ContentNodeVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Exact activity payload.

Optional. Nullable.

References [ActivityVersion](ActivityVersion.md). Must resolve to an authorized ActivityVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### template_course_version_id

Exact outline publication used as a managed template.

Optional. Nullable.

References [CourseVersion](CourseVersion.md). Must resolve to an authorized CourseVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### protected_paths

Managed JSON pointers or structural aspects.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 400
  },
  "maxItems": 64,
  "minItems": 0
}
```

### license_key

Approved use rules.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### digest

Entry manifest digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
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

Publication instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Exactly one payload binds, matching entry kind.

## Unique keys

- `id`
- `library_entry_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| library_entry_id, published_at | Entry versions and updates. |
| template_course_version_id | Template dependency impact. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
