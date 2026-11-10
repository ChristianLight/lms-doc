# ExternalToolResourceLink

Versioned LTI resource placement and deployment binding.

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

Registered tool binding.

Required. Null is rejected.

References [ExternalToolDeployment](ExternalToolDeployment.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Exact native external-tool activity version.

Required. Null is rejected.

References [ActivityVersion](ActivityVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_offering_id

Offering context for audience and membership.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_id

Specific occurrence in active course release.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resource_link_key

Opaque stable LTI resource-link ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### target_link_uri

Vetted link target within this deployment.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### custom_values

Approved platform-owned custom values. Every used key is declared by the active profile. Secrets and markup are rejected.

Required. Null is rejected.

```json
{
  "type": "object",
  "propertyNames": {
    "pattern": "^[a-z][a-z0-9_]{0,63}$"
  },
  "additionalProperties": {
    "type": "string",
    "minLength": 0,
    "maxLength": 1024
  },
  "maxProperties": 32
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

- Activity, deployment and offering belong to the same Institution.
- Repeated resource links in distinct placements cannot share learner context implicitly.

## Unique keys

- `id`
- `deployment_id, resource_link_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| course_offering_id, placement_id | Resolve external activity without using a tool URL as authority. |

## Retention

Retain while course or grade evidence refers to this binding.
