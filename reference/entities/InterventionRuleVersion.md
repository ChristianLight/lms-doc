# InterventionRuleVersion

Published human-reviewed support trigger and routing rule.

Owned by **records**.

## Fields

### id

Stable globally unique InterventionRuleVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_key

Stable rule family.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### revision

Monotonic immutable revision number within its stable identity.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### title

Authorized reason label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### trigger_kind

Exact safe signal type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "confirmed_overdue",
    "eligible_inactivity",
    "below_released_threshold"
  ]
}
```

### lookback_days

Bounded observation window.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 180,
  "default": 14
}
```

### minimum_count

Minimum observed eligible signal count.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100,
  "default": 2
}
```

### threshold

Applicable released ratio threshold, if any.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### grace_days

Eligibility grace after active enrollment.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 90,
  "default": 7
}
```

### cooldown_days

Minimum delay before equivalent new case.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 180,
  "default": 14
}
```

### routing_role

Authorized assigned role that handles review.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### state

Rule publication lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "superseded",
    "retired"
  ],
  "default": "draft"
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Incomplete signal feed never creates a risk verdict.
- Human approval before learner notification default.

## Unique keys

- `id`
- `institution_id, rule_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, rule_key | Resolve active authorized trigger profile. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishInterventionRule | Scope, source and routing approved Enable exact policy version. |
