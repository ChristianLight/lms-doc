# Cmi5Registration

cmi5 course assignment, learner and native evidence relationship.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Authorized learner enrollment.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Exact native packaged assignment.

Required. Null is rejected.

References [ActivityVersion](ActivityVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### package_version_id

Approved cmi5 package.

Required. Null is rejected.

References [PackageVersion](PackageVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_registration_uuid

cmi5 registration identity supplied to AU launches.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_number

Native registration attempt ordinal.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000
}
```

### state

Native registration lifecycle derived under policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "satisfied",
    "abandoned",
    "withdrawn"
  ]
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### institution_id

Institution that owns this registration and learning record profile.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_release_id

Effective assignment release pinned at registration.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Release belongs to this exact Enrollment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_id

Exact occurrence of the packaged activity in the assigned release.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Placement belongs to this exact release and resolves to the pinned ActivityVersion.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_structure_digest

Digest of immutable approved cmi5 course structure.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### satisfaction_policy_revision

Immutable MoveOn and evidence projection policy revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

## Integrity

- AU evidence is bound to this registration and exact course revision.
- Satisfied evidence derives from declared MoveOn and valid AU outcomes.
- One enrollment may launch the same ActivityVersion in different placements without sharing registration, AU evidence, or attempt ordinals.

## Unique keys

- `id`
- `external_registration_uuid`
- `enrollment_id, placement_id, activity_version_id, attempt_number`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, enrollment_id, placement_id, state | Resume only the current registration for the selected occurrence. |

## Retention

Retain under learner evidence policy.
