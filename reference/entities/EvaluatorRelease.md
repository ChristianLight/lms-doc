# EvaluatorRelease

Approved typed worker implementation and request/response contract.

Owned by **assessment**.

## Fields

### id

Stable globally unique EvaluatorRelease identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### type_key

Registered evaluator or capability identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### version

Release ordinal for evaluator family.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### worker_digest

Immutable execution build digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### contract_digest

Request and response schema digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### approved_by

Service registry approver.

Required. Null is rejected.

References [Principal](Principal.md). Service registry approver.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_at

Evaluator activation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### deprecated_at

Cutoff for new publications.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revoked_at

Security cutoff blocking execution.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### max_cpu_ms

Maximum CPU milliseconds for one run.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### max_wall_ms

Maximum wall-clock milliseconds for one run.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### max_memory_bytes

Maximum resident memory.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647
}
```

## Integrity

- Deprecation does not revoke historical execution.
- Revocation blocks any new run and preserves sealed evidence.

## Unique keys

- `id`
- `type_key, version`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| type_key, revoked_at, version | Resolve approved evaluator build. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
