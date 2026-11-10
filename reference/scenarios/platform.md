# Platform acceptance scenarios

## PLAT-001 — Institution isolation holds with a valid known resource ID

Covers `Person`, `ListPeople`, `AuditEvent`.

### Given

- Principal P has directory capability in institution A
- Known learner B1 belongs to institution B

### When

- P searches B's directory and then directly requests a scoped audit view about B1

### Then

- Both deny or return authorized non-disclosing absence. No B1 name, count or existence leaks.

### Fixture values

```json
{
  "institution_a": "north-school",
  "institution_b": "south-school",
  "known_learner": "B1",
  "expected_http_status": 404
}
```

## PLAT-002 — Two related children share a verified family inbox

Covers `Person`, `PersonContact`, `VerifyPersonContact`.

### Given

- Two siblings have separate educational identities and use one family email

### When

- Both contacts are verified under independently authorized sessions

### Then

- Contacts remain separate. No account linking, role transfer or educational merge occurs.

### Fixture values

```json
{
  "learner_numbers": [
    "P-880",
    "P-881"
  ],
  "shared_email": "household@example.test",
  "distinct_person_count": 2
}
```

## PLAT-003 — Provider subject collision does not merge accounts

Covers `ExternalIdentity`, `LinkExternalIdentity`.

### Given

- Two active Principals claim the same verified provider issuer and subject for one connection

### When

- A and B concurrently consume valid link proofs

### Then

- At most one binding commits. The loser receives SUBJECT_ALREADY_BOUND and no session for the winning Principal.

### Fixture values

```json
{
  "issuer": "https://id.example.test",
  "subject": "provider-42",
  "existing_principal_count": 2,
  "result_bound_count": 1
}
```

## PLAT-004 — Role scope is recomputed after a hierarchy move

Covers `OrganizationUnit`, `MoveOrganizationUnit`, `RoleAssignment`.

### Given

- Manager M holds a descendants grant in unit West. Course X belongs to unit P, a child of West.

### When

- Registrar moves P under East with approved current impact preview while M holds an active session

### Then

- Authorization epoch increments. M cannot access X on the next request. Old audit evidence still references West.

### Fixture values

```json
{
  "prior_epoch": 7,
  "expected_epoch": 8,
  "prior_path": [
    "West",
    "P"
  ],
  "current_path": [
    "East",
    "P"
  ]
}
```

## PLAT-005 — Non-overlapping grants are accepted at the exact boundary

Covers `RoleAssignment`, `ApproveRoleAssignment`.

### Given

- Assistant A has an approved scoped grant ending 2027-06-01T12:00:00Z

### When

- Approve a new matching role grant starting at the same instant

### Then

- There is no overlap under half-open semantics. A request at that instant selects only the new grant.

### Fixture values

```json
{
  "old_valid_until": "2027-06-01T12:00:00Z",
  "new_valid_from": "2027-06-01T12:00:00Z",
  "active_grants": 1
}
```

## PLAT-006 — Restriction overrides institutional authority

Covers `AccessRestriction`, `ApplyAccessRestriction`, `EmergencyAccessGrant`.

### Given

- Admin A has explicit institution view and a temporary incident grant. An active restriction covers one sensitive learner.

### When

- A uses the emergency grant to request that learner's protected attachment

### Then

- Deny wins. Audit records a restricted decision and no storage ticket is issued.

### Fixture values

```json
{
  "restriction_scope": "Person",
  "permission": "platform.storage.read",
  "expected_tickets": 0
}
```

## PLAT-007 — Guardian right ends while a notice is queued

Covers `GuardianRelationship`, `RevokeGuardianRelationship`, `NotificationDelivery`.

### Given

- Verified guardian G may view released reports for learner L and an optional report notice is queued

### When

- Revoke relationship before dispatch, then process the notification job

### Then

- Send is suppressed and a former guardian session cannot fetch the report. Existing audit survives.

### Fixture values

```json
{
  "category": "released_report",
  "provider_send_count": 0,
  "delivery_outcome": "suppressed"
}
```

