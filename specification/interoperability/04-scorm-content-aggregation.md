# 04. SCORM content aggregation, import and export

## 4.1 Profile boundaries

SCORM import recognizes a content package from its archive and manifest. The content aggregation model defines resource packaging and the activity tree. A run-time environment defines browser API behavior. Sequencing and navigation, where present, defines the delivery order and rollup. Record and test those three capabilities independently.

| Profile | Primary package cues | Strict behavior |
| --- | --- | --- |
| SCORM 1.2 | Root `imsmanifest.xml`, 1.2 manifest metadata and namespace bindings, `adlcp:scormtype` with lowercase `t` | Import organizations, items, SCOs, assets, launch data, mastery and supported prerequisites. Do not apply a 2004 sequencing model |
| SCORM 2004 second edition | Declared edition and matching profile schemas | Bind the edition's CAM, runtime and sequencing rules. An API-compatible launcher alone is a compatibility subset |
| SCORM 2004 third edition | Declared edition and matching profile schemas | Bind third-edition rules and conformance fixtures. Preserve source rules rather than normalizing to fourth-edition defaults |
| SCORM 2004 fourth edition | Declared edition and matching profile schemas | Require fourth-edition behavior for declared full support. Preserve edition-specific sequencing, navigation and objective metadata |
| Unverified 2004 package | 2004-like namespaces without reliable edition evidence | Review-only until importer identifies an approved edition and verifies profile. Never assume fourth edition |

Declare an edition's runtime support independently for player browser configurations. Package validation treats XML namespace URI and case as significant. Filename, ZIP extension, metadata display name, a JavaScript call or source authoring tool are supporting clues. Use a pinned per-edition schema catalog for definitive validation. Keep the untouched source manifest even when a reviewed compatibility adapter repairs a wrapper directory, case mismatch or stale metadata.

## 4.2 Manifest model and records

| Construct | Persisted representation | Constraints |
| --- | --- | --- |
| Manifest | PackageVersion with declared edition, original identifier, version text, profile evidence, original blob digest, normalized manifest digest and review status | Exactly one approved root. Original version is a lexical value independent of package revision |
| `organizations` and default | Ordered PackageOrganization records with one manifest-local default for a deliverable profile | Explicit default must resolve. Resource-only packaging is inventoryable without a learner launch |
| `organization` | PackageOrganization with external identifier, title, root rules, visibility and order | Identity unique within the owning manifest |
| `item` | PackageActivity occurrence with parent, sibling order, identifier, title, visibility, parameters, resource edge, time/launch metadata and sequencing rule pointers | Preserve repeated use of the same resource through distinct items. Validate cluster and leaf constraints for declared edition |
| `resources` and `resource` | PackageResource with original ID, media type, SCO/asset type, entry URI and composed base | Entry point required for launchable resource. Dependencies and file refs use validated exact paths |
| `file` | Resource-file association with normalized path, digest, media type and safety class | Multiple resources can point to one verified file. Executable web content remains isolated |
| `dependency` | Directed ResourceDependency between resources | Resolve in package scope. Reject cycles for approved deployment profile, or preserve cycle evidence for manual normalization |
| Metadata | Manifest, organization, item, resource and file metadata document or safely linked in-package record | Never fetch a metadata location during import. Keep rights, duration, language and catalog classification separate from grade policy |
| Rule extension | Edition-specific definition and owning item or organization | Parse known schemas into typed rules with source paths. Unsupported rules block dependent full sequencing claims |

Preserve package organization and resource identifiers as source text. PackageActivity identity is generated once per PackageVersion and organization occurrence. When resource `r1` appears as items `intro` and `review`, both point to the same PackageResource but have separate PackageRegistration state, bookmarks, limits and scores. A visibility flag controls navigation presentation and does not decide mastery or course permission. A 2004 non-leaf item cannot reference a launchable resource where the declared CAM prohibits it. A leaf item must resolve a resource. Submanifests require an independently tested profile. Default ingestion holds packages that depend on them for manual remediation instead of silently flattening organization or sequencing scope.

## 4.3 Path and parameter resolution

1. Enumerate exact archive entries before parsing references. Compare normalized URI path segments with archive names using NFC and case-sensitive matching. Reject case-fold collisions even on case-sensitive storage so development and deployment behavior agree.
2. Validate each `xml:base` at manifest, resources and resource scopes according to the edition. Compose inherited bases once in that order, using RFC 3986 URI resolution. A base representing a package directory requires its trailing slash where the edition requires it.
3. Parse an entry `href` into path, query and fragment. Percent-decode each path segment at most once for matching. Reject absolute paths, backslashes, escaped delimiters, encoded traversal, origin-relative paths, embedded NUL, network-path references, schemes other than an explicitly approved remote launch profile, and any path escaping the immutable package root.
4. Resolve and validate launch entry, `file` references and metadata locations against the package index. Dependency resolution visits each resource once and includes its own recursively required files.
5. Compose item `parameters` with the verified resource href using the declared edition's syntax. Preserve existing and repeated query keys in source order, then keep a single fragment. Reject malformed separators and any parameter that changes the URL origin, path or scheme. Do not pass LMS bearer tokens as item parameters.
6. Serve local launch paths by verified entry ID and canonical path. The resolver uses full paths and does not retry by filename or suffix. A package with two `driver.js` files under distinct directories is valid and both resolve exactly.

