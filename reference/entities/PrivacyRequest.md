# PrivacyRequest

Verified and auditable case for an individual data-rights or records request.

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

### subject_person_id

Individual whose records are in scope.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requester_principal_id

Verified actor who filed on own or delegated behalf.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### request_kind

Requested institutional workflow.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "access",
    "correction",
    "restrict",
    "dispose",
    "portability"
  ]
}
```

### scope_classes

Specific requested data classes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "identity_contact",
      "enrollment_history",
      "academic_official",
      "submissions",
      "drafts",
      "exam_telemetry",
      "audit",
      "connector_message",
      "communication",
      "backup",
      "private_export",
      "asset_bytes"
    ]
  },
  "minItems": 1,
  "maxItems": 12,
  "uniqueItems": true
}
```

### received_at

Time of institution receipt.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### due_at

Institution-specific review deadline. Default operational target is 30 days absent local override.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### proof_ref

Restricted authority and verification evidence.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision_ref

Restricted approved disposition or refusal record.

Optional. Nullable.

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
    "received",
    "verified",
    "executing",
    "completed",
    "denied",
    "blocked"
  ]
}
```

## Integrity

- Proof and jurisdictional authority are evaluated before disclosure or destructive action.
- Incomplete provider work remains blocked or executing and never reports complete.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, due_at | Find due and blocked cases |
| institution_id, subject_person_id, received_at | Find previous privacy decisions for the subject |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| received | verified | VerifyPrivacyRequest | Reviewer confirms identity, scope and authority Lock accepted request scope. |
| received | denied | DecidePrivacyRequest | Reviewer refuses unverified or unauthorized request Record reason and permitted follow-up route. |
| verified | executing | DecidePrivacyRequest | Approved lawful scope and purpose-specific steps are recorded Create disposition or export tasks. |
| verified | denied | DecidePrivacyRequest | Records authority denies scope with reason Record allowed appeal or correction route. |
| executing | blocked | RecordDispositionOutcome | Hold, dependency or provider issue prevents completion Record blocked task and escalate before deadline. |
| blocked | executing | ResumePrivacyRequest | Authorized reviewer resolves or scopes the outstanding blocker Resume pending task without replaying completed effects. |
| executing | completed | CompletePrivacyRequest | Every approved task is complete or lawfully excluded with evidence Record final status and restricted collection path if applicable. |
