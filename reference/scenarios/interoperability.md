# Interoperability acceptance scenarios

## INT-001 — Multipart finalization rejects gaps and verifies exact content

Covers `TransferUploadPart`, `FinalizeTransferUpload`, `TransferUploadFinalized`.

### Given

- Private upload declares 9 bytes. Parts are present at offsets 0 and 6, three bytes each.

### When

- Finalize with offsets 0 and 6.

### Then

- Return UPLOAD_PARTS_MISSING. No artifact becomes available and no finalization event exists.

### Fixture values

```json
{
  "declared_length": 9,
  "verified_offsets": [
    0,
    6
  ],
  "missing_offset": 3
}
```

## INT-002 — Repeated source key and local edits keep original identity

Covers `ExternalObjectMap`, `TransferRecord`, `BuildTransferPlan`.

### Given

- Approved crosswalk maps source scope term-a and item n1 to target A. Latest target revision was edited locally.

### When

- Plan reimport with the same source fingerprint.

### Then

- Suppress new version and preserve target A and local edits. Report informational divergence.

### Fixture values

```json
{
  "source_before": "aa",
  "source_after": "aa",
  "target_before": "01",
  "target_after": "02"
}
```

## INT-003 — Changed source and target require explicit three-way decision

Covers `ExternalObjectMap`, `BuildTransferPlan`, `ResolveTransferIssue`.

### Given

- An imported formula changed both at the source and in the native draft.

### When

- Reimport updated XML into the same mapping namespace.

### Then

- Set merge pending. Keep both baselines and prevent approval until assessment reviewer verifies parity.

### Fixture values

```json
{
  "prior_tolerance": "0.01",
  "source_tolerance": "0.1",
  "local_tolerance": "0.02"
}
```

## INT-004 — Unknown executable problem stays blocked

Covers `TransferIssue`, `ApproveTransferPlan`, `ResolveTransferIssue`.

### Given

- OLX problem includes a script that calls an external dependency. No equivalent verified grader is registered.

### When

- Attempt to accept the difference as a warning and apply plan.

### Then

- Reject BLOCKING_LOSS_CANNOT_BE_ACCEPTED. Learner publication remains unchanged.

### Fixture values

```json
{
  "problem_kind": "customresponse",
  "issue": "SCORING_PARITY_FAILED"
}
```

## INT-005 — Release barrier keeps partially promoted owner graph private

Covers `TransferJob`, `ApplyTransferPlan`, `TransferPlanApplied`.

### Given

- Curriculum owner staged its rows. Assessment owner's readiness receipt times out.

### When

- Retry with the same plan and idempotency key after the owner returns.

### Then

- First request exposes no staging. Retry activates exactly one generation and writes one mapping receipt.

### Fixture values

```json
{
  "owner_receipts": [
    "curriculum"
  ],
  "missing": "assessment",
  "attempts": 2
}
```

## INT-006 — Late destination revision forces renewed review

Covers `TransferApproval`, `ApplyTransferPlan`.

### Given

- Approved plan pinned native draft revision 7. Another editor publishes revision 8.

### When

- Apply the old approved plan.

### Then

- Reject TARGET_REVISION_CHANGED and return to awaiting review. Preserve both draft revisions.

### Fixture values

```json
{
  "approved_baseline": 7,
  "actual_baseline": 8
}
```

## INT-007 — Legacy library snapshot preserves draws and unresolved provenance

Covers `TransferRecord`, `BuildTransferPlan`.

### Given

- An OLX course contains six local problem IDs and a legacy reusable library key whose separate archive uses different IDs.

### When

- Stage the course and library in one plan.

### Then

- Preserve the six-item course-local pool and draw count two. Hold uncertain crosswalks for review.

### Fixture values

```json
{
  "draw_count": 2,
  "course_local": [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f"
  ],
  "reusable_source": [
    "p1",
    "p2",
    "p3",
    "p4",
    "p5",
    "p6"
  ]
}
```

## INT-008 — A signed archive still fails unsafe path validation

Covers `TransferArtifact`, `InspectTransferArtifact`.

### Given

- An archive passes configured signature verification and contains an encoded traversal entry.

### When

- Run quarantine inspection.

### Then

- Reject PACKAGE_PATH_REJECTED before expansion. Signature does not authorize bypass.

### Fixture values

```json
{
  "path": "static/%2e%2e/%2fsecret.html",
  "signature_valid": true
}
```

