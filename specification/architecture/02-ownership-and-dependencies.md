# Ownership and dependency rules

## Authoritative domains

| Domain | Authoritative records | Accepted dependencies | Downstream consumers |
| --- | --- | --- | --- |
| Platform | Institutional identity, organization, principals, grants, audit and operational delivery infrastructure | External identity provider, host account management | All domains |
| Curriculum | Reusable content, course publications, activity definitions and asset metadata | Platform scopes, approved assessment definition identifiers | Participation, interoperability and previews |
| Participation | Offerings, enrollment, effective release assignments, sections, groups, schedules, attendance and progress | Platform identity, curriculum releases, accepted activity evidence | Assessment, records and collaboration adapters |
| Assessment | Banks, items, assessment definitions/deliveries, attempts, submissions, marking and accepted grade evidence | Eligible enrollment and placement, exact curriculum and identity context | Records and progress projections |
| Records | Grade policies, selected grade evidence, released grades, reports, pathways, academic credit and qualifications | Enrollment, accepted evidence and academic periods | Learner review, transcripts, dashboards and approved integrations |
| Interoperability | Staged transfers, external mappings, package runtime and standards adapters | Owner command contracts and constrained delivery context | Owner domains through commands or validated evidence |

The platform provides shared mechanics while each academic owner validates its own business rules. For example, a platform role check can establish permission to mark. Assessment must still check the marker assignment, script state and conflict of interest. A roster grant can authorize enrollment management. Participation must still enforce capacity, prerequisite and cross-institution constraints.

## Collaboration and documents

Collaboration and document providers receive a projection of permitted membership and content access. The provider may own chat messages, meeting recordings or external file bytes. The LMS owns which academic scope authorizes a user to join, the assignment that requests a file, and the immutable submitted version accepted as evidence.

Do not make a course attempt depend on the successful creation of a remote chat room. Persist enrollment, the desired collaboration membership and the outbound event atomically. The adapter later confirms the provider state. A membership change revokes native LMS access immediately according to its effective policy and queues remote revocation. The user-facing integration state distinguishes pending, active, degraded and revocation pending. Native protected content checks remain authoritative while provider state converges.

A live document link can support collaborative authoring. A submitted document requires a stable content version or captured bytes, digest, content type, owner and accepted timestamp. If the provider cannot guarantee that version, copy the authorized submission into immutable evidence storage before acknowledging it. A mutable URL alone cannot support reproducible grading.

## Local transaction boundary

A domain command owns one authoritative transaction. It locks or conditionally updates the rows required to preserve its invariants and inserts its durable event into an outbox before commit. A failed transaction returns no success receipt and produces no externally visible domain event. It may leave a separately owned failed-job diagnostic or an audit record of a rejected request, which must be distinguishable from a completed academic operation.

The first deployment can place owner tables in one relational database. That permits a shared transaction for closely coupled creation while preserving owner APIs. A future split into services requires an explicit process coordinator and compensating or retryable steps. The specification does not assume distributed transactions between providers or independently deployed domains.

An API frontend must not acknowledge success and then enqueue the only copy of a submission or grade. Durable evidence is committed before the receipt is issued. A queue transports work derived from accepted state. The worker can be retried without inventing a second academic operation.

## Cross-domain creation

An offering can reference only a published and accessible course version. AssessmentDelivery references a valid placement and assessment version belonging to an authorized course release. GradeItem establishes which evidence contributes to the gradebook. These references can be created as an approved setup transaction or as a staged activation process.

For staged activation use the following sequence.

1. Curriculum publishes the complete course manifest.
2. Participation creates an offering in `draft` with the intended release.
3. Assessment creates draft deliveries for the manifest's assessment placements and validates their definition pins.
4. Records creates the grade policy and grade items, records evidence-source mappings and validates aggregation.
5. The activation coordinator records successful participant receipts and expected revisions.
6. Participation opens the offering only after every mandatory dependency is ready.
7. If a dependency changes before activation, invalidate the readiness receipt and repeat validation for that dependency.

A failure before activation leaves an inspectable draft. A setup retry reuses the same request key and target identities. Cleanup removes unactivated drafts only after checking that no accepted enrollment, attempt or issued record references them. A lifecycle such as active enrollment requires an explicit withdrawal or closure decision rather than cleanup deletion.

## Version rollout across domains

An offering default release applies to future enrollments. Existing enrollments carry an effective release assignment. A rollout uses a mapping from old placement keys to new placement keys, validates the content version and rules of each mapped placement, and records whether completion evidence is carried, re-evaluated, waived or left attached to its historical version.

The rollout must classify each active attempt.

| Situation | Default action | Permitted explicit exception |
| --- | --- | --- |
| Attempt has not started | Resolve new delivery from the effective release | Keep the learner on the old release until the next allowed point |
| Attempt is in progress | Continue with its pinned form and policy | Authorized intervention for incident response or accommodation |
| Submission is sealed | Preserve its evidence and captured context | Separate regrade under a new rule with approved mapping |
| Grade is released | Preserve the original release | Approved amendment or new grading policy calculation |
| Report or credential is issued | Preserve original issued revision | Formal supersession or revocation workflow |

A rollout affects access, completion and grades through their owners. It cannot mark new work complete merely because an old activity reused the same title. Equivalence requires stable identity, compatible versioned semantics and an explicit reviewed mapping.

## Read projections

Read projections combine authoritative facts for dashboards, search and analytics. Store source watermarks and the last successful refresh. An aggregate row includes its tenant and visibility scope. Cache keys include the fields that materially affect visibility, such as institution, principal or role-scope fingerprint, enrollment release, locale and record release state.

A projection can guide navigation but must not approve an assessment start, reveal an unposted grade, authorize a file download, or grant a cross-institution read. Those operations re-check the authoritative owner state. If the projection is stale, the request can refresh or return a recoverable conflict while preserving the learner's saved work.

Never combine records solely by display code, email or title. Cross-domain joins use stable identifiers and same-institution validation. Aggregated analytics apply an access policy to the contributing population and to the resulting output. A department summary cannot disclose a suppressed small group through drilldown or a complementary total.

## Dependency changes and deactivation

A provider failure changes operational health. A revoked academic relationship changes authorization. Keep these causes distinct. Staff can inspect both without treating a failed notification as failed enrollment.

A component upgrade declares readable and writable contract versions. The package installer verifies dependent versions before enabling writes. Where multiple versions must coexist during a rolling upgrade, use expand-then-contract schema migrations and explicit compatibility windows. Freeze write operations that cannot safely span the change and display an actionable maintenance state. Background workers carry their build and schema version so an old worker cannot write a newly interpreted payload.
