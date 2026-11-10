# StickyGateDecision

Evidence snapshot retained after an eligible activity first started with sticky continuity.

Owned by **participation**.

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

### enrollment_release_id

Exact learner publication assignment.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Must resolve to an authorized EnrollmentRelease in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Exact activity placement.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Exact placement must belong to the version pinned to the EnrollmentRelease.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### rule_version_id

Approved continuity policy.

Required. Null is rejected.

References [LearningRuleVersion](LearningRuleVersion.md). Must resolve to an authorized LearningRuleVersion in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### basis_digest

Canonical safe evidence and decision snapshot.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### source_record_ids

Authorized authoritative evidence, result or approval references.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 200,
  "minItems": 0
}
```

### first_started_at

Server action instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### state

Sticky decision availability.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "withdrawn"
  ],
  "default": "active"
}
```

## Integrity

- Only eligible native non-assessment activity can create ordinary sticky authorization.
- Withdrawal or safety can supersede without deleting decision basis.

## Unique keys

- `id`
- `enrollment_release_id, content_placement_id, rule_version_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| enrollment_release_id, content_placement_id | Fast sticky decision lookup. |

## Retention

Retain with scoped academic record history while referenced and through the institutional retention window or any hold.
