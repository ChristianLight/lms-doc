# DraftPlacement

Editable placement instance and pointer within an outline workspace.

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

Owning draft.

Required. Null is rejected.

References [CourseDraft](CourseDraft.md). Must resolve to an authorized CourseDraft in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_key

Stable course-scoped occurrence identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_key

Parent occurrence in same draft or null root.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sibling_scope_key

Server-derived root token or parent/ followed by the lowercase UUID from parent_key. Used to enforce unique root and child positions without nullable key semantics.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(root|parent/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})$"
}
```

### position

Zero-based contiguous sibling order.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 511
}
```

### kind

Validated display node type.

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

Pinned availability and completion definition.

Optional. Nullable.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### visibility

Default author intent.

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

### required

Required occurrence in eligible branch.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### alias

Optional local display title.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

## Integrity

- Exactly one payload kind selected.
- Positions contiguous and tree acyclic.
- Compute sibling_scope_key on every insertion and reparent. A null parent_key requires root. A present parent requires parent/ plus that exact parent UUID. Reject inconsistencies before commit.

## Unique keys

- `id`
- `course_draft_id, placement_key`
- `course_draft_id, sibling_scope_key, position`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_draft_id, sibling_scope_key, position | Sibling traversal. |
| content_node_version_id | Draft dependency impact. |
| activity_version_id | Draft activity use. |

## Retention

Retain through the institutional draft and audit window. Purge only when abandoned, unreferenced and free of holds.
