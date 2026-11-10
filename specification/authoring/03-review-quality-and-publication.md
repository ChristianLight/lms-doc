# 03. Review, quality gates and publication

The review workflow turns staged source-grounded proposals into institutional course content through the existing owner commands. It keeps evidence, reasons, grading assurance and distribution rights pinned to each accepted revision.

## 3.1 Review workspaces and authority

| Workspace | Reviewer work and permission | Blocked and retry behavior |
| --- | --- | --- |
| Source and rights | Inspect exact page crops and detected reading order against original render. Confirm selected scope, redactions, text, figure rights, OCR uncertainty and permitted source or derivative use | A missing page, uncertain sign, unapproved third-party asset or unauthorized use becomes a tracked issue. Review other independent material |
| Course plan | Check audience, prerequisites, objective coverage, sequencing, estimated effort and accessibility. Compare source coverage to adaptations and exclusions | Revise plan with a new stage result. Show downstream candidates that need regeneration or renewed review |
| Item and answer review | Inspect each scored item, correct response, rationale, distractors, rubrics and tests under a separate Assessment capability | Incomplete key, disputed rule, unsupported grader or untested precision boundary blocks that item. Accept only independently supported replacements |
| Candidate change review | Compare protected provenance and before/after draft with exact dependency list. Select whole or closed subset. Review generated vs source-supported labels and edit conflict | Independent accepted content can stay staged. A stale draft revision invalidates prior apply approval |
| Learner preview | Render lesson, math, captions, documents and keyboard interactions as a synthetic learner, across locale and relevant authorization profiles | Never starts official attempts. Missing accessible route or source leakage blocks the affected profile |
| Publication and export | Check exact approved course revision, supported asset use, profile-specific distribution rights and downgrade report | Keep publication and export separate. Unsupported profiles are blocked or require approved safe degradation |

The authoring approver must be a human principal independent of the generating agent. Under the default scored-item policy an assessment author cannot approve their own consequential key or marking rule. Source reviewers, curriculum publishers and assessment reviewers can be the same staff member only where their roles and institutional independence policies permit. Rights reviewers need permission to inspect the source and license evidence. Broad teaching or preview authority alone grants no raw source, prompt, answer-key or legal evidence access.

## 3.2 Validation gate matrix

| Gate | Blocking conditions | Verified evidence |
| --- | --- | --- |
| Custody and rights | Unsupported file, wrong digest, source hidden from task scope, revoked authority, unreviewed disclosure, required policy violation | Exact AssetVersion, verified Platform object, rights attestation, approved handling purpose |
| Provenance and extraction | Consequential fact has no exact accepted source, unsupported derivation, conflicting source readings, unreviewed equation or unavailable required page | Region and extraction run IDs, physical page and rectangle, extraction method, reviewed text or rendering digest |
| Content | Invalid typed payload, orphan placements, circular prerequisites, broken links or missing required locale | Content schema and manifest validator, exact draft diff and dependency report |
| Accessibility | Meaningful image without alternative, unreadable math, broken keyboard controls, unsupported learner PDF or missing required accessible equivalent | Accessible render checks, captions or transcript, manually reviewed sample and exception receipt |
| Assessment | Key missing or ambiguous, item misaligned to objective, defensible distractor marked wrong, unauthorized grading method, hidden data leak | Approved item and marking rule version, evaluator release and deterministic fixture report |
| Publication | Approval refers to different input, open blocking issue, withdrawal, concurrent author change, prior result invalidated | Sealed dependency digest, current draft revision and separate approving principal |
| Export | Unauthorized audience, package contains staff source or answer data, missing required behavior or target profile fails validation | Exact publication and manifest, output capability report, zip safety, profile conformance and target test result |

Warnings describe real risk and safe editorial options. A warning can be accepted only by the appropriate authorized reviewer, with rationale and exact candidate revision. Required missing source or correctness proof is blocking. An unresolved scored question cannot be published as summative or credited practice. A reviewer may remove it, obtain better source, supply reviewed authority or approve a different fully verifiable generated item. Preserve the decision record. A learner-facing public copy of the source may require a separate accessibility and distribution review even if the original was usable for private extraction.

## 3.3 Scored-item verification procedure

