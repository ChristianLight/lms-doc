# Participation acceptance scenarios

## PAR-001 — Last seat admits one learner

Covers `AdmitLearnerDirectly`, `Enrollment`, `SeatReservation`.

### Given

- Capacity 20. 19 seats occupied. No reservations.

### When

- Two different eligible direct admission commands overlap.

### Then

- Exactly one active enrollment and first release added. Losing request reports capacity conflict.

### Fixture values

```json
{
  "capacity": 20,
  "occupied": 19,
  "concurrent_requests": 2
}
```

## PAR-002 — Waitlist reservations hold seat across retries

Covers `OfferWaitlistSeat`, `AcceptSeatReservation`, `SeatReservation`.

### Given

- One eligible waitlisted learner and one unreserved seat.

### When

- Issue 48-hour hold. Retry accept after successful commit.

### Then

- Original enrollment and release IDs returned. Capacity consumed once.

### Fixture values

```json
{
  "offer_hours": 48,
  "retries": 2
}
```

## PAR-003 — Full feed preserves independent grants

Covers `StageRosterFeed`, `ApplyRosterFeed`, `EnrollmentSourceGrant`.

### Given

- Person P has direct and source S grants. Verified complete S feed omits P.

### When

- Apply full feed with explicit revocation.

### Then

- Only S grant ends. Stable enrollment remains active.

### Fixture values

```json
{
  "active_grants_before": [
    "direct",
    "S"
  ],
  "active_grants_after": [
    "direct"
  ]
}
```

## PAR-004 — Missing partial feed cannot revoke

Covers `ApplyRosterFeed`, `RosterSyncRun`.

### Given

- Full feed fails row validation and coverage incomplete.

### When

- Attempt apply with unseen grant revocation.

### Then

- No unseen grant ends. Report actionable diagnostics.

### Fixture values

```json
{
  "mode": "full",
  "complete": false,
  "failed_rows": 1
}
```

## PAR-005 — Transfer preserves historical attempt

Covers `TransferSection`, `SectionMembership`, `EnrollmentRelease`.

### Given

- Learner has an active exam pinned to Section A dates.

### When

- Move learner from A to B and close A-only learning group membership.

### Then

- Same enrollment and release remain. New starts use B. Old attempt policy remains pinned.

### Fixture values

```json
{
  "from": "A",
  "to": "B",
  "existing_attempt": true
}
```

## PAR-006 — Precedence applies fields independently

Covers `SetScheduleOverride`, `ReadPlacementAccess`, `ScheduleOverride`.

### Given

- Default due November 14 at 17:00. Section B sets November 15 at 12:00. Group sets recommended date only.

### When

- Learner override sets due November 15 at 18:00.

### Then

- Effective due 18:00. Group recommendation retained. Hard close unchanged.

### Fixture values

```json
{
  "timezone": "Africa/Windhoek",
  "section_due": "2026-11-15T12:00:00+02:00",
  "learner_due": "2026-11-15T18:00:00+02:00",
  "close": "2026-11-16T18:00:00+02:00"
}
```

## PAR-007 — Same group precedence conflicts fail closed

Covers `SetScheduleOverride`, `ReadPlacementAccess`, `ScheduleOverride`.

### Given

- Two simultaneously applicable groups rank 10 and set unequal due dates.

### When

- Try to add second override.

### Then

- Reject 422 SCHEDULE_WINDOW_CONFLICT. Existing invalid legacy state denies new starts.

### Fixture values

```json
{
  "group_ranks": [
    10,
    10
  ],
  "due_instants": [
    "2026-11-15T12:00:00Z",
    "2026-11-15T18:00:00Z"
  ]
}
```

## PAR-008 — Course release waits for in-progress exam

Covers `PlanReleaseRollout`, `ApproveReleaseRollout`, `ApplyReleaseRollout`, `ReleaseRolloutRow`.

### Given

- 30 learner releases use version 4. One learner has active exam.

### When

- Approve version 5 rollout and apply. Retry deferred learner after submission.

### Then

- 29 change immediately. Last changes once after terminal attempt. Attempt remains on version 4.

### Fixture values

```json
{
  "source": 4,
  "target": 5,
  "audience": 30,
  "deferred": 1
}
```

