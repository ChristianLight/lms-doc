# Delivery plan and acceptance

Use this plan to turn the domain specification into reviewable implementation work. Each increment defines a workflow that a real actor can complete, a data owner, and failure conditions that must be tested before widening access. The [Joomla implementation](joomla.md) maps these increments to components and installer packages.

## Start with a migration and scoring pilot

Record the source application release, enabled extensions and installed versions before classifying any archive. Use an approved private exchange for de-identified pilot data. Keep institution-specific material, package assets, learner responses and scoring keys out of public repositories.

| Pilot input | Evidence to collect |
| --- | --- |
| One typical published course | Course archive and read-only source outline, plus release settings and example links |
| One course with demanding mathematics | Item definitions, expected marks for correct and incorrect responses, tolerances, units, accepted forms, randomized fixtures and any custom grader dependencies |
| One standalone reusable library | A current archive and an example of where a course references it. Include an older-format sample if it appears in the live inventory |
| Each SCORM profile in use | Original ZIP when available, manifest edition, expected launch and resume behavior, and example completion and score mapping |
| External and separately hosted content | Link inventory, captions and asset export availability, authority and any tool dependencies |
| Historical records, if migrating them | Authorized exports of roster, results and completion with field mapping, academic policy, totals and provenance |

Deliver a loss report grouped by course, library and item type. Classify each record as equivalent, approximate with approval, retained in packaged or external form, or blocked. Include one row per missing dependency and any rule that changes learner outcomes. Approve mappings separately for text and layout, access and sequencing, and marks and feedback. The curriculum migration is viable when the institution can account for every required object and scoring case, and accepts the documented handling of exceptions.

## Build sequence

| Increment | Complete learner or staff workflow | Gate |
| --- | --- | --- |
| 0. Architecture and inventory | Inspect synthetic archives and a representative real course, declare format profiles and select a baseline exam and grade policy | Signed-off compatibility matrix and an installation spike that proves account mapping, generated forms and upgrade mechanics |
| 1. Author and deliver | Create and review a course and reusable lesson, publish it, create teacher-led and self-paced offerings, enroll students, and resume a lesson | Ordered versioned content, scope checks and progress remain correct across replays, section moves, and course revision changes |
| 2. Assess and issue records | Assemble native items, set deadlines and accommodations, start and finish an attempt, mark answers, review and issue a report card | Reproducible scoring, idempotent submission, release control and record provenance pass the academic acceptance suite |
| 3. Import and run packages | Preview and apply course and library imports. Upload and launch a supported SCORM package with resume and outcome capture | Imports reconcile and remain editable where declared. Each package profile passes its own browser and conformance suite |
| 4. Operate an institution | Run term and roster operations, moderation, accessibility and privacy workflows, integrations, historical exports and recovery | Operate a complete pilot term including interrupted integrations, workload tests, term closure, restore and approved corrections |
| 5. Extend | Add pathways, competency evidence, federated tools, transfer credit, delegated operations and expanded exchange profiles as needed | Each capability passes its own contract, safety, access and interoperability gates |

The importer and SCORM experiments start in increment 0. Full production support can follow after native delivery and grading are established. Keep compatibility profiles independently releasable so an incomplete profile does not affect a supported one.

## Domain commands and evidence

Names below identify use cases. A host application can expose them through HTTP, scheduled jobs, administrator forms, or a service library. Use the same authorization and validation for every caller.

| Command or query | Owner and request | Outcome |
| --- | --- | --- |
| Publish course version | Curriculum. Course, draft revision, release request and approved dependency manifest | Published immutable version or scoped validation errors |
| Pin offering release | Delivery. Offering, expected prior pin, published version, effective date and rollout decision | Updated release assignment with migration and impact evidence. Existing attempt snapshots remain valid |
| Request or activate enrollment | Delivery. Person, offering, applicable policy, optional class and source | Current enrollment or scoped rejection. Capacity and duplicate checks are transactional |
| Resolve learner outline | Delivery. Authorized principal, offering and effective instant | Pinned version, eligible placements, progress and access reason codes safe to disclose |
| Start, save or submit attempt | Assessment. Learner context, delivery, accepted input or finalization token and request key | Pinned form, persisted autosave revision, or immutable submission receipt |
| Accept marking evidence | Assessment. Submission, evaluator or authorized marker, evidence and version | Validated mark revision and grading event or actionable exception |
| Post grade or issue report | Academic records. Scope, selected policy and revisions, effective time and approver | Explicit release or issued revision. Replayed commands return the original receipt |
| Stage or apply import | Interoperability. Artifact, adapter profile, source namespace, target and review evidence | Staged graph and issue report, or committed draft graph with provenance |
| Commit package state | Interoperability. Constrained launch grant, package registration, session, occurrence and update sequence | Durable data-model changes and approved normalized outcomes |
| Project collaboration membership | Integration adapter. Source roster event and desired remote projection | Provider-scoped confirmation, queued retry, or operator-visible divergence |

