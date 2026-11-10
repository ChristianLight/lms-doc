# PackageOrganization

One ordered organization inside a verified package manifest.

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

### package_version_id

Owning version.

Required. Null is rejected.

References [PackageVersion](PackageVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_key

Exact manifest identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### title

Sanitized localized default display name.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1024
}
```

### ordinal

Source order.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000
}
```

### is_default

True only for the selected manifest default.

Required. Null is rejected.

```json
{
  "type": "boolean",
  "default": false
}
```

## Integrity

- A deliverable package has exactly one approved default when required by the profile.
- Every occurrence belongs to an organization in its own package.

## Unique keys

- `id`
- `package_version_id, external_key`
- `package_version_id, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| package_version_id, is_default | Resolve manifest default organization. |

## Retention

Same retention as the owning package.
