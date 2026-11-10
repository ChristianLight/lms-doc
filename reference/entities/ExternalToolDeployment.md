# ExternalToolDeployment

LTI 1.3 trust registration and context-limited service authorization.

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

### institution_id

Institution owning these data and their access policy.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### issuer

Exact configured OIDC issuer.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### client_id

Registered issuer client ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### deployment_key

Case-sensitive deployment claim.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### target_uris

Explicit registered target link URIs.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uri",
    "maxLength": 2048
  },
  "maxItems": 100,
  "minItems": 1,
  "uniqueItems": true
}
```

### redirect_uris

Exact registered OIDC callback allowlist.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uri",
    "maxLength": 2048
  },
  "maxItems": 100,
  "minItems": 1,
  "uniqueItems": true
}
```

### jwks_uri

Pinned origin or vetted location for public verification keys.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### scopes

Approved least-privilege service scopes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uri",
    "maxLength": 2048
  },
  "maxItems": 50,
  "minItems": 0,
  "uniqueItems": true
}
```

### role_profile

Versioned role translation policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pending",
    "active",
    "suspended",
    "retired"
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

### login_initiation_uri

Exact approved tool endpoint for third-party login initiation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

## Integrity

- Exact issuer, audience, nonce, deployment and target checks apply.
- Service scopes cannot exceed those approved by institution.

## Unique keys

- `id`
- `institution_id, issuer, client_id, deployment_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state | Resolve active deployment after cryptographic validation. |

## Retention

Retain deployment history while any resource link, grade evidence or consent audit refers to it.
