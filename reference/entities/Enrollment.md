# Enrollment

Durable participation of one institutional person in one offering.

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

Owning course delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Learner institutional identity.

Required. Null is rejected.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Participation state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "withdrawn",
    "closed"
  ],
  "default": "active"
}
```

### admitted_at

First authoritative acceptance.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state_effective_at

Current participation boundary.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revision

Optimistic revision.

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

- Retakes use another offering.
- Suspension and withdrawal preserve previous attempts.

## Unique keys

- `id`
- `offering_id, person_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, state, admitted_at | Personal learning dashboard. |
| offering_id, state, admitted_at | Scoped rosters and capacity. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | suspended | TransitionEnrollment | Authorized scope and reason. Revoke ordinary learning actions. |
| active | withdrawn | TransitionEnrollment | Approved withdrawal. End active capacity and remote group rights. |
| active | closed | TransitionEnrollment | Offering close or specific approved decision. Preserve review and records rights. |
| suspended | active | TransitionEnrollment | Recheck seat and participation status. Resume existing stable enrollment. |
| withdrawn | active | TransitionEnrollment | Registrar exception and seat available. Restore explicit release under same enrollment. |
| closed | active | TransitionEnrollment | Approved reactivation. Resume on explicit release. |
