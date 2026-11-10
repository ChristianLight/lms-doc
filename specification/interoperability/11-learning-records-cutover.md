# 11. Learning record exchange and institutional cutover

## 11.1 Profiles and evidence authority

| Profile | First implementation | Boundary |
| --- | --- | --- |
| xAPI 1.0.3 sender | Deliver explicitly mapped institutional events to an approved Learning Record Store (LRS). Pin version and test the recipient binding. | Sender support does not provide a general-purpose LRS. |
| xAPI 2.0 sender | Add a separate IEEE 9274.1.1 profile for destinations that support it. Pin version, schema, document concurrency and context capabilities. | Version negotiation does not convert a statement's meaning or enable unsupported fields. |
| cmi5 Quartz player | Launch assignable units (AUs) and consume the authorized profile statements through an xAPI 1.0.3 endpoint for the Quartz profile. Freeze the course structure, launch data and policy by registration. | Support a tested cmi5 and xAPI combination. Generic statement handling does not implement cmi5 launch or satisfaction. |
| Historical records transfer | Import restricted, approved identity crosswalks, progress, marks or attempt histories through their owning domains. | A content package and a learning telemetry stream do not establish formal historic grades. |

Formal grades, eligibility, completion and credentials originate in their owning domain. Learning statements, external results and archives can provide evidence. Each import or ingest path names its authority, coverage, trust class and policy revision. It must prove those claims before changing an authoritative record.

## 11.2 xAPI delivery and consumption

A sender creates an immutable LearningRecordDelivery from a committed native event and an approved profile map. Required fields are Institution, source event UUID, statement UUID, destination, version, map revision, payload digest, retry state, attempt count and created time. Optional fields are remote accepted time and an error class. Store full payload privately according to retention. Unique destination and statement UUID, and unique source event, destination and mapping revision. Index destination, next attempt and state. Restrict multiple emitted statements from one event by a stable mapping ordinal. Keep only the minimum delivery receipt and permitted subject alias after governed expiry.

Construct statement IDs before first send and keep them for retries. A deterministic ID may use an immutable source event, destination and mapping ordinal under a private namespace. Freeze the statement bytes or canonical decoded representation once created. An event correction emits a new statement or an authorized void under the selected profile. A successful void is a new statement referencing the prior statement, with the previous evidence still stored according to LRS semantics.

Bind every statement to a statement authority, protocol version, object type and correct typed fields.

| Field | Sender policy |
| --- | --- |
| actor | An Agent with exactly one permitted inverse functional identifier for the first profile. Default to a purpose-scoped pseudonymous account. Scope Groups and other actor forms through separate approved profiles. |
| verb | Profile-controlled IRI and optional localized display. Do not infer evidence meaning from localized labels. |
| object | Typed Activity, agent, statement reference or other allowed type according to the event profile. The first event maps normally use an absolute Activity IRI derived from an opaque placement ID. |
| result | Include success, completion, duration and score only when the mapping has evidence. Preserve raw, minimum, maximum and scaled semantics and reject malformed values. Exclude free-form answer text by default. |
| context | Include registration UUID only when it identifies a defined registration. Preserve approved relation types and extension IRIs. Never publish native role grants, accommodations or browser identifiers through free-form context. |
| timestamp, stored and authority | Use the verified native occurrence timestamp. The receiving LRS owns its storage time and authority validation. Do not use an untrusted reported timestamp to reorder native grades. |
| attachments | Disabled by default. A separate profile must check declared size, content type, digest, access, total payload and multipart rules. |

Use the profile's version header, request media type and authentication. For deterministic xAPI 1.0.3 delivery, submit to the statements endpoint with HTTP PUT and the statement UUID query parameter. A digest-matched remote record confirms a duplicate. Treat same ID with non-equivalent content as a conflict that requires review. A new ID generated after a timeout can duplicate evidence. Respect rate limits, pause on authentication or schema failures and retry network or transient server faults with capped jitter. Send in source order within the mapped aggregate where the contract needs order. Persist cursor and delivery state only after confirmed receipt. Source projections remain available through an LRS outage.

For an authorized inbound profile, authenticate the caller and normalize statements before applying any native effect. Validate version, statement identity, supported JSON and attachment shapes, full key semantics and size. Apply provider authority scopes before persisting or forwarding content. Repeated statement ID and equivalent content return the existing result. A conflicting statement ID enters an error queue and cannot replace evidence. Separate the LRS storage receipt from a projection update. Apply void authorization, statement-reference validation, and exclusion rules. Restrict raw statements, agent lookups, personal identifiers and free text to approved investigators. A portal's general analytics screen uses minimized aggregates.

For an xAPI document resource, scope state by Activity, Agent, registration where supplied, and state ID. Preserve key case and exact resource type. If the selected protocol requires entity tag checks, reject stale writes under that version rather than treating retries as unconditional replacement. Keep document changes separate from immutable statements. A deletion or cache expiry in the local analytics projection does not establish a protocol-level statement void.

