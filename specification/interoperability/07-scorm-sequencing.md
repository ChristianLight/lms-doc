# 07. SCORM 2004 sequencing, navigation and rollup

## 07.1 Behavior model and support boundary

SCORM 2004 sequences the activity tree of one selected package organization for one learner registration. It defines access to a delivered SCO or asset, attempt lifecycle, objective tracking, and aggregation into the package's root. It has no authority over native course prerequisites, enrollment, grades or access. Those remain native controls outside the package. The sequencer runs after the native authorization gate and cannot bypass it.

Implement a separate strategy per supported edition. The underlying Simple Sequencing behavior and edition-specific adjustments are part of conformance. Code below gives a state architecture, transaction boundary and implementation-oriented summary. Where the ADL edition documents define specific pseudocode branches and exceptions, implement and test those branches with their process identifiers. The official sample runtime helps cross-check expected transitions and includes sample-specific choices. It is not a replacement for the specification or conformance vectors.

Support declarations distinguish parser, RTE and sequencer. A deployment with 2004 RTE and a single-SCO launch adapter may say which packages it runs. A declaration of full edition support requires its edition-specific package, RTE, sequencing and navigation tests. A mixed package cannot silently switch to linear ordering when it requires author rules.

## 07.2 Immutable activity definition

Every package organization yields one tree. Its root is the organization and the child's sibling order is the manifest order until transformed by an authored selection or randomization rule. Validate a unique occurrence identifier per edition scope, at most one parent per non-root occurrence, complete parent references, no cycle and no orphan. SCO and asset leaves reference immutable package resources. Aggregations are clusters. Reject or flag a resource-bearing non-leaf according to edition content model restrictions. The same SCO resource can occur twice with different manifests or policies. Occurrence identity scopes every attempt and rule lookup.

| Definition group | Fields and defaults before edition-specific restrictions |
| --- | --- |
| Topology | `organization_id`, immutable `activity_id`, manifest ID, parent activity or null, source sibling ordinal, launch resource or null, kind root/cluster/SCO/asset, presentation title and `is_visible` true. Visibility affects presentation. Access still requires valid sequencing. |
| Sequencing controls | Choice true, Choice Exit true, Flow false, Forward Only false, Use Current Attempt Objective Information true, Use Current Attempt Progress Information true. These controls are interpreted in their edition-defined ancestor or child context. |
| Choice constraints | Constrain Choice false, Prevent Activation false. Retain declared edition extensions with exact scope. |
| Limits | Attempt count control and limit. Attempt/activity absolute and experienced duration controls, and available-time conditions where applicable. Absent is different from a present zero. Apply only controls defined as operative by the selected edition profile. |
| Authored rules | Separate ordered lists for precondition, postcondition and exit conditions. Each has exact action, all/any combination, condition operands, optional referenced objective, comparison threshold and negation. |
| Rollup controls | Rollup objective satisfied status true, Rollup progress completion status true, objective measure weight 1, and 4th Edition progress weight 1. Keep rule order, action and child selection quantifier. |
| Rollup consideration | Required for satisfied, not satisfied, completed and incomplete independently. The default is always. Other values identify an attempted, not-skipped or not-suspended activity as specified. Keep the satisfaction-if-active behavior from the declared edition. |
| Selection and randomization | Selection timing and randomization timing each default never. Optional select count is separate from selection timing. Reorder children defaults false. Enforce valid timing and count combinations at import. |
| Tracking | Tracked true, completion set by content false, objective set by content false. Keep separate runtime status and standard-derived tracking defaults. |
| Objectives | Ordered primary and auxiliary local objectives, satisfied-by-measure flag, normalized threshold, rollup contribution and global mappings. The selected edition supplies the exact omitted defaults. |
| Presentation | Edition-defined hide navigation controls plus allowed package layout metadata. This controls LMS presentation, never authorization for a request. |

Compile referenced sequencing declarations into typed immutable values. Keep namespace-qualified names, source line and file where possible. Compile a control-flow index of parent, ancestors, selected-sibling positions and manifest order. Do not compile all possible traversals from the full tree because current objective status, flags, availability and limits can change. Test extension support before publication. Unknown execution-affecting rules block standard mode. A package-specific compatibility decision is recorded as separate evidence.

## 07.3 Durable sequencing and tracking state

