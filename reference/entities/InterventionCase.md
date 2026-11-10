# InterventionCase

Scoped learner support work item derived from explained source facts.

Owned by **records**.

## Fields

### id

Stable globally unique InterventionCase identifier.

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

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Enrollment in the named offering and institution.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment in the named offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Exact enabled support rule.

Required. Null is rejected.

References [InterventionRuleVersion](InterventionRuleVersion.md). Exact enabled support rule.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### trigger_window_key

Canonical window key for idempotent case trigger.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### cutoff_at

Time boundary at which source data was evaluated.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### evidence_digest

Authorized minimal source signal lineage digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### reason_codes

Safe decision explanation codes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[a-z][a-z0-9._-]{0,63}$"
  },
  "maxItems": 20,
  "minItems": 1,
  "uniqueItems": true
}
```

### state

Support case workflow.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "assigned",
    "waiting",
    "resolved",
    "dismissed"
  ],
  "default": "open"
}
```

### assigned_to

Scoped active instructor or adviser when assigned.

Required. Nullable.

References [Principal](Principal.md). Scoped active instructor or adviser when assigned.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pointer_version

Case compare-and-swap token version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
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

## Integrity

- Support case cannot modify grades or access eligibility.
- Corrected source signal can close case with history.

## Unique keys

- `id`
- `enrollment_id, rule_version_id, trigger_window_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, assigned_to | Find scoped staff review queue. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.
