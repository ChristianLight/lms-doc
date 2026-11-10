# Attempt

One realized sitting or submission cycle for an enrollment or team.

Owned by **assessment**.

## Fields

### id

Stable globally unique Attempt identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Authorized offering-bound activity.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Authorized offering-bound activity.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Exact realized definition revision.

Required. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Exact realized definition revision.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Pinned policy for this delivery.

Required. Null is rejected.

References [DeliveryPolicyVersion](DeliveryPolicyVersion.md). Pinned policy for this delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### candidate_kind

Enrollment or frozen team participant.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "enrollment",
    "team"
  ]
}
```

### candidate_id

Stable Enrollment ID for individual work or stable LearningGroup ID for team work. Independent of versioned snapshots.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_id

Direct enrollment for individual sitting.

Optional. Nullable.

References [Enrollment](Enrollment.md). Direct enrollment for individual sitting.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### team_snapshot_id

Frozen team for group sitting.

Optional. Nullable.

References [TeamSnapshot](TeamSnapshot.md). Frozen team for group sitting.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Monotonic start ordinal per delivery and candidate.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### previous_attempt_id

Prior sitting for allowed retake or resubmission.

Optional. Nullable.

References [Attempt](Attempt.md). Prior sitting for allowed retake or resubmission.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Candidate lifecycle independent of marking state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "in_progress",
    "paused",
    "submitted",
    "expired",
    "abandoned",
    "voided"
  ]
}
```

### started_at

Authoritative start time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### deadline_at

Effective exclusive mutation cutoff.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### last_decision_at

Latest persisted admission time for nondecreasing timing.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### draft_version

Strong global draft and finalization validator.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### form_digest

Realized form and choice-order manifest hash.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### policy_snapshot_digest

Resolved policy, accommodation and deadline provenance.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### maximum

Total realized maximum on assessment scale.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### seed_key_version

Version of protected key used to derive randomized form seed.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### encrypted_seed_reference

Opaque protected seed storage reference.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### effective_policy

Captured time and authorized accommodations with no sensitive support context.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "opens_at": {
      "type": "string",
      "format": "date-time"
    },
    "due_at": {
      "type": "string",
      "format": "date-time"
    },
    "hard_close_at": {
      "type": "string",
      "format": "date-time"
    },
    "duration_seconds": {
      "type": "integer",
      "minimum": 1,
      "maximum": 604800
    },
    "pause_budget_seconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 3600
    },
    "applied_override_ids": {
      "type": "array",
      "items": {
        "type": "string",
        "format": "uuid"
      },
      "minItems": 0,
      "maxItems": 100
    },
    "alternate_version_id": {
      "type": "string",
      "format": "uuid"
    },
    "require_exam_grant": {
      "type": "boolean"
    }
  },
  "required": [
    "pause_budget_seconds",
    "applied_override_ids",
    "require_exam_grant"
  ],
  "additionalProperties": false
}
```

### active_section_key

Current allowed section where linear navigation applies.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### enrollment_release_id

Exact current offering course-version release pinned at individual start, null or omitted for a team.

Optional. Nullable.

References [EnrollmentRelease](EnrollmentRelease.md). Exact current offering course-version release pinned at individual start, null or omitted for a team.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Exact assessment placement within pinned release course version.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact assessment placement within pinned release course version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Exactly one of enrollment and team.
- At most one writable attempt per candidate and delivery.
- Submitted evidence is immutable.
- Individual attempt requires enrollment_release_id from the same Enrollment and offering. Team attempt uses one pinned release per frozen member.
- The exact ContentPlacement belongs to the CourseVersion of all captured EnrollmentRelease records and never changes after start.
- Rollout reserves compatible release state before changing any enrollment with uncertain or active launch.
- Team ordinal and writable-attempt uniqueness use stable LearningGroup ID. TeamSnapshot ID identifies the frozen version, never the quota identity.

## Unique keys

- `id`
- `delivery_id, candidate_kind, candidate_id, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, candidate_kind, candidate_id, state | Active sitting and historical attempts. |
| state, deadline_at | Indexed automatic expiry scan. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| in_progress | paused | PauseAssessmentAttempt | Policy grants pause within bound. Stop response edits and record pause start. |
| paused | in_progress | ResumeAssessmentAttempt | Policy and hard close still allow resumption. Compute capped duration deadline and renew writer lease. |
| in_progress | submitted | SubmitAssessmentAttempt | Authorized candidate finalizes matching acknowledged draft. Seal and issue one receipt. |
| in_progress | submitted | ExpireAssessmentAttempt | Deadline reached and auto submit policy. Seal last admitted responses. |
| paused | submitted | ExpireAssessmentAttempt | Hard close applies during pause and policy auto submits. Seal admitted responses. |
| in_progress | expired | ExpireAssessmentAttempt | Deadline reached and expiry-only policy. End writing with recorded disposition. |
| paused | expired | ExpireAssessmentAttempt | Hard close reached and expiry-only policy. End writing with recorded disposition. |
| in_progress | abandoned | AbandonAssessmentAttempt | Candidate authorized and policy permits abandonment. Preserve consumed ordinal and draft history. |
| submitted | voided | VoidAssessmentAttempt | Authorized incident disposition approves invalidation. Preserve receipt and emit voided grade evidence if applicable. |
