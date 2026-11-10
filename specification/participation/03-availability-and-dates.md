# 03. Access decisions, prerequisites and schedule calculation

## Decision request and response

The authoritative access decision consumes principal, requested action, enrollment ID, current effective EnrollmentRelease, stable placement key, current server instant, locale and provider purpose when applicable. It loads an authorized scope snapshot, policy versions and required eligibility evidence versions. It returns decision state, safe reason, available actions, earliest known unlock if disclosable, applicable schedule version and revision token. Internal diagnostics retain exact predicates and evidence references separately from learner output.

| State | Learner projection | API and side effects |
| --- | --- | --- |
| available | Title, content and authorized controls | 200 and render projection. New learning mutation rechecks decision |
| locked | Visible title and approved safe explanation | 403 LEARNING_LOCKED or locked outline entry. No content, files or assessment keys |
| hidden | Omitted from outline, search and counts | Generic 404 without title, schedule or evidence details |
| unavailable | Visible generic service error if caller has placement visibility | 503 LEARNING_UNAVAILABLE and retry hint. Preserve record |
| review_only | Allowed released feedback, materials or past results | Authorized safe history. Starting or editing work denied |

### Evaluation order

1. Resolve host principal and scoped LMS capability. If authenticated context, institution, enrollment or placement scope fails, return hidden. Scope any historical staff read through a separate capability. Current safety blocks outrank all normal rules.
2. Check offering and enrollment state. Withdrawn or suspended participation permits only separately authorized records review. Closed offering can allow review after result release without allowing new work.
3. Resolve exact release and placement. Evaluate each ancestor's visibility, audience and applicable start/close. A child cannot bypass a hidden ancestor or reach outside the offering's hard access bounds.
4. Resolve date fields independently with the algorithm below. Compare server instant to half-open windows. At an exact release instant access can begin. At the exclusive close instant ordinary starts cease.
5. Evaluate prerequisite expression against authoritative versioned evidence and membership. Apply any eligible override to its declared field or gate. Use safe publication text. A pending trusted source may yield unavailable or locked with neutral status and fail closed.
6. Recheck the required action and return authorized controls. An attempt or evidence write uses the supplied access snapshot revision or re-evaluates within its domain transaction. Never treat the earlier GET as authority for a later submit.

Cache only an authorized projection with a key including institution, effective release, placement, rule revision, action, membership and evidence revision and policy-defined clock bucket. Expire no later than the next known access boundary. Invalidate on suspension, scope change, release, date update and relevant evidence change. A cache outage recomputes or fails closed. Signed asset links and search results use the same decision.

## Gate language

Use the [versioned learning-rule schema](../curriculum/learning-rule.schema.json) to validate declarations. Allow typed nodes all, any, placement_completed, course_completed, result_at_least, member_of, time_at_or_after, approval and evidence_present. Bound depth at 12 and nodes at 100. Groups are nonempty. Negation is disabled by default because it can create difficult-to-explain revocations. A result threshold references released or expressly certified evidence and names the grade item, scale and version. A placement reference uses a stable key in the same course or a qualified previously completed course and institution-approved equivalence. A group predicate uses effective membership at evaluation time. A missing or unavailable leaf is false for access, and records a retry reason. An any branch true allows progression even if another branch is missing. For a locked gate explanation, expose only approved safe phrases and at most three next steps.

The default evaluates prerequisite gates live. If a non-assessment activity opts into sticky continuity, persist its first successful start as unlocked for that enrollment release. Sticky unlock is a persisted decision with evidence and rule version. Safety, scope, withdrawal and hard close can still block. For assessments use configured admission, immutable attempt policy and authoritative released or certified signals. A target rule change on rollout re-evaluates unless approved carry applies.

## Field-level schedule precedence

1. Seed explicit offering hard access bounds and base activity schedule. Resolve fixed instants and allowed enrollment-relative offsets using the calendar algorithm.
2. For each independently named field apply overrides of increasing specificity in this order. Offering override, active primary section, active learning group, and explicit enrollment. Course default is lowest. Group overrides at the same specificity must have an approved unique rank per field when they can apply simultaneously. The highest approved group rank wins. Ties on distinct values are validation errors at write and fail closed at runtime if imported legacy data bypasses validation.
3. An override action is inherit, set, or clear. Inherit leaves the lower rule untouched. Set supplies an instant or validated relative rule. Clear suppresses a lower optional date, such as recommended time or due date. Clear cannot suppress offering access bounds, release floor or mandatory final close.
4. Evaluate schedule consistency for every affected audience. Enforce release less than exclusive close, recommended date within declared scope where present, and due no earlier than release and no later than hard close. A late grace interval cannot extend past effective hard close unless a separately authorized calendar action moved that close.
5. At start snapshot the effective policy in the Attempt or relevant delivery record. On transfer, continue pinned active attempts. A revised due time affects future starts, and a reviewed recorded decision governs any accepted late work against a prior rule.

## Numeric examples

All times in the first examples are in the offering's Africa/Windhoek zone. Course default release is November 10 at 08:00, due November 14 at 17:00 and hard close November 16 at 18:00. Section B sets due November 15 at 12:00. Group G sets a recommended date and leaves due inherited. Enrollment P sets due November 15 at 18:00. P sees release November 10 at 08:00, recommendation from G, due November 15 at 18:00 and the same hard close. P’s instructor can explicitly clear the due time if optional. Submission remains allowed before the hard close, with no lateness derived from the removed due.

A group sets the due date November 17 while hard close is November 16. Return 422 SCHEDULE_WINDOW_CONFLICT, identifying the field, winning scope and hard close. Never silently clamp the due time. Two groups both rank 10 and set different dates for P. Reject configuration or membership changes introducing the conflict unless another authorized overriding policy resolves it. An existing conflict discovered from legacy import blocks new starts with an administrative diagnostic.

A self-paced enrollment starts October 30 at 15:00 in America/New_York and due is three local calendar days after the anchor. The resolved due is November 2 at 15:00 standard time, a 73-hour difference across the fallback. An explicitly configured 72 elapsed hours yields November 2 at 14:00. Store which offset type the author selected.

For Boolean gate all(A complete, any(B complete, C approved)), a learner with A complete and C approved can open. A learner with A complete and a pending B grade does not open unless C is approved. Return a neutral pending-step explanation and keep raw B results private until published.
