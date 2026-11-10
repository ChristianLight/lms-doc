# 02. Typed content, editors and renderers

## Content definition contract

The [version 1 learning-definition schema](learning-definition.schema.json) is the exact payload contract for the listed types. The server also checks aggregate document byte, depth, scope and reference limits. A renderable definition stores a type key, immutable type version, canonical JSON payload, locale variants, asset and object references, license and provenance. Application registration supplies the JSON Schema, default payload, editor field map, authorization projections, validation hooks, preview renderer, student renderer and migration handler for a particular type version. A payload version stays decodable for the entire retention life of a published course.

| Type | Required payload fields | Optional fields and bounds | Publication conditions |
| --- | --- | --- | --- |
| module, topic, lesson | title string 1–240 characters | summary rich text, objectives list at most 50 plain strings, estimated minutes 1–6000 | Structural children are in placements. A lesson has at least one authorized renderable child |
| rich_text | document with schema version and 1–2000 ordered blocks | per-variant reading direction and source metadata | Reject invalid typed blocks, missing internal references and unauthorized assets |
| image | asset version ID, decorative boolean | alt text 1–512 when informative, caption, intrinsic dimensions and optional long description | Decorative image has empty alternative text. Informative images require useful alternative text |
| document | asset version ID, link label, presentation enum of link or preview | accessible alternative resource ID, description, download filename override | Clean supported file, reviewed license, safe download and accessible route where required |
| video and audio | media asset or registered provider playback reference, title, duration in whole milliseconds | caption tracks, transcript reference, descriptions, poster, start and stop bounds | Time bounds fit duration. Required alternative material and provider restrictions pass checks |
| external_link | HTTPS URL and descriptive label | preview description, approved destination classification | URL parser rejects invalid or disallowed protocol, credentials and unsafe redirects during any server-side probing |
| internal_link | destination stable placement key and descriptive label | anchor within destination document | Key resolves in the frozen version. Authorization rechecked on every follow |
| activity | activity kind and typed config for that kind | learner instructions, accessibility alternatives, estimated time, completion signal names | Exactly one pinned supported implementation and valid dependent record set |
| imported_unresolved | source artifact ID, source location, unresolved reason and review state | redacted preview and suggested conversion | Blocks required publication until converted or replaced. Raw executable markup stays quarantined |

## Rich text payload v1

The canonical authoring model uses a structured document. The web renderer maps that model to a small semantic HTML vocabulary. Text leaves hold Unicode text and optional marks. Block IDs are unique within the locale variant and persist across edits when the same semantic block survives. Limit nesting to 12, rich text to 256 KiB UTF-8 per locale, and inline runs to 20,000.

```json
{
  "schema_version": 1,
  "blocks": [
    {"id": "h-1", "type": "heading", "level": 2, "text": "Equivalent fractions"},
    {"id": "p-2", "type": "paragraph", "runs": [
      {"type": "text", "text": "Divide numerator and denominator by "},
      {"type": "text", "text": "the same number", "marks": ["emphasis"]},
      {"type": "text", "text": "."}
    ]},
    {"id": "m-3", "type": "math", "notation": "tex_subset", "source": "\\frac{6}{8}=\\frac{3}{4}", "spoken": "Six eighths equals three quarters."}
  ]
}
```

| Block or inline kind | Validation and rendering |
| --- | --- |
| heading | Integer level 2–6. Course and page templates own page title level. Detect skipped levels for review |
| paragraph and block quote | Ordered text and inline links, emphasis, strong, code and math. Escape text before rendering |
| ordered list and unordered list | At least one item. Ordered list has positive start. Items contain paragraphs or sublists |
| code block | Plain text language hint and escaped text. Disable execution |
| table | At most 30 columns and 1000 cells, caption and header scope. Preserve linear reading order and render responsive overflow with keyboard access |
| media reference | UUID of approved asset version and local display metadata. Sign delivery links only after access check |
| link | Explicit destination union of permitted HTTPS and internal placement. Use descriptive text and indicate an external destination consistently |
| math | Source type, source bytes and optional reviewed spoken label. Render semantic structure as well as visual form |
| callout | Kind from note, tip, warning and example. Meaning remains visible to assistive technology and in monochrome |

