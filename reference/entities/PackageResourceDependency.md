# PackageResourceDependency

A validated manifest dependency edge between two resources.

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

### resource_id

Dependent resource.

Required. Null is rejected.

References [PackageResource](PackageResource.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### depends_on_id

Required resource in the same PackageVersion.

Required. Null is rejected.

References [PackageResource](PackageResource.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Position of original dependency declaration.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000
}
```

## Integrity

- Approved default import prohibits dependency cycles.
- No dependencies cross package versions.

## Unique keys

- `id`
- `resource_id, depends_on_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| depends_on_id | Find impacted resource launches after diagnostics. |

## Retention

Same retention as the owning package.
