# Scope and architecture

## Product boundary

The LMS owns the teaching and learning record. It defines what can be taught, who may participate, what a learner saw and submitted, how the work was marked, and which result was published. It provides staff authoring and administration surfaces and a learner-facing course, assessment and review experience. It runs both as a standalone institution deployment and with optional identity, roster, collaboration, storage and reporting integrations.

An institutional implementation must serve a school with teacher-led classes, a college with credit-bearing terms and multiple sections, and a university with delegated departmental administration, moderated exams and record retention. Small deployments can use a single institution, default organization unit and simple grading without activating every optional module.

| Area | Scope |
| --- | --- |
| Curriculum | Course catalog, programs, learning outcomes, outline, lessons, activities, media, translations, reusable content libraries, approvals and publishable versions |
| Teaching | Offerings, rosters, class sections, learning groups, cohorts, calendars, accommodations, announcements, attendance where required and staff dashboards |
| Learner experience | Enroll or accept a placement, navigate lessons, resume work, meet prerequisites, submit work, receive feedback, review progress and view released results |
| Assessment | Item bank, flexible forms, mathematics, practice, assignments, timed exams, multiple attempts, automated and human marking, moderation, appeals and regrades |
| Academic records | Gradebook, completion, published reports, report cards, credits and transcript or SIS exchange when enabled |
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
| Attempt | One authorized assessment or package run with pinned inputs and its own lifecycle |
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
| Curriculum author and reviewer | Draft, revise and review courses, libraries, media and item banks | Library, curriculum or unit scope. Separate publishing authority when policy requires it |
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
| Administration and identity | Institutions, units, periods, principals, role scopes and external identity mapping | Authorized actor context, policy and organizational references |
| Curriculum | Catalog, programs, course versions, nodes, activities, libraries, media references and outcomes | Published course manifests, authoring and preview contracts |
| Delivery | Offerings, sections, learning groups, cohorts, enrollments, schedules and progress | Access context, roster and activity completion evidence |
| Assessment | Item bank, exam definitions, assessment deliveries, attempts, submissions, rubrics and marking | Finalized marks with evidence and grading provenance |
| Academic records | Grade policies and results, moderation of official results, reports, credit and awards | Released results and authenticated records exports |
| Interoperability | Archives, adapters, import staging, external object mapping and package runtime state | Capability reports, imports through owner APIs and validated package outcomes |
| Operations | Audit, asynchronous work and provider connection state | Audit views, sync status and delivery receipts |

A component calls the owning domain’s command or query contract. It may keep a read projection with an explicit freshness contract. Other components never edit its authoritative tables. A cross-domain result is either committed with its authoritative state when local or sent via a durable, idempotent handoff. Only the assessment owner decides whether a submission is finalized. Only the records owner determines which grade is official.

## Release levels

The first institutional pilot must handle versioned course authoring, real curriculum migration, classroom and self-paced enrollment, reliable learning navigation, supported math and objective marking, staff grading, and a reproducible report card. SCORM compatibility is a separate testable runtime profile. Mature institutional operation adds broader interoperability, term management, complex exams, analytics, academic pathways and governance under the same model. The [delivery plan](delivery-plan.md) gives gates for each phase.
