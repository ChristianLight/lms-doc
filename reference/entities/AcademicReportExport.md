# AcademicReportExport

Scoped report output artifact and use authorization.

Owned by **records**.

## Fields

### id

Stable globally unique AcademicReportExport identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### snapshot_id

Exact approved metric snapshot.

Required. Null is rejected.

References [MetricSnapshot](MetricSnapshot.md). Exact approved metric snapshot.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### artifact_id

Protected CSV or structured report artifact if ready.

Required. Nullable.

References [AssetVersion](AssetVersion.md). Protected CSV or structured report artifact if ready.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### format

Permitted output representation.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "csv",
    "json",
    "xlsx"
  ]
}
```

### state

Export lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "ready",
    "failed",
    "revoked",
    "expired"
  ],
  "default": "queued"
}
```

### scope_digest

Caller and purpose scoped permissions fingerprint.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### expires_at

Exclusive artifact authorization expiry.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### output_digest

Actual export digest when ready.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Recheck authorization at download.
- A regenerated file is not published under old digest.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| snapshot_id, state, expires_at | Serve only valid export versions. |
| actor_id, created_at | Find purpose-authorized caller export history. |

## Retention

Retain under restricted purpose retention and hold. Erase or minimize secondary identifiers after expiry.
