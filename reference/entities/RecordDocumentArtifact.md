# RecordDocumentArtifact

Immutable accessible file generated from an exact academic document snapshot.

Owned by **records**.

## Fields

### id

Stable globally unique RecordDocumentArtifact identifier.

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

Report card origin, required for a report artifact.

Required. Nullable.

References [ReportCardRevision](ReportCardRevision.md). Report card origin, required for a report artifact.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### transcript_revision_id

Transcript origin, required for a transcript artifact.

Required. Nullable.

References [TranscriptRevision](TranscriptRevision.md). Transcript origin, required for a transcript artifact.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### asset_version_id

Protected immutable artifact version in same institution.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Protected immutable artifact version in same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### mime_type

Approved output representation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "text/html",
    "application/pdf",
    "application/json",
    "application/xml"
  ]
}
```

### digest

Output byte SHA-256 digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### size_bytes

File size for validation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### accessible_verified

Artifact passed required accessibility validation.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
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
- Use concrete partial uniqueness for nullable parents.
- Official download rechecks current recipient authorization.

## Unique keys

- `id`
- `report_revision_id, transcript_revision_id, mime_type, digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| report_revision_id, mime_type | Find permitted report artifact. |
| transcript_revision_id, mime_type | Find permitted transcript artifact. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
