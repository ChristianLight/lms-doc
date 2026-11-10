# InteractionDefinition

Versioned candidate renderer and expected response shape.

Owned by **assessment**.

## Fields

### id

Stable globally unique InteractionDefinition identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Parent authored item version.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Parent authored item version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Stable local response identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### family

Registered interaction family discriminator.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "single_choice",
    "multiple_choice",
    "short_text",
    "long_text",
    "matching",
    "ordering",
    "categorization",
    "math",
    "quantity",
    "files",
    "points"
  ]
}
```

### schema_revision

Pinned renderer and accepted response schema version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### display_order

Positive distinct order within item.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### label

Programmatic and visible response label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### config

Typed family-specific bounds, controls and options.

Required. Null is rejected.

```json
{
  "oneOf": [
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "single_choice"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "layout": {
          "type": "string",
          "enum": [
            "list",
            "select"
          ]
        },
        "clear_allowed": {
          "type": "boolean"
        }
      },
      "required": [
        "kind",
        "required",
        "options"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "multiple_choice"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "minimum": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        },
        "maximum": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "layout": {
          "type": "string",
          "enum": [
            "list",
            "select"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "options",
        "minimum",
        "maximum"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "short_text"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "character_limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 512
        },
        "multiline": {
          "type": "boolean"
        }
      },
      "required": [
        "kind",
        "required",
        "character_limit"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "long_text"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "character_limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 50000
        },
        "word_minimum": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10000
        },
        "word_maximum": {
          "type": "integer",
          "minimum": 0,
          "maximum": 10000
        },
        "format": {
          "type": "string",
          "enum": [
            "text"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "character_limit",
        "format"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "matching"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "left_options": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "right_options": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "left_capacity": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "right_capacity": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "minimum_pairs": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        },
        "maximum_pairs": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "keyboard_mode": {
          "type": "string",
          "enum": [
            "pair_selectors"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "left_options",
        "right_options",
        "left_capacity",
        "right_capacity",
        "minimum_pairs",
        "maximum_pairs",
        "keyboard_mode"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "ordering"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "options": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "ordering_mode": {
          "type": "string",
          "enum": [
            "all",
            "partial"
          ]
        },
        "minimum": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        },
        "keyboard_mode": {
          "type": "string",
          "enum": [
            "ordered_list_controls"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "options",
        "ordering_mode",
        "minimum",
        "keyboard_mode"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "categorization"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "categories": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "key": {
                "type": "string",
                "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
              },
              "label": {
                "type": "string",
                "minLength": 1,
                "maxLength": 1000
              },
              "fixed_position": {
                "type": "integer",
                "minimum": 0,
                "maximum": 100
              }
            },
            "required": [
              "key",
              "label"
            ],
            "additionalProperties": false
          },
          "minItems": 1,
          "maxItems": 100
        },
        "item_capacity": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "category_capacity": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "keyboard_mode": {
          "type": "string",
          "enum": [
            "category_selectors"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "items",
        "categories",
        "item_capacity",
        "category_capacity",
        "keyboard_mode"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "math"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "input_profile": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
        },
        "syntax_help": {
          "type": "string",
          "minLength": 1,
          "maxLength": 2000
        },
        "character_limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 2048
        },
        "notation": {
          "type": "string",
          "enum": [
            "expression",
            "equation",
            "finite_set",
            "interval",
            "vector",
            "matrix",
            "working_steps"
          ]
        },
        "allowed_symbols": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
          },
          "minItems": 0,
          "maxItems": 64
        }
      },
      "required": [
        "kind",
        "required",
        "input_profile",
        "syntax_help",
        "character_limit",
        "notation",
        "allowed_symbols"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "quantity"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "input_profile": {
          "type": "string",
          "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
        },
        "unit_mode": {
          "type": "string",
          "enum": [
            "required",
            "optional",
            "forbidden"
          ]
        },
        "allowed_units": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
          },
          "minItems": 0,
          "maxItems": 64
        },
        "notation_help": {
          "type": "string",
          "minLength": 1,
          "maxLength": 1000
        }
      },
      "required": [
        "kind",
        "required",
        "input_profile",
        "unit_mode",
        "allowed_units",
        "notation_help"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "files"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "asset_limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 10
        },
        "byte_limit": {
          "type": "integer",
          "minimum": 1,
          "maximum": 209715200
        },
        "allowed_media_types": {
          "type": "array",
          "items": {
            "type": "string",
            "minLength": 3,
            "maxLength": 120,
            "pattern": "^[a-z0-9.+-]+/[a-z0-9.+-]+$"
          },
          "minItems": 1,
          "maxItems": 32
        },
        "required_declaration": {
          "type": "boolean"
        }
      },
      "required": [
        "kind",
        "required",
        "asset_limit",
        "byte_limit",
        "allowed_media_types"
      ],
      "additionalProperties": false
    },
    {
      "type": "object",
      "properties": {
        "kind": {
          "type": "string",
          "enum": [
            "points"
          ]
        },
        "required": {
          "type": "boolean"
        },
        "coordinate_system": {
          "type": "string",
          "enum": [
            "cartesian",
            "polar"
          ]
        },
        "axis_bounds": {
          "type": "object",
          "properties": {
            "x_min": {
              "type": "string",
              "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
            },
            "x_max": {
              "type": "string",
              "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
            },
            "y_min": {
              "type": "string",
              "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
            },
            "y_max": {
              "type": "string",
              "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
            }
          },
          "required": [
            "x_min",
            "x_max",
            "y_min",
            "y_max"
          ],
          "additionalProperties": false
        },
        "minimum_points": {
          "type": "integer",
          "minimum": 0,
          "maximum": 100
        },
        "maximum_points": {
          "type": "integer",
          "minimum": 1,
          "maximum": 100
        },
        "keyboard_mode": {
          "type": "string",
          "enum": [
            "coordinate_table"
          ]
        }
      },
      "required": [
        "kind",
        "required",
        "coordinate_system",
        "axis_bounds",
        "minimum_points",
        "maximum_points",
        "keyboard_mode"
      ],
      "additionalProperties": false
    }
  ]
}
```

### stimulus_version_id

Optional approved shared stimulus from the same institution.

Optional. Nullable.

References [ItemStimulusVersion](ItemStimulusVersion.md). Optional approved shared stimulus from the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Keys never encode correctness.
- Family-specific schema and cardinality are validated at publication and save.

## Unique keys

- `id`
- `item_version_id, key`
- `item_version_id, display_order`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, display_order | Build the scoped candidate response form. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
