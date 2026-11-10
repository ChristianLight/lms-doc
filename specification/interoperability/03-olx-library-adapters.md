# 03. OLX and standalone library conversion

## 3.1 Input profiles

Implement recognition of course, legacy reusable library and modern reusable library archives independently. The outer container and verified inner profile are separate results. The documented cases describe the planned adapter. A successful bounded inspection does not imply an implemented migration. A nested SCORM ZIP is an asset of a course transfer and starts a separate package validation step. Current drafts, published snapshots, original source library, assigned local snapshot, and learner state are distinct graphs.

| Profile | Required signature | Key reconstruction |
| --- | --- | --- |
| `olx.course/1` | A `course.xml` at the root of a verified ZIP or tar/gzip container, or in one permitted wrapper directory. The root node is `course` with an embedded definition or exact scoped descriptor | Institution, source namespace, source organization, course code and run code form source course scope. Include block type and usage key beneath that scope |
| `olx.library.legacy/1` | One `library.xml` and type-scoped XML when records exist | Institution, source namespace, source organization and library code form scope. Do not share it with a similarly named course |
| `olx.library.archive/1` | ZIP root `package.toml` with `[meta].format_version = 1` and `[learning_package]` | Library key from package header. Entity key and revision number identify versioned entry. The case and full form of original identifiers remain intact |

Content can be written inline or split by type. A supported inline component with a valid body needs no separate type directory. A reference whose target is required by a selected published root stays blocked when the target is missing. A safely detached malformed or missing item remains a protected inventory issue. Enable each input container and structural form only after approved conformance and migration fixtures. Unknown root attributes are inert source metadata. The adapter never guesses destination Institution from a source `org` attribute. `origin_server`, author email and archived creation times are provenance data and provide no authority to bind the artifact to a previously registered source namespace.

## 3.2 Course discovery and tree construction

1. Open `course.xml` with entity expansion disabled. A descriptor such as `<course org="school" course="math" url_name="term1"/>` resolves `course/term1.xml`. An inline definition can carry its children directly. A root without explicit run, organization or course values needs an operator-supplied verified namespace mapping. Treat competing descriptors and alternate run roots as separate source-scope and policy candidates. The default plan selects one exact root. Never infer authority from equal course body bytes. An unselected alternate root remains outside the selected closure unless an operator separately authorizes and stages it.
2. Enumerate direct structural children in XML order. A pointer such as `<chapter url_name="number"/>` loads `chapter/number.xml`. Verify that the referenced root element type matches and compare any repeated IDs. Map `chapter` to a section-like ContentNode, `sequential` to an ordered module-like node, `vertical` to a learner page and leaf components to native blocks or ActivityVersions.
3. Create each immutable definition and each distinct ContentPlacement. Assign a distinct scoped occurrence identity when the same definition is used more than once. Source positions help identify initial candidates. Reordering indistinguishable repeats requires a reviewed stable mapping before reusing an occurrence ID. Reused references can share definitions while preserving separate placements. Reject a parent-child cycle, repeated identity with conflicting bytes, duplicate sibling placement or orphan prerequisite.
4. Capture visible title, locale, descriptions, access restrictions, start and due dates, and grouping and enrollment-track qualifiers from both recognized policy entries and XML. Record precedence by release profile. Where sources disagree or the source timezone is omitted, generate an unresolved setting instead of selecting a date or group.
5. Parse all reachable children before orphan classification. Keep unreachable definitions as detached source records. They may represent hidden content or former revisions. Require authorization to include detached content as a separate reusable item.
6. Resolve assets and links after all IDs are allocated. Rewrite only parsed nodes and CSS URLs under a vetted allowlist. Never perform an unrestricted string replacement of paths or hostnames inside learner text.
7. Produce separate source counts for structural nodes, placements, definitions, policies, media, external references, drafts, unsupported records and nested packages. Include the reachable and detached counts.

### Exact course records

