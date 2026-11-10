# 02. Agent curriculum production

Use a restricted authoring principal and the same owner commands used by staff. The agent proposes a source-grounded curriculum package in a staged run. Teachers review it in the native editor. The agent cannot publish courses, release marks, change an active offering, approve a source's rights, or supply missing institutional policy.

## 2.1 Run inputs and outputs

| Input | Required contract |
| --- | --- |
| Purpose and target | Exact institution, owning unit, target CourseDraft and expected revision, use mode, audience, locale and request owner |
| Source set | Ordered approved AssetVersions, pinned extraction runs and permitted physical page ranges |
| Teaching brief | Grade or proficiency band, audience prerequisites, learning time budget, objectives where supplied, teaching mode, target question families and adaptation limits |
| Assessment policy | Formative or summative, item count or blueprint constraints, permitted marking methods and accessibility alternatives |
| Data authority | Allowed provider, rights snapshot, disclosure policy, model input limits and expiry |
| Export policy | The delivery action preselects verified SCORM 2004 fourth edition; an explicit supported override is separately validated. Keep editable native backup as its own action, with independent rights, disclosure and fidelity checks |

The authoring job records agent principal, tool versions, model or provider release, schema version, generation parameters, authorized input digests, extraction versions, stage manifest digests and accountable reviewer. A generated output can vary when the model is rerun. Replaying a command returns its sealed prior result. Re-execution as a new candidate revision records its own provenance. Persist the prompt template version and typed user brief. Limit persistence of raw prompts and model logs to the applicable data policy.

Stages use the [task contract](authoring-task.schema.json). Tools can read only the whitelisted extraction runs and exact regions. A request declares stage, effect key and expected run revision. It can reference an earlier sealed manifest by StorageObject ID and digest. Tool responses return typed state, exact result IDs, safe diagnostic codes and durable receipt. Protected content is fetched separately through authorized storage. Do not send entire documents to a remote agent when the approved brief needs only selected regions.

## 2.2 Claim and derivation discipline

| Classification | Meaning | Required evidence |
| --- | --- | --- |
| Extracted | Direct transcription of authorized source wording, value, mathematical symbol, figure or table | Exact SourceRegion, accepted transcription and rights for the planned use |
| Source-supported paraphrase | Rewritten fact with the same proposition and no added premise | One or more exact regions and review that meaning, qualifications and units survived |
| Derived | New result computed from source values or rules using a declared derivation | Exact premise regions, formula or derivation recipe, units, domain and independent verification |
| Generated instructional material | Original objective, transition, example, quiz stem or distractor created for this teaching purpose | Approved adaptation authority and explicit generated label. Record relevant supporting concept regions where used and verify all material assertions |
| Human supplied | Teacher contributes missing knowledge or editorial choice under their own authority | Identified decision and source when applicable, with independent review for consequential grading |
| Unresolved | Missing, ambiguous, conflicting, out of range or unauthorized evidence | Stable issue code and exact blocked candidate path. Remains unpublishable where material |

Create lineage at material claim or block granularity, down to a table cell, answer key or mathematical expression where needed. A claim can refer to multiple regions. An objective can be an editorial instructional decision while its prerequisites or underlying facts are source-supported. Source references for a distractor show which misconception or transformation inspired it, never that the incorrect distractor is a source fact. The final native objects link to exact protected evidence. Learner output uses permitted attribution and safe citations without exposing source storage or staff answers.

A draft task can request more evidence or an instructor decision. A generated plausibility guess cannot fill a missing correct answer, contradictory source value, undefined variable, inaccessible image or unknown rounding rule. Withhold that scored item or replace it with a new approved item whose inputs and valid responses are independently complete. A novel exercise may choose explicitly fictional parameters under allowed adaptation. Its computed answer requires the same independent verification as a source-derived result. It is identified as generated in review.

## 2.3 Ordered stage workflow

