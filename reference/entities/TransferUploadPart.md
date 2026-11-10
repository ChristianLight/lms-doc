# TransferUploadPart

Immutable byte-range receipt used to assemble a private transfer artifact.

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

### artifact_id

Uploading aggregate.

Required. Null is rejected.

References [TransferArtifact](TransferArtifact.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### byte_offset

Zero-based byte offset.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### byte_length

Actual part bytes, capped at 64 MiB by default.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 67108864
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

### part_locator

Private staged blob key.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1024
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

- A replay at one offset must match both bytes and size.
- No overlapping offsets are allowed when assembled.

## Unique keys

- `id`
- `artifact_id, byte_offset`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| artifact_id, byte_offset | Verify complete non-overlapping upload coverage. |

## Retention

Delete part bytes after digest-verified assembly or within 24 hours of an expired upload. Keep digest evidence in finalization receipt.
