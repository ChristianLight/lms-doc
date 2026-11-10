# Competency

Stable academic outcome identity within one framework family.

Owned by **records**.

## Fields

### id

Stable globally unique Competency identifier.

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

### framework_key

Stable framework family within institution.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Stable competency code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$"
}
```

### archived

Exclude from new framework versions when retired.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
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

- Archive cannot delete published competency evidence.

## Unique keys

- `id`
- `institution_id, framework_key, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, framework_key, archived | Find active outcome identities. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
