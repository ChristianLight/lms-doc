# ItemBank

Scoped collection controlling authorship, access, reuse and copy.

Owned by **assessment**.

## Fields

### id

Stable globally unique ItemBank identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution that owns the bank.

Required. Null is rejected.

References [Institution](Institution.md). Institution that owns the bank.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_kind

Declared owner hierarchy type.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "Institution",
    "OrganizationUnit",
    "Course"
  ]
}
```

### owner_scope_id

Institution, organizational unit or course UUID selected by owner kind.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### name

Human-readable name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### normalized_name

Trimmed, NFC and case-folded name used for scoped uniqueness.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### created_by

Authorized creator within the same institution.

Required. Null is rejected.

References [Principal](Principal.md). Authorized creator within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Authoritative creation time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### archived_at

Time new activity against the bank was stopped.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### default_license

License identifier used only as authoring default.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

## Integrity

- Archive blocks new reuse and keeps historical versions resolvable.
- Cross-institution bank sharing requires explicit copy or transfer.

## Unique keys

- `id`
- `institution_id, owner_kind, owner_scope_id, normalized_name`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_kind, owner_scope_id | Authorized bank browsing by owner. |

## Retention

Retain while any scoped item or audit decision remains.
