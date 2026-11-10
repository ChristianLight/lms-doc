# GradePolicyAssignment

Effective grade policy pinned to an EnrollmentRelease.

Owned by **records**.

## Fields

### id

Stable globally unique GradePolicyAssignment identifier.

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

### enrollment_release_id

Exact active or historical content release in same enrollment.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Exact active or historical content release in same enrollment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Published same-offering grade policy.

Required. Null is rejected.

References [GradePolicyVersion](GradePolicyVersion.md). Published same-offering grade policy.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effective_from

Inclusive effective start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive end, null while open.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Publication staging and active state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "active",
    "superseded",
    "cancelled"
  ],
  "default": "staged"
}
```

### adoption_digest

Approved assignment scope fingerprint.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
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

- Effective intervals cannot overlap for the enrollment.
- Staged rows are invisible until assignment batch activation.

## Unique keys

- `id`
- `enrollment_release_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, effective_from, effective_to | Resolve exact assignment at cutoff. |
| offering_id, state, policy_version_id | Find staged or active assignment batches. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | active | ActivateGradePolicyAssignments | Expected batch complete and reviewed Switch assignment visibility atomically. |
| active | superseded | ActivateGradePolicyAssignments | New interval takes effect Close prior interval at new start. |