The interoperability domain owns these records. Common audit fields and exact API shapes live in the interoperability catalog. The table adds constraints needed by the sequencer.

| Record | Required state and cardinality | Query and retention |
| --- | --- | --- |
| `PackageSequencingState` | One per registration and organization. Immutable definition version, monotonic revision, current occurrence or null, suspended pointer or null, active path, session state, next attempt counters, and deterministic selection state per cluster. `current` can reference a recently ended leaf before the next valid request. Current and suspended pointers are not interchangeable. | Unique registration and organization. Index registration plus revision. Retain while registration remains resumable. Archive final revision with navigation receipts. |
| `PackageActivityAttempt` | Zero or more per occurrence within a registration. Attempt ordinal starts at 1. Parent attempt identity is nullable only for root. Start/end and suspended/resumed times, state active/suspended/ended/abandoned, known flags, completion status, progress measure, current absolute and experienced duration, and link to current SCO state. | Unique registration, occurrence and ordinal. Index current active/suspended attempts by occurrence and latest attempt by parent lineage. Preserve history for evidence and retention. |
| `PackageObjectiveState` | One row per attempt and local objective identity. Persist separate known flag and value for satisfaction and normalized measure. The 4th Edition profile also has independently known completion, progress, raw/min/max fields where applicable. Mapping provenance and source revision accompany a global projection. | Unique learner, Institution, resolved scope key and objective. Include the exact activity attempt in local scope, the root attempt where required, and omit attempt identity only for declared cross-attempt scope. Index reverse mapping subscriptions by resolved global scope and global ID. Restrict access to learner-specific tracking evidence. |
| `PackageNavigationReceipt` | Immutable result of one accepted idempotent command, with source UI/SCO/system, request/target, prior and resulting sequence revision, old/new occurrence and attempt IDs, outcome, terminal causes, and ordered bounded transition trace. | Unique registration and request ID. Index registration and result revision. Keep receipt at least as long as replay can occur. Retain an audit projection after trace expiry where permitted. |
| `PackageSequencingRule` | Immutable rule owner occurrence, rule family, sibling ordinal, action and typed condition list, including source path. Every rule belongs to one immutable PackageVersion. | Unique activity, family and ordinal. Index referencing objective IDs and rule dependencies for diagnostics. |

An activity cannot be active and suspended simultaneously. At most one leaf is active for one registration and organization. Active clusters form its ancestor path, except while a completed delivery awaits an acknowledged navigation decision. A selected child list is a frozen projection of one immutable source sibling list. A previously suspended attempt resumes its selection, randomization and attempt lineage. Never replace its pinned list using a newly installed package or a different seed.

Store clock intervals as timestamps and integer duration components. Absolute duration includes suspended gaps when defined. Experienced duration includes only experienced intervals. A suspended interval does not add experienced time. Institutional business rules can cap or disregard package-reported duration for reporting, while the original evidence remains available according to policy. Implement every edition's operative limit. A parsed limit which the supported edition deactivates does not accidentally become a native authorization rule.

## 07.4 Selection and randomization

1. For an applicable cluster, start with the definition's ordered children. For timing `once`, read or set the first applicable materialization for the package attempt scope. For `onEachNewAttempt`, use the identified cluster attempt number and its parent attempt lineage. For `never`, use the original list without an order mutation.
2. When selection is active and a selection count is present, select a subset without replacement using an auditable seed. Retain source order among chosen children until a separate randomization stage is applied. A select count of 0 must follow the edition binding and cannot silently become all children.
3. When reorder is active, shuffle the selected available children. One permitted implementation is a Fisher–Yates permutation fed by a deterministic cryptographic seed derivation. Record the algorithm version, generated seed reference and output occurrence IDs. Never reveal a secret seed to the package or learners.
4. Commit the selected order before delivery. Keep the order through resume, delivery retries, validity previews and server failover. Do not rerun selection for a cluster that is already active or suspended. Newly attempted clusters receive a new order only when timing requires it.
5. Unselected children are excluded from the current available tree. An unselected child's prior attempt remains auditable. A different use of the same resource is a different occurrence and can remain eligible elsewhere in the tree.

Example. Cluster P contains A, B, C and D. Its count is 3 and initial selection is A, C and D. A separate declared randomization makes the active order D, A, C. Continue from D goes toward A. Resume at A still has C after it. A second attempt on P reselects only if its timing says so. A speculative validity query cannot consume a new seed, reshuffle the live list or add to the attempt count.

