# CommandReceipt

Response replay authority for a retryable external or internal command.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### principal_id

Original effective actor. Recheck actor eligibility when replaying.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### operation_key

Stable command contract.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### request_key

Client idempotency key scoped to actor, operation and target.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### target_scope_key

Canonical target type and ID or collection scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### request_digest

Canonical payload and precondition fingerprint.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### result_status

Recorded committed HTTP result status.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 200,
  "maximum": 599
}
```

### result_ref

Protected minimal replayable response or result reference.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expires_at

Replay lifetime. Default 7 days for ordinary writes.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### correlation_id

Original accepted request workflow identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Exam submission and other irreversible domain commands preserve durable business-level uniqueness beyond the transport receipt's expiry.
- Do not replay a protected response after its resource access is revoked.

## Unique keys

- `id`
- `institution_id, principal_id, operation_key, target_scope_key, request_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, expires_at | Expire receipts after their permitted replay window |

## Retention

7 days by default. Use longer institution profile when client retries can safely outlast this window.
