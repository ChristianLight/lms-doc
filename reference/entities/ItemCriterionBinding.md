# ItemCriterionBinding

Maps item responses to a versioned scoring criterion.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemCriterionBinding identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Item version owning this criterion.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Item version owning this criterion.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Stable scoring key within item version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### marking_rule_version_id

Same-institution approved rule for automated judging.

Optional. Nullable.

References [MarkingRuleVersion](MarkingRuleVersion.md). Same-institution approved rule for automated judging.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_criterion_id

Same-institution criterion used for human judgment.

Optional. Nullable.

References [RubricCriterion](RubricCriterion.md). Same-institution criterion used for human judgment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### interaction_keys

Declared local response inputs for this criterion.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### dependency_keys

Other criterion keys required before evaluating this binding.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### maximum

Criterion bound within item scoring scale.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### blank_disposition

Approved zero, review or explicit excused rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### invalid_disposition

Configured response policy for a captured invalid value.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

## Integrity

- Exactly one evaluation source selected.
- Inputs and dependencies resolve in the same ItemVersion.
- No criterion cycle.
- Baseline requires all human criteria in one item version to use the same rubric revision.

## Unique keys

- `id`
- `item_version_id, key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, key | Evaluation graph lookup. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
