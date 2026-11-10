# PackageRuntimeElement

Edition-validated value for one runtime element path in an occurrence snapshot.

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

### sco_state_id

Current occurrence snapshot.

Required. Null is rejected.

References [PackageScoState](PackageScoState.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### element_key

Canonical data model name including validated indexes.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### value

Current raw lexical value with edition and SPM validation.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 65536
}
```

### commit_id

Durable commit that last changed this value.

Required. Null is rejected.

References [PackageCommit](PackageCommit.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### classification

Runtime value access and redaction class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "normal",
    "learner_response",
    "private_state",
    "identity"
  ]
}
```

### element_type

Pinned edition vocabulary or scalar type used by validator.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

## Integrity

- Write-only at the SCO interface does not mean value is absent internally.
- Do not leak protected values into telemetry or gradebook events.

## Unique keys

- `id`
- `sco_state_id, element_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| sco_state_id, classification | Apply privileged export filtering and restore exact state. |

## Retention

Follow occurrence retention. Raw learner responses and suspend data require stricter access and can expire independently under approved policy.
