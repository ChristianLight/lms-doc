# Command and event protocol

## Request context

Every command executes with an authenticated context assembled by the trusted application boundary. The request body cannot override that context. Its fields are institution ID, principal ID, authentication strength where relevant, delegated scope if present, current authorization revision, locale, request ID, and the server receipt time. The principal must be active and its identity link must resolve within the selected institution.

An administrator performing a delegated action identifies the acting principal and the represented scope. The resulting audit preserves both. A background worker acts under its own service principal and records the initiating principal or approved policy. Replaying an old job does not inherit unlimited authority from a previously logged-in administrator. The worker verifies that the job still has a permitted purpose and valid target state.

## Request keys and receipts

A command with non-repeatable effects requires an idempotency key. The client creates an opaque value of 16 to 128 characters and retains it until the result is known. The server scopes it by institution, principal, operation and target, and stores a canonical request fingerprint with it.

Use a durable receipt record containing operation, scoped key, payload digest, processing state, authoritative target and revision, response status, safe result body, first accepted time, completion time, and retention deadline. The digest uses canonical serialization of the semantically relevant request. Exclude transport headers, tracing IDs and access tokens. Include selected target IDs, policy choices and submitted values.

| Existing receipt | Incoming request | Result |
| --- | --- | --- |
| Absent | Valid and authorized | Create a processing claim and execute under the operation's transaction |
| Processing | Same digest | Return the processing receipt or wait within the documented bounded request window |
| Completed | Same digest and currently authorized read | Return the original receipt and result |
| Completed or processing | Different digest | Reject with `IDEMPOTENCY_CONFLICT` |
| Failed before authoritative commit | Same digest | Retry only when the error is marked retryable and the prior processing claim has expired safely |
| Receipt expired | Any | Resolve the target's natural uniqueness or command-specific history before permitting another effect |

Permission checks occur before disclosing a prior result. Idempotency prevents duplicate effects but does not grant durable access to sensitive returned data. A withdrawn learner can still query an authorized submission receipt under the review policy without receiving other records that the current access policy conceals.

## Revision concurrency

A mutable draft carries a monotonic owner revision. Update commands include `expected_revision` or an equivalent conditional header defined in the operation contract. The owner atomically compares and changes it. A mismatched body revision returns `REVISION_CONFLICT` with a safe current revision and permitted refresh link. A failed HTTP If-Match precondition returns 412, and a required missing If-Match returns 428. The guarded resource read and a successful versioned mutation supply the owner-issued strong ETag to use unchanged on the next request. ETags are scoped to the authorized representation and its schema and visibility variant. The server resolves them to the owner record revision rather than accepting a client-invented tag. The caller may fetch the latest draft and propose a merge. The server never applies an unreviewed last-writer-wins merge to grading rules, rosters or publication graphs.

For child collections, the parent revision covers membership and order. A full replacement request includes the complete collection, stable child IDs and expected parent revision. The owner verifies every submitted child belongs to the parent, validates all changes, and applies them atomically. A partial update endpoint uses explicit add, update, move and remove operations. It does not interpret omitted children as deletion.

For append-only evidence, uniqueness replaces mutable version comparison. Each response revision has an attempt-local sequence and a request key. A submission manifest selects exact accepted response revisions. Once sealed, later autosaves are rejected or retained as non-authoritative incident evidence according to the attempt policy. The finalization command's transaction decides which response revision was accepted before cutoff.

## HTTP representation

The generated OpenAPI document uses JSON Schema Draft 2020-12 through OpenAPI 3.1.1. Authentication in the portable API is a bearer service context. A host-session adapter can expose the same commands using its own authentication and anti-forgery mechanisms, with equivalent object authorization and receipts. The API contract does not require an implementation to expose every internal command over the public internet.

