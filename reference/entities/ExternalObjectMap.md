# ExternalObjectMap

Stable crosswalk between one source namespace and one canonical owner object.

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

### source_namespace

Registered and verified authoritative source.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### source_profile

Registered source identity profile. Container variants of the same decoding profile do not create separate identities.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-z][a-z0-9_.-]{0,55}/[0-9a-z][0-9a-z_.-]{0,31}$"
}
```

### source_scope

Stable source parent scope or root sentinel.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### object_kind

Registered mapped canonical type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### external_key

Exact source identifier retained as an opaque value.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### record_role

Stable crosswalk role distinguishing definitions from their placement and reference occurrences.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "definition",
    "placement",
    "asset",
    "policy",
    "reference",
    "package",
    "document"
  ]
}
```

### occurrence_key

Stable occurrence key in the approved source scope, or explicit definition sentinel. A changed ordinal alone cannot retarget an existing mapping.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```

### target_kind

Canonical owner entity type.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 64
}
```

### target_id

Canonical owner entity UUID, validated via owner adapter.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### baseline_tracks

Separate last approved source and target pair by publication layer. Published and draft tracks for one definition keep the same canonical identity.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "published": {
      "type": "object",
      "properties": {
        "source_revision": {
          "type": "string",
          "minLength": 1,
          "maxLength": 128
        },
        "source_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "target_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "job_id": {
          "type": "string",
          "format": "uuid"
        },
        "roster_snapshot_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "source_revision",
        "source_fingerprint",
        "target_fingerprint"
      ],
      "additionalProperties": false,
      "oneOf": [
        {
          "required": [
            "job_id"
          ],
          "not": {
            "required": [
              "roster_snapshot_id"
            ]
          }
        },
        {
          "required": [
            "roster_snapshot_id"
          ],
          "not": {
            "required": [
              "job_id"
            ]
          }
        }
      ]
    },
    "draft": {
      "type": "object",
      "properties": {
        "source_revision": {
          "type": "string",
          "minLength": 1,
          "maxLength": 128
        },
        "source_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "target_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "job_id": {
          "type": "string",
          "format": "uuid"
        },
        "roster_snapshot_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "source_revision",
        "source_fingerprint",
        "target_fingerprint"
      ],
      "additionalProperties": false,
      "oneOf": [
        {
          "required": [
            "job_id"
          ],
          "not": {
            "required": [
              "roster_snapshot_id"
            ]
          }
        },
        {
          "required": [
            "roster_snapshot_id"
          ],
          "not": {
            "required": [
              "job_id"
            ]
          }
        }
      ]
    },
    "shared": {
      "type": "object",
      "properties": {
        "source_revision": {
          "type": "string",
          "minLength": 1,
          "maxLength": 128
        },
        "source_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "target_fingerprint": {
          "type": "string",
          "pattern": "^[a-f0-9]{64}$"
        },
        "job_id": {
          "type": "string",
          "format": "uuid"
        },
        "roster_snapshot_id": {
          "type": "string",
          "format": "uuid"
        }
      },
      "required": [
        "source_revision",
        "source_fingerprint",
        "target_fingerprint"
      ],
      "additionalProperties": false,
      "oneOf": [
        {
          "required": [
            "job_id"
          ],
          "not": {
            "required": [
              "roster_snapshot_id"
            ]
          }
        },
        {
          "required": [
            "roster_snapshot_id"
          ],
          "not": {
            "required": [
              "job_id"
            ]
          }
        }
      ]
    }
  },
  "required": [],
  "additionalProperties": false,
  "minProperties": 1
}
```

### last_job_id

Successful curriculum transfer receipt for the last accepted import baseline. Absent for provider roster mappings.

Optional. Null is rejected.

References [TransferJob](TransferJob.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### last_roster_snapshot_id

Applied roster snapshot receipt for the last accepted feed baseline. Absent for curriculum imports.

Optional. Null is rejected.

References [RosterSnapshot](RosterSnapshot.md). Resolve same-institution authorized RosterSnapshot for the exact verified source authority.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "retired",
    "merge_pending"
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

### updated_at

Last authoritative mapping update.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Crosswalk updates require source authority and matching target baseline.
- Multiple aliases may identify one native object, but one source tuple cannot identify multiple current targets.
- A re-import compares only the matching accepted layer baseline. Local divergence does not advance the baseline or erase published history.
- A fork creates an independently scoped source branch or target lineage. It never silently retargets the existing active crosswalk.
- Each committed baseline retains exactly one transfer or roster application receipt. A roster or operational baseline uses the shared track and cannot mutate curriculum publication tracks.

## Unique keys

- `id`
- `institution_id, source_namespace, source_profile, source_scope, object_kind, external_key, record_role, occurrence_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, target_kind, target_id | Find reverse provenance for an owner object. |

## Retention

Keep active aliases while referenced. Keep retirement tombstones to prevent source ID reuse for seven years by default.
