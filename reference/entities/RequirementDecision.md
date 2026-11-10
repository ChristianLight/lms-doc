# RequirementDecision

Authorized waiver or substitution scoped to exact programme requirement.

Owned by **records**.

## Fields

### id

Stable globally unique RequirementDecision identifier.

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

### person_id

Educational identity within the same institution.

Required. Null is rejected.

References [Person](Person.md). Educational identity within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### program_enrollment_id

Learner programme context.

Required. Null is rejected.

References [ProgramEnrollment](ProgramEnrollment.md). Learner programme context.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requirement_id

Rule within assigned requirement version.

Required. Null is rejected.

References [ProgramRequirement](ProgramRequirement.md). Rule within assigned requirement version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_decision_id

Approved substitution source if relevant.

Required. Nullable.

References [CreditDecision](CreditDecision.md). Approved substitution source if relevant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### recognition_decision_id

Approved external support if relevant.

Required. Nullable.

References [RecognitionDecision](RecognitionDecision.md). Approved external support if relevant.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Earlier requirement decision if corrected.

Required. Nullable.

References [RequirementDecision](RequirementDecision.md). Earlier requirement decision if corrected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision_kind

Approved rule-level action.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "waiver",
    "substitution",
    "withdrawal"
  ]
}
```

### reason

Restricted and reviewable justification.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### effective_from

Inclusive decision boundary.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive expiration when any.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
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

- Waiver is not itself credit.
- Substitution names eligible source evidence.
- Revocation preserves earlier decision.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| program_enrollment_id, requirement_id, effective_from | Find eligible exceptions for audit. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
