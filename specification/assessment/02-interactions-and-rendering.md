# 02. Candidate interactions and form rendering

The renderer reads a public projection of the exact realized attempt form. A response validator converts individual submitted interaction values into versioned typed evidence. Grading receives sealed accepted values. Candidate endpoints cannot reach authoring rule records, private feedback, variant derivation or hidden media. Internal identifiers may be opaque in the client, but server authorization remains mandatory.

## Typed value registry

An interaction has a required key, family, configuration schema version, response schema version, label, required flag, order and cardinality. A response carries a type tag and value. Absence has a separate state. Clearing a value creates an explicit clear revision. Type tags must match the published interaction family. Unknown fields and overlong values are rejected before write.

| Family | Candidate value shape | Structural validation and marks |
| --- | --- | --- |
| Single selection | `{"kind":"single_choice","choice":"b"}` | Exactly one approved key. Selecting an unknown key is invalid. Correctness compares the key against protected accepted IDs. |
| Multiple selection | `{"kind":"multiple_choice","choices":["b","d"]}` | Unique keys from the realized options, configurable minimum and maximum. Store canonical order by key since this is a set. For per-choice mapped scoring sum the declared weights then clamp once to the published min/max. |
| Short text | `{"kind":"short_text","text":"Windhoek"}` | UTF-8 input, at most 512 Unicode scalar values by default. Preserve original for review and use the pinned normalization for matching. |
| Long text | `{"kind":"long_text","text":"My reasoning …"}` | 50,000 scalar values by default. Count words according to the documented locale profile if a length policy uses words. Store plain text in the baseline. A future sanitized structured rich content capability uses a separate explicit family revision. |
| Matching | `{"kind":"matching","pairs":[{"left":"x","right":"r"}]}` | Enforce source and target sets, unique pairs, and capacity per endpoint. Pairs are canonically sorted unless the declared interaction adds order. |
| Ordering | `{"kind":"ordering","items":["three","one","two"]}` | Each approved key exactly once for a total ordering. For a partial-order task, preserve sequence and require coverage defined by the prompt. |
| Categorization | `{"kind":"categorization","placements":[{"item":"i2","category":"warm"}]}` | Apply capacities and uniqueness according to whether each item can appear in one or many bins. Unknown categories and duplicate identical placements fail. |
| Math | `{"kind":"math","input":"3/4","locale":"en-NA"}` | Store the original and versioned parse result with source token spans. Enforce no hidden multiplication choices outside the chosen syntax profile. |
| Numeric with units | `{"kind":"quantity","input":"2.50","unit":"m/s","locale":"en-NA"}` | Separate number and unit controls. Empty unit accepted only where explicitly allowed by the item. Unit parsing uses the pinned registry. |
| File | `{"kind":"files","asset_version_ids":["b6f00bc8-1f11-4ed5-a405-19717e5703ab"]}` | IDs resolve in private attempt scope and were attached by an authorized learner/team member. Only approved scanned assets become accepted evidence. |
| Point or graph | `{"kind":"points","points":[{"x":"0.5","y":"2"}]}` | Use declared coordinate system and decimal bounds. Require an equivalent typed input path. Free drawings use a separate approved review surface. |

A composite item is a group of interactions in one item version. Each blank gets its own key, response and criterion bindings. Multiple fields for a single proof can be human reviewed together. One response can feed more than one criterion with explicit ordered dependencies. Each author-specified point total is the sum of criterion maxima and must equal the item maximum unless a declared bounded combination formula normalizes it.

### Common marking examples

For multi-select, correct A and C may contribute +2 each and distractors B and D contribute −1 each with item bounds [0,4]. A,C,D earns 3. B,D sums to −2 and earns 0. The author must disclose that incorrect selections reduce points. Strict all-or-nothing compares the exact set. A fallback to partial matching requires a changed rule revision.

For a matching item with links x→r, y→s and z→t, each valid expected pair earns 1 point. Extra pairs earn zero when allowed by the response schema. If one target may be used only once, x→r and y→r fails validation and the learner sees the conflict without an answer key.

A five-entry ordering item can use positional accuracy, longest increasing subsequence or explicitly ordered pair accuracy. Choose one rule before publication. In a three-entry item expected A,B,C, the submitted B,A,C earns 1/3 under positional marking and 2/3 under all-pairs precedence because both A and B precede C. A topological task accepts any ordering satisfying its declared constraints. Its score is correctly ordered declared edges divided by declared edges. Reject a cyclic authoring graph.

