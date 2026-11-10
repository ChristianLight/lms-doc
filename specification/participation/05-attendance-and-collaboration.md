# 05. Live learning, attendance and collaboration

## Live delivery records

| Record | Ownership and fields | Key and lifecycle |
| --- | --- | --- |
| MeetingSeries | Offering, optional Section or LearningGroup audience, organizer, title, zone, initial wall time, recurrence, duration, location kind, accessible participation reference and calendar revision | One stable ID. Draft, active, ended or cancelled. Index offering and audience |
| MeetingOccurrence | Series, recurrence ID, canonical start/end, venue or provider reference, current revision, check-in windows and roster freeze time | Unique series plus recurrence ID. Scheduled, open, closed or cancelled. Index start by offering |
| AttendanceEntry | Occurrence and Enrollment, active AttendanceRevision pointer, initial roster snapshot and current revision | Unique occurrence plus enrollment. Attended learner must match occurrence audience at capture time or have an explicit exception |
| AttendanceRevision | Entry, attendance decision, evidence type and reference, actor, recorded instant, rationale, prior revision and publication state | Immutable. At most one effective published decision. Retain prior corrections and scope |
| CollaborationSpaceLink | Offering, audience scope, purpose, IntegrationConnection ID, optional pending ExternalResourceMap ID, desired and observed revisions, sync state and next retry | Unique connection plus local scope and purpose. The platform owns provider object identifiers and mapping uniqueness. Remote identifier and launch URL are private |
| Announcement | Offering, audience scope, typed body, author, publish interval, severity, revision and delivery policy | Draft, scheduled, published, withdrawn. One delivery attempt per recipient/channel/revision idempotency key |

Meeting attendance defaults to instructor confirmation. Optional sources include time-bounded rotating codes or signed provider records. Each attendance source is a proposal unless explicitly approved as sufficient for the course and activity. Default check-in opens ten minutes before start and ends ten minutes after start. A learner gets an immediate receipt for a check-in request. A rejected or delayed provider callback leaves the learner able to request a correction. The default audience snapshot is captured at the meeting start. Absence is recorded only after close and a reviewed or policy-approved reconciliation of the applicable roster. A learner admitted after that snapshot is unrecorded unless staff make a reasoned addition.

### Attendance status and calculations

Use present, late, absent, excused and unrecorded. A cancelled meeting never contributes. Default treat present and late as one attended occurrence each. Excused is removed from the denominator. Unrecorded means pending and blocks a definitive attendance rate until resolved. Offer a provisional count labelled with coverage. One eligible occurrence contributes at most one attendance decision. Optional sessions are excluded from course thresholds unless explicitly configured. A qualified asynchronous equivalent satisfies the designated requirement through the same placement completion rule.

For 12 required occurrences, one is cancelled, one excused, two absent, one late and seven present. Eligible denominator is 10 and attended count is 8, so attendance is 80 percent. If one of the seven present is still unrecorded, show provisional 7 confirmed of 10 eligible and one pending, with no final percentage. A change from absent to excused yields denominator 9 and 8 attended, displayed as 89 percent rounded half-up. A course threshold compares the exact fraction, so the rounded display never creates a pass.

## Attendance and calendar mutations

1. Instructor schedules a meeting or recurrence under an offering calendar revision. Validate zone, effective period, audience and venue. Preview generated occurrences and DST handling. Create a remote meeting asynchronously if applicable.
2. At open, authorize learner and audience for that occurrence. A rotating code is hashed at rest, scoped to one occurrence and epoch, rate limited and replay-safe per learner. Provider callback verifies signature and maps a stable identity rather than matching names. Clock skew grace for signed requests is at most 2 minutes by default.
3. Instructor opens attendance screen with audience, proposals and unrecorded states. Save per-learner decisions using expected revision or a bulk batch with one result per requested row. Bulk submission displays exactly which records are ready to publish.
4. Publish decisions only after validation. Append immutable revisions and events. Participation consumes relevant decisions as completion evidence and records exact lineage. Academic records may consume a separate policy-governed result where applicable.
5. Learner sees their own published decision, correction route and instructional fallback. Staff can append corrected decision under a correction capability and reason. Earlier revision stays retained. Changes to completed coursework require explicit academic impact review.
6. Cancel or move a future occurrence by expected revision. Preserve historical occurrence ID and immutable attendance. If already started or closed, cancel requires elevated permission and an impact preview. Calendar sequence advances. Calendar and provider updates retry independently.

## Collaboration resources

Native learning and grading remain authoritative when a chat, file or video provider is unavailable. Space purpose values include discussion, video meeting, collaboration folder and staff room. Store desired membership revision, observed reconciliation projection and effect receipts. Provider credentials and exact resource identities resolve through the Platform-owned IntegrationConnection and ExternalResourceMap. Reconcile from that typed map before accepting remote state. A missing map leaves the link pending. A durable operation key combines link, local actor or learner, membership version and action. Reconciliation computes additions and removals from authoritative LMS roles and active enrollment. Withdrawals enqueue removal with priority and block new LMS launches immediately.

Scoped launch performs a fresh membership and space decision. It signs or redirects through an approved provider and returns an opaque reference. Avoid logging invite URLs, room credentials or message contents. Track pending, synced, degraded, retrying and retired. A remote resource can remain in a reconciliation queue after its local link retires. Provider group removal cannot delete the learner's academic history.

File sharing distinguishes immutable course asset, mutable collaboration folder and formal submission artifact. A submitted artifact retains digest, size, type, provider version, authorization and custody. Membership in a collaboration group does not grant staff assessment review, and room visibility does not imply official attendance.

## Announcements and notification policy

Announcements use explicit offering, section, learning group or learner audience. Freeze the audience at dispatch per channel while current permission continues to govern in-app reads. Revoking membership excludes future dispatch and blocks subsequent in-app access. Edit published text as a new revision. Withdrawal suppresses future distribution and exposes a retraction status to previously authorized users when policy requires. Email and external notification payloads carry a short permitted description and sign-in link. Grades, accommodations and sensitive attendance details stay in the authenticated LMS.

## Failure fixtures

| Scenario | Required result |
| --- | --- |
| Room provisioning times out after the remote API may have succeeded | Retry with the same idempotency key or reconcile by registered reference before creating again |
| Roster transfers before a meeting and after another | Each attendance view uses its own effective scope and snapshot |
| Provider sends two identical attendance events and a later incompatible revision | Exact duplicate returns the original receipt. New verified revision becomes a proposal or documented correction |
| Room removal is blocked by provider outage | LMS launch revoked immediately. Removal remains in a monitored retry queue |
| Staff schedules private exam support for a named group | Only permitted learners see the event and invitation. External calendar feed does not leak its title |
