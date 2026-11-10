# 10. External tools and roster synchronization

## 10.1 Roles and persistent bindings

The first LTI profile is platform-side Core 1.3, with separately enabled Deep Linking 2.0, Assignment and Grade Services 2.0 (AGS) and Names and Role Provisioning Services 2.0 (NRPS). A content-provider profile in which this system acts as the external tool has a separate registration, security review and acceptance suite. Imported legacy links enter draft review. Registration is independent of any link or cartridge.

| Record | Fields and constraints |
| --- | --- |
| ExternalToolDeployment | UUID, Institution, platform issuer, tool client ID, deployment key, approved login initiation and redirect URI sets, tool JWKS location, allowed target and frame origins, enabled services and scopes, status, revision and credential rotation metadata. Unique platform issuer and deployment key. Index Institution and status. A deployment belongs to exactly one approved Institutional trust boundary. |
| ExternalToolResourceLink | UUID, deployment, CourseOffering, exact ActivityVersion and placement, external-facing resource link ID, target URI, approved custom parameters and revision. Unique deployment and resource link ID. Index offering and placement. Copying a placement into another offering creates a new link. |
| ExternalGradeBinding | UUID, deployment, owning context, resource link when attached, GradeItem, canonical AGS line item URL, maximum, resource ID and tag when supplied, version and grading policy reference. Unique canonical URL. Index context and deployment and grade item. Maximum changes require the records owner's authorized update. |
| ExternalToolLaunch | UUID, deployment, authenticated Principal and browser-session digest, resource link or exact writable CourseVersion draft and destination revision, optional placement, allowed Deep Linking content and media types, multiplicity, pinned return URI and independent response-correlation digest. Store target URI, hashed state and nonce, issue and expiry time, and separate OIDC challenge and Deep Linking response consumption. Unique one-use challenge and correlation. |
| RosterFeed | UUID, Institution, partner namespace, edition, interface role, enabled endpoints or import types, authority by object and field, authorized scope, state, revision, applied watermark and latest snapshot sequence. Unique Institution and namespace. Index active feeds and next poll time. |
| ExternalObjectMap | Institution, feed namespace, source object type and exact sourcedId, canonical identity and current source revision. Unique Institution, namespace, kind and sourcedId. Retain mappings and tombstones for reconciliation and late replay. |

Endpoint configuration excludes credentials embedded in URLs, fragments where disallowed and unapproved scheme or host changes. Require HTTPS except controlled isolated fixtures. Resolve tool JWKS through an approved egress route and pin to the registered URL. Enforce payload and rate limits, support controlled key rotation and quarantine newly untrusted signing keys. Resolve unknown key IDs using a bounded refresh of the configured JWKS. JWT header URLs never change trusted key locations.

## 10.2 LTI launch and Deep Linking

**Platform launch flow.**

1. An authenticated learner opens a released external ActivityVersion. Check current Enrollment, release, availability and local authorization against the precise placement. Determine deployment, context, scoped role claims, target link URI and opaque user identifier. Record a launch challenge and render the standard login initiation request to the registered tool.
2. The request includes issuer, login hint, target link URI and when configured client ID, deployment ID and message hint. Opaque hints carry no student names or claims and reference only short-lived server state.
3. The tool makes an OIDC authorization request. Verify issuer, client, login and message hints, configured redirect URI, message type, nonce, target binding and current application session. Require the request shape and response mode specified by the LTI security profile. Consume the launch challenge at signing. Duplicate authorizations cannot produce a fresh token for the same consumed challenge.
4. Produce a signed LTI ID token as a form POST to the registered redirect URI. Include OIDC issuer, audience, subject where required, issued and expiry times, nonce, LTI version, message type and deployment. Resource launch carries a resource link claim, roles and exact target link URI. Add context and enabled service claims only for the binding. Default identity disclosure is the pairwise subject and role set. Name and email are explicit scoped opt-ins. When anonymous launch is enabled, use the specification's anonymous pattern and disable learner-linked services.
5. The tool verifies its stored OIDC state and nonce, registered issuer, signature, audience and authorized party rules, timing, deployment, message type and matching target. The tool treats resource link IDs as deployment-scoped. Browser restrictions on third-party state may require a permitted top-level launch. A fallback restarts OIDC and never relaxes token or nonce validation.

