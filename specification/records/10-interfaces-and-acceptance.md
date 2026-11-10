# 10 Records interfaces and acceptance

The [catalog](catalog.json) is the machine-readable companion for scoped entities, operations, events and acceptance fixtures. An endpoint is a proposed service contract. A deployment can bind an equivalent command bus while preserving payload semantics, state transitions and caller controls.

## Command mechanics

Use UUID path identifiers. Derive institution and principal from the authenticated session or scoped service token. If a UUID exists outside the caller's scope, return 404 to avoid confirming protected existence. Use 403 for a known, visible resource with an action the caller cannot perform. A command that creates, applies, releases or corrects official data requires Idempotency-Key. Scope keys by institution, principal and command. A reused key with a different canonical request returns 409 IDEMPOTENCY_CONFLICT. An identical retry returns the saved operation result. On lost HTTP response, the caller retries the same request and key. A new semantic request must use a new key.

Require an opaque If-Match token or explicit immutable parent ID for updates and approve/apply operations. Return a newly scoped ETag and representation. An outdated token returns 412 STALE_REVISION. If the preview's evidence, policy or prior release changed, return 409 PREVIEW_STALE with a fresh authorized preview action. Validation errors return 422 and bounded details without protected source data. Use 428 when a required HTTP precondition is absent, 429 for throttling and 503 for transient unavailability. Include Retry-After where applicable. Paged reads return cursor and as-of checkpoint. Bind the cursor to caller scope and query and reject a changed or revoked scope.

## Examples

A grade release preview binds a named cutoff, kind and authorized enrollment set. Only final rows that satisfy policy are release-ready.

```http
POST /v1/offerings/018fb410-01ad-71c7-b81c-9ef32274d511/grade-releases
Content-Type: application/json
Idempotency-Key: offering-final-2026-t2-run-1

{
  "academic_period_id": "018fb410-01ad-71c7-b81c-9ef32274d512",
  "purpose": "final",
  "enrollment_ids": ["018fb410-01ad-71c7-b81c-9ef32274d513"],
  "cutoff_at": "2026-10-31T16:00:00Z",
  "allow_partial": false
}
```

```json
{
  "id": "018fb410-01ad-71c7-b81c-9ef32274d514",
  "state": "staged",
  "manifest_digest": "4b243fde84d7516bc1490bd73442f861a3be3efe02e26c95271f1d6e770221d8",
  "ready_count": 1,
  "blocked_count": 0
}
```

The reviewer opens the staged release, checks outcome counts and submits the approved manifest digest. A changed input returns PREVIEW_STALE. A successful activation marks the manifest active and creates one release event. A conflicting old review does not update an active release. The browser announces success or stale state in text and provides a link back to the refreshed result list.

```http
POST /v1/grade-releases/018fb410-01ad-71c7-b81c-9ef32274d514/activation
Content-Type: application/json
Idempotency-Key: approved-release-2026-t2-1
If-Match: "v1-stage-514"

{
  "manifest_digest": "4b243fde84d7516bc1490bd73442f861a3be3efe02e26c95271f1d6e770221d8",
  "approval_note": "Final term review completed."
}
```

Example error body uses a machine identifier and human message. Only an authorized caller gets counts for the requested subset.

```json
{
  "type": "urn:lms:problem:preview-stale",
  "title": "Grade release preview changed",
  "status": 409,
  "code": "PREVIEW_STALE",
  "request_id": "018fb410-01ad-71c7-b81c-9ef32274d515",
  "detail": "Evidence changed after preparation. Create and review a new preview."
}
```

## Usability contracts

- Gradebook grid uses proper row and column headers, keyboard movement, stable focus and text status. Support virtualized rendering without making all visible cells keyboard traps. Provide a screen-reader-friendly per-learner detail mode with identical data.
- Bulk edits show a preview and validation. Rows outside scope are rejected even when hidden by the active filter. A parent policy requiring two-person approval applies to bulk edits. Do not implement bulk upload as unchecked spreadsheet writes.
- A staff member filters by section, period and role, then opens a learner's result explanation with source, adjusted score, denominator, policy and release status. A direct URL is scope-checked. A grade cell displays blank, zero, pending, excused and withheld distinctly.
- An official report work queue shows render progress, digest, prior issuer, replacement reason and issuance state. Provide an accessible HTML preview before print. If rendering fails, show the error class and retry action without exposing source details.
- The learner view explains differences between tentative progress, item feedback, released marks and final grades. The standard direct link never includes a protected score in the URL. Show correction history according to policy, retaining approval provenance for staff.
- A registrar bulk export reports rows, scope, suppressed records, schema and encrypted destination where applicable. On scope revocation cancel download and clear generated links. Historical audit remains available only to authorized readers.

## End-to-end acceptance

| Case | Setup and action | Required outcome |
| --- | --- | --- |
| Replay | Reprocess native evidence E3 then E2 then E3 | One current E3 selection. Earlier E2 remains retrievable for earlier cutoff. No duplicate grade or notification. |
| Exact arithmetic | Grades 50/50, 65/100, 12/24, low impact drop | B dropped. Persist 31/37. Display 83.78 percent. |
| Learner visibility | Teacher sees 9/10 posted and 1/10 withheld | Learner current aggregate remains 90 percent from posted evidence. Staff preview shows 50 percent. |
| Mark not missing | A submitted work has pending grader, B confirmed missing and 10 possible | Final blocks for A. B may be recognized zero under policy. Never convert A to zero. |
| Parallel release | Two final release activations overlap the same enrollment result | First commits with notification, second fails stale. No half-published manifest. |
| Corrected transcript | Course mark changes after official transcript | Original revision retains artifact digest. New grade release, credit review and replacement issue independently. |
| Transfer credit | Approved 3-credit transfer with no grade points | Adds 3 earned credits. GPA divisor and quality points unchanged. |
| Institutional isolation | Scoped assistant guesses UUID in another institution | No grade, existence clue, audit log detail or export. |
| Report reproducibility | Numeric release changes after CSV generation | Old authorized snapshot keeps cutoff and digest. New export reflects new release and uses distinct snapshot. |
| Programme overlap | Astronomy satisfies A, only Chemistry satisfies B | Allocator finds both fulfilled and counts 6 distinct credits. |
| Issuance replay | Credential approval response is lost and command retried | One credential, one issue event, same approved source evidence. |
| Analytics suppression | A report group has 7 unique people and can be derived from subtotal | Suppress small group and enough companion cells to prevent direct subtraction. |
