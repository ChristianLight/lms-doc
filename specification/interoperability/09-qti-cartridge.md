# 09. Assessment and curriculum exchange

## 09.1 Negotiated profiles

An exchange profile binds an Institution, partner, direction, package family, exact edition, schema bundle digest, supported feature IDs, publication gate and test corpus. Capabilities are displayed per direction. An importer can preserve a package for re-export while marking its contents ineligible for native delivery. A valid package can use capabilities beyond the local profile.

| Profile | Recognition | First implementation | Explicitly review-gated |
| --- | --- | --- | --- |
| QTI 2.1 | 2.1 ASI namespaces, registered package resource types and 2.1 bindings | Read standard item packages and selected linear tests. Convert matching and mapping templates. Export only after partner fixture parity. | Arbitrary response programs, vendor extensions, external processing and legacy unversioned XML |
| QTI 2.2 | 2.2 ASI namespaces and binding | Add a separately tested adapter when a partner needs it. Reuse semantic transforms through version-specific decoders. | Assuming a 2.1 document can be re-labelled or that APIP support follows from recognizing a namespace |
| QTI 3.0.1 ASI | QTI 3 namespace and selected 3.0.1 ASI schema and binding | Export and import the declared native subset with declarative content, math markup and accessibility review. | Custom interactions, adaptive engines, unimplemented accessibility alternatives and formal results reporting |
| Common Cartridge 1.0–1.3 | Exact manifest namespace, profile metadata and resource type table | Start with 1.3 full-cartridge content and link import. Add 1.0, 1.1 and 1.2 as separate import profiles when samples justify it. | Assuming resources or embedded tests have the same edition or feature set as the manifest |
| Thin Common Cartridge 1.3 | Declared thin profile and link or tool resource types | Import a link catalog and supported placement tree as drafts. | Treating a URL as offline content or a link as a live deployment |
| Common Cartridge and Thin Common Cartridge 1.4 | Versioned full, thin or K–12 profile | Separate opt-in profiles until a selected candidate-final binding and interoperability suite are pinned. | Enabling 1.4 features through a 1.3 compatibility switch |

The core store keeps a typed versioned assessment model. Importing a QTI assessment does not register arbitrary XML as a grader. Result exchange uses a separate profile, purpose and permission from curriculum transfer. Claim conformance for the directions, editions and capabilities verified through their applicable test programs.

## 09.2 Package intake and traceability

An authorized author selects an institution-owned TransferArtifact, a profile, an assessment library or curriculum destination and a dry-run policy. The importer performs archive safety checks before decoding. It chooses local XSDs by pinned profile. XML namespace bindings, schema locations and remote template strings never cause network fetches. A supplied schema location is only provenance. Each parser caps XML depth, element count, attributes, reference edges and total decoded text.

1. Resolve the manifest root and supported resource table. Build an index by manifest resource identifier and a separate index by canonical package path. Use neither title nor basename as identity.
2. Resolve every resource entry point, file, dependency and nested document reference relative to its containing document and declared base where the profile permits it. Canonicalize paths before lookup. Preserve fragments for navigation. Reject escaping paths, duplicate normalized paths, contradictory base declarations, missing required bytes and cycles in graphs that require acyclic references.
3. Parse QTI item and test roots from declared assessment resources. Record type, edition, XML locator, source identifier and byte digest. Identity for repeat imports is Institution, partner namespace, logical package identifier, resource type and qualified source identifier. A path change alone cannot retire and recreate an item.
4. Parse declarations, interactions, references and assets before scoring transformation. Validate nesting and asset integrity. Independently classify scoring, presentation and exportability. An unrecognized accessibility alternate can block release even if the score rule is supported.
5. Stage dependency-aware TransferRecords in deterministic order. Record output IDs and revisions for each Item, Assessment, Asset or ContentNode. Resolve a source slot separately from its ItemVersion so an item can appear twice with different order or points when allowed.
6. Return a summary and paged issues keyed by TransferRecord. Publish after required score, access and presentation proofs pass. A failed or incomplete dry run leaves published items intact.

