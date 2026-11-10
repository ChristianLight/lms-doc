# ActivityVersion

Immutable type contract and exact runtime dependency bindings.

Owned by **curriculum**.

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

### activity_id

Stable activity.

Required. Null is rejected.

References [Activity](Activity.md). Must resolve to an authorized Activity in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### payload

Type-specific locale instructions and configuration.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "type_key": {
      "type": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
    },
    "schema_version": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    },
    "default_locale": {
      "type": "string",
      "minLength": 2,
      "maxLength": 35,
      "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
    },
    "variants": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "locale": {
            "type": "string",
            "minLength": 2,
            "maxLength": 35,
            "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
          },
          "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 240
          },
          "body": {
            "type": "object",
            "maxProperties": 64
          },
          "review_state": {
            "type": "string",
            "enum": [
              "draft",
              "approved",
              "stale"
            ]
          },
          "source_digest": {
            "type": "string",
            "pattern": "^[0-9a-f]{64}$"
          }
        },
        "required": [
          "locale",
          "title",
          "body",
          "review_state"
        ],
        "additionalProperties": false
      },
      "maxItems": 60,
      "minItems": 1
    }
  },
  "required": [
    "type_key",
    "schema_version",
    "default_locale",
    "variants"
  ],
  "additionalProperties": false
}
```

### digest

Canonical payload and dependencies digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### assessment_version_id

Required for native assessment types.

Optional. Nullable.

References [AssessmentVersion](AssessmentVersion.md). Must resolve to an authorized AssessmentVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### package_version_id

Required for packaged activity.

Optional. Nullable.

References [PackageVersion](PackageVersion.md). Must resolve to an authorized PackageVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### signals

Declared evidence signal keys.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
  },
  "maxItems": 32,
  "minItems": 0
}
```

### created_by

Sealing actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Sealed instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Kind selects exactly one registered runtime.
- Attempts and scores never reside in this payload.

## Unique keys

- `id`
- `activity_id, revision`
- `activity_id, digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| assessment_version_id | Assessment version impact. |
| package_version_id | Package version impact. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.
