# PackageSharedDataStore

Edition-scoped shared runtime data declaration and current learner value.

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

### store_key

Verified manifest bucket identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 4000
}
```

### sharing_scope_key

Explicit learner and package scope chosen by approved policy.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 512
}
```

### store_value

Confidential shared text under edition value limits.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 0,
  "maxLength": 65536
}
```

### read_occurrence_ids

Manifest occurrences allowed to read this store.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Only activities in the approved sharing context.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 10000,
  "minItems": 0,
  "uniqueItems": true
}
```

### write_occurrence_ids

Manifest occurrences allowed to write this store.

Required. Null is rejected.

References [PackageActivity](PackageActivity.md). Only activities in the approved sharing context.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "format": "uuid"
  },
  "maxItems": 10000,
  "minItems": 0,
  "uniqueItems": true
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

Last durable change.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "date-time"
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

## Integrity

- Enable only when the edition declares this extension.
- Store grants are declared and separately checked on every read or write.
- The scope key includes the registration for attempt lifetime and excludes it for retained tree or approved system lifetime. Shared writes compare the store revision under lock, including concurrent distinct registrations.

## Unique keys

- `id`
- `institution_id, learner_person_id, sharing_scope_key, store_key`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, learner_person_id, sharing_scope_key | Find a learner store without treating the latest registration as its identity. |

## Retention

Same as protected runtime data for the owning learner registration.
