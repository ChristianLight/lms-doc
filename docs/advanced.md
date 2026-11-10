# Advanced learning and institutional extensions

These capabilities build on course versions, rostered delivery, assessment and academic records. Enable them by institutional policy. An institution can use standard course delivery independently of adaptive rules, credentials, public portfolios and programme qualification workflows.

| Capability | Owning domain | New records | Authoritative input |
| --- | --- | --- | --- |
| Managed curriculum propagation | Curriculum | Template subscription, proposed change and conflict resolution | Published course versions and offering bindings |
| Adaptive learning and remediation | Delivery | Versioned rule, assigned path and transition evidence | Completion and grade result revisions |
| Scheduled learning and attendance | Delivery | Meeting occurrence and attendance evidence | Course offering, section roster and enrollment |
| Portfolios and peer evidence | Delivery and Assessment | Portfolio submission and review allocation | Asset versions and assessment rubrics |
| Competencies and programme qualifications | Academic Records | Evidence, qualification decision, credential and status events | Course completions and released grades |
| Cross-listed delivery | Delivery | Teaching association and scoped visibility | Catalog offering, roster and reporting identity |

Existing version, event and authorization conventions apply to these extensions. Delivery makes eligibility and path decisions. Assessment marks and moderates work. Academic Records interprets released evidence for reporting, qualification and credentials.

## Managed curriculum propagation

A curriculum team can publish a shared template for courses in several departments. A subscriber keeps an explicit link to a source template and a mapped stable placement key. A course can use multiple shared libraries. A subscribed placement has one template origin. If nested templates are allowed, require explicit precedence.

| Record | Minimum relationships and fields |
| --- | --- |
| TemplateSubscription | Institution, template Course, subscriber Course, approved base CourseVersion, lock policy version, state and owner |
| TemplatePlacementMap | Subscription, template stable placement key, subscriber stable placement key and base revision |
| TemplateLockPolicyVersion | Institution, version, template node or placement scope, controlled fields and ordering rules, effective dates |
| TemplateSyncRun | Subscription, base template version, proposed version, target draft, requester, change-set digest, state and timestamps |
| TemplateSyncChange | Sync run, placement map or new source key, field or structural operation, base/upstream/local values or references, resolution and reviewer |

1. Compare the proposed release with the subscriber's approved base and current draft. Compute a three-way comparison by field, relationship and placement.
2. Propagate template-controlled fields to the proposed draft. Block unauthorized edits to controlled fields. Retain changes to locally controlled fields. Surface a conflict when both sides can edit a field and changed it differently, or when upstream deletes a placement with protected local dependencies.
3. Surface moves, deletions, grading policy and visibility separately. A release reviewer explicitly approves changes that affect grades, learner access or item compatibility.
4. Apply approved changes to a new draft. Validate its structure, assets, links and accessibility before publication. Publish a course version, then schedule an explicit offering transition when an active offering will adopt it.
5. Record per-subscriber results and conflicts. A failed subscriber can retry independently. If the target draft has changed, run a fresh comparison. A rollback creates a new revision and retains earlier delivery records.

**Acceptance.** A central author fixes a question stem and an instructor changes a local due date. The preview preserves the date, applies the stem to a new draft and leaves past attempts reproducible. A deletion with unresolved dependencies blocks that subscriber while other subscribers complete. Replaying the approved request creates one draft.

## Adaptive learning and remediation

Use versioned rules to assign practice, remediation, extension work or learner-selected alternatives. Triggers include scores, completion, recorded competency, prior credit and authorized teacher decisions. Rules refer to stable placement keys and resolve them against the learner's eligible delivery version.

| Record | Minimum relationships and fields |
| --- | --- |
| LearningPathVersion | Institution, CourseVersion, trigger placement or scoped evidence definition, ordered rules, fallback, transition policy and publication state |
| LearningPathRule | Path version, priority, predicate, output route, selected or required placements, effective range and combination policy |
| PathAssignment | Enrollment, pinned delivery version, path version, trigger event or evidence revision, resolved placement keys, selected choice, state and provenance |

- Use allowlisted predicates with typed values and explicit threshold boundaries. A missing or unreleased result must have explicit pending or fallback behavior.
- Validate missing targets, unintended gaps, overlapping predicates without precedence, unreachable nodes and dependency cycles. Make published rules reproducible against the same evidence and versions.
- Validate opportunities for comparable grades across routes. Treat unassigned conditional items as inapplicable. Where paths have different point totals, apply an approved comparable denominator or separate grade policy.
- Record decisions for explainability. A correction or regrade proposes a new assignment according to policy. Preserve attempted work. Require teacher review where a transition would remove access or alter marks. Record the actor and reason for an override.
- Evaluate access on the server and protect diagnostic labels and evidence from peers. Give learners accessible choices and explain their next actions without disclosing answer keys. Distinguish recommendations from decisions that change graded requirements.

