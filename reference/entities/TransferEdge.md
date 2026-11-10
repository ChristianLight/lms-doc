# TransferEdge

One typed relationship occurrence from a source record to a version-pinned destination, before native owner promotion.

Owned by **interoperability**.

## Fields

### id

Opaque immutable identity of the relationship occurrence.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### job_id

Owning transfer job.

Required. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### plan_revision

Frozen plan revision containing the source and any local target.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### from_record_id

Source record in the same frozen plan.

Required. Null is rejected.

References [TransferRecord](TransferRecord.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### edge_key

Adapter-owned exact semantic relationship occurrence key within the source record. Distinct from a display label or target ID.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### kind

Typed owner projection relationship. An ordinary hyperlink cannot be evaluated as a prerequisite.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "containment",
    "definition",
    "asset_use",
    "internal_link",
    "prerequisite",
    "library_pin",
    "assessment_binding",
    "grade_binding",
    "package_dependency",
    "translation",
    "policy_binding"
  ]
}
```

### required

Required for this source occurrence's selected deliverable. The plan separately computes reachability.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### ordinal

Order only where semantic order exists, such as outline containment or authored reference use.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### source_locator

Restricted original source location used for adjudication. Never emit it in a broad event.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 1024
}
```

### placement_context_record_id

Exact source placement occurrence that supplies context to a placement-sensitive relative link or policy.

Optional. Null is rejected.

References [TransferRecord](TransferRecord.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_source

Typed unresolved source resolver intent with optional layer, occurrence and revision pins.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "source_scope": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "object_kind": {
      "type": "string",
      "minLength": 1,
      "maxLength": 64
    },
    "source_key": {
      "type": "string",
      "minLength": 1,
      "maxLength": 512
    },
    "source_layer": {
      "type": "string",
      "enum": [
        "published",
        "draft",
        "shared"
      ]
    },
    "occurrence_key": {
      "type": "string",
      "minLength": 1,
      "maxLength": 256
    },
    "source_revision": {
      "type": "string",
      "minLength": 1,
      "maxLength": 128
    }
  },
  "required": [
    "source_scope",
    "object_kind",
    "source_key"
  ],
  "additionalProperties": false
}
```

### target_record_id

Resolved candidate target inside the same job and plan revision.

Optional. Null is rejected.

References [TransferRecord](TransferRecord.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_map_id

Reviewed, currently authorized same-institution external target binding used instead of a local record.

Optional. Null is rejected.

References [ExternalObjectMap](ExternalObjectMap.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### target_version_id

Exact canonical target revision when pinned after verified resolution. Owner validates the polymorphic kind.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### resolution

Primary verified resolution or blocking/optional disposition.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "resolved_local",
    "resolved_external",
    "unresolved",
    "ambiguous",
    "rejected",
    "accepted_optional_exclusion"
  ]
}
```

### issue_id

Current same-job issue documenting ambiguous, rejected or missing required resolution.

Optional. Null is rejected.

References [TransferIssue](TransferIssue.md). Reference must resolve within the same Institution and exact approved job or resource generation as described.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Resolved local edges name exactly one same-plan target record. Resolved external edges name exactly one same-institution authorized external map. Unresolved, ambiguous and rejected edges name neither.
- Required resolved dependency must retain an exact approved target version before promotion. No title, guessed path or matching digest silently resolves an edge.
- Containment and prerequisite graphs are validated as separate cycle-sensitive relation sets. Ordinary hyperlinks can be reciprocal.
- The same source reusable definition can create distinct context-specific edges from distinct placement records. Sharing a target does not merge edge occurrence identity.
- Edge order and target baseline are immutable for the current plan. Remediation produces a successor plan and new scope review.

## Unique keys

- `id`
- `job_id, plan_revision, from_record_id, edge_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| job_id, plan_revision, from_record_id, kind, ordinal | Read ordered and contextual outgoing relationships. |
| job_id, plan_revision, target_record_id, kind | Trace reverse dependency closure before releasing or replacing a target. |
| job_id, plan_revision, resolution, required | Find unresolved relationship blockers for review. |

## Retention

Retain applied graph and reviewed edges with transfer provenance. Expire abandoned private staging after the approved schedule and any active hold.
