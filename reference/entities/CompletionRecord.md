# CompletionRecord

Immutable earned, exempt or corrective completion decision.

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

### enrollment_release_id

Exact participation release.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Optional exact occurrence; null means offering scope.

Optional. Nullable.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the course version in the cited EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Exact decision basis.

Required. Null is rejected.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision

Decision type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "earned",
    "exempt",
    "revoked"
  ]
}
```

### evidence_ids

Accepted LearningEvidence identifiers or lineage through projector.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 2000,
  "minItems": 0
}
```

### supersedes_id

Prior decision for same scope.

Optional. Nullable.

References [CompletionRecord](CompletionRecord.md). Must resolve to an authorized CompletionRecord in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### actor_id

Trusted service or human approval actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### earned_at

Learning completion instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### recorded_at

Authoritative append time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason_code

Machine decision basis.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### decision_digest

Immutable rule and evidence checksum.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- Supersession stays within exact scope.
- No destructive overwrite or silent revocation.

## Unique keys

- `id`
- `enrollment_release_id, decision_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, content_placement_id, recorded_at | Effective and historical completion chain. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
