# Detailed LMS specification

Read the architecture contracts first, then the owning domain chapters and catalog for the feature being built. The [generated reference](../reference/README.md) provides the typed record and API surface.

## Contract artifacts

- [Entity and interface reference](../reference/README.md)
- [OpenAPI description](../reference/openapi.json)
- [Permission scope registry](platform/scope-registry.json)
- [Joomla component allocation](joomla/component-map.json)
- [Catalog structure schema](../tooling/catalog.schema.json)

## Reading order

## Architecture

- [Specification contract and reading order](architecture/01-specification-contract.md)
- [Ownership and dependency rules](architecture/02-ownership-and-dependencies.md)
- [Command and event protocol](architecture/03-command-and-event-protocol.md)

## Platform

- [01 Platform contracts and ownership](platform/01-platform-contracts.md)
- [02 Institutions, people and academic periods](platform/02-institutions-people-and-periods.md)
- [03 Authentication and account binding](platform/03-authentication-and-account-binding.md)
- [04 Scoped authorization, delegation and guardians](platform/04-scoped-authorization.md)
- [05 Privacy, retention and audit](platform/05-privacy-audit-and-disposition.md)
- [06 Secure storage, scanning and binary delivery](platform/06-secure-storage-and-content.md)
- [07 Accessibility, localization and inclusive operation](platform/07-accessibility-and-localization.md)
- [08 Durable commands, events and jobs](platform/08-durable-commands-events-and-jobs.md)
- [09 Provider synchronization and notifications](platform/09-provider-sync-and-notifications.md)
- [10 Reliability, recovery and release acceptance](platform/10-reliability-recovery-and-release.md)
- [Structured platform catalog](platform/catalog.json)

## Curriculum

- [01. Outline, identities and placement validation](curriculum/01-outline-and-identities.md)
- [02. Typed content, editors and renderers](curriculum/02-content-types-and-editor.md)
- [03. Course publication and release rollout](curriculum/03-publication-and-rollout.md)
- [04. Content libraries and managed template propagation](curriculum/04-libraries-and-templates.md)
- [05. Assets, media and localization](curriculum/05-assets-media-and-locales.md)
- [06. Authoring screens, agent operations and staged imports](curriculum/06-authoring-workflows.md)
- [Structured curriculum catalog](curriculum/catalog.json)

## Participation

- [01. Offerings, sections and academic calendars](participation/01-offerings-and-academic-calendar.md)
- [02. Enrollment, admission, rosters and group membership](participation/02-admission-and-rosters.md)
- [03. Access decisions, prerequisites and schedule calculation](participation/03-availability-and-dates.md)
- [04. Progress evidence, completion and recalculation](participation/04-progress-and-completion.md)
- [05. Live learning, attendance and collaboration](participation/05-attendance-and-collaboration.md)
- [06. Learner workflow and screen contracts](participation/06-learner-workflows.md)
- [07. Teacher workspace, interventions and reporting boundaries](participation/07-teacher-workflows.md)
- [08. Invitations, admission holds, follow preferences and learner support](participation/08-admission-invitations-and-support.md)
- [09. Cross-domain races, retries and reconciliation](participation/09-races-and-recovery.md)
- [Structured participation catalog](participation/catalog.json)

## Assessment

- [01. Bank, authoring and publication](assessment/01-bank-authoring.md)
- [02. Candidate interactions and form rendering](assessment/02-interactions-and-rendering.md)
- [03. Mathematics and deterministic evaluators](assessment/03-math-evaluators.md)
- [04. Assessment assembly and deterministic forms](assessment/04-form-and-variant-resolution.md)
- [05. Delivery, scheduling and exam access](assessment/05-delivery-and-exam-policy.md)
- [06. Attempt lifecycle, saving and immutable evidence](assessment/06-sitting-evidence-and-concurrency.md)
- [07. Coursework, teams, uploads and peer review](assessment/07-coursework-team-and-peer-review.md)
- [08. Marking, moderation, correction and appeals](assessment/08-marking-moderation-and-regrade.md)
- [09. API, handoff and verification contracts](assessment/09-api-and-integration-contracts.md)
- [10. Specialized profiles, branching and exam admission](assessment/10-assessment-profiles-and-special-forms.md)
- [11. Implementation verification and fixture strategy](assessment/11-verification-and-golden-vectors.md)
- [Structured assessment catalog](assessment/catalog.json)

## Records

- [01 Academic records authority and data model](records/01-authority-and-model.md)
- [02 Grade policy, categories and scales](records/02-grade-policy.md)
- [03 Grade calculation and worked cases](records/03-grade-calculation.md)
- [04 Evidence intake, corrections and regrade](records/04-evidence-corrections-and-regrade.md)
- [05 Grade release, period closure and correction](records/05-release-close-and-reopen.md)
- [06 Report cards, transcripts and official documents](records/06-report-cards-and-transcripts.md)
- [07 Credits, programme pathways and recognition](records/07-credits-programmes-and-recognition.md)
- [08 Competencies, qualifications and credentials](records/08-competency-qualifications-and-credentials.md)
- [09 Analytics, intervention and lineage](records/09-analytics-intervention-and-lineage.md)
- [10 Records interfaces and acceptance](records/10-interfaces-and-acceptance.md)
- [Structured records catalog](records/catalog.json)

## Interoperability

- [01. Format profiles and native curriculum archive](interoperability/01-format-profiles-and-native-archive.md)
- [02. Transfer workflow and provenance](interoperability/02-transfer-workflow-and-provenance.md)
- [03. OLX and standalone library conversion](interoperability/03-olx-library-adapters.md)
- [04. SCORM content aggregation, import and export](interoperability/04-scorm-content-aggregation.md)
- [05. SCORM 1.2 browser runtime and attempt state](interoperability/05-scorm-12-runtime.md)
- [06. SCORM 2004 runtime editions and data model](interoperability/06-scorm-2004-runtime.md)
- [07. SCORM 2004 sequencing, navigation and rollup](interoperability/07-scorm-sequencing.md)
- [08. Secure SCORM launch, sessions and durable saves](interoperability/08-scorm-player-security-and-durability.md)
- [09. Assessment and curriculum exchange](interoperability/09-qti-cartridge.md)
- [10. External tools and roster synchronization](interoperability/10-lti-rosters.md)
- [11. Learning record exchange and institutional cutover](interoperability/11-learning-records-cutover.md)
- [Structured interoperability catalog](interoperability/catalog.json)

## Joomla

- [Joomla package and component contract](joomla/01-package-and-component-contract.md)
- [Identities, generated forms and persistence](joomla/02-identities-forms-and-persistence.md)
- [Host identity and academic access](joomla/03-host-identity-and-academic-access.md)
- [Collaboration and document adapters](joomla/04-collaboration-and-document-adapters.md)
- [Agent build and release workflow](joomla/05-agent-build-and-release-workflow.md)
- [Component allocation and Admin View budget](joomla/06-component-allocation.md)