## INT-009 — Two activity occurrences share a resource but not state

Covers `PackageActivity`, `PackageResource`, `PackageScoState`, `OpenPackageLaunch`, `PackageActivityAttempt`.

### Given

- One resource is referenced by manifest items intro and review.

### When

- Commit a bookmark in intro and launch review.

### Then

- Review starts with its own state and cannot read intro bookmark.
- When the sequencer creates a new attempt at intro, it starts from edition defaults. Its earlier bookmark remains attached only to the historic intro attempt.

### Fixture values

```json
{
  "resource": "shared",
  "items": [
    "intro",
    "review"
  ],
  "intro_bookmark": "part-2"
}
```

## INT-010 — Replay returns a durable receipt without double time

Covers `CommitPackageRuntime`, `PackageCommit`, `PackageRuntimeCommitted`, `PackageRuntimeMutation`.

### Given

- First runtime request reached the server and receipt was lost.

### When

- Replay exact request and idempotency key, then finalize with 126,000 milliseconds.

### Then

- The replay returns state revision 8 and one receipt. The registration accrues 126,000 milliseconds once.

### Fixture values

```json
{
  "commit_request": {
    "protocol": 1,
    "registration_id": "019571a4-f8af-7ab1-8b7a-337194762001",
    "launch_session_id": "019571a4-f8af-7ab1-8b7a-337194762002",
    "occurrence_id": "019571a4-f8af-7ab1-8b7a-337194762003",
    "epoch": 4,
    "base_state_revision": 7,
    "first_sequence": 19,
    "mutations": [
      {
        "sequence": 19,
        "element": "cmi.location",
        "value": "review-2"
      },
      {
        "sequence": 20,
        "element": "cmi.completion_status",
        "value": "completed"
      },
      {
        "sequence": 21,
        "element": "cmi.score.scaled",
        "value": "0.85"
      }
    ],
    "finalize": false
  },
  "commit_response": {
    "registration_id": "019571a4-f8af-7ab1-8b7a-337194762001",
    "state_revision": 8,
    "accepted_through_sequence": 21,
    "commit_id": "019571a4-f8af-7ab1-8b7a-337194762004",
    "session_status": "active",
    "outcome_status": "pending_policy_projection"
  },
  "credited_ms": 126000
}
```

## INT-011 — Old tab cannot update after takeover

Covers `TakeOverPackageLaunch`, `CommitPackageRuntime`, `PackageLaunchSession`.

### Given

- Browser A owns epoch 3. Browser B takes over and receives epoch 4.

### When

- Browser A attempts a later score commit.

### Then

- Reject LAUNCH_EPOCH_STALE. Preserve browser B and existing accepted evidence.

### Fixture values

```json
{
  "old_epoch": 3,
  "new_epoch": 4,
  "attempted_score": "1"
}
```

## INT-012 — Invalid mutation makes a runtime batch atomic failure

Covers `CommitPackageRuntime`, `PackageRuntimeElement`.

### Given

- A 2004 session can write cmi.location but not cmi.learner_id.

### When

- Send both writes in one batch.

### Then

- Return RUNTIME_ELEMENT_REJECTED with first rejected sequence. Neither element changes.

### Fixture values

```json
{
  "accepted_through": 31,
  "mutation_elements": [
    "cmi.location",
    "cmi.learner_id"
  ],
  "rejected_sequence": 33
}
```

## INT-013 — Fourth-edition shared data grant refuses cross-occurrence write

Covers `PackageSharedDataStore`, `CommitPackageRuntime`.

### Given

- Manifest grants occurrence B read access to shared store memory and occurrence A write access.

### When

- Submit an edition-valid write under B.

### Then

- Reject write and preserve current value even though the field name and edition are supported.
- A new credit attempt on the same tree with default retention can read prior committed store data. An explicit attempt-lifetime store starts unset.

### Fixture values

```json
{
  "read_occurrences": [
    "B"
  ],
  "write_occurrences": [
    "A"
  ],
  "stored": "prior"
}
```

## INT-014 — Sequencing branch retains frozen child order after resume

Covers `PackageActivityAttempt`, `PackageSequencingState`, `NavigatePackageRegistration`.

### Given

- A selection cluster froze child order C then A for attempt 1 and suspended at C.

### When

- Resume then request Continue.

### Then

- Deliver A without drawing B or reseeding.

### Fixture values

