# RosterSnapshot

Privately staged authoritative or delta roster data and reconciliation baseline.

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

### feed_id

Owning feed.

Required. Null is rejected.

References [RosterFeed](RosterFeed.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### artifact_id

Input bytes or canonical API collection snapshot.

Required. Null is rejected.

References [TransferArtifact](TransferArtifact.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### sequence

Source or connector monotonic snapshot generation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### mode

Normative feed effect semantics.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "bulk",
    "delta"
  ]
}
```

### scope_complete

True only after full declared file or page set validation.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### record_count

Total verified source records.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 5000000
}
```

### proposed_withdrawal_count

Count from approved baseline, awaiting explicit review where required.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 5000000
}
```

### projection_digest

Exact reconciled graph and baseline digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[0-9a-f]{64}$"
}
```

### baseline_feed_revision

Revision before stage.

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
    "staged",
    "review",
    "applied",
    "failed"
  ]
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

### created_at

Server-assigned UTC time of creation.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Bulk deletes are never inferred until scope completeness and source authority are proven.
- Apply owner changes and feed watermark together.

## Unique keys

- `id`
- `feed_id, sequence`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| feed_id, state | Review staged roster generations before activation. |

## Retention

Retain approved reconciliation evidence. Expire raw roster payloads after 30 days by default once recovery and holds permit.
