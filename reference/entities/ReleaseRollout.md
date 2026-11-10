# ReleaseRollout

Authorized source-to-target publication and cohort snapshot.

Owned by **participation**.

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

### offering_id

Owning delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_course_version_id

Exact source version.

Required. Null is rejected.

References [CourseVersion](CourseVersion.md). Must resolve to an authorized CourseVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_course_version_id

Exact target version.

Required. Null is rejected.

References [CourseVersion](CourseVersion.md). Must resolve to an authorized CourseVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### mapping

Complete reviewed placement carry plan.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "source_placement_id": {
        "type": "string",
        "format": "uuid"
      },
      "target_placement_id": {
        "anyOf": [
          {
            "type": "string",
            "format": "uuid"
          },
          {
            "type": "null"
          }
        ]
      },
      "action": {
        "type": "string",
        "enum": [
          "unchanged",
          "equivalent",
          "reset",
          "removed"
        ]
      },
      "evidence_types": {
        "type": "array",
        "items": {
          "type": "string",
          "enum": [
            "acknowledgment",
            "view",
            "video_coverage",
            "assessment_submission",
            "assessment_result",
            "attendance",
            "package",
            "accessible_equivalent",
            "waiver",
            "carry"
          ]
        },
        "maxItems": 10,
        "minItems": 0
      },
      "equivalence_basis": {
        "anyOf": [
          {
            "type": "string",
            "minLength": 1,
            "maxLength": 1600
          },
          {
            "type": "null"
          }
        ]
      }
    },
    "required": [
      "source_placement_id",
      "target_placement_id",
      "action",
      "evidence_types",
      "equivalence_basis"
    ],
    "additionalProperties": false
  },
  "maxItems": 20000,
  "minItems": 0
}
```

### plan_digest

Canonical plan, audience and policy digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### state

Rollout lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "approved",
    "applying",
    "completed",
    "partial",
    "cancelled"
  ],
  "default": "draft"
}
```

### revision

Plan revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### approved_by

Independent authorized reviewer.

Optional. Nullable.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### apply_at

Earliest planned effective instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Source and target belong to same course.
- Map actions preserve historical attempts.

## Unique keys

- `id`
- `offering_id, plan_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, apply_at | Rollout administration and worker queue. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
