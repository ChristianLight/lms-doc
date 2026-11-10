# ServicePrincipalProfileVersion

Narrow, versioned mandate for non-interactive worker or connector work.

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

### principal_id

Registered service actor. Human principals are forbidden.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_principal_id

Accountable currently authorized human owner.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic mandate revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### scopes

Explicit permitted service scopes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "scope_type": {
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
      },
      "scope_id": {
        "type": "string",
        "format": "uuid"
      }
    },
    "required": [
      "scope_type",
      "scope_id"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 32
}
```

### command_keys

Declared supported commands.

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

### allowed_job_kinds

Exact job types eligible for this service actor.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "exam_marking",
      "release_dispatch",
      "asset_scan",
      "privacy_disposition",
      "sync",
      "notification",
      "bulk_report",
      "regrade",
      "course_import",
      "recovery_verification"
    ]
  },
  "minItems": 0,
  "maxItems": 10,
  "uniqueItems": true
}
```

### credential_ref

Restricted deployment or provider credential identifier. Raw credential material remains in custody.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._/-]*$"
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

Exclusive mandate expiration.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approval_ref

Independent security approval for scope, worker classes and credentials.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- No overlapping mandate windows for one Principal unless explicitly versioned under immediate supersession.
- A durable job mandate can complete a previously accepted effect but grants no academic authority outside that job.

## Unique keys

- `id`
- `institution_id, principal_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, principal_id, valid_from, valid_until | Resolve currently valid worker mandate |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
