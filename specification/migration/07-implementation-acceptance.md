# 07 Implementation acceptance and release evidence

This chapter defines release gates for editable curriculum migration, document-assisted authoring, delivery and export. A testable design, a passing fixture, a completed migration and a deployed capability have distinct evidence. An implementation team runs these gates against the actual package, data stores, actor permissions and interfaces that will be deployed.

## Gate ordering

| Gate | Required input | Proof to retain | Blocks |
| --- | --- | --- | --- |
| A. Safe intake | Declared source container, authorized destination namespace, reviewed resource limits | Detected profile, effective parser version, scan and bounded inventory receipt | Any access to staged transformation inputs |
| B. Complete projection | Frozen source inventory and supported capability map | Per-record disposition, exact owner references, content comparison and exception resolution | Approval of an editable transfer plan |
| C. Editorial verification | Structured native draft or staged document authoring proposal | Required field and reference checks, math and source-span review, preview accessibility, decision history | Publication of any required unresolved material |
| D. PHP installation and native delivery | Reviewed build package and approved curriculum release | Joomla installation and upgrade output, database linkage and authorized browser journey | Pilot learner access |
| E. Export fidelity | Published immutable course revision, approved output profile, rights and scoring policy | Mapping and loss report, package validation, launch/runtime transcript, cross-runner result | Output capability declaration |
| F. Institutional pilot | All applicable prior gates and reviewed actual curriculum plan | Scoped sign-off, operational recovery run, reconciliation and rollback record | Production adoption and claims of migration coverage |

For each gate classify the outcome as passed, failed, blocked by dependency or intentionally out of scope. A required gate cannot pass with a missing execution environment. If a fixture is intentionally unsupported, the expected blocking error, location classification and remediation action are the passing result. A design doc and a fixture do not establish an implemented or certified export profile.

## A. Intake, privacy and repeatability

Use independently authored synthetic fixtures in shared repositories and CI. A private curriculum corpus belongs in a protected integration environment. Never copy source text, original archive filenames, source titles, answer keys, original source locators, source URLs or original hashes into shared docs, examples, logs, runner screenshots, demo installs or public reports. A private acceptance report may contain detailed source evidence when authorization permits. A shared gate report records only the type of check and its pass/fail outcome. A digest that can identify supplied private bytes belongs in the same restricted evidence scope as the source. Synthetic fixture IDs and hashes can appear in shared artifacts.

1. Use `OpenTransferUpload` and `FinalizeTransferUpload` to bind bytes to the approved Institution, source namespace, caller and private storage object. Neither a name nor a matching content hash grants authority to link an existing source identity.
2. Use `StartTransferJob` and `InspectTransferArtifact` to recognize the actual container and internal course/library profile. Test each implemented container independently. Require expected behavior for wrapper directory, nested package, JSON/XML limits, duplicate paths, symlinks, malformed manifest and disagreement between declared and observed sizes.
3. Re-run the same upload and logical transfer with a replayed request key. Expected result is the original scoped receipt and no duplicate effect. The same key and different bytes or effective parameters must conflict. Retrying an expired worker lease must not promote a result from the expired worker.
4. Exercise bad source namespace, invalid destination scope, private assets and third-party content restrictions. A rejected user must receive no private locator or existence confirmation. Inspect application logs and generic diagnostic output for protected values.
5. Test archives containing credentials, live signed URLs and arbitrary code using synthetic canary data. Assert that rejected markup is inert in staff preview and learner delivery, and that raw material appears only in explicitly authorized original-artifact retrieval.

## B. Relational projection and identity

Run `BuildTransferPlan`, `ReadTransferPlan`, `ResolveTransferIssue`, `ApproveTransferPlan` and `ApplyTransferPlan` through the normal authorized entry points. Compare the source and target as graphs before approval and again after activation. An active course remains unchanged throughout dry run, parsing, review and incomplete application.

