# LearningRuleVersion

Immutable availability and completion policy for a placement or outline.

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

### institution_id

Rule owner.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_id

Course scope for placement resolution.

Required. Null is rejected.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_key

Stable policy identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic policy version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### gate

Validated bounded typed gate expression.

Required. Nullable.

```json
{
  "type": "object",
  "maxProperties": 12
}
```

### completion

Validated completion criterion and evidence set.

Required. Nullable.

```json
{
  "type": "object",
  "maxProperties": 12
}
```

### show_locked

Disclosure preference.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### continuity

Gate continuity rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "live",
    "sticky_after_start"
  ],
  "default": "live"
}
```

### digest

Canonical policy SHA-256.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- Gate AST depth at most 12 and at most 100 nodes.
- Exact references and safety checks remain mandatory.

## Unique keys

- `id`
- `course_id, rule_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_id, rule_key | Find pinned rule versions. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
