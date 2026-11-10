# AssessmentDelivery

Offering and curriculum placement binding for an assessment.

Owned by **assessment**.

## Fields

### id

Stable globally unique AssessmentDelivery identifier.

Required. Null is rejected.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### offering_id

Offering authorized to host delivery.

Required. Null is rejected.

References [CourseOffering](CourseOffering.md). Offering authorized to host delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### content_placement_id

Placement in the pinned CourseVersion authorized for this offering.

Required. Null is rejected.

References [ContentPlacement](ContentPlacement.md). Placement in the pinned CourseVersion authorized for this offering.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### assessment_version_id

Current published revision for new starts.

Required. Null is rejected.

References [AssessmentVersion](AssessmentVersion.md). Current published revision for new starts.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### policy_version_id

Current published policy for this delivery.

Optional. Nullable.

References [DeliveryPolicyVersion](DeliveryPolicyVersion.md). Current published policy for this delivery.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### grade_item_id

Optional academic item scoped to this offering and placement.

Optional. Nullable.

References [GradeItem](GradeItem.md). Optional academic item scoped to this offering and placement.

```json
{
  "type": "string",
  "format": "uuid"
}
```

### state

Offering delivery lifecycle. Archived is a restricted retention disposition after closure.

Required. Null is rejected.

```json
{
  "type": "string",
  "enum": [
    "draft",
    "published",
    "suspended",
    "closed",
    "archived"
  ]
}
```

### write_version

Concurrent publisher guard.

Required. Null is rejected.

```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 2147483647
}
```

### audience_digest

Approved offering eligibility and audience definition snapshot digest.

Required. Null is rejected.

```json
{
  "type": "string",
  "pattern": "^[a-f0-9]{64}$"
}
```

## Integrity

- An in-progress attempt keeps captured version after change.
- Grade item must be authorized by academic records.

## Unique keys

- `id`
- `offering_id, content_placement_id`

## Query indexes

| Fields | Query purpose |
| --- | --- |
| offering_id, state | Staff and candidate delivery discovery. |

## Retention

Retain through the latest dependent active assessment, historical academic evidence or applied hold.

## Transitions

| From | To | Command | Guard and effects |
| --- | --- | --- | --- |
| draft | published | PublishAssessmentDelivery | All dependencies and policy gates valid. Publish exact version and policy. |
| published | suspended | SuspendAssessmentDelivery | Authorized staff records suspension reason. Block new starts and preserve open sessions by default. |
| suspended | published | ResumeAssessmentDelivery | Blocking incident resolved and dependencies valid. Allow new starts under approved policy. |
| published | closed | CloseAssessmentDelivery | Delivery owner approves closure. Block new starts and preserve existing evidence. |
| suspended | closed | CloseAssessmentDelivery | Authorized owner closes the suspended delivery. Preserve historical attempts and existing permitted review. |