1. Render the learner item without answer material. Independently solve it using only the learner prompt and its authorized assets. Compare the independent answer to expected response and source premise.
2. Run the exact registered evaluator on frozen fixture responses under the same normalization, domain, seed, unit and precision rules as delivery. Require valid scores within bounds and reproducible diagnostics. Manual items require reviewer calibration rather than automatic score fixtures.
3. Verify expected score, correctness state and allowed feedback for every fixture. Separate blank, invalid and incorrect. Record evaluator version, canonical fixture digest, rule digest, observed result digest and authorized decision.
4. Run boundary and adversarial vectors appropriate to the type. Selected-response tests include every single choice and ambiguous wording. Exact numeric tests include meaningful equivalent formatting and wrong unit where applicable. Symbolic tests include domain restrictions, grammar edges, valid alternate forms and unsafe input. Parameterized tests include fixed seeds and known boundary seeds.
5. Verify that staff-only answer keys, solution drafts, source evidence, unsafe assets and diagnostic data do not appear in learner HTML, preview without permission, exports for a learner audience, logs, public API errors or data bundled into the browser. Approved feedback follows Assessment release rules.
6. If any verification fails, record exact blocker and leave affected item unapproved. A rule or evaluator change invalidates the fixture evidence for that revision and reruns independent review.

A model may propose alternative accepted answers. Only deterministic evaluator evidence or an authorized human scoring policy can accept them for consequential marking. Validate [candidate interactions](../assessment/02-interactions-and-rendering.md), [math evaluator rules](../assessment/03-math-evaluators.md) and [assessment verification](../assessment/11-verification-and-golden-vectors.md).

## 3.4 Publication and independent export

Apply only the reviewed candidate subset and exact stage digest. Require dependency closure and matching draft version. Links from an immutable target version refer to source region and candidate lineage without including raw source in the native learning body. Attach exact source derivation links using the existing owner operation receipt and accepted candidate digest. A source correction produces a later extraction run and candidate review. It does not rewrite published evidence or historical attempts.

Publish the reviewed assessment dependencies first, then pin their exact versions in native activity definitions. Submit and review the whole draft. Revalidate exact permissions, safety, source rights, locale, assessment dependencies, required visibility and expected revision. Commit the immutable course version. The authoring job has no permission to activate offerings. Reuse the standard [publication and rollout contract](../curriculum/03-publication-and-rollout.md).

The canonical authoring result is the approved native curriculum. An editable export uses the platform-neutral [native archive profile](../interoperability/01-format-profiles-and-native-archive.md). A portable delivery request separately targets tested SCORM 2004 fourth edition by default, subject to profile capability and review. It carries eligible structural IDs, versions, content and assets according to audience and rights. Internal authoring provenance can be retained in a separate protected record or explicitly authorized administrative profile. Default exclude original source PDFs, OCR text, page overlays, internal prompts, review notes and staff-only grading keys from learner distribution.

Generate SCORM, QTI or another target independently from the exact approved canonical release or authorized transfer snapshot. Each export has its own profile, entitlement and supported capabilities, manifest checksum, validation and degradation report. A SCORM output can deliver supported content and completion behavior through its runtime. It cannot claim to preserve native server-only answer confidentiality if the conversion includes browser-accessible scoring code or keys. Where those semantics cannot be preserved, use an approved content-only export, an explicitly authorized external activity boundary or reject that target profile. Never weaken the canonical course to fit a portable format. Validate target roundtrip where import is supported and run edition-specific runtime acceptance for SCORM.

## 3.5 Version and incident cases

| Trigger | Required behavior |
| --- | --- |
| Source page replaces a figure or corrects a numerical example | New source version and extraction. Find linked candidate and published versions with reverse provenance, create scoped diff and review only affected claims |
| Reviewer approves candidate revision 4 while agent seals revision 5 | Old approval stays recorded but cannot apply to revision 5. A stale revision fails with an actionable conflict |
| Asset rights revoked after an export was queued | Export worker rechecks current authority before delivery. Mark affected references and preserve previously issued artifact history under policy |
| Export supports content but fails a native symbolic evaluator | Report unsupported grading profile. No silent conversion to lenient string comparison or issuance of false compatibility result |
| Source document lacks a stated answer or required input | Block scored candidate, show exact region and missing item. Continue with independently complete approved content |
| User requests resume after lease expiry | Reconcile existing exact receipts and claim a new fence. A former worker cannot overwrite accepted candidate results |
| Teacher elects to expose a learner reading | Reserve a learner asset revision with permitted usage and reviewed accessible output. Link it in a native lesson through normal publication |

The [synthetic source-to-course fixture](synthetic-source-to-course.json) includes generated learning blocks, two checked assessment proposals, an unresolved source exercise, and profile-specific export outcomes.
