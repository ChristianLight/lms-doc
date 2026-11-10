# CollaborationSpaceLink

Scoped provider resource mapping and synchronization state.

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

### offering_id

Owning delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Must resolve to an authorized CourseOffering in the owning institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### audience

Effective local launch scope.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "kind": {
      "type": "string",
      "enum": [
        "offering",
        "section",
        "learning_group",
        "enrollment"
      ]
    },
    "id": {
      "type": "string",
      "format": "uuid"
    }
  },
  "required": [
    "kind",
    "id"
  ],
  "additionalProperties": false
}
```

### purpose

Provider function.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "discussion",
    "meeting",
    "folder",
    "staff_room"
  ]
}
```

### connection_id

Registered connection that owns provider credential and permission scope.

Required. Null is rejected.

References [IntegrationConnection](IntegrationConnection.md). Same institution as offering, state and allowed actions must permit purpose.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### external_resource_map_id

Platform-owned desired and observed external identity for this space.

Optional. Nullable.

References [ExternalResourceMap](ExternalResourceMap.md). Map local type CollaborationSpaceLink and local ID this link, with same connection and institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### desired_revision

Latest effective roster change.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647,
  "default": 1
}
```

### observed_revision

Last reconciled provider state.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 2147483647,
  "default": 0
}
```

### state

Integration state.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "pending",
    "synced",
    "degraded",
    "retrying",
    "retired"
  ],
  "default": "pending"
}
```

### next_retry_at

Bounded retry schedule.

Optional. Nullable.

```json
{
  "type": "string",
  "format": "date-time"
}
```

## Integrity

- Unique connection and audience and purpose across active links.
- Local launch rechecks current participation even if remote removal is delayed.
- Remote identifiers and actual observed provider effect state are derived through the typed external map. Local revisions govern academic launch.

## Unique keys

- `id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, purpose, state | Scoped communication workspace. |
| state, next_retry_at | Provider retry and revocation monitoring. |

## Retention

Retain for the configured operational interval. Purge or de-identify after expiry when no academic reference or hold applies.
