# TransferJob

A retryable plan to detect, review and promote an inbound graph or export selection.

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

### actor_principal_id

Authorized actor or service identity for the recorded operation.

Required. Null is rejected.

References [Principal](Principal.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### artifact_id

Inbound input or outbound artifact when produced.

Optional. Null is rejected.

References [TransferArtifact](TransferArtifact.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_namespace

Authorized source namespace.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### format

Exact approved format profile.

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

### source_container

Exact verified outer container of the selected input. Absent on exports and before verified inspection.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "zip",
    "tar_gzip",
    "xml",
    "csv",
    "json"
  ]
}
```

### source_profile

Pinned case-sensitive source decoding profile, independent of archive extension and target format.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9_.-]{0,55}/[0-9a-z][0-9a-z_.-]{0,31}$"
}
```

### inspection_manifest_id

Immutable restricted index of scanned input, candidate roots, rejected entries and adapter evidence.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### inspection_manifest_digest

Canonical fingerprint of protected verified inspection inventory.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### adapter_build

Immutable adapter and policy build identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### direction

Direction of transfer.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "import",
    "export"
  ]
}
```

### mode

Configured operational intent.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "dry_run",
    "editable_draft",
    "historical",
    "delivery_package",
    "export"
  ]
}
```

### target_scope

Typed scope identifier and optional owner key, interpreted under format profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### selected_source_roots

Exact approved artifact roots, logical source scopes, layers and dependency fingerprints. Persist when the import plan is built. Mutually exclusive with an outbound selection.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "root_key": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256
      },
      "kind": {
        "type": "string",
        "enum": [
          "course",
          "library",
          "package",
          "assessment",
          "historic_scope"
        ]
      },
      "source_scope": {
        "type": "string",
        "minLength": 1,
        "maxLength": 256
      },
      "layer": {
        "type": "string",
        "enum": [
          "published",
          "draft",
          "shared"
        ]
      },
      "dependency_digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      },
      "root_record_id": {
        "type": "string",
        "format": "uuid"
      }
    },
    "required": [
      "root_key",
      "kind",
      "source_scope",
      "layer",
      "dependency_digest",
      "root_record_id"
    ],
    "additionalProperties": false
  },
  "maxItems": 1000,
  "minItems": 1,
  "uniqueItems": true
}
```

### root_commit_policy

One selected required dependency closure commits atomically. Required when several roots are selected. Independent promotions require separately approved jobs.

Optional. Null is rejected.

```json
{
  "type": "string",
  "const": "atomic_selected_closure"
}
```

### dependency_artifacts

Immutable authorized input artifact IDs and verified digests, distinct by artifact.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "artifact_id": {
        "type": "string",
        "format": "uuid"
      },
      "sha256": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      },
      "source_profile": {
        "type": "string",
        "pattern": "^[a-z][a-z0-9_.-]{0,55}/[0-9a-z][0-9a-z_.-]{0,31}$"
      }
    },
    "required": [
      "artifact_id",
      "sha256",
      "source_profile"
    ],
    "additionalProperties": false
  },
  "maxItems": 200,
  "minItems": 0,
  "uniqueItems": true
}
```

### plan_revision

Revision of frozen selection, graph and owner baselines. Changes on plan rebuild or repair only. Approval or heartbeat increments job revision without changing this field.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### selection_digest

Fingerprint of immutable outbound selection.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### plan_digest

Fingerprint of staged owner commands and target baseline.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### plan_manifest_id

Exact immutable current plan manifest. Its protected predecessor reference preserves inspectable prior plan revisions, owner baselines, edges or export reports.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Exact clean StorageObject owned by this transfer plan and Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### generation_id

One target generation for the applying or applied import. Allocated before any staged owner command and stable during retries.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### generation_visibility

Authoritative visibility of committed imported generation. Absent until commit. Private permits only authorized editor workflows.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "private",
    "activated"
  ]
}
```

### generation_receipt_digest

Fingerprint of exact committed generation, plan revision, owner receipts, crosswalk result and visibility.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### generation_committed_at

UTC time visibility and mapping receipt committed.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### owner_stage_receipts

One protected, independently verified receipt per required owner. No owner draft may surface before the generation visibility decision.

Optional. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "owner": {
        "type": "string",
        "minLength": 1,
        "maxLength": 80
      },
      "baseline_digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      },
      "stage_receipt_id": {
        "type": "string",
        "format": "uuid"
      },
      "stage_receipt_digest": {
        "type": "string",
        "pattern": "^[a-f0-9]{64}$"
      }
    },
    "required": [
      "owner",
      "baseline_digest",
      "stage_receipt_id",
      "stage_receipt_digest"
    ],
    "additionalProperties": false
  },
  "maxItems": 32,
  "minItems": 1,
  "uniqueItems": false
}
```

### selection_manifest_id

Immutable protected archive-export selection, including exact source revisions, option choices, rights snapshots and receiving profile. Validate the stored representation with export-projection.schema.json and its owning command.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### export_profile_revision

Pinned approved egress profile revision. Review is repeated if target format or profile changes.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### export_edition

Exact output edition validated independently from inbound format detection.