**Fixture LR-A.** A completed lesson generates one source event and statement. The receiver stores the request then drops the HTTP response. Retry uses the same UUID and payload, producing one persisted statement and one successful delivery record. An attempted edit to that statement under the original UUID is quarantined. A report correction creates a second traceable evidence action without changing the first statement.

## 11.3 cmi5 package and launch contract

Import the selected Quartz course structure and validate it against a local XSD. Support standalone course XML and the declared ZIP profiles. A ZIP requires root `cmi5.xml`. Validate course, block and AU IDs, containment, localized titles, launch method, moveOn, mastery score and URL. An embedded AU uses a resolved package path. A remote AU needs a fully qualified permitted URL and separate review for rights, egress, access and execution isolation. Reject collisions with reserved launch query parameters. Preserve the publisher AU ID for provenance and assign a distinct platform activity IRI stable for that AU across launches in the registration. Prefer the same assigned IRI across registrations for the same immutable AU identity.

| Record | Persistence contract |
| --- | --- |
| Cmi5Registration | UUID, Institution, Enrollment, pinned EnrollmentRelease, exact ContentPlacement, ActivityVersion, package version, attempt ordinal, external registration UUID, immutable course structure digest and effective satisfaction policy revision. Unique Enrollment, placement, ActivityVersion and ordinal. The external UUID is unique within endpoint scope. Reusing an ActivityVersion at a second placement creates an independent registration. |
| Cmi5LaunchSession | UUID, registration, AU key and assigned IRI, launch mode, learner pseudonym reference, fetch nonce digest, token digest, generation, launch and expiry times, fetched time when redeemed, state and last evidence ordinal. Unique registration and generation, plus unique nonce. Index active registration and expiry. Retain state transitions with audit but expire grants and tokens. |
| AU satisfaction projection | Registration, AU key, evidence statement IDs, completed and passed flags, waiver state, status and revision. One projection per registration and AU. Recompute parent blocks from required children. Keep source evidence under the institutional retention policy and append correction decisions. |

1. A learner opens an available AU through an active Enrollment. Resolve or create the registration using the exact released placement before opening the AU session. Verify enrollment release, placement, immutable course version, permission and browser launch policy. Lock the registration. If it has an active launch, record the required abandonment event and revoke the prior session before creating the new generation. Never admit later statements for a closed generation.
2. Build `LMS.LaunchData` in xAPI State for the authorized activity, actor and registration. Include the required context template, launch mode and moveOn. The template carries the session ID extension and publisher ID grouping Activity. Include authored launch parameters, mastery score and entitlement key when specified, and an optional validated return URL. A mastery score is a decimal from zero through one with at most four decimal places. The AU may extend the template without replacing its fields and may not change the launch data document. Record the `launched` statement and the session context. Persist launch evidence before returning the launch URL.
3. Build the AU URL with URL-encoded `endpoint`, `fetch`, `actor`, `registration` and `activityId`. The actor is a minimal Agent with account, avoiding sensitive personal information. Launch in the selected OwnWindow or AnyWindow context. Set referrer policy to avoid disclosing launch capabilities and avoid token logging in every transit component.
4. The AU uses HTTP POST to redeem the fetch URL once. A valid request returns HTTP 200 and JSON. Success provides `auth-token`. A duplicate does not issue another token and returns the profile error structure. Make redemption atomic against session state and nonce. A response lost after redemption requires a fresh launch under the declared session policy. Issue a session-limited xAPI credential with access only to the intended actor, activity, registration and profile operations.
5. Require `initialized` as the first AU statement, once per session. Validate actor, object, registration, session ID extension, profile category and issuer for every defined verb. The AU may then emit applicable profile statements in Normal mode and ends with `terminated`. For Browse or Review, accept required initialization and termination and block other cmi5-defined AU statements. Keep broader xAPI statements separate from satisfaction.
6. Accept durable statement IDs idempotently. Validate completed and passed uniqueness for the AU and course registration, and their result semantics. For a passed or failed statement with applicable scaled score, check the configured mastery threshold and preserve the exact score. Successful retries may acknowledge an already accepted statement without advancing state. A new statement received after termination or abandonment fails. Close and revoke a timed-out session with the appropriate recorded evidence. Pending delivery and validity checks precede native completion projection.

The fetch and xAPI interfaces have separate authentication and privacy responsibilities. If the browser cannot reach the approved origin or start the required window, surface an accessible launch error and restart with a new session. Never copy the fetch credential into a query for later xAPI requests. Do not accept a claim from a content origin as evidence without the session credential and validated event.

## 11.4 MoveOn and cross-attempt evidence

For each AU and registration, keep flags for accepted Completed and Passed evidence across valid sessions. Keep Failed evidence separately. A failed attempt cannot satisfy a Passed requirement. Apply an institution-approved waiver only through an authorized actor and reason, retaining evidence independently of authored moveOn.

| moveOn | Rule before waiver |
| --- | --- |
| NotApplicable | Satisfied independently of Completed and Passed evidence |
| Completed | Accepted Completed |
| Passed | Accepted Passed |
| CompletedAndPassed | Accepted Completed and Accepted Passed |
| CompletedOrPassed | Accepted Completed or Accepted Passed |

