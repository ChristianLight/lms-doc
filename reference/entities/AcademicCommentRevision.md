# AcademicCommentRevision

Approved teacher report narrative separated from grade inputs.

Owned by **records**.

## Fields

### id

Stable globally unique AcademicCommentRevision identifier.

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

### academic_period_id

Academic period within institution.

Required. Null is rejected.

References [AcademicPeriod](AcademicPeriod.md). Academic period within institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Optional scoped offering.

Required. Nullable.

References [CourseOffering](CourseOffering.md). Optional scoped offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### report_card_id

Optional scoped report identity.

Required. Nullable.

References [ReportCard](ReportCard.md). Optional scoped report identity.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### comment_key

Stable comment series identifier.

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

### body

Plain-text comment or sanitized restricted-rich-text representation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 6000
}
```

### visibility

Approved maximum audience.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "learner",
    "approved_delegate",
    "staff_only"
  ]
}
```

### approved_at

Approval time, absent for draft.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approved_by

Approver in valid academic scope.

Required. Nullable.

References [Principal](Principal.md). Approver in valid academic scope.

```json
{
  "type": "string",
  "format": "uuid"
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

- Private comments are never embedded in learner artifacts.
- Report issuance pins exact approved revision.

## Unique keys

- `id`
- `comment_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, academic_period_id, offering_id | Collect approved comments by report scope. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.
