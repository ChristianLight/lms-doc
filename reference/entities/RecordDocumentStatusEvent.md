# RecordDocumentStatusEvent

Append-only issued document state and public verification effect.

Owned by **records**.

## Fields

### id

Stable globally unique RecordDocumentStatusEvent identifier.

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

Scoped report revision when applicable.

Required. Nullable.

References [ReportCardRevision](ReportCardRevision.md). Scoped report revision when applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### transcript_revision_id

Scoped transcript revision when applicable.

Required. Nullable.

References [TranscriptRevision](TranscriptRevision.md). Scoped transcript revision when applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### event_kind

Issuance or correction status event.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "issued",
    "superseded",
    "voided"
  ]
}
```

### effective_at

Effective document status time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason

Restricted correction rationale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
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

- Exactly one document parent.
- Never replace old artifact content for same verification identifier.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| report_revision_id, effective_at | Resolve report verification status. |
| transcript_revision_id, effective_at | Resolve transcript verification status. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