## 07.5 Rules and three-valued conditions

Use **true**, **false** and **unknown**. A completion predicate on an unknown status yields unknown. A known-status predicate tests the known flag and returns false when absent. An objective measure threshold compares an exact known normalized value to a declared decimal threshold. A missing referenced measure yields unknown. Negating unknown preserves unknown. An all-list is false if any member is false, true when all are true, and otherwise unknown. An any-list is true if any member is true, false when all are false, and otherwise unknown. A rule triggers only on true. Empty authored condition lists fail validation when the binding requires a condition.

| Predicate | Inputs and result |
| --- | --- |
| `always` and edition-defined `never` | Constant true or false. |
| `satisfied` | Objective progress known flag and satisfied value. Unknown unless known. |
| `objectiveStatusKnown` | Known flag of the referenced or primary objective. |
| `objectiveMeasureKnown` | Known flag of the referenced or primary objective normalized measure. |
| `objectiveMeasureGreaterThan`, `objectiveMeasureLessThan` | Strict comparison against the authored normalized measure threshold. Equality fails both. |
| `completed` | Attempt progress known flag and completion status of the relevant activity tracking context. |
| `activityProgressKnown` | True when progress is known, otherwise false. |
| `attempted` | Applicable attempt exists in the edition's selected tracking context. |
| `attemptLimitExceeded` | Evaluate declared count control against the applicable attempt count. Starting an attempt and resuming an existing one have distinct effects. |
| `timeLimitExceeded`, `outsideAvailableTimeRange` | Use only when the edition binding and behavior make the relevant condition operative. Evaluate against the edition clock and declared control, never client timestamp alone. |

The precondition family includes `skip`, `disabled`, `hiddenFromChoice`, `stopForwardTraversal`. The same node can qualify for distinct actions in different evaluation processes. Filtering for skip must not silently evaluate a hide rule as a skip rule. Skip affects flow selection. Disabled prevents delivery. Hidden from choice governs Choice eligibility and does not automatically block Flow or Jump. Stop forward traversal can block a Choice across intervening forward activity. This is distinct from hiding or disabling the target itself.

The exit-condition family supports the edition's exit action. Traverse active ancestors in the order specified by the edition's exit-action process and close descendants before ending an exiting ancestor. The postcondition family includes `exitParent`, `exitAll`, `retry`, `retryAll`, `continue` and `previous` where allowed by the profile. Evaluate ordered rules only at the first candidate defined by the termination process. An eligible postcondition can replace the caller's requested next action. Continue from a closed or abandoned scope cannot be simulated by a rule engine that ignores which attempts have ended.

## 07.6 Overall sequencing transaction

Use an optimistic revision check at the boundary and a serialized per-registration transition internally. The terminal SCO journal and navigation intent can be received together. The RTE records a successful terminal receipt before a fresh launch grant can be emitted. If the grant service fails after sequencing is committed, reissue a grant for the reserved delivery. Do not repeat the sequencing transaction or increment the attempt count twice.

```text
request_navigation(registration, caller, request, expected_revision, idempotency_key):
    verify_native_access(registration, caller, registration.organization)
    begin_serialized_transition(registration)
    prior = find_receipt(registration, caller, idempotency_key)
    if prior exists:
        verify_request_fingerprint(prior, request)
        return prior
    check_exact_revision(expected_revision)
    snapshot = load_definition_attempts_and_committed_sco_state()
    operation = edition.validate_navigation(snapshot, request)
    if operation.rejected:
        return store_rejection_receipt_without_state_change()
    terminal = edition.terminate_if_required(snapshot, operation.termination)
    apply_mapped_tracking_and_rollup(terminal)
    sequencing_request = terminal.override_or(operation.sequencing)
    candidate = edition.traverse(snapshot, sequencing_request)
    validate_candidate_delivery_and_native_scope(candidate)
    if candidate.deliverable:
        edition.end_old_branch_prepare_new_branch_and_begin_or_resume(candidate)
    return commit_new_revision_receipt_and_delivery_outbox()
```

A rejected navigation request must not end the active activity before the selected edition's navigation validation rules allow it. Distinguish prevalidation failure from an allowed termination that yields no subsequent delivery. In the second case, commit the valid terminal work and return a bounded outcome such as end session or waiting for request. Never synthesize a fallback first leaf.

