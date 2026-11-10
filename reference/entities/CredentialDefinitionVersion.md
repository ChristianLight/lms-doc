# CredentialDefinitionVersion

Approved credential appearance, disclosure and verification policy.

Owned by **records**.

## Fields

### id

Stable globally unique CredentialDefinitionVersion identifier.

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

### definition_key

Stable credential family.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic immutable revision number within its stable identity.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
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

### title

Credential display label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### issuer_name

Issuer name pinned for claims.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### achievement_type

Authorized award type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "qualification",
    "competency",
    "microcredential"
  ]
}
```

### locale

Credential language.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9-]+$"
}
```

### verification_mode

Issuer verification profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "disabled",
    "authenticated",
    "opaque_link",
    "signed_exchange"
  ],
  "default": "disabled"
}
```

### allowed_claims

Approved field keys eligible for disclosure.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "pattern": "^[a-z][a-z0-9._-]{0,63}$"
  },
  "maxItems": 32,
  "minItems": 1,
  "uniqueItems": true
}
```

### signature_profile

Exact deployed signing profile when used.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

### valid_days

Optional credential lifetime override within award validity.

Required. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 36500
}
```

### state

Template publication state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "superseded",
    "retired"
  ],
  "default": "draft"
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

## Integrity

- Public disclosure defaults disabled.
- Verification mode and claim set pinned on issue.

## Unique keys

- `id`
- `institution_id, definition_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, definition_key | Find approved issuer definitions. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishCredentialDefinition | Issuer, purpose and claims verified Freeze published disclosure profile. |
