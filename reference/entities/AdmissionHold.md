# AdmissionHold

Effective registrar-controlled restriction to normal enrollment eligibility.

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

### offering_id

Restricted offering.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Learner subject.

Required. Null is rejected.

References [Person](Person.md). Person must belong to the same institution as the offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason_code

Restricted internal classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### safe_explanation

Learner-safe next action.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1000
}
```

### issued_by

Accountable authorized registrar.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

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

Exclusive end when finite.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revision

Lifecycle compare-and-swap token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

## Integrity

- Hold blocks new normal admission; existing enrollment state changes separately.
- Private justification is retained in an authorized audit record only.

## Unique keys

- `id`
- `offering_id, person_id, effective_from, reason_code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, person_id, effective_from, effective_to | Resolve present admission holds. |

## Retention

Retain with scoped academic record history while referenced and through the institutional retention window or any hold.
