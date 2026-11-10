# GradeOverrideDecision

Append-only accepted, rejected or revoked override decision.

Owned by **records**.

## Fields

### id

Stable globally unique GradeOverrideDecision identifier.

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

### request_id

Approved scoped override request.

Required. Null is rejected.

References [GradeOverrideRequest](GradeOverrideRequest.md). Approved scoped override request.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### prior_decision_id

Previous decision when superseding or revoking.

Required. Nullable.

References [GradeOverrideDecision](GradeOverrideDecision.md). Previous decision when superseding or revoking.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### predecessor_key

Canonical nonnull key, root for first decision or prior decision UUID thereafter.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(root|[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})$"
}
```

### decision

Recorded registrar action.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "approve",
    "reject",
    "revoke"
  ]
}
```

### decision_reason

Restricted reason for the action.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### reviewed_fingerprint

Exact approved input preview.

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

### decided_at

Recorded decision time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_at

Academic effective instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Predecessor key is root only for a first decision and otherwise equals prior decision UUID. Compare request head under lock to prevent branching.
- Revocation targets an approved active decision.
- Active override on a result cannot silently vanish when source evidence changes.

## Unique keys

- `id`
- `request_id, predecessor_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| request_id, decided_at | Read approved decision and revocation lineage. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
