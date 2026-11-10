# MarkingRuleVersion

Protected typed grading rule and evaluator release identity.

Owned by **assessment**.

## Fields

### id

Stable globally unique MarkingRuleVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution that may use the rule.

Required. Null is rejected.

References [Institution](Institution.md). Institution that may use the rule.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_key

Stable key for rule revision series.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### revision

Monotonic rule revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### evaluator_release_id

Approved registered compatible evaluator.

Required. Null is rejected.

References [EvaluatorRelease](EvaluatorRelease.md). Approved registered compatible evaluator.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parameters

Validated expected values and private scorer settings.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "kind": {
        "type": "string",
        "enum": [
          "number",
          "rational",
          "text",
          "identifier",
          "boolean",
          "structured"
        ]
      },
      "value": {
        "type": "string",
        "minLength": 1,
        "maxLength": 16000
      }
    },
    "required": [
      "name",
      "kind",
      "value"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 128
}
```

### minimum

Lowest possible criterion score.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### maximum

Highest possible criterion score.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### fixture_digest

Verified frozen tests and outcomes.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### digest

Protected rule content digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### approved_by

Authorized rule approver.

Required. Null is rejected.

References [Principal](Principal.md). Authorized rule approver.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Effective approval time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Minimum does not exceed maximum.
- Inputs are bounded typed values and never raw executable code.

## Unique keys

- `id`
- `institution_id, rule_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, rule_key, revision | Protected lookup and regrade compatibility. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
