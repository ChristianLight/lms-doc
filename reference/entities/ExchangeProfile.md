# ExchangeProfile

Institution-authorized interoperable exchange direction and capability snapshot.

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

### standard

Format or protocol family.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "native",
    "scorm",
    "qti",
    "common_cartridge",
    "lti",
    "oneroster",
    "xapi",
    "cmi5",
    "historical"
  ]
}
```

### edition

Exact version or package edition.

Required. Null is rejected.

```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 80
}
```

### direction

Approved direction.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "ingress",
    "egress",
    "bidirectional"
  ]
}
```

### capabilities

Precisely declared supported features.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 128
  },
  "maxItems": 128,
  "minItems": 1,
  "uniqueItems": true
}
```

### limitations

Compatibility limits visible to operators.

Required. Null is rejected.

```json
{
  "type": "array",
  "items": {
    "type": "string",
    "minLength": 1,
    "maxLength": 256
  },
  "maxItems": 128,
  "minItems": 0,
  "uniqueItems": false
}
```

### endpoint_origin

Approved exchange destination origin for service profiles.

Optional. Null is rejected.

```json
{
  "type": "string",
  "format": "uri",
  "maxLength": 2048
}
```

### privacy_class

Maximum permitted data class.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "public_curriculum",
    "restricted_curriculum",
    "student_records"
  ]
}
```

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "active",
    "suspended",
    "retired"
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

- One active profile per installed capability and institution direction unless scopes are explicitly disjoint.
- Unknown required capabilities block exchange.

## Unique keys

- `id`
- `institution_id, standard, edition, direction, revision`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, standard, state | Find supported and active exchange profiles. |

## Retention

Retain active versions and configuration history as long as exchange receipts refer to them.
