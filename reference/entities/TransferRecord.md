# TransferRecord

A typed source object and its proposed target binding in one immutable staging revision.

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

Transfer job and source profile.

Required. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_scope

Stable parent scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### object_kind

Canonical or source-profile object type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### source_key

Exact original case-sensitive source key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### source_revision

Source snapshot key or content-derived revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### source_locator

Archive relative path and node selector, not an arbitrary URL.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### source_fingerprint

Digest of preserved source record identity, bytes and projection-relevant metadata.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### parent_record_id

Structural parent within the same job.

Optional. Null is rejected.

References [TransferRecord](TransferRecord.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### dependency_record_ids

Typed job record dependencies validated against the staging graph.

Required. Null is rejected.

References [TransferRecord](TransferRecord.md). Every referenced record belongs to this transfer job.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 2048,
  "minItems": 0,
  "uniqueItems": true
}
```

### target_kind

Authorized destination owner entity class.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### target_id

Canonical target identity in the registered owner domain.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_revision_id

Target immutable version or staged pointer.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### baseline_target_digest

Target fingerprint used in three-way comparison.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### disposition

Machine-produced coverage classification, review decision stored independently.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "equivalent",
    "mapped_with_loss",
    "intact_package",
    "external_dependency",
    "blocked",
    "unchanged",
    "retirement_candidate"
  ]
}
```

### projection_digest

Staged owner command projection fingerprint.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- References stay within the job graph or an explicit authorized external map.
- Protected drafts are not visible to learners.
- Every processed or blocked source object contributes to the reconciliation totals.

## Unique keys

- `id`
- `job_id, source_scope, object_kind, source_key, source_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, disposition | Build by-disposition transfer count. |
| target_kind, target_id | Reconcile a canonical object against source evidence. |

## Retention

Retain source and target fingerprints with job evidence. Expire private payloads under their own information class.
