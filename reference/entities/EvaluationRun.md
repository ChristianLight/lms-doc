# EvaluationRun

Durable worker execution fact over exact sealed evidence.

Owned by **assessment**.

## Fields

### id

Stable globally unique EvaluationRun identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Realized candidate item eligible for evaluation.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Realized candidate item eligible for evaluation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Sealed evidence for same attempt.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Sealed evidence for same attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evaluator_release_id

Approved worker build.

Required. Null is rejected.

References [EvaluatorRelease](EvaluatorRelease.md). Approved worker build.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### marking_rule_version_id

Protected rule for this execution.

Required. Null is rejected.

References [MarkingRuleVersion](MarkingRuleVersion.md). Protected rule for this execution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### input_digest

Exact grading inputs and pinned dependencies.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### purpose

Initial, regrade, appeal or private preview purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "initial",
    "regrade",
    "preview",
    "appeal"
  ]
}
```

### run_revision

Intentional run revision independent of retries.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### state

Durable worker lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "leased",
    "retry_wait",
    "scored",
    "manual_review",
    "failed"
  ]
}
```

### execution_count

Number of leases issued.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647
}
```

### lease_id

Opaque active worker lease.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### lease_expires_at

Exclusive current lease cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### retry_at

Next permitted claim time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### outcome

Verified worker response class.

Optional. Nullable.

```json
{
  "type": "string",
  "enum": [
    "scored",
    "invalid_response",
    "manual_review",
    "retryable_error",
    "terminal_error"
  ]
}
```

### result_digest

Canonical verified output digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### safe_error_code

Allowlisted operational diagnostic.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### result_criteria

Verified typed criterion outcomes when accepted.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "criterion_key": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      },
      "points": {
        "type": "string",
        "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
      },
      "maximum": {
        "type": "string",
        "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
      },
      "disposition": {
        "type": "string",
        "enum": [
          "scored",
          "blank",
          "invalid",
          "manual_review",
          "excused"
        ]
      },
      "feedback_code": {
        "type": "string",
        "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
      }
    },
    "required": [
      "criterion_key",
      "maximum",
      "disposition"
    ],
    "additionalProperties": false
  },
  "minItems": 0,
  "maxItems": 64
}
```

### started_at

Authoritative first worker claim time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### completed_at

Accepted terminal completion time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Accept result only for active lease, digest, approved scorer and bounded schema.
- Error stays pending or review, never becomes zero by itself.

## Unique keys

- `id`
- `attempt_item_id, input_digest, purpose, run_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| state, retry_at | Find ready grading work. |
| state, lease_expires_at | Recover abandoned worker leases. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| queued | leased | ClaimEvaluationRun | Approved worker and available exact job. Assign lease and increment execution count. |
| retry_wait | leased | ClaimEvaluationRun | Retry time reached with retry budget. Assign new lease and increment execution count. |
| leased | scored | CompleteEvaluationRun | Active lease and verified scored output. Freeze result digest. |
| leased | manual_review | CompleteEvaluationRun | Valid indeterminate or authorized manual outcome. Create review work. |
| leased | retry_wait | CompleteEvaluationRun | Retryable fault and remaining budget. Schedule capped retry. |
| leased | failed | CompleteEvaluationRun | Unrecoverable run or exhausted retries. Create protected exception work. |
| leased | retry_wait | RecoverEvaluationLease | Lease expired without accepted result. Close lease and requeue with configured backoff. |
| leased | failed | RecoverEvaluationLease | Lease expired without accepted result and retry budget is exhausted. Close the expired lease and record technical exception review. |
