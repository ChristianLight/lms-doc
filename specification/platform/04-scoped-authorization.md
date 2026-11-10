# 04 Scoped authorization, delegation and guardians

## Typed ancestry

Every operation resolves a canonical resource path and permitted typed ancestors. One academic record may have both an instructional scope and a subject Person. A capability on either context only applies if the permission explicitly admits that route. Use declared relationships rather than generic graph reachability. The [scope registry](scope-registry.json) declares every eligible permission target, whether it can receive a direct RoleAssignment, the institution lookup path, allowed authority parent edges and mandatory domain guard. A tenant lookup path proves custody only. It creates no inheritance. An effective roster relation can produce an eligible scope only through an explicit registry query, such as the SectionMembership that matches an Enrollment at server time. Use a historical membership instant only when the owner contract pins it and the requested operation explicitly authorizes historical scope.

Only explicit assignable contexts can receive a role grant. A library editor can receive a grant on one Library, a cohort administrator on one Cohort, and an examiner on one AssessmentDelivery. The parent OrganizationUnit and Institution can be eligible where the capability and descendants option admit that exact path. An Attempt, PackageLaunchSession or GradeEvidence is an owner-derived target. It never receives a standalone RoleAssignment. Attempt access depends on its typed delivery path plus candidate ownership, approved academic duty or a named marking assignment, as applicable. Existing ItemBankGrant and MarkingAssignment remain additional requirements for their domain operations.

| Target | Default scope paths | Predicates in addition to role |
| --- | --- | --- |
| Institution configuration | Institution | Administrative approval as required. Scope does not include academic records by default. |
| Curriculum draft | Course, owning OrganizationUnit ancestry, Institution | Author, reviewer or publisher capability and lifecycle state. |
| Learning and teaching | CourseOffering, Section or LearningGroup, owning OrganizationUnit ancestry, Institution | Current enrollment for a learner or current staff assignment for class work. Course-level authoring authority does not confer access to learners in offerings. |
| Assessment response | Attempt owner, Enrollment, CourseOffering and declared section | Own attempt or authorized marking assignment. Review and release state are separate. Scope derivation retains the attempt's pinned enrollment. |
| Official result or report | Grading scope, subject Person, CourseOffering or AcademicPeriod | Released projection, duty purpose, record-correction rules and audited export. |
| Guardian summary | Learner Person and verified GuardianRelationship | Current relationship, category allowlist, permitted status, current release and dependency policy. |
| Provider route | IntegrationConnection and Institution | Credential profile, allowed action, currently enabled connection and domain authority rules. |
| Asset bytes | Owner resource's exact path | Current resource visibility, exact published or approved version, storage verdict and access ticket. |

An ancestor capability applies through descendants only when the role assignment sets `include_descendants=true` and the capability admits that typed ancestor. AcademicPeriod grouping is for explicitly period-scoped operations and does not infer classroom membership. A Program, Course or Cohort has no authority edge to an offering merely because it appears in its catalog or roster. A program membership cannot grant access to a course or its grades unless a typed command contract explicitly allows it. A group assignment stays in that group even when a learner shares their class with other groups.

## Decision algorithm

1. Validate authenticated actor, target institution and request context. Reject unavailable resource or untrusted scope. Derive target scope path from owner and current metadata.
2. Check institutional, Principal and Person lifecycle restrictions. Apply current AccessRestriction matching actor or all subjects, capability, scope and time. A match denies immediately.
3. Load approved RoleAssignments and active EmergencyAccessGrants at database time. Match `valid_from <= now < valid_until` with null end allowed for approved standing assignments. Match target type and exact ID or an allowed ancestor with descendants flag. Scope records must be from the same institution.
4. Accept candidate permissions from each grant's pinned definition. Default deny when none match. If more than one candidate matches, evaluate additional owner predicates with each valid authority. A denied owner predicate cannot be overridden by another role label unless the same action admits a separate authorized custody path.
5. Check separation of duties and domain conditions. These can include current enrollment, authorized grader, own actor, review timing, approval by a different person, no pending privacy restriction, or current plan revision. An emergency grant supplies only its exact allowlisted action.
6. Return allowed projection or a classified internal denial. Publish a safe user message and record restricted audit evidence. Cache only decisions keyed by institution, Principal epoch, institution epoch, capability, resource and relevant version. Bound TTL by earliest authorization end, next scheduled institution authorization policy activation and a 30-second maximum. Protected reads and writes with revocation guarantees verify live epochs and the currently effective policy version.
7. For versioned writes recheck the decision in the authoritative transaction under resource and relevant authorization checks. A changed scope or valid-time boundary between user confirmation and write must trigger review. Export jobs reauthorize before generating protected bytes and again before collection.