## PLAT-008 — Closing a term preserves existing report snapshots

Covers `AcademicPeriod`, `SetAcademicPeriodState`.

### Given

- An open term has issued reports pinned to period version 2

### When

- Registrar closes the term and subsequently reopens with independent approval

### Then

- New association follows state. Old reports retain their original schedule and context.

### Fixture values

```json
{
  "initial_version": 2,
  "closed_version": 3,
  "reopened_version": 4,
  "historical_report_period_version": 2
}
```

## PLAT-009 — Concurrent hold prevents destruction

Covers `LegalHold`, `PlaceLegalHold`, `StartDispositionTask`, `DispositionTask`.

### Given

- Submission S is past retention and a disposal job is queued

### When

- A valid hold commits before the worker obtains the target lock

### Then

- Worker reports LEGAL_HOLD_ACTIVE or blocked. Binary and authoritative record remain.

### Fixture values

```json
{
  "retain_days": 365,
  "age_days": 400,
  "target": "submission-S",
  "expected_deletes": 0
}
```

## PLAT-010 — Processor timeout leaves privacy request incomplete

Covers `PrivacyRequest`, `RecordDispositionOutcome`, `CompletePrivacyRequest`.

### Given

- Local data is deleted and protected external file outcome is uncertain

### When

- Worker records blocked outcome and reviewer attempts to complete the case

### Then

- Completion denied. No repeat destructive call without evidence. Local completed action key is preserved.

### Fixture values

```json
{
  "local_steps_applied": 1,
  "external_steps_blocked": 1,
  "case_state": "blocked"
}
```

## PLAT-011 — Rejected binary never becomes readable

Covers `ReserveStorageUpload`, `FinalizeStorageUpload`, `RecordStorageScan`, `IssueAccessTicket`.

### Given

- Author uploads a file claimed as a PDF to a known allowed resource

### When

- Backend digest verifies but content inspection finds active unsafe executable content

### Then

- Record unsafe verdict, quarantine and deny all delivery tickets, including for the uploader.

### Fixture values

```json
{
  "claimed_media_type": "application/pdf",
  "scanner_verdict": "unsafe",
  "object_state": "rejected",
  "ticket_count": 0
}
```

## PLAT-012 — Ticket cannot be redeemed after access revocation

Covers `IssueAccessTicket`, `RedeemAccessTicket`, `RevokeRoleAssignment`.

### Given

- Teacher holds valid five-minute download ticket for assessment attachment

### When

- Teaching grant is revoked one minute after issuance. Teacher retries after two minutes.

### Then

- Gateway checks current epoch and owner permission. No response bytes are released.

### Fixture values

```json
{
  "ticket_ttl_seconds": 300,
  "revocation_after_seconds": 60,
  "redeem_after_seconds": 120,
  "delivered_bytes": 0
}
```

## PLAT-013 — Incomplete roster response never withdraws absent learners

Covers `SyncRun`, `ApplySyncPage`, `FinishSyncRun`, `Enrollment`.

### Given

- Two learners exist in the current class and an inbound full snapshot times out after page one

### When

- Finalize with failure and no provider completion marker

### Then

- Keep both enrollments and record the last safe checkpoint. No absence removal appears.

### Fixture values

```json
{
  "existing_enrollments": 2,
  "records_seen": 1,
  "complete_marker_present": false,
  "withdrawals": 0
}
```

## PLAT-014 — Explicit null does not clear a forbidden profile field

Covers `IntegrationAuthorityRule`, `ApplySyncPage`.

### Given

- Profile email rule denies clearing and synchronization adapter receives authenticated explicit null

### When

- Apply a page with the null field and a second row where the key is absent

### Then

- Explicit null produces a rejected field issue. Absence is no-op. No silent email change.

### Fixture values

```json
{
  "clear_allowed": false,
  "input_null": {
    "email": null
  },
  "input_absent": {},
  "cleared_fields": 0
}
```

