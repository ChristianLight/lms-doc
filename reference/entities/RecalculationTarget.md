# RecalculationTarget

One independently retryable revision comparison within a run.

Owned by **records**.

## Fields

### id

Stable globally unique RecalculationTarget identifier.

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

### run_id

Owning run in same offering.

Required. Null is rejected.

References [RecalculationRun](RecalculationRun.md). Owning run in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_result_id

Stable recalculation target.

Required. Null is rejected.

References [GradeResult](GradeResult.md). Stable recalculation target.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### base_revision_id

Prior scoped revision used to compare, if any.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). Prior scoped revision used to compare, if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### candidate_revision_id

New computed candidate if successful.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). New computed candidate if successful.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### input_fingerprint

Per-target frozen policy and evidence digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### state

Independent target processing status.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "leased",
    "ready",
    "failed",
    "stale",
    "applied"
  ],
  "default": "queued"
}
```

### lease_expires_at

Exclusive worker lease validity.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### error_code

Scoped recoverable computation error.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### difference_kind

Primary preview difference.

Required. Nullable.

```json
{
  "type": "string",
  "enum": [
    "unchanged",
    "score",
    "outcome",
    "eligibility",
    "multiple"
  ]
}
```

### revision_guard

Compare-and-swap target guard.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

## Integrity

- Lease expiry allows same logical target retry.
- Candidate cannot publish official grade without release.

## Unique keys

- `id`
- `run_id, grade_result_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| run_id, state, grade_result_id | Claim deterministic worker batches. |

## Retention

Retain according to institution audit retention and hold. Keep source pointers while a retained official output requires them.
