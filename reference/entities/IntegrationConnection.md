# IntegrationConnection

Institution-scoped versioned connector configuration and authority boundary.

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

### connection_key

Stable institution-unique name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### provider_kind

Supported functional profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "identity",
    "roster",
    "collaboration",
    "document",
    "media",
    "learning_tool",
    "notification",
    "authoring"
  ]
}
```

### api_profile

Declared versioned adapter capability profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### endpoint_origin

Approved canonical HTTPS origin. No embedded user information, query or fragment.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### credential_ref

Secret custody reference. Never return credential material.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._/-]*$"
}
```

### allowed_actions

Allowlisted capabilities for this installation.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 64,
    "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
  },
  "minItems": 1,
  "maxItems": 40,
  "uniqueItems": true
}
```

### authority

Which side owns desired changes. Split requires field-level rules.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "local",
    "provider",
    "split"
  ]
}
```

### retirement_days

Grace interval for controlled revocation of unused connector state.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 365,
  "default": 30
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "disabled",
    "enabled",
    "suspended",
    "retired"
  ]
}
```

## Integrity

- Endpoint or credential changes create a new observed configuration version. In-flight writes recheck the version and recipient before external effects.
- Provider absence or suspension never implicitly withdraws a learner or deletes an academic record.

## Unique keys

- `id`
- `institution_id, connection_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, provider_kind, state | Select eligible connector by profile |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| disabled | enabled | SetIntegrationConnectionState | Authorized reviewer verifies capabilities, credentials and data processing Allow approved operations and schedule initial reconciliation. |
| enabled | suspended | SetIntegrationConnectionState | Operator or incident response suspends Stop outbound effects and disable inbound handling except required receipts. |
| suspended | enabled | SetIntegrationConnectionState | Scope checks and reconciliation are approved Resume idempotent operations with current configuration. |
| disabled | retired | SetIntegrationConnectionState | Credentials revoked and references accounted for Retain redacted configuration history. |
| suspended | retired | SetIntegrationConnectionState | Credentials revoked and references accounted for Retain redacted configuration history. |
