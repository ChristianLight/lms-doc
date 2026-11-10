# Curriculum, participation and learning delivery

The authoring system publishes reusable curriculum. The delivery system makes a specific publication available to a specific audience under an academic schedule. Learner records follow the person’s enrollment in that delivery instance. A change to one of these concerns must have an explicit effect on the others.

This overview covers everyday curriculum and participation. Use the [course outline contract](../specification/curriculum/01-outline-and-identities.md), [participation model](../specification/participation/01-offerings-and-academic-calendar.md) and [detailed specification index](../specification/README.md) for build details.

## Terminology and scope

| Term | Meaning |
| --- | --- |
| Institution | The administrative and data boundary for one school, college, university or training provider. |
| Organization unit | A unit within an institution such as a campus, faculty or department. A unit can own courses and offerings and can scope delegated permissions. |
| Academic period | A reporting and scheduling interval such as a school year, term or semester. Periods may nest. |
| Program | A curriculum of required or elective courses, optionally grouped into pathways or stages. |
| Course | The enduring academic identity of a subject or learning experience. |
| Course version | An immutable publication of the course outline, its content and activity revisions, and its curriculum-level policies. A working draft exists separately from a published snapshot. |
| Course offering | A delivery instance of a course. It holds the schedule, delivery mode, enrollment policy and current publication to use for new enrollments. |
| Section | A rostered class within an offering. It can have its own teacher, timetable, capacity and due dates. Use *section* for a roster and *module* for curriculum navigation. |
| Cohort | An institution-level group that can persist across several offerings, such as the entering class of 2027. |
| Learning group | A team or other subset of learners within an offering. It may be limited to a section and used for targeted content or shared work. |
| Enrollment | The durable participation of one learner in one offering. It anchors progress, attempts and results. |
| Content node | A stable identity for reusable content. A published content node version freezes the content payload and its references. |
| Placement | An occurrence of content in a course version. Several placements can reference the same content and still carry independent learning rules and progress. |
| Activity | A stable identity for something the learner can do. Its version specifies the interaction and any completion signals. |

### Curricular levels

| Level or type | Typical contents | Navigation and progress |
| --- | --- | --- |
| Module | A week, unit of study or major theme containing topics or lessons. | Visible heading in the course outline. May have a release rule and derived progress. |
| Topic | An optional grouping of lessons or nested topics within a module. | Visible heading or navigation step when used. |
| Lesson | A learner-facing page with an ordered sequence of resources and activities. | Provides a stable deep link, previous and next controls, resume behavior and a completion rule where relevant. |
| Resource | Rich text, accessible mathematical notation, image, link, downloadable file, audio or video. | May be embedded within a lesson or exposed as a linked resource. Viewing is recorded only where relevant to a declared rule. |
| Activity | Practice, questionnaire, assignment, quiz, exam, survey, attendance check, discussion task, live session or packaged learning. | Has explicit learner instructions and may emit completion evidence, generate a submission or link to assessment. |

A draft outline is an ordered tree in a CourseDraft. The virtual root has no placement row. Every placement has a unique position within its derived sibling scope, which identifies the virtual root or its parent. Publishing freezes the outline in a CourseVersion. Validate legal parent-child types and reject cycles, orphaned nodes and ambiguous positions before publication. An imported hierarchy that cannot be mapped without structural loss must retain source ordering and expose the mapping for review. Changing a display title or moving a placement preserves its stable key. Copying or inserting a second occurrence creates a new key. Learner-facing links carry the offering and stable placement key. The server resolves them against the publication applicable to the current enrollment and checks access before rendering. An unresolved link should display a useful unavailable or superseded message where disclosure is permitted.

Separate shared content from the rules applied to each occurrence. For example, two placements can use the same algebra explanation while setting different prerequisites or completion criteria. A placement can carry an instance title, locale-aware display label, required or optional status, availability policy and completion policy. Assessment binds a graded placement to an `AssessmentDelivery` that references a Records-owned `GradeItem` when applicable. A reused activity keeps separate attempts and completion for each occurrence.

