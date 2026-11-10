# BackupSet

Protected manifest of a verified restorable database, object and event horizon.

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

### environment_key

Approved environment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### base_set_ref

Base backup ID for dependent change coverage.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### application_version

Exact deployed application build.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### schema_version

Exact database migration version.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### data_horizon

Verified point-in-time record coverage.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### object_horizon

Compatible retained object-version horizon.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### inventory_digest

Canonical digest of object inventory and base manifest.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### audit_anchor_ref

Restricted trusted audit anchor at this horizon.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### event_checkpoint_ref

Durable event and consumer checkpoint inventory.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### encryption_key_version_ref

Opaque custodian version reference.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._/-]*$"
}
```

### manifest_digest

Canonical signed manifest digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### manifest_signature_ref

Restricted signature and signer evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### retire_after

Scheduled rotation threshold subject to dependent sets and holds.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "captured",
    "verified",
    "invalid",
    "retired"
  ]
}
```

## Integrity

- No set becomes verified without valid signature, compatible database and object horizon, available key and verified coverage chain.
- Do not retire a still required base or held manifest. An exercise records restore success separately.

## Unique keys

- `id`
- `institution_id, environment_key, manifest_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, environment_key, state, data_horizon | Find verified recovery coverage and prior base backups |

## Retention

35 days by default for protected daily generation, subject to dependency chain and holds.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| captured | verified | VerifyBackupSet | Manifest custody and coverage checks pass Register eligible backup set. |
| captured | invalid | VerifyBackupSet | Signature, horizon or key availability check fails Keep evidence and disallow recovery use. |
| verified | invalid | VerifyBackupSet | Subsequent verification detects incomplete coverage or lost key Alert operators and block automatic restore selection. |
| verified | retired | RetireBackupSet | Coverage and hold checks allow retirement Remove set from eligible restore inventory. |