```json
{
  "source_order": [
    "A",
    "B",
    "C"
  ],
  "frozen_order": [
    "C",
    "A"
  ],
  "suspended": "C"
}
```

## INT-015 — Objective unknown is distinct from failed

Covers `PackageObjectiveState`, `PackageObjectiveMapping`, `NavigatePackageRegistration`.

### Given

- Shared objective normalized measure is unknown before the mapped SCO reports an outcome.

### When

- Evaluate a rule requiring known measure less than threshold.

### Then

- Do not treat unknown as numeric zero. Evaluate using edition knownness semantics.

### Fixture values

```json
{
  "known": false,
  "threshold": "0.6"
}
```

## INT-016 — Valid QTI subset requires answer and score parity

Covers `QueueCurriculumExport`, `ExchangeProfile`, `BuildTransferPlan`.

### Given

- A multi-select QTI fixture scores exact A+C as 2 and A alone as 1. Native candidate would score A alone as zero.

### When

- Run transfer parity vectors.

### Then

- Mark the difference as blocking until exact partial-credit behavior is verified.

### Fixture values

```json
{
  "responses": [
    [
      "A",
      "C"
    ],
    [
      "A"
    ]
  ],
  "expected_scores": [
    "2",
    "1"
  ],
  "actual_scores": [
    "2",
    "0"
  ]
}
```

## INT-017 — Wrong LTI audience cannot establish a native launch

Covers `BeginToolLaunch`, `ExternalToolLaunch`, `ExternalToolDeployment`.

### Given

- Deployment registered issuer and client expected-client. A signed assertion has another audience.

### When

- Redeem or validate the launch assertion.

### Then

- Reject token despite valid signature. No resource context or service scopes are exposed.

### Fixture values

```json
{
  "registered_client": "expected-client",
  "assertion_audience": "other-client",
  "signature_valid": true
}
```

## INT-018 — Stale AGS score does not change native evidence

Covers `ExternalGradeBinding`, `PostExternalScore`, `ToolGradeEvidenceReceived`.

### Given

- The active binding accepted a 9 of 10 result at 10:05 UTC.

### When

- Receive 5 of 10 at 10:04 UTC and then replay original 10:05 payload.

### Then

- Earlier update is ignored. Identical replay returns prior receipt. No formal grade release occurs.

### Fixture values

```json
{
  "first_score": "9",
  "older_score": "5",
  "first_timestamp": "2026-10-01T10:05:00Z",
  "older_timestamp": "2026-10-01T10:04:00Z"
}
```

## INT-019 — Partial roster snapshot never withdraws absent enrollments

Covers `RosterFeed`, `RosterSnapshot`, `StageRosterSnapshot`.

### Given

- Connector expects three pages and page 3 fails. A learner appears only on page 3.

### When

- Try to stage a bulk reconciliation.

### Then

- Reject ROSTER_SCOPE_INCOMPLETE and keep all enrollments and feed watermark.

### Fixture values

```json
{
  "required_pages": 3,
  "received_pages": 2,
  "withdrawn": 0
}
```

## INT-020 — LRS statement retry reuses immutable ID

Covers `LearningRecordDelivery`, `QueueLearningRecordDelivery`, `RecordLearningRecordDelivery`.

### Given

- Destination response was lost after accepting statement ID a.

### When

- Retry outbound delivery using same statement ID and digest.

### Then

- Accept remote equivalent outcome once without creating new native grade evidence.

### Fixture values

```json
{
  "statement_id": "019571a4-f8af-7ab1-8b7a-337194762001",
  "first_transport_result": "lost_response",
  "replay_count": 1
}
```

## INT-021 — cmi5 Browse launch cannot create scoring evidence

Covers `Cmi5Registration`, `BeginCmi5Session`, `RedeemCmi5Fetch`.

### Given

- AU session is in Browse mode and credential fetched once.

### When

- Receive a completion statement then reuse fetch credential.

### Then

- Reject completion as outside mode and return profile fetch error without a second credential.
- A separate enrollment placement that reuses this ActivityVersion receives its own cmi5 registration UUID and no inherited AU evidence.

### Fixture values

```json
{
  "mode": "Browse",
  "statement_verb": "completed",
  "fetch_attempts": 2
}
```

## INT-022 — Historical cumulative grade never creates fictitious attempts

Covers `StageHistoricalRecords`, `TransferRecord`.

### Given

- Verified source supplies a learner's course total 82 percent but lacks per-item response and version data.

### When

- Stage historical summary import.

### Then

