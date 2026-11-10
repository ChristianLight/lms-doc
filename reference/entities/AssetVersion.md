# AssetVersion

Versioned bytes or provider object, verified metadata and access policy.

Owned by **curriculum**.

## Fields

### id

Stable opaque identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### asset_id

Logical owner.

Required. Null is rejected.

References [Asset](Asset.md). Must resolve to an authorized Asset in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### storage_mode

Selects platform StorageObject or exact pinned provider resource.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "managed",
    "externally_hosted"
  ],
  "default": "managed"
}
```

### storage_object_id

Exact platform-managed binary and custody record.

Optional. Nullable.

References [StorageObject](StorageObject.md). Same institution and owner_resource_type AssetVersion with owner_resource_id matching this version. Required to finalize a managed version.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### storage_scan_result_id

Platform verdict supporting asset acceptance.

Optional. Nullable.

References [StorageScanResult](StorageScanResult.md). Must match the exact storage object, verified digest and current scanner policy. Required for approved managed bytes.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_resource_map_id

Platform-owned mapping to an exact externally hosted provider version.

Optional. Nullable.

References [ExternalResourceMap](ExternalResourceMap.md). Map is in same institution, local type AssetVersion, and local ID equals this asset version. Provider must guarantee pinned version for publication.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### digest

Verified bytes digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### bytes

Verified size in bytes.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10737418240
}
```

### media_type

Detected media type.

Optional. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 120
}
```

### filename

Sanitized display filename.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 240
}
```

### rights_key

Scoped rights policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### state

Current safety state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "awaiting_upload",
    "quarantined",
    "scanning",
    "approved",
    "rejected",
    "withdrawn"
  ],
  "default": "awaiting_upload"
}
```

### created_by

Uploading principal.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Approved content pins exact AssetVersion.
- Approved bytes and verified metadata are immutable.
- Managed versions use a StorageObject and platform scan result. Externally hosted versions use a pinned ExternalResourceMap and cannot carry a managed storage object.
- Approval follows the platform authoritative object or provider result. Withdrawal blocks this resource without modifying platform custody state.
- Only explicitly hosted versions can use the hosted approval command. Managed bytes require a trusted platform scan verdict.
- An authoring-source AssetVersion uses a Platform StorageObject of evidence purpose. Learner content placements require a separate approved content-purpose AssetVersion with rights and accessibility checks even if the bytes match.

## Unique keys

- `id`
- `asset_id, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| asset_id, state, revision | Asset versions and withdrawal impact. |
| state, created_at | Scanner and quarantine work queue. |

## Retention

Preserve while referenced by a publication, active delivery, retained academic evidence or legal hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| awaiting_upload | quarantined | FinalizeAssetUpload | Received staged object verifies. Persist server digest and queue scan. |
| scanning | approved | RecordAssetScan | Verified safe scan and type. Expose asset version for authorized adoption. |
| scanning | rejected | RecordAssetScan | Scan rejects or mismatch. Retain protected evidence. |
| approved | withdrawn | WithdrawAssetVersion | Authorized safety decision. Immediately deny new delivery. |
| quarantined | scanning | FinalizeAssetUpload | Platform confirms object finalization and a fenced scan was scheduled. Expose scan pending or in progress in the authoring projection. |
| awaiting_upload | approved | ApproveHostedAssetVersion | Externally hosted and platform map confirms immutable revision. Bind exact provider resource to the authorized asset version. |
| quarantined | approved | RecordAssetScan | Matching platform scan success arrives before the scanning projection. Link verified platform receipt and authorize asset adoption. |
| quarantined | rejected | RecordAssetScan | Matching platform rejection arrives before the scanning projection. Link retained platform receipt and keep asset inaccessible. |
