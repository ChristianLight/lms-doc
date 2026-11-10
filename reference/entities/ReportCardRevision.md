# ReportCardRevision

Immutable report card snapshot staged for rendering and issuance.

Owned by **records**.

## Fields

### id

Stable globally unique ReportCardRevision identifier.

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

### report_card_id

Stable series for same learner and academic period.

Required. Null is rejected.

References [ReportCard](ReportCard.md). Stable series for same learner and academic period.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### template_version_id

Pinned approved report-card template.

Required. Null is rejected.

References [ReportTemplateVersion](ReportTemplateVersion.md). Pinned approved report-card template.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Previous same-series report card, if any.

Required. Nullable.

References [ReportCardRevision](ReportCardRevision.md). Previous same-series report card, if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_release_entry_ids

Authorized released grades in report period.

Required. Null is rejected.

References [GradeReleaseEntry](GradeReleaseEntry.md). Authorized released grades in report period.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 2048,
  "minItems": 0,
  "uniqueItems": true
}
```

### comment_revision_ids

Approved exact comment revisions.

Required. Null is rejected.

References [AcademicCommentRevision](AcademicCommentRevision.md). Approved exact comment revisions.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 500,
  "minItems": 0,
  "uniqueItems": true
}
```

### attendance_revision_ids

Approved attendance source pointers.

Required. Null is rejected.

References [AttendanceRevision](AttendanceRevision.md). Approved attendance source pointers.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 5000,
  "minItems": 0,
  "uniqueItems": true
}
```

### revision

Monotonic immutable revision number within its stable identity.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
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

### state

Rendering and issuance state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "render_failed",
    "ready",
    "issued",
    "superseded",
    "void"
  ],
  "default": "staged"
}
```

### cutoff_at

Exact academic cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### input_digest

Pinned approved source references and scope digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### snapshot_digest

Canonical structured document content digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### snapshot_storage_id

Protected immutable canonical snapshot bytes inside institution.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Protected immutable canonical snapshot bytes inside institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### locale

Approved document locale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9-]+$"
}
```

### render_version

Renderer contract and layout algorithm version.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### issued_by

Approver with authority to issue this document.

Required. Nullable.

References [Principal](Principal.md). Approver with authority to issue this document.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### issued_at

Recorded official issuance timestamp.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### verification_key_digest

Digest of opaque verification code if enabled.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### classification

Maximum allowed disclosure.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "internal",
    "private",
    "recipient_restricted"
  ],
  "default": "private"
}
```

## Integrity

- Issued snapshot bytes cannot change.
- Only permitted released grade pointers qualify.

## Unique keys

- `id`
- `report_card_id, revision`
- `report_card_id, snapshot_digest, input_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| report_card_id, state, revision | Find working and current issued revisions. |
| person_id, issued_at | Find historical learner reports. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | ready | RenderAcademicDocument | Rendered artifacts verified and digest matches Stage authorized accessible artifact. |
| ready | issued | IssueReportCard | Current scope and input guard match Issue report and update series pointer. |
