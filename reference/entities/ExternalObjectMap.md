# ExternalObjectMap

Stable crosswalk between one source namespace and one canonical owner object.

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

### source_namespace

Registered and verified authoritative source.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### source_scope

Stable source parent scope or root sentinel.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### object_kind

Registered mapped canonical type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### external_key

Exact source identifier retained as an opaque value.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### target_kind

Canonical owner entity type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### target_id

Canonical owner entity UUID, validated via owner adapter.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### last_source_revision

Most recent approved source version.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### last_source_fingerprint

Canonical fingerprint of the most recent approved source input.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### last_target_fingerprint

Fingerprint of the target at last successful promotion.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### last_job_id

Successful transfer receipt that established this baseline.

Required. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "retired",
    "merge_pending"
  ]
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

### updated_at

Last authoritative mapping update.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Crosswalk updates require source authority and matching target baseline.
- Multiple aliases may identify one native object, but one source tuple cannot identify multiple current targets.

## Unique keys

- `id`
- `institution_id, source_namespace, source_scope, object_kind, external_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, target_kind, target_id | Find reverse provenance for an owner object. |

## Retention

Keep active aliases while referenced. Keep retirement tombstones to prevent source ID reuse for seven years by default.
