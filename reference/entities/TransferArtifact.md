# TransferArtifact

Immutable archived input or output bytes and classified handling evidence.

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

### institution_id

Institution owning these data and their access policy.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### uploader_principal_id

Authorized actor or service identity for the recorded operation.

Required. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Pre-registered import provenance or outbound destination namespace.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### original_filename

Sanitized basename for operator display only.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255
}
```

### byte_length

Actual length counted during stream verification.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 4398046511104
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

### media_type

Detected container media type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### storage_object_id

Platform-owned private bytes with owner resource, object version, scan status, digest and retention hold.

Required. Null is rejected.

References [StorageObject](StorageObject.md). The StorageObject belongs to this Institution and exact TransferArtifact generation, with package, evidence or export purpose.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### storage_scope

Institution-local storage trust and retention partition.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### detected_format

Detected input shape independently of installation support.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native_curriculum",
    "olx_course",
    "olx_legacy_library",
    "olx_versioned_library",
    "scorm_12",
    "scorm_2004_2",
    "scorm_2004_3",
    "scorm_2004_4",
    "scorm_2004_unverified",
    "qti_21",
    "qti_22",
    "qti_301",
    "common_cartridge",
    "oneroster_12",
    "cmi5_quartz",
    "historic_records"
  ]
}
```

### signature_evidence

Safe evidence for matching manifest signature and version.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### scan_engine

Scanner and signature version for the latest observation.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### rights

Verified distribution rights status.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "institution_owned",
    "licensed",
    "restricted",
    "unknown"
  ]
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "uploading",
    "quarantined",
    "accepted",
    "rejected",
    "expired"
  ]
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

### retain_until

Minimum planned availability deadline before hold checks.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- The verified digest is immutable after quarantine.
- Raw archive reads need explicit artifact authority and permission to every included data class.
- Detect and retain profile evidence before import approval.
- Release eligibility requires an accepted StorageObject version with matching hash and exact byte length. Quarantine may read it only through the storage owner. Storage deduplication never shares domain authorization.

## Unique keys

- `id`
- `institution_id, storage_scope, sha256`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, created_at | Review intake in institution order. |
| state, retain_until | Select purge candidates with hold checks. |

## Retention

Retain accepted curriculum originals while referenced and by default 365 days after transfer. Quarantine or failed artifacts expire after 30 days unless an active investigation or hold applies.