A durable domain event includes event ID, type and schema version, institution, aggregate identity and revision, occurred and recorded instants, producer, principal or source identity, and correlation key. Keep private answer keys, raw learner responses and accommodation reasons out of event payloads. Consumers deduplicate per event and record accepted versions or ordering dependencies. Where a receiver cannot apply an event yet, retain a retryable receipt and reconcile against the authoritative owner rather than guessing a result.

## Academic and technical acceptance

| ID | Scenario | Required result |
| --- | --- | --- |
| LMS-01 | An author proposes a library update after two offerings have been published | Both offerings retain their pinned behavior until an authorized rollout. The changed references appear in a diff |
| LMS-02 | A teacher changes a due date for one section and grants extra time to one learner | Other sections retain their policy. Effective windows and priority are visible to the authorized learner and staff |
| LMS-03 | An enrolled learner moves section while working on an exam | Roster permissions change prospectively. The in-flight exam preserves its pinned form and start policy unless a documented override is applied |
| LMS-04 | Two devices open and finalize the same limited-attempt exam | Only one allowed attempt and one authoritative receipt are recorded. Repeated or stale writes have explicit results |
| LMS-05 | A network interruption occurs at the deadline | The client reports the authoritative status on reconnect. Previously accepted responses, cutoff rules and any finalization remain auditable |
| LMS-06 | An equation item accepts a rearranged expression but rejects a missing domain restriction | Fixture outcomes match the authored equivalence rule and feedback policy across repeat runs. Expensive or malformed inputs fail safely |
| LMS-07 | Two markers disagree, a moderator decides, and a released result is appealed | Independent marks remain visible to authorized roles. Moderation and appeal decisions preserve both the original and amended academic record |
| LMS-08 | A records officer issues a report while other learners have pending or excused work | The grade policy treats pending, excused, missing and zero as defined. The report identifies the issued grade and policy revisions |
| LMS-09 | An archive is reapplied after a teacher locally edits an imported question | Identity is preserved. An unchanged source is a safe replay, and divergent updates require an explicit decision |
| LMS-10 | A package resumes after an interrupted session | It loads the last acknowledged state under the same registration and version. Invalid or late commits cannot change another registration |
| LMS-11 | A learner tries a direct URL for another learner’s grade, upload or active exam solution | The system rejects the access without leaking sensitive metadata, including through exports, cached views, or adapter links |
| LMS-12 | Chat or document sharing is unavailable | Native delivery, attempts and grades remain available. The integration reports its status and reconciles after recovery |
| LMS-13 | A reviewer navigates and completes a math assessment using the keyboard and a supported screen reader | Navigation, instructions, expression input, timing, errors, save status and feedback are usable under the supported accessibility profile |
| LMS-14 | The institution restores from a backup mid-term | The restore accounts for uploads, acknowledged submissions, issued results and replayable integration state within the agreed recovery objectives |
| LMS-15 | An AI agent creates a draft lesson and an assessment with generated variants | Permissions allow scoped draft creation. Validation, fixture evidence and reviewer approval are required before students see it |

## Decisions that need institution input

| Decision | Why it affects the build |
| --- | --- |
| Installed release, plug-ins, library formats and SCORM editions | Fixes the adapter profiles, package extraction plan and migration test corpus |
| Scoring fidelity and must-preserve question types | Determines what can be converted directly and what requires a dedicated evaluator or an approved replacement |
| Authoritative sources for identity, rosters and official records | Prevents conflicting writes between the LMS and institutional systems |
| Local rules for exam access, grade weighting, reviews, amendments and completion | Defines configurable academic policy and sign-off for effective grades |
| Reporting periods, report-card formats, credits and transcript obligations | Determines which records the LMS issues or exports and which system owns long-term authority |
| Retention, access to sensitive student data, data residency and safeguarding policy | Sets permissions, exports, integrations and operational recovery boundaries |
| Concurrency, peak exam schedule, recovery limits, locales and supported devices | Sets measurable load, restore and accessibility targets |
| File-sharing permissions and existing provider APIs | Defines provisioning, revocation, and which files can be copied or only referenced |
