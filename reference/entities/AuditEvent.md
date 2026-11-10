# AuditEvent

Durable event for a sensitive action, access decision or disclosure.

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

### actor_id

Authenticating actor or null for system actor without a local principal.

Optional. Nullable.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### authority_assignment_id

Grant used where applicable.

Optional. Nullable.

References [RoleAssignment](RoleAssignment.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### subject_person_id

Restricted affected person identity when required for access reports.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### scope_type

Nearest assignable authority context type used or evaluated. The exact owner target is stored separately.

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

Nearest assignable authority context ID. Use Institution when a registered mandate has no more specific grant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### action

Stable permission or audited domain action key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### target_type

Opaque target class.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### target_id

Opaque target ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_version

Committed record version when applicable.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### outcome

Semantics of the event without response payload.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "allowed",
    "denied",
    "committed",
    "failed",
    "disclosed"
  ]
}
```

### occurred_at

Server UTC instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### correlation_id

Request or job trace identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason_code

Safe normalized reason without freeform protected text.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### evidence_ref

Separate custody-controlled evidence object.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### stream_seq

Ordered sequence within institution audit partition.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### record_hash

Digest of canonical audit metadata and prior hash in the same partition.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### previous_hash

Absent for the first event of a partition.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- Append only under audit custody. Retention removes a verified segment with a separately protected segment receipt.
- Academic mutation and its audit or authoritative event are atomic. Whole responses, answer keys and secrets are excluded.

## Unique keys

- `id`
- `institution_id, stream_seq`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, target_type, target_id, occurred_at | Trace a restricted resource history |
| institution_id, actor_id, occurred_at | Review privileged activity |

## Retention

Default 365 days for ordinary operational records. Follow approved audit schedule and active holds. Academic version history has its own retention.
