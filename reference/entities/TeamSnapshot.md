# TeamSnapshot

Frozen membership and credit eligibility for one team delivery.

Owned by **assessment**.

## Fields

### id

Stable globally unique TeamSnapshot identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### delivery_id

Offering-bound team activity.

Required. Null is rejected.

References [AssessmentDelivery](AssessmentDelivery.md). Offering-bound team activity.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learning_group_id

Source group scoped to the offering.

Required. Null is rejected.

References [LearningGroup](LearningGroup.md). Source group scoped to the offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### membership_revision

Source membership snapshot sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### members

Frozen scoped enrollment members and participation capabilities.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "enrollment_id": {
        "type": "string",
        "format": "uuid"
      },
      "role": {
        "type": "string",
        "enum": [
          "editor",
          "observer",
          "submitter"
        ]
      },
      "eligible_for_credit": {
        "type": "boolean"
      },
      "enrollment_release_id": {
        "type": "string",
        "format": "uuid",
        "x-entity-reference": "EnrollmentRelease"
      }
    },
    "required": [
      "enrollment_id",
      "role",
      "eligible_for_credit",
      "enrollment_release_id"
    ],
    "additionalProperties": false
  },
  "minItems": 1,
  "maxItems": 200
}
```

### captured_at

Time membership and eligibility were evaluated.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### capture_request_id

Stable owner-coordinated start reservation identity, unique for this team capture.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Members belong to the same offering.
- Current access remains required for edits.
- Historical eligibility is immutable.
- Each member supplies the EnrollmentRelease current at attempt start. All captured releases resolve to the same delivery placement CourseVersion.
- Each attempt captures one fresh exact eligibility snapshot. Historical snapshot changes never reset team quota.

## Unique keys

- `id`
- `delivery_id, learning_group_id, capture_request_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| delivery_id, learning_group_id | Find frozen group participation. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
