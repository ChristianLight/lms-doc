# RosterSyncRow

Validated source row and resulting LMS decision.

Owned by **participation**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### roster_sync_run_id

Batch owner.

Required. Null is rejected.

References [RosterSyncRun](RosterSyncRun.md). Must resolve to an authorized RosterSyncRun in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### row_number

Physical or logical source order.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000000
}
```

### external_grant_key

Stable external enrollment identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### source_person_key

Source identity, never email fallback.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### person_id

Verified local person.

Optional. Nullable.

References [Person](Person.md). Must resolve to an authorized Person in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Resolved offering.

Optional. Nullable.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### operation

Explicit source change.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "upsert",
    "end"
  ]
}
```

### state

Row disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "ready",
    "applied",
    "unresolved",
    "rejected"
  ]
}
```

### reason_code

Machine reason.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

## Integrity

- No implicit account match.

## Unique keys

- `id`
- `roster_sync_run_id, row_number`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| roster_sync_run_id, state | Issues and eligible row batch. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
