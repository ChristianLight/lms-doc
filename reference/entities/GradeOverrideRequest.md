# GradeOverrideRequest

Scoped proposal to override computed result or academic disposition.

Owned by **records**.

## Fields

### id

Stable globally unique GradeOverrideRequest identifier.

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

### grade_result_id

Affected grade result in same offering.

Required. Null is rejected.

References [GradeResult](GradeResult.md). Affected grade result in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### base_revision_id

Exact current computation anchoring the request.

Required. Null is rejected.

References [GradeResultRevision](GradeResultRevision.md). Exact current computation anchoring the request.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Approval lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "requested",
    "under_review",
    "approved",
    "rejected",
    "stale",
    "withdrawn"
  ],
  "default": "requested"
}
```

### override_kind

Requested exceptional interpretation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "numeric",
    "outcome",
    "incomplete",
    "withdrawal",
    "gate_exception"
  ]
}
```

### requested_ratio

Proposed exact ratio when numeric.

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

### requested_outcome

Proposed disposition or pass/fail when applicable.

Required. Nullable.

```json
{
  "type": "string",
  "enum": [
    "pass",
    "fail",
    "incomplete",
    "withdrawn",
    "exempt"
  ]
}
```

### reason

Restricted staff rationale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### learner_explanation

Approved learner-visible explanation.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2000
}
```

### effective_at

Proposed academic effective date.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Optional expiry allowed for provisional override.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### base_fingerprint

Material input fingerprint approved by requester.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
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

- Numeric and outcome fields follow override kind.
- Official approval needs distinct reviewer and unchanged inputs.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| grade_result_id, state, created_at | Find open override requests for target. |
| offering_id, state, created_at | Review queue by scope. |

## Retention

Retain according to institution audit retention and hold. Keep source pointers while a retained official output requires them.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | approved | DecideGradeOverride | Authorized independent approval and matching base Append effective decision and grade revision. |
| requested | rejected | DecideGradeOverride | Authorized reviewer rejects request Record reason and leave effective grade intact. |
| requested | stale | DecideGradeOverride | Material calculation changed Require a new reviewed request. |
