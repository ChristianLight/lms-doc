# AssessmentBranchDecision

Immutable authorized route choice from a sealed section boundary.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentBranchDecision identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Exact active practice attempt that allows conditional routing.

Required. Null is rejected.

References [Attempt](Attempt.md). Exact active practice attempt that allows conditional routing.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### from_section_key

Resolved origin section in pinned assessment.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### route_revision

Positive sequence for candidate progression.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### response_manifest_digest

Sealed subset of acknowledged response heads for predecessor section.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### rule_key

Pinned reviewed branch rule and fallback profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### status

Resolved, pending or blocked route.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "resolved",
    "pending",
    "blocked"
  ]
}
```

### target_section_key

Resolved next approved section when successful.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### effective_at

Authoritative route evaluation or decision time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- No cycles.
- A resolved route survives reload, reevaluation and correction.
- Evaluator unavailability never implies an incorrect answer.

## Unique keys

- `id`
- `attempt_id, from_section_key, route_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_id, route_revision | Resume exact determined route. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