| Record | Persistence contract |
| --- | --- |
| ExchangeProfile | Required UUID, institution UUID, standard and edition enum, direction enum, profile key, schema digest SHA-256, capability IDs, state and integer revision starting at 1. Unique Institution, profile key and revision. Index Institution and active direction. Keep each revision while a job or publish decision references it. |
| TransferArtifact | Immutable archive bytes with SHA-256, Institution, original filename and byte length. Package answer keys are restricted assessment content. Index digest in its trust scope. Keep governed evidence while an active TransferRecord or decision needs it. |
| TransferRecord | Item records store qualified source key, path, profile revision, source fingerprint, target identity and revision and disposition. Item reference records additionally store parent placement and source occurrence identifier. Unique job and qualified source key. Index job and disposition, and target type and identity. |
| MarkingRuleVersion | Assessment-owned immutable rule version and digest. The adapter keeps the typed operator tree, template ID, response declarations and outcome visibility on the scoring side. Candidate preview never includes protected rule constants. |
| Package proof | Import evidence comprises issues, resolved mappings and an immutable parity artifact. The proof binds evaluator version, renderer build and digest of case vectors to the reviewed ItemVersion or AssessmentVersion. Re-evaluate when a pinned dependency changes. |

## 09.3 Native interpretation of QTI item data

The first delivery subset is non-adaptive and time-independent. It supports single and multiple choice, inline choice, ordering, matching with explicit directed pairs, text entry with an exact typed comparator and extended text mapped to a native manually marked response. Numeric text entry can compile to a bounded expression profile when every operator and tolerance is represented. A file upload or extended response requires an approved native grading policy or blocked release.

| QTI information model | Canonical treatment |
| --- | --- |
| Item identifier, title, locale and body | Item and ItemVersion. Validate a nonempty per-document identifier. Preserve its case and language inheritance. Convert the body to accessible, sanitized content nodes. |
| Response declaration | An interaction schema with variable identifier, cardinality, base type, authored default and limits. Correct values and mappings stay restricted. Validate unique declarations and the binding of each response variable to at most one interaction. |
| Outcome declaration | A typed output with identifier, default, visibility, optional normal bounds and interpretation. Explicitly bind the numeric score output and range. Preserve other outputs privately or block delivery when required. |
| Choice and association IDs | Stable source values. Reject duplicate choice definitions and absent choices. Browser visual order is independent. Ordered responses preserve sequence and multiple cardinality retains multiplicity when an operator needs it. |
| Template declaration and processing | A declarative generation policy when every operator, seed step and domain is available. Pin values on AttemptItem. External code, undefined variables or unsupported random generation blocks automatic grading. |
| Feedback, hints and solutions | Keep the condition and release point in MarkingRuleVersion or a feedback policy. An unreproducible condition remains in staging for review. |
| Accessibility | Preserve labels, alternatives, languages, tracks, MathML, keyboard rules and supported preference hooks. Review imported interactions with keyboard and assistive technology. Test timing separately. |

Represent null, zero, empty string and absent field distinctly. A declared response starts null in the item session and receives its authored default when the first attempt starts. A session that never interacts remains null. Process a blank user action under the interaction binding and stored response event. Require deliberate submission instead of inferring an answer from a visually selected default. Outcome initialization and non-adaptive resets follow the bound ASI edition and declaration, including numeric zero initialization where applicable. Adaptive outcomes can persist across evaluations. The first engine refuses adaptive items.

Bind operators against cardinality and base type at import. Initially support scalar identifier, boolean, string, integer and float, and directed pair in the matching profile. Use exact decimal in the native points ledger. Where an operator requires the selected edition's numeric semantics, calculate under those semantics at the adapter boundary and convert the result through an explicit quantization policy. Reject unsupported records, malformed numbers, infinities, implicit casts and overflow. Candidate-submitted syntax never becomes a host-language expression. Treat evaluation failure separately from an incorrect response.

## 09.4 Scoring compiler and worked cases

Register exact known response-template identifiers per edition. Accept historical standard aliases only after documenting equivalence and testing the registered definition offline. Parse package-local template files only through the bounded AST compiler. The evaluator caps depth and operations, forbids arbitrary invocation and pins the rule digest. The first profile supports restricted equality, declared mappings, Boolean guards and score assignments. Each added arithmetic and conditional operator requires a published type and null truth table. An unknown or remote operator blocks scored delivery.

