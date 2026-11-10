# GradeContribution

Traceable result contribution or exclusion decision.

Owned by **records**.

## Fields

### id

Stable globally unique GradeContribution identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### institution_id

Owning institution. All scoped references resolve inside it.

Required. Null is rejected.

References [Institution](Institution.md). Owning institution. All scoped references resolve inside it.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering within the same institution.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering within the same institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### result_revision_id

Computed revision in same offering.

Required. Null is rejected.

References [GradeResultRevision](GradeResultRevision.md). Computed revision in same offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### ordinal

Deterministic order within explanation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 10000
}
```

### grade_item_id

Line supplying a direct leaf if applicable.

Required. Nullable.

References [GradeItem](GradeItem.md). Line supplying a direct leaf if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### evidence_id

Original accepted evidence for leaf when applicable.

Required. Nullable.

References [GradeEvidence](GradeEvidence.md). Original accepted evidence for leaf when applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### child_revision_id

Exact aggregate or item child revision, if applicable.

Required. Nullable.

References [GradeResultRevision](GradeResultRevision.md). Exact aggregate or item child revision, if applicable.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### completion_record_id

Exact immutable accepted completion revision for same enrollment, offering and placement when completion is the source.

Required. Nullable.

References [CompletionRecord](CompletionRecord.md). Exact immutable accepted completion revision for same enrollment, offering and placement when completion is the source.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### coverage_snapshot_id

Pinned applicability and source-coverage snapshot, mandatory for missing_zero.

Required. Nullable.

References [GradeCoverageSnapshot](GradeCoverageSnapshot.md). Pinned applicability and source-coverage snapshot, mandatory for missing_zero.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### disposition

Precise use or exclusion reason.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "counted",
    "dropped",
    "bonus",
    "excused",
    "inapplicable",
    "unreleased",
    "pending",
    "missing_zero",
    "superseded",
    "technical_exception",
    "excluded_formative"
  ]
}
```

### ratio

Adjusted exact contributor ratio when applicable.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### configured_weight

Configured denominator contribution before exclusions.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### used_weight

Exact applied contribution or null when excluded.

Required. Nullable.

```json
{
  "type": "object",
  "properties": {
    "numerator": {
      "type": "string",
      "pattern": "^(0|[1-9][0-9]{0,19727})$"
    },
    "denominator": {
      "type": "string",
      "pattern": "^[1-9][0-9]{0,19727}$"
    }
  },
  "required": [
    "numerator",
    "denominator"
  ],
  "additionalProperties": false
}
```

### effective_due_at

Pinned approved deadline used for calculation.

Required. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### late_deduction

Deduction in points before selection.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^(?:(?:0|[1-9][0-9]{0,5})(?:\\.[0-9]{0,5}[1-9])?|1000000)$"
}
```

### reason_code

Safe localized explanation key.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9._-]{0,63}$"
}
```

## Integrity

- Cannot disclose hidden evidence through learner explanation.
- Child link cannot create a calculation cycle.
- At most one of evidence, child revision and completion record is set per contribution. A counted, dropped or bonus decision needs exactly one, except a confirmed missing zero needs a coverage snapshot.
- Validate immutable completion source owner, enrollment release, activity scope and exact revision at cutoff. An incomplete or revoked completion is never an authorized passing grade.
- A completion source cannot depend directly or transitively on the grade it supplies.

## Unique keys

- `id`
- `result_revision_id, ordinal`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| evidence_id, result_revision_id | Find academic decisions affected by score correction. |
| completion_record_id, result_revision_id | Find academic decisions affected by completion correction. |
| result_revision_id, disposition | Present lineage filtered by recipient scope. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.