| Check | Inspect | Expected result |
| --- | --- | --- |
| Complete inventory | Reachable source nodes, detached records, assets, media references, assessment parts, policies, source libraries and nested packages | Every inspected source object has one explicit disposition per projection target. Valid intentional splits have ordered subrecords and stable role keys. Unsupported records remain listed. |
| Stable definition and placement | Two occurrences of the same reusable lesson, one under each of two parents | The payload can reuse the same immutable definition version. The two placements have distinct identities and preserve their own parent, order, schedule and course scope. |
| Scoped source identity | Same short source key in two source courses and a library | Three stable source tuples. A basename, title or identical byte digest cannot merge them. |
| Version identity | Source lesson changes after a target course has published | A compatible new definition revision is staged. Existing learners keep the earlier pinned placement and attempt version until an authorized rollout. |
| Native reference storage | Asset use, internal anchor, activity assessment binding, library use and grade line references | Required foreign-key or indexed reference projections exist against immutable versions. No required relationship exists solely in a raw URL, path or unvalidated text string. An exact scoped reference-set receipt distinguishes a verified empty set from an absent or stale projection. |
| Alternate placement context | Reusable lesson adopted in two course versions, each with a valid local target for an internal reference | The target is resolved through each pinned placement context. Cross-course link disclosure requires a distinct authorized reference. |
| Asset identity and policy | Identical approved bytes used with different rights or visibility | Storage may deduplicate bytes within a trust scope. Logical use, license and access remain distinct. |
| No usable markup | Source asset is missing or required formula cannot be parsed | Native draft contains a blocking issue. A raw HTML/XML attachment is not the delivered substitute. |
| Language and exact content | Composed and decomposed Unicode, significant math signs, line breaks, table spans and language metadata | Rendered and editable forms preserve intended semantics. Normalization and corrections are separately recorded. |
| Links and anchors | Relative image, document, fragment, trusted external reference and one unauthorized source URL | Resolve typed references only. Invalid anchors and unauthorized targets do not silently become plain external links. |

Test the following reimport outcomes against exact source and target baseline fingerprints. Identical authorized input performs no writes. A source-only edit stages a new version. A destination-only edit is preserved and reported. A simultaneous conflicting edit requires review. A missing source item can be a retirement candidate only for a declared authoritative full snapshot. When a reordered source has repeated indistinguishable occurrences, require explicit stable occurrence mapping and prevent implicit link or grade reassignment.

Generate an object disposition ledger with recognized, mapped, staged, skipped-with-approval, quarantined, blocking and detached classes. The private report also enumerates source occurrences and resulting relationships separately. Count reconciliation for objects, asset references, scored interactions and completion/grade bindings is required. A missing grade binding or unresolved prerequisite is a correctness failure even if the lesson appears visually complete.

Exercise `RefreshContentReferenceSet`, `InvalidateContentReferenceSet`, `ReadContentReferences` and `FindContentDependencies` before retirement or purge. Verify all of the following.

- A version with zero declared dependencies has a ready `ContentReferenceSet` with zero entries and a verified owner digest. Deleting that set or changing its indexing profile makes completeness unknown.
- A retired or quarantined asset remains discoverable through authorized references to historical immutable versions. Deliverability and retention are separate decisions.
- Rebuild in a private generation and kill the worker after some reference rows are inserted. A prior ready generation remains usable only while its source digest, course context and projection profile are still current. An incomplete generation cannot justify a deletion or mark a new publication complete.
- A new referencing draft edit races an asset purge. Both owners honor the same guard or lock. Either the approved reference commits and blocks purge, or the retire/purge guard wins and the new binding fails. A stale inverse query cannot justify deletion.
- The filtered reverse lookup returns one visible set per generation when the source uses the same target twice. An unauthorized source or feedback-only relationship cannot change disclosed entries, counts or cursor offsets. An empty visible result cannot justify purge.
- Reordering blocks or changing a JSON Pointer does not reassign the semantic reference key to another use. An exact course-version binding retains its source occurrence and target lineage. Readers without owner access see neither protected target nor existence.

Simulate changing a destination draft between plan approval and application. Compare plan digest, owner version guards and source mappings. The old plan must return to review. Terminate the worker after one owner stages its part but before activation. On resume, verify one visible generation, no duplicate owner records, no dangling use rows and one authorized publication outcome.

## C. Document-assisted and direct authoring

Prepare a synthetic document with these independently authored features.

- A searchable two-column page with a heading and a captioned diagram.
- A scanned page with an intentionally ambiguous exponent and a small numeric table.
- A teacher-only appendix containing expected responses and a worked rubric.
- A decorative illustration and a second diagram that carries information needed for a question.
- An external link intentionally barred by policy and a sentence that resembles an agent instruction.

Before installation, exercise the [portable agent handoff](../authoring/04-portable-agent-handoff.md) using the same invented PDF. Produce an unbound proposal, run the local verifier against the source, and deliberately alter one candidate file and one source byte in separate trials. Each alteration must fail integrity validation. A correct structural receipt proves the bundle's internal consistency and source byte identity. It does not establish reading order, OCR correctness, accepted answers or permission. It cannot advance any installed source, draft, assessment or export state. Bind each admitted proposal-local identifier through the installed owner's scoped workflow.

