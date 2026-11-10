# GradePeriodClose

Gradebook closure guard for one offering and academic period.

Owned by **records**.

## Fields

### id

Stable globally unique GradePeriodClose identifier.

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

Exact gradebook reporting period within institution.

Required. Null is rejected.

References [AcademicPeriod](AcademicPeriod.md). Exact gradebook reporting period within institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Close lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "closing",
    "closed",
    "correction_open",
    "resealed"
  ],
  "default": "open"
}
```

### guard_version

Monotonic optimistic concurrency version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### checkpoint_digest

Approved grade evidence and expected learner checkpoint.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### closed_by

Approver with close permission.

Required. Nullable.

References [Principal](Principal.md). Approver with close permission.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### closed_at

Closure instant.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### resealed_at

Most recent reseal instant.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Close requires all expected final dispositions and acknowledged dependencies.
- Source evidence arriving after closure becomes correction input only.

## Unique keys

- `id`
- `offering_id, academic_period_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, academic_period_id | Find blocked periods and registrar work queue. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| open | closing | BeginGradePeriodClosure | Registrar authorizes close preparation Capture roster and evidence reconciliation boundary. |
| closing | closed | CloseGradePeriod | All final results or approved dispositions exist Seal ordinary release writes. |
| closed | correction_open | OpenGradeCorrectionWindow | Approved scoped correction targets Open only named targets. |
| resealed | correction_open | OpenGradeCorrectionWindow | A separate correction is approved after reseal Open new named targets under fresh scope guard. |
| correction_open | resealed | ResealGradePeriod | Window outputs reviewed Seal correction mutations. |
