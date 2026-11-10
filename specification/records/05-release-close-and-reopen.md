# 05 Grade release, period closure and correction

## Release purposes and visibility

A GradeResultRevision can be computed, staff-visible and accurate without being released. An audience only sees eligible revision pointers in active GradeReleaseEntries. Purposes are learner feedback, interim report, final course grade and official correction. One grade item can be released before the course result. An assessment feedback release may reveal item explanations, according to its own policy, while academic grade results remain withheld. Academic grade release cannot override hidden answer-key policy.

The default policy requires explicit release for all grades. An institution can enable automatic item release for low-stakes assessed lines after every required mark and moderation prerequisite passes. Never auto-release a final grade, regrade, official override or incomplete decision. A role assignment that permits preparing scores does not imply a release permission. Special visibility such as one learner, a section or a recipient uses recipient filters authorized at activation time. The GradeReleaseEntry pins enrollment and result, and its authorized recipients derive from current scope at read time. Closed records never become world-readable.

## Prepare and activate

1. Select offering, academic period, scope, purpose and cutoff. The preview displays intended audiences, result and status counts, blocked rows, existing releases, outstanding appeals and known downstream corrections.
2. Capture the immutable release set and latest evidence vector. Incomplete, unmarked or quarantined evidence blocks a final target unless an authorized nonnumeric disposition resolves it.
3. An authorized reviewer approves final and correction releases. The default final reviewer is registrar. For item/interim release an assigned teacher may approve their own routine release. A two-person institution policy requires a different approver for selected purposes. A teacher's section permissions cannot expand to offering-wide release.
4. Publish the prepared immutable set, using a compare-and-swap guard for policy, relevant evidence and prior active release. A superseding correction identifies each prior release entry affected.
5. Activate the release and its recipient access predicate in one transaction. Notifications, analytics and export consume the same committed release. A failure to deliver notification does not hide an active grade.

Large releases stage entries in bounded batches. A release manifest tracks expected count, content digest and ordered result IDs. Only the active manifest is queryable by learners. Verify the manifest digest at activation. A release preview must paginate learner details and enforce the same scope for export. A retry uses the same manifest id and cannot republish duplicate notification events. If two reviewers activate conflicting sets, one acquires the release guard and the other sees a stale preview.

If release visibility was incorrect, revoke or replace the offending entries through a new authorized event. Clear cached views and invalidate future download links. Keep the incident record and delivery history. The system cannot recover data the recipient already downloaded. Do not allow a replacement to rewrite the original purpose, release time or actor.

## Grade periods and closure

| State | Permitted action |
| --- | --- |
| Open | Ordinary evidence intake, staff calculation, interim release |
| Closing | Prepare final cutoffs, verify exceptions, reconcile source sequences |
| Closed | Read and export effective final records. New input staged as a correction. |
| Correction open | Modify only approved targets within defined window and approver scope |
| Resealed | Close a correction window after replacement release or documented no-change result |

A GradePeriodClose relates an offering and AcademicPeriod. It is distinct from any global term status. Closing requires academic period end or a permitted early-close decision, effective enrollment list, released finals or approved nonnumeric dispositions, no unapproved blocking overrides and acknowledged evidence checkpoint. The required assessor may still mark source items after close. Their new evidence triggers a correction queue without mutating the official result.

An authorized correction is scoped to exact result IDs and reason, with expiration. It does not reopen the offering to all edits or learners. Roles and target states are rechecked before activation. If a correction affects a prerequisite, transcript, award or transfer, emit a downstream review event. Preserve any already relied-upon decisions. A policy may prevent automatically granting newly unlocked access during correction while still notifying the authorized programme adviser.

**Example.** Section S has 30 learners. Twenty-eight have complete grades, one has an approved incomplete and one has unmarked required evidence. A final set can activate for 29 eligible learners while the one row remains unreleased when selective release is permitted. Closing the period is blocked until that learner is marked or receives a recognized disposition. An accepted late regrade after closure appears in the registrar queue. The 29 original releases remain active until an approved correction release changes a named target.

## Outbound notifications and audit

Outbox notification events use purpose, release entry and recipient scope with an idempotency key. Default message content says that a result is available and includes an authenticated deep link. Do not put a score or sensitive reason in a subject, webhook debug log or push preview. A worker resolves current recipient eligibility before sending. A retracted release or revoked guardian authorization cancels undelivered notifications. Attempts and permanent failures are visible to operations without exposing grade content. Support a manual retry and a separate learner access channel.

Store policy publication, release, supersession, revocation, closure, reopen, report export and privileged access with actor, authority scope, target, request id, prior/current fingerprints and recorded timestamps. Restrict audit visibility to authorized review. Do not put essay content or identity secrets into the audit stream.
