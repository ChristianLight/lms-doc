# AssessmentSlot

Fixed item or approved pool placement in the exact assembly.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentSlot identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Assembly containing the slot.

Required. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Assembly containing the slot.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### section_version_id

Section of the same AssessmentVersion.

Required. Null is rejected.

References [AssessmentSectionVersion](AssessmentSectionVersion.md). Section of the same AssessmentVersion.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### key

Unique local slot identity.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[A-Za-z][A-Za-z0-9_-]{0,63}$"
}
```

### display_order

Distinct slot order within its section.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### fixed_item_version_id

Published fixed item approved for reuse.

Optional. Nullable.

References [ItemVersion](ItemVersion.md). Published fixed item approved for reuse.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### pool_version_id

Published pool permitted in this scope.

Optional. Nullable.

References [ItemPoolVersion](ItemPoolVersion.md). Published pool permitted in this scope.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### variant_profile_id

Approved generator when the fixed slot selects one.

Optional. Nullable.

References [VariantProfileVersion](VariantProfileVersion.md). Approved generator when the fixed slot selects one.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### occurrences

Number of selected item occurrences.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 1000000
}
```

### maximum

Maximum per occurrence in assessment scale.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?!-0(?![\\s\\S]))-?(0|[1-9][0-9]{0,8})(\\.[0-9]{0,5}[1-9])?(?![\\s\\S])"
}
```

### required

Whether all resolved criteria require disposition.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### shuffle_choices

Allow per-attempt option permutation.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

## Integrity

- Exactly one of fixed item and pool selected.
- Occurrences is 1 to 500, with fixed item default 1.
- Zero maximum is permitted only for ungraded slots.

## Unique keys

- `id`
- `assessment_version_id, key`
- `section_version_id, display_order`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| section_version_id, display_order | Resolve section slots in author order. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.