- Keep summary and source provenance. Record zero imported assessment attempts.

### Fixture values

```json
{
  "historic_grade": "82",
  "source_attempt_count": null,
  "target_attempts_created": 0
}
```

## INT-023 — Local acknowledgment is distinct from server commit

Covers `CommitPackageRuntime`, `PackageCommit`, `PackageLaunchSession`.

### Given

- Package writes pending bookmark in a browser with durable local storage. Network is offline.

### When

- Commit in strict remote mode and close browser.

### Then

- Return edition failure or show retry. No server receipt and no grade release are invented.

### Fixture values

```json
{
  "network": "offline",
  "browser_storage": true,
  "durability_profile": "strict_remote"
}
```

## INT-024 — Sensitive archive projection excludes unauthorized answer keys

Covers `QueueCurriculumExport`, `TransferArtifact`, `ExchangeProfile`.

### Given

- Operator can export curriculum but does not hold answer export authority.

### When

- Request native export with include_answers true.

### Then

- Return ANSWER_EXPORT_DENIED. A separate redacted learner profile may proceed with no protected refs.

### Fixture values

```json
{
  "include_answers": true,
  "answer_authority": false
}
```

## INT-025 — Operator uploads, seals and privately stages a deterministic curriculum input

Covers `OpenTransferUpload`, `RecordTransferUploadPart`, `FinalizeTransferUpload`, `StartTransferJob`, `TransferArtifact`, `TransferJob`.

### Given

- Authorized transfer operator has a registered namespace and six-byte synthetic file with part bytes abc and def.

### When

- Open upload, record parts at offsets 0 and 3, replay identical part 0, finalize with the verified whole digest, and start dry run.

### Then

- Replay returns the same part identity, one artifact is quarantined and one received transfer job is created. No course becomes learner-visible.

### Fixture values

```json
{
  "source_namespace": "urn:school-example:fractions",
  "parts": [
    {
      "offset": 0,
      "bytes": "abc"
    },
    {
      "offset": 3,
      "bytes": "def"
    }
  ],
  "full_sha256": "bef57ec7f53a6d40beb640a780a639c83bc29ac8a9816f1fc6c5c6dcd93c4721",
  "mode": "dry_run"
}
```

## INT-026 — Private transfer pagination is bound to one version and permits safe cancellation

Covers `ReadTransferPlan`, `CancelTransferJob`, `ResolveTransferIssue`.

### Given

- Reviewer has plan revision 4 and its next-page cursor. Another reviewer attaches the missing caption and creates revision 5.

### When

- Use the revision 4 cursor, fetch again without the cursor, and cancel revision 5 before promotion.

### Then

- Reject first read with CURSOR_PLAN_CHANGED. Fresh read sees revision 5. Cancellation records a terminal job and revokes private stage grants.

### Fixture values

```json
{
  "cursor_revision": 4,
  "active_revision": 5,
  "visible_generations": 0
}
```

## INT-027 — Expired transfer worker is fenced after a successful reclaim

Covers `ClaimTransferJobLease`, `InspectTransferArtifact`, `TransferJob`.

### Given

- Worker A claimed epoch 17 for 60 seconds and stopped heartbeating. Its lease expired at 10:01:00 UTC.

### When

- Worker B claims at 10:01:01 UTC. Worker A then tries to commit its completed scan at epoch 17.

### Then

- Worker B receives epoch 18. The stale inspection gets WORKER_FENCE_STALE and cannot change the typed source graph.

### Fixture values

```json
{
  "old_epoch": 17,
  "new_epoch": 18,
  "claim_at": "2026-10-01T10:01:01Z",
  "expired_at": "2026-10-01T10:01:00Z"
}
```

## INT-028 — Package approval, origin-bound redemption and lease expiry preserve saved prefix

Covers `ApprovePackageVersion`, `OpenPackageLaunch`, `RedeemPackageLaunch`, `ReadPackageRuntimeReceipt`, `ExpirePackageLaunch`, `PackageLaunchSession`.

### Given

- Reviewer approved strict 1.2 package with browser evidence. Enrolled learner receives an isolated launch scoped to epoch 1.

### When

- Try redemption at an unapproved origin, redeem at the approved origin, accept two writes, let the writer expire without Finish and query the receipt through the owning learner session.

### Then

- Wrong origin fails. Approved redemption succeeds only once. Expiry marks interrupted with accepted prefix 2. The owning authenticated learner reads the receipt and no Finish or completion evidence is invented.

