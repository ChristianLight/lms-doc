# RecordDisclosureRequest

Purpose-scoped approval and delivery request for an academic document.

Owned by **records**.

## Fields

### id

Stable globally unique RecordDisclosureRequest identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Educational identity within the same institution.

Required. Null is rejected.

References [Person](Person.md). Educational identity within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### report_revision_id

Requested report revision, if chosen.

Required. Nullable.

References [ReportCardRevision](ReportCardRevision.md). Requested report revision, if chosen.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### transcript_revision_id

Requested transcript revision, if chosen.

Required. Nullable.

References [TranscriptRevision](TranscriptRevision.md). Requested transcript revision, if chosen.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### destination

Approved institutional recipient identifier or self-access code.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 320
}
```

### purpose

Authorized disclosure purpose.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "self",
    "transfer",
    "admission",
    "employer",
    "authorized_other"
  ]
}
```

### state

Disclosure workflow.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "requested",
    "approved",
    "delivered",
    "denied",
    "expired",
    "revoked"
  ],
  "default": "requested"
}
```

### requested_by

Authenticated learner, delegate or registrar.

Required. Null is rejected.

References [Principal](Principal.md). Authenticated learner, delegate or registrar.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approved_by

Authorized approver or null before decision.

Required. Nullable.

References [Principal](Principal.md). Authorized approver or null before decision.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expires_at

Exclusive approved delivery expiry.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Current authorization at generation and download.
- Exactly one document reference after approval.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, state, created_at | Find learner and registrar disclosure requests. |
| state, expires_at | Expire pending download permissions. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | approved | DecideRecordDisclosure | Purpose and recipient authorized Grant bounded recipient disclosure. |
| approved | delivered | DeliverRecordDisclosure | Grant remains valid Record recipient-specific delivery. |