## PLAT-015 — Callback duplicates are distinguished from payload substitution

Covers `AcceptInboundMessage`, `InboxReceipt`.

### Given

- Connector sends a verified message ID and digest A

### When

- Repeat message with identical bytes, then send same ID with a different validly signed digest B

### Then

- Identical replay returns first receipt. Digest B is rejected and investigated. Apply at most once.

### Fixture values

```json
{
  "message_id": "provider-event-42",
  "identical_repeats": 1,
  "substitution_attempts": 1,
  "authoritative_effect_count": 1
}
```

## PLAT-016 — Expired worker fence cannot commit

Covers `ClaimPlatformJob`, `ReapExpiredJobLease`, `CompletePlatformJob`.

### Given

- Worker A claims a job under fence 17, then stalls past 120 seconds

### When

- Reaper expires fence 17. B claims the job under fence 18 and commits. A wakes and submits completion.

### Then

- B's effect persists once. A receives LEASE_FENCED and cannot close B's claim.

### Fixture values

```json
{
  "expired_fence": 17,
  "active_fence": 18,
  "lease_seconds": 120,
  "effects": 1
}
```

## PLAT-017 — Provider acknowledgement loss does not duplicate email

Covers `NotificationDelivery`, `RecordNotificationOutcome`, `RetryPlatformJob`.

### Given

- Mail provider may have accepted a notice before timeout and offers no idempotent resend

### When

- Record uncertain and attempt automatic repair without a provider lookup

### Then

- Job blocks. No second send occurs until absence is verified or service configuration supports stable keys.

### Fixture values

```json
{
  "send_requests": 1,
  "provider_deduplication": false,
  "delivery_state": "uncertain"
}
```

## PLAT-018 — Restore reapplies withdrawal, erasure and queued effects before reopening

Covers `RecoveryExercise`, `RecordRecoveryMilestone`, `DispositionTask`, `CommandReceipt`.

### Given

- Backup is from 10:00 and later records include a role revocation, protected deletion and accepted provider notice

### When

- Restore to 10:00, replay durable journals in isolation, verify references and compare service objectives

### Then

- Withdrawn access remains denied, deleted bytes are not served, and provider notice is not repeated.

### Fixture values

```json
{
  "backup_time": "2027-02-02T10:00:00Z",
  "post_backup_events": [
    "role_revoked",
    "disposition_applied",
    "notification_accepted"
  ],
  "unintended_deliveries": 0
}
```

## PLAT-019 — Locale preference does not reinterpret exam deadline

Covers `UpdatePersonPreferences`, `AcademicPeriod`, `Attempt`.

### Given

- Student's exam deadline is already resolved to a server instant and preferred timezone is UTC

### When

- Student changes presentation timezone and browser locale while exam is in progress

### Then

- Shown local time changes. The server acceptance instant and due-at snapshot are identical.

### Fixture values

```json
{
  "deadline_utc": "2027-08-20T08:00:00Z",
  "new_timezone": "Africa/Windhoek",
  "expected_local_time": "2027-08-20T10:00:00+02:00"
}
```

## PLAT-020 — Same idempotency key with different intent returns a conflict

Covers `CommandReceipt`, `RequestRoleAssignment`.

### Given

- A valid role assignment command with key k1 commits for learner class C1

### When

- Repeat exact body and key, then use k1 with a different bounded interval

### Then

- Identical replay returns original receipt. Changed normalized body receives IDEMPOTENCY_CONFLICT.

### Fixture values

```json
{
  "idempotency_key": "fixture-c1-grant",
  "body_variants": 2,
  "committed_assignments": 1
}
```

## PLAT-021 — Credential rotation prevents stale connector writes

Covers `UpdateIntegrationConnection`, `SyncRun`, `SetIntegrationConnectionState`.

### Given

- Old run was pinned to enabled connector version 4 and is about to mutate provider membership

### When

- Suspend connector and rotate credential reference under reviewed version 6 before old dispatch

### Then

- Old run fails configuration check. Reconciliation begins only with newly enabled version.

