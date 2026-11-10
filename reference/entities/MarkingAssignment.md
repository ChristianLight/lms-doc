# MarkingAssignment

Authorized staff scope for reviewing one exact item and submission.

Owned by **assessment**.

## Fields

### id

Stable globally unique MarkingAssignment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Exact realized item.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Exact realized item.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### submission_id

Sealed submission of same attempt.

Required. Null is rejected.

References [AttemptSubmission](AttemptSubmission.md). Sealed submission of same attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### marker_id

Scoped eligible staff assignment or null for open claim.

Optional. Nullable.

References [Principal](Principal.md). Scoped eligible staff assignment or null for open claim.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### blind_code

Opaque candidate label under moderation policy.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### marking_pass

Independent marking pass ordinal.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### state

Open, assigned, submitted, revoked or expired.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "open",
    "assigned",
    "submitted",
    "revoked",
    "expired"
  ]
}
```

### due_at

Review queue target.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### write_version

Assignment and draft concurrency version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### current_draft_digest

Protected marker-attributed draft head for scope and concurrency.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### current_draft_id

Current private draft revision for the exact still assigned marker.

Optional. Nullable.

References [MarkDraftRevision](MarkDraftRevision.md). Current private draft revision for the exact still assigned marker.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Multiple passes require distinct markers when independent.
- Scope grants are rechecked on every read and write.

## Unique keys

- `id`
- `attempt_item_id, marking_pass`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| marker_id, state, due_at | Marker queue and overdue work. |
| attempt_item_id, state | Resolve independent moderation inputs. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| open | assigned | ClaimMarkingAssignment | Eligible staff claims exact open task. Record marker and advance version. |
| assigned | submitted | SubmitItemMark | Assigned marker and compatible frozen rubric. Append provisional immutable ItemMarkRevision. |
| assigned | open | ReassignMarkingAssignment | Coordinator authorizes reassignment. Preserve previous draft and revoke prior access. |
| assigned | assigned | ReassignMarkingAssignment | Coordinator names a qualified replacement within scope. Withdraw former access and bind the new marker. Retain independently attributed draft snapshots. |
