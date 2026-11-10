# EmergencyAccessGrant

Short-lived additional individual authority for an incident.

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

Individually attributable named actor.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_by_id

Independent security approver.

Optional. Nullable.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scope_type

Exact scope type. No implicit descendants.

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

Validated scope target.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### capability_keys

Narrow pre-approved emergency capabilities.

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
  "maxItems": 12,
  "uniqueItems": true
}
```

### incident_ref

Existing institution incident ticket identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### expires_at

Exclusive expiry. Required when active and max 60 minutes after activation.

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
    "requested",
    "active",
    "revoked",
    "denied"
  ]
}
```

## Integrity

- Actor, approver and requester must be attributable. Recipient cannot approve. Every use has an audit event and alert.
- Emergency authority cannot bypass restriction, academic release policy or legal hold.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, state, expires_at | Enforce emergency permission lifetime |

## Retention

Default 365 days for ordinary operational records. Follow approved audit schedule and active holds. Academic version history has its own retention.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | active | DecideEmergencyAccess | Independent security reviewer confirms incident and narrower regular access cannot restore service Set expiry and alert the incident owner. |
| requested | denied | DecideEmergencyAccess | Reviewer records refusal Keep incident evidence. |
| active | revoked | RevokeEmergencyAccess | Incident owner closes or security revokes Bump Principal epoch and expire derived access immediately. |
