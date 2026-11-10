# ExternalGradeBinding

One deployment-scoped grade-service line item mapped to an owner GradeItem.

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

### deployment_id

Authorized service and role context.

Required. Null is rejected.

References [ExternalToolDeployment](ExternalToolDeployment.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resource_link_id

Optional link scope permitted by approved deployment.

Optional. Null is rejected.

References [ExternalToolResourceLink](ExternalToolResourceLink.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_item_id

Formal destination validated by records owner.

Required. Null is rejected.

References [GradeItem](GradeItem.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_line_item_key

Scoped opaque service line-item ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### points_maximum

Positive maximum for grade normalization and service exchange.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:0|[1-9][0-9]{0,11})(?:\\.[0-9]{1,6})?$"
}
```

### release_policy_revision

Pinned assessment and records policy boundary.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "disabled",
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

- A tool result is imported evidence, never direct formal grade publication.
- Scale transformations and above-maximum policy are explicit.

## Unique keys

- `id`
- `deployment_id, external_line_item_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| grade_item_id, state | Find evidence sources for formal item. |

## Retention

Retain for life of associated grade and policy evidence.
