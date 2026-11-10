# GuardianRelationship

Verified and expiring rights relation between an observer and a learner.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### guardian_person_id

Requested or approved guardian or observer.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learner_person_id

Learner subject.

Required. Null is rejected.

References [Person](Person.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### relationship_kind

Relationship and evidentiary category.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "parent",
    "legal_guardian",
    "adult_delegate",
    "observer"
  ]
}
```

### evidence_ref

Protected verified evidence reference. Do not expose to teachers or observers.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### visible_categories

Approved summary categories.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "progress_summary",
      "attendance_summary",
      "released_report",
      "teacher_contact"
    ]
  },
  "minItems": 0,
  "maxItems": 4,
  "uniqueItems": true
}
```

### valid_from

Inclusive activation time. Absent while requested.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### valid_until

Exclusive expiration or compulsory review time. Required when verified.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reviewed_by_id

Independent institution reviewer.

Optional. Nullable.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "requested",
    "verified",
    "revoked",
    "denied"
  ]
}
```

## Integrity

- No default visibility categories. A relationship is required in addition to capability. Staff cannot approve where a conflict applies.
- Learner adult or unknown age status requires explicit institution-approved authority for continued visibility.
- No overlapping verified relationship for the same ordered pair unless institution supports separately evidenced scopes.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, learner_person_id, state, valid_until | Recheck active guardians for disclosure and learner status changes |
| institution_id, guardian_person_id, state | List verified learner relationships |

## Retention

Retain live and historic references while required by enrollment or records. Apply identity_contact policy to separately protected contact data.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | verified | DecideGuardianRelationship | Evidence and age-sensitive policy verified by an independent reviewer Record category mask and expiry, bump authorization epoch. |
| requested | denied | DecideGuardianRelationship | Reviewer records insufficient evidence or inapplicable policy Send minimal outcome notification. |
| requested | revoked | RevokeGuardianRelationship | Authorized actor withdraws pending request End approval eligibility. |
| verified | revoked | RevokeGuardianRelationship | Authorized actor, learner status change or safeguarding decision ends visibility Bump authorization epoch and revoke access immediately. |
