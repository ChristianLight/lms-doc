# 02. Identity allocation and link resolution

## 2.1 Independent identities

A hexadecimal-looking key is an opaque source identifier. Its spelling does not prove a UUID version, uniqueness across systems, or whether it identifies a definition, an occurrence or a revision. Accept non-UUID spellings, repeated type/key pairs across layers and reused raw keys in independently scoped archives. The target can use globally unique IDs without inheriting those assumptions.

| Identity | Canonical meaning | Authority and scope |
| --- | --- | --- |
| Source namespace | Stable registered connector or authorized source installation identity | Institution and approved source owner. Never inferred from a URL or archive wrapper |
| Source course scope | Exact selected source organization, course and run tokens | Namespace and approved course selection. Alternate runs remain separate |
| Source definition | Kind and raw external key, with exact case and validated representation | Source course or library scope |
| Source revision | A verified source version token, or stable fingerprint of identified bytes and dependencies | Source definition, typed profile and layer evidence |
| Source occurrence | One declared relationship from a parent occurrence to a child definition | Source release graph with an exact edge location |
| Canonical content and activity | UUID identities for ContentNode, Activity, Item, LibraryEntry and related versions | Target Institution and owning domain |
| Canonical placement | UUID of one ContentPlacement linking the selected immutable CourseVersion and a position | Target course release and exact parent placement |
| Physical asset bytes | Verified content digest and private StorageObject | Approved storage and rights boundary. Logical AssetVersion identity remains separate |

A source run and a native CourseOffering can correspond by approved policy, but the archive's key does not create participants or release a new offering. Metadata indicating another URL origin cannot extend source namespace authority. The same source key appearing as a page and as a file entry is two different key spaces.

## 2.2 Allocation and crosswalk algorithm

1. Normalize and validate archive paths while preserving the original source key. The normalized path is a locator. Do not lower-case source identity, decode it recursively or remove punctuation to fit a target GUID.
2. Confirm the Institution, source namespace, course or library scope, object kind and external key. Serialize the tuple unambiguously as distinct typed fields. Use a documented canonical encoding or a registered scope key if a transport field has a smaller length limit. Preserve original values under restricted provenance access and reject ambiguous or unsupported truncation.
3. Use the ExternalObjectMap for stable canonical identity. A first import reserves one UUID in staging per validated tuple, with a uniqueness guard. Retries and concurrent jobs must observe the same reservation or explicitly rebase. Do not create a target UUID from a raw source block key merely because it has 32 hexadecimal characters.
4. Use TransferRecord for the immutable input revision, exact source locator, staged candidate, baseline target revision and disposition. Record an independently computed source fingerprint for the definition body and all behavior-affecting profile inputs. Logical identity and content hash have separate roles.
5. Allocate or resolve all definition identities before rewriting relationships. Then create versioned edges, AssetVersions, item definitions and placements through their domain owners. Stage published and draft projections separately and bind known versions precisely.
6. Apply three-way comparison on reimport. Unchanged source bytes keep the existing target identity. A source-only change can propose a new target version. Concurrent source and target changes require explicit comparison. A missing source key can raise retirement review only for an authoritative complete snapshot.
7. Promotion confirms all scoped owner receipts, stable map revisions, dependency decisions and the approved generation. An interrupted job remains private. Retry does not allocate duplicate identities or mutate earlier learner history.

Canonical identifiers do not need to be deterministic across Institutions or unrelated forks. A clean-room fork can allocate fresh canonical IDs and retain a lineage mapping. Preserve original identifiers under limited access for support and future reconciliation. A destination course can deliberately retain an imported item as reusable content after its source placement is retired, with independent rights and provenance.

## 2.3 Placement correspondence and repeated definitions

An edge ordinal tells where an occurrence appeared in one snapshot. It is useful for deterministic traversal, but it is not a durable identifier across reorder or moves. A source display name, content hash and authoring path can all recur.

Match a later snapshot using the strongest available evidence.

1. A source placement-specific key that is stable and scoped to this exact run can identify the occurrence.
2. If the parent placement is already matched and the definition has one unique matching child occurrence, compare neighboring and type evidence before retaining the existing occurrence identity.
3. If the same definition moved across parents, require stable placement evidence or explicit reviewer confirmation. Otherwise stage a new occurrence and a retirement candidate rather than silently rewriting historical placement identity.
4. If identical children recur and no stable occurrence keys distinguish them, mark an ambiguity. Never match by the new ordinal alone.
5. For a newly authored inline object with no source key, use its exact path and fingerprint to identify it inside this transfer. Treat inferred correspondence on a different snapshot as a review candidate.

Consider an invented two-page outline that reuses one chart under both `observations` and `review`. Allocate one Chart ContentNodeVersion and two ContentPlacements. The order of the two placements can change without changing the content definition. A link aimed at the chart definition alone is ambiguous. It must supply a scope and unique placement or receive a review decision. A submission or progress record belongs to the attempt and occurrence that actually produced it.