### Fixture values

```json
{
  "old_version": 4,
  "suspended_version": 5,
  "rotated_version": 6,
  "old_remote_mutations": 0
}
```

## PLAT-022 — Expired proof cannot become valid after relinking another account

Covers `VerificationChallenge`, `BeginExternalIdentityLink`, `LinkExternalIdentity`.

### Given

- Human Principal requests account link with nonce N and configured browser session A

### When

- Attempt completion with browser session B and then with session A after 15 minutes

### Then

- Both fail without binding the subject. A fresh recent-authentication flow is required.

### Fixture values

```json
{
  "ttl_seconds": 900,
  "wrong_session": "B",
  "expired_seconds": 901,
  "new_bindings": 0
}
```

## PLAT-023 — Service mandate cannot claim a job outside its approved queue

Covers `ServicePrincipalProfileVersion`, `PublishServicePrincipalProfile`, `ClaimPlatformJob`.

### Given

- A scan worker is scoped to institution I and asset_scan

### When

- The worker requests exam_marking and separately attempts a claim in institution J

### Then

- Both denied without changing any job fence. Its valid scan claim remains possible.

### Fixture values

```json
{
  "worker_profile": "asset-scan",
  "approved_job_kinds": [
    "asset_scan"
  ],
  "forbidden_job_kinds": [
    "exam_marking"
  ],
  "forbidden_claims": 0
}
```

## PLAT-024 — A dispatched effect with no acknowledgement remains uncertain

Covers `OutboundEffect`, `AuthorizeOutboundDispatch`, `RecordOutboundOutcome`.

### Given

- A connector commits dispatch intent and sends an authorized room membership removal

### When

- Worker dies after provider applies removal and before receiving acknowledgement

### Then

- Reconciliation detects provider membership already absent and confirms same stable effect. A second provider mutation is unnecessary.

### Fixture values

```json
{
  "remote_requests": 1,
  "verified_absence": true,
  "final_state": "confirmed"
}
```

## PLAT-025 — Backup base cannot be retired while a verified descendant depends on it

Covers `BackupSet`, `VerifyBackupSet`, `RetireBackupSet`.

### Given

- Base backup S is past rotation threshold and dependent set D is newest verified restore path

### When

- Operator requests retirement of S

### Then

- Retirement denied under coverage lock. D remains eligible. Record the dependency without leaking backup credentials.

### Fixture values

```json
{
  "sets": [
    "S",
    "D"
  ],
  "dependent_sets": 1,
  "retired_sets": 0
}
```

## PLAT-026 — Failed pages cannot advance the committed cursor

Covers `SyncPageReceipt`, `ApplySyncPage`.

### Given

- A provider page at cursor c17 contains 12 valid rows and a last row that violates authority

### When

- The adapter cannot durably stage the invalid row due to transaction failure

### Then

- No receipt commits and cursor remains c17. Retrying the same bytes applies at most one effect per row.

### Fixture values

```json
{
  "initial_cursor": "c17",
  "next_cursor": "c18",
  "input_count": 13,
  "checkpoint_after_failed_attempt": "c17"
}
```

## PLAT-027 — Provisioned school closure preserves controlled academic custody

Covers `CreateInstitution`, `PublishInstitutionPolicy`, `SetInstitutionState`.

### Given

- An independently approved deployment adds school WEST and fixes the default locale and zone. Registrar has custody approval.

### When

- Provision WEST, publish a reviewed 15-minute idle timeout policy, suspend WEST, deny normal sign-in, then request closure with registrar approval.

### Then

- Exactly one institution root and independent policy chain exist. Closure leaves 3 issued records available only through the retained records workflow. A second institution stays active.

### Fixture values

```json
{
  "institution_code": "WEST",
  "idle_session_minutes": 15,
  "prior_records": 3,
  "normal_interactive_access": false,
  "closed_state": "closed"
}
```

## PLAT-028 — Unit archival and term creation honor distinct structures