| Status | Meaning | Caller action |
| --- | --- | --- |
| 200 | An existing or updated authoritative result is available | Consume the receipt and returned revision |
| 201 | A new authoritative resource was committed | Retain its ID and receipt |
| 202 | Durable work was accepted but completion is pending | Poll the receipt or await the scoped event |
| 204 | An operation committed and has no response body | Retain the request key and any receipt header |
| 400 | The protocol envelope cannot be interpreted | Correct the request representation |
| 401 | Authentication is missing or expired | Renew authentication through the provider and retry the same request key if safe |
| 403 | The actor lacks permission for the requested action | Seek an authorized actor or corrected scope |
| 404 | The authorized resource cannot be resolved | Refresh the permitted resource list |
| 409 | State, revision or idempotency conflicts | Inspect authoritative state and reconcile |
| 410 | A documented ephemeral resource has expired | Follow the owner-provided renewal or restart action |
| 412 | An HTTP revision precondition failed | Fetch the authorized current representation and reassess the change |
| 413 | The request exceeds its declared byte or item limit | Use the supported chunk or batch protocol |
| 422 | Schema or business validation failed | Correct the identified fields without changing unrelated work |
| 428 | A required conditional header is missing | Read the target and supply its strong ETag |
| 429 | Scoped workload limits were exceeded | Honor retry timing and reuse the request key |
| 503 | Durability or a required owner is unavailable | Query the receipt before retrying |

Credentials and access tickets travel in the declared authentication or secret headers. The catalog parameter_locations metadata maps those abstract command arguments to headers. They are excluded from query strings, cache keys, analytics URLs and ordinary request logs.

Error bodies use a problem object with `type`, `title`, `status`, `code` and `request_id`. Optional `detail` explains a safe corrective action. Field errors use JSON pointers, machine-readable codes and localized messages. Never include protected solution values, student records outside the caller's scope, provider secrets or full uploaded documents in error text.

## Event envelope

An event is emitted after an authoritative commit through a durable outbox. Its envelope contains event ID, event type, contract version, producer, institution ID, aggregate type and ID, aggregate revision, occurred time, recorded time, causation ID, correlation ID, initiating principal where permitted, and payload. A payload schema is stored in the event catalog. The envelope version and payload contract version evolve independently.

`occurred_at` records the business instant established by the owner. `recorded_at` records when the event entered durable storage. A delayed import can therefore preserve historical academic dates without pretending the event was created in the past. Consumers use aggregate revisions and dependencies for ordering, not the wall clock alone.

A consumer stores an inbox receipt keyed by consumer name and event ID. Applying the event and recording that receipt form one transaction. On redelivery, return the accepted result or acknowledge the duplicate. A message marked accepted must never have its side effect applied twice. Provider effects require a provider request key or a reconciliation query before retrying after an uncertain response.

## Out-of-order delivery

The event policy declares whether each consumer can accept revisions out of order, must buffer until a predecessor appears, or can replace a projection by fetching authoritative state. For a grade result release, applying an older revision after a newer one must not restore the old current pointer. A historical ledger can retain both while selecting the highest authorized release sequence.

When an event depends on another object, retain it in a waiting state with the missing dependency and a bounded retry schedule. Do not create placeholder users, grades or enrollments to satisfy a failed lookup. After the retry limit, expose an operator-visible reconciliation item with the exact unresolved keys and permitted recovery. An operator retry reuses the original event identity.

## Batch operations

Every batch endpoint declares atomic or partial-success semantics. Publication and sealed submission manifests are atomic. Large imports can stage individual records, then promote a complete validated graph atomically or under an activation barrier. Bulk notifications allow per-recipient outcomes. Bulk grade posting validates the full selected population, records the approved set, and publishes only through the declared batch policy.

A partial-success response identifies each item by its stable request key with status, target ID or issue code, and safe retry action. It never reports only a count when the caller needs to reconcile which learner or course changed. An atomic batch failure returns the failing validation set and confirms that the authoritative target graph was not activated.

## Pagination and asynchronous reads

Collections use bounded page sizes and a stable order with a unique tie-breaker. A cursor binds institution, query filters, permission context, sort key and optional snapshot watermark. Reject a cursor reused for another tenant or query. A changed authorization context requires a new cursor. Long reports run against an explicit reporting cutoff or snapshot and declare how concurrent updates are handled.

Asynchronous exports have a separate authorization check at creation and download. A download grant is short-lived, scope-bound and revoked when the permitted purpose expires. The retained export file carries its schema/profile version, record count, content digest and source watermark. Audit the export's purpose and requesting principal independently from its storage URL.
