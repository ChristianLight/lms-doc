# 07. Teacher workspace, interventions and reporting boundaries

## Workspace views

| View | Staff actions | Scope and separation |
| --- | --- | --- |
| Offering overview | View schedule, publication, enrollment state, content availability and integrations | Instructor sees assigned offering or section projection. Institution admin configures broader scope separately |
| Rosters and groups | Filter active or historic members, assign approved groups, request transfer and export if separately granted | Former membership is not current grade visibility. Assistant capabilities inherit only explicit assignment scope |
| Calendar and overrides | Schedule release or meeting, compare effective dates for affected audiences, preview and apply allowed overrides | Sensitive accommodations require separate capability. Summary exposes only authorized information |
| Learner progress | Inspect assigned requirements, last accepted evidence, overdue tasks and stale projection status | Pending private grades and answer keys remain protected. Teachers see scoped evidence and authorized reason |
| Attendance | Open check-in, review proposals, publish outcomes and request or approve correction | Initial decision and correction have separate capabilities. Learner sees their published outcome |
| Communications | Publish announcement, link room or document, preview audience and inspect dispatch state | Content targeting and provider membership follow effective roster. Separate audit retention from classroom logs |
| Assessment links | Open relevant marking queue, released work and assessment status | Assessment owns evaluation and attempt policy. Records owns released grades and formal report output |

## Operational workflow

1. Instructor receives effective RoleAssignment for an offering, section or learning group. On sign-in show scoped workspaces and whether history is available. Impersonation-like preview uses synthetic learner context with a clear banner and no official mutations.
2. Select scope and dates. Server applies filtering before aggregating or paginating. Show applied scope and cursor. A membership change refreshes projection and invalidates stale export or action intents.
3. Identify a learning intervention by rule, such as required overdue work or failing a released formative threshold. Distinguish unavailable integration, absent evidence, ungraded work and grade release delay. No automated intervention silently changes an academic record.
4. Open a learner-specific action with prerequisite, current projection and expected revision. Record action, evidence, applicable dates, audience, reason and optional follow-up. Sensitive notes have explicit visibility and retention. Default learner-visible messages are separate from restricted case notes.
5. Preview affected schedule and permissions. A date change uses published field precedence. An exemption, extension or approval records capability and exact scope. Bulk action enumerates chosen enrollment IDs and per-row validation. It never expands to a changed dynamic filter after confirmation.
6. Apply authorized mutation with an idempotency key. Record results and asynchronous notification state. A conflict shows current details and leaves unsent notes intact. Outage of provider does not roll back committed native academic actions.
7. Reconcile progress, calendar and communication projections. Show stale status and accepted evidence timestamps. A roster export includes selection, policy version, generated time, audit reference and revocation or expiry. Default export expiry 24 hours, authorized staff only.

## Display definitions

| Label | Exact condition |
| --- | --- |
| Assigned | Eligible in current release and assigned audience by rule |
| Scheduled | Assigned but ordinary start instant is in future |
| In progress | At least one accepted nonterminal event exists under the current release |
| Overdue | Effective due instant has passed, required action incomplete, and no exemption |
| Awaiting result | Authoritative receipt exists and applicable result source is pending |
| Completed | Effective CompletionRecord or satisfied projection under declared policy |
| Exempt | Active approved exclusion from the criterion |
| Projection delayed | Authoritative source sequence exceeds projected sequence beyond the normal processing envelope |

Teachers need accessible table alternatives for charts, keyboard filters, meaningful empty states and explicit totals. Small-group aggregate visibility follows institution privacy thresholds. Scope group counts, exports and dashboard search by capability. Course managers with catalog authority may see curriculum structure without learner names.

## Staff acceptance sequence

A teacher assigned to Section B views only its roster and can draft an announcement for Section B. The teacher proposes due date 17:00 for that section. A learner-specific authorized due date of 19:00 remains effective, and the preview labels its higher precedence without exposing private justification. A teaching assistant can mark ordinary attendance under an assigned capability and cannot apply a records correction outside scope. A student transfers to Section A between preview and bulk publication. The batch rechecks current authorization and reports the moved row while continuing authorized independent rows. A pending provider outage leaves the gradebook and published course progress available with a reconciliation notice.