| Source input | Recognition | Canonical projection |
| --- | --- | --- |
| `course.xml`, `course/<run>.xml` | Descriptor and tree root | Course, CourseVersion, source offering metadata candidate |
| `chapter/<key>.xml`, `sequential/<key>.xml`, `vertical/<key>.xml` | Typed structural references or inline nodes | ContentNode and ContentNodeVersion plus ordered ContentPlacement |
| `html/<key>.xml`, companion `.html` | Parse `filename` according to profile or inline markup and CDATA. Never trust a basename with a path separator | Typed editorial block with sanitized rich text, semantic tables, media, accessibility and link records |
| `problem/<key>.xml` | Prompt, response controls and grading configuration under `problem` | ItemVersion and MarkingRuleVersion with a corresponding ActivityVersion or assessment slot |
| `video/<key>.xml` | Display label, `html5_sources` decoded as JSON, stream references, `youtube_id_1_0`, video identifier, transcript children or transcript mapping | Video activity and asset candidates. Approved URLs and transcript language and format remain explicit |
| `about/`, `tabs/`, `info/`, `custom_tags/` | Separate static editorial pages and profile-specific extension content | Metadata page or ancillary ContentPlacement with original route retained |
| `assets/assets.xml`, `policies/assets.json`, `static/` | Optional metadata, logical paths and shared bytes | AssetVersion with raw digest, media type, rights, and full origin key |
| `policies/<run>/policy.json` | Keyed course or block metadata. Validate top-level and value types | Versioned scope-local settings candidates |
| `policies/<run>/grading_policy.json` | `GRADER` rows and `GRADE_CUTOFFS` mapping | Grade categories, category weights, minimum category count, drop count and grade-scale candidates |
| `drafts/` | Changed draft subtrees with original `parent_url` and `index_in_children_list` | Draft-only candidate revisions associated to a verified parent, without modifying published projection |
| `library_content/<key>.xml` | Source library key and source revision, draw policy, and child copies when present | Versioned assessment pool, linked LibraryEntry candidate and local immutable item snapshot |
| `scorm/<key>/package.zip` | Referenced by `scorm_package_path` on a package activity descriptor when available | Independent SCORM transfer artifact and PackageVersion after validation |

Attributes can contain JSON encoded in XML. Parse XML once and JSON once. Do not HTML-decode a second time. A transcript stored as SubRip should preserve exact timing and asset provenance. WebVTT conversion keeps original bytes, tests valid cue ordering and escapes learner markup. A video provider ID without media bytes becomes a reviewed remote dependency. Do not synthesize transcripts or publish with missing required accommodation assets.

### Schedule, grades and prerequisites

Map source dates to candidates for CourseOffering and AssessmentDelivery policy. Keep calendar timestamp plus source timezone and source field. Unqualified local dates require an institution timezone choice and explicit daylight-saving handling. Preserve `graded`, format category, visibility and release gates separately. Only a graded activity contributes evidence to a GradeItem. Hidden content is not equivalent to excluded grade weight.

For example, a source category `Assignments` with weight `0.40`, minimum count 3 and drop count 1 and a category `Exam` with weight `0.60` convert to exact weights `0.4` and `0.6`. If the source evidence confirms lowest normalized item drop and equal remaining assignment weight, assignment results 70, 80 and 90 out of 100 yield 85 percent after dropping 70. With exam 75 percent the aggregate is `0.4 × 85 + 0.6 × 75 = 79`. A minimum count of three is preserved independently and evaluated as a policy rather than reinterpreted as a required grade threshold. If the observed source policy uses points-weighted totals or drops only eligible completed items, the destination must encode the verified alternative or block parity approval.

Prerequisites may carry completion and minimum score requirements. The adapter must bind each reference to a canonical target placement or criterion. An unresolved reference is blocking even when learners can render the page. Verify prerequisites across an offering through stable placement scope. Detect cycles before approval and record what becomes newly inaccessible if a prerequisite is changed.

### Published and draft layers

Import the main tree first. Allocate draft nodes by source key without replacing the published definition. Bind a changed draft subtree to its verified parent and child index. Resolve the full scoped parent usage key and exact layer before interpreting the index against the captured sibling order. Two different draft children claiming one slot or anchor need a reviewed ordering. A parent from an alternate run or unknown layer stays unresolved. A draft-only child with no published version is visible only to authorized editors. A later incoming archive with no draft folder does not delete an existing private destination draft. An opaque source key, including a 32-character hexadecimal value, does not become a native UUID. Source revision IDs and accepted published fingerprints remain separate from target draft revisions and their crosswalk baselines. Transfer plans can explicitly retain a local private draft during a source update.

## 3.3 Content and relationship rewriting

