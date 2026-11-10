# PeerReviewAllocationRun

Frozen peer graph, algorithm and assignment set for one round.

Owned by **assessment**.

## Fields

### id

Stable globally unique PeerReviewAllocationRun identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Approved policy used for this allocation.

Required. Null is rejected.

References [PeerReviewPolicyVersion](PeerReviewPolicyVersion.md). Approved policy used for this allocation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### round

Ordinal review round under policy.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### cohort_digest

Sealed reviewer, submission and exclusion inputs.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### assignment_digest

Canonical assignment graph and shortfall manifest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### cutoff_at

Roster and sealed work snapshot time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### allocated_by

Authorized coordinator or approved service.

Required. Null is rejected.

References [Principal](Principal.md). Authorized coordinator or approved service.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### allocated_at

Authoritative publication time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Allocation retries reproduce same eligible edges.
- Freeze submitted evidence reference per edge.

## Unique keys

- `id`
- `policy_version_id, round`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| policy_version_id, round | Resolve active and prior review allocations. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
