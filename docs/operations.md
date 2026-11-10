# Security, accessibility, integrations, and operations

This chapter defines controls and release evidence for a learning platform that may hold student records, unpublished assessments, and official academic results. The institution sets deployment policies and names the owners responsible for them. Apply these controls to administrative, learner, API, bulk processing, and integration entry points.

## Authorization and trust boundaries

Authenticate through the institution's identity provider or host platform. Resolve the authenticated subject to an internal Principal. Use an immutable identity-provider subject plus issuer where external mapping is needed. Email and display name can change and are unsuitable as account keys. Disable access promptly when an account or assignment is revoked. Preserve attributable academic history according to policy.

| Actor | Decision scope and safeguards |
| --- | --- |
| Learner | Read published, currently available content and own permitted attempts and results within an active enrollment. Check review policy separately from submission and grading status. |
| Teacher or teaching assistant | Act within a current teaching assignment. Authoring, examining, grading, grade release, bulk export, and access to accommodations are separate permissions. An assigned grader can work within the assigned class or queue. |
| Reviewer or registrar | Review, moderate, release, or amend results within a delegated institution, program, term, or class. Require explicit permission and reason for official corrections. |
| Guardian or observer | Use a verified, time-bounded relationship and explicit institutional visibility policy. Limit access to the linked learner's allowed summaries. Apply role and policy changes when a learner's status changes. |
| Operator or support | Hold operational capabilities separately from access to academic records. Use individually attributed, time-limited emergency access with an approval or incident reference and alerting. |
| Integration or authoring agent | Use its own non-interactive principal and narrowly scoped credentials. An authoring agent can propose drafts and run validation. Publishing, grade release, enrollment changes, and access to learner records require separate grants. |

- Authorize each operation against the resource and scope on the server. Resolve its institution, offering, enrollment, and visibility from trusted records. Enforce the same rules for search, counts, caching, exports, attachments, and queued work. Treat a globally unique identifier as a locator.
- Check access again when issuing signed downloads or collecting export results, and before a delayed human-initiated job publishes its side effects. Record who requested and performed the job. Scope cache keys by institution and the access decision where applicable. Prevent shared caches from serving personalized responses.
- Configure strong authentication for privileged users, session expiry and revocation, protection against cross-site request forgery, parameterized storage access, safe rendering, and abuse limits. Apply rate limits by operation so that a burst of valid exam submissions can proceed.
- Keep answer keys, unreleased feedback, staff notes, accommodation details, and credential secrets out of learner APIs, assets, analytics, logs, and client bundles. Use separate projections where the same record has different audiences.
- Use distinct trust boundaries for authored text, uploaded files, standards packages, external tools, and graders. Sanitize rendered markup and disallow active content in native lessons. Treat executable package content as a separate runtime capability. Grant it only the learner's authorized launch context and runtime operations. Require containment and browser compatibility tests before enabling execution. Keep graders away from identity stores, secrets, and external networks by default.
- Quarantine external files before import or serving. Limit archive entry count, expansion, recursion, and total bytes. Reject absolute paths, traversal, ambiguous paths, and symlinks. Disable external XML entity processing. Validate file content, scan according to institutional policy, and deliver untrusted attachments from a controlled origin with safe download headers.
- Validate external destinations. Restrict callback, media, and fetch hosts as appropriate and block unintended internal network access. Check the resolved endpoint and redirects where remote fetching is allowed. Rotate and revoke connector credentials, and restrict service accounts by scope and operation.

Use [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) to select and verify security controls. For specific controls consult the OWASP guides on [authorization](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html), [file upload](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html), [server-side request forgery](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html), and [logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).

## Student privacy and records

Keep an inventory of the data required for identity, instruction, assessment, accessibility, operations, and institutional reporting. Assign each record class an owner, purpose, authorized audiences, retention rule, export policy, and permitted processors. A deployment serving minors must settle age-related access, guardian authority, safeguarding reporting, and communications policy. Keep accommodation evidence separately protected and give proctors and teachers only the approved exam adjustment and information needed for their duties.

