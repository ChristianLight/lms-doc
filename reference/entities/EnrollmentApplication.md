# EnrollmentApplication

Application, invitation acceptance or waitlist status before participation.

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

Offering applied for.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Intended learner.

Required. Null is rejected.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requested_section_id

Optional same-offering destination.

Optional. Nullable.

References [Section](Section.md). Must resolve to an authorized Section in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### admission_policy_version_id

Policy snapshot governing submitted request.

Required. Null is rejected.

References [AdmissionPolicyVersion](AdmissionPolicyVersion.md). Must resolve to an authorized AdmissionPolicyVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### route

Authorized application route.

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

### state

Application lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "requested",
    "waitlisted",
    "admitted",
    "declined",
    "cancelled",
    "expired"
  ],
  "default": "requested"
}
```

### priority

Approved waitlist priority, smaller sorts first.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000,
  "default": 0
}
```

### eligibility_snapshot

Applied checks and privileged references.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "rule": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
      },
      "result": {
        "type": "string",
        "enum": [
          "pass",
          "fail",
          "pending",
          "waived"
        ]
      },
      "basis_id": {
        "anyOf": [
          {
            "type": "string",
            "format": "uuid"
          },
          {
            "type": "null"
          }
        ]
      }
    },
    "required": [
      "rule",
      "result",
      "basis_id"
    ],
    "additionalProperties": false
  },
  "maxItems": 150,
  "minItems": 0
}
```

### submitted_at

Authoritative queue time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
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

## Integrity

- One open application per person and offering by default.
- Use source grants for distinct independent authority.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, priority, submitted_at, id | Deterministic eligible queue. |
| person_id, offering_id, state | One pending application policy. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | waitlisted | ApplyForEnrollment | Eligible but no unreserved seat. Queue with stable order. |
| requested | admitted | DecideEnrollmentApplication | Eligibility and capacity verified. Create or return Enrollment and first release. |
| waitlisted | admitted | AcceptSeatReservation | Unexpired reservation and eligibility. Consume reserved seat once. |
| requested | declined | DecideEnrollmentApplication | Authorized denial with reason. Record safe applicant disposition. |
| waitlisted | cancelled | CancelEnrollmentApplication | Same learner or authorized registrar. Release reservation if present. |
