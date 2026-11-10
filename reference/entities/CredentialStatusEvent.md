# CredentialStatusEvent

Append-only credential status transition and reviewer evidence.

Owned by **records**.

## Fields

### id

Stable globally unique CredentialStatusEvent identifier.

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

### credential_id

Credential belonging to same subject and issuer.

Required. Null is rejected.

References [Credential](Credential.md). Credential belonging to same subject and issuer.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Monotonic transition number in credential lifecycle.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### status

Exact approved lifecycle transition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "issued",
    "suspended",
    "reinstated",
    "revoked",
    "expired",
    "superseded"
  ]
}
```

### effective_at

Academic verification state effective instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### reason

Restricted authorized status justification.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 3000
}
```

### replacement_id

New approved issued credential if superseded.

Required. Nullable.

References [Credential](Credential.md). New approved issued credential if superseded.

```json
{
  "type": "string",
  "format": "uuid"
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

- Revoked terminal.
- Expiry is evaluated at exclusive boundary.
- Invalid transitions do not alter verification.

## Unique keys

- `id`
- `credential_id, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| credential_id, effective_at, ordinal | Resolve verification state at time. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
