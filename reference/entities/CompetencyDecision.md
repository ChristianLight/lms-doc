# CompetencyDecision

Immutable aggregate determination of a learner competency.

Owned by **records**.

## Fields

### id

Stable globally unique CompetencyDecision identifier.

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

### competency_version_id

Pinned exact skill and evidence policy.

Required. Null is rejected.

References [CompetencyVersion](CompetencyVersion.md). Pinned exact skill and evidence policy.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evidence_ids

Accepted exact source revisions considered.

Required. Null is rejected.

References [CompetencyEvidence](CompetencyEvidence.md). Accepted exact source revisions considered.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 500,
  "minItems": 0,
  "uniqueItems": true
}
```

### supersedes_id

Prior mastery decision in same person and competency.

Required. Nullable.

References [CompetencyDecision](CompetencyDecision.md). Prior mastery decision in same person and competency.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### status

Published or prospective mastery outcome.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "insufficient",
    "developing",
    "demonstrated",
    "expired",
    "revoked"
  ]
}
```

### level_code

Derived scale code, null when no level available.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### cutoff_at

Academic evaluation cutoff.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### expires_at

Optional exclusive mastery expiration.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### fingerprint

Exact policy and evidence lineage digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
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

- Separate insufficient evidence from lowest observed rank.
- Order is based on observed instant, source revision and stable ID.

## Unique keys

- `id`
- `person_id, competency_version_id, fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| person_id, competency_version_id, cutoff_at | Resolve historical and current authorized mastery decisions. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
