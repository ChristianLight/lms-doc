# CompetencyFrameworkVersion

Published versioned institutional skill or academic standards hierarchy.

Owned by **records**.

## Fields

### id

Stable globally unique CompetencyFrameworkVersion identifier.

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

### framework_key

Stable framework family.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### revision

Monotonic immutable revision number within its stable identity.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### created_at

Authoritative recorded creation instant.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

### title

Approved framework title.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### locale

Source definition locale.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 2,
  "maxLength": 35,
  "pattern": "^[A-Za-z0-9-]+$"
}
```

### external_identifier

Verified external standard identifier, if any.

Required. Nullable.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 500
}
```

### issuer_name

Issuing authority label.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 200
}
```

### state

Framework publishing lifecycle.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "superseded",
    "retired"
  ],
  "default": "draft"
}
```

### structure_digest

Approved hierarchy and edges digest.

Required. Nullable.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

### actor_id

Authorized actor within institution at decision time.

Required. Null is rejected.

References [Principal](Principal.md). Authorized actor within institution at decision time.

```json
{
  "type": "string",
  "format": "uuid"
}
```

## Integrity

- Prerequisite and aggregate edges acyclic.
- Source lineage and prior version persist.

## Unique keys

- `id`
- `institution_id, framework_key, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, state, framework_key | Select published competency frameworks. |

## Retention

Retain while a referenced academic decision, publication or document is retained. Apply institution retention and holds before disposition.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishCompetencyFramework | Topology, policy and source scope verified Freeze framework and competencies. |
