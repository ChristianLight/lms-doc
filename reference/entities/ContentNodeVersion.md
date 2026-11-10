# ContentNodeVersion

Sealed version of a typed content definition.

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

### content_node_id

Stable definition owner.

Required. Null is rejected.

References [ContentNode](ContentNode.md). Must resolve to an authorized ContentNode in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic content revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### payload

Canonical typed locale variants validated against matching registered schemas.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "type_key": {
      "type": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
    },
    "schema_version": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    },
    "default_locale": {
      "type": "string",
      "minLength": 2,
      "maxLength": 35,
      "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
    },
    "variants": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "locale": {
            "type": "string",
            "minLength": 2,
            "maxLength": 35,
            "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          },
          "body": {
            "type": "object",
            "maxProperties": 64
          },
          "review_state": {
            "type": "string",
            "enum": [
              "draft",
              "approved",
              "stale"
            ]
          },
          "source_digest": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$"
          }
        },
        "required": [
          "locale",
          "title",
          "body",
          "review_state"
        ],
        "additionalProperties": false
      },
      "maxItems": 60,
      "minItems": 1
    }
  },
  "required": [
    "type_key",
    "schema_version",
    "default_locale",
    "variants"
  ],
  "additionalProperties": false
}
```

### digest

Canonical version digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### created_by

Sealing author or agent.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Sealed instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Only sealed versions can be placed.
- Type, locale and asset references are resolved before publication.

## Unique keys

- `id`
- `content_node_id, revision`
- `content_node_id, digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| content_node_id, created_at | Revision history. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