**Acceptance.** A learner scoring at a threshold receives the documented route. A correction changes a pending route while attempted work stays visible to the learner until a reviewed transition. Retries and out-of-order events cannot create duplicate or older assignments. Both paths allow full credit under the approved policy.

## Scheduled learning and attendance

Represent an online meeting, laboratory, fieldwork period or classroom session as a scheduled occurrence. Remote providers may supply evidence. The LMS owns the roster, authorization decision and attendance record.

| Record | Minimum relationships and fields |
| --- | --- |
| MeetingSeries | Institution, CourseOffering, optional Section, organizer, calendar and time-zone rules, recurrence, provider link and accessibility details |
| MeetingOccurrence | Series, occurrence key, original and current time, delivery mode, location or provider reference, capacity and state |
| AttendanceMarkRevision | Occurrence, Enrollment, status, minutes if relevant, evidence source, actor, reason and revision time |
| AttendancePolicyVersion | Offering or programme scope, required occurrences or minimum minutes, makeup and excused rules, effective dates |

Materialize recurring occurrences with stable keys. A reschedule retains attendance history and links to the replacement if an occurrence is cancelled and replaced. Reconcile remote join events, teacher registers and authorized corrections. Deduplicate repeated join or exit events and aggregate overlapping intervals without adding the same minute twice. Specify evidence precedence and surface conflicts for review. Keep present, late, absent, excused and unknown distinct. When attendance affects completion or marks, apply versioned policy and emit evidence to the owning domain. Attendance alone does not imply competency.

**Acceptance.** A teacher corrects a register after an outage. The earlier evidence stays available to authorized reviewers. The gradebook receives the permitted result once. Staff outside the section cannot see the register. A cancellation and a daylight-saving transition preserve attendance and occurrence identity.

## Learner portfolios and peer evidence

A private portfolio holds learner-created work, reflections and achievement evidence across courses. A course submission pins an immutable snapshot. Personal editing and sharing continue on separate versions. An institutional template can specify required evidence types, reflection prompts and rubric criteria.

| Record | Minimum relationships and fields |
| --- | --- |
| PortfolioEntryVersion | Portfolio owner, entry, revision, narrative, AssetVersions, competency references, author and visibility |
| PortfolioSubmission | Enrollment, AssessmentDelivery, submitted version or bundle, time and assessment attempt |
| PeerReviewAllocation | AssessmentDelivery, target submission, eligible reviewer, rubric version, disclosure mode, assigned/due times and lifecycle |
| PeerReviewFeedback | Allocation, submitted criterion decisions and comments, moderation state and release event |

- Allocate reviews within an authorized scope. Exclude self-review and known conflicts. Specify late submissions, small classes, withdrawal, reassignment and reviewer capacity.
- Support identified, reviewer-anonymous and double-anonymous views. Define who can unmask participants. Address names in filenames, attachment metadata and learner-authored content. Provide accessible review and reporting tools.
- Use peer feedback for practice by default. If it contributes marks, publish the minimum number of valid reviews, aggregation, exception handling and staff override policy. Staff review abuse reports and affected decisions.
- Permit authorized learners to share or export personal evidence selectively. Support expiring, revocable share links. Assessment evidence retains institutional access and retention rules.

**Acceptance.** A learner withdraws after allocation. Replacement reviews are assigned once. A later portfolio edit cannot change the original rubric outcome. Revoking a share removes public access and preserves the submitted assessment snapshot.

## Competency and qualification management

Track course completion, competency mastery and institutional qualification separately. A programme may confer a qualification from several outcomes, credit totals, mandatory milestones, a practical task or recognized prior learning. Version the requirements and preserve the specific evidence used in a decision.

