# Assessment

Stable identity and publication head for an assessment.

Owned by **assessment**.

## Fields

### id

Stable globally unique Assessment identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning assessment.

Required. Null is rejected.

References [Institution](Institution.md). Institution owning assessment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_id

Course owning native assessment definition.

Required. Null is rejected.

References [Course](Course.md). Course owning native assessment definition.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### title

Authoring and candidate title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### created_by

Scoped assessment author.

Required. Null is rejected.

References [Principal](Principal.md). Scoped assessment author.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### published_version_id

Current published revision of this Assessment.

Optional. Nullable.

References [AssessmentVersion](AssessmentVersion.md). Current published revision of this Assessment.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- An offering-specific delivery holds release dates and membership, not this definition.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_id, created_at | Scope authoring inventory. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
