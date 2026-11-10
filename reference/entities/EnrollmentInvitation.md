# EnrollmentInvitation

One-use intended-person invitation into an offered admission path.

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

Delivery scope.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### person_id

Verified intended learner.

Required. Null is rejected.

References [Person](Person.md). Person must belong to the same institution as the offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### section_id

Optional offered section.

Optional. Nullable.

References [Section](Section.md). Must resolve to an authorized Section in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### token_digest

Hash of opaque random invitation capability.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### state

Invitation lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "issued",
    "used",
    "revoked",
    "expired"
  ],
  "default": "issued"
}
```

### bypass_application_window

Approved scoped exception to registration dates.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### issued_at

Issue time.

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

### issued_by

Authorized inviter.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### application_id

Application created by token use.

Optional. Nullable.

References [EnrollmentApplication](EnrollmentApplication.md). Must resolve to an authorized EnrollmentApplication in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Only matching authenticated person may consume.
- An invitation is not a seat reservation or enrollment.

## Unique keys

- `id`
- `token_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, person_id, state | Scope-safe outstanding invitation list. |
| state, expires_at | Expiry sweep. |

## Retention

Retain with scoped academic record history while referenced and through the institutional retention window or any hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| issued | used | ApplyForEnrollment | Verified person, offered route and unexpired invitation. Create or return invitation-backed application. |
| issued | revoked | RevokeEnrollmentInvitation | Authorized scoped owner and unused token. Prevent future use immediately. |