Covers `CreateOrganizationUnit`, `ArchiveOrganizationUnit`, `CreateAcademicPeriod`, `OrganizationUnit`, `AcademicPeriod`.

### Given

- School S is active. Department Maths is an active child with two active offerings. Calendar year 2027 exists.

### When

- Attempt to archive S, archive Maths before transfer, create an overflowing child term, then create the in-range term and archive Maths after its two responsibilities transfer.

### Then

- First two archives fail due to dependencies. The overflowing period is rejected. The contained period exists as draft. Final archive retains Maths history and both transferred offerings.

### Fixture values

```json
{
  "parent_starts_on": "2027-01-01",
  "parent_ends_before": "2028-01-01",
  "bad_child_ends_before": "2028-01-02",
  "good_child_ends_before": "2027-12-01",
  "transferred_offerings": 2
}
```

## PLAT-029 — Person onboarding and compromise follow separate lifecycles

Covers `CreatePerson`, `RegisterPrincipal`, `SetPrincipalState`, `SetPersonState`, `UnlinkExternalIdentity`.

### Given

- A registrar receives verified learner number NEW-710. No account or grade history exists yet.

### When

- Create Person and two authorized human Principals, link permitted independent providers, and record an enrollment. Suspend Principal A for compromise, unlink its provider binding, and later mark Person inactive.

### Then

- A cannot sign in after suspension, B retains eligible access until Person becomes inactive, and both subsequently lose protected access. Enrollment is still attributable to the original Person.

### Fixture values

```json
{
  "learner_number": "NEW-710",
  "principals": [
    "A",
    "B"
  ],
  "historical_enrollments": 1,
  "eligible_after_principal_a_suspension": [
    "B"
  ],
  "eligible_after_inactivity": []
}
```

## PLAT-030 — Replacing a shared household email requires new proof

Covers `BeginPersonContact`, `VerifyPersonContact`, `RevokePersonContact`, `CreateNotificationPreference`, `SetNotificationPreference`.

### Given

- Learner L has verified email contact A and receives opted-in learning reminders at A. One reminder is queued.

### When

- Begin verification for replacement B, try to use A's old proof, verify B with its new proof, revoke A, then disable optional email before the queued reminder sends.

### Then

- Old proof cannot verify B. B is independently verified, A is revoked, and no reminder is sent because current preference is disabled. Required in-app exam receipts remain available.

### Fixture values

```json
{
  "old_proof_accepted": false,
  "new_contact_state": "verified",
  "old_contact_state": "revoked",
  "external_reminders_sent": 0,
  "in_app_receipts_available": true
}
```

## PLAT-031 — Role definition review never widens existing scoped assignments

Covers `PublishRoleDefinition`, `RequestRoleAssignment`, `RejectRoleAssignment`, `RoleDefinitionVersion`, `RoleAssignment`.

### Given

- Existing assistant assignments use assistant-custom revision 1 with two capabilities. Security reviewer approves revision 2 with a third capability.

### When

- Publish revision 2, request revision 2 in sibling section beyond delegated scope, then request it within scope and have reviewer reject based on missing training evidence.

### Then

- Existing assignments retain exactly two capabilities. Out-of-scope proposal creates no grant. In-scope proposal is denied by reviewer without activating the third capability.

### Fixture values

```json
{
  "old_revision": 1,
  "new_revision": 2,
  "existing_capability_count": 2,
  "proposals_activated": 0,
  "review_outcome": "denied"
}
```

## PLAT-032 — Guardian disclosure is granted only for approved release categories

Covers `RequestGuardianRelationship`, `DecideGuardianRelationship`, `ReadGuardianSummary`, `RevokeGuardianRelationship`.

### Given

- Learner L has one released report and one unreleased assessment. Verified guardian evidence is submitted.

### When

- Request relationship, try to read while requested, independently approve progress_summary only, read progress and request released_report, then revoke the relationship.

### Then

- No pending disclosure occurs. Exactly the approved progress view is available until revocation. Report and unreleased work are never exposed.

