# Scope and architecture

This overview introduces the product and its ownership boundaries. Use the [detailed specification](../specification/README.md) and [ownership rules](../specification/architecture/02-ownership-and-dependencies.md) for implementation contracts.

## Product boundary

The LMS owns the teaching and learning record. It defines what can be taught, who may participate, what a learner saw and submitted, how the work was marked, and which result was published. It provides staff authoring and administration surfaces and a learner-facing course, assessment and review experience. It runs both as a standalone institution deployment and with optional identity, roster, collaboration, storage and reporting integrations.

An institutional implementation must serve a school with teacher-led classes, a college with credit-bearing terms and multiple sections, and a university with delegated departmental administration, moderated exams and record retention. Small deployments can use a single institution, default organization unit and simple grading without activating every optional module.

| Area | Scope |
| --- | --- |
| Curriculum | Course catalog, learning objectives, outline, lessons, activities, media references, translations, reusable libraries, approvals and publishable versions |
| Teaching | Offerings, rosters, class sections, learning groups, cohorts, calendars, scoped schedule adjustments, announcements, attendance and staff dashboards |
| Learner experience | Enroll or accept a placement, navigate lessons, resume work, meet prerequisites, submit work, receive feedback, review progress and view released results |
| Assessment | Item bank, flexible forms, mathematics, practice, assignments, timed exams, assessment accommodations, attempts, automated and human marking, moderation, appeals and regrades |
| Academic records | Gradebook, academic release, published reports, report cards, credits, programs, competencies, credentials and transcripts |
| Interoperability | Course and library import, versioned content exports, SCORM player, roster and external tool connectors, portable results and historical migration |
| Operations | Permission administration, audit, retention, backups, restore, accessible authoring and delivery, localization, reporting and operational observability |

A site can delegate authentication, storage, document sharing, video hosting, chat, conferencing, or authoritative student and transcript records. The LMS still controls eligibility, assessment submission and effective academic results. Payment, payroll, general finance and standalone productivity suites belong to integrations. Proctoring and plagiarism detection are policy-governed integrations. They require a reviewable staff workflow for exceptions and must never directly change a grade.

## Shared vocabulary

| Term | Meaning |
| --- | --- |
| Institution | A school, college, university or tenant boundary for ownership and access |
| Organization unit | A campus, department, faculty, school division or equivalent delegation scope |
| Program | An organized curriculum pathway with course requirements and optional credit rules |
| Course | The durable catalog identity, such as Algebra I |
| Course version | An immutable published curriculum snapshot once released |
| Course offering | A delivery instance of a course with availability, policies, staff and learners. An always-open self-paced course is also an offering |
| Section | A rostered class inside an offering, with optional teacher and schedule. A curriculum outline section is called a module or topic in this specification |
| Cohort | An institution-level grouping that can span offerings, such as Grade 10 |
| Learning group | A collaboration or activity grouping within one offering |
| Enrollment | A learner’s participation in one offering, independent of section or group changes |
| Content node | A reusable module, topic, lesson or resource identity. A placement gives a node or activity its context within a course version |
| Activity | An interactive or tracked learning task, such as a practice exercise, discussion prompt, assignment or package launch |
| Assessment | A definition of the evidence to collect and how to evaluate it. An assessment delivery binds it to a particular offering and placement |
| Attempt | One authorized native assessment sitting with pinned inputs and its own lifecycle. A package registration anchors the state of a packaged learning run |
| Completion | Evidence that published requirements were met. A pass is a grading decision and may be a completion requirement |
| Mark and grade | A mark is awarded evidence at item or criterion level. A grade is a result selected or calculated under an academic policy |
| Report card | An issued snapshot of academic results for a learner and reporting period, with auditable amendments |

## Actors and access

A role is an assignment within a scope and effective time range. A person can teach one offering, mark in a second, and study in a third. Authentication identifies the principal. Authorization combines the requested action, institutional boundary, relationship to the object and applicable release policy. System-wide operational access is separated from educational access.

