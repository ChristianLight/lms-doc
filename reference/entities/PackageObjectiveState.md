# PackageObjectiveState

Tracked local or shared objective state with independent knownness flags.

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

### registration_id

Registration required for attempt-lifetime state, absent for a verified cross-attempt learner scope.

Optional. Null is rejected.

References [PackageRegistration](PackageRegistration.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_attempt_id

Owning local activity attempt when not shared.

Optional. Null is rejected.

References [PackageActivityAttempt](PackageActivityAttempt.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### objective_scope

Whether objective uses local or explicitly mapped shared scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "local",
    "shared"
  ]
}
```

### external_key

Exact objective identifier in its configured scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### satisfaction_known

True when satisfaction flag is initialized.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### satisfied

Satisfaction value used only when known.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### measure_known

True when normalized measure is initialized.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### normalized_measure

Edition-specific bounded normalized measure lexeme.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 24
}
```

### completion_known

Whether edition-supported mapped completion is initialized.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### completed

Completion value used only when known.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### progress_known

Whether edition-supported mapped progress is initialized.

Required. Null is rejected.

```json
{
  "type": "boolean"
}
```

### progress_measure

Known normalized progress in [0,1].

Optional. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^(?:0|[1-9][0-9]{0,11})(?:\\.[0-9]{1,6})?$"
}
```

### raw_score

Known edition-supported objective raw score lexical value.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### minimum_score

Known edition-supported objective minimum lexical value.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
}
```

### maximum_score

Known edition-supported objective maximum lexical value.

Optional. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 32
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

### institution_id

Institution isolation root.

Required. Null is rejected.

References [Institution](Institution.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### learner_person_id

Exact authorized learner whose state may be shared.

Required. Null is rejected.

References [Person](Person.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### organization_id

Manifest organization when sharing is limited to its tree.

Optional. Null is rejected.

References [PackageOrganization](PackageOrganization.md). Reference must resolve in the exact owning Institution.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### persistence_scope

Resolved persistence scope from edition manifest and explicit tenant trust profile.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "attempt",
    "tree_across_attempts",
    "approved_system"
  ]
}
```

### resolved_scope_key

Unambiguous identity for local attempt, tree attempt, tree-across-attempts or approved learner-wide scope.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

## Integrity

- Enforce one scoped objective per registration and objective key with local attempt included where applicable.
- A missing measure is distinct from zero.

## Unique keys

- `id`
- `institution_id, learner_person_id, resolved_scope_key, external_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| registration_id, objective_scope, external_key | Resolve objective map during sequencing. |
| institution_id, learner_person_id, resolved_scope_key | Resolve authorized global mapped objective identity independent of registration. |

## Retention

Retain with sequencing and outcome evidence.
