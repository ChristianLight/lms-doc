# ItemTranslation

Candidate-facing locale overlay for one item version.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemTranslation identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Item version in the same bank and revision.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Item version in the same bank and revision.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### locale

Distinct requested localization.

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

### interaction_keys

Canonical key coverage in actual displayed order.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
  },
  "minItems": 0,
  "maxItems": 64
}
```

### option_keys

Versioned ordered keys grouped by interaction, where local option keys retain their original meaning.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "interaction_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "keys": {
        "type": "array",
        "items": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
        },
        "minItems": 0,
        "maxItems": 100
      }
    },
    "required": [
      "interaction_key",
      "keys"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 64
}
```

### reviewed_by

Reviewer with bank and locale capability.

Optional. Nullable.

References [Principal](Principal.md). Reviewer with bank and locale capability.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Independent language approval time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### labels

Localized candidate labels, descriptions, control context and choice bodies by stable interaction and option keys.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "interaction_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "label": {
        "type": "string",
        "minLength": 1,
        "maxLength": 200
      },
      "accessible_description": {
        "type": "string",
        "minLength": 1,
        "maxLength": 4000
      },
      "leading_content": {
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
        "maxItems": 8,
        "minItems": 1
      },
      "trailing_content": {
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
        "maxItems": 8,
        "minItems": 1
      },
      "option_labels": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "option_key": {
              "type": "string",
              "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
            },
            "label": {
              "type": "string",
              "minLength": 1,
              "maxLength": 1000
            },
            "display_content": {
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
              "maxItems": 16,
              "minItems": 1
            }
          },
          "required": [
            "option_key",
            "label"
          ],
          "additionalProperties": false
        },
        "maxItems": 100,
        "minItems": 0
      }
    },
    "required": [
      "interaction_key",
      "label"
    ],
    "additionalProperties": false
  },
  "maxItems": 64,
  "minItems": 0
}
```

## Integrity

- Every canonical interaction and option key appears exactly once within its proper interaction.
- Translation does not alter expected values.
- Optional labels contain at most one localized label or rich choice body per exact stable source key. Missing overlay fields use the approved canonical localization fallback.

## Unique keys

- `id`
- `item_version_id, locale`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, locale | Resolve approved locale fallback. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