Resolve URI references with a parser aware of the current asset scope. For course content, `/static/diagram.svg` looks up the course-wide asset root. For modern library content, it looks up the component version's `static/` root. `/jump_to_id/<unit>` resolves through the source course's unit map to a canonical ContentPlacement. Relative links resolve from the authored document directory only when the profile declares that behavior. Preserve query strings and fragments on a successful safe rewrite. Escaped slash and ambiguous double-percent encoding are errors.

| Case | Decision |
| --- | --- |
| Internal anchor to a verified unit | Render via canonical placement lookup with stable anchor and current localized label |
| Full URL at the inventoried old course host | Parse route. Rewrite only if source host, course key and usage key all match a verified record |
| Referenced asset digest matches existing bytes | Reuse bytes in the permitted store. Preserve separate AssetVersion rights and display metadata |
| External video, lab, interactive embed or linked tool | Preserve candidate URL, title and rights. Review a new approved deployment and media host before learner access |
| Unsafe embed script, inline handler or unsupported CSS URL | Remove from projected markup and classify accessibility or learning loss. Keep restricted source evidence |
| Relative link with two possible destinations | Record blocking ambiguity for dependent graded content and require a human selection |

Normalize link display without rewriting link semantics. Preserve accessibility descriptions, meaningful text, keyboard operation and original media correspondence. For SVG and mathematical markup use a separate element and attribute allowlist. Strip scripts, remote fetching, event handlers and navigational elements that escape the intended host.

## 3.4 Assessment conversion matrix

Parse response types and controls independently. Preserve source ordinal path and expected response identity so separately rendered controls still submit to the correct scorer. Treat a problem with three response nodes as one source item with three interactions when the source owns one weight, hint and attempt counter. Separate child marks and aggregation under an explicit canonical rule.

| Response type | Required source evidence | Destination contract |
| --- | --- | --- |
| `multiplechoiceresponse`, `choiceresponse`, `optionresponse` | Option order, stable lexical option keys, correct flags, acceptable combinations, feedback, shuffle and partial credit | Single or multiple selection with explicit option IDs. Truth tables verify empty, mixed and excess selections |
| `stringresponse` | Expected responses, case handling, regex dialect or exact mode, variants and feedback | Unicode normalization and comparison flags. Rewrite regex to allowlisted grammar with bounded complexity. Case and whitespace rules remain explicit |
| `numericalresponse` | Expected value, accepted answers, absolute or percent tolerance, units and precision | Decimal evaluator with explicit inclusive interval and unit policy. Zero reference and percentage tolerance require a separately defined fallback |
| `formularesponse` | Variable names and dimensions, sample bounds and count, canonical expression, domain, case and tolerance | Evaluator profile with exact expression syntax, deterministic samples and domain failures. Symbolic equality is a separate configurable rule |
| `customresponse` | Script body or declared grader, inputs, outputs, errors, seed policy, partial credit and feedback | Restricted replacement rule, manually verified native evaluator or approved remote grader. Imported script remains inert |
| Drag/drop, graphing, image regions, file or external assessment | Region coordinates and scoring, graph semantics, rubric and dependencies as applicable | Typed interaction if matching behavior exists. Otherwise rebuild or hold as a blocked dependency |
| Open or peer-assessed submission | Prompt, rubric, criteria, allowed files, assignment policy and peer/staff workflow | Native human scoring with distinct rubric and moderation snapshots. Grade history uses a separate learner record transfer |

Preserve `weight`, `attempts` or maximum submissions, `showanswer`, `rerandomize`, reset behavior, hints and exposure rules. Default to protected solutions when source display behavior is ambiguous. Retain original authored values even when normalized projections are produced. Choice order, bank sampling and formula parameter randomization are separate behaviors.

### Math and embedded grader parity

A formula sample attribute shaped `x,y@1,2:3,4#5` contains variable names `x,y`, lower bounds `1,2`, upper bounds `3,4` and a sample count of five. Validate matching dimensions, finite numeric bounds, lower at most upper and bounded sample counts. Never apply source scripts to establish bounds. Record source comparator mode, sample generator, evaluation precision and script mechanism if known. Exact historical samples require the original seed state and source PRNG implementation. Freeze destination sample coordinates for reproducible future marks.