Representative claim set for an authenticated learner follows. Values and timestamps are synthetic and signatures are omitted. The long URI keys are normative claim names.

```json
{
  "iss": "https://school.example",
  "aud": "tool-client-37",
  "sub": "h1H8Rk2Lq7m9",
  "iat": 1794307800,
  "exp": 1794308100,
  "nonce": "v37zl6gP4r1n",
  "https://purl.imsglobal.org/spec/lti/claim/deployment_id": "d-22",
  "https://purl.imsglobal.org/spec/lti/claim/version": "1.3.0",
  "https://purl.imsglobal.org/spec/lti/claim/message_type": "LtiResourceLinkRequest",
  "https://purl.imsglobal.org/spec/lti/claim/target_link_uri": "https://tool.example/activities/fractions",
  "https://purl.imsglobal.org/spec/lti/claim/resource_link": {"id": "r-184"},
  "https://purl.imsglobal.org/spec/lti/claim/roles": [
    "http://purl.imsglobal.org/vocab/lis/v2/membership#Learner"
  ]
}
```

**Authoring and selection.** An authorized editor launches `LtiDeepLinkingRequest` from a specific course draft. The platform stores a single-use correlation value, intended destination revision, accepted content types, media types and multiple-selection permission. It sends those constraints and `deep_link_return_url` in `deep_linking_settings`. A returned `LtiDeepLinkingResponse` is a signed form POST in the standard `JWT` field. Check tool issuer and registered client relationship, platform audience, deployment, dates, signature and echoed data when supplied. Match and consume the transaction. Validate every returned content item against the allowed types, destination, bounds and URL rules. An empty selection closes without creating activity. For nonempty valid selection show an accessible preview with title, type, origin, fallback and proposed grade effect. Confirmation compares the destination revision, creates inert draft links and moves no learner. If the draft changed since launch, review is repeated against the latest revision. A returned tool URL never grants the tool a deployment.

Tools authenticate server-to-server services with the registered LTI OAuth 2.0 client credentials and signed client assertion profile. Validate assertion issuer, subject, approved token endpoint audience, expiry, signature and unique token ID. Issue short-lived service credentials for the requested scopes intersected with registration and deployment policy. At each service call verify context, deployment and resource binding independently of possession of a scope.

## 10.3 Grades and membership services

**AGS contract.** Line items are GradeItem bindings, not arbitrary writes to grade tables. A tool can create, query, update or delete only the objects covered by its granted service scope, resource binding and policy. Map line item availability and optional resource ID and tag as typed values. A deleted external line item retires its binding. It does not delete GradeResultRevision or alter a released ReportCardRevision. Tools can read authorized results only within their scope and follow provided pagination links.

A score submission posts the standard media type `application/vnd.ims.lis.v1.score+json` to the line item's `/scores` endpoint. The request uses the subject from LTI identity binding, never an email. The following score is final at the provider.

```json
{
  "userId": "h1H8Rk2Lq7m9",
  "timestamp": "2026-11-10T08:52:11.325Z",
  "scoreGiven": 14,
  "scoreMaximum": 20,
  "activityProgress": "Completed",
  "gradingProgress": "FullyGraded"
}
```

The adapter verifies the line item, current deployment, context, Enrollment and immutable source correlation. Validate finite nonnegative score, required score maximum when a value is present, progress enumerations and ISO timestamp. A valid above-maximum AGS score is preserved as source evidence. A zero-denominator value is held for review under the native numeric policy because scaling is undefined. An omitted or null score signifies a clear of the previous tool result. It is distinct from zero and does not erase teacher overrides or historic evidence. Keep source activity progress separate from grading progress. By default, only `FullyGraded` contributes to grade evidence for publication. Pending, PendingManual and Failed remain visible to assessors as workflow states. The gradebook owner's release and conflict policies still apply.

