# VerificationChallenge

Short-lived, one-use proof for a particular verified contact or identity link intent.

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

Actor authorized to satisfy the challenge.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### contact_id

Contact being verified, when purpose is contact verification.

Optional. Nullable.

References [PersonContact](PersonContact.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### connection_id

Identity connector, when purpose is an external account link.

Optional. Nullable.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### purpose

Exact operation to which this challenge is bound.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "verify_contact",
    "link_external_identity"
  ]
}
```

### target_version

Version of the contact or principal being verified.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### secret_fingerprint

Keyed fingerprint of proof. Present only while a challenge is open. No plaintext proof persists.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### expires_at

Exclusive expiry, default creation plus 15 minutes.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### attempts

Attempts observed. Starts at zero.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 5
}
```

### consumed_at

First durable successful use.

Optional. Nullable.

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
    "open",
    "consumed",
    "revoked"
  ]
}
```

## Integrity

- Require one contact for contact verification and one connection for account link. Proof fingerprint includes purpose and target.
- Five failed attempts revoke the challenge. Expiry is enforced using server time even when persisted state is open.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, purpose, state, expires_at | Find current verification challenge and revoke stale intent |

## Retention

Keep outcome metadata for 30 days by default and erase secret fingerprint when terminal.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| open | consumed | VerifyPersonContact | Verified contact version and proof match Commit contact state and mark proof consumed. |
| open | consumed | LinkExternalIdentity | Verified provider state and Principal version match Commit unique subject binding and mark proof consumed. |
| open | revoked | RevokePersonContact | Contact authority withdrawn Reject the previously issued proof. |
