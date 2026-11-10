# PackageObjectiveMapping

Immutable declared read or write edge between an activity objective and a target objective.

Owned by **interoperability**.

## Fields

### id

Immutable identity allocated once by the interoperability owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_id

Declaring manifest activity.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### local_key

Exact local objective identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### target_key

Exact declared mapped objective identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### read_dimensions

Approved dimensions read from target.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "satisfaction",
      "measure",
      "completion",
      "progress",
      "raw",
      "min",
      "max"
    ]
  },
  "maxItems": 7,
  "minItems": 0,
  "uniqueItems": true
}
```

### write_dimensions

Approved dimensions written to target.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "satisfaction",
      "measure",
      "completion",
      "progress",
      "raw",
      "min",
      "max"
    ]
  },
  "maxItems": 7,
  "minItems": 0,
  "uniqueItems": true
}
```

### source_locator

Exact edition manifest rule location.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

## Integrity

- Edition profile determines available dimensions and default flags.
- Conflicting mappings must fail compilation or have exact normative resolution.

## Unique keys

- `id`
- `activity_id, local_key, target_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| activity_id, local_key | Resolve permitted objective dimensions in sequencing order. |

## Retention

Retain as package rule provenance.