Serialize updates per deployment, line item and user. Compare timestamp with latest accepted score. An older update cannot change authoritative state. An equal timestamp with the same canonical payload is an acknowledgement-only retry. Conflicting same-timestamp messages are retained as diagnostic evidence and rejected from grade mutation. Apply successful new source events and durable outbox writes atomically. Use canonical digest of the normalized score record for retries. Provider outages are retried with capped backoff outside browser sessions. Grade reads after a successful write may use the prior released result while new evidence awaits release.

The supplied 14 of 20 scales to 21 of 30 when that grade item uses 30 points. If the tool later reports 22 of 20, preserve the raw score and 1.1 ratio in the provider receipt. The calculated equivalent is 33 of 30. The owning grade-item policy determines whether to accept 33 as GradeEvidence, cap it, or hold it for adjudication. Never create GradeEvidence beyond the native policy range. A delayed 11 of 20 event with earlier timestamp changes neither result. A later clear produces a distinct source withdrawal which can be reviewed under existing grade policy.

**NRPS contract.** Expose membership for the authorized context and deployment only, with active status and role URIs permitted by policy. Default fields are scoped user ID, permitted roles and membership status. Include name, email or sourced identity only when the policy expressly authorizes it. Restrict filter parameters to authorized resource links and role types. Use stable pagination and scoped opaque cursors, require equivalent scope on every page and reject a cursor copied from another context. Never return institution-wide directory results when the caller holds course access. Soft-deactivated enrollment remains as audit and is disclosed only if membership policy and the binding allow it.

Staff UI separates deployment administration, placement configuration, privacy disclosures and grade reconciliation. Show provider connectivity and errors without token data. Learners see an accessible launch status and an approved retry option. Distinguish expired challenge, unbound target, denied scope, unknown context, stale destination and untrusted signing key. Grade reconciliation UI shows source timestamp, normalized points, pending state and release impact without exposing other contexts.

## 10.4 OneRoster CSV and REST roles

Begin with a 1.2 Consumer for Rostering and an authorized Gradebook exchange profile. Resource services and Provider roles have separate capabilities. CSV and REST are different bindings. The CSV 1.2.1 binding still expects `oneroster.version` value `1.2`. Manifest entries declare per-file mode `absent`, `bulk` or `delta`. Apply the standard data precedence rules if metadata hints disagree with row data, log a conformance issue and block promotion where the intended authoritative set cannot be proved. The transport may be an authenticated upload or approved managed exchange. Any download channel uses separate scoped service credentials. A 1.1 adapter, if implemented, cannot infer all 1.2 multiple-role information.

| Source record | Keys, links and policy |
| --- | --- |
| Academic sessions | Source key, type, title, start and end dates, optional parent and school year. Map to AcademicPeriod hierarchy, validate acyclicity and compatible child ranges. Preserve original date strings for re-export. |
| Organizations | Source key, type, name, parent and business identifier. Resolve Institution and OrganizationUnit only within approved tenant boundary. A new district source key cannot create a new tenant automatically. |
| Courses and classes | Preserve course source key separately from class key. Class references a course, school and one or more terms. Map to Course and CourseOffering with Section when an approved institutional policy groups class records into one offering. Preserve period and context links. |
| Users, roles and profiles | Map exact source keys to Person or require adjudication. Handle multiple scoped roles from the appropriate edition and files. External records cannot create host-wide administrative role grants. Demographics, metadata and agent or guardian relations are excluded unless separately approved. |
| Enrollments | Preserve source key, class, user, school, role, effective dates and primary flag when permitted. Map learner membership to Enrollment and authorized staff relationships to scoped assignments. More than one source reference to the same Person and offering still yields one Enrollment. |
| Categories, line items and results | Resolve class context, category, learner, ranges and score status using the Gradebook binding. Preserve exception flags, source scale and receipt time as evidence. Manual grade release still uses the records domain. |
| Resources | Preserve approved metadata and relationships. Importing catalog descriptions does not launch external tools or authorize asset fetching. |

