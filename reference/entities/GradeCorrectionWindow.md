# GradeCorrectionWindow

Time-bounded approval to correct selected closed-period results.

Owned by **records**.

## Fields

### id

Stable globally unique GradeCorrectionWindow identifier.

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

### period_close_id

Closed period in same offering.

Required. Null is rejected.

References [GradePeriodClose](GradePeriodClose.md). Closed period in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_result_ids

Named targets eligible for correction.

Required. Null is rejected.

References [GradeResult](GradeResult.md). Named targets eligible for correction.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 10000,
  "minItems": 1,
  "uniqueItems": true
}
```

### state

Correction access state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "expired",
    "closed"
  ],
  "default": "active"
}
```

### reason

Why ordinary closure exception was approved.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
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

### opens_at

Inclusive start timestamp.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive authorized end.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### sealed_at

Recorded reseal instant if completed.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- An expired window cannot activate a correction.
- Cannot expand scope without new authorization.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| period_close_id, state, expires_at | Find active correction boundary and expire stale work. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
