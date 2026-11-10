# InterventionAction

Restricted human case action or reviewed support communication.

Owned by **records**.

## Fields

### id

Stable globally unique InterventionAction identifier.

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

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### case_id

Scoped support case in same offering.

Required. Null is rejected.

References [InterventionCase](InterventionCase.md). Scoped support case in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### action_kind

Recorded authorized support action.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "assign",
    "request_information",
    "contact",
    "dismiss",
    "resolve",
    "reopen"
  ]
}
```

### channel

Approved minimal disclosure channel.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "internal",
    "learner_portal",
    "approved_message"
  ]
}
```

### reason

Purpose-restricted note or action reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### occurred_at

Action timestamp.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
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

- No staff note is added to the transcript or grade feedback.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| case_id, occurred_at | Read ordered scoped intervention timeline. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.
