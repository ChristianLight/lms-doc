# PackageCommit

Immutable runtime batch receipt with exact accepted sequence and state revision.

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

### launch_session_id

Active session that submitted a valid batch.

Required. Null is rejected.

References [PackageLaunchSession](PackageLaunchSession.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sco_state_id

Changed occurrence state.

Required. Null is rejected.

References [PackageScoState](PackageScoState.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### payload_digest

Digest of canonical request envelope and mutations.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### first_sequence

First sequence in this receipt, or next expected sequence for an empty finalization.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### accepted_through_sequence

Highest accepted contiguous sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### mutation_count

Number of typed mutations accepted atomically.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 256
}
```

### state_revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### finalized

True if this receipt closed the run-time session.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### accepted_at

Database commit time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- A repeated payload cannot award duplicate time or evidence.
- Receipt exists only after atomic state and outbox commit.

## Unique keys

- `id`
- `launch_session_id, first_sequence, accepted_through_sequence, finalized`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| sco_state_id, state_revision | Audit accepted state history and recover replay acknowledgments. |

## Retention

Retain replay receipts for the registration retention horizon when used as grade or progression evidence.
