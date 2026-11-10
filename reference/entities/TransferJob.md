# TransferJob

A retryable plan to detect, review and promote an inbound graph or export selection.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning these data and their access policy.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### actor_principal_id

Authorized actor or service identity for the recorded operation.

Required. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### artifact_id

Inbound input or outbound artifact when produced.

Optional. Null is rejected.

References [TransferArtifact](TransferArtifact.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Authorized source namespace.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### format

Exact approved format profile.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native_curriculum",
    "olx_course",
    "olx_legacy_library",
    "olx_versioned_library",
    "scorm_12",
    "scorm_2004_2",
    "scorm_2004_3",
    "scorm_2004_4",
    "scorm_2004_unverified",
    "qti_21",
    "qti_22",
    "qti_301",
    "common_cartridge",
    "oneroster_12",
    "cmi5_quartz",
    "historic_records"
  ]
}
```

### adapter_build

Immutable adapter and policy build identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### direction

Direction of transfer.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "import",
    "export"
  ]
}
```

### mode

Configured operational intent.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "dry_run",
    "editable_draft",
    "historical",
    "delivery_package",
    "export"
  ]
}
```

### target_scope

Typed scope identifier and optional owner key, interpreted under format profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### selection_digest

Fingerprint of immutable outbound selection.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### plan_digest

Fingerprint of staged owner commands and target baseline.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### fence_epoch

Monotonic worker ownership epoch.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### worker_key

Authenticated worker lease owner.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### lease_expires_at

UTC fencing deadline.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### checkpoint

Opaque resumable partition and item position, excludes learner payload.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "received",
    "quarantined",
    "validated",
    "staged",
    "awaiting_review",
    "approved",
    "applying",
    "applied",
    "failed",
    "cancelled"
  ]
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### updated_at

Server time of last transition.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Import requires an artifact and export requires an immutable selection.
- Only the active fence can checkpoint or alter the plan.
- A changed plan digest invalidates all previous approvals.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, updated_at | Find reviewer and worker queues. |
| state, lease_expires_at | Find claimable expired worker leases. |

## Retention

Retain job, decision history and published owner receipts for seven years by default. Expire failed private staging after 30 days unless held.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| received | quarantined | InspectTransferArtifact | Artifact assembled and worker holds current fence. Record scan and archive limits. |
| quarantined | validated | InspectTransferArtifact | Format and schema checks pass. Pin adapter and typed source graph. |
| validated | staged | BuildTransferPlan | Every source record counted and candidate objects staged. Pin baseline revisions and plan fingerprint. |
| staged | awaiting_review | BuildTransferPlan | Report and stage artifacts durable. Expose scoped review. |
| awaiting_review | approved | ApproveTransferPlan | Required reviewers approve exact plan and no blocker remains. Write immutable approval. |
| approved | applying | ApplyTransferPlan | Approval and plan revision remain current. Stage owner receipts behind publication barrier. |
| applying | applied | ApplyTransferPlan | All owners confirm the staged generation and baseline. Activate one generation and record mapping. |
| applying | awaiting_review | ApplyTransferPlan | One baseline changed before activation. Keep staging private and invalidate prior approvals. |
| awaiting_review | staged | ResolveTransferIssue | Review decision changes candidate projections. Rebuild affected records and increment plan revision. |
| awaiting_review | cancelled | CancelTransferJob | Requester authorized and no visible commit exists. Revoke stage grants. |