## PAR-009 — Video coverage merges intervals

Covers `RecordLearningEvidence`, `LearningProgress`.

### Given

- Duration 100000 ms and threshold 90 percent.

### When

- Report [0,40000), [30000,70000), [80000,99000) and duplicate [0,40000).

### Then

- Distinct coverage 89000 ms. Not complete.

### Fixture values

```json
{
  "duration_ms": 100000,
  "intervals": [
    [
      0,
      40000
    ],
    [
      30000,
      70000
    ],
    [
      80000,
      99000
    ],
    [
      0,
      40000
    ]
  ],
  "expected_coverage_ms": 89000
}
```

## PAR-010 — Late package evidence keeps old lineage

Covers `RecordLearningEvidence`, `EnrollmentRelease`, `LearningEvidence`.

### Given

- Package registration started on release R1. R2 is now effective.

### When

- Receive trusted committed package event for R1.

### Then

- Evidence recorded on R1. R2 changes only if approved carry allows it.

### Fixture values

```json
{
  "old_release": "R1",
  "current_release": "R2",
  "carry_allowed": false
}
```

## PAR-011 — Attendance denominator excludes cancelled and excused

Covers `PublishAttendance`, `AttendanceRevision`.

### Given

- 12 required occurrences including one cancelled and one excused.

### When

- Publish two absent, one late and seven present.

### Then

- Eight attended of ten eligible, 80 percent.

### Fixture values

```json
{
  "required": 12,
  "cancelled": 1,
  "excused": 1,
  "absent": 2,
  "late": 1,
  "present": 7,
  "expected_percentage": 80
}
```

## PAR-012 — Provider outage blocks remote launch only

Covers `SetCollaborationSpace`, `LaunchCollaborationSpace`, `CollaborationSpaceLink`.

### Given

- Offering active while provider is unavailable.

### When

- Create group room and request launch.

### Then

- Retryable pending or degraded provider state. Learning and academic records remain accessible.

### Fixture values

```json
{
  "provider": "unavailable",
  "native_delivery": "available"
}
```

## PAR-013 — Stale resume does not overwrite newer session

Covers `SaveResumeCheckpoint`, `ProgressResume`.

### Given

- Browser B accepted server resume revision 12. Offline browser A retains revision 11.

### When

- A reconnects and saves expected revision 11.

### Then

- 409 REVISION_CHANGED. Revision 12 remains. Offer local checkpoint as explicit choice.

### Fixture values

```json
{
  "accepted_revision": 12,
  "stale_revision": 11
}
```

## PAR-014 — Attendance correction appends before reviewing impact

Covers `CorrectAttendance`, `PublishCompletionCorrection`, `AttendanceRevision`, `CompletionRecord`.

### Given

- An attendance decision contributed to awarded completion.

### When

- Publish correction and open academic impact review.

### Then

- Old decision and completion remain auditable. Any completion change creates authorized supersession.

### Fixture values

```json
{
  "old": "present",
  "new": "excused",
  "completion_requires_review": true
}
```

## PAR-015 — Offering setup and safe activation

Covers `CreateOffering`, `PublishOfferingCalendar`, `PublishAdmissionPolicy`, `CreateSection`, `UpdateSection`, `UpdateOffering`, `TransitionOffering`, `CourseOffering`, `OfferingCalendarVersion`.

### Given

- Published Algebra version 4 and academic period 2027-T1 are available.

### When

- Create ALG-2027-T1 with capacity 60. Add Sections A and B with capacity 30 and scoped instructors. Update B to capacity 32 while empty. Set offering capacity 62 and publish validated calendar and manual or self admissions. Schedule and activate.

### Then

- Offering activates under exact version 4 and calendar revision 1. Sections retain independent caps. A second attempt to activate without a teacher returns OFFERING_NOT_READY.

### Fixture values

```json
{
  "course_version": 4,
  "initial_capacity": 60,
  "final_capacity": 62,
  "section_capacities": [
    30,
    32
  ],
  "final_state": "active"
}
```

## PAR-016 — New offering default affects future enrollments

Covers `SetOfferingDefaultPublication`, `AdmitLearnerDirectly`, `EnrollmentRelease`.

