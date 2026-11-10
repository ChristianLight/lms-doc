# RegradeJob

Approved scope, dry-run manifest and correction lifecycle.

Owned by **assessment**.

## Fields

### id

Stable globally unique RegradeJob identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Offering-scoped correction target.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Offering-scoped correction target.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_rule_version_id

Exact scoring rule originally applied in affected population.

Required. Null is rejected.

References [MarkingRuleVersion](MarkingRuleVersion.md). Exact scoring rule originally applied in affected population.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### replacement_rule_version_id

Approved compatible correction rule.

Required. Null is rejected.

References [MarkingRuleVersion](MarkingRuleVersion.md). Approved compatible correction rule.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### preview_digest

Stable exact regrade population and computed effects.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### proposed_by

Scoped requester.

Required. Null is rejected.

References [Principal](Principal.md). Scoped requester.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_by

Independent approver where required.

Optional. Nullable.

References [Principal](Principal.md). Independent approver where required.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Preparation, preview, approved execution and final state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "planned",
    "previewed",
    "approved",
    "running",
    "completed",
    "stopped"
  ]
}
```

### allow_decrease

Whether approved policy permits decreasing previously released evidence.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### preserve_manual_overrides

Protect separately accepted manual decisions.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### reason

Why the correction is requested.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### counts

Reconciliation counters by case disposition.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "planned": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    },
    "changed": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    },
    "unchanged": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    },
    "excluded": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    },
    "conflicted": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    },
    "failed": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2147483647
    }
  },
  "required": [
    "planned",
    "changed",
    "unchanged",
    "excluded",
    "conflicted",
    "failed"
  ],
  "additionalProperties": false
}
```

## Integrity

- Approval pins the dry-run digest.
- A conflict never overwrites an intervening adjudication.
- Abort never rolls back completed judgments.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, state | Find active or historical correction batches. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| planned | previewed | PreviewAssessmentRegrade | Exact eligible scope and rules are available. Freeze candidate and case preview. |
| previewed | approved | ApproveAssessmentRegrade | Approver confirms unchanged digest and institutional rules. Authorize sealed correction plan. |
| approved | running | RunAssessmentRegrade | Worker receives durable approved job. Process idempotent cases against original heads. |
| running | completed | FinishAssessmentRegrade | All cases have terminal dispositions. Seal reconciliation summary. |
| running | stopped | StopAssessmentRegrade | Authorized operator requests stop. Prevent new cases and preserve accepted work. |
