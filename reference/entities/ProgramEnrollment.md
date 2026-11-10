# ProgramEnrollment

Person admission and immutable programme requirement assignment.

Owned by **records**.

## Fields

### id

Stable globally unique ProgramEnrollment identifier.

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

### program_id

Approved institutional programme.

Required. Null is rejected.

References [Program](Program.md). Approved institutional programme.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requirement_version_id

Pinned version in exact programme.

Required. Null is rejected.

References [ProgramRequirementVersion](ProgramRequirementVersion.md). Pinned version in exact programme.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### entry_period_id

Institutional academic period of entry.

Required. Null is rejected.

References [AcademicPeriod](AcademicPeriod.md). Institutional academic period of entry.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### predecessor_id

Previous programme admission or renewal for same person.

Required. Nullable.

References [ProgramEnrollment](ProgramEnrollment.md). Previous programme admission or renewal for same person.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Programme participation state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "paused",
    "withdrawn",
    "completed",
    "superseded"
  ],
  "default": "active"
}
```

### admitted_at

Approved academic entry instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expected_end_at

Target completion if known.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### pointer_version

Lifecycle guard.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
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

- At most one active admission per person and programme by default unless explicit dual-award policy.
- Renewal references predecessor and creates new stable identity.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| program_id, state, entry_period_id | Find scoped programme cohorts and renewal cases. |
| person_id, program_id, admitted_at | Find admission and renewal history. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | completed | ApproveQualification | Satisfied audit and authorized approval Record programme completion with award decision. |
