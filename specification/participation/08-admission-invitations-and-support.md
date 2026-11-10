# 08. Invitations, admission holds, follow preferences and learner support

## Admission invitation

The registrar first chooses an offering and a verified institutional Person. The invitation dialog shows which application route will be offered, optional section, exclusive expiry, whether the ordinary application window will be bypassed and why. Default lifetime is seven days, with a maximum of 30 days. An invitation creates authority to apply. A separate explicit SeatReservation is required for an exclusive capacity promise.

The service allocates an opaque token with at least 128 bits of entropy, stores a cryptographic digest, and sends it only through an authorized dispatch route. Keep raw tokens out of audit logs, event payloads and staff lists. The landing view first authenticates the invited person, then checks expiry and scope and shows safe next actions. An unverified email cannot establish recipient identity. An institution that invites a person before account creation uses the host identity verification flow and resolves the verified Person before normal application.

Token consumption is part of the same application transaction. It consumes the invitation exactly once. A request losing its response can replay the same idempotency key to retrieve its original application. Two concurrent attempts with the same token and different keys either converge on the original authorized application or return 409 INVITATION_ALREADY_USED. A wrong person or institution receives the generic unavailable response. Revocation and consumption lock the same invitation row. If consumption commits first, the registrar handles the resulting application through its own decision workflow. If revocation commits first, no token use is permitted.

## Hold and reconsideration

An AdmissionHold has an exact person and offering scope. It starts at an inclusive instant and ends at an exclusive instant. Several holds can apply simultaneously. Every active hold must be resolved or explicitly waived by approved authority for the current application. Admission continues to hold the scoped lock or recheck the hold revision after an asynchronous eligibility proof arrives. An expired or ended hold preserves its historical basis for the application decision. A hold affects the admission process. Changing a current enrollment requires a distinct participation decision.

The default learner projection says registration is on hold and presents the authorized next action. Detailed reasons and appeals documentation are visible only to an authorized registrar, assigned support officer or the learner when institutional policy permits it. An automatic hold created by a source feed is still an explicit reviewed policy with provenance, expiry and approved safe wording.

## Course follows

A follow is a personal discovery and notifications preference. It can exist for a visible course even when the person has no enrollment. Store one current preference per course and person. The dashboard distinguishes followed courses from active learning. Unfollow suppresses new notices and preserves the minimal proof needed to prevent an old retry from recreating the preference. Changes to course visibility remove it from ordinary discovery results without exposing private metadata through a prior follow. A user can remove or disable an owned preference without being shown the restricted course title.

## Instructor interventions

The workspace displays actionable evidence and current staff scope. A teacher can record a reminder, request support, schedule a meeting or refer a review. Select one enrolled learner and an approved basis. The service checks authority at record time, not merely when opening the screen. A record can hold a private note reference and optional follow-up. Keep learner-visible wording separate from private notes. The note lives behind an independent capability and approved retention policy.

Follow-up can be open, completed or cancelled. A later teacher can see it only if their current role and the approved handover rule permit access. Changes to grades, due dates, accommodations, enrollment status or completion go through their respective commands, each with its own permissions and audit. A provider delivery failure can keep a message pending without discarding the native support record. An unauthorized request cannot infer whether the intervention or note exists.

| Fixture | Expected result |
| --- | --- |
| Expiry is 09:00 UTC, first use arrives exactly 09:00 UTC | Return invitation unavailable. No application and no capacity change |
| Registrar revokes while invited learner accepts | One transaction wins on the token. The loser reads the exact authorized outcome |
| Learner follows a visible course, then catalog visibility is restricted | Existing preference can be disabled. Catalog details and participation do not leak |
| Learner has two active holds and one ends | Admission remains held by the other active reason. Show the current safe next action |
| Instructor B opens a learner's support record then loses teaching scope | Recheck on mutation. Deny save without leaking private notes |
