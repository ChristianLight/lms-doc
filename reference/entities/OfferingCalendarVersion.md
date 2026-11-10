# OfferingCalendarVersion

Published offering-wide hard dates with exact civil-time context.

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

Calendar owner.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic calendar revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### timezone

IANA zone used for calendar arithmetic.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### tzdb_version

Time zone database release.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### windows

Resolved UTC bounds with explicit nulls.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "enroll_open_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "enroll_close_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "learn_open_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "learn_close_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "review_open_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    },
    "review_close_at": {
      "anyOf": [
        {
          "type": "string",
          "format": "date-time"
        },
        {
          "type": "null"
        }
      ]
    }
  },
  "required": [
    "enroll_open_at",
    "enroll_close_at",
    "learn_open_at",
    "learn_close_at",
    "review_open_at",
    "review_close_at"
  ],
  "additionalProperties": false
}
```

### effective_from

Activation boundary.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approved_by

Calendar approving principal.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### published_at

Durable publish instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- All present windows have inclusive starts and exclusive ends.
- Prior calendars stay pinned to already issued contexts.

## Unique keys

- `id`
- `offering_id, revision`
- `offering_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, effective_from | Select effective version at an action instant. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