### Fixture values

```json
{
  "edition": "1.2",
  "approved_origin": "https://launch-17.example-content.org",
  "wrong_origin": "https://school.example.org",
  "accepted_through": 2,
  "final_state": "interrupted"
}
```

## INT-029 — A signed Deep Linking response is scoped to its selected version and does not publish

Covers `RegisterToolDeployment`, `BeginToolLaunch`, `ApproveDeepLinkSelection`, `ExternalToolResourceLink`.

### Given

- Integration admin registers an exact HTTPS issuer and client. Teacher launches Deep Linking against draft A revision 6, with pinned browser binding and two-item limit.

### When

- The tool returns a signed item targeting an allowed origin and a second item from a denied origin. The teacher starts a fresh correlated launch and submits only a valid allowed item, then replays that response.

### Then

- First response fails validation and stages nothing even if the denied item is unselected. Fresh valid response stages exactly one inert link. Its replay returns the same receipt or TOOL_LAUNCH_REPLAYED. No placement is published.

### Fixture values

```json
{
  "issuer": "https://tool.example.org",
  "allowed_target": "https://tool.example.org/lessons/ratio",
  "denied_target": "https://other.example.org",
  "selected_indices": [
    0
  ]
}
```

## INT-030 — Roster bulk apply atomically changes authoritative scope and watermark

Covers `StageRosterSnapshot`, `ApplyRosterSnapshot`, `RosterSnapshotApplied`, `RosterFeed`.

### Given

- Complete snapshot sequence 43 covers one term and proposes withdrawal of two feed-owned enrollments and no locally managed enrollment.

### When

- Attempt approval with withdrawal count 1, then approve exact count 2 using the unchanged projection digest and baseline.

### Then

- First apply rejects ROSTER_WITHDRAWAL_NOT_APPROVED. Second applies both feed-owned withdrawals and advances watermark to 43 in one transaction.

### Fixture values

```json
{
  "prior_sequence": 42,
  "new_sequence": 43,
  "predicted_withdrawals": 2,
  "wrong_approval_count": 1
}
```

## INT-031 — AGS binding cannot be reused for another course item

Covers `BindExternalGradeItem`, `PostExternalScore`, `ExternalGradeBinding`.

### Given

- Deployment has line item math-quiz in offering A with maximum 20. Offering B contains a similarly named GradeItem.

### When

- Bind line item to authorized GradeItem A, then submit a conflicting bind to B and valid score 3 of 4 to A.

### Then

- Conflicting bind is rejected. Accepted evidence for A normalizes to 15 of 20. No grade release or update to B.

### Fixture values

```json
{
  "external_line_item": "math-quiz",
  "score_given": "3",
  "score_maximum": "4",
  "destination_maximum": "20",
  "mapped_points": "15"
}
```

## INT-032 — cmi5 defined statements are ordered and mode constrained

Covers `BeginCmi5Session`, `RedeemCmi5Fetch`, `RecordCmi5StatementEvidence`, `Cmi5LaunchSession`.

### Given

- Authorized Normal AU launch pins actor, registration, AU and session. A separate Browse launch is also authorized.

### When

- In Normal mode, receive completed before initialized, then initialized and replay completed. Send passed from the Browse session.

### Then

- The first Normal completion remains pending until its predecessor. Verified replay applies eligible evidence once. Browse scoring returns CMI5_MODE_FORBIDS_EVIDENCE.

### Fixture values

```json
{
  "normal_arrival": [
    "completed",
    "initialized",
    "completed"
  ],
  "browse_verb": "passed",
  "eligible_normal_completion_count": 1
}
```

## INT-033 — Independent cmi5 registrations for repeated placements

Covers `ResolveCmi5Registration`, `Cmi5Registration`, `Cmi5RegistrationResolved`, `BeginCmi5Session`.

### Given

- Enrollment E is assigned the same ActivityVersion and PackageVersion at placements A and B.

### When

- Resolve A twice with identical key, complete its AU, resolve B, then begin a B session.

### Then

- A reuses one UUID. B has a different UUID and its own attempt ordinal 1. A completion does not satisfy B.

### Fixture values

```json
{
  "same_activity_version": true,
  "placements": [
    "A",
    "B"
  ],
  "attempt_ordinals": [
    1,
    1
  ],
  "completed_placements": [
    "A"
  ]
}
```

## INT-034 — Platform launch consumes tool-originated state and nonce once

