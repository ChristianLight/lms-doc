# Transcript

Stable learner transcript series per institutional profile.

Owned by **records**.

## Fields

### id

Stable globally unique Transcript identifier.

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

### profile_code

Named approved transcript series profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### current_revision_id

Current issued revision in this series.

Required. Nullable.

References [TranscriptRevision](TranscriptRevision.md). Current issued revision in this series.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pointer_version

Optimistic current document pointer version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
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

- Issuing to an external recipient requires current authorized purpose.

## Unique keys

- `id`
- `person_id, profile_code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, profile_code | Find transcript series by permitted profile. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