| External or internal request | Preconditions and edition operation |
| --- | --- |
| Start | New sequencing session with no current activity. Build initial available lists as required. Apply forward traversal from the root. A package with no permitted leaf yields the edition's explicit no-delivery outcome. |
| Resume All | No current activity and a durable suspended activity. Construct the suspended branch using frozen selections. Restore an eligible suspended leaf or apply edition-defined behavior for a suspended cluster. Resume does not allocate a new attempt merely to regain communication. |
| Continue | Current activity exists and the applicable parent allows flow. End active current activity when necessary and evaluate exit/postcondition rules. Traverse forward from the first candidate selected by termination. At exhaustion apply edition end-session rules. |
| Previous | Current activity exists, its applicable parent allows flow and forward-only controls permit this request. End the active current activity as required and traverse backward with the edition's cluster-entry handling. |
| Choice | Target exists in the current organization. Validate its Choice eligibility, applicable Choice Exit controls, selected ancestry, hidden rules and traversal constraints. Terminate the current activity only if that navigation request is valid. Resolve the requested target or the first deliverable descendant of an eligible flow cluster. |
| Jump | 4th Edition request targets an edition-permitted activity occurrence directly. It uses Jump validation rather than Choice traversal and can reach a leaf hidden from Choice. Still apply selected-activity, delivery and attempt conditions required by the edition. Never expose Jump as an unrestricted learner navigation button. |
| Exit | End the current active activity, update tracking, evaluate exit and postcondition rules and leave an appropriate sequencing state. An isolated leaf Exit does not mean Exit All. |
| Exit All | End the applicable active branch through the root and close the sequencing session. Use the edition-specific process rather than manufacturing individual learner requests. |
| Abandon | Discard the current attempt's applicable tracking effect per edition and close that activity. Do not run normal postconditions for Abandon. Record a distinct outcome from successful completion. |
| Abandon All | Apply abandonment to the active branch and close the sequencing session. Preserve immutable security/audit evidence according to policy without projecting it as completed tracking. |
| Suspend All | Mark the edition-determined active branch suspended and record the suspended activity. Clear current delivery and close the sequencing session without completing suspended attempts. |
| Retry and Retry All | Internal requests produced by applicable postconditions. Resolve them through the edition's retry and limit processes. A retry can start a fresh allowed attempt and must retain the earlier attempt's history. |
| No request | No implicit Continue. A normal SCO Terminate can still require closing the current delivery and evaluating the appropriate edition termination behavior. |

Postcondition control-flow cycles are possible with malicious or ill-configured packages. The engine records one bounded trace and applies a transition-step budget. Use a deterministic maximum of 10,000 tree visits and 1,000 rule transitions per command in the baseline service. An exceeded budget returns a diagnostic incident and blocks additional automation for the affected launch. Preserve already accepted RTE data and do not silently advance the learner. Any retry starts from the committed revision rather than a partially applied tree walk.

## 07.7 Flow, Choice and delivery implementation

### Flow traversal

Use an iterative cursor over the available tree with current occurrence, direction, entry direction and the path to the root. A candidate needs the relevant parent's Flow enabled. Move among selected siblings and ascend or descend through available clusters. Apply skip to the current candidate or branch according to the edition's Flow processes. Check disabled and applicable limits on entry. If a cluster allows Flow, descend to its first selected child for forward entry or the edition-determined backward entry. Do not confuse forward-only backward-entry special behavior with permission to move backward among siblings. The 4th Edition reference behavior can enter a forward-only cluster backward via its first child and switch direction forward. Record this case explicitly in tests.

Distinguish `candidate_deliverable`, `candidate_blocked`, `traversal_exhausted` and `sequencing_session_ended`. Skipping a branch can permit a later candidate. Encountering an unskipped but disabled activity is not universally equivalent to skipping it. Follow the edition's outcome for the exact process stage. Start can begin traversal at the root. Continue and Previous start from the first candidate after termination, which may be an ancestor due to an exit action.

### Choice traversal

Normalize target lookup to one manifest occurrence in the selected organization. Check the target and its selected ancestors. Check hidden-from-choice rules along the target path. Then locate the lowest common ancestor with the current activity, or use the root when the session has no current activity and the edition permits Choice from that state.

