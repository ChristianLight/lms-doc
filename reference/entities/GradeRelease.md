# GradeRelease

Immutable staged set and active visibility guard for official grade publication.

Owned by **records**.

## Fields

### id

Stable globally unique GradeRelease identifier.

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

### academic_period_id

Grading and reporting period within same institution.

Required. Nullable.

References [AcademicPeriod](AcademicPeriod.md). Grading and reporting period within same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### purpose

Publication class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "learner_feedback",
    "interim",
    "final",
    "correction"
  ]
}
```

### state

Staged, active and superseded visibility state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "approved",
    "active",
    "superseded",
    "revoked",
    "stale"
  ],
  "default": "staged"
}
```

### cutoff_at

Approved academic evidence cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### manifest_digest

Exact sorted result and audience manifest digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### ready_count

Number of valid entries staged.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100000
}
```

### blocked_count

Blocked scoped results.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100000
}
```

### allow_partial

Selective eligible final release permitted for this staged set.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### scope_version

Compare-and-swap scope guard version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### prepared_by

Authorized preparer in offering scope.

Required. Null is rejected.

References [Principal](Principal.md). Authorized preparer in offering scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_by

Authorized release reviewer in offering scope.

Required. Nullable.

References [Principal](Principal.md). Authorized release reviewer in offering scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Approval timestamp, absent before approval.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### activated_at

Actual learner visibility activation time.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
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

- Manifest digest and entries freeze at staging completion.
- No entry becomes visible before parent activation.
- Activation checks current evidence and all scope guards.

## Unique keys

- `id`
- `offering_id, purpose, manifest_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, academic_period_id, state, purpose | Find active and staged releases for scope. |
| offering_id, activated_at | Find releases for outbound and audit review. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | active | ActivateGradeRelease | Reviewed digest and inputs still match Atomically activate eligible entries and write outbox. |
| active | revoked | WithdrawGradeRelease | Authorized correction or exposure action Remove active recipient visibility and audit. |
