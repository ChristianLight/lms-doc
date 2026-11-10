# AttemptSubmission

Single final sealed response manifest and receipt.

Owned by **assessment**.

## Fields

### id

Stable globally unique AttemptSubmission identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Target authorized attempt.

Required. Null is rejected.

References [Attempt](Attempt.md). Target authorized attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### receipt_id

Opaque globally unique finalization receipt.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### manifest

Ordered accepted revision references and explicit blank states.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "attempt_item_id": {
        "type": "string",
        "format": "uuid"
      },
      "interaction_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "response_revision_id": {
        "type": "string",
        "format": "uuid"
      },
      "disposition": {
        "type": "string",
        "enum": [
          "value",
          "blank",
          "pending_asset",
          "invalid_captured"
        ]
      }
    },
    "required": [
      "attempt_item_id",
      "interaction_key",
      "disposition"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 32000
}
```

### manifest_digest

Canonical sealed evidence hash.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### actor_id

Authorized candidate finalizer. Null for the automatic expiry worker.

Optional. Nullable.

References [Principal](Principal.md). Authorized candidate or staff finalizer, null for time worker.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Candidate submission or automatic expiry disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### effective_at

Candidate accepted time or scheduled automatic deadline.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### processed_at

Time durable sealing transaction completed.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- One authoritative submission per attempt.
- Manifest and referenced versions are immutable.
- Processed time is not before effective time.
- A complete form contains at most 32,000 interaction entries. Enforce cumulative response, manifest and protected attachment byte budgets before sealing.

## Unique keys

- `id`
- `attempt_id`
- `receipt_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| receipt_id | Recover candidate receipt without exposing answers. |
| attempt_id, manifest_digest | Verify marking input lineage. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
