# PackageRegistration

One learner package attempt pinned to a course release and package version.

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

### enrollment_id

Enrollment whose effective release authorizes this registration.

Required. Null is rejected.

References [Enrollment](Enrollment.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### enrollment_release_id

Exact release at assignment and launch.

Required. Null is rejected.

References [EnrollmentRelease](EnrollmentRelease.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### activity_version_id

Native assigned packaged activity version.

Required. Null is rejected.

References [ActivityVersion](ActivityVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### package_version_id

Immutable package selected at registration.

Required. Null is rejected.

References [PackageVersion](PackageVersion.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### placement_id

Course occurrence scoped to effective release.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### organization_id

Selected organization inside package version.

Required. Null is rejected.

References [PackageOrganization](PackageOrganization.md). Reference must resolve inside the owning Institution or the directly owned aggregate.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### attempt_number

Ordinal among learner registrations for this placement and assigned version.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000
}
```

### epoch

Single-writer grant generation.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### runtime_policy_revision

Immutable mapping from package state to native evidence.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 9007199254740991
}
```

### total_time_ms

Exact fixed-unit millisecond projection only when duration has no unresolved calendar components.

Optional. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 0,
  "maximum": 9007199254740991
}
```

### active_launch_session_id

Current authoritative launch session if any.

Optional. Null is rejected.

References [PackageLaunchSession](PackageLaunchSession.md). Session belongs to this exact registration and epoch.

```json
{
  "type": "string",
  "format": "uuid"
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

### state

Authoritative lifecycle state advanced only through owner commands.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "completed",
    "withdrawn"
  ]
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

### duration_total

Lossless duration sum. Preserve calendar components separately from fixed elapsed units.

Required. Null is rejected.

```json
{
  "type": "object",
  "properties": {
    "years": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "months": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    },
    "fixed_milliseconds": {
      "type": "integer",
      "minimum": 0,
      "maximum": 9007199254740991
    }
  },
  "required": [
    "years",
    "months",
    "fixed_milliseconds"
  ],
  "additionalProperties": false
}
```

## Integrity

- Single writer epoch. No evidence accepts a stale grant.
- Package, organization and source placement remain pinned.
- Runtime state and learner grade evidence remain separate.

## Unique keys

- `id`
- `enrollment_id, placement_id, activity_version_id, attempt_number`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| institution_id, enrollment_id, state | List a learner's authorized package registrations. |
| package_version_id, state | Find retention and withdrawal impact. |

## Retention

Follow owning learner record retention, with a seven-year default for graded evidence when institutional rules allow. Apply approved holds.
