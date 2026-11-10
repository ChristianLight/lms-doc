# ProgramAuditRuleResult

Source-traceable outcome of one named programme requirement.

Owned by **records**.

## Fields

### id

Stable globally unique ProgramAuditRuleResult identifier.

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

### audit_id

Immutable exact programme audit.

Required. Null is rejected.

References [ProgramAuditResult](ProgramAuditResult.md). Immutable exact programme audit.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requirement_id

Rule in audited requirement version.

Required. Null is rejected.

References [ProgramRequirement](ProgramRequirement.md). Rule in audited requirement version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_decision_ids

Exact source award revisions counted by this rule.

Required. Null is rejected.

References [CreditDecision](CreditDecision.md). Exact source award revisions counted by this rule.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 1000,
  "minItems": 0,
  "uniqueItems": true
}
```

### competency_decision_ids

Approved mastery inputs for gate.

Required. Null is rejected.

References [CompetencyDecision](CompetencyDecision.md). Approved mastery inputs for gate.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 500,
  "minItems": 0,
  "uniqueItems": true
}
```

### requirement_decision_id

Explicit waiver or substitution used.

Required. Nullable.

References [RequirementDecision](RequirementDecision.md). Explicit waiver or substitution used.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### status

Rule-level outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "fulfilled",
    "shortfall",
    "waived",
    "blocked",
    "needs_review"
  ]
}
```

### used_credit

Exact credit used in rule, zero where not applicable.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### shortfall_credit

Remaining credits required, zero for other kinds.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### reason_code

Localized explanation code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

## Integrity

- Source and requirement scope must match owning audit.
- Waiver only satisfies named rule.

## Unique keys

- `id`
- `audit_id, requirement_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| audit_id, status | Read exact audit rule explanations. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