| Path relationship | Traversal obligations |
| --- | --- |
| Current equals target | Permit only if the edition's same-activity rules, exit processing and delivery validation allow it. A resume is distinct from a fresh attempt. |
| Same parent | Determine traversal direction using current available sibling positions. Enforce stop-forward or forward-only restrictions on applicable steps. |
| Target is descendant | Walk down the path. Confirm required Choice controls, selected branches and no forbidden activation. An inactive protected ancestor can block direct entry. |
| Target is ancestor | Walk up the current path and validate applicable Choice Exit constraints. Do not simply deliver an aggregation node. A deliverable descendant may require Flow. |
| Cross-branch | Validate Choice Exit along the exiting path, evaluate constrained-choice set, then validate entry controls along the target branch. Inactive target ancestors can have Prevent Activation. |

Once target traversal succeeds, test leaf eligibility or run the edition's cluster-to-leaf Flow entry process. If the target is a cluster with Flow disabled and the profile supplies no direct leaf, produce no delivery rather than launching an arbitrary first resource. In 4th Edition, Jump uses its distinct target evaluation and can bypass Choice-specific restrictions. It is not interchangeable with selecting that target from a table of contents.

### Delivery and first attempt versus resume

Delivery validates leaf, resource and the complete path to root using the edition's delivery request process. Do not deliver a cluster directly. Require an intact release snapshot, available item, all applicable limit checks, authorized placement, learner enrollment, and browser security compatibility. These guards are repeated at commit when a validity query was made earlier.

Transition out of the previous branch through the common ancestor. Close, retain or resume attempts according to current state and edition rules. Create fresh attempts on inactive new branch nodes in root-to-leaf order. Mark the leaf active, update current pointer and initialize its learner-session projection. Restore suspended state without incrementing attempt count where the process selects resume. Persist the navigation receipt, attempt identities, new revision and delivery reservation together. Emit the browser launch response only after the state is committed.

## 07.8 Objective mappings and rollup

Local objectives belong to one activity context. Primary objective is the objective contributing to rollup when configured. Maintain separate values and known flags for objective satisfaction, normalized measure, completion and progress. Missing, false and numeric zero must be different values.

A global objective has a declared scope and identifier. Read/write mappings are per local objective, field and direction. Map normalized measure and satisfaction in the base profile. Apply raw/min/max scores, completion and progress measure only where the 4th Edition mapping extension defines them. Do not copy undeclared fields between SCOs. Use the manifest's global scoping rules within the LMS's mandatory institution and learner isolation. A scope with attempt lifetime includes the exact root attempt in its key. An authorized global objective can survive a root retry and can be mapped across approved trees. Its key is independent of the current registration ID. System-global package scope does not permit cross-learner sharing or cross-tenant writes. Keep an immutable typed map plus reverse dependencies. Reject an ambiguous writable mapping that cannot be resolved under edition rules and this product's tenancy policy.

When a SCO attempts to finalize its tracking, use committed RTE values and edition-derived completion/success. Apply completion/content-set and objective/content-set policies at the correct end-attempt step. Some leaf attempts get default tracking completion or objective satisfaction when content was not required to set the value and did not report it. An explicit unknown from the content and an omitted value are separately representable. Do not apply normal end-attempt defaults while a leaf is suspended. Recompute affected clusters from deepest to root, and include clusters affected by authorized global objective writes. Evaluate the entire propagation under the same tracked revision.

