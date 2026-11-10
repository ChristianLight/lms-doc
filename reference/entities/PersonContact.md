# PersonContact

Restricted verified contact point used for allowed direct communications.

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

### person_id

Contact owner.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### kind

Contact channel.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "email",
    "telephone",
    "postal"
  ]
}
```

### protected_value_ref

Reference to encrypted and access-controlled raw contact value.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### value_fingerprint

Institution-keyed HMAC over channel and normalized contact value for per-person deduplication.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### verified_at

Successful confirmation time. Absent when pending or revoked.

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
    "pending",
    "verified",
    "revoked"
  ]
}
```

## Integrity

- A shared contact point can belong to multiple people and must never merge them.
- Never return the protected value or fingerprint in roster, metrics, role or audit exports.
- Telephone uses normalized E.164 where possible. Email lowercases the domain and preserves local-part semantics.

## Unique keys

- `id`
- `institution_id, person_id, kind, value_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, person_id, state, kind | Select verified contacts for a person and channel |

## Retention

Retain live and historic references while required by enrollment or records. Apply identity_contact policy to separately protected contact data.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | verified | VerifyPersonContact | Single-use proof matches the contact version and purpose Set verified_at and revoke the proof. |
| pending | revoked | RevokePersonContact | Owner or privacy administrator requests removal Invalidate pending proof. |
| verified | revoked | RevokePersonContact | Owner or privacy administrator requests removal Disable downstream delivery and schedule disposal of the protected value. |
