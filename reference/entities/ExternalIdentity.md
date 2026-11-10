# ExternalIdentity

Verified subject binding between an external identity registration and a Principal.

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

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### principal_id

Linked human or service actor.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### connection_id

Registered identity connection for this issuer and client context.

Required. Null is rejected.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### issuer

Exact issuer identifier from the trusted authentication configuration.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### subject_fingerprint

Institution-scoped HMAC of exact issuer and subject in this connection.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### protected_subject_ref

Restricted encrypted provider subject for reconciliation and key rotation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### verified_at

Binding verification instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "linked",
    "unlinked"
  ]
}
```

## Integrity

- A linked provider subject points to one Principal. This system refuses silent reassignment, email correlation, and accidental relinking of a tombstone.
- Exact issuer and provider registration must match the token or trusted host assertion.

## Unique keys

- `id`
- `institution_id, connection_id, issuer, subject_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, state | Find all verified identities of a Principal |

## Retention

Retain inactive references and outcome history while in-use dependent records remain. Scrub secrets and contact attributes according to policy.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| linked | unlinked | UnlinkExternalIdentity | Authority is reverified and acceptable recovery path remains or Principal is already suspended Bump Principal epoch, invalidate existing sessions, retain uniqueness tombstone. |
