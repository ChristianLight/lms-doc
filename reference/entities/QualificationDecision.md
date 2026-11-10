# QualificationDecision

Approved institutional award, correction or revocation from a programme audit.

Owned by **records**.

## Fields

### id

Stable globally unique QualificationDecision identifier.

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

Programme participation of same person.

Required. Null is rejected.

References [ProgramEnrollment](ProgramEnrollment.md). Programme participation of same person.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### program_audit_id

Exact approved non-hypothetical audit.

Required. Null is rejected.

References [ProgramAuditResult](ProgramAuditResult.md). Exact approved non-hypothetical audit.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Corrected decision for same award lineage if any.

Required. Nullable.

References [QualificationDecision](QualificationDecision.md). Corrected decision for same award lineage if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### renewal_of_id

Prior qualification linked for renewal.

Required. Nullable.

References [QualificationDecision](QualificationDecision.md). Prior qualification linked for renewal.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### status

Institutional decision type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "awarded",
    "suspended",
    "revoked",
    "superseded"
  ]
}
```

### award_code

Authorized institutional qualification code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### effective_at

Official academic award effective time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive expiry if policy sets one.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason

Approved rationale or correction record.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
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

- Award requires satisfied approved programme audit.
- Renewal uses distinct enrolment or approved programme renewal state.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, effective_at, status | Find permitted institution award history. |
| program_enrollment_id, status, effective_at | Resolve award basis and qualification renewal. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
