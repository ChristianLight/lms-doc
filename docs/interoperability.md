# Interoperability and curriculum migration

A package adapter translates an external representation into the canonical learning model or registers it for isolated playback. Native authoring, package playback, assessment exchange, tool launch, roster exchange and historical records have separate acceptance criteria.

## Format profiles and scope

| Profile | Payload and use | Required behavior and boundary |
| --- | --- | --- |
| Native curriculum archive | Versioned manifest, content and question definitions, media, reusable libraries and relationships | Round-trip the supported authorable curriculum. Preserve versions, dependency provenance, hierarchy, order, references, locales and assets. Keep records and answer keys under separate export permissions. |
| OLX course archive | Gzip-compressed tar archive containing course hierarchy, XML components, HTML, policies and assets | Convert supported content and assessment rules into editable native drafts. Inspect packages and dependencies independently. |
| Legacy OLX library archive | Gzip-compressed tar archive with a library descriptor and XML content | Import reusable components, collections when present or explicitly mapped, and source keys. Resolve course references using source identifiers and evidence of the correct revision. |
| Versioned library archive | ZIP with `package.toml`, entity and collection TOML, component XML, and versioned assets | Support format version 1 through its own adapter when found in the inventory. Preserve the current draft and published snapshots when present. Report history absent from the archive. |
| SCORM 1.2 | ZIP content package with an `imsmanifest.xml` and a browser runtime contract | Play conforming package activities and capture learner state. Publish the tested package, runtime, and browser support matrix. |
| SCORM 2004 | ZIP content package with edition-specific runtime and sequencing and navigation | Scope the runtime and sequencing independently. Verify the editions and behaviors used by real packages. Claim full conformance for an edition only after the required tests pass. |
| 1EdTech QTI | Assessments, items, resources, response-processing definitions and separately scoped results data | Use a declared version and interaction and processing profile. Prioritize versions represented in partner exchanges. Validate math, accessibility, and scoring semantics. |
| 1EdTech Common Cartridge | Portable curriculum outline, resources and optionally external tool or assessment references | Treat every cartridge version and supported resource type as a separate profile. Record every dropped or unresolved resource. |
| 1EdTech LTI 1.3 and Advantage | Signed external tool launch with separately authorized services | Implement as a tool boundary. Scope deployments, audiences, role claims and access tokens. Deep Linking adds resources, AGS exchanges permitted grade results, and NRPS exposes permitted names and roles. |
| 1EdTech OneRoster 1.2 | Rostering, gradebook or resource exchange over CSV or REST | Map external schools, classes, terms, users and enrollments by stable identifiers. Enable only approved services and export fields. Retain authority and deletion semantics of the source. |

A learning record interface, such as xAPI or cmi5, is a separate future profile. Telemetry may support analysis and reconciliation. Formal grades and enrollment states originate from authorized transactions in their owning modules.

## Canonical transfer records

| Record | Required data and relationships |
| --- | --- |
| `TransferArtifact` | Owning Institution, authorized uploader or exporter, source digest, byte length, detected format, schema or edition, original filename, restricted storage reference, rights metadata and retention class. Equivalent bytes can share storage within the applicable trust boundary. |
| `TransferJob` | Institution, artifact or export selection, adapter version, source namespace, destination scope, manifest version, mode, lifecycle state, idempotency key, operator, timestamps and checkpoints. |
| `TransferRecord` | Job, source object kind and scoped key, parent key, source revision and fingerprint, relationship or asset dependencies, target kind and identity, target revision, disposition and reviewer decision. |
| `TransferIssue` | Job and source locator, severity, machine-readable reason, sanitized explanation, affected dependants, owner, resolution state, evidence and review record. |
| `ExternalObjectMap` | Institution, source namespace, source scope, object kind and original source key uniquely identify the mapped canonical object. Preserve the original key string and its case. Keep source version and canonical version in revision-level mapping records. |
| `ExternalToolDeployment` | Institution, registered tool and issuer, client and deployment IDs, key metadata, allowed origins and service scopes. A resource link binds an ActivityVersion to this deployment and its external resource ID. |
| `PackageVersion` | Artifact digest, format edition, parsed manifest and launch profile. One or more package activities map the manifest's organization and item occurrences to launchable resources. A shared resource can have multiple distinct activity occurrences. |
| `PackageRegistration` | Enrollment, ContentPlacement, assigned ActivityVersion and PackageVersion, attempt number, status, state revision and time totals. It owns per-occurrence SCO state, objectives, interactions and launch-session records. |

