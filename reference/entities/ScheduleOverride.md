# ScheduleOverride

Effective scoped field changes for an offering and optional placement.

Owned by **participation**.

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

### offering_id

Schedule owner.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_key

Optional target placement key.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### audience

Exactly one authorized target scope.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "kind": {
      "type": "string",
      "enum": [
        "offering",
        "section",
        "learning_group",
        "enrollment"
      ]
    },
    "id": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": [
    "kind",
    "id"
  ],
  "additionalProperties": false
}
```

### rank

Ordering among co-applicable group overrides.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000,
  "default": 0
}
```

### fields

Unique field-level inherit, set or clear actions.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "field": {
        "type": "string",
        "enum": [
          "release",
          "recommended",
          "due",
          "grace_until",
          "close"
        ]
      },
      "action": {
        "type": "string",
        "enum": [
          "inherit",
          "set",
          "clear"
        ]
      },
      "rule": {
        "anyOf": [
          {
            "oneOf": [
              {
                "type": "object",
                "properties": {
                  "kind": {
                    "type": "string",
                    "enum": [
                      "absolute"
                    ]
                  },
                  "instant": {
                    "type": "string",
                    "format": "date-time"
                  }
                },
                "required": [
                  "kind",
                  "instant"
                ],
                "additionalProperties": false
              },
              {
                "type": "object",
                "properties": {
                  "kind": {
                    "type": "string",
                    "enum": [
                      "relative"
                    ]
                  },
                  "anchor": {
                    "type": "string",
                    "enum": [
                      "offering_open",
                      "enrollment_start"
                    ]
                  },
                  "unit": {
                    "type": "string",
                    "enum": [
                      "local_days",
                      "elapsed_minutes"
                    ]
                  },
                  "offset": {
                    "type": "integer",
                    "minimum": -525600,
                    "maximum": 525600
                  }
                },
                "required": [
                  "kind",
                  "anchor",
                  "unit",
                  "offset"
                ],
                "additionalProperties": false
              }
            ]
          },
          {
            "type": "null"
          }
        ]
      }
    },
    "required": [
      "field",
      "action"
    ],
    "additionalProperties": false
  },
  "maxItems": 5,
  "minItems": 1
}
```

### revision

Monotonic same-scope revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### effective_from

Inclusive start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approved_by

Accountable authorized actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason_code

Approved decision type.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

## Integrity

- Overlap cannot yield incompatible equal-rank group values.
- Clear cannot remove hard policy bounds.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, placement_key, effective_from, effective_to | Load applicable schedule overlay. |
| offering_id, rank | Detect co-applicable tie. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
