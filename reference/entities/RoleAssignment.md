# RoleAssignment

An exact role revision granted to a Principal for an explicit scope and time window.

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

Recipient of the contextual grant.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### role_definition_version_id

Pinned capability definition.

Required. Null is rejected.

References [RoleDefinitionVersion](RoleDefinitionVersion.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scope_type

Explicit capability context type.

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

Resource identity in the institution. Validate against the registry for scope_type.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### include_descendants

When true, apply only through the declared typed scope relations.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### valid_from

Inclusive activation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### valid_until

Exclusive expiration time. Null only for approved standing grants.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### granted_by_id

Actor responsible for proposing the grant.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_by_id

Independent approver for sensitive grants.

Optional. Nullable.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Purpose of the assignment. Sanitize when displaying or exporting.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1000
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
    "approved",
    "revoked",
    "denied"
  ]
}
```

## Integrity

- Serialize overlapping writes for the tuple principal, role family, scope type and scope ID. Multiple approved overlapping windows for that tuple are forbidden.
- An expired approved grant has no effect. Revocation never rewrites history.
- Assignee cannot approve their own grant. Scope overlap does not authorize a role outside the delegate's approved authority.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, state, valid_from, valid_until | Resolve current subject grants |
| institution_id, scope_type, scope_id, state | Review active and pending assignments in a scope |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | approved | ApproveRoleAssignment | Independent approval and current delegation authority satisfy the privilege policy Bump institution authorization epoch and log grant. |
| pending | denied | RejectRoleAssignment | Security reviewer records decision Retain rejected grant for audit. |
| pending | revoked | RevokeRoleAssignment | Proposer or authorized administrator cancels Mark future activation unavailable. |
| approved | revoked | RevokeRoleAssignment | Security or scope manager with revocation rights acts Bump authorization epoch and immediately reject further protected access. |
