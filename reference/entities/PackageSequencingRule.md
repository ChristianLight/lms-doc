# PackageSequencingRule

Edition-specific typed control or rule with a verified manifest locator.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_id

Activity or cluster owning the rule.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### phase

Sequencing evaluation phase.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "control",
    "pre",
    "exit",
    "post",
    "rollup",
    "objective",
    "selection",
    "randomization",
    "presentation"
  ]
}
```

### ordinal

Stable evaluation order within its phase.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000
}
```

### action

Approved action token in edition's vocabulary.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

### conditions

Typed ordered conditions interpreted by phase.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "operator": {
        "type": "string",
        "minLength": 1,
        "maxLength": 32
      },
      "operand": {
        "type": "string",
        "minLength": 1,
        "maxLength": 128
      },
      "threshold": {
        "type": "string",
        "minLength": 0,
        "maxLength": 128
      }
    },
    "required": [
      "operator",
      "operand"
    ],
    "additionalProperties": false
  },
  "maxItems": 128,
  "minItems": 0,
  "uniqueItems": false
}
```

### combination

How rule conditions combine.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "all",
    "any",
    "none"
  ]
}
```

### source_locator

Exact XML node location for diagnostics.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

## Integrity

- Unknown mandatory rule types cannot be silently interpreted.
- Raw source retains edition schema context.

## Unique keys

- `id`
- `activity_id, phase, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| activity_id, phase | Read the edition rule set for traversal and rollup. |

## Retention

Retain with package and sequencing profile.
