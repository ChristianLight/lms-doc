# SeatReservation

Time-bounded hold for eligible waitlist candidate.

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

### application_id

Promoted candidate.

Required. Null is rejected.

References [EnrollmentApplication](EnrollmentApplication.md). Must resolve to an authorized EnrollmentApplication in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering capacity scope.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### section_id

Optional section seat.

Optional. Nullable.

References [Section](Section.md). Must resolve to an authorized Section in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### token_digest

Hash of one-use acceptance token.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### issued_at

Issue instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive expiry.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Seat lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "held",
    "consumed",
    "released",
    "expired"
  ],
  "default": "held"
}
```

## Integrity

- Only held and unexpired reservations count.
- Capacity check, consumption and enrollment commit together.

## Unique keys

- `id`
- `token_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, expires_at | Capacity and expiration jobs. |
| application_id, state | One active reservation per application. |

## Retention

Retain for the configured operational interval. Purge or de-identify after expiry when no academic reference or hold applies.
