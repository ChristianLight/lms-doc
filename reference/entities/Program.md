# Program

Stable institutional programme of study or credential pathway.

Owned by **records**.

## Fields

### id

Stable globally unique Program identifier.

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

### organization_unit_id

Academic programme owner in institution.

Required. Null is rejected.

References [OrganizationUnit](OrganizationUnit.md). Academic programme owner in institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Unique institutional programme code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### title

Current display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### level_code

Institutional award level or framework code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### state

Catalog availability.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "retired"
  ],
  "default": "active"
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

- Retirement stops new assignments while preserving requirements and awards.

## Unique keys

- `id`
- `institution_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, organization_unit_id, state | Find scoped active programmes. |

## Retention

Retain as authoritative academic history according to record retention and legal hold. Preserve supersession lineage.
