# ContentPlacement

Exact placement in one frozen publication.

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

### course_version_id

Exact published outline.

Required. Null is rejected.

References [CourseVersion](CourseVersion.md). Must resolve to an authorized CourseVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_key

Stable course occurrence key.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_placement_id

Exact parent in this version or virtual root.

Optional. Nullable.

References [ContentPlacement](ContentPlacement.md). Parent must belong to same course version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sibling_scope_key

Server-derived root token or parent/ followed by the lowercase UUID from parent_placement_id. Used to enforce unique root and child positions without nullable key semantics.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(root|parent/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$"
}
```

### position

Frozen contiguous sibling position.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 511
}
```

### kind

Frozen display type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "module",
    "topic",
    "lesson",
    "rich_text",
    "image",
    "document",
    "video",
    "audio",
    "external_link",
    "internal_link",
    "activity",
    "imported_unresolved"
  ]
}
```

### content_node_version_id

Structural or resource payload.

Optional. Nullable.

References [ContentNodeVersion](ContentNodeVersion.md). Must resolve to an authorized ContentNodeVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Action payload.

Optional. Nullable.

References [ActivityVersion](ActivityVersion.md). Must resolve to an authorized ActivityVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Pinned learning rule.

Optional. Nullable.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### required

Required in eligible branch.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### visibility

Frozen visibility intent.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "visible",
    "locked",
    "hidden"
  ],
  "default": "visible"
}
```

### alias

Optional local title.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

## Integrity

- Version-owned parent, exclusive payload and acyclic tree.
- Stable key is never a substitute for exact ID in academic evidence.
- Compute sibling_scope_key on every insertion and reparent. A null parent_placement_id requires root. A present parent requires parent/ plus that exact parent UUID. Reject inconsistencies before commit.

## Unique keys

- `id`
- `course_version_id, placement_key`
- `course_version_id, sibling_scope_key, position`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_version_id, sibling_scope_key, position | Ordered authorized renderer traversal. |
| content_node_version_id | Published resource impact. |
| activity_version_id | Published activity impact. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