| Rollup operation | Algorithm and edge cases |
| --- | --- |
| Objective measure | Over edition-eligible tracked children with known normalized objective measure and positive weight, compute `sum(measure × weight) / sum(weight)`. Unknown children do not act as numeric zero. No contributing weight produces unknown. Respect the selected edition's rules for inactive/suspended attempts and data inherited through objective mappings. |
| Progress measure | In 4th Edition, use the independent known progress measure and progress weights. Compute the weighted fraction of eligible known contributions. No contributing weight produces unknown. This fraction is not interchangeable with objective measure. |
| Objective satisfaction | Apply edition Rollup Objective Satisfied controls. If the primary objective is satisfied by measure, compare its rolled-up normalized measure against its own threshold with equality satisfying it. Otherwise evaluate the applicable satisfaction and not-satisfied rules and preserve unknown where no authoritative result exists. |
| Completion status | Apply the Rollup Progress Completion controls. For a 4th Edition cluster completed by measure, compare the progress measure to the threshold. Otherwise evaluate completion and incomplete rules. |
| Rule child set | Form an eligible set based on selected available children, tracked status, delivery mode, action's rollup consideration and applicable current-attempt controls. Then evaluate each child's three-valued predicate. Quantifier is all, any, none, at least count or at least percent. Use the edition's exact treatment of empty and unknown cases rather than generic language collection methods. |
| Missing custom rollup rules | Use edition default rules independently for satisfaction and completion. In the 4th Edition baseline, known non-final child information can establish an incomplete or not-satisfied aggregate until an all-required positive condition succeeds. If relevant evidence is entirely unknown, preserve unknown. |
| Required For conditions | For each action, evaluate its own always, if attempted, if not suspended or if not skipped scope under the edition behavior. Do not prefilter all rollup rules with one shared list. |
| Current-attempt scope | When configured, an ancestor uses child tracking from its current attempt lineage. Preserve previous child attempts for audit but do not let them silently satisfy the new parent attempt. |

Worked rollup example. Root has three selected tracked children with objective weights 1, 3 and 4. A and B report normalized scores 0.8 and 0.6. C reports unknown. Objective measure is `(0.8×1 + 0.6×3) / (1+3) = 0.65`. A root objective threshold of 0.65 is satisfied. A and B separately report progress measures 1.0 and 0.4 with progress weights 2 and 1. Progress rollup is `(1×2 + 0.4×1) / (2+1) = 0.8`. A 0.9 completion threshold leaves root incomplete despite objective satisfaction. If C later reports known zero normalized measure, it contributes its denominator weight and the objective measure becomes `2.6/8 = 0.325`.

Worked rule example. Four eligible children have completion results true, true, false and unknown. An `atLeastCount(2)` completed rule passes. An `all` completed rule does not. A different action's `ifAttempted` gate can exclude the unknown unattempted child, but the remaining false child still prevents all-completed. For `atLeastPercent`, use the edition-defined threshold conversion and fixture expected outcome near boundaries. The ADL 4th Edition reference implementation compares true count with `floor(p × eligible_count + 0.5)` for nonempty eligible sets. Confirm the normative edition and official cases before substituting a generic ratio comparison or another rounding rule.

## 07.9 Player controls, audit and support

The player renders controls for the permitted navigation sources. For a valid resume, label the action Resume and identify the relevant activity when accessible. Continue and Previous update their available state from a versioned snapshot. Do not show an arbitrary Next action as enabled merely because the activity has a following manifest sibling. The table of contents marks hidden, unavailable or unselected items using the selected edition's rules. Respect permitted author hiding of LMS controls. Provide screen reader accessible names, a status region for rejected actions, preserved keyboard focus after recoverable errors and a clear reason when a learner cannot advance.

A validity preview uses a cloned, immutable working state and the same edition engine. It cannot write objectives, allocate attempts, consume random seeds or send analytics. Return the current sequence revision and tri-state validity. Any execution request is reevaluated after relevant state changes. A preview for one target does not authorize a later call. Author and administrator diagnostics may expose node IDs, phase, edition subprocess and rule result without disclosing answer keys or other learners' state.

Use stable outcomes such as `DELIVERED`, `WAITING_FOR_REQUEST`, `SEQUENCE_ENDED`, `NOT_VALID`, `DELIVERY_BLOCKED`, `STALE_STATE`, `PROFILE_UNSUPPORTED` and `TRANSITION_BUDGET_EXCEEDED`. Map these to private diagnostic labels and the appropriate external API, without exposing backend internals to the SCO. One replay with the same idempotency key and request returns the prior receipt. A changed payload with that key is rejected. An API client can reread the current revision and request validity before attempting a fresh command.

## 07.10 Synthetic fixtures and conformance gates

