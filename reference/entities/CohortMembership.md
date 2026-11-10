# CohortMembership

Effective-dated institution person membership.

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

### person_id

Institutional learner identity.

Required. Null is rejected.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### cohort_id

Cohort in same institution.

Required. Null is rejected.

References [Cohort](Cohort.md). Must resolve to an authorized Cohort in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effective_from

Inclusive start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### source

Provenance.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "manual",
    "self",
    "invitation",
    "cohort",
    "roster",
    "rule",
    "transfer"
  ]
}
```

### assigned_by

Actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Membership alone never creates offering access.

## Unique keys

- `id`
- `person_id, cohort_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| cohort_id, effective_from, effective_to | Scoped cohort rostering. |
| person_id, effective_to | Person cohort eligibility. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
