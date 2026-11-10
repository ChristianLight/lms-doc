# AdmissionPolicyVersion

Versioned eligibility, capacity and seat offer policy.

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

Offering owner.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic policy revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### routes

Allowed distinct admission routes.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "manual",
      "self",
      "invitation",
      "cohort",
      "roster",
      "rule",
      "transfer"
    ]
  },
  "maxItems": 7,
  "minItems": 1
}
```

### course_prerequisite_ids

Course requirements evaluated against verified completions.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 100,
  "minItems": 0
}
```

### requires_approval

Registrar must decide.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### waitlist_enabled

Queue eligible applicants when full.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### seat_offer_hours

Hold a promoted seat for this duration.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 168,
  "default": 48
}
```

### suspension_holds_seat

Suspended participation consumes capacity.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### effective_from

First valid instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### digest

Frozen policy and prerequisite digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

## Integrity

- Approval and enrollment state must be evaluated separately.

## Unique keys

- `id`
- `offering_id, revision`
- `offering_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, effective_from | Effective registration policy. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