| Actor | Typical authority | Required boundary |
| --- | --- | --- |
| Platform operator | Deployment, upgrades, backups and recovery | Ordinary platform administration confers no academic review authority. Emergency access is time-bound and audited |
| Institution administrator | Configure institution, units, identity mapping and delegated roles | Institution scope, with explicit permissions for grades, identity exports and audit |
| Registrar or records officer | Terms, enrollment corrections, official results, credit and transcripts | Academic period, program or institution scope. Record corrections require provenance |
| Curriculum author and reviewer | Draft, revise and review courses, libraries and media references | Library, curriculum or unit scope. Separate publishing authority when policy requires it |
| Item author and reviewer | Draft and review bank items, scoring rules and assessment definitions | Assigned bank or assessment scope, with separate permissions for answer keys and publication |
| Teacher or course lead | Manage delivery, announcements, progress and classroom grading | Assigned offering or section. Authoring rights require a separate grant |
| Teaching assistant or learning coach | Support instruction and optionally grade assigned work | Explicit roster, grading and visibility scope. A generic assistant assignment grants no access to protected exam solutions or accommodations |
| Examiner, marker and moderator | Authorize exams, mark assigned scripts, moderate and review appeals | Assessment and allocated scripts. Anonymity, independent marks and release authority are configurable |
| Learner | View eligible material, submit and see own released records | Active or historical access as permitted by enrollment and review policy |
| Guardian or observer | View specifically authorized learner information | Explicit relationship, purpose, expiration and per-record visibility. Default access is empty |
| Support or auditor | Investigate a ticket or inspect audit evidence | Narrow, auditable scope with redaction and approved elevation |
| Agent or integration | Import drafts, update rosters or exchange files and events | Service principal, explicit scopes, job provenance and approval of sensitive effects |

Permission checks run on every server read and write, including exports, downloads, background jobs and object lookups. Reject cross-institution references at write time. Visibility of an unpublished version, answer key, another learner’s data, or an unposted result is governed separately from the right to open the course. Withdrawal and suspension revoke active access under policy while preserving lawful records and authorized historical review. Resolve overlaps between staff scopes without broadening access to unrelated groups.

## Domain ownership

Use clear internal interfaces and separate data ownership. A first deployment can run as one application with one transactional database and workers, with independently installable interface modules when the host requires them. Preserve the same contracts if individual services are separated later.

| Domain | Owns | Publishes or exposes |
| --- | --- | --- |
| Platform | Institutions, units, academic periods, identities, scoped roles, audit, durable jobs, storage custody, provider connections and external resource mappings | Authorized actor context, scoped file retrieval, integration and operational receipts |
| Curriculum | Course catalog, drafts and published versions, placements, resources, activities, learning rules, libraries and asset version references | Published course manifests, authoring, validation and preview contracts |
| Participation | Offerings, sections, groups, cohorts, enrollments and release assignments, schedules, attendance, progress and completion | Access decisions, effective schedules, roster and learning evidence |
| Assessment | Item bank, assessment definitions and deliveries, attempts, submissions, accommodations, rubrics and marking | Finalized marking evidence with provenance and authorized assessment feedback |
| Records | Grade policy, results and release, academic programs, credits, competency decisions, reports, transcripts and credentials | Official released results, academic decisions and authenticated records exports |
| Interoperability | Archives, format adapters, transfer staging, import object mapping, tool launch and package runtime state | Capability reports, imports through owner commands and validated package outcomes |

A component calls the owning domain’s command or query contract. It may keep a read projection with an explicit freshness contract. Other components never edit its authoritative tables. A cross-domain result is either committed with its authoritative state when local or sent via a durable, idempotent handoff. Assessment finalizes native submissions. Interoperability commits package runtime state and submits validated evidence through owner contracts. Records determines which grade is official.

## Release levels

The first institutional pilot must handle versioned course authoring, real curriculum migration, classroom and self-paced enrollment, reliable learning navigation, supported math and objective marking, staff grading, and a reproducible report card. SCORM compatibility is a separate testable runtime profile. Mature institutional operation adds broader interoperability, term management, complex exams, analytics, academic pathways and governance under the same model. The [delivery plan](delivery-plan.md) gives gates for each phase.
