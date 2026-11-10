# RoleDefinitionVersion

Immutable set of permitted capabilities and allowed delegation for an institutional role key.

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

### role_key

Stable role family code. Protected system keys cannot be redefined.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### revision

Monotonically increasing version for this role family.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### capability_keys

Capability keys in reviewed stable catalog.

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
  "maxItems": 200,
  "uniqueItems": true
}
```

### allowed_scope_types

Scope kinds at which the role can be assigned.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
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
  "minItems": 1,
  "maxItems": 15,
  "uniqueItems": true
}
```

### delegable_role_keys

Role families the holder may propose where separately authorized.

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
  "minItems": 0,
  "maxItems": 50,
  "uniqueItems": true
}
```

### published_by_id

Principal approving this definition.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effective_at

Earliest time at which a new assignment may reference this revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Existing grants retain their exact role revision until intentionally replaced. A new role version never silently broadens a grant.
- Institution-defined roles cannot grant restricted platform or custody operations absent approval.

## Unique keys

- `id`
- `institution_id, role_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, role_key, effective_at | Find assignable published role revision |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