| Stage | Input and operation | Sealed output and progress gate |
| --- | --- | --- |
| Plan coverage | Read accepted source and teaching brief. List topics, prerequisites, terms, worked examples, holes and possible objectives | Source coverage map, measurable outcomes and estimated time. Human confirms audience and exclusions before costly generation |
| Plan course | Arrange modules, optional topics and lessons. Link objectives to explanation, worked example, practice, assessment and remediation where applicable | Ordered outline with candidate stable keys, estimated minutes, requiredness, lesson inventory, language coverage and proposed placement gates |
| Produce learning blocks | Create typed rich text, headings, math, safe images, table or document references, accessible alternatives and internal navigation | Candidate definitions, source derivation links and dependency closure. Unsupported assets stay staged as issues |
| Produce assessment | Build a blueprint and items with response kind, correct outcomes, distractors, scoring and remediation | Candidate item, expected response and marking rule proposals, worked solutions, rationale and grade test vectors |
| Verify candidates | Validate registered schemas, rendered preview, rights and provenance, gate graph and assessment evaluator vectors | Validation report with blocking errors, advisory issues, exact object paths and actionable owner |
| Stage owner commands | Resolve selected candidate IDs and compute a deterministic dependency order, target expected revisions and change diff | Apply plan and digest covering proposed authoring commands and sealed dependencies. Draft remains unchanged until approved apply |
| Apply reviewed selection | Curriculum and Assessment owner commands commit authorized selected drafts and references | Per-domain receipts and exact version mapping. Incomplete cross-domain candidates remain staged, with no offering activation |
| Review and export | Follow independent item, assessment, curriculum and export checks | Exact native publication and the requested editable or independently approved delivery exports |

A planning row for each lesson includes a stable candidate key, source links, objective IDs, audience and prerequisites, estimated duration, explanation blocks, practice items, assessed objectives, accessibility needs and unresolved evidence. Use bounded objectives with observable verbs and a criterion when a real standard or brief supplies one. For example, convert two whole minutes into seconds using the defined relationship, with an exact integer response. Avoid claiming institutional mastery level or credit value unless authorized.

