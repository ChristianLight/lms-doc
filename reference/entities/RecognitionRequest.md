# RecognitionRequest

Requested transfer credit, equivalency, prior learning or exemption.

Owned by **records**.

## Fields

### id

Stable globally unique RecognitionRequest identifier.

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

### person_id

Educational identity within the same institution.

Required. Null is rejected.

References [Person](Person.md). Educational identity within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### program_enrollment_id

Optional scope for recognition within a programme.

Required. Nullable.

References [ProgramEnrollment](ProgramEnrollment.md). Optional scope for recognition within a programme.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### claimed_course_id

Claimed local equivalent course if identified.

Required. Nullable.

References [Course](Course.md). Claimed local equivalent course if identified.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### claimed_requirement_id

Claimed rule within approved programme version.

Required. Nullable.

References [ProgramRequirement](ProgramRequirement.md). Claimed rule within approved programme version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### claim_kind

Specific proposed recognition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "transfer_credit",
    "prior_learning",
    "substitution",
    "waiver",
    "exemption"
  ]
}
```

### issuer_label

Restricted declared issuing organization.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### external_reference

Restricted source certificate or record identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 400
}
```

### evidence_assets

Approved uploaded verification assets for review.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Approved uploaded verification assets for review.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 30,
  "minItems": 1,
  "uniqueItems": true
}
```

### state

Recognition review lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "requested",
    "under_review",
    "approved",
    "rejected",
    "stale",
    "withdrawn"
  ],
  "default": "requested"
}
```

### verification_consent

Recorded permission for external verification when required.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

### verification_method

Approved latest verification channel.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### verification_evidence_digest

Exact immutable evidence set reviewed by verifier.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### verification_outcome

Latest reviewed source eligibility state.

Required. Nullable.

```json
{
  "type": "string",
  "enum": [
    "verified",
    "not_verified",
    "information_required"
  ]
}
```

### verified_by

Authorized source verifier, distinct from final credit reviewer where applicable.

Required. Nullable.

References [Principal](Principal.md). Authorized source verifier, distinct from final credit reviewer where applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### verified_at

Latest recorded verification instant.

Required. Nullable.

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

- Verification consent alone is not a grant of institutional credit.
- Review cannot alter source artifact bytes. Retain every review in the audit ledger and latest exact reviewed digest in the request guard.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, created_at | Find registrar or verifier recognition queue. |
| person_id, state, created_at | Read authorized learner recognition requests. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| requested | under_review | ReviewRecognition | Verification started by authorized reviewer Record immutable verification outcome. |
| under_review | approved | DecideRecognition | Independent approver and verified evidence Create recognition decision. |
