# CourseOffering

Delivery instance of one stable course in one academic period.

Owned by **participation**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_unit_id

Delegated owning unit.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Must resolve to an authorized OrganizationUnit in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_id

Logical course.

Required. Null is rejected.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### academic_period_id

Reporting period.

Required. Null is rejected.

References [AcademicPeriod](AcademicPeriod.md). Must resolve to an authorized AcademicPeriod in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### default_course_version_id

Default for future enrollments.

Required. Null is rejected.

References [CourseVersion](CourseVersion.md). Published version must belong to this offering course.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Display offering code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### normalized_code

Case-folded uniqueness key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Delivery display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### mode

Delivery mode.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "self_paced",
    "teacher_led",
    "blended"
  ],
  "default": "teacher_led"
}
```

### timezone

IANA time zone identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### capacity

Null is unbounded offering capacity.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000000
}
```

### state

Offering lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "scheduled",
    "active",
    "closed",
    "archived",
    "cancelled"
  ],
  "default": "draft"
}
```

### revision

Compare-and-swap token.

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

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### activated_at

Actual activation instant.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Default release changes affect future admissions only.
- Current calendar and admission policy required to activate.

## Unique keys

- `id`
- `institution_id, academic_period_id, normalized_code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_unit_id, academic_period_id, state | Scoped administration filter. |
| course_id, state | Course delivery use and activation checks. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | scheduled | TransitionOffering | Valid published curriculum and calendar. Expose eligible scheduled offering. |
| scheduled | active | TransitionOffering | Active date, staffing and calendar valid. Enable approved admissions and delivery. |
| active | closed | TransitionOffering | Attempt impact reviewed. Block new starts and preserve authorized review. |
| closed | archived | TransitionOffering | Ordinary participation ended. Retain scoped academic history. |
| draft | cancelled | TransitionOffering | Recorded authorized reason. Disable delivery and admissions. |
| scheduled | cancelled | TransitionOffering | Affected roster reviewed. Revoke new starts and notify affected audience. |
