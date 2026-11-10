# Institution

Independent policy, access and retention boundary.

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

### code

Public operator-issued code unique within this deployment. Stable after activation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### name

Institution display name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 180
}
```

### default_locale

Fallback BCP 47 content and UI language.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
}
```

### default_timezone

Default civil zone validated against the deployed IANA database.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^(UTC|[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+)+)$"
}
```

### authorization_epoch

Institution-wide permission version. Bump in each role, delegation, hierarchy or visibility policy mutation.

Required. Null is rejected.

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
    "active",
    "suspended",
    "closed"
  ]
}
```

## Integrity

- Institution ID is its root scope ID. No operation treats a subordinate organization as an independent tenant.
- Closing or suspending gates access while retaining academic records and scoped privacy processing.

## Unique keys

- `id`
- `code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| state, code | Filter institutional operations and identify active tenant |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | suspended | SetInstitutionState | Security administrator confirms incident or approved suspension Stop teaching and learner access except authorized privacy and recovery operations. |
| suspended | active | SetInstitutionState | Authorized recovery and access checks complete Increment authorization epoch and reopen assigned services. |
| suspended | closed | SetInstitutionState | Registrar approves closure and archival ownership is recorded Retain protected record retrieval through approved records workflows. |
