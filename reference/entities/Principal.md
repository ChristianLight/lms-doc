# Principal

Institution-local actor that authenticates through a host or a service credential.

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

Human's educational identity. Null for service actors.

Optional. Nullable.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### kind

Human or non-interactive actor class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "human",
    "service"
  ]
}
```

### authorization_epoch

Principal-local permission and session version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### last_authenticated_at

Last successfully bound authentication time. Administrative visibility only.

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
    "active",
    "suspended",
    "retired"
  ]
}
```

## Integrity

- Human requires a Person. A service has no Person or learner enrollment.
- More than one authorized Principal may map to a Person. Academic records attach to Person.
- Suspension does not automatically unsuspend or reactivate linked Person or credential.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, person_id, state | Find human credentials during offboarding or privacy processing |

## Retention

Retain live and historic references while required by enrollment or records. Apply identity_contact policy to separately protected contact data.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | suspended | SetPrincipalState | Authorized security officer acts or compromise signal is confirmed Bump local epoch, revoke sessions, credentials and queued interactive authority. |
| suspended | active | SetPrincipalState | Security review clears the account and linked Person is active Issue fresh sessions only after reauthentication. |
| active | retired | SetPrincipalState | Verified irreversible credential retirement is approved Disable access and preserve actor attribution. |
| suspended | retired | SetPrincipalState | Verified irreversible credential retirement is approved Disable access and preserve actor attribution. |
