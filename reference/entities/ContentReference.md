# ContentReference

Typed, rebuildable relation extracted from one captured native definition or resolved publication use.

Owned by **platform**.

## Fields

### id

Derived row identity. Never use it as an authored link or student progress identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### set_id

Exact parent set controlling institution, owner, context and visibility.

Required. Null is rejected.

References [ContentReferenceSet](ContentReferenceSet.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### generation

Parent generation this derived row belongs to.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### reference_key

Owner-local semantic key under the projection profile. Use an explicit typed local key where present; otherwise derive from locale, stable containing block or interaction key, relation role and canonical target plus anchor, with deterministic multiplicity suffix for identical edges. Array position or label alone is not identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256,
  "pattern": "^[A-Za-z0-9._:/@-]+$"
}
```

### reference_key_digest

SHA-256 of exact UTF-8 semantic key under the declared profile; compare full keys on collision.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### field_pointer

RFC6901 pointer locating the reference in captured normalized owner payload. Diagnostic location, never identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "maxLength": 2048,
  "pattern": "^(?:/(?:[^~/]|~[01])*)*$"
}
```

### relation

Typed relation discriminator; exactly its corresponding target field is populated.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "asset",
    "content_definition",
    "activity_definition",
    "assessment",
    "package",
    "external_resource",
    "placement",
    "placement_selector"
  ]
}
```

### required_for_publication

Source owner policy classification; not chosen by the projection caller.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### anchor

Validated target-local fragment, retained independently of canonical target identity.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### asset_version_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [AssetVersion](AssetVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_node_version_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [ContentNodeVersion](ContentNodeVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [ActivityVersion](ActivityVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### package_version_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [PackageVersion](PackageVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_resource_map_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [ExternalResourceMap](ExternalResourceMap.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_placement_id

Exact authorized target version or placement; never substitute a mutable latest pointer.

Optional. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_selector

Deferred same-course stable placement selector in a definition set. It must be resolved in every required publication binding.

Optional. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "placement_key": {
      "type": "string",
      "format": "uuid"
    },
    "context": {
      "const": "same_course_version"
    }
  },
  "required": [
    "placement_key",
    "context"
  ],
  "additionalProperties": false
}
```

## Integrity

- Exactly the target field selected by relation exists; absent alternatives are omitted rather than null.
- Generation equals the ready parent set generation whenever this row is used as complete dependency evidence.
- Derive semantic key and field pointer from schema-declared owner content. Reject duplicate keys, hash collision, unresolved typed target or source outside the institution.
- Placement selectors are allowed only in definition sets. Placement sets resolve them to exact target placement in the same CourseVersion, with the original anchor. Cross-course links require a separately implemented capability and cannot be silently promoted.
- Non-placement exact targets are reauthorized by their owner for every user read and export. Presence in a source or reverse relation list grants no access.
- A target asset withdrawal can disable delivery while retention still protects the historical bytes. Dependency existence is not a license or a current publication permission.
- Raw URLs, auth tokens, answer text and copied learner data are excluded. External targets use an approved ExternalResourceMap identity.
- Native owner payloads remain the editing and rendering authority. Projection entries are regenerated by registered owner readers, not manually edited.
- Anchor is stored only in the top-level anchor field. The target selector contains no second anchor location.
- Direct approved HTTPS literals remain validated editorial link values. Only provider-managed dependencies with an actual ExternalResourceMap receive external_resource rows; never create a provider mapping solely to index an ordinary website link.

## Unique keys

- `id`
- `set_id, generation, reference_key_digest`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| set_id, generation | Read or replace one complete generation in semantic-key order. |
| asset_version_id, set_id | Find exact reverse dependencies on AssetVersion. |
| content_node_version_id, set_id | Find exact reverse dependencies on ContentNodeVersion. |
| activity_version_id, set_id | Find exact reverse dependencies on ActivityVersion. |
| assessment_version_id, set_id | Find exact reverse dependencies on AssessmentVersion. |
| package_version_id, set_id | Find exact reverse dependencies on PackageVersion. |
| external_resource_map_id, set_id | Find exact reverse dependencies on ExternalResourceMap. |
| target_placement_id, set_id | Find exact reverse dependencies on ContentPlacement. |

## Retention

Retain the active generation while its source set is retained. Obsolete rebuild generations may be deleted after committed replacement; preserve audit evidence outside this projection.
