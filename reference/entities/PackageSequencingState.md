# PackageSequencingState

Authoritative execution cursor, frozen attempt tree and revision.

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

### registration_id

Single current instance of edition sequencing for the package attempt.

Required. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### organization_id

Immutable selected activity tree.

Required. Null is rejected.

References [PackageOrganization](PackageOrganization.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### current_occurrence_id

Current delivery or activity cursor.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### suspended_occurrence_id

Resume cursor for a suspended activity.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### active_path

Ordered activity IDs from root through current active path.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Each occurrence lies in this state's organization tree.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 256,
  "minItems": 0,
  "uniqueItems": true
}
```

### delivery_pending

Whether a selected resource still awaits authorized launch.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### ended

Whether this sequencing session has ended.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### sequence_revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### updated_at

Server time of last sequencing transaction.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Current and suspended pointers must be in the same immutable activity tree.
- The active path has no gaps or cycles and frozen per-attempt child lists live on activity attempts.

## Unique keys

- `id`
- `registration_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| organization_id, ended | Find active sequencing instances by organization. |

## Retention

Retain cursor and immutable navigation outcomes with registration evidence.