Covers `BeginToolLaunch`, `AuthorizeToolOidcLaunch`, `ToolLoginInitiated`, `ToolLaunchAuthorized`.

### Given

- Learner is authorized for a released resource and registered tool callback https://tool.example.org/lti/redirect.

### When

- Start login initiation, return exact hints and tool-originated state S1 and nonce N1, then replay the same authorization and try an unregistered redirect.

### Then

- Only first authorized request signs. The ID token carries N1 and the form carries S1. Replay or altered redirect cannot obtain another token.

### Fixture values

```json
{
  "tool_state": "S1",
  "tool_nonce": "N1",
  "redirect_uri": "https://tool.example.org/lti/redirect",
  "tokens_signed": 1
}
```

## INT-035 — Root selection and typed edges remain scoped to the selected graph

Covers `InspectTransferArtifact`, `BuildTransferPlan`, `ReadTransferPlan`, `ReadTransferEdges`, `TransferJob`, `TransferRecord`, `TransferEdge`.

### Given

- One synthetic ZIP has two root candidates with shared body bytes and separate policy scopes.
- The chosen root contains two placements of one reusable definition and a valid inline extension with no same-type directory. A detached pointer is missing.

### When

- Inspect the container and profile. Explicitly select one frozen root key. Build the plan and page the outgoing edges by exact plan revision.

### Then

- The verified container and decoder profile are recorded independently. Shared body does not merge root policy.
- The placements and context-sensitive links have distinct occurrence keys. The inline definition resolves. The detached problem remains restricted inventory.

### Fixture values

```json
{
  "candidate_roots": 2,
  "selected_roots": 1,
  "shared_definitions": 1,
  "distinct_placements": 2,
  "detached_missing_pointers": 1
}
```

## INT-036 — Required selected edges block dry-run application and expose no generation

Covers `BuildTransferPlan`, `ApplyTransferPlan`, `ApproveTransferPlan`, `TransferEdge`, `ExternalObjectMap`.

### Given

- The selected published graph has a missing required dependency. A dry-run plan includes a detached warning as well.

### When

- Read reconciliation, attempt approval and application, then restore the dependency and approve a separate editable plan. Apply keep_private twice with one logical key.

### Then

- No dry-run owner-visible drafts or active crosswalks exist. An unresolved required edge cannot be promoted.
- Once reviewed and repaired, the exact private generation and scoped map commit once. No EnrollmentRelease or learner publication changes.

### Fixture values

```json
{
  "dry_run_writes": 0,
  "required_unresolved": 1,
  "detached_warnings": 1,
  "private_generations": 1,
  "learner_publications": 0
}
```

## INT-037 — Completed portable export pins approval, exact bytes and revocable collection

Covers `QueueCurriculumExport`, `RecordCurriculumExportProjection`, `ApproveTransferPlan`, `CompleteCurriculumExport`, `ReadCurriculumExport`, `AuthorizeCurriculumExportDownload`.

### Given

- A synthetic published course is eligible for a tested fourth-edition generator. Its portable projection intentionally excludes one optional private editorial note.

### When

- Queue the exact profile, record protected reports, independently approve the plan, complete verified bytes, replay the completion, read the safe projection and request a ticket.
- Revoke the actor's export authority before ticket redemption.

### Then

- One completed exact edition and output digest are recorded. The optional omission is reported. Identical retry creates no second result or event.
- Revoked authority blocks redemption even before the collection window ends.

### Fixture values

```json
{
  "format": "scorm_2004_4",
  "required_losses": 0,
  "optional_differences": 1,
  "completed_results": 1,
  "bytes_after_revocation": 0
}
```

## INT-038 — Prohibited solution disclosure and unverified output never fall back

Covers `QueueCurriculumExport`, `RecordCurriculumExportProjection`, `ApproveTransferPlan`, `CompleteCurriculumExport`, `ReadCurriculumExport`.

### Given

- The target edition is disabled on one profile. A second approved profile could render a required assessment only by embedding confidential solutions.

### When

- Try the disabled output and the recognized-but-unverified input edition. Attempt portable projection under the second profile with answer disclosure off.

### Then

- The unsupported directions are rejected without fallback. The scorer is a blocking required loss. No approval can make an output available or relabel another edition.

### Fixture values

```json
{
  "input_only_format": "scorm_2004_unverified",
  "embedded_disclosure_allowed": false,
  "required_losses": 1,
  "available_results": 0
}
```
