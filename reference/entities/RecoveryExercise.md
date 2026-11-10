# RecoveryExercise

Approved recovery test or incident reconciliation with protected evidence.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### environment_key

Approved infrastructure environment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### backup_set_ref

Immutable signed recovery manifest reference.

Required. Null is rejected.

References [BackupSet](BackupSet.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_time

Requested recovery point.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### actual_restore_time

Verified durable record horizon.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### rpo_seconds

Maximum acceptable age of data loss target.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 86400
}
```

### rto_seconds

Maximum restoration service downtime target.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 604800
}
```

### started_at

Exercise start time.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reopened_at

Verified service reopening or simulated equivalent.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### evidence_ref

Protected restore checklist and integrity evidence.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "planned",
    "restoring",
    "verifying",
    "passed",
    "failed"
  ]
}
```

## Integrity

- Reconnect delivery systems only after fencing old writers, replaying revocations and dispositions, and verifying integrity.
- Passing requires measured RPO and RTO, application-level integrity and an independent verification sign-off.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, environment_key, created_at | Find last tested recovery capability |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| planned | restoring | RecordRecoveryMilestone | Operator selects an approved backup manifest and fenced environment Start recovery timing. |
| restoring | verifying | RecordRecoveryMilestone | Database and asset versions restored to compatible horizon Run verification without enabling public access. |
| verifying | passed | RecordRecoveryMilestone | Independent approver accepts all checks and numerical objectives Open eligible service or mark simulation passed. |
| restoring | failed | RecordRecoveryMilestone | Restore or manifest integrity check fails Keep traffic disabled and record discrepancy. |
| verifying | failed | RecordRecoveryMilestone | Recovery objectives or consistency checks fail Keep traffic disabled and preserve evidence. |
