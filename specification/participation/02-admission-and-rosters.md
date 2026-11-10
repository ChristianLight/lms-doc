# 02. Enrollment, admission, rosters and group membership

## Distinguish authority, request and participation

| Type | Purpose and state |
| --- | --- |
| EnrollmentApplication | Applicant and offering, requested section, route, submission time, verified eligibility snapshot, state and revision. States requested, waitlisted, admitted, declined, cancelled, expired |
| Enrollment | Unique person and offering. States active, suspended, withdrawn, closed. Stores admitted instant, source provenance and current revision. Course outcome is separate |
| EnrollmentSourceGrant | Admitted Enrollment, source namespace, stable source grant key, effective interval and source state. The earlier application preserves its own route and eligibility evidence. Create a grant only at or after admission. Multiple independent active routes can support one enrollment |
| EnrollmentRelease | Enrollment, exact course version, half-open interval, reason code, rollout ID and predecessor. One current active release per enrollment |
| AdmissionPolicyVersion | Offering, policy version, modes and eligibility rules, required prerequisite predicates, waitlist sorting, caps and allowed override roles |
| RosterSyncRun and RosterSyncRow | Feed provider, mode, sequence, checksum, expected policy revision and staged per-row disposition, with audit and error summary |

Public preview, invitation, paid eligibility and course follow use independent lifecycle records. Course follow is a discovery subscription and has no authority to take an assessment. An invitation can create an application and optionally bypass a normal application window where policy grants an explicit exception. Token use is bound to an intended person or verified address, single use, revocable and expires after 7 days by default.

## Eligibility and capacity algorithm

1. Resolve authenticated principal to active institution person or verify staff's roster-management capability. Load the offering and admission policy revision. Prohibit self-assignment to privileged staff roles.
2. Verify offered route, active state, application interval, subject consent where required, section eligibility, course prerequisites, and registrar holds. Distinguish waiting evidence from ineligible. Snapshot evaluated predicates, approved prerequisite equivalence and actor for each bypass. Keep reason data visible only to the applicant and authorized staff.
3. Under one transaction, acquire the offering and target section capacity locks in stable identifier order. Check duplicate applications and existing active enrollment. Check available seats as capacity minus currently active or suspended seats and unexpired admission reservations. A null cap imposes no bound. Withdrawn and closed enrollment do not consume seats by default.
4. If eligible and a seat is available, upsert source grant and activate the single person-offering Enrollment. Allocate the first EnrollmentRelease on the current offering default and any selected SectionMembership. If the existing participation is withdrawn or closed, require an authorized reactivation decision or use a new offering for a retake.
5. If full and waitlists are enabled, assign a deterministic priority and queue time, using application ID as final tie-break. Default ordering is chronological among equally eligible applicants. Approved institutional priority may apply before queue time. Never alter priority silently.
6. Commit enrollment, capacity, audit and outbox together. Provider membership and notifications happen after commit. If one asynchronous side fails, retry that side effect with its stable operation key.

Waitlist promotion rechecks conditions and reuses the same locked admission transaction. By default offer a seat for 48 hours, reserve capacity and allow acceptance with fresh eligibility check. Expiration releases the reservation and advances to the next eligible candidate. A direct admission cannot consume a reserved seat. Declining an invitation removes that specific grant route, with other eligible routes evaluated independently.

## Rostering commands and bulk feeds

| Command | Preconditions | Effects |
| --- | --- | --- |
| Apply | Expected offering, authorized route, intended person | Create or return one pending application. Evaluate policy and queue or admit where permitted |
| Decide or promote | Registrar authority, expected application revision, current policy checks | Append explicit decision, reserve seat or create enrollment transactionally |
| Accept reservation | Active reservation token and eligibility | Consume reservation exactly once, activate or return existing enrollment |
| Transfer section | Active enrollment, destination belongs to offering, scoped authority to both affected sections | Close previous membership and open target at same effective instant. Recheck capacity, group constraints and dates |
| Assign group | Group active, membership mode permits actor and cohort/section scope valid | Append interval and enqueue remote room change where configured |
| Suspend or withdraw | Existing enrollment and recorded decision | Change state with effective time. Preserve attempt and progress references and close collaboration grants where required |
| Reactivate | Authorized decision, available seat and explicit release decision | Reopen participation and choose retain current academic release or reviewed rollout |
| Reconcile feed | Source authorization, matching institution and monotonic sequence | Stage identities, validate dry run, apply chosen membership changes, preserve row results |

A full snapshot may end grants absent from a verified complete feed. An incremental feed changes grants only when explicit operations are present. A provider must name feed mode and checkpoint. Hash the payload and reject a reused sequence with changed digest. A partial full-snapshot failure cannot revoke unmatched grants. External identity matching uses source namespace and stable external keys. Ambiguous or unknown identity queues a mapping issue. Never assume same names, email addresses or institutional numbers from different namespaces identify the same person.

Store source namespace, stable external enrollment ID, resolved local person and offering, last seen sequence, grant state, valid from, and optional valid to. Source authority can affect only that source's grant unless institutional policy explicitly designates it the master. A full reconciliation ends absent grants atomically for one verified unit and feed scope. If another active route remains, participation stays active unless an explicit suspension rule takes precedence.

On section transfer within an offering, retain submissions and results. Re-evaluate schedule and content membership effective at transfer. Default use the new schedule for future actions, freeze existing attempt policy and protect learners from an earlier due date for work started under the old schedule by requiring an instructor decision. Any authorized teacher access to earlier work uses explicit historical policy. A group constrained to the departed section closes on the same instant. Across offerings create a new enrollment and record any approved transfer of credit separately.

## Privacy and classification

Roster export requires a separate capability and creates an audit trail with query scope and file retention. Instructor views exclude unneeded identifiers and personal details. Peer views show only policy-approved names in the authorized group context. Guardians receive person-specific access after relationship verification and consent or institutional authority. Staff and agent searches never merge unlinked identities.

## Worked examples

Two eligible learners request the final unreserved seat in concurrent direct admission commands. The first capacity transaction commits. The other sees no seat and returns 409 CAPACITY_CHANGED or enters the waitlist under its authorized route. A retry by the first learner returns the same enrollment and release. An existing held seat is already excluded from direct capacity. Two retries of that reservation use the same token and return one enrollment and release.

A snapshot from source S drops learner P. P retains a valid direct registrar grant. Reconciliation ends S's grant, keeps P active and records the provenance. A later incremental feed with an older sequence yields 409 ROSTER_SEQUENCE_STALE and no membership edits. If S instead supplies a new unknown person key with the same display email, the row enters identity review and leaves P's record untouched.
