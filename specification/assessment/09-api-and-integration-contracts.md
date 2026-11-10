# 09. API, handoff and verification contracts

The domain exposes separate author, candidate, marker, scheduler, worker and academic evidence surfaces. All mutable records have stable UUIDs. Opaque immutable references and authorization are required on read and write. ETags are strong validators for mutable document representations. Candidate saves carry per-response compare-and-swap versions. See [HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html#name-if-match). See the adjacent [catalog](catalog.json) for request fields, errors, permissions and persistence invariants.

## Request examples

The candidate starts from an offering-bound delivery. The identity is resolved from the authenticated principal and candidate enrollment. The policy acknowledgement digest matches the displayed effective policy. An unknown UUID returns the same outward denial as an out-of-scope resource where existence is sensitive.

```http
POST /v1/assessment-deliveries/82ad87c8-4e29-4821-ad85-05e49da78204/attempts
Idempotency-Key: 01HT6T958CT6TCH2X67W0RKP6A
Content-Type: application/json

{"enrollment_id":"877daed9-977c-432e-bf27-c8f4b20574a2","expected_enrollment_release_id":"53410893-ff5c-4f57-bd22-0ca33f1f2ca4","policy_acknowledgement_digest":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```

```json
{
  "attempt_id": "095776b4-053a-4fda-804b-801b1d79df31",
  "state": "in_progress",
  "ordinal": 1,
  "enrollment_release_id": "53410893-ff5c-4f57-bd22-0ca33f1f2ca4",
  "deadline_at": "2026-11-10T10:37:00Z",
  "draft_version": 1,
  "lease_id": "94f6f8b9-51c4-463b-871d-d34c147fd7d2"
}
```

An autosave targets explicit attempt item and interaction. The payload is protected from HTTP logs. One expected revision per response allows separate fields to merge safely.

```http
POST /v1/assessment-attempts/095776b4-053a-4fda-804b-801b1d79df31/saves
Idempotency-Key: 01HT6V1X9C0K44BASZ5P26JQ27
Content-Type: application/json

{"lease_id":"94f6f8b9-51c4-463b-871d-d34c147fd7d2","edits":[{"attempt_item_id":"1a586135-0f38-452d-bb26-884bf30d6179","interaction_key":"quantity","expected_revision":2,"action":"set","value":{"kind":"quantity","input":"36","unit":"km/h","locale":"en-NA"}}]}
```

```json
{
  "attempt_id": "095776b4-053a-4fda-804b-801b1d79df31",
  "draft_version": 4,
  "accepted_at": "2026-11-10T10:35:14.000Z",
  "results": [{"attempt_item_id":"1a586135-0f38-452d-bb26-884bf30d6179","interaction_key":"quantity","revision":3,"state":"valid"}]
}
```

Finalize takes the candidate's confirmed draft version in the strong precondition header and the last returned version in the request. A missing precondition receives `428 PRECONDITION_REQUIRED`. A stale precondition receives `412 DRAFT_CHANGED`. An unchanged draft with unacknowledged blanks receives `422 BLANKS_NOT_ACKNOWLEDGED` when policy requires acknowledgement. A distinct concurrent start receives `409 ATTEMPT_ALREADY_ACTIVE` and can recover its eligible attempt pointer from availability. Support redaction based on whether the caller can learn the record exists.

```http
POST /v1/assessment-attempts/095776b4-053a-4fda-804b-801b1d79df31/submission
If-Match: "attempt-draft-4"
Idempotency-Key: 01HT6V2PMRWY54ZVTNAXJKNY8S
Content-Type: application/json

{"lease_id":"94f6f8b9-51c4-463b-871d-d34c147fd7d2","expected_draft_version":4,"acknowledge_blanks":true}
```

```json
{
  "attempt_id":"095776b4-053a-4fda-804b-801b1d79df31",
  "submission_id":"c5224931-cfee-4bee-8a7d-60872f2a6e6b",
  "receipt_id":"ee577c30-73d5-4938-bc28-96d944fe63cc",
  "state":"submitted",
  "effective_at":"2026-11-10T10:35:15.000Z",
  "processed_at":"2026-11-10T10:35:15.000Z"
}
```

Errors carry status, machine-readable code, safe field issues and trace ID. A response conflict returns 409 with current known revision for authorized fields. Expiry returns a receipt link when a submission already exists, or terminal state and next action. Apply `429` and `Retry-After` when short admission or evaluation service limits apply. Exports and bulk jobs return operation IDs, progress counters and protected outcome downloads rather than blocking interactive requests.

## Academic grade evidence boundary

Assessment emits one native GradeEvidence revision per source tuple of delivery, enrollment, attempt and grade item. It records accepted raw points and maximum for earned evidence before academic attempt and late-penalty policy, grading state, effective submission time, attempt ordinal, captured enrollment release, assessment and delivery policy revisions, native due classification, accepted time, ordered ItemMarkRevision IDs or protected lineage digest and predecessor. Team marking projects one evidence revision per eligible frozen member. The same evidence owner accepts manual, package and external observations through `AcceptExternalGradeEvidence` after validating producer registration, source scope, point limits, approval reference and strictly ordered revision. Records staff can operate an approved manual score UI that submits to this owner. It does not write evidence storage. Candidate eligibility, attempt timing and attempt source remain queryable by academic policy. This domain emits observed attempt facts and does not choose highest, latest, weighted, missing, credit, override or released course grade. Separate academic commands decide policy and release.

When a revision is accepted, domain commit writes evidence and outbox atomically. The payload includes evidence ID, enrollment and offering scope, source key and monotonic evidence revision. Event identity and occurrence time are taken from the shared envelope. It omits answer values, private rubric comments and score content unless a separately authorized service contract explicitly needs a protected payload. Consumer fetches authorized evidence and deduplicates by event ID and source revision. A duplicate event cannot add a second result. A consumer missing revision 2 but receiving revision 3 fetches the gap or authoritative head, preserving lineage. Cancellation or excuse arrives as a new evidence revision rather than deleting prior evidence. Official report records can reference earlier revisions permanently under policy.

Candidate feedback release stays in assessment. Official academic GradeRelease and report cards are independently owned. One service exposing an official grade must not accidentally bypass held candidate assessment feedback or answer restrictions.

## Acceptance suite

Run typed fixtures at schema, command, transaction and read projection levels. An evaluator fixture pins profile version, inputs, expected safe outputs, private reason and deterministic digest. A workflow fixture declares initial states, actors, request order, authority times, durable effects, emitted events and forbidden observations.

| Case | Observed behavior |
| --- | --- |
| Stale role grant | A revoked marker receives denial before fetching submission assets. A previously assigned task does not grant new access by itself. |
| Deadline boundary | Exact equality to the deadline rejects new response. Worker seals last earlier save under auto submit. |
| Crash after sealing | Restart restores one receipt and one durable submission event. Duplicate delivery schedules no extra mark. |
| Worker replay | Expired lease result is ignored. Current result and an identical retry create one accepted result. |
| Parent age-out | A retained sealed attempt remains readable to authorized records staff when a course offering or bank is archived. |
| Unsupported file | Upload completion detects invalid type, rejects and never includes it in the final manifest. |
| Provisional confidentiality | Candidate view, accessible HTML, notifications and analytics omit private marks until release. |
| Grade evidence correction | Revision 2 supersedes revision 1 without mutating the prior revision or official report snapshot. |
| Protected inputs | Evaluation diagnostics contain allowlisted codes and numeric resource telemetry without the answer key, candidate response or accommodation evidence. |
| Import sample drift | Re-evaluation of representative source and target fixtures detects a scoring mismatch before release. |

Measure candidate save latency, clock deviation, held-mark counts, worker queue time, evaluator fault rate and regrade conflict rate. Scope operational metrics to avoid response details and small-group inference. Use chaos tests for node crashes between each durable write, delayed outbox dispatch, delayed scans and clock incidents. Formal acceptance requires reproducible attempts and appeal evidence under a simulated restore.