### Given

- Learners A and B use version 4. Offering version 5 was independently published.

### When

- Set version 5 as default and admit learner C.

### Then

- C receives version 5. A and B keep their version 4 releases and exact progress.

### Fixture values

```json
{
  "prior_version": 4,
  "new_default": 5,
  "affected_existing": 0,
  "new_learner_version": 5
}
```

## PAR-017 — Institution cohort and section-bound group remain distinct

Covers `CreateLearningGroup`, `CreateCohort`, `SetGroupMembership`, `SetCohortMembership`, `CloseMembershipContainer`, `Cohort`, `LearningGroup`.

### Given

- Student P is in institution I and Section B of offering O.

### When

- Create cohort 2027 and add P. Create Section A group Debate and try adding P. Transfer P into Section A and add P to Debate, then close Debate.

### Then

- Cohort membership gives no offering access. First group add fails scoped section check. Second succeeds. Closure preserves ended interval and the institutional cohort.

### Fixture values

```json
{
  "cohort_code": "2027",
  "group_code": "Debate",
  "initial_section": "B",
  "required_section": "A"
}
```

## PAR-018 — Application denial and waitlist cancellation remain distinct

Covers `ApplyForEnrollment`, `DecideEnrollmentApplication`, `CancelEnrollmentApplication`, `EnrollmentApplication`.

### Given

- Offering requires approval and currently has no unreserved seat.

### When

- Learner P applies with verified prerequisites. Registrar waitlists P. P cancels. Learner Q applies and authorized registrar declines with a safe reason.

### Then

- P ends cancelled and Q declined. Neither creates enrollment. Applicant projections expose only own decision and next action.

### Fixture values

```json
{
  "capacity_available": 0,
  "states": [
    "cancelled",
    "declined"
  ],
  "new_enrollments": 0
}
```

## PAR-019 — Suspension and reactivation preserve work

Covers `TransitionEnrollment`, `Enrollment`.

### Given

- Enrollment has release R4, two submissions and active collaboration.

### When

- Suspend for approved reason. Request new start. Reactivate with keep release option.

### Then

- Ordinary start denied during suspension. Resume restores same Enrollment and R4. Work retained and provider removal or addition tracked separately.

### Fixture values

```json
{
  "release_before": "R4",
  "release_after": "R4",
  "prior_submissions": 2,
  "state_sequence": [
    "active",
    "suspended",
    "active"
  ]
}
```

## PAR-020 — Acknowledgment, bookmarks and dashboard are separate

Covers `AcknowledgeLearningPlacement`, `SaveLearnerBookmark`, `RemoveLearnerBookmark`, `ReadLearnerDashboard`, `LearningEvidence`, `LearnerBookmark`.

### Given

- Learner P sees required reading R and optional practice B.

### When

- Bookmark R with label Review before exam, acknowledge R twice with the same intent, read dashboard and remove bookmark.

### Then

- One accepted evidence. Dashboard advances to next actionable required item. Bookmark removal changes no progress. Staff do not see the label.

### Fixture values

```json
{
  "acknowledgment_retries": 2,
  "expected_evidence": 1,
  "private_label": "Review before exam"
}
```

## PAR-021 — Meeting reschedule and check-in retain stable occurrence

Covers `ScheduleMeetingSeries`, `ChangeMeetingOccurrence`, `OpenMeetingCheckIn`, `CheckInToMeeting`, `MeetingOccurrence`.

### Given

- Teacher owns Section B and a weekly online tutorial at Tuesday 10:00.

### When

- Schedule series with first recurrence, move that occurrence to 11:00, open window 10:50–11:10, then check in at 10:55 twice with the same intent.

### Then

- Same occurrence UID and higher sequence. One proposed attendance revision, no published decision.

### Fixture values

```json
{
  "initial_hour": 10,
  "changed_hour": 11,
  "check_in": "10:55",
  "expected_proposals": 1
}
```

## PAR-022 — Scoped announcement edit and withdrawal

Covers `SaveAnnouncement`, `WithdrawAnnouncement`, `Announcement`.

### Given

- Teacher assigned Section B only. B contains learners P and Q.

### When

