# RecognitionDecision

Append-only decision on recognized study, credit or requirement mapping.

Owned by **records**.

## Fields

### id

Stable globally unique RecognitionDecision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Educational identity within the same institution.

Required. Null is rejected.

References [Person](Person.md). Educational identity within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### request_id

Original authorized recognition request.

Required. Null is rejected.

References [RecognitionRequest](RecognitionRequest.md). Original authorized recognition request.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Prior decision for same recognition.

Required. Nullable.

References [RecognitionDecision](RecognitionDecision.md). Prior decision for same recognition.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### predecessor_key

Canonical nonnull key, root for first decision or superseded decision UUID.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(root|[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12})$"
}
```

### evidence_digest

Approved immutable evidence snapshot digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### outcome

Disposition of evidence recognition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "accepted",
    "rejected",
    "revoked"
  ]
}
```

### mapped_course_id

Approved institutional equivalence if any.

Required. Nullable.

References [Course](Course.md). Approved institutional equivalence if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### mapped_requirement_id

Exact approved rule mapping if any.

Required. Nullable.

References [ProgramRequirement](ProgramRequirement.md). Exact approved rule mapping if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### credit_scheme_id

Normalized credit unit if awarded.

Required. Nullable.

References [CreditUnitSchemeVersion](CreditUnitSchemeVersion.md). Normalized credit unit if awarded.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### earned_credit_units

Approved distinct credits. Waiver has zero by default.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$",
  "default": "0"
}
```

### gpa_eligible

Explicit reviewed inclusion in GPA.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### effective_at

Academic recognition effective instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Optional expiry of rule satisfaction.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason

Authorized reviewer rationale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Predecessor key is root only for a first decision and otherwise equals superseded decision UUID. Lock recognition request head to prevent branching.
- Cannot grant external GPA silently.
- Nonzero credit requires approved unit scheme.
- Revoke by new decision.

## Unique keys

- `id`
- `request_id, predecessor_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, effective_at, outcome | Resolve recognition facts at academic cutoff. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
