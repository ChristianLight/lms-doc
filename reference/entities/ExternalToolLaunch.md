# ExternalToolLaunch

Single-use OIDC state and nonce record for a scoped launch.

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

### deployment_id

Authorized tool.

Required. Null is rejected.

References [ExternalToolDeployment](ExternalToolDeployment.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resource_link_id

Launch destination when resource launch.

Optional. Null is rejected.

References [ExternalToolResourceLink](ExternalToolResourceLink.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### actor_principal_id

Authorized actor or service identity for the recorded operation.

Required. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### launch_kind

Exact LTI message intent.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "resource",
    "deep_link"
  ]
}
```

### target_link_uri

Pinned target URI of authorization request.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
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

### expires_at

Maximum state lifetime.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### consumed_at

OIDC challenge consumption time when the platform issues the ID token. This does not consume a later Deep Linking response.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### course_offering_id

Owning released or authoring context.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_version_id

Exact editor-selected draft destination for deep linking.

Optional. Null is rejected.

References [CourseVersion](CourseVersion.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### destination_placement_id

Optional placement or container destination pinned to the draft version.

Optional. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### destination_revision

Draft compare-and-swap revision required for authoring intent.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### browser_session_digest

Binding to authenticated app browser session, not a raw cookie or token.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### deep_link_correlation_digest

One-use digest of platform-generated echoed deep-link data.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### accepted_content_types

Permitted LTI Deep Linking content types for this challenge.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 100
  },
  "maxItems": 20,
  "minItems": 1,
  "uniqueItems": true
}
```

### accepted_media_types

Allowed media types for this authoring challenge.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 128
  },
  "maxItems": 20,
  "minItems": 0,
  "uniqueItems": true
}
```

### accept_multiple

Whether tool may return more than one item.

Optional. Null is rejected.

```json
{
  "type": "boolean"
}
```

### deep_link_return_uri

Exact trusted platform callback URL for this authoring challenge.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### response_consumed_at

Independent one-use timestamp for a validated deep-link response.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### login_hint_digest

Digest of the one-use opaque platform-issued login hint.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### message_hint_digest

Digest of the platform-issued message hint when present.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### tool_state_digest

Digest of tool-generated state supplied only at authorization.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### tool_nonce_digest

Digest of tool-generated nonce supplied only at authorization.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- Launch credentials must be single-use and bound to current authenticated session.
- No private key or raw token is persisted in audit.
- Resource launch requires a released resource link, exact context and same browser binding. Deep Linking launch requires a writable draft destination, draft revision, return URI, allowed content types and independent response correlation.
- Consume OIDC signing and Deep Linking callback independently. A replay cannot obtain a second ID token or replace the validated selection.
- Authorize once only. Validate state and nonce from the tool request, sign the requested nonce and echo the exact tool state to its registered redirect. Raw secrets do not enter ordinary receipts or logs.

## Unique keys

- `id`
- `deployment_id, login_hint_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| expires_at | Purge expired launch secrets and replay keys under policy. |

## Retention

Retain digest replay records for configured security horizon and purge raw transient values immediately.
