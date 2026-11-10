# Person

Institution-local educational identity, independent of credentials.

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

### display_name

Current approved name used in LMS views.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 180
}
```

### legal_name_ref

Protected reference to legal-name evidence. Present only where institutional records require it.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learner_number

Optional institution-issued academic identifier. Unique among all historical non-null values.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### preferred_locale

User-selected interface locale.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$"
}
```

### preferred_timezone

User-selected presentation timezone.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^(UTC|[A-Za-z_+-]+(?:/[A-Za-z0-9_+-]+)+)$"
}
```

### age_status

Restricted policy result. It carries no birth date.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "unknown",
    "minor",
    "adult"
  ],
  "default": "unknown"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "inactive",
    "restricted",
    "pseudonymized"
  ]
}
```

## Integrity

- No automatic cross-institution deduplication. A name or email never proves identity.
- Pseudonymization preserves the surrogate identity and protected official records to the extent policy requires.
- Restricted state blocks interactive academic access except purpose-specific records workflows.

## Unique keys

- `id`
- `institution_id, learner_number`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, display_name | Access-filtered institution directory and controlled lookup |

## Retention

Retain live and historic references while required by enrollment or records. Apply identity_contact policy to separately protected contact data.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | inactive | SetPersonState | Authorized registrar confirms departure Increment linked Principal authorization epochs and reject learner and staff access. |
| inactive | active | SetPersonState | Readmission or correction is approved Re-evaluate current assignments and enrollment before authorizing. |
| active | restricted | SetPersonState | Privacy or safeguarding authority approves restriction Invalidate linked sessions and enforce restricted operations. |
| inactive | restricted | SetPersonState | Privacy or safeguarding authority approves restriction Limit record processing. |
| restricted | inactive | SetPersonState | Authorized reviewer lifts restriction without readmission Retain records and leave access inactive. |
| restricted | active | SetPersonState | Authorized reviewer lifts restriction and activation is approved Re-evaluate linked Principal and current assignments. |
| inactive | pseudonymized | RecordDispositionOutcome | Approved disposition and applicable hold checks pass Detach approved contact data and keep legally retained references. |
| restricted | pseudonymized | RecordDispositionOutcome | Approved disposition and applicable hold checks pass Detach approved contact data and keep legally retained references. |
