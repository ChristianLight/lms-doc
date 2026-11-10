# Cmi5LaunchSession

One cmi5 AU session and one-use credential fetch record.

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

### registration_id

Owning registration.

Required. Null is rejected.

References [Cmi5Registration](Cmi5Registration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### au_key

Verified assignable-unit identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### session_uuid

cmi5 context session ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### launch_mode

Effective mode for this AU launch.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "Normal",
    "Browse",
    "Review"
  ]
}
```

### fetch_digest

Digest of one-use fetch credential.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### lease_expires_at

Maximum credential and launch lease expiry.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### fetched_at

One-time fetch success time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### terminated_at

Valid terminated evidence time.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "issued",
    "fetched",
    "initialized",
    "terminated",
    "abandoned",
    "revoked"
  ]
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### generation

Monotonic generation fencing current launch and credential.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### au_activity_iri

Assigned platform activity IRI for this AU, verified against immutable package map.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### credential_digest

Stored digest of the bounded credential issued after fetch.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### last_evidence_ordinal

Highest accepted evidence ordinal for this session.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

## Integrity

- Browse and Review cannot alter completion, success or score evidence.
- Fetched credentials cannot be returned to a second fetch request.

## Unique keys

- `id`
- `session_uuid`
- `fetch_digest`
- `registration_id, generation`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| registration_id, state | Reject stale credential reuse and record abandonment. |

## Retention

Retain session evidence under registration policy and destroy credentials when consumed or expired.
