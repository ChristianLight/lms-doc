# RetentionPolicy

Versioned disposition rule selected by institution and data class.

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

### record_class

Data classification with documented authoritative owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "identity_contact",
    "enrollment_history",
    "academic_official",
    "submissions",
    "drafts",
    "exam_telemetry",
    "audit",
    "connector_message",
    "communication",
    "backup",
    "private_export",
    "asset_bytes"
  ]
}
```

### revision

Monotonic revision per record class.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### trigger

Date origin for calculating eligibility.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "creation",
    "closure",
    "withdrawal",
    "publication",
    "replacement",
    "completion",
    "provider_ack"
  ]
}
```

### retain_days

Minimum retention in complete UTC days after trigger.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 36525
}
```

### disposition

Action applied only with owner verification.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "delete",
    "pseudonymize",
    "archive",
    "manual_review"
  ]
}
```

### effective_from

Inclusive effective date. The current revision is latest approved at or before evaluation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### effective_before

Exclusive review deadline for the approved rule.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### approved_by_id

Independent institutional authority approving the rule.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### reason

Policy evidence and approval reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1000
}
```

## Integrity

- Unknown policy or trigger blocks disposal. New policy never retroactively shortens retention without explicit approved migration.
- Legal holds and outstanding corrections are applied before disposition.

## Unique keys

- `id`
- `institution_id, record_class, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, record_class, effective_from | Select current applicable disposition policy |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.