Text matching defaults to NFC, Unicode case-fold only when configured, trim boundary whitespace, collapse internal whitespace only when configured, and accent preservation. Published expected values undergo the same ordered transformations. Empty after normalization is a blank, not an arbitrary match. Alternative exact values may carry different marks. Reject ambiguous alternatives that normalize identically with different marks. Approved regex mode uses a bounded, non-backtracking engine, whole-string matching by default and fixed input bounds. Human review is the default for free prose.

## Rendering and accessible navigation

The public delivery projection carries delivery, attempt and form version IDs, candidate locale, expiry, section definitions, allowed navigation, attempt item IDs, resolved prompt blocks, interaction definitions, display order and the candidate's own saved values. It contains no expected values, scoring expressions, private work samples, unreleased feedback or candidate identifiers of other learners. Assets are served through candidate-scoped short-lived references and allowlisted media renderers. Strip scripts, inline handlers, tracking URLs and executable documents from candidate content. Rich HTML sanitization is versioned as a rendering dependency.

Each form element has a unique label, visible instructions, programmatic name and stable error association. A group of radio buttons or checkboxes has a group legend. Reorder and match interactions have keyboard buttons and an equivalent list-based input. A graph uses input fields or accessible tables for the same coordinate evidence. Inline math renders a human-readable preview from the parsed value and exposes accessible math and text syntax help. The caret and question position survive validation errors. Announce save and timer changes at an appropriate rate and keep the screen reader from repeating every countdown tick. Never encode answer state using color alone.

A candidate can flag an item for review where navigation permits it. A flag is unscored session metadata with its own update path. With linear navigation, committing a next step can lock the prior section only after the user confirms the action and the server acknowledges the current responses. The navigation lock is server enforced. Time policies are covered in the exam chapter.

## Validation stages

1. Authenticate candidate or authorized team editor. Resolve current attempt lease, delivery, form version and interaction key. Assert the target item belongs to the attempt and is currently writable.
2. Validate the raw JSON shape, kind discriminator, Unicode and body size. Bound parsing complexity before reading expensive rich content or evaluating mathematical grammar.
3. Validate interaction cardinality, known local keys, locale, attachments, public schema version and normalization profile. Apply semantic checks that reveal no expected answer. On practice parse failures, show a notation explanation and retain the editor text locally until corrected.
4. Persist original value, validated canonical representation or explicit clear marker, hash, parse status, accepted server time and author. To preserve evidence of an invalid expression submitted under a formal policy that permits literal capture, store it as `invalid_captured` with the approved parse error code. It is eligible for manual disposition or policy-defined zero. Malformed envelopes and cross-scope evidence cannot be captured.
5. Finalization freezes the last accepted revisions for every interaction. Evaluate public required flags according to finalization policy. The default candidate finalization asks for acknowledgement of blanks and preserves explicit blank entries in its receipt manifest. Forced expiry does not create fabricated answers.
6. A marking service reads the private rule and the sealed manifest using separate capabilities. Learner-safe feedback appears only under the review policy.

Use a 256 KiB encoded save limit, at most 64 edits per save and a configured smaller per-interaction limit. File bytes travel through a separate upload interface. Exam responses stay out of ordinary analytics, browser shared caches, notification payloads and logs. Shared device policies default to memory-only local drafts and require explicit approval for encrypted offline storage.

## Status and error details

| State | Candidate message and effect |
| --- | --- |
| Unsaved local | Show unsaved indicator. Navigation that drops local edits asks for confirmation. |
| Saved | Display authoritative receipt time and a single status announcement. |
| Rejected structure | Show field message plus error summary. No response revision is added. |
| Invalid captured | Show validity warning and save confirmation where the delivery permits literal capture. The receipt indicates the state without revealing marks. |
| Conflict | Keep the local edit, fetch newer revision and offer the authorized learner an explicit retry or replacement choice. |
| Closed | Read-only form. Last acknowledged answers and receipt are shown according to policy. Pending edits are not represented as accepted. |

Accessibility targets [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and the rendering profile may use [MathML Core](https://www.w3.org/TR/mathml-core/). The native type registry is separate from the [QTI information model](https://www.imsglobal.org/sites/default/files/spec/qti/v3/info/imsqti_asi_v3p0p1_infomodel_v1p0.html). Export requires an explicit compatible mapping for the interaction, cardinality, stimulus and marking rule.
