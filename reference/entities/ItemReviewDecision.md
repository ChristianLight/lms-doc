# ItemReviewDecision

Immutable decision against one reviewed item digest.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemReviewDecision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Review target in the reviewer bank scope.

Required. Null is rejected.

References [ItemVersion](ItemVersion.md). Review target in the reviewer bank scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_digest

Exact approved, returned or rejected graph.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### reviewer_id

Authorized reviewer, independent where required.

Required. Null is rejected.

References [Principal](Principal.md). Authorized reviewer, independent where required.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision

Approval or return outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "approve",
    "changes_requested",
    "reject"
  ]
}
```

### reason

Private concise rationale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### decided_at

Authoritative decision time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A decision never approves a changed graph.

## Unique keys

- `id`
- `item_version_id, content_digest, reviewer_id, decided_at`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| item_version_id, decided_at | Ordered version review history. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
