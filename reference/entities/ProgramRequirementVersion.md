# ProgramRequirementVersion

Immutable academic requirements for a programme entry or approved transfer.

Owned by **records**.

## Fields

### id

Stable globally unique ProgramRequirementVersion identifier.

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

### program_id

Programme within institution.

Required. Null is rejected.

References [Program](Program.md). Programme within institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_scheme_id

Published unit scheme for awards in this version.

Required. Null is rejected.

References [CreditUnitSchemeVersion](CreditUnitSchemeVersion.md). Published unit scheme for awards in this version.

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

Academic requirement publication.

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

### name

Version label for academic planners.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 180
}
```

### effective_from

Inclusive academic calendar date.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date"
}
```

### effective_to

Exclusive academic cutoff if any.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date"
}
```

### minimum_total_credits

Required distinct credit sum.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$",
  "default": "0"
}
```

### minimum_resident_credits

Required institutional residency credits.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$",
  "default": "0"
}
```

### maximum_transfer_credits

Maximum accepted transfer units for completion, null if uncapped.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### minimum_gpa

Optional exact GPA requirement.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### gpa_repeat_basis

GPA repeat treatment.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "all",
    "latest",
    "highest"
  ],
  "default": "all"
}
```

### credit_repeat_basis

One awarded course credit selection.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "earliest_pass",
    "latest_pass",
    "highest_pass"
  ],
  "default": "earliest_pass"
}
```

### qualification_valid_days

Credential qualification lifetime or null for no expiry.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 36500
}
```

### renewal_opens_days

Calendar-day renewal opening before expiry.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 36500,
  "default": 0
}
```

### publication_digest

Canonical requirement graph digest.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

## Integrity

- Minimum residency cannot exceed minimum total where total positive.
- Requirements acyclic, typed and bounded before publication.
- Version changes never alter prior audit.

## Unique keys

- `id`
- `program_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| program_id, state, effective_from, effective_to | Resolve permitted admission and renewal versions. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishProgramRequirements | Graph and eligibility policy validated Freeze approved version. |
