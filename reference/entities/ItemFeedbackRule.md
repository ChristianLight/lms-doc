# ItemFeedbackRule

Protected versioned hint, targeted feedback or model solution bound to an exact item version.

Owned by **assessment**.

## Fields

### id

Immutable rule UUID within the institution.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Owning exact ItemVersion. Require same bank, version and protected authoring scope.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Owning exact ItemVersion. Require same bank, version and protected authoring scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Stable local rule key within the item version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### ordinal

Stable authored evaluation and disclosure sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 256
}
```

### trigger

Approved disclosure trigger family, separate from delivery visibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "on_demand",
    "criterion_outcome",
    "choice_selected",
    "choice_set",
    "text_match",
    "alternate_accepted",
    "model_solution"
  ]
}
```

### interaction_key

Optional exact response control in the owning item version.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### criterion_key

Optional exact criterion binding key in the owning item version.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### predicate

Private typed trigger operands interpreted under the pinned match profile.

Optional. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "outcome": {
      "type": "string",
      "enum": [
        "correct",
        "partial",
        "incorrect"
      ]
    },
    "choice_keys": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "maxItems": 100,
      "minItems": 0
    },
    "matcher_profile": {
      "type": "string",
      "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
    },
    "match_value": {
      "type": "string",
      "minLength": 1,
      "maxLength": 2048
    },
    "alternate_key": {
      "type": "string",
      "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
    }
  },
  "required": [],
  "additionalProperties": false
}
```

### content

Protected sanitized rich body with immutable asset references.

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
      },
      "asset_version_id": {
        "type": "string",
        "format": "uuid"
      },
      "accessible_text": {
        "type": "string",
        "minLength": 1,
        "maxLength": 4000
      }
    },
    "required": [
      "key",
      "format",
      "value"
    ],
    "additionalProperties": false
  },
  "maxItems": 64,
  "minItems": 1
}
```

## Integrity

- On-demand and solution rules have no answer predicate. Targeted rules require exactly the operands for their trigger.
- Interaction, criterion and choice keys resolve in the same version. Matcher profile must be bounded and approved.
- Content, predicates and source answer identities stay out of candidate form, disclosure metadata and public grade projections until individually authorized.
- Published rule is immutable. A replacement creates another ItemVersion.

## Unique keys

- `id`
- `item_version_id, key`
- `item_version_id, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, trigger, ordinal | Resolve ordered authorized candidate help or review rules for exact pinned item. |

## Retention

Retain with the owning item version and all attempts, disclosures and holds that cite it.