Example. An assistant has grade-entry rights in section S1 and authoring rights on the whole course. The assistant can grade assigned attempts in S1, can edit permitted drafts, and cannot view attempts in S2. Adding an institution administrator grant does not grant S2 access. A safeguarding denial scoped to one S1 learner overrides the section grade-entry permission for that learner.

## Default role split

| Role family | Default powers | Requires a separate grant |
| --- | --- | --- |
| Institution administrator | Manage organizational setup and propose permitted roles | Grade, mark, publish results, privacy disposal |
| Registrar | Person and academic-period duties per approved configuration, official records review per policy | Course editing, assessment authoring, operational secret custody |
| Teacher | Teach assigned offering or section and manage classroom activities | Official result release where policy requires independent reviewer |
| Assistant | Scoped teaching support, preview, assigned marking queue only with approval | See other sections, release grades, view protected evidence |
| Grader | Mark assigned items or learners, submit rubric feedback | Publish assessment, grant more scopes, finalize report |
| Moderator or publisher | Relevant scoped review and release decision | Original grading where independence rule applies |
| Learner | Own approved enrollment, attempts and released feedback | Another learner's records, draft answer keys |
| Guardian | Approved released summary categories | Any access absent verified current relationship |
| Platform operator | Infrastructure, recovery, monitored repair | Academic records, raw identity data, security decision approval |
| Service actor | Specific worker or connector operations and exact scope | Interactive delegation, administrator panels or arbitrary export |

The catalog enumerates capability and eligible role mappings. Default role assignments are opt-in except where a verified participation workflow explicitly establishes access. Ordinary requested grants default to pending. An institution may allow immediate approval for reviewed ordinary assistant roles in one section. Independent approval is always required for broad institution grants, custody or privacy, grade release, impersonation and emergency access. A role family definition is versioned. Existing grants stay pinned unless a deliberate migration approves the exact new capability and scope set. To remove a dangerous old capability, revoke affected assignments or apply an immediate explicit restriction while remediation proceeds.

## Delegation and concurrency

For proposals, verify the requester's own current authority can delegate the proposed family and scope for the requested interval. Reject a descendant flag broader than the delegator's. Default grant duration is the offering end for classroom work and 90 days for other non-standing duties. Standing grants require written approval and scheduled review every 90 days. End may not exceed source delegation authority unless independent institutional approval explicitly grants it.

Lock on `institution + principal + role family + scope type + scope ID` for overlapping grants. Intervals overlap when start A precedes end B and start B precedes end A. Null end is positive infinity. Adjacent windows are allowed. A grant ending at noon and a replacement starting at noon never both apply to that instant. Revocation bumps scope epoch before acknowledgement. Cache purge, websocket disconnect and provider member removals follow the local security decision.

## Guardian and emergency access

A guardian relationship is a separate evidence-backed record. Its default category list is empty. Approval records allowed categories, effective window and reviewer. Default maximum review window is 365 days and may be shorter for safeguarding. At adulthood, unknown age transition or conflicting custody report, suspend disclosure until authorized review. An adult learner delegation requires explicit and revocable evidence. Verify each read and notification at dispatch, not only when a role is granted. Never expose other students, marks that are unreleased, response details, private teacher notes or custody evidence through guardian projections.

Emergency approval requires an incident ID, exact scope, reviewed capability set and an individual actor with recent strong authentication. Default 30 minutes, hard limit 60 minutes. Emergency use cannot erase audit, bypass explicit denial, override an academic release condition, or dispose of records. Notify the incident owner immediately, log each use with the grant ID, and require incident review before closing.

## Access management screens

The role workbench filters by person, role family, scope, effective time and status. An impact preview lists exact permissions, eligible descendants and any required reviewer. Approval highlights overlapping windows, owner predicates and independence blockers in text. A simulated learner view displays separately scoped preview content and does not impersonate a real learner or mutate academic state. Guardian case review never exposes evidence to unrelated staff. Emergency use displays scope and expiration with a keyboard-accessible stop action.
