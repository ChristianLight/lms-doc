# StorageObject

One private stored binary or pinned provider version used by a domain-owned resource.

Owned by **platform**.

## Fields

### id

Server-assigned opaque identity. Never reused.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution owning this record

Required. Null is rejected.

References [Institution](Institution.md). Exact institution root

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

UTC instant of initial durable creation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### version

Starts at 1. Increment exactly once per authoritative mutation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### updated_at

UTC instant of the latest authoritative mutation. Server assigned.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### owner_resource_type

Exact owning domain resource type from the storage registry.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64,
  "pattern": "^[A-Za-z0-9][A-Za-z0-9._-]*$"
}
```

### owner_resource_id

Owning resource UUID. Validate existence and scope with the domain owner.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### owner_resource_version

Owning resource generation when upload was initiated.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### purpose

Access and scanning profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "content",
    "submission",
    "evidence",
    "export",
    "package"
  ]
}
```

### backend

Selected private storage or registered provider mode.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "database",
    "object_storage",
    "document_provider",
    "media_provider"
  ]
}
```

### provider_version_id

Immutable external version. Required when using a provider.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### protected_object_key_ref

Restricted backend locator. Never supplied by the uploading client.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### expected_bytes

Approved declared upper bound for this upload.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483648
}
```

### observed_bytes

Measured stored size.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483648
}
```

### content_sha256

Digest measured in quarantine.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 64,
  "maxLength": 64,
  "pattern": "^[0-9a-f]{64}$"
}
```

### verified_media_type

Server-verified media type.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### available_at

When authorized delivery became possible.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Current lifecycle state. Mutate only through declared transitions.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "reserved",
    "uploaded",
    "scanning",
    "available",
    "rejected",
    "revoked",
    "disposed"
  ]
}
```

## Integrity

- No read before successful scan and authoritative domain linkage. Authorization derives from the domain resource and requested version.
- Digest match never grants cross-institution visibility. Serving and upload origins are isolated from trusted application sessions.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, owner_resource_type, owner_resource_id, state | Resolve current stored content for a domain resource |
| institution_id, state, created_at | Find stale quarantine objects and cleanup candidates |

## Retention

Quarantine reserves 24 hours, rejected uploads 7 days by default. Available content follows its owner and hold policy.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| reserved | uploaded | FinalizeStorageUpload | Upload receipt and object version verify against reservation Enqueue content verification. |
| uploaded | scanning | ClaimPlatformJob | Authorized scanner obtains active lease Bind scanning lease to measured binary. |
| scanning | available | RecordStorageScan | Verified content and current scan profile permit release Pin immutable object version and record scan evidence. |
| scanning | rejected | RecordStorageScan | Unsafe type, unexpected bytes, invalid digest or scan finding Quarantine payload and record normalized reason. |
| available | revoked | RevokeStorageObject | Security signal or domain owner withdraws binary Reject new reads, terminate active gateway access where possible. |
| revoked | disposed | RecordDispositionOutcome | Current policy and legal hold recheck allow deletion Write storage disposal receipt and retain protected reference. |
