# PrivacyCaseStep

Scoped non-destructive work item for a verified privacy request.

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

Approved parent request.

Required. Null is rejected.

References [PrivacyRequest](PrivacyRequest.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### action

Authorized purpose and work type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "collect",
    "correct",
    "restrict_processing",
    "restore_processing"
  ]
}
```

### target_type

Authoritative resource type. Resolve against domain registry.

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

Scoped target identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expected_target_version

Exact approved version to revalidate before access or change.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### data_class

Approved scope for collected or changed fields.

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

### instruction_ref

Protected authorized field projection or proposed correction evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effect_key

Stable effect identity for canonical approved operation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### result_ref

Protected artifact or verified applied canonical effect reference.

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
    "applied",
    "blocked",
    "excluded"
  ]
}
```

## Integrity

- Scope and authorization are checked before collection or owner mutation. This step grants no deletion authority.
- A subject correction uses canonical owner operation. Historical evidence and issued records retain original versions until an authorized correction.

## Unique keys

- `id`
- `institution_id, privacy_request_id, effect_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, privacy_request_id, state | Detect incomplete verified case work |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | applied | RecordPrivacyCaseStep | Authorized canonical projection or mutation was durably applied to the exact target Record protected result and audit. |
| pending | blocked | RecordPrivacyCaseStep | Authority, record version or provider outcome remains unresolved Block request completion and escalate. |
| pending | excluded | RecordPrivacyCaseStep | Authorized records officer records lawful exclusion and evidence Preserve exclusion evidence without disclosing excluded record. |
| blocked | pending | ResumePrivacyRequest | Authorized reviewer supplies new evidence or unblocks canonical operation Requeue unfinished approved work. |
