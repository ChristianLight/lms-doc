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

Ordered rich content blocks with sanitized renderer format.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
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
      }
    },
    "required": [
      "key",
      "format",
      "value"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 256
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
