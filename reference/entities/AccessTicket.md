# AccessTicket

Short-lived opaque delivery authority bound to one principal, binary and purpose.

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

Authenticated requester.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### storage_object_id

Exact immutable object.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### token_fingerprint

Hash of a cryptographically random bearer token. Raw token never stored.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### resource_version

Owner record version evaluated at issue.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### principal_epoch

Principal authorization version at issue.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### institution_epoch

Institution authorization version at issue.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### purpose

Permitted delivery operation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "download",
    "stream",
    "preview"
  ]
}
```

### expires_at

Absolute expiry. Default five minutes, capped by the approved access lifetime.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revoked_at

Explicit revocation when applicable.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Redeem against the same authenticated Principal and current domain decision. Restricted objects use gateway retrieval with revocation checks.
- Streaming tickets are scoped to bounded resource and range requests. A ticket is never a backend storage key.

## Unique keys

- `id`
- `token_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, expires_at | Find live tickets during incident revocation |

## Retention

Keep metadata for 30 days after expiry unless an audit or hold policy applies.