| Trace | Setup and execution | Expected result |
| --- | --- | --- |
| SN-001 resource reuse | Two leaf occurrences reference the same SCO resource. Attempt one, suspend, then start the other under allowed navigation. | Independent occurrence state, attempt count and bookmarks. Shared state appears only through an explicitly permitted store or objective mapping. |
| SN-002 branching | Root Flow is enabled. A is available. B has an applicable skip precondition while its prerequisite objective is unknown. C is available. Start, close A, Continue. | Flow treats unknown according to the actual rule predicate. For a condition of `not objectiveStatusKnown`, B is skipped and C is selected. Replacing it with `not satisfied` while satisfaction is unknown does not trigger skip. |
| SN-003 active branch exit | Current A is inside protected cluster P. Target B is inside sibling cluster Q. P denies Choice Exit. | Choice rejected during the applicable validation, with active A and its bookmark unchanged. Authorized normal Exit follows its distinct process. |
| SN-004 backward entry | Traverse backward into a cluster that is forward-only, with children X and Y. | Exercise the edition's backward cluster-entry branch and record the first-child/direction-switch outcome where applicable. A direct Previous prohibited by current parent remains invalid. |
| SN-005 selection stability | Cluster P selection and order materialize as D,A,C. Suspend at A, validate Continue from a separate view, then Resume All. | A resumes on the same attempt. The selected list is unchanged, and a later Continue follows C. |
| SN-006 postcondition override | A's first true postcondition requests retry. Learner selects Continue with an attempt slot remaining. | Engine closes first attempt A, evaluates its postcondition, starts a fresh A attempt and reserves a single delivery. A duplicate command returns the same receipt. |
| SN-007 abandon distinction | Package reports an uncommitted passed result on A. Authorized Abandon ends the active delivery. | No fabricated pass from the abandoned working state. Retain allowed audit cause and distinguish from normal termination. |
| SN-008 jump versus choice | B is selected and otherwise deliverable but hidden from Choice. In 4th Edition compare Choice and explicit package Jump to B. | Choice unavailable. Authorized 4th Edition Jump can resolve B under edition Jump validation. A 3rd Edition profile rejects the Jump capability. |
| SN-009 known-zero rollup | Use the weighted example in §07.8, first without C's measure and then with zero. | Root scores exactly 0.65 then 0.325, with stable raw and projected tracking. |
| SN-010 shared objective propagation | A writes a global measure 0.72 under a valid mapping. B has permission to read the measure and a precondition comparing it with 0.7. C maps only status. | B's rule can observe 0.72 after the authorized commit. C does not acquire the score. A separate learner sees unknown. |
| SN-011 stale concurrent navigation | Two tabs get revision 12. One valid Continue commits revision 13. The other tries Previous against 12. | Previous is rejected stale. Only one new attempt is started. Replay the accepted Continue key without allocating a second attempt. |
| SN-012 launch response lost | End active A and commit delivery reservation for B. Browser loses response before loading B. | Reread the receipt and reacquire B's authorized launch grant. B's attempt counter and A's session time change only once. |
| SN-013 no possible delivery | All eligible children are skipped or barred, according to profile. Start or Continue reaches the edition no-delivery branch. | An explicit no-delivery or end-session result is returned. Native LMS does not silently open the first package file. |

For each supported edition, maintain a matrix of navigation request validation, termination outcomes, flow and Choice traversal branches, content delivery, limits, all known/unknown combinations, selection timing, default and authored rollup and ADL extensions. Match official test assertions to stable internal trace points. Conformance fixtures test the same runtime deployed in production with actual browser navigation and cross-origin controls. Synthetic tests complement them with hostile manifests, version mismatches, duplicate requests, disconnects and tenant isolation. Do not advertise a successful edition profile until the production-equivalent version passes the applicable official vectors.

## 07.11 Normative and reference material

- [1EdTech Simple Sequencing Information and Behavior Model 1.0](https://www.imsglobal.org/simplesequencing/ssv1p0/imsss_infov1p0.html)
- [1EdTech Simple Sequencing XML Binding 1.0](https://www.imsglobal.org/simplesequencing/ssv1p0/imsss_bindv1p0.html)
- [ISO/IEC TR 29163-4, SCORM 2004 3rd Edition Sequencing and Navigation](https://www.iso.org/standard/53537.html)
- [ADL SCORM 2004 4th Edition book archive](https://lms.technology/SCORM20044_index.html)
- [ADL 4th Edition Testing Requirements](https://adlnet.gov/assets/uploads/SCORM_2004_4ED_v1_1_TR_20090814.pdf)
- [ADL 4th Edition reference sequencer](https://github.com/adlnet/SCORM-2004-4ed-SampleRTE/tree/master/src/org/adl/sequencer)
- [ADL 4th Edition conformance test suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite)