Verify the institution's governing law, contracts, record schedules, regulatory duties, data residency and transfer requirements, and breach response before enrolling real learners. Applicability can differ by jurisdiction, institutional status, student age, and type of processing. Examples of regimes that may need review include [FERPA in the United States](https://studentprivacy.ed.gov/faq/which-educational-agencies-or-institutions-does-ferpa-apply) and the [EU General Data Protection Regulation](https://eur-lex.europa.eu/eli/reg/2016/679/oj). Record the actual policy for each deployment.

| Entity | Minimum data and rules |
| --- | --- |
| `RetentionPolicy` | Institution, record class, event that starts the clock, retention period, disposition, effective dates, version, and policy owner. Distinguish submissions, academic records, assessment telemetry, audit records, messages, backups, and integration exports. |
| `LegalHold` | Authorized case, record selector or affected references, start, approval, status, and release. A hold blocks automated destruction for records in scope. |
| `PrivacyRequest` | Request type, verified requester, subject, scope, applicable deadline, disposition, restricted evidence reference, and completion record. Support access, correction, restriction, and eligible disposal or export according to local policy. |
| `AuditEvent` | Unique event ID, UTC time, institution and resource scope, actor and acting authority, action, target reference and version, result, reason code, correlation ID, and restricted evidence reference where needed. |

- Treat retention and account revocation separately. Protect official records through the applicable retention period. Where disposal is allowed, cover derived stores, file replicas, exports in system custody, and external processors. Document backup expiry and reapply valid deletions and suspensions after a restore before reopening access.
- Scope exports to the requester, data subject, and purpose. Exclude information about other learners where applicable. Authorize export creation and collection separately. Expire downloads and avoid placing academic or sensitive data in email or chat notifications.
- Default analytics to the minimum necessary data and separate pseudonymous learning events from identified reporting views. Restrict raw event access. Suppress small-group results where the institution's disclosure policy requires it. Treat a pseudonym as personal data when it can be linked back to a learner.
- Give authoring agents synthetic or approved instructional data. Store source, rights, model or tool version, and review outcome for agent-generated drafts. Send student work or identifying data to an external service only under approved policy with explicit scope and traceable purpose. Establish an accessible alternative and approval policy before using any proctoring service that collects intrusive data.

## Audit and operational evidence

Keep an append-only academic audit trail protected by dedicated permissions and disposition policy. Capture access to restricted records, scoped role changes, impersonation and emergency access, content publication, exam accommodation changes, accepted submissions, overrides, moderation, regrades, grade and report release or correction, exports, and integration disclosure. Keep high-volume operational telemetry separate. Capture score changes through academic record versions and link audit evidence to them. Exclude credentials, session tokens, answer keys, complete responses, and sensitive notes from general logs.

Commit the authoritative academic change with its audit or durable event record. Preserve the original actor and reason when delivery is retried. Where external disclosure follows, record delivery and failure as separate events. Detect gaps or tampering, control access to the audit store, monitor the logging pipeline, and apply policy-defined retention. Include integration configuration, deployed schema and evaluator versions, and relevant correlation IDs in incident reviews.

## Accessibility and inclusion