- Publish Section B announcement Quiz review moved to Friday. Transfer Q out of B. Attempt to publish another revision and withdraw it.

### Then

- Dispatch snapshots exact authorized audience each time. Q receives no future dispatch and has no subsequent in-app B content access. Withdrawal suppresses queued attempts.

### Fixture values

```json
{
  "audience": "section-B",
  "original_recipients": 2,
  "revised_recipients": 1
}
```

## PAR-023 — Teacher workspace and roster export respect effective scope

Covers `ReadTeacherWorkspace`, `ExportScopedRoster`, `Section`.

### Given

- Section A has 30 learners and Section B has 24. Teacher owns B with a separate export grant.

### When

- Read workspace and request B CSV. Try to export A.

### Then

- Projection count 24 before later roster changes. A export is inaccessible. B artifact contains only allowed fields and default expiry 24 hours.

### Fixture values

```json
{
  "section_a": 30,
  "section_b": 24,
  "visible_count": 24,
  "export_expiry_hours": 24
}
```

## PAR-024 — Stale provider reconciliation cannot restore old access

Covers `SetCollaborationSpace`, `ReconcileCollaborationSpace`, `LaunchCollaborationSpace`, `CollaborationSpaceLink`.

### Given

- Link desired revision 4 included learner P. Withdrawal generated revision 5 excluding P.

### When

- Receive delayed revision 4 provider success then verified revision 5 removal.

### Then

- Old receipt cannot advance current state or authorize launch. Current removal receipt settles the new revision.

### Fixture values

```json
{
  "old_revision": 4,
  "withdrawal_revision": 5,
  "launch_allowed": false
}
```

## PAR-025 — Invitation token belongs to one verified learner

Covers `IssueEnrollmentInvitation`, `RevokeEnrollmentInvitation`, `ApplyForEnrollment`, `EnrollmentInvitation`.

### Given

- Registrar invites learner P for Section B. No capacity is reserved.

### When

- Learner Q attempts use. Registrar revokes unused invitation. P follows expired link.

### Then

- Q receives generic unavailable response. Revocation leaves no application or seat consumed. P sees authorized unavailable status.

### Fixture values

```json
{
  "issued_to": "P",
  "wrong_person": "Q",
  "seat_reservations": 0,
  "terminal_state": "revoked"
}
```

## PAR-026 — Follow and application hold preserve separate scopes

Covers `SetCourseFollow`, `SetAdmissionHold`, `ApplyForEnrollment`, `CourseFollow`, `AdmissionHold`.

### Given

- Catalog visible to P. Registrar opens an offering-specific hold with safe next action.

### When

- P follows course and then applies. Registrar ends hold and P retries under current policy.

### Then

- Follow succeeds without admission. First application cannot admit. Later eligibility re-evaluates without reassigning identity.

### Fixture values

```json
{
  "initial_hold": "active",
  "follow_grants_enrollment": false,
  "after_hold": "recheck"
}
```

## PAR-027 — Sticky unlock cannot override current safety blocks

Covers `SetGateOverride`, `OpenNativeLearningActivity`, `ReadPlacementAccess`, `GateOverrideDecision`, `StickyGateDecision`.

### Given

- Learner has reviewed prior-learning approval and activity explicitly has sticky continuity.

### When

- Authorized teacher grants clause approval. Learner opens activity, approval later ends, then institution withdraws unsafe asset.

### Then

- First start pins eligible sticky decision. Routine gate end follows sticky policy. Safety block prevents new delivery, with original decision retained.

### Fixture values

```json
{
  "continuity": "sticky_after_start",
  "initial_gate": "approved",
  "safety_withdrawal_blocks": true
}
```

## PAR-028 — Intervention remains separate from outcome change

Covers `RecordParticipationIntervention`, `ParticipationIntervention`, `CompletionRecord`.

### Given

- Teacher owns learner P and a required task is overdue.

### When

- Record support reminder with approved purpose and mark completed when learner responds.

### Then

- Support log advances. Required deadline and academic completion remain unchanged absent explicit separate authoritative mutations.

### Fixture values

```json
{
  "basis": "required-work-overdue",
  "states": [
    "open",
    "completed"
  ],
  "grade_changes": 0
}
```
