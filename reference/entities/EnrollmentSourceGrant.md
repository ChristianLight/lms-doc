# EnrollmentSourceGrant

Independent source-specific authority supporting participation.

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

### enrollment_id

Affected participation.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Must resolve to an authorized Enrollment in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Configured authoritative source.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### external_grant_key

Stable upstream or internal grant key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### seen_sequence

Last accepted source sequence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991,
  "default": 0
}
```

### effective_from

Inclusive grant start.

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

Grant lifecycle.

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

## Integrity

- A feed writes only its own grants.
- Prior grant intervals survive removal.

## Unique keys

- `id`
- `source_namespace, external_grant_key, enrollment_id, effective_from`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_id, state, effective_to | Resolve remaining independent grants. |
| source_namespace, seen_sequence | Snapshot reconciliation and replay. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
