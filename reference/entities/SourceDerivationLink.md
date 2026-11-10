# SourceDerivationLink

Immutable protected claim-level provenance edge from a source region or approved generated origin to a candidate and optionally exact learning target.

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

### authoring_run_id

Exact authoring run scope.

Required. Null is rejected.

References [CurriculumAuthoringRun](CurriculumAuthoringRun.md). Must resolve to an authorized CurriculumAuthoringRun in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_region_id

Exact accepted source region when the classification requires one.

Optional. Nullable.

References [SourceRegion](SourceRegion.md). Must be a sealed accepted region in the run exact source set and still readable under the source rights and scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### candidate_id

Stable candidate identity inside the run.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### candidate_revision

Exact immutable candidate revision.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000000
}
```

### candidate_digest

Canonical candidate revision checksum.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### target_kind

Candidate-only or exact owner version target.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "candidate",
    "content_node_version",
    "activity_version",
    "asset_version",
    "item_version",
    "marking_rule_version",
    "assessment_version",
    "course_version"
  ]
}
```

### content_node_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [ContentNodeVersion](ContentNodeVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [ActivityVersion](ActivityVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### asset_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [AssetVersion](AssetVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### item_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [ItemVersion](ItemVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### marking_rule_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [MarkingRuleVersion](MarkingRuleVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [AssessmentVersion](AssessmentVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### course_version_id

Optional exact owner target version selected by target_kind.

Optional. Nullable.

References [CourseVersion](CourseVersion.md). Same institution and authorized target ancestry. Exact revision must match the authenticated owner receipt.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_path

Canonical RFC 6901 JSON Pointer into the authorized target or candidate; use empty pointer for whole object.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 500
}
```

### classification

Relationship of claim to source and author action.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "extracted",
    "source_supported_paraphrase",
    "derived",
    "generated_instruction",
    "human_supplied",
    "unresolved"
  ]
}
```

### link_fingerprint

Canonical uniqueness key over target, region, claim type, candidate revision and derivation group.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### derivation_group_id

Groups independently indexed premise edges for the same claim.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### verification_object_id

Protected rule, computation result, human decision or verification report.

Optional. Nullable.

References [StorageObject](StorageObject.md). Same institution. Platform purpose evidence and exact owner CurriculumAuthoringRun. Resolve actual object version and digest before use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### disclosure

Default no raw source projection.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "staff_only",
    "approved_attribution"
  ],
  "default": "staff_only"
}
```

### recorded_by_id

Authorized source or owner receipt actor.

Required. Null is rejected.

References [Principal](Principal.md). Must resolve to an authorized Principal in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### created_at

Append time.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Extracted, source-supported paraphrase and derived links require an accepted source region.
- Derived links require a protected computation or review basis. One edge per accepted source premise; common derivation group binds premises.
- Candidate-only target has no owner reference. An exact target must populate only the typed ID matching target kind.
- No direct learner reads. Approved attribution is a separately filtered projection, with answer-key and source access enforced.

## Unique keys

- `id`
- `authoring_run_id, link_fingerprint`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| source_region_id, created_at | Reverse dependency and source-rights withdrawal impact. |
| authoring_run_id, candidate_id, candidate_revision | Exact candidate traceability. |
| content_node_version_id, created_at | Inspect authorized exact target lineage. |
| activity_version_id, created_at | Inspect authorized exact target lineage. |
| asset_version_id, created_at | Inspect authorized exact target lineage. |
| item_version_id, created_at | Inspect authorized exact target lineage. |
| marking_rule_version_id, created_at | Inspect authorized exact target lineage. |
| assessment_version_id, created_at | Inspect authorized exact target lineage. |
| course_version_id, created_at | Inspect authorized exact target lineage. |

## Retention

Retain protected decisions while needed for reviewed source derivation and retention policy or hold. Retain authorized academic lineage tombstone after eligible source disposition.