An evaluator must distinguish a syntax failure, domain error, false comparison, resource limit, unsupported function and evaluator crash. For expression `x^2/x`, equivalence to `x` across a domain that includes zero differs from equivalence over nonzero samples. For expected 100 with 2 percent tolerance, examples 98 and 102 pass if endpoints are inclusive, 97.999 and 102.001 fail. With an expected value of zero, 2 percent alone yields a zero-width interval unless a verified source policy supplies another rule. Include probes at singularities, bounded extremes, decimal separators, wrong units and equivalent noncanonical expressions.

Embedded source code is an analysis artifact. Tokenize and fingerprint with strict size limits but never import or execute it in a parser, learner renderer or live scorer. Classify whether it computes parameters, score, feedback, dependencies or external calls. A reviewed replacement includes side-by-side deterministic vectors with input, source output, target output, parameters, score, feedback, and evaluator version. Pin representative seeds where available. The assessment owner approves every deviation affecting marks. For legacy continuation, external evaluation requires a separately provisioned worker or secure tool integration with isolated egress, no database access and explicit request policy.

## 3.5 Library import

### Legacy library transfer

Parse `library.xml` for organization, library code, title and ordered type references. Read each `<type>/<key>.xml` by pointer. Treat policy and asset directories as optional profile features. Do not require legacy libraries to contain group membership or rights. Course-local copies use their own scope even when data matches a library entry byte for byte.

For an assignment referencing `library-v1:Example+Numbers` revision `r18` with six local candidate copies and draw count two, preserve an immutable six-item local pool if every candidate is available and verified. Resolve provenance to the reusable library separately. Never infer the source item key solely from title or matching grade result. Map source keys from explicit definitions or reviewer-supplied verified metadata. If only five candidates are present, draw count two is possible but the distribution changed. Block parity approval unless the pool is restored or a reviewer approves a known new version.

### Modern versioned library transfer

| Location | Fields and validations |
| --- | --- |
| `package.toml` | `[meta].format_version` required integer 1. Require `created_at` and `[learning_package]` `key`, `title`, `description`, `created`, `updated`. Restrict optional operator metadata to provenance access |
| `entities/xblock.v1/<type>/<code>.toml` | `[entity]` with `key` matching exact path type and code, `created`, `can_stand_alone`. `[entity.draft]` optional and `[entity.published]` may be empty. Validate each pointed `version_num` against `[[version]]` with unique positive `version_num` and required `title` |
| `entities/xblock.v1/<type>/<code>/component_versions/v<N>/block.xml` | One scoped document per declared version. Type must agree with metadata. HTML can be CDATA rather than a companion file |
| `.../component_versions/v<N>/static/` | Resolve assets in the exact component revision. No fallback to another version with a same-named file |
| `entities/<key>.toml` | One container marker at `[entity.container.section]`, `[entity.container.subsection]`, or `[entity.container.unit]`. Each `[version.container]` lists ordered child entity keys |
| `collections/<key>.toml` | `[collection]` with `key` matching the filename, `title`, `description`, `created`, and `entities` as an array of exact entity keys. Resolve keys before exposing membership |

Create both referenced component versions if they differ. When draft and published pointers name the same revision, create one immutable definition and keep the two pointer states. The archive does not promise revisions between current snapshots. Resolve container child identities first and bind children to the matching publication graph. A published parent with a draft-only child is a blocking structural issue. Do not infer a component's library identity from filename alone. Preserve full archive entity key and library-scoped source identifier. Collection membership is separate from ordered child placement and from teacher permissions.

## 3.6 Nested packages and verification

A package descriptor can exist without package bytes. Validate the explicit source `scorm_package_path` against the archive index and digest if provided. If no path is declared, inspect an approved package inventory and record the exact mapping decision. Never bind the first ZIP with a matching basename. Compare known original bytes and reconstructed ZIP semantic manifest and file digests separately. Do not register either as an editable native course.

Build the acceptance corpus from a synthetic course, legacy library, modern library and real permitted source exports. The minimum matrix includes one source XML pointer and one inline node, shared course assets, repeated component-local asset name, unresolved link, unsupported script, multi-input problem, sampled formula, rotated package digest, and a draft-only unit. Record file-level and per-record transformations in the transfer report. The included `fixtures/olx` example demonstrates a versioned text element, numeric tolerance, package-ready directory shape and a missing link case without third-party curriculum.
