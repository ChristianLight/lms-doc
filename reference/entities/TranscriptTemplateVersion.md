# TranscriptTemplateVersion

Versioned transcript presentation and approved field choices.

Owned by **records**.

## Fields

### id

Stable globally unique TranscriptTemplateVersion identifier.

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

### template_key

Stable transcript template family.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
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

### name

Internal template display name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 160
}
```

### state

Template publication state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "superseded",
    "retired"
  ],
  "default": "draft"
}
```

### layout

Versioned structural fields and output language.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "include_grade_legend": {
      "type": "boolean"
    },
    "include_attendance": {
      "type": "boolean"
    },
    "include_comments": {
      "type": "boolean"
    },
    "include_competencies": {
      "type": "boolean"
    },
    "include_gpa": {
      "type": "boolean"
    },
    "include_program_awards": {
      "type": "boolean"
    },
    "heading": {
      "type": "string",
      "minLength": 1,
      "maxLength": 180
    },
    "document_language": {
      "type": "string",
      "minLength": 2,
      "maxLength": 35,
      "pattern": "^[A-Za-z0-9-]+$"
    }
  },
  "required": [
    "include_grade_legend",
    "include_attendance",
    "include_comments",
    "include_competencies",
    "include_gpa",
    "include_program_awards",
    "heading",
    "document_language"
  ],
  "additionalProperties": false
}
```

### publication_digest

Approved template and renderer contract digest.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
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

### published_at

Publication time.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Cannot enable a field disallowed for this audience or template class.
- Publishing freezes approved template fields and layout.

## Unique keys

- `id`
- `institution_id, template_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, template_key | Find approved templates for issuing records. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishTranscriptTemplate | Authorized template reviewed and purpose validation succeeds Freeze layout and publication digest. |
