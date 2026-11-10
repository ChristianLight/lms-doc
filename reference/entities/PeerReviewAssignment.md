# PeerReviewAssignment

Scoped reviewer access to one frozen candidate submission.

Owned by **assessment**.

## Fields

### id

Stable globally unique PeerReviewAssignment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### allocation_run_id

Frozen round assignment graph.

Required. Null is rejected.

References [PeerReviewAllocationRun](PeerReviewAllocationRun.md). Frozen round assignment graph.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reviewer_enrollment_id

Authorized reviewer in the offering and selected audience.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Authorized reviewer in the offering and selected audience.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Sealed work eligible under the same round.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Sealed work eligible under the same round.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pseudonym

Opaque audience-specific label.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### state

Stored assignment workflow state or derived expiry at due_at while still invited or opened.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "invited",
    "opened",
    "submitted",
    "revoked",
    "expired"
  ]
}
```

### due_at

Exclusive review cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### write_version

Optimistic review draft version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### replaces_id

Optional revoked assignment whose coverage is replaced.

Optional. Nullable.

References [PeerReviewAssignment](PeerReviewAssignment.md). Optional revoked assignment whose coverage is replaced.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- No self, same-team or unauthorized edge.
- Anonymity projection omits source identity.

## Unique keys

- `id`
- `allocation_run_id, reviewer_enrollment_id, submission_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| reviewer_enrollment_id, state, due_at | List assigned reviewer tasks. |
| submission_id, state | Assess incoming review coverage. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| invited | opened | OpenPeerReview | Reviewer maintains active scoped eligibility. Expose sanitized evidence and start draft. |
| opened | submitted | SubmitPeerReview | Exact eligible draft and rubric received before deadline. Seal review revision and route moderation. |
| invited | revoked | ReplacePeerReview | Coordinator documents unavailability. Withdraw access and allocate replacement or staff fallback. |
| opened | revoked | ReplacePeerReview | Coordinator documents unavailability. Withdraw access and preserve draft audit. |
