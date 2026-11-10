# GradePolicyVersion

Offering-scoped immutable grade calculation and release policy.

Owned by **records**.

## Fields

### id

Stable globally unique GradePolicyVersion identifier.

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

### policy_key

Stable policy family within the offering.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
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

### state

Policy lifecycle.

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

### supersedes_id

Prior policy version within same offering.

Required. Nullable.

References [GradePolicyVersion](GradePolicyVersion.md). Prior policy version within same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scale_version_id

Published scale in the institution.

Required. Null is rejected.

References [GradeScaleVersion](GradeScaleVersion.md). Published scale in the institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### root_category_id

Exactly one root of this policy tree.

Required. Nullable.

References [GradeCategoryVersion](GradeCategoryVersion.md). Exactly one root of this policy tree.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### algorithm_version

Deployed reference calculation contract identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$",
  "default": "grade-calc-v1"
}
```

### attempt_selection

Default candidate selection across eligible attempts.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "latest",
    "first",
    "highest",
    "average",
    "manual_selection"
  ],
  "default": "latest"
}
```

### missing_final

Policy for confirmed missing at final cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "zero_confirmed",
    "incomplete_review"
  ],
  "default": "zero_confirmed"
}
```

### max_ratio

Offering result ceiling including authorized bonus.

Required. Null is rejected.

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

### auto_item_release

Permit low-stakes item release under explicit policy.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### require_second_final_reviewer

Require separate final release approver.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### allow_selective_final

Allow approved partial final release while retaining period closure blockers.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### structure_digest

Canonical versioned graph and policy digest.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### published_at

Publication instant.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Exactly one root category at publication.
- Every included item validates maximum, source mapping, and weight.
- Never mutate published calculation fields.

## Unique keys

- `id`
- `offering_id, policy_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, revision | Locate published current and historical policy versions. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishGradePolicy | Complete policy tree and adoption guard validated Seal graph digest and publish revision. |
