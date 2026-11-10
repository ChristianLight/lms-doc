# SourceExtractionRun

Exact protected source PDF extraction and review history.

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

### institution_id

Owning institution.

Required. Null is rejected.

References [Institution](Institution.md). Must resolve to an authorized Institution in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_asset_version_id

Immutable authoring-source PDF.

Required. Null is rejected.

References [AssetVersion](AssetVersion.md). Same institution. AssetVersion has verified managed bytes and StorageObject purpose evidence.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_course_id

Optional explicitly authorized teaching scope.

Optional. Nullable.

References [Course](Course.md). Must resolve to an authorized Course in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### predecessor_run_id

Exact sealed predecessor for corrections.

Optional. Nullable.

References [SourceExtractionRun](SourceExtractionRun.md). Must resolve to an authorized SourceExtractionRun in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### platform_job_id

Coordinator job.

Required. Null is rejected.

References [PlatformJob](PlatformJob.md). Same institution, job_kind course_import and target type SourceExtractionRun.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### requested_by_id

Responsible scoped author.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rights_evidence_object_id

Sealed usage attestation and reviewed rights basis.

Required. Null is rejected.

References [StorageObject](StorageObject.md). Same institution. Platform purpose evidence and exact owner source AssetVersion. Resolve actual object version and digest before use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rights_snapshot

Approved use snapshot. Check current authority again before any protected effect.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "rights_key": {
      "type": "string",
      "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
    },
    "policy_revision": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2147483647
    },
    "purposes": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": [
          "private_extract",
          "external_process",
          "adapt",
          "reuse_excerpt",
          "reuse_figure",
          "learner_download",
          "external_export",
          "publish_derived"
        ]
      },
      "maxItems": 8,
      "minItems": 1,
      "uniqueItems": true
    },
    "approved_by_id": {
      "type": "string",
      "format": "uuid"
    },
    "effective_from": {
      "type": "string",
      "format": "date-time"
    },
    "effective_to": {
      "type": "string",
      "format": "date-time"
    },
    "export_profiles": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
      },
      "maxItems": 20,
      "minItems": 0
    },
    "provider_connection_id": {
      "anyOf": [
        {
          "type": "string",
          "format": "uuid"
        },
        {
          "type": "null"
        }
      ]
    },
    "approval_digest": {
      "type": "string",
      "pattern": "^[0-9a-f]{64}$"
    },
    "recipient_scope_codes": {
      "type": "array",
      "items": {
        "type": "string",
        "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
      },
      "maxItems": 40,
      "minItems": 0,
      "uniqueItems": true
    }
  },
  "required": [
    "rights_key",
    "policy_revision",
    "purposes",
    "approved_by_id",
    "effective_from",
    "effective_to",
    "export_profiles",
    "provider_connection_id",
    "approval_digest",
    "recipient_scope_codes"
  ],
  "additionalProperties": false
}
```

### source_digest

Measured verified source PDF SHA-256.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### profile_key

Approved extraction profile and tool configuration.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z0-9][A-Za-z0-9_.-]{0,79}$"
}
```

### profile_digest

Canonical tool versions, limits and extraction parameters.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### page_ranges

Normalized sorted nonoverlapping zero-based physical ranges.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "from_page": {
        "type": "integer",
        "minimum": 0,
        "maximum": 100000
      },
      "to_page_inclusive": {
        "type": "integer",
        "minimum": 0,
        "maximum": 100000
      }
    },
    "required": [
      "from_page",
      "to_page_inclusive"
    ],
    "additionalProperties": false
  },
  "maxItems": 500,
  "minItems": 1
}
```

### run_fingerprint

Canonical source, profile, rights, range, predecessor and corrections identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### page_count

Physical count reported by trusted parser.

Optional. Nullable.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 100001
}
```

### committed_page_count

Number of accepted physical page receipts.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 500,
  "default": 0
}
```

### manifest_object_id

Sealed reviewed extraction manifest. Page inventory and tool transforms are indexed inside the manifest.

Optional. Nullable.

References [StorageObject](StorageObject.md). Same institution. Platform purpose evidence and exact owner SourceExtractionRun. Resolve actual object version and digest before use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### manifest_digest

Verified canonical extraction manifest digest.

Optional. Nullable.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### reviewed_by_id

Human approving exact manifest.

Optional. Nullable.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Extraction lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "queued",
    "extracting",
    "needs_review",
    "sealed",
    "blocked",
    "canceled"
  ],
  "default": "queued"
}
```

### revision

Run compare-and-swap revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### created_at

Start instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Source PDF is authoring-only and protected by managed evidence purpose.
- One accepted page shard per run and physical page. Sealed pages and regions are immutable.
- A corrected reading creates new sealed extraction with predecessor and new affected region keys.
- A sealed manifest reconciles exact page ordinals, evidence object identities, region digests and reviewed exclusions.
- Export and learner distribution require separate applicable purposes, recipient scope and profile authorization even after private extraction or adaptation.

## Unique keys

- `id`
- `institution_id, run_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, source_asset_version_id, state | History by source, changed extraction and impacted drafts. |
| platform_job_id, state | Coordinator recovery and outbox replay. |

## Retention

Retain protected decisions while needed for reviewed source derivation and retention policy or hold. Retain authorized academic lineage tombstone after eligible source disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| queued | extracting | CommitSourceExtractionPage | Valid page job fence and exact source. Commit first bounded page receipt. |
| extracting | needs_review | CommitSourceExtractionPage | All selected page indices have accepted receipts or explicit unresolved outcomes. Freeze review candidate coverage. |
| needs_review | sealed | SealSourceExtraction | Independent reviewer, exact manifest and every required region resolved. Pin sealed evidence manifest and accepted rights snapshot. |
| needs_review | blocked | SealSourceExtraction | Review identifies mandatory unresolved evidence. Record exact blocked paths and permit a later corrected extraction. |