Generate or allocate stable globally unique IDs for canonical objects. A course key from one installation can recur in a separate installation. A component key can recur in another course, an edition of a library or a different object type. The mapping namespace and scope distinguish them. Treat slugs and paths as locators. Asset deduplication by content digest does not merge authorship, rights, logical paths or visibility. The same item used in two placements retains separate activity context and scores where required.

A transfer may preserve an incoming ID when namespace, object ownership and trust policy permit. Otherwise retain it as provenance and assign a canonical ID. On repeat import, match the mapping and compare both the previous imported fingerprint and the current target revision. Unchanged inputs replay safely. Upstream changes produce proposed revisions. Local changes require an explicit merge or fork decision. Absence from a later content export produces a reviewable retirement candidate. Full authoritative roster snapshots and explicit incremental tombstones have separate deletion policies.

## Import and publication workflow

1. **Inventory.** Identify the source installation and releases, archive type and metadata, content owner and applicable rights. Record counts and dependency types across courses, libraries, assets, problems and independently hosted media. Accept separate authorized sources for rosters and historical records.
2. **Quarantine.** Stream the archive to private storage, calculate its digest and apply quotas before and during decompression. Parse with network resolution and external entities disabled. Verify expansion ratio, entry count, total bytes, depth, content types and duplicate or case-colliding paths. Reject unsafe paths, encoded traversal, symlinks, hard links, device files and unknown executable import hooks. Enforce nested archive limits. Perform resource-intensive validation in a bounded worker.
3. **Parse and inventory.** Detect structure by manifest, signature and schema. Preserve original locators and per-record checksums. Enumerate recognized entries, unsupported extensions, missing dependencies, invalid links, malformed scoring rules and remote resources. Native content rendering uses a separate sanitization policy for HTML, CSS, SVG, MathML and media.
4. **Resolve.** Allocate or reuse canonical identifiers before rewriting references. Build an ordered content graph and asset path map. Resolve libraries, reused item versions, internal links, prerequisites, cross-course references, resources and rubric bindings against a staging graph. Detect cycles where the relation requires a directed acyclic graph. Preserve deliberately external links and classify unexpected old-host references for review. Never retrieve remote URLs during parsing. Optional media retrieval has its own explicit authorization and bounded fetch policy.
5. **Transform and compare.** Produce a proposed editable draft, a packaged activity, a reviewable approximation or an unresolved record. Separate package defaults from site and offering policy. Display what learners would see, how the grade would be computed and how this import differs from the current revision.
6. **Approve and promote.** Obtain sign-off from authorized content and assessment reviewers for losses affecting access, accessibility, scoring or progression. Apply staged drafts as an atomic graph revision or keep them private until all staged references are valid. Publishing is an independently authorized transition. Released CourseVersions and active attempts remain pinned to their assigned versions.
7. **Verify and reconcile.** Re-run the import to demonstrate idempotency. Reconcile totals and references with the source inventory. Export a machine-readable issue list and a reviewer summary by course and library. Retain original bytes and validation evidence according to institutional retention policy.

Track job states such as received, quarantined, validated, staged, awaiting review, applied, cancelled and failed. Jobs use resumable checkpoints, idempotent writes and a durable audit history. Redact keys, credentials, student identifiers and private URLs from ordinary logs. Rollback before publication discards private staging. A post-publication correction issues a new revision or retires a release according to policy and preserves historical assignments and attempts.

