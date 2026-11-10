# AcademicPeriod

Institutional academic interval such as year, semester, quarter, or term.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### parent_id

Enclosing period in the same institution, if any.

Optional. Nullable.

References [AcademicPeriod](AcademicPeriod.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Institution-wide stable catalog and reporting key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### name

Display label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 180
}
```

### kind

Scheduling taxonomy.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "academic_year",
    "semester",
    "trimester",
    "quarter",
    "term",
    "session",
    "custom"
  ]
}
```

### starts_on

Inclusive civil date in timezone.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date"
}
```

### ends_before

Exclusive civil date. Must follow starts_on.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date"
}
```

### timezone

IANA timezone used for civil date boundaries.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^(UTC|[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+)+)$"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "open",
    "closed",
    "archived"
  ]
}
```

## Integrity

- Child window is contained within parent. Overlapping sibling periods are allowed for concurrent tracks.
- Changing a period does not rewrite existing offering deadlines, published schedules, or report revision snapshots.
- Closed period may be reopened with evidence and dual approval when official reports exist.

## Unique keys

- `id`
- `institution_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, parent_id, starts_on | Traverse time hierarchy and list candidate offerings |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | open | SetAcademicPeriodState | Date containment and zone validation pass Allow new offering associations. |
| open | closed | SetAcademicPeriodState | Scheduled close is accepted or registrar records exceptions Block new offering associations and use correction workflow. |
| closed | open | SetAcademicPeriodState | Registrar and independent approver agree where official reports exist Publish updated period version. |
| closed | archived | SetAcademicPeriodState | No current operational dependency Retain history and restrict changes. |
