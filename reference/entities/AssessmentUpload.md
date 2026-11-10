# AssessmentUpload

Private attempt-scoped staged file and scan state.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentUpload identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_id

Candidate attempt requiring artifact.

Required. Null is rejected.

References [Attempt](Attempt.md). Candidate attempt requiring artifact.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_item_id

Item occurrence in same attempt.

Required. Null is rejected.

References [AttemptItem](AttemptItem.md). Item occurrence in same attempt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### interaction_key

File interaction local key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### uploader_id

Authorized candidate or team editor.

Required. Null is rejected.

References [Principal](Principal.md). Authorized candidate or team editor.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### filename

Untrusted display filename without path separators.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 255,
  "pattern": "^[^/\\\\]+$"
}
```

### declared_mime

Declared upload media type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 3,
  "maxLength": 120,
  "pattern": "^[a-z0-9.+-]+/[a-z0-9.+-]+$"
}
```

### bytes_expected

Maximum allowed content size for reserved upload.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 209715200
}
```

### content_digest

Verified immutable file digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### asset_version_id

Approved private file version in exact attempt scope.

Optional. Nullable.

References [AssetVersion](AssetVersion.md). Approved private file version in exact attempt scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Upload and scan lifecycle. Detached is a derived candidate selection view from the current response revision.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "initiated",
    "quarantined",
    "approved",
    "rejected",
    "detached"
  ]
}
```

### expires_at

Staging lease deadline.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Only approved scanned assets can enter sealed evidence.
- Attachments remain scope-restricted.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| attempt_id, interaction_key, state | Resolve approved or pending candidate artifacts. |
| state, expires_at | Expire unused staging targets. |

## Retention

Expire abandoned quarantine on staging schedule. Retain sealed assets for the submission retention period.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| initiated | quarantined | CompleteAssessmentUpload | Bytes, digest and media assertions validate. Register candidate file in quarantine. |
| quarantined | approved | CompleteAssessmentScan | Trusted scan result confirms clean immutable asset. Allow attachment to exact attempt response. |
| quarantined | rejected | CompleteAssessmentScan | Scan or format validation fails. Keep out of candidate evidence. |