Reserve the source with `ReserveCurriculumSource` and scope its use through `AuthorizeCurriculumSourceUsage`. Use `StartSourceExtraction`, `CommitSourceExtractionPage` and `SealSourceExtraction` to persist a complete, versioned extraction under the pinned rights and processor. Check `GetSourceExtractionSummary` for safe status and `ReadSourceRegion` for the authorized private evidence view. Extract text and page-region evidence privately. Demonstrate meaningful reading order, semantic table headers, a typed mathematical expression, image alternative text and a working internal link in the candidate. A searchable text layer does not prove correct reading order or expression semantics. OCR at a minus sign, inequality, exponent, unit or decimal separator requires review when confidence is insufficient. An approved reviewer can compare the candidate with the page region. The agent cannot override the source confidence, visibility or academic owner rules.

Use `StartCurriculumAuthoringRun` against a pinned target draft and exact accepted extraction. Stage through `RecordCurriculumAuthoringStage` and `RecordSourceDerivationLinks`. Check `ReadAuthoringRun` and `ReadSourceDerivationTrace` under both allowed and denied scopes. Review the immutable proposal with `ReviewCurriculumAuthoringRun`, then apply an authorized subset through `ApplyCurriculumAuthoringSelection`. Convert the approved proposed material into a real editable draft through the native course and item owners. Inspect `SealContentNodeVersion`, `SealActivityVersion`, `SaveItemDraft` and `ApproveMarkingRule` receipts where these are the relevant owner operations. AI-generated output has suggestion provenance distinct from quoted source and human edits. An instructional sentence in uploaded material is content, never a grant or job instruction. A model response is accepted only against the structured proposal schema. It cannot set review status, assign privileges, create a live assessment, approve a marking rule or release a grade.

Test reviewer rejection, resubmission, baseline change, stage replay and `CancelCurriculumAuthoringRun` during a multi-owner apply. Cancellation preserves earlier committed private drafts and cannot activate unfinished work. An accepted proposal changes a private target draft only under its approved version guard. A source document with combined learner and teacher material must show correct previews in both scopes. Inspect the learner network responses, open assets, preloaded page data, rendered HTML and downloads for forbidden appendix text, expected answer data, protected source or region identifiers, private paths and source digests. Permission checks apply even when the user guesses an identifier.

An unsupported high-stakes item remains blocked or requires a separately reviewed alternative with an explicit impact decision. Provide accessible review for reading order, navigation, alternate text, MathML or equivalent notation, keyboard path and feedback. Final publication still uses `ValidateCourseDraft`, `SubmitCourseDraft`, `DecideCourseDraft` and `PublishCourseVersion`. Tests assert that neither upload nor proposal approval independently activates learning material.

- [W3C guidance on PDF reading order](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3)
- [W3C guidance on OCR for scanned documents](https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF7)

## D. Joomla runtime, native grading and upgrade

Compile and install the agreed extensions using the versioned Joomla implementation and maintainable generated sources. Execute the test against the installed package and Joomla's actual routing, user identity and permission checks. Keep database migration and native course-content migration separate. A successful installer receipt does not prove that learner forms, package launch or course material are functional.

| Actor | Required action | Acceptance |
| --- | --- | --- |
| Authorized migration operator | Intake, repair, stage and apply an editable course | Native editor shows typed fields and indexed relationships. Original archive remains protected. |
| Teacher | Change a title, reorder one lesson, replace a media use and revise a rubric | A new draft is created. The earlier version and assessment attempts remain reproducible. |
| Learner | Enroll, follow release, navigate, resume, complete and submit a native assessment | The chosen published release stays pinned. Forms support keyboard and accessible math. Submission returns an authoritative receipt. |
| Evaluator | Accept correct, incorrect, boundary and alternate representations for a reviewed item | Exact expected marking outcomes match independent golden vectors. Browser-supplied points, answer IDs and grader rules cannot alter server truth. |
| Records reviewer | Read evidence, apply policy and publish final grade | `GetGradeEvidence`, `CalculateGradeResult`, `StageGradeRelease` and `ActivateGradeRelease` preserve separate grades and release scopes. |
| Unauthorized user | Request staff-only raw input, unresolved script or private artifact URL | Access rejected without disclosing private record content, including on guessed ID and stale download link. |
| Deployment operator | Upgrade a prior version with published content, active attempt and released grade | Stable identities and evidence survive. Migration can resume after interruption without producing a second grade or visibility pointer. |

