# LegalHold

Approved institution case that prevents disposition of specified records.

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

### case_key

Unique institution case key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### target_kind

Type of selector. Resolve against trusted institutional records.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "person",
    "record",
    "offering",
    "record_class"
  ]
}
```

### target_id

Required for person, record and offering selectors. Null for an institution-wide record-class hold.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### record_class

Required for class selector. Otherwise narrows the named target if supplied.

Optional. Nullable.

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

### effective_from

Inclusive instant from which destruction is forbidden.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### authorized_by_id

Records authority imposing hold.

Required. Null is rejected.

References [Principal](Principal.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### released_at

Time of independent authorized release.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
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
    "released"
  ]
}
```

## Integrity

- No expiration by default. Only an authorized records reviewer can release a hold.
- Use shared scope locking against destruction so an approved hold cannot pass through a race.

## Unique keys

- `id`
- `institution_id, case_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, target_kind, target_id, record_class | Resolve current blockers during selection and execution |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | released | ReleaseLegalHold | Independent authorized reviewer approves release Record release reason and re-evaluate eligible pending records without automatic deletion. |
