# ItemVersion

Immutable published prompt, response and evaluation graph.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_id

Stable item whose bank controls access.

Required. Null is rejected.

References [Item](Item.md). Stable item whose bank controls access.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic revision within the item.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### base_version_id

Earlier revision of the same item.

Optional. Nullable.

References [ItemVersion](ItemVersion.md). Earlier revision of the same item.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Workflow lifecycle and new selection eligibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "in_review",
    "approved",
    "published",
    "withdrawn"
  ]
}
```

### draft_version

Strong authoring compare-and-swap sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### locale

Canonical authored language.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z]{2,8}(-[A-Za-z0-9]{1,8}){0,6}$"
}
```

### prompt

Ordered public preorder forest of rich leaves, layout containers and stable interaction slots. Parent keys resolve earlier in this exact graph.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "oneOf": [
      {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "format": {
            "type": "string",
            "enum": [
              "sanitized_html",
              "text",
              "asset",
              "math"
            ]
          },
          "value": {
            "type": "string",
            "minLength": 1,
            "maxLength": 50000
          },
          "asset_version_id": {
            "type": "string",
            "format": "uuid"
          },
          "accessible_text": {
            "type": "string",
            "minLength": 1,
            "maxLength": 4000
          },
          "parent_key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          }
        },
        "required": [
          "key",
          "format",
          "value"
        ],
        "additionalProperties": false
      },
      {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "format": {
            "type": "string",
            "enum": [
              "interaction"
            ]
          },
          "interaction_key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "parent_key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          }
        },
        "required": [
          "key",
          "format",
          "interaction_key"
        ],
        "additionalProperties": false
      },
      {
        "type": "object",
        "properties": {
          "key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "format": {
            "type": "string",
            "enum": [
              "container"
            ]
          },
          "container_kind": {
            "type": "string",
            "enum": [
              "flow",
              "inline_flow",
              "paragraph",
              "ordered_list",
              "unordered_list",
              "list_item",
              "table",
              "table_caption",
              "table_head",
              "table_body",
              "table_foot",
              "table_row",
              "table_header",
              "table_cell"
            ]
          },
          "parent_key": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "table_semantics": {
            "type": "string",
            "enum": [
              "data",
              "layout"
            ]
          },
          "header_scope": {
            "type": "string",
            "enum": [
              "row",
              "col",
              "rowgroup",
              "colgroup"
            ]
          },
          "header_keys": {
            "type": "array",
            "items": {
              "type": "string",
              "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
            },
            "maxItems": 32,
            "minItems": 0
          },
          "row_span": {
            "type": "integer",
            "minimum": 1,
            "maximum": 32
          },
          "column_span": {
            "type": "integer",
            "minimum": 1,
            "maximum": 32
          },
          "list_start": {
            "type": "integer",
            "minimum": 1,
            "maximum": 10000
          }
        },
        "required": [
          "key",
          "format",
          "container_kind"
        ],
        "additionalProperties": false
      }
    ]
  },
  "maxItems": 2048,
  "minItems": 1
}
```

### asset_version_ids

Approved immutable assets belonging to the institution and permitted bank.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Approved immutable assets belonging to the institution and permitted bank.

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

### tags

Non-sensitive taxonomy and search tags.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 128
  },
  "minItems": 0,
  "maxItems": 128
}
```

### content_digest

Digest over the complete versioned graph.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### created_by

Author or drafting service with bank grant.

Required. Null is rejected.

References [Principal](Principal.md). Author or drafting service with bank grant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_by

Independent authorized releasing principal.

Optional. Nullable.

References [Principal](Principal.md). Independent authorized releasing principal.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_at

Effective published time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### outcome_reference_ids

Scoped institution-owned outcome references approved through curriculum.

Optional. Null is rejected.

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

### license_reference

Applicable content rights and reuse license identifier.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

## Integrity

- One editable draft per item by default.
- Approval binds exact content digest.
- Published content graph cannot change.
- At most 64 interactions, 128 criteria and 2,048 prompt nodes at depth 16, with a 256 KiB cumulative normalized public content budget per item.
- When prompt slots are used, every interaction has one exact slot. Container ancestry and preorder must be valid. Rich content leaves cannot contain executable control placeholders.

## Unique keys

- `id`
- `item_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_id, state, revision | Select newest eligible authored versions. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | in_review | SubmitItemForReview | Blocking publication issues resolved. Freeze requested digest and submit reviewer task. |
| in_review | approved | ReviewItemVersion | Reviewer approves exact frozen graph. Record an immutable review decision. |
| in_review | draft | ReviewItemVersion | Reviewer requests changes or rejects draft. Record decision and resume editing. |
| approved | published | PublishItemVersion | Approval digest and dependencies match. Advance current publication pointer. |
| published | withdrawn | WithdrawItemVersion | Publisher supplies scope-valid reason. Block newly selected use. |
