# RegradeCase

Per-attempt plan and authoritative batch outcome.

Owned by **assessment**.

## Fields

### id

Stable globally unique RegradeCase identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### job_id

Approved parent regrade scope.

Required. Null is rejected.

References [RegradeJob](RegradeJob.md). Approved parent regrade scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Attempt in job delivery.

Required. Null is rejected.

References [Attempt](Attempt.md). Attempt in job delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### input_digest

Frozen original sealed evidence and accepted mark heads.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### expected_mark_revision_ids

CAS heads used in preview.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). CAS heads used in preview.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

### old_points

Original accepted score for comparison.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### proposed_points

Dry-run candidate value where available.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### disposition

Verified preview and case status.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### result_mark_ids

Committed corrections scoped to same attempt.

Required. Null is rejected.

References [ItemMarkRevision](ItemMarkRevision.md). Committed corrections scoped to same attempt.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "minItems": 0,
  "maxItems": 1000
}
```

## Integrity

- A case mutates results at most once per approved input fingerprint.

## Unique keys

- `id`
- `job_id, attempt_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, disposition | Track partial progress and reconciliation. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
