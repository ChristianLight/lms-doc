# RosterFeed

A verified roster source with field ownership and replay watermark.

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

### institution_id

Institution owning these data and their access policy.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Unique external identifier namespace.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### mode

Authorized transport binding.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "csv",
    "rest"
  ]
}
```

### authority

Maximum effects this feed can propose.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "read_only_preview",
    "approved_delta",
    "approved_full"
  ]
}
```

### field_authority

Data classes the feed owns.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "identity_alias",
      "term",
      "organization",
      "course",
      "section",
      "enrollment",
      "resource",
      "grade"
    ]
  },
  "maxItems": 8,
  "minItems": 1,
  "uniqueItems": true
}
```

### cursor

Latest successfully applied opaque REST checkpoint.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 1024
}
```

### last_sequence

Last durable full or delta generation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### source_watermark

Source watermark committed with reconciliation results.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "active",
    "paused",
    "retired"
  ]
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Never authorize withdrawal from partial, failed or non-authoritative snapshots.
- Check whether roster feed ownership overlaps managed fields.

## Unique keys

- `id`
- `institution_id, source_namespace`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state | List active feeds and detect possible overlapping authorities. |

## Retention

Retain active authority records and reconcile receipts per institutional roster audit policy.
