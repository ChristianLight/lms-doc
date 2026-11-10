# RecalculationRun

Scoped dry run or reviewed recalculation job with pinned policy and inputs.

Owned by **records**.

## Fields

### id

Stable globally unique RecalculationRun identifier.

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

Exact candidate policy in same offering.

Required. Null is rejected.

References [GradePolicyVersion](GradePolicyVersion.md). Exact candidate policy in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### algorithm_version

Candidate calculation engine version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### state

Job lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "running",
    "ready",
    "partially_ready",
    "applying",
    "applied",
    "cancelled",
    "failed"
  ],
  "default": "queued"
}
```

### mode

Authorized recalc intent.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "preview",
    "proposed_correction",
    "policy_adoption"
  ],
  "default": "preview"
}
```

### reason

Recorded review purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### input_cutoff_at

Approved evidence boundary.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### input_digest

Frozen target set and exact cutoff vector digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### review_digest

Deterministic complete comparison fingerprint.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### expected_count

Size of frozen target set.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100000
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

- Preview never changes learner-visible grade.
- Approved apply requires current material target state and exact review digest.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, created_at | Find job by offering and status. |

## Retention

Retain according to institution audit retention and hold. Keep source pointers while a retained official output requires them.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| queued | running | ProcessRecalculationTarget | Worker scoped to named run and lease Claim bounded target work. |
| running | ready | ProcessRecalculationTarget | All targets have a usable candidate Finalize stable review digest. |
| ready | applied | ApplyRecalculationRun | Independent approval and target preconditions Advance computed pointers and write outbox, no grade release. |