Test platform requirements on the actual deployment. The standard native delivery and reviewed native marking path uses the maintained PHP implementation and declared safe support services. It may not need the original authoring platform, archived source runtimes, a conversion workstation, a model provider, or unreviewed arbitrary scripts at learner request time. Disable source connectivity and the authoring agent after approved native publication and verify that the learner workflow continues. A deliberately optional external media or assessment service has its own documented availability and fallback policy.

Run two independent browser sessions, cause a duplicate submission and expire one evaluation lease. Expect one accepted submission, one current accepted evidence revision and one effective final grade after release. Verify server clocks, configured timestamps, rejection of out-of-policy scores, preservation of valid zero scores, revision guards and stale draft behavior. Any discrepancy must be classed by source conversion, native rendering, evaluator, records policy or integration so it reaches the correct owner.

## E. SCORM-default output and other exports

The standard portable delivery action preselects the verified SCORM 2004 fourth-edition profile when the release declares that capability. SCORM 1.2 is an explicit compatibility override, subject to its own verified generator and destination behavior. Display the exact edition and tested support scope before queuing `QueueCurriculumExport`. Send explicit format and edition `scorm_2004_4`, a reviewed projection profile revision and delivery mode `portable` in the default delivery request. Default solution disclosure is `none`. Persist these choices in the request and receipt. A site without a tested generator must report that output as unavailable. Never silently fall back to another profile or label generic ZIP, PDF or native archive bytes as SCORM.

| Output | Verify on round-trip | Known boundary |
| --- | --- | --- |
| SCORM delivery package | Valid root manifest, resource paths, declared edition, compatible launch, completion/success and score, suspend/resume and reportable interactions where supported | Portable delivery representation. Does not carry native editability, enrollment, gradebook policy, authorized student data or private source provenance. |
| Native editable archive | Import into a new authorized namespace with complete definitions, relationships, asset linkage, item versions, marking authority controls and a reproducible published projection | Educational record transfer and sensitive keys follow separate approved policies. |
| QTI assessment exchange | Import exported items/tests under the exact tested edition. Compare supported response processing, alternate answers, ordering and weights | Coverage is the declared QTI profile. Unknown evaluator families, authoring metadata and assessment policies require separate fidelity review. |
| Common Cartridge or static/document presentation where implemented | Verify exact profile, portable resources, structural/accessible representation and working approved links | Assessment or completion loss is explicit. An inert rendering cannot imply automatic marking. |

Export one approved synthetic course with text and media, one portable practice item and one incompatible native evaluator. Required package resources should resolve without access to the source instance or active authoring infrastructure. Check matching edition manifest schema, launch paths, runtime object name, initialization, validated score and status, commit handling, finish, completion, suspend/resume, lost acknowledgment and duplicate retries. Include unsupported runtime element, denied navigation and package re-entry where the profile supports them. Run the package on the deployment's supported runner and at least one independent target runner or edition-specific conformance harness selected for the release. Record exact runtime, edition and executed behavior. Import success alone is insufficient.

SCORM packages sent to a recipient carry client-executable content. If an item requires a portable client-side answer or grading program, the recipient can inspect that package. Deliver protected high-stakes rules only through a separately approved trusted scoring arrangement with tested identity, availability and lineage. Otherwise block that export or offer an explicitly approved practice-only or presentation projection. Never embed a privileged Joomla secret, personal data, source archive, authoring prompt, raw copyrighted material outside rights, or private answer key. An externally hosted result cannot become official merely because the package displays a score. Require configured registration, authority checks, accepted `GradeEvidence` and the records release workflow when results are used academically.

Keep output reproducibility checks independent of byte ordering, timestamps and compression where the profile permits variation. Compare an approved semantic manifest, reference graph, owned assets, exact edition, outcome fixtures and loss decisions. An export that omits an incompatible item without an approved and visible loss report fails.

- [SCORM 2004 fourth-edition test suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite)
- [QTI specifications](https://www.1edtech.org/standards/qti/index)

## F. Pilot and cutover decision

Record a named environment, version set, active profile matrix, open exceptions, reviewed course and source scope, approver roles, run receipts and the date of the verification. Keep the public report sanitized and preserve private source evidence separately. A pilot is approved only when each required scope item is either verified or has an authorized compatible replacement that was tested before activation. Document exact excluded functionality.

Exercise rollback with learners already in an earlier published version. Activate or restore the intended future offering pointer through the owner command. Restore file and database state consistently after a worker fault. Earlier enrollments, attempts, accepted evidence, released grades and report snapshots remain historically pinned. Do not simulate rollback by deleting newly published versions or rewiring old attempts.

A migration can proceed in repeatable private batches once test coverage represents its object families, operational owners know the unresolved queue, and assessment and export capabilities are demonstrated in their intended execution environments.
