# CreditDecision

Versioned credit ledger line derived from final grade or recognition.

Owned by **records**.

## Fields

### id

Stable globally unique CreditDecision identifier.

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

### course_id

Institutional course identity when equivalent or native.

Required. Nullable.

References [Course](Course.md). Institutional course identity when equivalent or native.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Native enrollment for grade-based credit, if applicable.

Required. Nullable.

References [Enrollment](Enrollment.md). Native enrollment for grade-based credit, if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### release_entry_id

Official final grade source if native.

Required. Nullable.

References [GradeReleaseEntry](GradeReleaseEntry.md). Official final grade source if native.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### recognition_decision_id

Approved prior learning or transfer source if external.

Required. Nullable.

References [RecognitionDecision](RecognitionDecision.md). Approved prior learning or transfer source if external.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_scheme_id

Exact normalization unit version.

Required. Null is rejected.

References [CreditUnitSchemeVersion](CreditUnitSchemeVersion.md). Exact normalization unit version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Previous credit decision for same award source.

Required. Nullable.

References [CreditDecision](CreditDecision.md). Previous credit decision for same award source.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_key

Stable logical award stream.

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

### equivalence_key

Institution-approved repeat grouping if applicable.

Required. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_kind

Ledger source family.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "institutional",
    "transfer",
    "recognition"
  ]
}
```

### attempted_units

Normalized credits attempted.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### earned_units

Normalized credits earned.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### gpa_eligible

Allow inclusion in institutional GPA calculation.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### gpa_points

Exact points per credit when GPA eligible.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### academic_completed_at

Effective completion or recognition timestamp.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Effective credit disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "awarded",
    "not_awarded",
    "revoked"
  ]
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

## Integrity

- Exactly one approved source basis.
- GPA eligibility independent from earning credits.
- No duplicate award for same recognized source.

## Unique keys

- `id`
- `credit_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, academic_completed_at, state | Find effective award lineage at programme cutoff. |
| release_entry_id, state | Assess grade correction consequences. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