Target [WCAG 2.2 Level AA](https://www.w3.org/TR/WCAG22/) for learner, teacher, and administrative workflows. Use [ATAG 2.0](https://www.w3.org/TR/ATAG20/) as guidance for both accessible authoring and helping authors create accessible material. Record an accessibility status for content assets and imported activities, and provide an equivalent accessible path for required work when a package or embedded tool creates a barrier.

| Surface | Required behavior and verification |
| --- | --- |
| Authentication and navigation | Complete sign-in, navigation, and confirmation by keyboard and with assistive technology. Verify landmarks, headings, focus order and visibility, zoom and reflow, target sizes, labels, and accessible error recovery. |
| Authoring and learning content | Preserve semantic headings, lists, tables, and meaningful link text. Prompt for text alternatives and captions, flag structural issues, and distinguish automated warnings from reviewed content. Preview on phone, with keyboard, and in relevant right-to-left or translated layouts. |
| Math and interactive items | Use structured notation, such as MathML, with a tested screen-reader path and an accessible way to enter and review expressions. Provide a keyboard path for matching, ordering, and diagram interactions with equivalent scoring. Verify real learner input and feedback on supported assistive-technology combinations. |
| Video and audio | Support keyboard-accessible controls, captions and audio descriptions where required, and transcripts or equivalent material as appropriate. Provide a low-bandwidth route for required content. |
| Timed assessment | Show the deadline, save status, retry state, and submission result in accessible status messages. Apply approved accommodations when setting server time limits. Test navigation, timeout recovery, and equivalent interaction under the actual assessment timing policy. |
| Reports | Offer an accessible on-screen result view. Verify downloadable formats separately when they serve as required records or communications. |

Run automated checks on every relevant release. Before rollout, manually test complete workflows with keyboard, screen reader, and mobile device, and include representative institution content. Track defects with the affected workflow and accommodation. Do not rely on a single scan or component test to assess a complete course or exam.

## Integration contracts and data ownership

Keep local course delivery, exam submissions, grading, completion, and official academic records available when optional external systems are unavailable. Integrate providers through documented, replaceable boundaries.

| Boundary | Ownership and failure behavior |
| --- | --- |
| Identity provider | The provider authenticates. The LMS owns its Principal reference, contextual authorization, and academic records. Use the provider's immutable subject. Reconciliation handles account changes and duplicate or unmatched identities without silently merging learners. |
| Student information system | Configure an authority matrix for identity attributes, term, classes, enrollment, and grade export. Preview roster changes, validate class scope, process effective dates, reconcile removals, and queue disputed mappings. Evaluate [OneRoster 1.2](https://www.imsglobal.org/spec/oneroster/v1p2) for school roster and result exchange. |
| Collaboration provider | The provider owns room and message storage, presence, and moderation tools. The LMS owns academic enrollment and desired room membership. Create rooms from the agreed offering or class scope. Reconcile removal and role changes, and keep rosters separate between classes. Messaging and calls can degrade independently of lessons and assessments. |
| Document or media provider | The LMS owns attachment references, visibility, and links to the relevant published revision. The provider owns managed file versions, scanning or streaming according to the contract. Preserve the version required for the course or submission and recheck access at retrieval. Report missing content and expiry without quietly substituting another version. |
| External learning tool | Register per institution and grant the least necessary launch and service scope. Evaluate [LTI 1.3 and LTI Advantage](https://www.1edtech.org/standards/lti) for tool launches, roster access, content selection, and grade return where needed. Authorize each grade return against the declared activity, enrollment, and registration. The LMS retains official grade release and correction authority. |
| Notification provider | The LMS decides who receives a message and why. External services deliver a minimal payload, track bounce or failure, and respect opt-out where applicable. The LMS displays authoritative changes even when delivery fails. |
| Authoring or scoring service | The LMS grants narrowly scoped requests and owns the resulting draft or marking decision. Version and validate responses. Use deterministic rules or authorized human review for official marks, with errors routed to review rather than represented as zero. |

| Entity | Minimum data and rules |
| --- | --- |
| `IntegrationConnection` | Institution, provider and API profile, enabled operations, credential reference, authority policy, configuration version, and lifecycle status. Scope every inbound and outbound operation to one connection. |
| `ExternalIdentity` | Connection, provider subject, internal Principal, verification and status. A verified provider subject maps to at most one Principal within the connection. Keep historical changes traceable. |
| `ExternalResourceMap` | Connection, local resource type and ID, external type and ID, state and last reconciled version. This mapping tracks live synchronization. Imported source provenance belongs to the interoperability mapping. |
| `OutboxEvent` | Event ID, institution and aggregate, aggregate version, event type, schema version, occurrence time, causal and correlation IDs, and minimal payload or protected record reference. Persist with the authoritative mutation before asynchronous delivery. |
| `InboxReceipt` | Connection, message ID, payload hash, received time, processing state, outcome, and handled time. Enforce uniqueness for the connection and message ID. |
| `SyncRun` | Connection, direction, mode, starting and committed cursor, checkpoint, item counts, redacted issues, and result. Support dry run, resumable full reconciliation, incremental runs, and operator-reviewed repair. |
| `NotificationDelivery` | Logical notification, recipient, channel, template version, deduplication key, provider reference, delivery status, and last attempt. Preserve user-facing notification state separately from transport delivery. |

Define an API contract with authentication, permissions, schema versions, pagination and cursors, documented failure modes, and replay rules. Support an idempotency key on retryable writes and reject reuse with a conflicting payload. Sign and verify webhook delivery where used, check replay windows, and deduplicate incoming events before applying changes. Use resource versions to reject stale writes. Define order where it matters per aggregate or connection. Report throttling and transient failures, retry with bounded backoff, and give operators a safe way to reconcile repeated failures. Treat absence in a partial provider response separately from an explicit deletion or removal. Provider failure must never silently turn an assessment into a failed mark or an entire class into withdrawn enrollments.

## Reliability, scale, and recovery

- Start with clear write ownership for each record and strong consistency for submission acceptance, attempt limits, grade release, and official reports. Keep read models for progress dashboards and analytics rebuildable. Display their freshness where delays matter.
- Persist accepted submissions before confirming them. Preserve the client idempotency key, server time, and receipt, and return the same receipt on a valid retry. A client distinguishes local draft, saved response, and accepted submission. Handle competing updates from multiple tabs explicitly and use server time for exam policy. Test mobile interruption, time-zone and daylight-saving transitions, and an outage at the deadline.
- Queue imports, external synchronization, media processing, bulk reports, and large regrades. Reserve processing capacity for time-sensitive work such as exam marking. Give jobs lease expiry, checkpoints where applicable, bounded retries, and a terminal error state. Make result application idempotent. Pause or throttle by institution or job class during demand spikes.
- Index the primary institution, offering, enrollment, assessment, and status access patterns. Paginate large lists, isolate bulk export work, and store large assets independently of transactional records with controlled access. Use versioned content caches and keep sensitive outputs out of shared caches.
- Establish load profiles for a small school, simultaneous institutional exams, and sustained large enrollments. Set actual traffic assumptions and numerical objectives with the deployment owner. Test peak concurrent starts, autosaves, and submissions, marking backlog, roster reconciliation, import size and asset delivery, and report production. Include a slow or disconnected network profile and provider failures. Measure p95 latency, sustained throughput, duplicate or lost writes, queue age, and recovery time.
- Define service objectives, recovery point objective, and recovery time objective per capability. Maintain protected backups of authoritative records, assets, audit data, and recovery configuration. Verify a consistent restore across files and academic records, check referential integrity, and reconcile external state. Exercise disaster recovery and failover before relying on them in exam periods. Use the [NIST contingency planning guide](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) for planning guidance.
- Monitor authorization failures, enrollment and grade sync lag, submit receipt rates, marking latency, unexpected grade changes, and import failures. Use alerts with accountable owners and runbooks for incident containment, degraded operation, reopening access, and notifying affected institutions. Rehearse database upgrades and backfills using representative anonymized or synthetic data. Define rollback or forward-recovery steps for schema and package changes before deployment.

## Cross-cutting release gates

| Gate | Evidence required |
| --- | --- |
| Authorization | Automated tests deny cross-institution, cross-class, and cross-learner access using valid IDs. Exercise the UI, API, search, export, downloads, asynchronous jobs, and provider callbacks. Verify revocation and unpublished content behavior. |
| Secure intake and runtime | Exercise archive traversal, duplicate paths, decompression limits, malicious markup, external XML entities, unsafe outbound URLs, and forged callbacks. Verify isolated content and grading runtimes cannot reach host credentials or other users' data. |
| Accessibility | Complete sign-in, authoring, a structured math question, a timed accommodated exam, feedback review, and report retrieval with representative assistive technology. Verify imported content as part of the course workflow. |
| Academic durability | Reproduce double submission, concurrent edits, delayed or repeated marking, provider loss, and a restore with an exam underway. Confirm accepted work is traceable to the right enrollment and revision, academic totals agree, and every correction is attributable. |
| Privacy and integration | Run a scoped data request, approved disposal and hold tests, a role removal, a roster diff, provider outage and recovery, and signed webhook replay. Verify monitoring and exports follow their allowed purposes and visibility rules. |
| Operations | Record the deployment's load envelope, release checks, recovery objectives, last successful restore, support owners, and safe handling for failed jobs. Measure outcomes under the agreed workload before expanding the rollout. |