| Record | Minimum relationships and fields |
| --- | --- |
| CompetencyFrameworkVersion | Institution, framework identifier and revision, competency hierarchy and mastery scale |
| CompetencyAlignment | Activity, item, criterion, course or programme revision, competency reference, relationship and evidence rule |
| CompetencyEvidence | Person or Enrollment, competency revision, source kind and revision, observed scale result and dates, reviewer where relevant |
| ProgramRequirementVersion | Program, revision, required and elective groups, credits, prerequisites, equivalencies, repeat rules, currency and effective dates |
| ProgramEnrollment | Person, Program, assigned requirement version, dates, status and prior enrollment or renewal reference |
| RequirementDecision | ProgramEnrollment, requirement revision, evidence, equivalency or waiver, actor, rationale and decision revision |
| QualificationDecision | ProgramEnrollment, policy revision, evidence revision set, issuer or approver, type, time and superseded decision |
| Credential | Qualification decision, issuer, subject, credential definition version, issue and optional expiration times, verification identifier |
| CredentialStatusEvent | Credential, transition type, effective time, reason visibility, authorized actor and optional replacement |

- Express framework hierarchy, dependencies and equivalence with stable external identifiers and revision history. Prevent cyclic dependencies where sequencing matters. Preserve old alignments after updates.
- Define evidence aggregation per competency. Options include most recent valid demonstration, minimum number of demonstrations or rubric levels with a minimum for each criterion. Keep insufficient evidence, in progress, demonstrated, superseded and expired distinct.
- A programme audit shows rule satisfaction, credit groups and remaining requirements. Define when an achievement can count toward multiple groups. Require scoped approval, reason and evidence for a substitution or waiver. Reproduce the audit as of a named policy version and evidence cutoff.
- Support manual assignment and approved eligibility rules. A renewal can open before expiry. Create a distinct enrollment for renewal while preserving the prior qualification. Expiry, withdrawal, revocation and supersession have distinct meanings.
- Treat an issued credential as a stable attestation with independently managed current status. Provide privacy-preserving verification or signed exchange. Disclose approved claims only. For public verification use revocable opaque identifiers. For signed exchange, manage signing keys, rotation and historical verification. Resolve expired, revoked, superseded and currently valid statuses.
- A grade correction may prompt review of qualification and credential status. Preserve the original issued claim and use an explicit invalidation or replacement if approved.

Evaluate exchange profiles independently. CASE exchanges competency and standards frameworks. Open Badges represents individual achievements. Comprehensive Learner Record can package several achievements. Interoperability claims require tests for the exact supported profiles. Apply institutional privacy and retention policy to credential verification.

**Acceptance.** A learner receives recognized prior credit, completes a required course and earns a qualification under the correct requirements. Renewal records separate evidence and credentials. A public verifier sees only the approved verification result. A verifier without required authorization receives no credential details. Replaying issuance or revocation produces one transition per approved decision.

## Cross-listed delivery and delegated operation

Cross-listing lets official offerings share instruction. Each official offering remains the authority for enrollment, catalog code, transcript grouping and grade return. Model an effective-dated TeachingAssociation with a shared delivery context and links to participating sections. Each section mapping identifies the authoritative offering, reporting grade items and effective dates. Define how a learner enrolled in two participating offerings is assigned to one or both delivery contexts, which official enrollments receive results, and when separate attempts are required.

- Decide per association whether sections share announcements, learning groups, rosters, collaboration rooms or assessments. Default to section-confined roster and discussion visibility.
- Place cross-listed instructor and assistant privileges in scoped assignments. A single-section teacher can grade only eligible submissions in that section unless granted cross-section duties.
- Require authorized review and a migration plan when moving or merging a section after delivery opens. Preserve original scope and report mappings for earlier attempts and released grades. A split restores future boundaries while retaining records under historical scope.
- Scope delegated administration by organizational unit, academic period and capability. Specify which policies are centrally owned and which settings local operators may change.

**Acceptance.** Two catalog offerings share a classroom and published lessons. Learners keep their original enrollments and grade export destinations. A section teacher sees only the authorized roster. Moving a section after submissions creates an auditable transition and preserves the record owner's access.

## Release gates

| Gate | Evidence |
| --- | --- |
| Curriculum coordination | Three-way comparison, subscriber exceptions, local edits, publication, rollback and idempotency tested |
| Adaptive delivery | Threshold boundaries, missing evidence, path equivalence, regrade and section privacy tested |
| Scheduled learning | Rescheduling, reconciliation, grade mapping and attendance privacy tested |
| Portfolio and peer work | Immutable submissions, allocation fairness, accessible editing, abuse handling and share revocation tested |
| Academic pathways | Policy replay, prior learning, award approval, renewal and credential verification tested |
| Shared teaching | Roster ownership, scoped communication, grade return and split after submissions tested |

## Standards references

- [Competencies and Academic Standards Exchange](https://www.1edtech.org/standards/case)
- [Open Badges](https://www.1edtech.org/standards/open-badges)
- [Comprehensive Learner Record](https://www.1edtech.org/standards/clr)