Strip scripts, event handlers, inline styles, forms, iframes, executable SVG and unauthorized remote resources from external HTML conversion. Record unsupported constructs against their source location. Avoid opening even a preview of an untrusted original in the editor origin. Preserve the source in quarantined transfer storage for authorized inspection. Sanitization runs server-side and applies equally to pasted, imported and agent-generated content. Permit approved interactive activities through a registered renderer and validated data schema.

## Mathematics rendering

Author editors accept a supported TeX notation subset or structured MathML, validate it, and render a live preview with both visual output and its assistive representation. Define source length at most 8192 characters, maximum 128 syntax nesting depth, and a bounded macro expansion count of 1000 if macros are enabled. The default disables user-defined macros, external references and URL commands. The service caches safe generated output by math source digest, locale and renderer version. A renderer error marks the equation draft invalid and shows a localized error and source focus target. Published versions retain an accessible fallback when the browser cannot display the preferred renderer.

Treat a math display as content. An assessment interaction has a separate typed response contract and marking evaluator. The renderer sends symbols and instructions to students. It never infers a grading rule from a displayed equation or exposes the expected answer.

## Activity bindings

| Kind | Pinned dependency or required config | Runtime boundary |
| --- | --- | --- |
| acknowledgment | prompt, acknowledgment label, completion signal version | Participation records an authenticated explicit action |
| self_check, quiz, exam, assignment | AssessmentVersion ID, offering delivery binding policy ID, learner instructions | Assessment validates access again and owns attempts, feedback and marks |
| survey | Form version ID, eligibility policy and consent display | Survey adapter emits completion without revealing anonymous response contents |
| live_session | Meeting binding key or series selection, participation evidence policy | Participation resolves scheduled meetings and accepts approved evidence |
| collaboration | Collaboration space binding, task instructions, completion method | Provider handles communication. LMS owns academic completion |
| package | PackageVersion ID, supported runtime edition, adapter policy version | Interoperability manages the isolated player and package-reported evidence |
| external_tool | Approved tool registration and launch policy version | Integration performs validated launch and verifies callbacks before accepting outcomes |

A runtime resolves the exact content and type versions pinned to the learner release. It first authorizes the placement, then produces a learner-safe render model with accessible resources and only approved action controls. A missing renderer returns 503 CONTENT_RUNTIME_UNAVAILABLE and records a diagnostic. It must leave progress and attempts unchanged. Authoring preview has a separate permission and isolated preview actor. Keep official mutations disabled and mark preview clearly for assistive technologies and visible display.

## Content editor field behavior

The editor requests a type-specific edit projection and sends a new full canonical payload with its expected draft revision. Validation returns paths such as `/variants/en/blocks/2/source`, a machine error code and a localized message. Highlight the corresponding control, display a focusable error summary and preserve unsaved user input when the service reports a conflict. The editor autosaves against the latest confirmed revision and distinguishes local pending, saved, conflict and offline states. Each text, reorder or dialog action must be reachable without a pointer. A keyboard reorder announces new position and supports undo as a new revision.

A read-only renderer type registry can expose the client editor schema, version and declared capability names. It may never expose a secret grader schema, integration credential, raw plugin code or hidden activity state. Expired runtime versions can be withdrawn by an authorized safety operation, then replaced through a reviewed publication. Type migration runs on a draft copy with input and output digests, explicit warnings, a mapped dependency list and verified render diff.

Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) on editor and learner surfaces and use [ATAG 2.0](https://www.w3.org/TR/ATAG20/) for authoring assistance. [MathML Core](https://www.w3.org/TR/mathml-core/) informs the semantic math representation.
