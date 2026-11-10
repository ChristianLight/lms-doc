# PackageResourceFile

Full verified relative-path reference and immutable file evidence.

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

Resource that declares or depends on the path.

Required. Null is rejected.

References [PackageResource](PackageResource.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### path

Exact canonical, case-sensitive package-relative path.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 2048
}
```

### sha256

Lowercase SHA-256 hexadecimal digest of the exact named bytes.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### byte_length

Verified bytes.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### media_type

Validated serving content type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### safety_class

Serving policy and preview restrictions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "web_executable",
    "media",
    "document",
    "metadata",
    "blocked"
  ]
}
```

## Integrity

- Resource-specific file edges may share a blob only after digest and trust checks.
- No path collision after the chosen canonical path validation.

## Unique keys

- `id`
- `resource_id, path`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| resource_id, safety_class | Inspect executable and blocked resources. |

## Retention

Same retention as package. Resource files are never directly served from a private object key.
