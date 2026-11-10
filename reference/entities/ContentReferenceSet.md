# ContentReferenceSet

Complete, owner-fenced derived relationship coverage for one exact definition and optional publication placement context.

Owned by **platform**.

## Fields

### id

Platform-assigned application identity; remains stable while this logical reference set is refreshed.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Institution containing the source and its private relation index.

Required. Null is rejected.

References [Institution](Institution.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_kind

Allowlisted source owner record kind; select a fixed resolver, never a client-provided SQL table.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "ContentNodeVersion",
    "ActivityVersion",
    "ItemVersion",
    "ItemTranslation",
    "ItemStimulusVersion",
    "MarkingRuleVersion",
    "RubricVersion",
    "LearningRuleVersion",
    "InteractionDefinition",
    "ItemFeedbackRule"
  ]
}
```

### source_version_id

Exact source row or revision ID for source_kind. Verify through the registered typed resolver; content equality is not identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### context_kind

Definition extraction or binding of that definition in one exact course placement.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "definition",
    "placement"
  ]
}
```

### context_key

Non-null unique context: literal definition, or lower-case canonical UUID of source_placement_id. It is not an ordinal or URL.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 48
}
```

### course_version_id

Required only for placement binding; exact frozen or staged target course graph.

Optional. Null is rejected.

References [CourseVersion](CourseVersion.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### source_placement_id

Required only for placement binding; its transitive dependency closure must pin the named source version.

Optional. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### definition_set_id

Required only for placement binding; corresponding current definition set for exactly the same source owner and version.

Optional. Null is rejected.

References [ContentReferenceSet](ContentReferenceSet.md). Resolve the exact referenced record through its registered owner and prove the same institution and captured version context before write or use.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### definition_generation

Definition generation used for this binding. A newer definition generation invalidates it.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### source_digest

Canonical owner payload and reference-bearing metadata digest captured for this generation.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### graph_digest

Required for placement binding; exact publication graph and stable placement-key mapping digest.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### projection_profile

Versioned reference extraction rules and canonical key encoding profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

### generation

Owner-fenced generation. Entries and completion receipt must agree with it.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### revision

Optimistic token for operational refresh and invalidation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### state

Ready means complete coverage including a validated zero-reference result; it does not grant reader authority.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pending",
    "ready",
    "stale",
    "failed"
  ]
}
```

### entry_count

Exact active generation entry count; zero is meaningful only with ready state.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 100000
}
```

### entries_digest

Canonical sorted semantic references digest, including the empty collection when appropriate.

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### validated_at

Server time when captured source, graph and complete entry generation were checked.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### last_error_code

Fixed non-content-bearing reconciliation code. No raw source text or locators.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

## Integrity

- Resolve source_kind through a fixed owner registry and verify source_version_id, its institution and current owner digest. No index row authenticates or authorizes source access.
- A definition context has no placement fields. A placement context has all placement fields, context_key equals the exact source placement UUID, and its dependency closure pins this exact source version.
- Ready means every schema-declared reference is extracted, target checked and represented, including an exact empty set. Published placement sets contain no unresolved required target selectors.
- A source or graph mutation must mark this set and affected bindings stale in the same authoritative transaction, or refresh them there. Independent remote transactions require a publication barrier and fail-closed destructive operations.
- Do not infer global coverage from the existing rows. Before target deletion, the owner-defined census of all retained reference-bearing source versions must match ready sets or be replaced by an equivalent authoritative locked scan.
- Complete generation replacement, row count, entries digest, source token check and ready transition commit atomically. A partial build never advances the ready receipt.
- Reference creation and target deletion acquire the same target retention fence. The fence prevents a concurrent new reference from appearing after the deletion census.
- Source retirement may remove the set only after authoritative source retention ends. Index rows are rebuildable and cannot remove historic source or target evidence.
- A placement refresh verifies the corresponding definition set is ready with matching source digest and projection profile, and pins its generation under the same lock/recheck barrier. Source digest equality alone does not prove definition generation equality.
- Definition sets contain placement_selector rows when a stable same-course link remains context-dependent. Exact target_placement_id rows belong only to a placement context; a required placement selector cannot survive as unresolved in that context.
- The complete source census includes registered LearningRuleVersion selectors and InteractionDefinition configuration references as well as visible prose. Protected marking/feedback and teacher-only references remain under their source owner disclosure policy.

## Unique keys

- `id`
- `institution_id, source_kind, source_version_id, context_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, validated_at | Find stale or incomplete sets without scanning private content. |
| definition_set_id, definition_generation | Invalidate placement bindings when their definition projection changes. |
| course_version_id, state | Check exact publication graph readiness. |

## Retention

Retain while the exact source version or its publication binding remains retained. Rebuild on corruption; owner audit records retain refresh or invalidation decisions separately.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| pending | ready | RefreshContentReferenceSet | Complete source and reference validation committed. Increment revision and persist complete generation or stale marker with durable owner event; preserve authoritative source. |
| ready | stale | InvalidateContentReferenceSet | Source or graph dependency changes under owner fence. Increment revision and persist complete generation or stale marker with durable owner event; preserve authoritative source. |
| stale | ready | RefreshContentReferenceSet | New captured generation fully reconciled. Increment revision and persist complete generation or stale marker with durable owner event; preserve authoritative source. |
| failed | ready | RefreshContentReferenceSet | Failure corrected and source digest still current. Increment revision and persist complete generation or stale marker with durable owner event; preserve authoritative source. |
