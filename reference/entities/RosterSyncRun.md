# RosterSyncRun

Staged full or incremental feed with provenance and checksum.

Owned by **participation**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Source institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Registered feed source.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### scope_key

Verified feed partition and coverage.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### sequence

Monotonic source sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### digest

Verified feed bytes.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### mode

Reconciliation semantics.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "full",
    "incremental"
  ]
}
```

### complete

Provider verifies full partition coverage.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### state

Feed lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "validated",
    "applied",
    "partial",
    "failed"
  ],
  "default": "staged"
}
```

### staged_at

Accepted preflight instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Incomplete or failed full feed cannot revoke unseen grants.

## Unique keys

- `id`
- `institution_id, source_namespace, scope_key, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, source_namespace, scope_key, state, sequence | Read feed checkpoint and queued reconciliation. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