Optional. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native_1",
    "olx_course_1",
    "olx_legacy_library_1",
    "olx_library_archive_1",
    "scorm_1_2",
    "scorm_2004_2",
    "scorm_2004_3",
    "scorm_2004_4",
    "qti_2_1",
    "qti_2_2",
    "qti_3_0_1",
    "common_cartridge_1_3"
  ]
}
```

### capability_report_id

Protected immutable capability projection keyed to exact source selection, generator and destination. Validate the stored representation with export-projection.schema.json and its owning command.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### capability_report_digest

Verified digest of exact capability decisions.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### loss_report_id

Protected immutable loss report for that projection. A zero-loss report is still required. Validate the stored representation with export-projection.schema.json and its owning command.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### loss_report_digest

Verified digest of exact loss decisions and required feature blockers.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### export_validation_report_id

Immutable protected artifact validation and independent profile test evidence. Validate the stored representation with export-projection.schema.json and its owning command.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### export_validation_report_digest

Verified validation report digest for exact output bytes and selected profile.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### export_result_storage_id

Protected clean immutable output owned by this completed export job. Absent while queued or under review.

Optional. Null is rejected.

References [StorageObject](StorageObject.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### export_result_digest

SHA-256 of the generated output bytes.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### export_result_bytes

Measured positive byte length of the verified output.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### export_expires_at

Exclusive authorized output collection expiry. Does not dispose underlying academic records.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### export_completed_at

Authoritative UTC instant result validation and availability were committed.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### fence_epoch

Monotonic worker ownership epoch.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### worker_key

Authenticated worker lease owner.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 128
}
```

### lease_expires_at

UTC fencing deadline.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### checkpoint

Opaque resumable partition and item position, excludes learner payload.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### revision

Monotonic aggregate revision used for compare-and-swap.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "received",
    "quarantined",
    "validated",
    "staged",
    "awaiting_review",
    "approved",
    "applying",
    "applied",
    "failed",
    "cancelled"
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

### updated_at

Server time of last transition.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Import requires an artifact and export requires an immutable selection.
- Only the active fence can checkpoint or alter the plan.
- A changed plan digest invalidates all previous approvals.
- Every import after inspection pins source container, source profile and immutable inspection manifest. A staged import pins selected roots, dependency artifact digests and plan revision.
- Import dry run does not create owner-visible drafts, active crosswalks, generation commitments or learner effects.
- A generation can commit once. Require all exact owner receipts and active approvals, then publish private editor visibility or an explicitly authorized activation barrier with crosswalk receipts. No partial root is visible.
- Export uses a direction-enabled exact format, edition and profile revision. The selection is immutable. Required losses and missing disclosure or rights approvals block result availability.
- An applied export has one protected output, validation receipt and collection expiry. Retrying completion returns the same result. A generated or expired output cannot be redownloaded solely by knowing its UUID.
- The current plan manifest pins its exact graph or export reports and predecessor manifest. A replaced private generation remains closed and cannot be resumed under a successor plan.
- Every selected root names its exact same-plan TransferRecord, so dependent reachability is reproducible for each selected root.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, updated_at | Find reviewer and worker queues. |
| state, lease_expires_at | Find claimable expired worker leases. |
| institution_id, generation_id | Resolve immutable generation receipt across fenced retries. |
| institution_id, direction, state, export_expires_at | Find completed export artifacts approaching collection expiry. |

## Retention

Retain job, decision history and published owner receipts for seven years by default. Expire failed private staging after 30 days unless held.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| received | quarantined | InspectTransferArtifact | Artifact assembled and worker holds current fence. Record scan and archive limits. |
| quarantined | validated | InspectTransferArtifact | Format and schema checks pass. Pin adapter and typed source graph. |
| validated | staged | BuildTransferPlan | Every source record counted and candidate objects staged. Pin baseline revisions and plan fingerprint. |
| staged | awaiting_review | BuildTransferPlan | Report and stage artifacts durable. Expose scoped review. |
| awaiting_review | approved | ApproveTransferPlan | Required reviewers approve exact plan and no blocker remains. Write immutable approval. |
| approved | applying | ApplyTransferPlan | Approval and plan revision remain current. Stage owner receipts behind publication barrier. |
| applying | applied | ApplyTransferPlan | All owners confirm the staged generation and baseline. Commit exactly one private or separately authorized activated generation with baseline, crosswalk and owner receipts. |
| applying | awaiting_review | ApplyTransferPlan | One baseline changed before activation. Keep staging private and invalidate prior approvals. |
| awaiting_review | staged | ResolveTransferIssue | Review decision changes candidate projections. Rebuild affected records and increment plan revision. |
| awaiting_review | cancelled | CancelTransferJob | Requester authorized and no visible commit exists. Revoke stage grants. |
| received | awaiting_review | RecordCurriculumExportProjection | Export worker is current and protected reports match exact frozen selection. Pin immutable capability and loss reports and plan revision without making a result available. |
| awaiting_review | awaiting_review | RecordCurriculumExportProjection | An authorized private reprojection changes decisions or has an identical receipt. Replay same reports or append a new projection revision and invalidate approvals for changed results. |
| approved | applying | CompleteCurriculumExport | Worker fence and current approved export profile and projection match. Verify restricted generated artifact and independent validation evidence. |
| applying | applied | CompleteCurriculumExport | Exact output bytes, validation results and release gates are verified. Commit export receipt and short-lived collection eligibility in one durable transaction. |
