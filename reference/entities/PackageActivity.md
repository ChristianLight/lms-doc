# PackageActivity

One manifest occurrence with distinct tracking and sequencing identity.

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

### organization_id

Containing organization.

Required. Null is rejected.

References [PackageOrganization](PackageOrganization.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### parent_id

Containing cluster within the same organization.

Optional. Null is rejected.

References [PackageActivity](PackageActivity.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resource_id

Launchable leaf resource within the same PackageVersion.

Optional. Null is rejected.

References [PackageResource](PackageResource.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_key

Exact original item identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### title

Sanitized accessible display title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1024
}
```

### ordinal

Zero-based source sibling position.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000
}
```

### is_visible

Navigation visibility, independent of authorization.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": true
}
```

### parameters

Validated original item query parameter string.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 2048
}
```

### launch_data

Edition-constrained initial run-time launch data.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 65536
}
```

### mastery_value

Edition-compatible original mastery or normalized threshold, interpreted under manifest profile.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:0|[1-9][0-9]{0,11})(?:\\.[0-9]{1,6})?$"
}
```

### time_limit_action

Validated edition-specific behavior.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

## Integrity

- Sibling ordinal is unique under the same parent, including the root set.
- Cluster and leaf combinations obey verified edition constraints.
- A visible resource requires an assigned launch grant.

## Unique keys

- `id`
- `organization_id, external_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| organization_id, parent_id, ordinal | Traverse ordered package activity tree. |
| resource_id | Find occurrences that share a resource. |

## Retention

Same retention as the owning package.