Example source chain `xml:base="content/"`, resource base `unit-2/`, entry `start.html?lang=en#intro`, and an approved item query parameter `theme=plain` results in package path `content/unit-2/start.html`, query `lang=en&theme=plain`, and fragment `intro`. An entry `%2e%2e/%2fadmin.html` never becomes a launch candidate. Exact normalized URL validation still applies when data is served after launch.

## 4.4 Import and approval

Import SCORM as a private TransferArtifact. The scan records manifest root, candidate profile, archive and normalized manifest digests, byte counts, source asset rights and package reviewer. Profile validation rejects malformed CAM, unsupported mandatory extensions, missing launch resources, resource dependency cycles under the default profile, and undeclared network demands. Store referenced but unused files and unreferenced package assets as separate inventory counts. JavaScript imports inside a static analyzer are hints and dynamic dependencies are runtime compatibility evidence.

A source runtime manifest declaration provides initial data. For SCORM 1.2, preserve mastery score, launch data, max time and time-limit action when declared. Parse prerequisite expression only under the explicit 1.2 profile and retain unresolved IDs. For 2004, preserve normalized completion threshold and measure, objective references, time-limit action, launch data and sequencing extensions without silently migrating their semantics. Map manifest fields to exact run-time data elements at session initialization. A previously closed registration never takes new launch data merely because a new PackageVersion exists.

Reviewers see package outline, each resource path and type, asset count, detected extension needs, browser-test results, data exposure, current network grants, packaging profile and execution support. Preview uses a separate synthetic enrollment and sinks all writes into a test registration. If authorized, the reviewer can approve use for an ActivityVersion after conformance evidence and required rights are in place. Any file changes generate a new immutable PackageVersion. Existing registrations and sessions retain the previous version until native reassignment policy permits a new attempt.

## 4.5 Export profile

A package generator is an optional feature separate from native curriculum export. Declare targets per edition and publish a supported projection of content, assessment and score policy. The first candidate profile can render authored rich text, approved local media, accessible interactions with explicitly portable scoring and a bounded list of SCOs. It cannot export private answer banks, external tool credentials, server-side scripted marking, learner history or a privacy-sensitive integration unless the relevant native policy and destination contract explicitly authorize it. Student-facing SCOs inherently contain any client-side marking logic they use. For high-stakes content, prefer a server-backed activity profile or reject export of protected solutions.

1. Freeze selected immutable source versions and verify owner permissions, media rights and grading review.
2. Build a portable activity tree and assign deterministic XML identifiers from safe source keys. Keep package item and resource identifiers distinct and stable across repeat export of the same graph.
3. Write exact schema-version metadata, namespace bindings, default organization, items, resources, file declarations and dependencies. Write sequencing only for profiles with verified generator and player coverage.
4. Emit self-contained HTML, CSS, scripts and media with bounded paths and no application credentials. The SCO code searches the correct edition API and handles loss of connection and explicit finish. Plain assets do not send scores.
5. Validate the produced package using the pinned edition schemas and independent reference-player fixtures. Test root manifest, launch location, score and completion and suspend/resume. Return a loss report before making the export available.
6. Build ZIP with sorted paths and deterministic content where requested. Store export digest and selected source snapshot. Include license metadata where permitted, then expire download authorization independently from underlying published curriculum.

Repackaging an intact third-party package is a different mode. Preserve untouched original bytes unless rights or a supported remediation workflow permit a normalized variant. Hash the original and normalized variants independently. A package that validates on the target browser is still checked against the declared edition and scope before conformance is claimed.

## 4.6 Evidence

Acceptance requires reference content, a real approved vendor package, and synthetic tests. Include one SCO and one asset, nested structures, repeated resource occurrence, multiple organizations, internal dependencies, invalid traversal, strict root mismatch, manifest prefix changes, edition ambiguity, metadata-only resource library, and unsupported sequencing extension. Include archive digest, declared edition, profile revision, player revision, browser and test date in the test record.

- [ADL fourth-edition content aggregation model](https://lms.technology/for/scorm/2004/4th_edition/standards/SCORM_2004_4ED_v1_1_CAM_20090814.pdf)
- [ADL fourth-edition testing requirements](https://adlnet.gov/assets/uploads/SCORM_2004_4ED_v1_1_TR_20090814.pdf)
- [ADL fourth-edition test suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite)
- [URI generic syntax](https://www.rfc-editor.org/rfc/rfc3986)