### Fixture values

```json
{
  "approved_categories": [
    "progress_summary"
  ],
  "available_released_reports": 1,
  "unreleased_assessments": 1,
  "allowed_reads_before_revocation": 1,
  "allowed_reads_after_revocation": 0
}
```

## PLAT-033 — Emergency approval and restriction lifting follow independent decisions

Covers `RequestEmergencyAccess`, `DecideEmergencyAccess`, `RevokeEmergencyAccess`, `RevokeAccessRestriction`, `AccessRestriction`.

### Given

- Incident IR-401 affects provider installation C. Worker operator O requests read-only connector diagnostics. A separate active containment restriction covers outbound writes.

### When

- O requests emergency access, attempts to approve own request, reviewer R approves diagnostics for 30 minutes, O reads, reviewer revokes grant, and a second reviewer approves lifting containment.

### Then

- Self-approval denied. Exactly one diagnostic read succeeds and is audited. No outbound write is granted by the emergency grant or restriction lift.

### Fixture values

```json
{
  "incident_ref": "IR-401",
  "grant_minutes": 30,
  "diagnostic_reads": 1,
  "outbound_writes": 0,
  "self_approval_allowed": false
}
```

## PLAT-034 — A held privacy case resumes only its pending approved step

Covers `PublishRetentionPolicy`, `SubmitPrivacyRequest`, `VerifyPrivacyRequest`, `DecidePrivacyRequest`, `ReleaseLegalHold`, `ResumePrivacyRequest`, `ListAuditEvents`, `CompletePrivacyRequest`.

### Given

- Learner L requests approved scope for two old drafts. Existing 90-day rules protect the drafts. One draft remains held.

### When

- Publish a new 60-day rule, submit and verify request at age 95 days, independently approve two tasks, complete one, encounter hold on the other, release hold, and resume then complete. Auditor requests scoped metadata.

### Then

- Prior 90-day minimum was honored. Exactly two disposal effects occur once each. Audit returns approved action metadata and no draft content.

### Fixture values

```json
{
  "prior_days": 90,
  "current_days": 60,
  "draft_age_days": 95,
  "drafts": 2,
  "resumed_tasks": 1,
  "total_disposals": 2,
  "audit_contains_draft_text": false
}
```

## PLAT-035 — Security revocation interrupts future reads of a vulnerable file

Covers `RevokeStorageObject`, `IssueAccessTicket`, `RedeemAccessTicket`, `StorageObject`.

### Given

- A clean published PDF has an active access ticket when a scanner rules update detects unsafe content.

### When

- An authorized security officer revokes the binary and two readers request another ticket or redeem an old one.

### Then

- Both later access paths fail. The previous published resource shows degraded file dependency. The file bytes and scan evidence remain quarantined until approved disposal.

### Fixture values

```json
{
  "old_ticket_count": 1,
  "new_ticket_count": 0,
  "bytes_delivered_after_revocation": 0,
  "binary_state": "revoked",
  "disposed": false
}
```

## PLAT-036 — Connector activation, cancel and reviewed removal keep exact roster versions

Covers `CreateIntegrationConnection`, `SetIntegrationConnectionState`, `StartSyncRun`, `ApproveSyncRun`, `CancelSyncRun`, `SyncPageReceipt`.

### Given

- An institution wants to onboard a roster adapter with profile roster-v1 and two active learners.

### When

- Register disabled, approve enable, run and cancel a dry run, then stage one absence in a verified complete snapshot. A reviewer tries to approve with stale local enrollment version, refreshes and approves exact current diff.

### Then

- Disabled connection sends nothing. Canceled dry run does not advance persistent cursor. Stale approval mutates nothing. Reviewed current decision invokes one canonical removal and records the applied version.

### Fixture values

```json
{
  "profile": "roster-v1",
  "dry_run_cursor_advances": 0,
  "reviewed_prior_version": 7,
  "reviewed_current_version": 8,
  "applied_removals": 1
}
```

## PLAT-037 — External map conflict cannot silently resurrect a removed account

