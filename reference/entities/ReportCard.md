# ReportCard

Stable learner and academic period report identity.

Owned by **records**.

## Fields

### id

Stable globally unique ReportCard identifier.

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

Term or report period in same institution.

Required. Null is rejected.

References [AcademicPeriod](AcademicPeriod.md). Term or report period in same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### report_kind

Institutional report purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "progress",
    "interim",
    "period_end"
  ]
}
```

### current_revision_id

Current issued revision if one exists.

Required. Nullable.

References [ReportCardRevision](ReportCardRevision.md). Current issued revision if one exists.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pointer_version

Optimistic current document pointer version.

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

- Current pointer only references issued same-card revision.
- Restaging does not remove issued revision.

## Unique keys

- `id`
- `person_id, academic_period_id, report_kind`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, academic_period_id, report_kind | Find report-card issuance population. |
| person_id, academic_period_id | Find scoped learner document series. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
