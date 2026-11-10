# AttemptLease

Scoped writer admission token for one attempt and device or team editor.

Owned by **assessment**.

## Fields

### id

Stable globally unique AttemptLease identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Active attempt target.

Required. Null is rejected.

References [Attempt](Attempt.md). Active attempt target.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### principal_id

Authenticated authorized editor.

Required. Null is rejected.

References [Principal](Principal.md). Authenticated authorized editor.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### lease_revision

Monotonic writer session revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### issued_at

Creation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive validity cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### revoked_at

Explicit takeover or access revocation.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Taking over a formal sitting revokes the prior writer.
- No lease bypasses current authorization or deadline.

## Unique keys

- `id`
- `attempt_id, principal_id, lease_revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_id, revoked_at, expires_at | Check active writer lease under attempt lock. |

## Retention

Retain token fingerprints and operation history through the appeal period.
