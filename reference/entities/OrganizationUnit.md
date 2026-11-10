# OrganizationUnit

An administrative subdivision such as campus, department or faculty.

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

### parent_id

Parent unit within the same institution. Null identifies a root unit.

Optional. Nullable.

References [OrganizationUnit](OrganizationUnit.md). Same institution and applicable scope

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Stable institution-unique administrative key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### name

Display name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 180
}
```

### kind

Kind used for navigation and management.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "campus",
    "faculty",
    "department",
    "school",
    "division",
    "service"
  ]
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
    "archived"
  ]
}
```

## Integrity

- Maximum 16 unit ancestors. Refuse cycles under an institution hierarchy write lock.
- Move recomputes the affected paths atomically and bumps authorization epoch. Historical grant events carry the evaluated old path.

## Unique keys

- `id`
- `institution_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, parent_id, state | List child units and validate descendants |

## Retention

Retain policy and authority history while records that depend on it exist. Apply institution archive rules after required verification.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| active | archived | ArchiveOrganizationUnit | No active children or transferable responsibility remains Preserve paths on historical evidence. |