- **Match-correct template.** Validate declarations and template-required identifiers. Compare scalar values by base type. For ordered containers, compare lengths and values by index. For multiple containers, compare multiplicity by typed value. A null response follows the exact template branch. Numeric zero is a real response.
- **Map-response template.** For a non-null input, walk each distinct typed value once. Resolve explicit keys before the default. Preserve case controls where the binding permits them. Sum contributions and apply optional bounds. Null follows the template's blank branch rather than the unknown-value default. Bind the numeric outcome to native points separately.
- **Map-response-point and spatial interactions.** Preserve shapes, mapping order, coordinate space and resource dimensions. A profile that enables them must implement the edition's overlap rules and count each mapped area once per container. The first delivery subset blocks spatial mapping.
- **Conditional feedback.** Evaluate on a server with restricted rule access. The author trace, assessor trace and learner release view have different permissions. A response-save acknowledgement does not reveal whether a protected correct option matched.

For QTI-A, additive primary colors are stored as three identifiers in a multiple response. The same three identifiers in any order earn 1. A repeated identifier is rejected by the choice validator. The operator is separately tested with typed containers outside that control. A blank response takes the null branch and earns 0 under the configured template.

For QTI-B, a mapping uses `raven = 2.25`, `wren = 0.75`, `goose = -0.50`, default `-0.25` and limits 0 through 2.50. The response `[wren, raven, goose]` maps to 2.50 and earns 5.00 on a five-point native scale. The map operator independently processes `[raven, raven, wren]` as 3.00 before clipping to 2.50. An unmapped identifier contributes -0.25 before the lower bound produces 0. A declared score range of zero width blocks publication. With a nonzero minimum, require approved zero-based or range-normalized scaling since the mappings can assign different points.

For QTI-C, a section draws two item references from three eligible slots without replacement. A historic attempt records ordered slots `[S3,S1]` and sequence revision 8. Replay requires those slots, pinned item versions and original choice order. A new native attempt can draw another allowed combination. A recovered section size alone gives no proof about a prior candidate's draw.

## 09.5 Assessment hierarchy, export and accessibility

Convert AssessmentTest to an AssessmentVersion with test-part and nested section scopes. Persist each reference as an AssessmentSlot with source reference key, ItemVersion, weight, parent section, position, mandatory flag and supported time and attempt policy. Resolve navigation and submission modes independently. Branching, skipping, replacement, section ordering, item session controls, variable mappings and test outcome processing each require an enabled capability. Preserve unreproduced policy in provenance.

For fixed linear export, write the manifest and QTI files with deterministic ordering, stable identifiers and required resource dependencies. Keep IDs across exports of the same logical item. Emit only selected languages and approved assets. Compare a re-import into empty staging against the expected graph, rendered prompts and independent score vectors. Exact bytes verify repeat exports of an unchanged native revision. A converted package requires semantic parity.

Sanitize MathML and preserve the source AST or authorized alternative text when required. A rendered equation and an algebraic marking rule are separate capabilities. Portable custom interactions require a separate vetted runtime. Export blocks unsupported interactive behavior unless an editor creates a reviewed alternate assessment under a new version.

The staging UI offers structure, item mapping, behavior, assets, accessibility and parity views. Provide a candidate preview with the live keyboard sequence and focus management and a restricted grader preview with answers and condition traces. Both views show the source locator and revision. Announce asynchronous progress and completion in an accessible status region. Editors remedy content issues. Assessment approvers authorize changed scoring and accessibility behavior before release.

## 09.6 Common Cartridge resource and placement conversion

The pinned manifest profile determines resource vocabulary and dependency structure. Cartridge transfer preserves supported curriculum structure, resources and metadata. Embedded assessment, playback or tool resources enter their own adapters.