## Curriculum mapping

| Source object or behavior | Canonical target and migration checks |
| --- | --- |
| Course root and ordered curriculum containers | Course, CourseVersion and ordered ContentPlacement records pointing to ContentNodeVersions. Keep a separate CourseOffering for each delivery. Explicitly preserve gates, self-paced or scheduled settings, navigational visibility and assessment boundaries. |
| Editable page, text, image, captioned video or attachment | Versioned ContentNode or Activity, typed accessible blocks, AssetVersion or approved external media reference. Rewrite package-local links with full path context. Verify captions, transcripts, variants, font and image licensing, old host references, provider rights and authorization. |
| Internal unit link, static path, policy and static page | Resolve links by source keys before publishing. Track references to prerequisites and linked objects separately from page HTML. Keep policy JSON or equivalent as structured candidate settings with explicit mapping for dates, time zone, weights, drop rules and access. |
| Question with one or more response controls | Versioned assessment item with one or more interactions, score rule, expected response, hint, explanation, feedback policy, point allocation, partial-credit conditions and accessibility labels. Map only after comparing reference responses and scoring edge cases. |
| Numeric and mathematical expression responses | Typed numeric or math evaluators with explicit tolerance, domain, variables, accepted expressions, constants, unit rules, precision, rounding and undefined-value behavior. Report assumptions or unsupported functions. Test mathematically equivalent responses and representative wrong responses with source-side evidence. |
| Bank selection and parameter randomization | Library entries and versioned pool definition with draw count, eligible members or versioned filter, replacement rules and randomization moment. Freeze selected items, parameter values and seed per target attempt when created. Distinguish selection among items, randomization within an item and choice order. Report whether previous per-learner draws and parameter values are recoverable. |
| Library link, copy or override | Preserve provenance, source library and item key, and known source revision. Bind released content to an explicit target version. Keep local overrides and diff them against upstream updates. Treat unresolved links as missing dependencies even when a usable preview or snapshot exists. |
| Assignment, rubric or external grader | Preserve prompts, rubrics, criteria, max marks, settings and feedback evidence. Rebuild unsupported peer workflows or grading integrations as separate native activities or use a configured, authorized external tool. |
| Custom scripts and extension blocks | Preserve bytes and metadata privately, record dependencies, and choose declarative conversion, manual redesign, approved integration or isolated legacy playback. Block affected graded activities from release until assessed for behavior. |
| Actual SCORM package | Register verified package bytes and manifest independently, then attach a PackageVersion to an ActivityVersion. A descriptor alone generates a missing-package issue. Retrieve original package bytes, or use the bundled copy when verified. Preserve the original separately if exact source bytes are required. |

Typical OLX signatures include `course.xml` with chapter, sequential, vertical and component references, type-specific XML directories, optional companion HTML, `static/`, `policies/<run>/` and sometimes `drafts/`. The adapter must validate the hierarchy rather than guess order from filenames. Handle recognized variants by release profile and retain XML elements or attributes with unresolved meaning. Legacy library archives may include `library.xml` and per-type XML. A versioned library ZIP keeps asset paths local to each component version, so the same relative asset name can resolve to different files in one archive.

Classify every source record as native equivalent, mapped with explicit differences, intact packaged activity, externally resolved, or blocked. Static HTML may render while its embedded interactive script, graphing tool, fonts or video service remains unavailable. A plain text representation of an unsupported equation is a review artifact. Unsupported grading, incorrect feedback, empty question pools, absent assets required for assessment and unresolved prerequisites are publication blockers. Preserve both detected and operator-approved coverage counts.

### Historical data migration

Treat curriculum, operations and student evidence as separate transfer projects with independent permissions, retention, and audit. Historical feeds can include identity aliases, offering rosters, enrollments, section and group assignments, progress, attempts, response versions, marks, overrides, released report cards and credential references. Obtain each from an authorized report or API, or from an approved read-only source extraction when the records are unavailable through public exports.

