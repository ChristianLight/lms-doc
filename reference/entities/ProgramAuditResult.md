# ProgramAuditResult

Immutable evaluation of a programme and exact input cutoffs.

Owned by **records**.

## Fields

### id

Stable globally unique ProgramAuditResult identifier.

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

Learner admission and requirements.

Required. Null is rejected.

References [ProgramEnrollment](ProgramEnrollment.md). Learner admission and requirements.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requirement_version_id

Exact pinned version evaluated.

Required. Null is rejected.

References [ProgramRequirementVersion](ProgramRequirementVersion.md). Exact pinned version evaluated.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### status

Outcome of typed requirements evaluation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "incomplete",
    "satisfied",
    "needs_review",
    "blocked"
  ]
}
```

### cutoff_at

Academic evaluation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### algorithm_version

Deterministic allocation implementation.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### fingerprint

Digest of policy, input cutoffs and evaluation.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### is_hypothetical

Planning only if true, never an issuance basis.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### total_credit

Distinct approved credits counted in result.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### resident_credit

Distinct institutional residency credits.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### transfer_credit

Distinct accepted transfer and recognized credit.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### search_states

Number of explored candidate allocation states.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100000
}
```

### gpa

Programme-scope exact GPA, when computable.

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

- Hypothetical audit cannot authorize qualification.
- Bound exhaustion cannot report satisfied.
- Total credits count distinct credit sources.

## Unique keys

- `id`
- `program_enrollment_id, fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| program_enrollment_id, cutoff_at, status | Find current audit and prior cutoffs. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
