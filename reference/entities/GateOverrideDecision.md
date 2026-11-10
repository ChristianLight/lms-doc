# GateOverrideDecision

Audited explicit prerequisite approval or waiver scoped to one enrollment release and placement.

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

### enrollment_release_id

Exact learner context.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Exact gate target.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the version pinned to the EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Applicable exact rule.

Required. Null is rejected.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approval_key

Approval node key or whole allowed gate code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### effective_from

Inclusive start.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_to

Exclusive end.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Override lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "ended"
  ],
  "default": "active"
}
```

### approved_by

Authorized grantor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason_code

Internal reason classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### safe_message

Optional learner-safe projection.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1000
}
```

### revision

Optimistic token.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

## Integrity

- Only declared approved prerequisite clauses can be waived.
- Safety, authorization and mandatory hard dates take precedence.

## Unique keys

- `id`
- `enrollment_release_id, content_placement_id, approval_key, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, content_placement_id, approval_key, effective_to | Applicable override evaluation. |

## Retention

Retain with scoped academic record history while referenced and through the institutional retention window or any hold.
