# 01 Academic records authority and data model

## Responsibility

Academic Records consumes accepted assessment evidence and selects an official grade according to a versioned policy. Assessment owns question responses, item marks, moderation of evaluator or reviewer marks, and its source evidence. Delivery owns enrollment, eligibility, assignment windows and delivery release. Academic Records owns the gradebook, release of grades to recipients, credit, transcript, competency aggregation and formal qualification. An inbound integration supplies evidence through an authorized adapter. It may never directly write an official grade, issue a record or grant credit.

| Fact | Authoritative source | Permitted records interpretation |
| --- | --- | --- |
| Response was submitted | Assessment | Determine whether selected attempt is eligible for official credit |
| Raw score was scored or superseded | Assessment | Select accepted evidence and apply published grade policy |
| Learner was assigned a route or activity | Delivery | Set applicability within grade calculation, without inferring zero |
| Assignment deadline was accommodated | Delivery or assessment owner of effective deadline | Use pinned effective deadline for late policy and missing status |
| Attendance or external outcome arrived | Authorized provider through named input | Validate source, normalize declared scale and apply policy |
| Staff entered a mark for offline work | Assessment manual evidence intake | Accept only assigned staff and approved item source |
| Course is passed or failed | Academic Records approved result | Emit release version for eligible downstream use |
| Course credit was earned | Academic Records credit policy | Issue a credit decision referencing released grade or recognition |
| Learner demonstrated a skill | Academic Records competency decision | Preserve source and applicable framework version |

A GradeItem is the stable identity of a gradebook line. Its GradeItemVersion pins a placement key, source binding, maximum, deadline policy and hierarchy under a GradePolicyVersion. An Enrollment has independent grade results per item and summary scope. GradeResultRevision is the immutable calculated or approved revision of that result. GradeRelease supplies the authorized visibility and official lifecycle. A transcript contains published final results and credit decisions chosen at an explicit cutoff. A report card may contain published interim results and reports its status prominently.

## Main relationships

- An Institution has many grade scales, grade policies, academic records, programmes and competency frameworks. No operational relationship crosses its boundary.
- One CourseOffering has one or more GradePolicyVersion records. An offering default selects which published policy to stage for newly created enrollment releases. A GradePolicyAssignment binds the appropriate version to an EnrollmentRelease during an explicit time range. One effective assignment applies at a calculation cutoff. A policy adoption plan expands affected enrollment releases and validates dependencies before activation.
- One GradePolicyVersion has one calculation root and zero or more grading categories. Every counted GradeItemVersion belongs to exactly one category in that version. Noncounting lines can share a category for display.
- One GradeItemVersion can map to one specific assessment delivery or other source binding. A given AssessmentDelivery and policy version can have at most one grade-counting binding. Imported split items need explicit distinct source dimensions and a mapping approval.
- One Enrollment has one GradeResult identity per result target. The target is an item, category or course summary for one grading period or whole offering. The result identity persists across compatible policy revisions. Every GradeResultRevision references exactly one GradeResult and exactly one policy assignment. Immutable sources attached to a result explain how it was derived. Staff previews use a separate pointer from final-purpose calculations. A learner-current projection is derived from authorized release entries and cannot change either pointer.
- One GradeRelease can contain many GradeReleaseEntry rows. Each entry pins one GradeResultRevision. One learner can receive a revised release after an original release. A later release supersedes prior visible entries only for the same target and release purpose.
- One Person can have many credit decisions, report cards, transcript revisions, programme enrollments and credentials. The Person identity is local to the institution. Document recipient authorization is evaluated for every download.

## Time and source identity

Persist UTC instants with explicit local time zone when an operator enters an academic deadline. Use the established institutional period and calendar. Record both effective academic time and recorded processing time when they differ. A cutoff is an immutable source vector of revision identities and source sequence bounds, not a query against mutable current rows. Worker sequence describes intake order. Source sequence describes the ordering within its authoritative stream. A late-arriving correction does not become older because its academic effective date is earlier.

Every saved result specifies institution, enrollment, target, policy and algorithm version, purpose, source cutoff, normalized score and status, calculation fingerprint and recording time. Store an ordered evidence list or a content-addressed snapshot with durable source links. Source links include stable reference, exact revision and disposition such as counted, dropped, excluded, provisional or stale. The fingerprint uses a declared canonical encoding and SHA-256. It covers policy, results, rational decisions and evidence pointers. Regenerating an identical official revision must deduplicate within the same GradeResult. Derived search and summary rows can be rebuilt from authoritative records.

## Roles and screens

| Screen | Default roles | Primary scope and controls |
| --- | --- | --- |
| Gradebook | Assigned instructor, assistant with grade-read delegation | CourseOffering and assigned sections. Grader-only work queue requires explicit permission. |
| Grade policy and scales | Curriculum approver and registrar | Institution or authorized offering. Draft edit, test preview, publish and adoption. |
| Release and closure | Registrar, instructor authorized for low-stakes item release | Offering and period. Final and correction review require registrar. |
| Learner grades | Learner and explicitly authorized delegate | Person and enrollment. Released marks and explanatory details only. |
| Official records | Registrar and restricted records staff | Institution, person and record purpose. Preview, issue, replace, verify and audit. |
| Programme audit and credentials | Programme adviser or registrar | Assigned programme scope. Personal portfolios remain separately permissioned. |
| Early intervention | Assigned staff with purpose-specific permission | Authorized offerings or caseloads. Row-level scope on every query and export. |

Learning assistants can prepare manual grade evidence if permitted. They cannot approve their own official overrides or release final grades. Learners can view their own released results and permitted feedback. Guardians and advisers need an effective scoped assignment and institutional sharing policy. A service account has named permissions, selected sources, ceilings and no blanket grading or learner read permission.

## Safety defaults

An educational score is a decimal measurement. It is neither a role nor an identity. A correctable result is an append-only record. Stable data links survive course editing, late intake and authorized withdrawal. Course or person archival never silently removes official data. Default to separate preview, publication and official issuance. Derive institution from the actor context and validate it against resources. Never trust institution, enrollment, target or person identifiers in an untrusted event without an authorization and relationship check.

The [catalog](catalog.json) defines fields, commands, scope checks, events and cases. Related data contracts remain with their owning domains.
