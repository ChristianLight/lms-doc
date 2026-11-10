# GradeResult

Stable result target identity for one learner enrollment.

Owned by **records**.

## Fields

### id

Stable globally unique GradeResult identifier.

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

### enrollment_id

Enrollment in the named offering and institution.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Enrollment in the named offering and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_kind

Scope of result.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "item",
    "category",
    "period",
    "course"
  ]
}
```

### grade_item_id

Required item target in same offering, otherwise null.

Required. Nullable.

References [GradeItem](GradeItem.md). Required item target in same offering, otherwise null.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### category_key

Stable category key when target is a grade category.

Required. Nullable.

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

### target_key

Canonical nonnull kind and target key used for uniqueness.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 170
}
```

### current_revision_id

Latest official-purpose computed or override revision under scope guard.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). Latest official-purpose computed or override revision under scope guard.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### current_preview_revision_id

Latest staff-current projection revision, independent of final computed pointer.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). Latest staff-current projection revision, independent of final computed pointer.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pointer_version

Optimistic official-purpose pointer version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### preview_pointer_version

Independent staff-current preview pointer version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
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

- Target key canonicalizes nullable components.
- Result pointer is not a publication pointer. Staff preview pointer never supersedes final or correction pointer.

## Unique keys

- `id`
- `enrollment_id, target_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, academic_period_id, target_kind | Find staff reporting and period closure targets. |
| enrollment_id, target_kind, target_key | Read learner result targets in scope. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