Every required objective needs at least one teaching opportunity and one appropriate form of evidence, or an explicit human-approved exclusion. Practice can interleave worked examples with learner problems and gradually remove scaffolding. Record coverage rather than inflating item count. Use the [practice guide on organizing instruction](https://ies.ed.gov/ncee/wwc/PracticeGuide/1) as one input to the pedagogy profile.

## 2.4 Assessment production rules

1. Start from an objective and intended evidence. Choose an existing supported response type such as single choice, multiple response, exact numeric, numeric with unit, mathematical expression, multipart or rubric-reviewed open response. Unsupported behavior stays an issue.
2. Define the candidate-visible instructions and grading scope. State units, precision, rounding, response format and domain when they affect correctness. Use precise learner language and accessible math rendering. Do not add decorative complexity that changes the skill being measured.
3. Generate the correct response, evaluation rule and human-readable worked solution separately. Classify each as extracted, derived, generated or human supplied. The expected answer must have a complete evidence path. A worked solution should include the decisive steps and common misconception feedback.
4. For selected-response items create a stable option ID per choice. Every distractor needs a plausible misconception and evidence it fails the key under the exact rule. Check duplicates after Unicode, numeric and mathematical normalization. For multiple selection verify every scored subset policy, treatment of empty response and maximum points.
5. For numeric items store exact decimal, rational or integer target and separately declared tolerance when authorized. Specify absolute or relative formula, inclusive boundaries, near-zero behavior, valid units and scale. A tolerance rule cannot widen acceptance silently. Test exact, equivalent, boundary, beyond boundary, wrong unit, blank, malformed and out-of-domain responses.
6. For symbolic items pin evaluator release, allowed grammar and equivalence mode. Verify domain, excluded points and multiple accepted forms. A string that renders correctly can still be outside the supported evaluation grammar. Reject untrusted source code, scripts and evaluator instructions as input data. Use the [mathematics evaluator specification](../assessment/03-math-evaluators.md).
7. For parameterized items verify deterministic generator version, constraints, answer evaluator and chosen seed policy. Test boundary seeds and a fixed published fixture set. Reject any invalid seed, non-unique option set, undefined denominator, impossible value or contradictory key. Use manual review for equivalence or nuance beyond supported evaluator assurance.
8. For open responses pin a rubric with observable criteria and anchors. Preserve distinctions between manual marking, deterministic autograding and practice-only feedback. A generative language model can propose a rubric or reviewer note. It does not become the official evaluator for consequential work under the default profile.

The content production manifest stores exact prompt, choices, expected response, explanation, evaluator fixture set and provenance as staff-only assets or Assessment draft payloads. It exposes only safe item identifiers and validation summaries to the broader authoring dashboard. A learner or export profile receives answer keys only where its specific audience and release policy permit them.

## 2.5 Owner command mapping

| Task or approved action | Owning contracts | Commit boundary |
| --- | --- | --- |
| Reserve and verify source asset | Platform `ReserveStorageUpload`, `FinalizeStorageUpload`, `RecordStorageScan`. Curriculum `ReserveCurriculumSource`, `FinalizeAssetUpload`, `RecordAssetScan`, `AuthorizeCurriculumSourceUsage` | Storage and asset owners use their own guarded receipts |
| Assemble lessons and media | `CreateContentNode`, `SealContentNodeVersion`, `SealLearningRuleVersion`, `CreateActivity`, `SealActivityVersion` | Every definition and dependency is exact and immutable when sealed |
| Apply course outline | `CreateCourseDraft` and `MutateDraftOutline` with current revision and ordered operation list | One draft transaction per selected bounded mutation batch |
| Build question and marking candidates | `CreateItemDraft`, `SaveItemDraft`, `SaveItemTranslation`, `SubmitItemForReview`, `ReviewItemVersion`, `ApproveMarkingRule`, `PublishItemVersion` | Agents can stage drafts. Authorized humans own review and publication |
| Assemble assessment | `CreateAssessmentDraft`, `SaveAssessmentDraft`, `ReviewAssessmentAssembly`, `PublishAssessmentVersion` | Published item and marking rule versions are pinned by the published assessment definition |
| Validate and publish course | `ValidateCourseDraft`, `PreviewCourseDraft`, `SubmitCourseDraft`, `DecideCourseDraft`, `PublishCourseVersion` | Approval and publication bind exact draft, dependency and validation digests |
| Export | Interoperability `QueueCurriculumExport` and exact target-profile validation | Editable native and delivery export artifacts each get a separate manifest and report |

An outline may retain an unresolved assessment dependency while staged. It becomes an exact activity binding only when the owning assessment publication is available. Never mint untracked item or asset versions to bypass owner commands. A late item review result leaves course apply waiting for that exact dependency. Agent-produced native draft and export stages do not assign grades or create official learner attempts.

## 2.6 Tool transaction and resume rules

The coordinator persists stage input fingerprint, expected run revision, stage state, covered pages or candidates, approved prior receipt, attempt count, lease owner and expiry, and exact output manifest digest. An operator may retry a transient failure, request a new candidate revision or cancel future stages. Cancelling a run preserves accepted owner writes and review history. Undo is a reviewed draft revision or owner correction.

A per-target stable operation key derives from run ID, stage, candidate ID, effect kind and exact input digest. A repeated worker claim uses the same effect key. Side effects call the destination owner's normal idempotent commands. If the coordinator times out after an owner commits, reconcile the durable receipt before retry. A stale expected draft revision returns a conflict with the safe changed paths. Generate a rebase or merge plan and require review for any substantive conflict. Dependency order is source and rights, plans, typed definitions, assessment item approvals, assessment publication, activity bindings, placements, course review and publication, then export.

Applying a large staged set can require multiple owner transactions. Each independently committed step records exact receipt. A dependency failure prevents subsequent dependent writes, but earlier approved draft objects remain staged and inspectable. The coordinator cannot publish on its own or mark a partial batch fully applied. Show complete, blocked, retryable and not attempted outcomes separately. Keep the offering unchanged until Participation activation is explicitly authorized.

See the [synthetic traceability fixture](synthetic-source-to-course.json) for one complete authoring decision and one blocked source item.
