# GradePolicyAdoptionBatch

Reviewed staged effective grade policy assignments with atomic visibility switch.

Owned by **records**.

## Fields

### id

Stable globally unique GradePolicyAdoptionBatch identifier.

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

### policy_version_id

Published grade policy in same offering.

Required. Null is rejected.

References [GradePolicyVersion](GradePolicyVersion.md). Published grade policy in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assignment_ids

Complete staged immutable assignment set. Empty only when changing the offering default alone.

Required. Null is rejected.

References [GradePolicyAssignment](GradePolicyAssignment.md). Complete staged immutable assignment set. Empty only when changing the offering default alone.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 100000,
  "minItems": 0,
  "uniqueItems": true
}
```

### set_default_for_new_enrollments

Select this policy for new enrollment releases at the approved effective time.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### scope_digest

Authorized enrollment scope and expected predecessor digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### effective_at

Approved effective time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Adoption review and visibility lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "approved",
    "active",
    "superseded",
    "revoked",
    "stale"
  ],
  "default": "staged"
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

- Current assignments remain visible until whole batch activates.
- A changed predecessor or enrollment release rejects activation.
- Activated default-setting batches are ordered by exclusive approved effective boundary and guarded sequence. Offering default is the latest active applicable default-setting batch.

## Unique keys

- `id`
- `policy_version_id, scope_digest, effective_at`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, effective_at | Find approved staged cutovers. |

## Retention

Retain according to institution audit retention and hold. Keep source pointers while a retained official output requires them.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | active | ActivateGradePolicyAssignments | Complete batch and exact predecessors match Switch assignments using one visibility guard. |