| Cartridge resource | Draft model | Review condition |
| --- | --- | --- |
| Organization, item and title | CourseVersion with ordered ContentPlacement tree and source IDs | Missing default organization, duplicate placement, invalid type or illegal dependency |
| Bundled web content and attachments | ContentNodeVersion, typed blocks and AssetVersion | Unsanitized script, remote path, broken fragment or absent required asset |
| Web link | External-resource content block with approved destination | Unknown origin, expired access or unsafe scheme |
| Supported LTI descriptor | Inert tool resource candidate with launch URL and metadata | Missing approved deployment, legacy-only target or credentials in the artifact |
| Discussion prompt | Native discussion activity draft with instructions and provider capability | Missing integration or mismatched access and scoring |
| Assessment and question bank | Item and Assessment import through the embedded QTI profile | Unknown edition, scoring mismatch or disabled interaction |
| Metadata and alignment | Preserve source vocabulary, level, catalog and locale with scoped mapping | Unknown institutional vocabulary, unsupported required alignment or rights issue |

Build the ordered placement tree by traversing organization items. Traverse resource dependencies independently, cache one staged asset or node per resource identity and preserve the selected organization and all accepted alternative trees. Two occurrences of one resource can share a content version and maintain distinct placement identity, access and analytics. Classify included resources outside the tree as unplaced. Missing required dependencies block affected placements and produce traceable issues.

A full cartridge can carry local assets and references. A Thin profile primarily conveys links and metadata. Mark remote dependencies and connection requirements. Do not fetch arbitrary URLs during import. A later LTI binding uses the registered deployment instead of any secret from the archive. A broken connection leaves the placement in a review state with accessible explanation.

For CC-A, O1 contains two placements of R1 and one of R2. R1 depends on image I1. R2 is a tool link without a deployment. Import creates three placements, one shared content version for R1, one image AssetVersion and one inactive candidate for R2. Binding R2 does not change R1 or enrollments. Removing the image blocks both R1 placements and reports the dependency once with two affected occurrences.

## 09.7 Interface, errors and conformance gates

The generic transfer API owns the job. The following request starts an authorized dry run.

```json
{
  "artifactId": "c58c515d-932d-45c7-aae6-7cedfd150d22",
  "profileKey": "qti-3.0.1-item-linear",
  "profileRevision": 4,
  "destinationId": "5f00b873-27a6-4d97-a989-73df0dbd217b",
  "mode": "dry_run",
  "unsupportedFeaturePolicy": "block_affected_records"
}
```

Require an idempotency key for job creation and bind it to Institution, actor and request digest. A repeat returns the same job. Different content with that key returns 409. Polling returns job state, aggregate dispositions and a bounded issue cursor. Publication compares the approved staging digest and current destination revision. A change since approval requires fresh review. Issue codes distinguish `PACKAGE_SCHEMA_MISMATCH`, `QTI_UNBOUND_RESPONSE`, `QTI_UNKNOWN_TEMPLATE`, `QTI_UNSUPPORTED_OPERATOR`, `QTI_PARITY_FAILED`, `CARTRIDGE_DEPENDENCY_MISSING`, `CARTRIDGE_TOOL_UNBOUND` and `ASSET_RIGHTS_REVIEW`. Protocol-specific error responses retain normative media types.

Acceptance fixtures verify inbound parsing, accessible presentation, answer permissions, deterministic export, malformed archives, unsupported-feature reporting and grade equivalence. Keep tests for source policies beyond the claimed subset. Formal results exchange and conformance belong to separate profiles and evidence.

- [1EdTech QTI specification index and versioned bindings](https://www.1edtech.org/standards/qti/index)
- [1EdTech QTI 3.0.1 Assessment, Section and Item Information Model](https://www.imsglobal.org/sites/default/files/spec/qti/v3/info/imsqti_asi_v3p0p1_infomodel_v1p0.html)
- [1EdTech QTI 3 Results Reporting](https://developers.imsglobal.org/sites/default/files/spec/qti/v3/rr-bind/index.html)
- [1EdTech Common Cartridge profiles](https://www.1edtech.org/standards/cc)
- [1EdTech Common Cartridge 1.3 implementation profile](https://www.imsglobal.org/cc/ccv1p3/imscc_Implementation-v1p3.html)
- [1EdTech Common Cartridge 1.4 implementation guide](https://www.imsglobal.org/node/167531)
