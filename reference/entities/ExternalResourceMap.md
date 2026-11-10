# ExternalResourceMap

Live synchronization binding to a provider resource.

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

### connection_id

Connector that owns the mapping.

Required. Null is rejected.

References [IntegrationConnection](IntegrationConnection.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### local_type

Canonical resource kind.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### local_id

Institution-local resource UUID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_type

Provider model type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### external_id

Stable provider identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### external_version

Last acknowledged provider revision or ETag.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### local_desired_version

Local version reconciliation seeks.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### reconciled_local_version

Most recent successfully acknowledged local version.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
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
    "pending_removal",
    "removed",
    "conflict"
  ]
}
```

## Integrity

- No automatic rebinding after removal or collision. Content transfer provenance belongs to ExternalObjectMap.
- Authority rule and connector version govern each field mutation.

## Unique keys

- `id`
- `institution_id, connection_id, local_type, local_id`
- `institution_id, connection_id, external_type, external_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, connection_id, state | Find conflicts and removal work |

## Retention

Retain inactive references and outcome history while in-use dependent records remain. Scrub secrets and contact attributes according to policy.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| linked | pending_removal | SetExternalResourceDesiredState | Owner provides current local version and explicit removal evidence Queue idempotent provider removal. |
| pending_removal | removed | ApplySyncPage | Provider confirms disappearance or deletion Retain tombstone and outcome evidence. |
| linked | conflict | ApplySyncPage | Incoming mapping or version conflicts with validated local authority Preserve local records and queue review. |
| conflict | linked | ResolveExternalResourceConflict | Authorized reviewer confirms a verified match Advance desired version and retry reconciliation. |
