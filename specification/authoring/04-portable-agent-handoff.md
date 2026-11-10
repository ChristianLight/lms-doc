# 04. Portable agent handoff from a PDF

An agent with authorized access to a local PDF and this repository can produce an **unbound curriculum proposal** before the LMS is installed. The proposal gives a teacher a reviewable course plan, typed content and assessment candidates, source evidence and verification results. The installed LMS later supplies the real institution, people, owner IDs, rights decisions and publication receipts.

## Give the agent this task

Copy this request into an agent that can read the attached PDF and the repository revision you intend to use. Audience, teaching time and objectives are optional. The agent records tentative teaching assumptions separately from source facts.

```text
Use the attached PDF and https://github.com/ChristianLight/lms-doc.
Read specification/authoring/01 through 04, authoring-task.schema.json,
proposal-bundle.schema.json, and the curriculum and assessment contracts they reference.

Create a local unbound review proposal for a teacher. Work in a private directory.
Use only approved local or attached-document tools. Keep source text, page crops,
answer keys, scoring vectors and review notes within that directory. Do not
send the PDF, extracts or outputs to a network service or publish or upload them.

Identify the original PDF bytes and physical pages. Extract only the selected
pages and record exact source regions, coverage and uncertainty. Propose
measurable objectives, an ordered outline, lesson content, worked examples
and appropriate assessments. Distinguish source transcription, paraphrase,
calculation, generated instruction and unresolved facts. Do not supply a
correct answer when required information or independent verification is missing.

Use the existing task and content schemas. Initialize one persisted proposal ID
for this project and derive proposal-local IDs from it. Record the source digest
separately. Use artifact files for payloads and verify their digests.
Record blockers, candidate-specific grading evidence and rights or accessibility
questions. Deliver proposal.json and review.md with the referenced private files.
Run the repository verifier on the proposal against the original PDF.

Use SCORM 2004 fourth edition as the requested delivery profile if a delivery
export is wanted, with capability and review still pending. Record an editable
native archive separately if requested. Do not produce a published LMS or
SCORM artifact from this unbound proposal. Return the private proposal location,
verification outcome, review blockers and decisions the teacher needs to make.
```

When the source is too large, encrypted, damaged, permission-restricted or unreadable using authorized tools, record the actual obstruction. Continue with an explicitly identified readable subset only when that remains useful. The authoring protocol accepts a proposal with recorded blockers. Teacher review can use the valid material while withholding incomplete items.

## Prepare and verify locally

Run these commands from a checked-out copy of the repository. Set `PDF_PATH` to the actual local input path. The verifier reads local files and returns JSON summaries. It does not extract PDF content, generate curriculum, contact providers or create packages.

```bash
set -eu
: "${PDF_PATH:?Set PDF_PATH to the local source PDF}"
REPO_DIR="$(pwd)"
PRIVATE_RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/lms-proposal.XXXXXXXX")"
chmod 700 "$PRIVATE_RUN_DIR"
python3 -m venv "$PRIVATE_RUN_DIR/.venv"
PYTHON="$PRIVATE_RUN_DIR/.venv/bin/python"
"$PYTHON" -m pip install -r "$REPO_DIR/tooling/requirements.txt"
VERIFY="$REPO_DIR/specification/authoring/verify-authoring-proposal.py"
"$PYTHON" "$VERIFY" self-test
"$PYTHON" "$VERIFY" init "$PRIVATE_RUN_DIR" --source "$PDF_PATH"
printf 'Private proposal directory: %s\n' "$PRIVATE_RUN_DIR"
```

The dependency installation is separate from content processing. It does not transmit the PDF. If the required package is installed, use that Python environment and skip installation.

After the agent writes the files, verify against the same PDF in the same shell.

```bash
"$PYTHON" "$VERIFY" verify "$PRIVATE_RUN_DIR/proposal.json" --source "$PDF_PATH"
```

Use the `proposal_id` from the initialization command to generate exact local IDs. It is randomly allocated once and kept in `proposal-identity.json`. Resume or copy the same proposal with that identity. Start an independent proposal in a new directory, even if it uses the same PDF. For a source region use key `region:<physical-page-index>:<region-ordinal>`. For other objects choose a durable lowercase semantic key such as `candidate:minutes-to-seconds` or `placement:measurement-intro` and keep the key when its content is edited.

```bash
PROPOSAL_ID="$("$PYTHON" "$VERIFY" init "$PRIVATE_RUN_DIR" --source "$PDF_PATH" |
  "$PYTHON" -c 'import json,sys; print(json.load(sys.stdin)["proposal_id"])')"
"$PYTHON" "$VERIFY" local-id "$PROPOSAL_ID" region:0:0
"$PYTHON" "$VERIFY" local-id "$PROPOSAL_ID" candidate:minutes-to-seconds
```

Local UUIDs identify objects only inside the proposal scope. The source namespace and digest identify the exact PDF bytes and grant no authority. Independent proposals with identical bytes can use the same semantic keys without sharing object IDs. The verifier accepts an offline proposal when the source bytes, relative paths, artifact digests, schemas and checked dependency links match. A zero exit status authorizes nothing. Its output reports `admitted`, `published` and `exported` as false. Page count and OCR findings come from the authorized extractor. The verifier checks their claimed metadata for consistency and checks the actual PDF byte identity. Content accuracy, rights, accessibility and the installed evaluator remain separate review decisions.

## Expected output

