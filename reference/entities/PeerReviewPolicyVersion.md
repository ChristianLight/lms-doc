# PeerReviewPolicyVersion

Immutable reviewer eligibility, anonymity and aggregation policy.

Owned by **assessment**.

## Fields

### id

Stable globally unique PeerReviewPolicyVersion identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Offering-bound delivery requiring peer review.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Offering-bound delivery requiring peer review.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rubric_version_id

Approved rubric pinned for all round assignments.

Required. Null is rejected.

References [RubricVersion](RubricVersion.md). Approved rubric pinned for all round assignments.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Policy revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### incoming_required

Minimum valid received reviews before graded aggregation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### outgoing_required

Requested outgoing tasks per reviewer.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### opens_at

Earliest assignment and reviewer opening.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### closes_at

Exclusive final review deadline.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### anonymous

Whether audience-specific anonymized projections are required.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### graded

Independent approval to use peer marks as scoring evidence.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### no_reciprocals

Whether opposite review edges are forbidden.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### digest

Allocation, eligibility and aggregation profile digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

## Integrity

- Formal graded mode defaults to at least three valid marks per assessed criterion.
- Missing reviews trigger staff fallback.

## Unique keys

- `id`
- `delivery_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, revision | Resolve pinned peer round policy. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
