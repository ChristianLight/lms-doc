# Section

Rostered instructional class inside one offering.

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

### offering_id

Owning delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### code

Normalized section code.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### title

Human section name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### capacity

Null means no independent section cap.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000000
}
```

### timezone

Optional named local zone.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 100
}
```

### state

Roster lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "closed"
  ],
  "default": "active"
}
```

### revision

Concurrency token.

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

- No membership outside offering.

## Unique keys

- `id`
- `offering_id, code`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state, title | Authorized section list and roster scope. |

## Retention

Retain with academic participation while referenced and throughout the institutional retention period and any active hold.
