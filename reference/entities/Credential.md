# Credential

Immutable credential claim tied to exact academic qualification or mastery.

Owned by **records**.

## Fields

### id

Stable globally unique Credential identifier.

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

### definition_version_id

Approved exact issuer definition.

Required. Null is rejected.

References [CredentialDefinitionVersion](CredentialDefinitionVersion.md). Approved exact issuer definition.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### qualification_id

Authorized exact qualification award if applicable.

Required. Nullable.

References [QualificationDecision](QualificationDecision.md). Authorized exact qualification award if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### competency_decision_id

Approved mastery determination if applicable.

Required. Nullable.

References [CompetencyDecision](CompetencyDecision.md). Approved mastery determination if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### replaces_id

Earlier credential being replaced, if any.

Required. Nullable.

References [Credential](Credential.md). Earlier credential being replaced, if any.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_key

Stable issue scope key for uniqueness across nullable source kinds.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### claim_digest

Canonical approved immutable credential claim digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### claim_storage_id

Protected canonical claim representation.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Protected canonical claim representation.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### verification_key_digest

Opaque public or authenticated token digest if used.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### verification_method

Pinned approved signing verification method identifier.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### issued_at

Official issue instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Exclusive expiration when applicable.

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

## Integrity

- Exactly one source basis.
- Revoked credentials require separate replacement identity.
- Public lookup discloses only approved claims.

## Unique keys

- `id`
- `definition_version_id, source_key`
- `verification_key_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, issued_at | Read authorized credential history. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