Create a crosswalk using trusted identity-system identifiers and source-side keys. Names and emails can aid review, with ambiguous matches queued for a human decision. Never import password hashes, session tokens or former access grants through curriculum archives. Maintain an archive of original evidence under restricted access and imported timestamps, currencies, formats, scoring scale and status values where relevant. Use explicit policy for incomplete, exempt, missing, withheld and failed results. Imported summary grades can be published as historical snapshots with provenance. They must not generate fictitious underlying attempts.

Decide which offerings are rebuilt with new learner starts, which may resume in a compatible schema, and which finish on the source platform. Attempt replay requires response, assignment, grading, revision, and randomization evidence. Aggregate grades alone only support historical result import. Reconcile counts, independent grade distributions, sample marks, completion states and identity mappings per offering. Plan an agreed write freeze, authorized final delta and rollback window. Record the cutover boundary so changes and activity are captured in one system of record for each cohort.

## SCORM package and runtime design

### Packaging and launch

- Validate the root `imsmanifest.xml`, declared profile, organizations, items, resource pointers, dependency references, namespaces, resource types and launch paths. Parse one or more organizations, preserve default organization and distinguish launchable assets from SCOs that use the runtime API. Register every item occurrence and relationship separately. Resource entry points are relative to the immutable package root. Record unsupported sequencing or resources before launch.
- Derive the launch grant from the authenticated learner's Enrollment, assigned ActivityVersion, PackageVersion, attempt and activity occurrence. Grant minimal claims for a short lifetime, validate release and assignment before every start, and keep package bytes outside native authoring and privileged file systems.
- Run imported JavaScript on an isolated content origin with a compatible launcher frame. Legacy packages discover a same-origin parent or opener API. Give them that API through a launcher that shares the permitted package context and has no application cookies, privileged endpoints, or grade credentials. The authenticated application and the launcher communicate through a narrowly typed bridge that validates origin, window source, session nonce, payload and occurrence. Use isolated storage namespaces or origins across trust boundaries and validate CSP, popup and top-navigation policies. Untrusted content can reach only the browser capabilities granted by the profile.
- Preserve exact relative asset paths, query strings and fragment semantics subject to path validation. Restrict network and external navigation by default, then review compatibility exceptions for authorized origins. Supply only the learner identity data the declared runtime requires. Log attempts to escape a permitted path without logging student response values.

### Runtime contract and scoring

| Behavior | SCORM 1.2 | SCORM 2004 |
| --- | --- | --- |
| API discovery object | `API` | `API_1484_11` |
| Lifecycle | `LMSInitialize`, `LMSCommit`, `LMSFinish` | `Initialize`, `Commit`, `Terminate` |
| Data and diagnostics | `LMSGetValue`, `LMSSetValue`, `LMSGetLastError`, `LMSGetErrorString`, `LMSGetDiagnostic` | `GetValue`, `SetValue`, `GetLastError`, `GetErrorString`, `GetDiagnostic` |
| Progress and status | Interpret `cmi.core.lesson_status` under the declared policy and retain the raw value. Support edition-defined entry, exit and timing semantics. | Keep `cmi.completion_status` and `cmi.success_status` separate. Preserve progress measure and edition-specific entry, exit and time values. |
| Score | `cmi.core.score.raw`, min and max where supplied | `cmi.score.raw`, min, max and scaled values where supplied |
| Bookmark and suspend data | `cmi.core.lesson_location` and `cmi.suspend_data` | `cmi.location` and `cmi.suspend_data` |
| Multi-activity progression | Profile-specific launch and LMS navigation plus any supported 1.2 manifest constraints | Use the declared edition's navigation requests, attempt tracking, objectives, sequencing rules and rollup when in scope. |