Covers `SetExternalResourceDesiredState`, `ResolveExternalResourceConflict`, `RecordInboundOutcome`, `ExternalResourceMap`.

### Given

- A local person is mapped to provider P-77 at desired version 12 and has an active collaboration membership.

### When

- Publish explicit local removal at version 13. Receive a stale inbound identity update and record rejection. Reconciliation reviewer attempts to match a new P-77 by email then verifies the provider's original opaque identity.

### Then

- Desired removal remains at 13. Stale inbound does not reopen membership. Email-only resolution fails. Approved exact map reconciliation retains history and confirms removal.

### Fixture values

```json
{
  "old_local_version": 12,
  "desired_version": 13,
  "external_id": "P-77",
  "stale_message_state": "rejected",
  "reopened_memberships": 0
}
```

## PLAT-038 — Heartbeat and cancellation never close a different worker's lease

Covers `HeartbeatJobLease`, `FailPlatformJob`, `CancelPlatformJob`, `JobLease`.

### Given

- A job is leased at fence 30 with 120-second deadline. The first provider call fails before it is sent.

### When

- Heartbeat at 30 seconds, record transient failure with safe retry, cancel while waiting, then retry stale heartbeat and attempt to claim.

### Then

- Heartbeat had extended the live lease. Failure scheduled one retry at the specified bound. Cancellation prevents any new claim and stale heartbeat receives LEASE_FENCED.

### Fixture values

```json
{
  "initial_fence": 30,
  "heartbeat_after_seconds": 30,
  "initial_attempt_count": 1,
  "automatic_retry_min_seconds": 5,
  "post_cancel_claims": 0
}
```

## PLAT-039 — Recovery starts only from signed verified coverage

Covers `CaptureBackupSet`, `VerifyBackupSet`, `PlanRecoveryExercise`, `RecordRecoveryMilestone`.

### Given

- Backup object horizon covers 10:04:00, database horizon covers 10:03:30 and manifest is signed. Incident started at 10:05:00.

### When

- Capture and verify the set, plan restore at 10:03:30, record start and verification, then try to pass before independent approval and again after approved evidence.

### Then

- Unverified pass is rejected. Verified exercise reports RPO 90 seconds and RTO 7500 seconds, with protected result manifest retained.

### Fixture values

```json
{
  "incident_at": "2027-02-02T10:05:00Z",
  "verified_horizon": "2027-02-02T10:03:30Z",
  "reopened_at": "2027-02-02T12:10:00Z",
  "rpo_seconds": 90,
  "rto_seconds": 7500
}
```

## PLAT-040 — Changed remote payload cannot reuse an existing provider effect key

Covers `PrepareOutboundEffect`, `AuthorizeOutboundDispatch`, `RecordOutboundOutcome`, `OutboundEffect`.

### Given

- An authorized room removal operation is prepared under a stable effect key and digest A.

### When

- Retry identical preparation, then attempt preparation under same key with digest B and different recipient. Dispatch approved digest A once and record verified outcome.

### Then

- First replay resolves same prepared intent. Recipient substitution rejected before dispatch. Exactly one matching effect confirmed.

### Fixture values

```json
{
  "intents_committed": 1,
  "different_digests": 2,
  "effect_dispatches": 1,
  "confirmed_effects": 1
}
```

## PLAT-041 — Corrected labels and calendar metadata preserve released snapshots

Covers `UpdateAcademicPeriod`, `CorrectPersonDisplayName`, `AcademicPeriod`, `Person`.

### Given

- A published assessment and issued report pin learner name L1 and period version 4. A registrar finds an approved learner name correction and a term boundary error.

### When

- Attempt date correction without review, then submit authorized reviewed change and correct the current display name with evidence.

### Then

- Unreviewed dates fail. Authorized current period and name versions advance. Published assessment deadlines and old report label remain at their historical values until formal owner correction.

### Fixture values

