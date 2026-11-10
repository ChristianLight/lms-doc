# TranscriptRevision

Approved structured transcript snapshot and pinned academic record cutoff.

Owned by **records**.

## Fields

### id

Stable globally unique TranscriptRevision identifier.

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

### transcript_id

Stable transcript series for same learner.

Required. Null is rejected.

References [Transcript](Transcript.md). Stable transcript series for same learner.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### template_version_id

Published institution transcript template.

Required. Null is rejected.

References [TranscriptTemplateVersion](TranscriptTemplateVersion.md). Published institution transcript template.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### supersedes_id

Previous same-series revision, when replaced.

Required. Nullable.

References [TranscriptRevision](TranscriptRevision.md). Previous same-series revision, when replaced.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_release_entry_ids

Exact authorized final grade and correction pointers.

Required. Null is rejected.

References [GradeReleaseEntry](GradeReleaseEntry.md). Exact authorized final grade and correction pointers.

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

### credit_decision_ids

Approved institutional or transfer credit line revisions.

Required. Null is rejected.

References [CreditDecision](CreditDecision.md). Approved institutional or transfer credit line revisions.

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

### qualification_ids

Approved awards for this learner.

Required. Null is rejected.

References [QualificationDecision](QualificationDecision.md). Approved awards for this learner.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 1000,
  "minItems": 0,
  "uniqueItems": true
}
```

### gpa

Exact GPA ratio before display rounding.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### gpa_credit_units

Total credits contributing to GPA denominator.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### earned_credit_units

Total approved and deduplicated earned credits.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
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

- Final release entries only.
- GPA null when no GPA-eligible credits.
- Issued revision and artifact digest remain unchanged after correction.

## Unique keys

- `id`
- `transcript_id, revision`
- `transcript_id, snapshot_digest, input_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| transcript_id, state, revision | Find approved and historical transcript revisions. |
| person_id, issued_at | Find person transcript chronology. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| staged | ready | RenderAcademicDocument | Rendering succeeds on immutable input Stage usable outputs. |
| ready | issued | IssueTranscript | Authorized issuer and matching input digest Issue transcript and update series pointer. |
