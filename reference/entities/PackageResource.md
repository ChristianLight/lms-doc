# PackageResource

Manifest resource shared by zero or more launchable occurrences.

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

Verified package scope.

Required. Null is rejected.

References [PackageVersion](PackageVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_key

Manifest resource identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### kind

Whether resource uses the SCORM runtime.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "sco",
    "asset"
  ]
}
```

### media_type

Manifest resource type or approved content media class.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### base_path

Canonical composed package-relative base.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 2048
}
```

### entry_path

Approved launch entry without query or fragment.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### entry_query

Preserved validated source query.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 1024
}
```

### entry_fragment

Preserved safe original fragment.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 256
}
```

## Integrity

- Any launchable occurrence must resolve a validated entry inside this version.
- Resource sharing does not share learner attempt state.

## Unique keys

- `id`
- `package_version_id, external_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| package_version_id, kind | List SCO and asset resource coverage. |

## Retention

Same retention as the owning package.