## 2.4 Link inventory and resolver

Extract URL-bearing markup from the parsed XML body and sanitized or inert HTML parser. Record source location, attribute role, layer, raw target, optional query and fragment, and requiredness. Source markdown that duplicates rendered markup is separate authoring evidence. Counting both as independent placed links can inflate coverage. Inline CSS, `srcset`, MathML/SVG attributes, script-generated URLs, runtime tool redirects and player navigation each require a declared parser profile. A structural diagnostic with fewer parsers reports the coverage boundary.

| Input form | Resolution rules |
| --- | --- |
| `/jump_to_id/<key>` | Parse exact route, decode a single safe key once and resolve a selected unit in the approved course and appropriate layer. Bind to a unique ContentPlacement, not a private draft or raw XML filename |
| Absolute or scheme-relative legacy URL | Require registered authority and allowed scheme, host, port and route. Verify exact course and run scope where the route carries it. A matching-looking terminal key cannot authorize the hostname |
| Typed legacy source object URI | Parse with a known source grammar. Validate organization, course, run, object kind and key. Convert only after the associated scope is approved |
| `/static/<path>` or typed asset URI | Resolve under the applicable course or component asset root. Compare exact safe path and verified storage bytes. Keep metadata association and rights independently |
| Relative media or content link | Resolve against a known authored or delivery base in this profile. File adjacency does not prove browser route semantics. If the base is unknown, retain a reviewable unresolved target |
| Local fragment | Keep only when it identifies an approved destination element after sanitization or a mapped accessible anchor. Do not convert fragment syntax into a source definition key |
| Ordinary external HTTPS link | Preserve as an external reference subject to policy. Do not fetch or recast it as internal without authority |
| Non-HTTP, unsafe, malformed or unsupported route | Preserve restricted evidence and classify the issue. Never execute a URL or render an unsafe scheme |

Reject user-info credentials, path traversal, encoded separators, ambiguous nested encodings and invalid Unicode. Normalize URL origin using an exact approved authority rule with IDNA and explicit port handling. Resolve path segments without changing key case. Keep repeated safe query parameters and fragments only when the approved route profile declares their role. Remove, redact or reject authentication tokens and undeclared parameters. Do not carry an old signed URL through a canonical internal route.

For a published source page, an apparent destination that is only available in a draft is not a learner link. For a private draft preview, apply the approved draft graph and source scope explicitly. Do not infer a target from a file found in an alternate or detached run. A file present under `vertical/` can remain nonlaunchable because the selected CourseVersion has no corresponding ContentPlacement.

### Invented resolver cases

| Source context | Input | Expected state |
| --- | --- | --- |
| Approved run `spring`, one visible placement of `seedlings` | `/jump_to_id/seedlings#diagram` | Resolve the placement and mapped diagram anchor |
| Same course, selected only draft contains `later` | `/jump_to_id/later` on published page | Draft-only dependency. Never expose it through the published route |
| Current course contains `seedlings` | `https://unknown.example/jump_to_id/seedlings` | Absolute route needs approved authority. Do not resolve by matching key |
| Current course contains two approved occurrences of a reused definition | Definition-only shortcut to that key | Ambiguous occurrence. Require an exact scope or selection |
| Course static store contains `art/growth.svg` | `/static/art%2fgrowth.svg` | Encoded separator rejected even though a decoded filename exists |
| Alternate run contains `private-notes` | `/jump_to_id/private-notes` in the selected run | Detached or out-of-scope. Do not select it automatically |
| Published page with required chart | `/static/art/absent.svg` | Blocking missing asset until resolved or reviewed replacement is applied |

## 2.5 Report, approval and acceptance

Group findings into selected learner blocking, selected authoring remediation, detached inventory and diagnostics. For each, show disposition, affected exact scopes and dependency impact. Restricted reviewers can view the raw locator and candidate mappings. Authorized operational diagnostics may include scoped counts without raw identifiers. Public reports for private source tests state the checks and outcomes without exposing underlying archive inventories, URL values, keys or fingerprints.

A link to an unavailable mandatory assessment, prerequisite or required accessibility resource blocks publication of its dependant. A cosmetic broken link can be accepted as a documented difference only by the owning authority. Do not treat a partial external route match as proof of source equivalence. Replacement mapping creates a new plan revision and invalidates prior approval of affected projections.

Validate that repeated imports preserve crosswalk identity, approved order, edge targets and rights. Include synthetic cases for source key reuse across runs and layers, repeated placements, case collision, draft-only destination, absolute origin without authority, encoded separator, asset with duplicate basename under different folders, and accepted resolution replay. Reconcile each target with the selected release graph before publishing.