```json
{
  "period_original_version": 4,
  "period_current_version": 5,
  "name_original": "L1",
  "name_current": "L2",
  "original_report_name": "L1",
  "original_deadline_changes": 0
}
```

## PLAT-042 — One data access case excludes another learner's records

Covers `PrivacyCaseStep`, `RecordPrivacyCaseStep`, `CompletePrivacyRequest`.

### Given

- Authorized learner requests own academic export. A teacher file contains own evidence and another learner's data.

### When

- Apply approved exact projection and record independent excluded field evidence before completion.

### Then

- Only own allowed fields reach the private artifact. No source content is deleted or mutated. Request is complete after all approved projections and exclusions are recorded.

### Fixture values

```json
{
  "approved_person": "L1",
  "excluded_person": "L2",
  "artifact_person_count": 1,
  "deleted_records": 0,
  "final_request_state": "completed"
}
```

## PLAT-043 — An empty reference set has positive completeness evidence

Covers `ContentReferenceSet`, `ContentReference`, `RefreshContentReferenceSet`, `ReadContentReferences`.

### Given

- A synthetic published text definition contains no reference-bearing nodes.
- The source owner returns an exact digest and allows this actor to reconcile it.

### When

- Refresh the definition set and read the returned generation.

### Then

- A ready set records entry_count zero and the canonical empty-sequence digest.
- Read returns zero entries from that generation. A nonexistent set never gives the same readiness guarantee.

### Fixture values

```json
{
  "source_kind": "ContentNodeVersion",
  "context_key": "definition",
  "expected_count": 0
}
```

## PLAT-044 — Source edits and target retirement share a reference fence

Covers `ContentReferenceSet`, `InvalidateContentReferenceSet`, `RefreshContentReferenceSet`.

### Given

- A source mutation introduces an asset reference while an asset purge requests a dependency census.

### When

- Serialize both commands through the same target retention fence and source invalidation transaction.

### Then

- If the reference wins, purge sees a current complete dependency or stale coverage and retains the asset.
- If retirement wins, creation rejects the retired target and the source cannot publish.
- A stale set never authorizes deletion.

### Fixture values

```json
{
  "orderings": [
    "reference_first",
    "retirement_first"
  ],
  "expected_missing_asset_publication": false
}
```

## PLAT-045 — One reusable definition binds links separately in two releases

Covers `ContentReferenceSet`, `ContentReference`, `RefreshContentReferenceSet`, `ReadContentReferences`.

### Given

- One definition contains a stable same-course placement selector.
- Two courses adopt the definition and each has its own exact target placement.

### When

- Create a definition set and refresh each publication placement context.

### Then

- The definition retains the selector without inventing a global placement target.
- Each binding pins its own course graph and exact source and target placement.
- Changing one graph invalidates only applicable bindings. Cross-course target substitution is rejected.

### Fixture values

```json
{
  "source_contexts": 2,
  "expected_distinct_bindings": 2
}
```

## PLAT-046 — A relation row cannot impersonate another target family

Covers `ContentReference`, `RefreshContentReferenceSet`.

### Given

- The relation is asset but the candidate row also includes a package target.

### When

- Validate the candidate and attempt owner reconciliation.

### Then

- The schema rejects the mixed row and reconciliation never marks a generation containing it ready.
- Digest collision is checked against full semantic keys rather than merging identities.

### Fixture values

```json
{
  "relation": "asset",
  "forbidden_extra_target": "package_version_id"
}
```

## PLAT-047 — Asset access does not reveal protected feedback dependencies

Covers `FindContentDependencies`, `ContentReferenceSet`, `ContentReference`.

### Given

- An authorized author may inspect a shared asset but cannot inspect an exam feedback rule that also uses it.

### When

- The author opens the asset dependency inspector.

### Then

- Only source relationships the author may know exist are returned, with no hidden-source count or cursor gap disclosure.
- The filtered result never authorizes asset deletion; retirement sees the protected dependency through its separately authorized complete census.

### Fixture values

```json
{
  "visible_relations": 0,
  "retention_dependency_exists": true
}
```
