# 07 Accessibility, localization and inclusive operation

## Acceptance basis

Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) for complete supported user workflows and [ATAG 2.0](https://www.w3.org/TR/ATAG20/) for authoring tool behavior and author guidance. The release test scope includes renderer, HTML authoring, assessments, authentication, downloads, external activities and recovery screens. Browser automation flags regressions. Manual interaction verifies the tasks and assistive technology combinations automation cannot establish. Conformance and any public claim require independent evidence for the actual deployed scope and institution content.

## Content and interactions

| Surface | Implemented requirement | Verification |
| --- | --- | --- |
| Navigation and authentication | Semantic landmarks, skip routes, visible focus, accessible names, independent keyboard operation, and approved sign-in alternatives. | Use keyboard only from login to exam start and back. Check zoom, small screen, reflow, and mobile focus. Test accessible authentication under the configured provider. |
| Authoring editor | Semantic block options, keyboard control, controlled focus, image alternative and media captions prompts, safe paste, preview and accessible error list. | Author and publish text, table, image and mathematical content with keyboard and supported screen reader. Correct a flagged heading and reopen its preview. |
| Interactive items | Use native controls where practical, label feedback, associate errors with input, and announce autosave and server acknowledgement. | Complete matching or ordering by keyboard without drag. Compare permitted response semantics and scores with the pointer path. |
| Math | Preserve structured mathematical notation, such as [MathML](https://www.w3.org/TR/mathml-core/), and support accessible equation input, navigation and review. Include text explanation where a symbol or graph is unclear in the supported stack. | Read nested fractions, exponents and signs with at least two supported assistive stacks. Enter equivalent numeric and symbolic answers, then confirm the same scoring contract. |
| Audio and video | Accessible player controls, captions and description appropriate to the content, and transcript or equivalent learning route where needed. | Navigate playback and captions with keyboard and screen reader. Verify essential content remains reachable on the low-bandwidth route. |
| Assessments | Visible and spoken status, server deadline and autosave distinction. Apply documented accommodations and accessible alternatives with equivalent learning outcomes. | Test countdown, focus retention, interrupted save, resume, timeout, alternate interaction and accommodated timing. |
| Reports and documents | Accessible on-screen view of required result, status and reason. Assess exported documents separately when required for record or accommodation. | Navigate full result table with headings, ordered totals, accessible chart alternatives and download warnings. |

Keep an accessibility review status per published content release and imported activity. Statuses are `unchecked`, `reviewed`, `exception_with_equivalent` and `blocked`. A known barrier in required content blocks learner release unless the equivalent accessible activity is approved, linked, and tested. The exception records affected interaction, affected audiences, owner, substitute path, approval, review deadline and the exact revision. A new version invalidates review for changed interactions. Do not treat a package vendor declaration as release evidence.

Manual support baseline starts with one desktop screen reader on two supported browser engines, one current mobile screen reader, keyboard-only, 200% zoom and a 320 CSS pixel responsive viewport where applicable. Validate high contrast, reduced motion, captions, bidirectional content and actual institution-created examples. A failure preventing a required task is release-blocking unless an approved equivalent path is tested and genuinely reachable.

## Locale, language and direction

Store user interface preference, authored content language, and reporting language independently using [BCP 47 language tags](https://www.rfc-editor.org/rfc/rfc5646). Locale resolution tries explicit allowed request choice, user preference, institution default, then shipped application fallback. Content resolution uses the published language policy, exact eligible translation and declared fallback. Show language status and optionally a choice. Do not machine-translate a live exam or result without reviewed versioning. Preserve individual block language and direction in markup.

Use timezone preferences only for display. Store authoritative assessment deadlines as UTC instants plus source timezone and civil value when audit requires it. Use the [IANA timezone database](https://www.iana.org/time-zones). For a civil timestamp within a daylight-saving gap, reject and request a valid time. For a repeated hour, require explicit first or second occurrence. Record the resolved offset, chosen occurrence and zone database version. A subsequent preference, clock or tzdata change cannot alter a published deadline without an approved owner transition.

Example. In a zone where 01:30 occurs twice when clocks move back, the two choices resolve to separate instants. An operator explicitly picks the later occurrence. A student changing display zone sees a new label and keeps the original resolved deadline. A field displaying a decimal mark may use locale comma separators, while an API score uses the grading domain's canonical decimal string and the input parser's published rules.

## Recovery interaction

Do not use colour alone to signal unsaved or expired work. A student sees `local draft`, `saving`, `saved on server`, or `accepted submission` with timestamp and safe retry. Preserve focus and inputs after recoverable errors. Report conflict with instructions to use the current server state or save a distinct local draft, without implying both are accepted. Announce significant time changes without continuously interrupting assistive technology. Offer a reachable support route and print-safe receipt where authorized.