Use the edition's data element names, value types, constraints, index semantics, read/write permissions and error codes. Implement synchronous browser API behavior and specify the persistence guarantee behind successful commits. Persist accepted state before success is represented as durable and provide a recovery path for interrupted sessions. Do not rely on page unload as the sole save path. Use monotonic sequence and durable idempotency keys so repeated sends or stale tabs cannot double-count time or overwrite newer state. Keep session lifecycle, per-SCO data, score history and learner-facing progress separately. Resume restores the correct SCO occurrence, bookmark and suspend data under its registration. New attempts start from their own registered state.

Map raw statuses, score values and timestamps to accepted completion evidence and GradeEvidence through a versioned adapter policy. Delivery updates LearningProgress and Academic Records calculates any GradeResultRevision. Keep the original values and preserve distinctions among incomplete, failed, passed, complete and unknown when the edition permits. Handle valid zero, absent min or max, repeated commits, and scores outside the gradebook scale explicitly. Store interactions under their proper permissions. Gradebook aggregation follows declared attempt and source precedence, points and release policies. SCO-originated results are package-reported evidence. Assessment policy decides whether that evidence meets the assurance required for a consequential exam.

### Conformance and compatibility

Record the standard and edition, the package profile, runtime coverage, multi-SCO sequencing scope, browser matrix, test suite version, and package fixtures. Exercise reference and real packages for API discovery, return values and last-error behavior, init/commit/terminate ordering, suspend/resume, retry/reset, multiple organizations, multiple SCO occurrences, asset dependencies, objectives/interactions, grade and completion rollup, interrupted network, concurrent tabs and package version isolation. Verify 2004 branching, navigation requests and rule/rollup handling where claimed. Report precisely which behaviors passed. A package with a missing or unsupported feature enters an actionable review state.

SCORM playback does not imply package authoring or SCORM export. If SCORM generation is commissioned, define a distinct feature with an explicit portable rendering subset, SCO boundaries, generated runtime calls, package version, and independent target-player conformance tests. Keep native editorial exchange and standards-based item exchange available for users who need editable content and question logic.

## Export and interoperability verification

The native curriculum format must publish its manifest schema, required and optional fields, version policy, stable IDs, typed references, canonical serialization rules and asset digests. Unknown mandatory capabilities fail validation and unknown optional fields remain round-trippable when safe. Manifest dependencies must be independently resolvable or explicitly bundled within approved rights. Export access to answers, rubrics, unpublished revisions and learner records is separately scoped from ordinary instructional content.

External integrations negotiate explicit service and data profiles. LTI service calls bind to one deployment, resource link and authorized gradebook destination. Validate OIDC state, nonce, signature and claims at launch, apply least-privilege grade and roster scopes, and process result updates idempotently. Roster exchange distinguishes authoritative synchronization from one-time import and stages role, section, status and membership changes for audit. QTI adapters verify machine scoring and feedback against exchange fixtures. Content-cartridge adapters report version, namespace, external tool and resource coverage.

Minimum release gates for curriculum migration are a successful dry run, complete object inventory, stable IDs over reimport, correct order and references, resolved mandatory assets, accessible learner preview, representative assessment parity, a documented fallback for every blocked object, and an educator-approved pilot. Grade and history cutover has its own reconciliation and approval gate. Build fixtures from a small representative sample of each archive variant plus malformed, adversarial and partial samples.

## Specifications

- [ADL SCORM programmer guide](https://adlnet.gov/assets/uploads/SCORM_Users_Guide_for_Programmers.pdf)
- [ADL SCORM 2004 fourth edition testing requirements](https://adlnet.gov/assets/uploads/SCORM_2004_4ED_v1_1_TR_20090814.pdf)
- [ADL SCORM 2004 fourth edition test suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite)
- [1EdTech QTI specifications](https://www.1edtech.org/standards/qti/index)
- [1EdTech Common Cartridge](https://www.1edtech.org/standards/cc)
- [1EdTech LTI Advantage conformance guide](https://standards.1edtech.org/lti/specifications/guides/conformance/conformance-guide)
- [1EdTech OneRoster 1.2 specification](https://standards.1edtech.org/oneroster/specifications/standards/v1p2)
