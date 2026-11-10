# PackageVersion

Immutable SCORM or cmi5 package profile, source bytes and validated manifest projection.

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

### artifact_id

Archive bytes accepted for the owning trust boundary.

Required. Null is rejected.

References [TransferArtifact](TransferArtifact.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### profile

Playback profile family.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "scorm",
    "cmi5"
  ]
}
```

### edition

Exact standard edition declared and validated.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### manifest_identifier

Original scoped manifest ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### manifest_digest

Digest of validated manifest projection.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### manifest_locator

Exact approved root manifest path.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### schema_build

Immutable schema bundle and compatibility policy version.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### network_allowlist

Exact reviewed origins the content execution may reach.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uri",
    "maxLength": 2048
  },
  "maxItems": 50,
  "minItems": 0,
  "uniqueItems": true
}
```

### review_status

Runtime and rights review gate.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staged",
    "approved",
    "blocked",
    "withdrawn"
  ]
}
```

### reviewer_principal_id

Approver when approved.

Optional. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### compatibility

Verified packaging profile classification.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "strict",
    "review_only",
    "unsupported"
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

## Integrity

- A byte or validated manifest change creates a new version.
- Approval is separately scoped and does not activate a course assignment.
- Existing registrations retain the assigned package digest.

## Unique keys

- `id`
- `artifact_id, profile, edition, schema_build`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, review_status, created_at | Find unreviewed packages and withdrawn versions. |

## Retention

Retain bytes and projection while referenced by any registration, exam evidence or active assignment. Preserve review and digest evidence after eligible disposal.
