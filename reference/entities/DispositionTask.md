# DispositionTask

One independently retryable disposition step against a specific record version and store.

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

### privacy_request_id

Source request or null for routine schedule.

Optional. Nullable.

References [PrivacyRequest](PrivacyRequest.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_id

Approved rule applied to this class.

Required. Null is rejected.

References [RetentionPolicy](RetentionPolicy.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### record_class

Data class at approval.

Required. Null is rejected.

```json
{
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
}
```

### target_type

Authoritative domain object kind.

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

Exact target identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_version

Observed source version. Re-evaluate before mutating.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### store_key

Registered data store or processor boundary.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### action

Approved step outcome type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "delete",
    "pseudonymize",
    "archive",
    "exclude"
  ]
}
```

### eligibility_at

Earliest execution time calculated under the pinned rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### action_key

Idempotent opaque key for this store, subject, operation and approved case.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### outcome_ref

Restricted deletion receipt, redaction evidence or blocked reason.

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
    "pending",
    "running",
    "applied",
    "blocked",
    "excluded"
  ]
}
```

## Integrity

- Recheck active holds, target version and current minimum retention immediately before execution.
- Retain a minimal restore-safe ledger of completed disposition outside the mutable primary backup generation.

## Unique keys

- `id`
- `institution_id, action_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, eligibility_at | Find eligible tasks for lease claim |
| institution_id, privacy_request_id, state | Calculate authoritative request status |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | running | StartDispositionTask | Authorized worker rechecks rule and obtains the target lock Claim task with fencing token. |
| running | applied | RecordDispositionOutcome | Current fence and verified store acknowledgement Record durable outcome and restore ledger. |
| running | blocked | RecordDispositionOutcome | Hold, stale version or uncertain processor state Record reason without claiming disposal. |
| running | excluded | RecordDispositionOutcome | Authorized reviewer documents lawful retained record Record rule and evidence reference. |
| blocked | pending | ResumePrivacyRequest | Reviewer approves refreshed scope or confirms blocker has cleared Requeue unapplied task only. |
