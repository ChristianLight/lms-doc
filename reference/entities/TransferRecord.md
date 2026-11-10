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

### plan_revision

Immutable transfer plan revision that owns this candidate record. Never resolves against a newer plan implicitly.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
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

### source_layer

Independent source publication layer. Shared definitions have no draft or published-only selector.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "published",
    "draft",
    "shared"
  ]
}
```

### record_role

Semantic source occurrence role. Reusable definitions and placements always have separate records.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "definition",
    "placement",
    "asset",
    "policy",
    "reference",
    "package",
    "document"
  ]
}
```

### occurrence_key

Stable source-scoped occurrence disambiguator. Use defined sentinel definition for a single non-occurrence record. An ambiguous move or reorder requires review.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### reachability

Classification in the frozen selected root dependency closure. Detached and outside-selection rows do not certify publishability.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "selected_required",
    "selected_optional",
    "detached",
    "outside_selection"
  ]
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
- A record and its typed TransferEdge relationships are immutable within a plan revision. Plan correction appends another revision.
- An opaque source key is not a native UUID. Allocation uses approved scoped identity and occurrence, never a raw hexadecimal token or archive path.
- Required selected reachability with an unresolved blocking issue prohibits promotion of the dependent root. Detached and outside-selection records remain in restricted inventory.

## Unique keys

- `id`
- `job_id, plan_revision, source_scope, object_kind, source_key, source_layer, record_role, occurrence_key, source_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, disposition | Build by-disposition transfer count. |
| target_kind, target_id | Reconcile a canonical object against source evidence. |
| job_id, plan_revision, reachability, disposition | Reconcile selected roots and detached issue counts without mixing plan generations. |

## Retention

Retain source and target fingerprints with job evidence. Expire private payloads under their own information class.
