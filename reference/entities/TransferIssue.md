# TransferIssue

A classified transformation, validation or parity outcome requiring scoped review.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### job_id

Job producing the finding.

Required. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### record_id

Affected staged object when applicable.

Optional. Null is rejected.

References [TransferRecord](TransferRecord.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### issue_key

Stable evidence digest used to deduplicate retries.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### code

Machine-readable issue reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

### severity

Effect on stage and promotion.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "blocking",
    "warning",
    "information"
  ]
}
```

### safe_summary

Redacted summary for authorized review.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2000
}
```

### evidence_locator

Restricted evidence record locator.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### classification

Handling policy for underlying evidence.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "normal",
    "answer_protected",
    "personal",
    "security"
  ]
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "investigating",
    "accepted_difference",
    "resolved",
    "superseded"
  ]
}
```

### resolution_reason

Explicit acceptance or correction justification.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2000
}
```

### reviewer_principal_id

Actor responsible for this resolution.

Optional. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Blocking scoring loss cannot become an accepted difference without a verified replacement that changes the issue classification.
- Safe summaries exclude responses, tokens and unredacted scripts.

## Unique keys

- `id`
- `job_id, issue_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, severity, state | List unreviewed publication blockers. |

## Retention

Retain issue and review result for the life of the plan and associated publication. Expire sensitive raw evidence separately.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| open | accepted_difference | ResolveTransferIssue | Non-blocking issue has reviewed rationale and matching revision. Record actor and explicit loss. |
| open | resolved | ResolveTransferIssue | Verified correction validated against affected records. Queue scoped revalidation. |
