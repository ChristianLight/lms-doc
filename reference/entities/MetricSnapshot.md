# MetricSnapshot

Immutable aggregate or restricted report projection with reproducible lineage.

Owned by **records**.

## Fields

### id

Stable globally unique MetricSnapshot identifier.

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

### definition_version_id

Exact report algorithm and privacy defaults.

Required. Null is rejected.

References [MetricDefinitionVersion](MetricDefinitionVersion.md). Exact report algorithm and privacy defaults.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Scoped offering if selected.

Required. Nullable.

References [CourseOffering](CourseOffering.md). Scoped offering if selected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### academic_period_id

Scoped academic period if selected.

Required. Nullable.

References [AcademicPeriod](AcademicPeriod.md). Scoped academic period if selected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### cutoff_at

Academic snapshot cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### source_vector

Ordered producer checkpoint vector.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "producer": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9._-]{0,63}$"
      },
      "partition": {
        "type": "string",
        "minLength": 1,
        "maxLength": 128
      },
      "sequence": {
        "type": "integer",
        "minimum": 0,
        "maximum": 9007199254740991
      },
      "digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      }
    },
    "required": [
      "producer",
      "partition",
      "sequence",
      "digest"
    ],
    "additionalProperties": false
  },
  "maxItems": 4096,
  "minItems": 0
}
```

### scope_digest

Canonical caller-authorized filter and reporting purpose digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### output_digest

Canonical redacted report output digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### data_storage_id

Protected report cells or references.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Protected report cells or references.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### coverage

Source coverage quality.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "complete",
    "partial",
    "unavailable"
  ]
}
```

### population_count

Authorized unique person population before suppression.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000000
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

- No snapshot downloadable after caller scope revoked.
- Suppression applies equally to visible and exported data.

## Unique keys

- `id`
- `definition_version_id, scope_digest, cutoff_at, output_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, definition_version_id, created_at | Find approved scoped reports. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.