Decode strict UTF-8 while accepting a BOM, and preserve exact header names and specification column order. Reject malformed quoting, disallowed carriage returns within fields, inconsistent field counts and invalid case in enums and identifiers. CSV quoting and embedded comma-list handling are separate parsing stages. Accept declared extension columns only after standard columns and use a registered allowlist. Downloaded operator diagnostics and CSV previews neutralize spreadsheet formulas. Standard exchange exports preserve valid protocol fields and should be opened as data.

## 10.5 Reconciliation, watermarks and proofs

1. Lock the RosterFeed configuration revision and capture the previous applied sequence. Stage manifest and normalized rows. Bulk rows have blank status and dateLastModified. Delta rows require the defined timestamp precision and `active` or `tobedeleted`. For absent files, stage no change.
2. Resolve references in dependency order while keeping raw source keys. Reuse existing scoped maps. Exact duplicate payloads are one input. Contradictory duplicate IDs block affected records. Do not match by email or display name unless the operator verifies identity against an approved authoritative identifier.
3. For REST, use scoped OAuth 2.0 and the enabled binding's pagination, media types and filters. Capture each page digest and snapshot boundary. If a provider lacks a snapshot token, use a recorded upper bound on change time where supported and overlap on the next poll. A partial page sequence may stage additions for review but cannot prove bulk absence. Retry read-only pagination at the previous boundary, with bounded jitter and Retry-After handling.
4. For an accepted complete bulk set, the authorized source scope is the reference set. Previous source-owned records absent from that complete set become retirement candidates. Apply them only after checking source authority, scope and completeness. Defaults are no destructive cascade and an operator hold when at least 20 records or over 5 percent of active scope are to be removed, whichever threshold is reached first. A valid tombstone closes the source grant or membership by effective policy. Preserve other authorities, grades and past audit.
5. For a delta, compare each object's provider modification time and canonical digest. An older update is quarantined as stale. Equal timestamp and digest is a retry. Equal timestamp with changed contents is a source conflict. A previously unknown tombstone records the source watermark to prevent a stale add. A newer source update may reactivate a tombstoned relationship under normal enrollment controls.
6. Apply via domain-owner commands with idempotency keys derived from feed, sequence and source key. Authorize removals separately from preview. Commit bounded batches and durable journal steps. Mark a feed sequence complete only when required journals are reconciled. Keep declared retry policy and set the high-watermark last. For competing jobs compare feed revision and sequence and reject stale apply.

Example ROSTER-A starts with 100 authoritative active memberships. A complete bulk file omits 8, so it creates 8 retirement candidates and pauses under the default percentage hold. An upload lacking the final page creates no absence candidates. In a later accepted delta, source enrollment E7 is tombstoned at `09:31:00.000Z` and a late active row from `09:30:59.000Z` is ignored. The original CourseOffering membership remains in audit, with prior GradeResultRevision history. A separately authorized native membership is unaffected.

An internal stage command requires the feed UUID, exact source artifact UUID, expected feed revision and declared snapshot sequence. Return a transfer job, status and issue cursor. Apply requires a stage digest, expected feed revision and source authority approval. Changed plans return `409 ROSTER_STAGE_CHANGED`. Malformed rows carry stable file and row locators with identity values masked. A dry-run screen shows proposed creations, conflict resolution, field authority and removals with keyboard-accessible filters. Explicitly verify overlapping authority, tombstone replay, clock ties, date boundary, credential rotation, learner data minimization and missing-page failures.

- [LTI Core 1.3](https://www.imsglobal.org/spec/lti/v1p3/)
- [1EdTech Security Framework](https://www.imsglobal.org/spec/security/v1p0/)
- [LTI Deep Linking 2.0](https://standards.1edtech.org/lti/specifications/launch_messages/deep_linking/lti-deep-linking-spec)
- [LTI Assignment and Grade Services 2.0](https://www.imsglobal.org/spec/lti-ags/v2p0/)
- [LTI Names and Role Provisioning Services 2.0](https://www.imsglobal.org/spec/lti-nrps/v2p0/)
- [OneRoster 1.2 models and REST bindings](https://standards.1edtech.org/oneroster/specifications/standards/v1p2)
- [OneRoster CSV Binding 1.2.1](https://www.imsglobal.org/spec/oneroster/v1p2/bind/csv/)