Project block and course satisfaction by evaluating each required member and nested block. Emit one Satisfied statement for each newly satisfied block and one for the course. Use stable assigned block and course Activity IDs distinct from publisher IDs. Reuse the triggering AU session ID or generate a unique ID for satisfaction determined outside a launch. Use idempotent evidence IDs and avoid writing new native results for repeated close messages. Progress and satisfaction are separate from achievement score. A profile may map a verified source score to GradeEvidence only through a binding and institutional release policy.

For CMI-A, AU-1 has CompletedAndPassed and mastery 0.80. Normal launch 1 ends with Completed and Failed at 0.75. AU-1 remains unsatisfied. Normal launch 2 emits Passed at 0.85 and terminates. Existing Completed plus Passed now satisfies AU-1. AU-2 with NotApplicable is already satisfied. The parent block and course become satisfied once. A late score from launch 1 is rejected. A Browse launch emitting a new Passed at 0.95 cannot change satisfaction or grade evidence. A fresh registration starts without AU-1's prior completion.

## 11.5 Historical record transfer

Set a cutover policy per CourseOffering. Available choices are native fresh start, historical outcome snapshot, exact attempt replay after validation, and source teach-out. A source teach-out remains authoritative until its closure and can provide a later verified historic export. One serving authority owns each effective period, and switching authority requires approved cutover evidence. Separate learner-record TransferArtifacts from content artifacts and limit identity, response and grades to authorized migration operators.

| Source row | Minimum fields | Target and limits |
| --- | --- | --- |
| Identity crosswalk | Institution, source namespace and user key, verified canonical Person ID, verification method, reviewer and timestamp | ExternalIdentity or ExternalObjectMap. Ambiguous candidates require adjudication. Password, session and old global privilege records are excluded. |
| Enrollment or staff membership | Course and offering keys, person key, relationship type, effective dates and source state | Enrollment and scoped assignments through owners. Preserve source membership evidence and valid periods. |
| Progress or completion | Person and offering references, versioned placement where available, source status, occurrence time and source evidence | LearningProgress or CompletionRecord only with mapped semantics and placement. Aggregate progress may be a read-only historic record. |
| Grade snapshot | Person, offering, assessment or final-result reference, points and scale where known, source status, released time, version and source key | Historical GradeEvidence and GradeResultRevision through the records owner. Distinguish score zero, missing, exempt, withheld, failed and incomplete. No synthetic attempt rows. |
| Attempt replay evidence | Item versions and exact slot and option ordering, parameter values, response revisions, submitted time, scoring rules, provenance and original outcomes | Attempt, AttemptItem and imported scoring evidence only after the complete version and ordering proof. Use source result snapshot when evidence is incomplete. |
| Report and credential | Release period, exact original status and evidence or verification reference | Immutable historic report revision or external credential pointer. A native credential is a separately authorized act. |

Stage raw artifacts privately with a source cutoff and digest. Normalize source timestamps with their offset and explicit zone rules. Match by approved source identity and course offering keys. Validate every foreign key, permission and status mapping. Sum source and target counts by state, offering and source scope. Where grade scales are known, compare source and target independently computed totals, grading distributions and missing/exempt counts. Collect reviewer sign-off on the largest deviations and representative edge cases. Preserve evidence needed for student record challenges.

Reconcile and execute a write freeze on the old source or record the selected source as authoritative through the declared watermark. Capture the last ordered delta, seal evidence and compare its digest to the approved stage. Apply idempotent commands with durable run ledger and immutable source-key/revision mapping. Confirm the final cutover before taking native submissions. If apply partially fails, keep the new offering inaccessible and resume the recorded batch. A rollback before activation drops staged writes through owner APIs. Once learners have submitted after activation, move back only through an explicitly reconciled correction window. Never reopen both systems as simultaneous write authorities for the same records.

Historical screens separate anonymized preview, privileged crosswalk, reconciliation and final authorization. Provide accessible filters by offering, status and failure type, along with summarized totals that omit candidate responses. An import request binds source artifact, source namespace, cutoff timestamp, destination offering, policy revision, expected destination revision and idempotency key. A stale scope, grade rule or crosswalk requires reapproval. Incident recovery leaves import evidence accessible only under its existing role and retention policy.

For HIST-A, an approved source export contains 40 results. It has 31 numeric marks, including two genuine zeros, three exemptions, four missing grades and two withheld grades. Import creates 40 historical outcomes with corresponding states, 31 numeric points values and zero Attempt rows. A new gradebook learner view may show the two withheld rows only under the permitted release policy. A conflicting identity map blocks that person's records before cutover and cannot reassign the outcomes by email match.

- [ADL xAPI 1.0.3 release and specification files](https://github.com/adlnet/xAPI-Spec/releases/tag/1.0.3)
- [IEEE xAPI base standard documentation](https://opensource.ieee.org/xapi/xapi-base-standard-documentation)
- [cmi5 Quartz specification](https://github.com/AICC/cmi-5_Spec_Current/blob/quartz/cmi5_spec.md)
- [cmi5 course structure schema](https://w3id.org/xapi/profiles/cmi5/v1/CourseStructure.xsd)
