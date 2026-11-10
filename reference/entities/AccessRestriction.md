# AccessRestriction

Explicit deny gate for safeguarding, investigation or emergency response.

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

Affected principal or null when policy denies every principal in scope.

Optional. Nullable.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scope_type

Validated scope type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "Institution",
    "OrganizationUnit",
    "AcademicPeriod",
    "Program",
    "Course",
    "CourseOffering",
    "Section",
    "LearningGroup",
    "Cohort",
    "Library",
    "Person",
    "IntegrationConnection",
    "AssessmentDelivery",
    "ExternalToolDeployment",
    "RosterFeed"
  ]
}
```

### scope_id

Exact target scope ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### capability_keys

Only these declared capabilities are blocked.

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
  "maxItems": 50,
  "uniqueItems": true
}
```

### include_descendants

Apply to scoped descendants when explicitly approved.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### valid_from

Inclusive activation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### valid_until

Exclusive boundary. Default emergency maximum 24 hours.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason_ref

Restricted case evidence. Public messages remain generic.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### issued_by_id

Authorized security officer or automated containment actor.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
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
    "revoked"
  ]
}
```

## Integrity

- Restriction wins over any role grant. Empty capability lists are rejected.
- A service suspension may be institutional. No unaudited system bypass.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, scope_type, scope_id, state, valid_until | Resolve matching restrictions before grants |
| institution_id, principal_id, state | Review subject-specific restrictions |

## Retention

Default 365 days for ordinary operational records. Follow approved audit schedule and active holds. Academic version history has its own retention.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | revoked | RevokeAccessRestriction | Independent reviewer confirms containment has ended Increment authorization epoch and retain evidence. |