| File or directory | Contents and visibility |
| --- | --- |
| `proposal-identity.json` | Persistent scope, source byte fingerprint and size written by `init`. Copy this with the proposal when resuming the same work |
| `proposal.json` | Exact [unbound envelope](proposal-bundle.schema.json), source digest, physical page selection, hashed relative references to the page and stage files and desired future profiles |
| `review.md` | Private teacher brief with assumptions, verified coverage, teaching outline, source gaps, item and grading blockers, rights questions, alternatives and recommended review order |
| Page evidence files and shards | One projected `source_page_evidence` record per selected physical page and hashed private evidence object with accepted reading candidates, exact coordinates, methods and issues |
| Stage JSON files | The existing `coverage_plan`, `course_plan`, `learning_blocks`, `assessment_candidates` and `verification` manifest **body** objects. Leave `apply_plan` and `owner_apply` to installed owner APIs |
| Candidate and verification files | Existing typed content or assessment proposals, protected keys, solutions and independently checked fixtures. References use local file paths. Keep every file protected by default |

The wrapper uses the [authoring task schema](authoring-task.schema.json). For a page evidence record omit `extraction_run_id`. For each stage file write only its existing `body`, with no installed `authoring_run_id` envelope. In these records replace a `storage_object_id` property with `relative_path` pointing to the protected local file, keeping `content_sha256` and `purpose: evidence`. The outer proposal file uses `relative_path` and `sha256` for each manifest reference. All outer and artifact hashes are measured SHA-256 of the exact local file bytes. Set each offline candidate digest to its payload file SHA-256. The local verifier bounds inputs to 50 MiB for source bytes, 20 MiB per proposal artifact and 256 MiB total artifact reads. Use canonical, relative forward-slash paths within the private directory. Empty, escaping, ambiguous and symlinked artifact paths are rejected.

For a complete content candidate, write the exact [native typed learning definition](../curriculum/learning-definition.schema.json) as its payload and keep each locale variant in draft. For an activity candidate, use the `SealActivityVersion` request without `base_revision`, with its typed definition in `payload` and locally bound references. Material claims and objective or placement source links can cite candidate regions on ready pages. Use issue or coverage records for excluded or unresolved regions. For a complete item or assessment candidate, use the existing `SaveItemDraft` or `SaveAssessmentDraft` request body without `expected_draft_version`. For a marking rule proposal, use `ApproveMarkingRule` request data without the installed `institution_id` and `evaluator_release_id`. Identify intended evaluator behavior in the review evidence. Refer to local candidate IDs for dependencies that an admission mapping will resolve. Each planned outline occurrence needs one `placement` candidate using the existing `MutateDraftOutline` insert placement shape. Match the planned placement key, parent, position, kind and requiredness. Use exactly one typed local `content_node_version_id` or `activity_version_id`. An assessed activity needs exactly one typed local `assessment_version_id` in its dependency list. If an occurrence or assessed activity cannot be bound, add a blocking `PLACEMENT_BINDING_MISSING` issue at `/outline/<placement-key>` or `ASSESSMENT_BINDING_MISSING` at `/candidates/<candidate-id>` respectively. The verifier checks this graph before reporting a useful review proposal. Store unsupported or incomplete item blockers in the issue lists and `review.md`. Never insert a fake answer to meet a schema. Keep offline verification `evaluator_release_id` null. Local calculations and fixtures can establish independent checks, while installed evaluator acceptance remains pending.

The [synthetic source-to-course walkthrough](synthetic-source-to-course.json) illustrates claim classes, a blocked source question, verified candidate keys and export decisions. The self-test validates that fixture and its expected digests. The fixture models a source transcript for testing and is separate from a proposal bound to actual PDF bytes.

## Bind the proposal when an LMS is available

1. An authorized operator selects the institution, owning course draft and protected source purpose. Use `ReserveCurriculumSource` and the exact Platform storage and scanning workflows. Verify that the approved storage digest matches the proposal's measured PDF digest.
2. Record the effective rights through `AuthorizeCurriculumSourceUsage`. Treat offline authority notes and local checks as proposed evidence. Recheck the actual source, usage, recipients and provider constraints.
3. Resolve the offline evidence into the existing `SourceExtractionRun`, `SourceRegion` and protected evidence contracts through validated page receipts and human seal. Include the persisted proposal scope in the authorized source crosswalk. Map every accepted local source reference to the correct exact owner identity. A second proposal based on the same PDF receives a separate crosswalk.
4. Stage the approved teaching brief and create `CurriculumAuthoringRun` under the real principal and expected CourseDraft revision. Validate and bind the selected candidate IDs to the appropriate owner operations and exact local-to-installed map. Reuse matching applied receipt on a retry.
5. Review and apply through `ReviewCurriculumAuthoringRun` and `ApplyCurriculumAuthoringSelection`. Curriculum and Assessment own their subsequent review and publication commands. When installed evaluation is available, run the pinned evaluator fixtures against the exact assessment definition.
6. From the approved bound release, request an editable native archive or independently capability-gated delivery profile using `QueueCurriculumExport`. A portable delivery request targets tested SCORM 2004 fourth edition by default. A suitable exporter, asset and question compatibility, disclosure clearance and runtime verification must all pass before an artifact can be issued.

A learner export has its own authorized manifest and audience. Publish selected learning content under the corresponding release rules. Keep original source, OCR and region evidence, staff keys, rejected candidates and review notes in the protected authoring record. A teacher can distribute a separately reviewed learner PDF through its own asset and lesson reference.
