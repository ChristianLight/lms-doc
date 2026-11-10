# InstitutionPolicyVersion

Immutable reviewed safety defaults used by new policy decisions.

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

### revision

Monotonic institution profile revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### effective_at

Inclusive activation time. New decisions select the latest approved effective revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### idle_session_minutes

Idle timeout for an ordinary interactive session.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 5,
  "maximum": 180,
  "default": 30
}
```

### absolute_session_minutes

Absolute timeout. Cannot be less than idle timeout.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 30,
  "maximum": 1440,
  "default": 720
}
```

### recent_auth_minutes

Age limit for sensitive self-service and elevated approvals.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 30,
  "default": 10
}
```

### privileged_authentication

Default required privilege authentication strength.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "mfa",
    "phishing_resistant"
  ],
  "default": "mfa"
}
```

### standing_role_review_days

Periodic review deadline for indefinite grants.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 365,
  "default": 90
}
```

### guardian_review_days

Maximum approved guardian term before review.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 365,
  "default": 365
}
```

### privacy_due_days

Operational case target subject to approved institutional law and records policy.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 365,
  "default": 30
}
```

### examination_zero_acknowledged_loss

Whether high-stakes exam release requires tested zero loss of acknowledged submissions in the declared failure domain.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### approved_by_id

Independent policy reviewer.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### approval_ref

Protected evidence of applicable law, scope and review.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Publication does not reinterpret deadlines or rewrite approved custody evidence. Revocation or tighter authentication policy can invalidate access immediately.
- A deployment cannot claim high-assurance exam readiness without passing the corresponding recovery profile.

## Unique keys

- `id`
- `institution_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, effective_at | Select current approved institution policy |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
