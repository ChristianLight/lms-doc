# 05 Privacy, retention and audit

## Institutional data schedules

Use these startup defaults as product configuration, then approve schedules before enrolling real learners. They are operational defaults and do not set statutory deadlines. The institution confirms applicable records, residency, safeguarding, guardian and processor duties. Examples include [the U.S. Department of Education's FERPA applicability guidance](https://studentprivacy.ed.gov/faq/which-educational-agencies-or-institutions-does-ferpa-apply) and [the EU General Data Protection Regulation](https://eur-lex.europa.eu/eli/reg/2016/679/oj).

| Class | Default trigger and interval | Default action and owner |
| --- | --- | --- |
| Official results, report revisions and enrollment history | Closure of academic relationship or record replacement, with no automatic deadline | Manual review by registrar. Preserve until an approved schedule authorizes archive or disposal. |
| Assessed submissions and learner drafts | Final approved result or abandonment plus 365 days for submissions, 90 days for drafts | Manual review for graded evidence. Remove eligible abandoned drafts through owner command. |
| Raw exam telemetry | Attempt completion plus 30 days | Delete unless held or required for unresolved academic integrity review. |
| Identity contact and evidence | Withdrawal or supersession plus 90 days | Review purpose and dependents. Delete or pseudonymize approved contact values while retaining required academic identity. |
| General audit metadata | Event creation plus 365 days | Review verified segment and legal holds. Preserve necessary disclosure and academic evidence under separate schedules. |
| Inbound connector payloads and export copies | Applied or released plus 30 days for connector diagnostics, 7 days for private exports | Dispose redacted artifacts after delivery or replay horizon. Download grants expire separately. |
| Optional external communication | Delivery completion plus 90 days for platform metadata | Dispose platform copies. Provider retention and deletion acknowledgements follow agreed processing contract. |
| Daily backup | Creation plus 35 days | Rotate protected backup generation according to restore coverage and holds. |
| Asset bytes | Owner disposal approval and last permitted dependent reference ends | Remove bytes only after domain and storage prove eligible release of every protected reference. |

Track ownership of content licenses and institutional records separately. A general email opt-out does not waive retention of security notices or permit use of academic records for analytics. A data request, transfer, or disclosure requires appropriate authority and purpose. Accept a learner or verified delegate's request, not unauthenticated proof in a public inbox. Minimize exports and redact records about others unless specifically authorized. Log scope, purpose and decision without copying the exported payload.

## Disposition algorithm

1. Resolve the latest approved policy effective at review time and any pinned earlier minimum. If evidence for the trigger date is absent, mark the record ineligible and report the missing dependency.
2. Compute earliest eligible instant as trigger instant plus policy days in UTC. Apply `max(pinned_minimum, latest_minimum)` by default. A signed reviewed policy migration can replace the earlier minimum for explicitly identified records. A current policy expiry blocks automated disposal.
3. Check active LegalHold at exact record, Person, CourseOffering and record-class scopes. Evaluate open grade correction, exam incident and active version dependencies. Protected references and held byte copies can outlive visible content.
4. Stage a DispositionTask for each storage or processor boundary with the stable action key. Show scope, reason, owner and expected target version. A coordinator reviews any incompatible or missing results before completing the case.
5. Acquire hold scope locks before target locks in deterministic order. Re-evaluate retention and authoritative target under lock. Commit local disposal, audit and external follow-up intent atomically when local. For an external destructive call serialize start with hold application and persist dispatch before calling. Once a provider call is in flight, a new hold blocks further attempts and triggers containment. The system cannot assert that the prior irreversible effect was prevented.
6. Confirm applied effects or lawful exclusions before completion. Timeouts, missing receipts and unverified provider responses leave cases blocked. A hold release requeues review and does not itself dispose of anything.
7. Write a protected restore-safe ledger containing action ID, affected reference, operation, rule and committed time. Reapply it to restored backups before serving data. Preserve the ledger longer than the oldest backup that can resurrect the record.

Worked example. A draft is abandoned at 2027-04-15 14:00 UTC. Its prior rule retained for 90 days and a new rule requires 60. The default earliest boundary remains 2027-07-14 14:00 UTC. A hold imposed on 2027-07-12 blocks disposal after that instant. If review releases the hold on 2027-07-20, the worker may re-evaluate then. A held file with an unresolved report reference remains ineligible after the release until the dependency is cleared.

## Non-destructive case steps

Use PrivacyCaseStep for access, portability, correction and processing restrictions. Resolve each step to a single owner record version and approved protected instruction. For collection, use the owner's authorized projection and generate a protected artifact. Omit other learners' identities, employer material, answer keys and unrelated protected information according to the approved policy. For correction, invoke the canonical domain operation and preserve original academic audit and issued versions. For processing restriction, commit the corresponding owner restriction and check queued work. Do not use destructive retention eligibility for these steps. Holds still constrain permitted mutations and disclosure under their approved scope. Completing a case requires all disposition and non-destructive steps to be applied or lawfully excluded.

## Request and audit screens

The privacy case queue shows received, verified, executing, blocked, completed and denied, ordered by due date. A 30-day operational target applies until replaced by an approved profile. Escalate to the records owner at 75% of the target elapsed and daily while overdue. The reviewer sees the evidence, approved selectors, responsible processor and task status. Requesters see only their own sanitized status and may collect approved results through an authenticated link. The screen must never mark a request complete merely because a notification was sent.

Audit is append-only during retention. Persist the actor, authenticated authority, target, version, resource scope, UTC instant, result, reason code and correlation identifier. Do not log passwords, secrets, external bearer tokens, exam responses, clinical details or full grade exports. Keep restricted evidence in its approved store and link by opaque reference. Audit evidence reading is itself recorded with purpose. Sensitive reads with a required audit trail fail closed if durable audit cannot be accepted.

Create a per-institution ordered audit stream. Canonicalize allowed fields using one versioned serialization and compute `hash_n = SHA-256(serialized_event_n || hash_(n-1))`. Keep periodic signed anchor digests in separate restricted custody, because an unanchored hash chain alone does not prevent an administrator rewriting the chain. A simple implementation serializes the short append transaction per institution. If measured workload requires partitioning, use stable independent chains with a signed stream directory and keep individual ordering guarantees per target. Verify continuity and anchors daily. A policy-approved disposal removes verified sealed segments only after checking outstanding holds. Retain a deletion receipt and anchor evidence without retaining disposed payload.

## AI and intrusive processing

An agent can write a draft only through a scoped service Principal and approved source material. Record provenance, model or tool version, allowed input classes, review and accepted draft revision. Student records, submitted work, accommodations and provider analytics require a separately approved institutional purpose and adapter field policy. Keep telemetry collection purpose-specific. Enable invasive proctoring only after approved policy, accessible alternatives and processing review. Flag models or provider scores as review inputs unless the authorized grading contract explicitly permits them as reproducible evidence.
