# PackageRuntimeMutation

Per-sequence digest and disposition needed to compare retransmitted or overlapping runtime prefixes.

Owned by **interoperability**.

## Fields

### id

Immutable interoperability record identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### launch_session_id

Exact writer session and epoch.

Required. Null is rejected.

References [PackageLaunchSession](PackageLaunchSession.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### commit_id

Durable accepted transaction for this sequence.

Required. Null is rejected.

References [PackageCommit](PackageCommit.md). Commit and mutation have the same launch session and occurrence attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sequence

Exact contiguous sequence within this launch session.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### element_key

Validated canonical element address.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### value_digest

Digest of canonical lexical value and exact element address. Use keyed digest for protected small vocabularies.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### disposition

Durable state scope actually changed.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "attempt_state",
    "session_state",
    "shared_store"
  ]
}
```

## Integrity

- Only accepted sequences receive a row. A reused sequence is accepted as a replay only if its exact element and value digest match. No raw learner response appears in replay metadata.

## Unique keys

- `id`
- `launch_session_id, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| commit_id, sequence | Read immutable ordered acceptance history. |

## Retention

Retain at least through all authorized replay and receipt recovery windows. Longer grade evidence retention follows the registered institution policy.
