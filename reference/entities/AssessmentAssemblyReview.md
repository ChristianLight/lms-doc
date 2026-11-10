# AssessmentAssemblyReview

Independent approval of exact assembly and feasible scorer dependencies.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentAssemblyReview identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Version owned by reviewed course scope.

Required. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Version owned by reviewed course scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_digest

Exact reviewed draft and pinned dependency graph.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### fixtures_digest

Checked form selection, scoring, renderer and locale evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### reviewer_id

Authorized reviewer, independent from authors where policy requires.

Required. Null is rejected.

References [Principal](Principal.md). Authorized reviewer, independent from authors where policy requires.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### decision

Approve, reject or request review changes.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "approve",
    "reject",
    "needs_work"
  ]
}
```

### reason

Protected explanation and unmet requirements.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### decided_at

Authoritative decision time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Any content or validation dependency digest change invalidates prior publication approval.
- Approval does not publish.

## Unique keys

- `id`
- `assessment_version_id, content_digest, reviewer_id, decided_at`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assessment_version_id, content_digest, decision | Find exact current publication approval. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