### Curriculum and academic records

| Record | Relationships and required information |
| --- | --- |
| `Program` and program requirements | Records owns program definitions and versioned requirements for required courses, electives, sequencing, equivalencies and credit units. Program enrollment pins the applicable requirements. |
| Course catalog entry | A published view of the course or offering with discoverability, eligibility summary, audience, language, description, duration, credits where relevant and catalog prerequisites. Public previews reference an explicit allowlist of content. |
| Competency framework and competency | Records owns competency identities, framework versions and competency versions. Courses and assessments can refer to these through approved alignments. |
| Alignment | Records binds an approved activity version, item version, rubric criterion or grade item to a competency version and records the instructional relationship. |
| Competency evidence | Records accepts authorized learner evidence with source and rule provenance and evaluates competency under an approved policy. |

One course may appear in several programs. A program may require one course from an equivalency set and accept prior learning through a reviewed recognition decision. Keep academic credit, estimated effort, completion, passing and competency mastery separate. See the [program and credit contract](../specification/records/07-credits-programmes-and-recognition.md) and [competency contract](../specification/records/08-competency-qualifications-and-credentials.md). [CASE 1.1](https://standards.1edtech.org/case/) is an exchange option for framework definitions and associations.

## Authoring and publication

1. Create the course identity, descriptive metadata, objectives and catalog visibility. Assign the owner, course authors, reviewers and publisher.
2. Start a draft from a blank template, an earlier publication or a staged import. Support outline reordering, duplication, nested editing, asset selection, native activities, standardized packages and reusable library content. Keep the author’s active branch or revision visible.
3. Edit content using structured controls for rich text, mathematics, media, file references, accessibility metadata and internal links. Provide a teacher preview with correct-answer and feedback behavior where authorized. Provide learner preview by persona, section, locale and simulated time. Preview uses test identities or a segregated context that cannot create official results.
4. Review the draft and its diff against the last publication. Validate broken references, prerequisite cycles, missing translations for required locales, asset availability, assessment settings, schedule constraints and required accessibility information. Report blocking errors separately from warnings and record permitted exceptions.
5. Publish a snapshot as a single operation. Its manifest pins placement identities, content node versions, activity versions, asset versions and the applicable curriculum-level policy versions. Records maintains versioned outcome alignments. Associate it with selected offerings through an explicit operation. Retain previous versions for audit, replay and authorized review.
6. Schedule activation or begin a new offering on the selected publication. The delivery catalog and search projection should expose only activated content allowed for the relevant audience.

The usual draft lifecycle is `draft → in_review → approved → published`. A reviewer can set `changes_requested`. An authorized author can abandon a draft before publication. Publication is immutable and may later be superseded or archived. Use an expected draft revision to protect against concurrent edits. Publishing and import promotion are idempotent and fail atomically on incomplete dependencies. Record who requested, reviewed and activated a change, when it took effect, and which artifacts it affected.

Distinguish an offering’s default publication from each enrollment’s effective publication, tracked by `EnrollmentRelease`. Enrollments start on the offering default. Changing the default affects future enrollments. For an active learner, an explicit rollout records the prior and new course version and maps the changed placements. Carry forward completion only where the revised placement is declared equivalent under a reviewed policy. Preserve the publication and configuration already pinned to every assessment attempt. The default defers rollout for a learner with a protected active assessment or package session. An emergency withdrawal can block access to a compromised resource immediately while retaining history for authorized staff. A rollback creates an audited activation of a previous publication and follows the same compatibility checks.

### Reusable content and assets

- `Library` grants scoped contributor, reviewer, publisher and consumer capabilities. `LibraryEntry` identifies a reusable resource, activity or template. A `LibraryEntryVersion` pins its exact published definition. Library collections and tags help discovery. Display ownership, license, provenance, locale, publication history and known usages to authorized staff.
- **Linked reuse** pins the library publication and its dependencies. When the library changes, the course author sees a diff and can incorporate the new version into a draft. Published courses continue to resolve their pinned version. **Independent copy** creates a new editable identity with recorded provenance. Clarify which action the author is taking.
- Course templates can distribute a shared outline to several courses or offerings. Keep template-to-consumer links, protected fields, accepted local changes, sync status and conflict decisions explicit. Template update and offering activation are separate steps.
- A protected content item can carry explicit rights for reuse, redistribution, modification and cross-institution access. Revoked authoring access can prevent new adoption while existing retained references follow the applicable license and withdrawal policy.
- An `Asset` has durable identity. An `AssetVersion` records a typed storage or provider reference, verified binary metadata when applicable, provenance, rights and approval state. Store locale-dependent captions, transcript, descriptive text and accessible alternatives as associated resources or tracks. A shared content library entry links to asset versions. Deleting a library entry in authoring must respect live or retained references.
- Model translations as locale variants of a logical content revision, with review status and an explicit fallback policy. Record the actual locale and version shown for graded content. A missing translation can fall back for an informational page where allowed and block publication for a required assessment translation.
- The native content schema supports export of reusable bodies and metadata independent of the renderer. Plugins declare their type, schema version, editor, renderer, validation, accessibility requirements and emitted signals. A document or interactive package requiring special handling should remain visible in the import report until a supported rendering or replacement path is chosen.

### Assisted authoring

An authoring agent uses the same validated create, edit, upload and preview operations as a human author under its own scoped principal. It can propose outline changes, explanations, item drafts, alignment suggestions, accessible descriptions and migrations. Operations carry the agent identity, job or batch identifier, revision precondition and provenance. Jobs produce a reviewable diff and can be abandoned or re-run idempotently. Generated assessment answers and keys require review against expected examples, boundary cases and alternative valid answers. Agent-generated work enters a draft and is subject to human review and publish authority. Authoring inputs should exclude learner records and live assessment evidence unless an approved workflow specifically authorizes access and use.

## People, roles and participation

Authentication establishes a `Principal`. The LMS associates human principals with a `Person` through managed identity links. Service and agent principals have distinct identities. The role system grants capabilities in context. An institution grant can be delegated to an organization unit. A course grant controls authoring or library use. Offering, section and group grants control delivery access. Capabilities for authoring, publication, roster changes, grading, grade release, reporting and data export are separate.

| Actor | Scope and ordinary responsibilities |
| --- | --- |
| Institution administrator | Configures organization units, access policies, academic calendar, integrations and delegated administrator rights. Access to learner records follows an explicit separate capability. |
| Registrar or enrollment officer | Manages rosters, admissions, transfers, withdrawals and authoritative learner identity links within an institution or unit. |
| Curriculum manager | Owns course catalog management, delegates authoring and approves curriculum publication as assigned. |
| Records officer | Manages official results, program rules, academic awards and authorized corrections under separately delegated authority. |
| Course author or librarian | Creates and updates assigned course drafts or shared library entries and prepares reviewed imports. |
| Reviewer or publisher | Reviews or publishes curriculum within the granted scope. Offering activation requires a separate Participation grant. |
| Teacher or lead instructor | Teaches an offering or section, manages its learning schedule, assignments and announcements, and views progress and results within the assigned scope. |
| Teaching assistant | Supports assigned sections or groups. Roster exports, accommodations, grade modification and answer-key access each require explicit grants. |
| Assessor, moderator or examiner | Marks assigned work, moderates or approves released grades, and reviews appeals under the relevant policy. Blind marking uses an assignment identifier rather than learner identity where enabled. |
| Proctor or invigilator | Manages exam check-in or records session incidents for assigned learners and time windows, with only the exam information needed for the duty. |
| Learner | Participates under an enrollment and reviews personal progress, submissions and authorized released outcomes. Group membership can expose group materials according to policy. |
| Guardian or observer | Can access a named learner’s approved information through a verified, scoped and time-bound relationship where institutional policy permits it. |
| Support or auditor | Has purpose-limited access to diagnostics or an audit view under a documented, logged delegation. |
| Service or agent | Performs scoped jobs such as roster sync, import, notifications or drafting under an individually identifiable service credential. |

Keep class membership and permission assignment distinct. Section rosters can contain learners and linked teaching assignments. Teaching assignments must carry an explicit offering or section scope and effective interval. Cohort membership is institutional grouping, useful for enrollment policies and reporting. A learning group can support a project team, discussion, collaboration or differentiated instruction within an offering. Membership changes preserve effective dates and provenance. Public learner rosters are opt-in and governed separately from staff access. Learners see group participants and profile fields only where the teaching or collaboration policy permits it.

### Offering and enrollment workflow

1. Staff create the offering with course publication, academic period, effective time zone, delivery mode, enrollment window, sections, staffing and capacity. Add class meeting times, release windows and calendar rules.
2. Accept enrollment through staff assignment, learner self-enrollment, an invitation, an approval queue, cohort assignment or an external roster feed. Public course discovery, a waitlist or a course follow subscription each has its own record and permissions.
3. Check eligibility, prerequisites, class capacity, duplicate active enrollment, administrative holds and the applicable registration window. Admit a learner or record a waitlisted or declined application with a reason and a clear next action. Capacity changes and waitlist promotions must be safe when accepted concurrently.
4. Activate the enrollment. Resolve its effective publication, section memberships and applicable schedule. Provision authorized collaboration resources through a retryable integration. A delay in external provisioning leaves native learning and academic records available.
5. Allow transfer to another section within the offering by ending the old membership and starting the new one. Keep the enrollment and all submitted work. Record any date or prerequisite effects. A transfer to a different offering creates a separate enrollment and uses a reviewed credit or attempt-transfer policy if appropriate.
6. Suspend, withdraw or close participation with an effective date and reason. Revoke live actions and external memberships according to policy. Preserve attempts, results and traceability. Expiration of delivery access and eligibility for academic review can follow distinct policies.

Keep an enrollment application lifecycle such as `requested`, `waitlisted`, `admitted`, `declined`, `cancelled` and `expired` separate from participation lifecycle states such as `active`, `suspended`, `withdrawn` and `closed`. Keep course outcome such as complete, passed or failed separate from participation status. Finishing required work can still leave a learner eligible to access other released content. A retake in another offering produces a new enrollment. Reinstating participation in the same offering records an authorized state transition with the existing history and an approved reset can change what future work counts while preserving prior evidence.

An external roster sync maps stable upstream identifiers by source and institution. Staged reports show additions, transfers, suspensions, missing identifiers and conflicts before destructive roster changes take effect. Explicitly distinguish full snapshots from incremental feeds. A source withdrawal ends that source’s authority to grant access. Where other valid admission sources remain, apply the configured precedence and keep the enrollment active if appropriate. Confirm or suspend unresolved changes instead of reassigning an existing account by matching names or email addresses. Use the same transaction to update authoritative membership and queue downstream notifications. [OneRoster 1.2](https://standards.1edtech.org/oneroster/specifications/standards/v1p2) provides an exchange vocabulary for K–12 rostering and should be mapped to the local participation model.

## Learning delivery and progress

### Delivery modes and time

| Mode | Expected behavior |
| --- | --- |
| Self-paced | Rolling or fixed enrollment window. Activity schedules can derive from an enrollment-relative anchor. An offering may have a final cutoff even when learners progress independently. |
| Teacher-led | Shared meeting and release schedule. Section calendars allow parallel classes with different teachers, meeting times and dates. |
| Blended or hybrid | Native pages and activities combine with scheduled instruction, group collaboration and recorded attendance or equivalent participation evidence. |

An offering schedule distinguishes enrollment opens and closes, content release, recommended date, due date, grace period, submission close and review window. Store instants and the named time zone used for local scheduling. Specify behavior at boundaries and for daylight-saving changes, especially when deriving enrollment-relative dates. Apply any authorized override to named dates and actions. Distinguish an inherited field, a replaced date, and explicit removal where policy permits. Apply field-level precedence from the base schedule through offering, primary section, ranked learning group and explicit enrollment overrides. Validate conflicts and preserve mandatory bounds. Show which time zone and rules apply on the learner’s dashboard, in reminders and when displaying submission receipts. A change to a live schedule records a revision, identifies affected learners and triggers updated calendar or notification messages. An assessment already in progress retains its attempt policy unless an authorized intervention explicitly changes it.

### Availability and completion

An access decision combines the caller’s current authorization, the enrollment’s effective course version, the placement or parent visibility, release time, applicable audience, prerequisites and scoped overrides. A direct link, search result, API read, file delivery and embedded player must consult the same decision. Distinguish visible, locked with a safe explanation, and hidden. Staff preview uses a separate capability and records no learner progress.

Version and validate declarative prerequisite rules. Support all-of and any-of combinations of prior course completion, activity completion, released or staff-certified outcome, date or enrollment-relative time, membership, and reviewed manual clearance. Resolve prerequisites through canonical identifiers. Reject circular, unresolved or unreachable required paths. Keep enrollment eligibility gates separate from activity visibility gates. Reevaluate gates live by default. A published sticky rule for an eligible native non-assessment activity can retain a first successful unlock under the same release. Suspension, safety withdrawal and hard close take precedence. Overrides record scope, grantor, reason, effective period and expiry. A rule may disclose a learner-appropriate next action without exposing restricted metadata or an unpublished score.

| Evidence | Authoritative source and handling |
| --- | --- |
| Viewed or acknowledged | A permitted authenticated client action or explicit learner acknowledgement, if the published policy accepts it. Viewing is engagement evidence and alone cannot establish mastery. |
| Video participation | Provider or player playback evidence with resume position and policy-defined coverage. Provide an equivalent accessible activity when viewing telemetry is incomplete or unsuitable. Avoid counting repeated playback or seeking as cumulative watch coverage. |
| Submitted | The authoritative submission or assessment receipt linked to the enrollment and occurrence. Duplicate client notifications do not create a second submission. |
| Marked or passed | A finalized result or an approved outcome snapshot consumed by the declared rule, with a defined policy for regrades. |
| Attended or performed | An authorized attendance or instructor record for live instruction, approved observation or offline work. Optional synchronous and asynchronous equivalent participation can satisfy the same criterion under a declared rule. |
| Staff override or exemption | An explicit signed decision with reason, scope, effective period and audit trail. |

`LearningProgress` is a projection over accepted evidence for one exact `EnrollmentRelease` and `ContentPlacement`. It tracks state, rule version, evidence count, timestamps and the projected sequence. `ProgressResume` separately holds a private navigation checkpoint. The delivery states are `not_started`, `in_progress`, `completed` and `exempt`, with access gates and pass or fail tracked separately. Keep source events idempotent and use source-specific sequence or version to handle late, repeated and out-of-order reports. Compute module or course progress from the required eligible placements. Optional, hidden, exempt or not-yet-released items each follow the explicit denominator policy. Show counts and label the basis of a percentage. A deadline, unlock or exemption can change the eligible path, so record completion decisions and their basis to preserve awarded outcomes.

### Learner and staff experience

- The learner dashboard shows current courses, next actions, dates, announcements, feedback availability and progress. The course view offers a navigable outline, prerequisites, bookmarks, recent activity and resume. It should identify required versus optional activities and retain an explicit completion message when the learner finishes a course.
- The player supports keyboard use, touch, accessible document and mathematical presentation, and clear progress or submission status. Save and resume on reconnect. Allow reading or low-bandwidth media where feasible, and use the authoritative assessment service for attempts and deadlines. Retried commands carry stable identifiers so the user receives a durable confirmation.
- The learner review surface displays published grades, feedback, policies, prior attempts where released, allowed files and an appeal or clarification route. Keep access to results after the offering closes configurable independently of edit and submit access.
- The teacher dashboard shows the scoped roster, pacing, missing work, progress and approved interventions. Limit visibility of sensitive data by capability. Explain whether records are absent, delayed or unavailable. Teachers can publish targeted announcements and reminders, and staff can record interventions with an auditable reason and approved audience.
- The course calendar includes class meetings, dates and time zone. Feed links, downloads and notification jobs are scoped and revocable. Track announcement targeting and delivery attempts. Prefer secure sign-in links and exclude answer keys, sensitive results or accommodations from ordinary email or chat content.

## Collaboration, documents and media

Native LMS records own academic decisions and assignment instructions. A collaboration provider can supply chat, meetings, discussion rooms and group file sharing. Model a `CollaborationSpaceLink` for an offering, section or learning group with a scoped `IntegrationConnection`, an `ExternalResourceMap` once provisioned, purpose, audience and reconciliation revisions. Platform owns provider identifiers and credentials. Provision membership through a scoped integration that can retry safely. Reconcile and end membership when participation changes. Separate remote sync errors and archive status from teaching status. Scope cross-section discussion explicitly. Apply instructor or moderator roles and report mechanisms appropriate to the collaboration context.

A file provider can store versioned documents for instructors and students. A managed `AssetVersion` binds a Platform `StorageObject` and its verified scan decision. An externally hosted version binds an exact `ExternalResourceMap`. Course readings and assessed work refer to authorized immutable versions or retained snapshots where required. Use separate links for mutable collaboration folders. Resolve permissions for preview and download on every request or via a short-lived scoped access grant. Carry ownership, permitted use, retention and accessibility metadata with the learning reference. When an instructor replaces a file used in grading, preserve the previously submitted or published version for audit.

Media may be hosted locally or externally. Pin an authorized managed or external media version and store caption tracks, transcript, audio description where required, fallback download or equivalent activity, and access rights. Support transcripts and low-bandwidth alternatives. A provider outage should report playback as unavailable and expose the configured fallback. Only approved evidence can satisfy a required media rule.

Target [WCAG 2.2 AA](https://www.w3.org/TR/WCAG22/) for learner and staff surfaces and use [ATAG 2.0](https://www.w3.org/TR/ATAG20/) to guide the editor. Require semantic headings, alt text or decorative designation, accessible links and table headers, captions, clear input labels and errors, keyboard and screen reader support, zoom and reflow, and alternatives to pointer-only interactions. Offer accessible mathematics with readable notation and text equivalents where needed. Exercise assistive technologies across real content and assessments. Design accessible preview and validation for the authoring workflow, including manual review for failures that automation cannot detect.

## Acceptance scenarios

| Scenario | Required outcome |
| --- | --- |
| One course is offered to two classes and to rolling enrollments. | Each roster and schedule resolves independently. Shared material reuses the same immutable assets and records each learner’s work under the correct enrollment. |
| A teacher corrects a shared explanation during a term. | A draft shows the changed library revision. Existing publications and attempts remain reproducible. An approved rollout maps eligible progress to the replacement. |
| An author inserts a lesson from a library twice. | Both placements have distinct stable keys and independent completion. Reordering preserves keys and links. |
| A student moves sections and a teacher from the old section requests a new result. | Existing participation history stays with the learner. The current roster, dates and permissions follow effective assignment and the authorized history policy. |
| An external roster drop arrives while the learner also has an active staff enrollment source. | Sync resolves the source-specific membership and preserves remaining authorized access. It records the decision and any changed external memberships. |
| A student opens a locked lesson by direct URL or a stale search result. | The request applies the current access decision. Restricted content, assets and sensitive rule inputs are withheld. |
| A learner reconnects after uploading or marking a reading complete. | The response returns the existing accepted evidence for a retry. Concurrent or late events yield the correct final projection. |
| The collaboration provider fails during class creation. | The offering and roster can operate. The remote membership request enters a visible retry or reconciliation queue. |
| A caption track is missing on a required video. | Publication validation reports the issue and applies the institution’s accessibility policy. Authorized staff can attach an equivalent route where allowed. |
| An authoring agent proposes a new mathematics lesson and quiz. | The reviewer sees provenance, diff, accessibility checks, answer tests and the proposed publication dependencies. Official results cannot be created by preview or a draft operation. |
