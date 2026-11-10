# TransferApproval

Immutable approval of an exact staged plan and bounded scope.

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

### job_id

Approved plan owner.

Required. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### plan_revision

Reviewed plan version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### plan_digest

Exact graph and baseline digest approved.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### plan_manifest_id

Protected immutable manifest reviewed by this approval. Must match the approved digest and exact plan revision.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Exact clean StorageObject owned by this transfer plan and Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reviewer_principal_id

Authorized actor or service identity for the recorded operation.

Required. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approval_kind

Which owner gate the decision satisfies.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "curriculum",
    "assessment",
    "privacy",
    "publication",
    "export_projection"
  ]
}
```

### reason

Review evidence and rationale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2000
}
```

### scope_keys

Concrete scopes approved by this actor.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 256
  },
  "maxItems": 200,
  "minItems": 1,
  "uniqueItems": true
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

## Integrity

- Approvals cannot be edited or moved to a new plan revision.
- Reviewer authority is revalidated before activation.
- An export projection approval pins both the frozen selection and the exact capability and loss report digest. Required losses cannot be approved into a successful output.

## Unique keys

- `id`
- `job_id, plan_revision, reviewer_principal_id, approval_kind`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, plan_revision, approval_kind | Check all required gates for one plan. |

## Retention

Retain with the transfer and publication audit history.
