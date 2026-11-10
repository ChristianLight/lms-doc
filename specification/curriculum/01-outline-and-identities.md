# 01. Outline, identities and placement validation

## Write ownership and identity

Curriculum owns course metadata, reusable learning definitions, drafts, publication snapshots, library distributions and asset references. Participation owns course offering schedules, enrollment release assignments and learner progress. Assessment owns question and assessment definitions, attempts and marking. Academic Records owns authoritative grades and formal reports. An activity placement can reference an assessment version without copying its answers or changing its rubric.

All persisted identities use UUIDs. Importers retain source keys in the transfer mapping and use the generated identifier for internal links. Business codes use case-insensitive uniqueness within the stated institution or owner scope. UUIDs, asset digests and names solve different problems. A digest verifies bytes, a business code supports discovery, and a UUID remains a reference after a move or rename.

| Identity | Assigned by | Remains stable when | Receives a new identity when |
| --- | --- | --- | --- |
| Course ID | Curriculum | Code alias, owner, title, publication or delivery mode changes | Staff clone an independent course |
| CourseDraft ID | Curriculum | Authors edit, return from review or resolve an import into the same draft | Authors fork a separate working draft |
| CourseVersion ID | Curriculum | An immutable version is scheduled, activated, archived or reactivated | Publication creates a new snapshot |
| ContentNode ID | Curriculum | Body, locale, assets or title changes | A copy becomes independently editable |
| ContentNodeVersion ID | Curriculum | Authors reuse that exact immutable revision | A changed definition is sealed |
| Activity ID | Curriculum | Shared instructions or interaction settings change | The activity is copied independently |
| ActivityVersion ID | Curriculum | An offering uses the same definition | Instructions, settings or pinned dependencies are sealed anew |
| Placement key | Curriculum | A pedagogical occurrence is renamed or moved within its own course | Authors duplicate it, move it into an independent course or replace its pedagogical role |
| ContentPlacement ID | Curriculum | A pinned course version remains available | A new course version materializes the placement, even if the stable key is reused |
| Asset ID | Curriculum | A new file is approved for the same logical resource | Staff create a separate resource with different use rights or purpose |
| AssetVersion ID | Curriculum | Identical approved file reference is reused | Bytes, provider object identity, license or canonical accessible representation changes |

Externally published links contain offering ID and stable placement key. They resolve through the requester's currently effective enrollment release. Administrative historical views include the course version and exact placement ID. A deleted key can have a curated current redirect only within the same course. Validate authorization on the destination and use a generic missing response when source visibility would disclose hidden content. Retain the original key and its former exact version for academic history.

## Aggregates and transaction scope

| Aggregate | Fields relevant to storage design | Keys and retention |
| --- | --- | --- |
| Course | Institution, owner unit, normalized code, public title, summary, default locale, state, active catalog revision, lock revision | Unique institution plus normalized code. Index institution, unit and state. Archive while referenced by offerings or academic records |
| CourseDraft | Course, base publication if any, owner principal, workflow state, revision, last reviewed digest and timestamp | Index course and state. Stale abandoned drafts eligible for scheduled purge after holds and reference checks |
| DraftPlacement | Draft, stable placement key, optional parent stable key, sibling position, display kind, one payload reference, visibility and completion references, optional alias | Unique draft plus placement key and draft plus derived sibling scope key plus position. Index parent for child list and payload identity for usages |
| CourseVersion | Course, publication number, exact outline digest, manifest storage key, authoring draft digest, approving and publishing principals and time | Unique course plus publication number and course plus approved draft digest. Index course plus published instant. Preserve while referenced by history |
| ContentPlacement | CourseVersion, stable placement key, optional parent placement ID, contiguous order, display kind, payload version, gate and completion version references | Unique course version plus stable key and course version plus derived sibling scope key plus order. Index payload version for impact checks |
| ContentNodeVersion and ActivityVersion | Stable definition, monotonically assigned revision, type revision, canonical typed payload, manifest digest, provenance and author | Unique stable definition plus revision. Index definition plus created instant. Immutable once sealed |

A draft uses stable keys for edits and has a virtual root whose children have a null parent. Persist a non-null sibling scope key derived as root for a null parent and parent/ followed by the canonical lowercase parent UUID otherwise. For drafts derive it from the stable parent key. For publications derive it from the exact parent placement ID. Check the derivation on every insert or reparent. The unique position key then applies to the virtual root even when the storage engine treats nulls as distinct. Assign each sibling an integer position from 0 without gaps. A persistence layer with immediate unique checks on position can perform renumbering through temporary positions outside the normal range within the transaction, or use deferrable uniqueness. The committed state must satisfy contiguous positions.

One draft can contain at most 20,000 placements, 512 siblings at any parent and 12 ancestor levels. A module groups topics or lessons. A topic groups other topics or lessons up to the global depth bound. A lesson groups resources and activities. Root allows modules and lessons to support short courses. A resource and an activity are leaves. The course has at least one learner-visible lesson to publish unless it is deliberately a catalog-only course with no active offering. Staged imports may be incomplete but must preserve source ordering and report unmapped locations.

Payload references are an exclusive union. A structural node or resource has one ContentNodeVersion. An activity has one ActivityVersion. A typed internal link is a resource with a validated destination key. An activity link never carries its own answer key or learner-specific state. All references must belong to the same institution or to an explicitly licensed and published shared source. Publication copies referenced identifiers, content digests and applicable policy versions into a manifest in deterministic depth-first order.

## Outline mutations

Every mutation supplies the draft revision from its last read. Lock the draft or use a compare-and-swap update. A successful edit increases revision exactly once for the entire change and clears any approval on the earlier digest. A stale draft edit returns 409 DRAFT_CHANGED with the current revision and conflicting keys. The client can rebase when server changes touch different placements and parent ordering has not changed. Reparenting and concurrent position edits require an explicit review of the merged order.

| Operation | Preconditions | Atomic effects |
| --- | --- | --- |
| Insert | Parent exists, compatible payload, no duplicate client placement key, valid position | Create key and row, insert into sibling list, renumber, validate scope and record edit |
| Reorder or reparent | Source exists, target parent exists or is root, target is outside source subtree | Remove source, insert at requested index in the list after removal, renumber both affected lists and revalidate descendants |
| Duplicate subtree | Source is accessible and target depth/count limits fit | Allocate all new placement keys, copy in traversal order, rewrite in-subtree links and gate references, retain outside links where valid, record old-to-new map |
| Remove subtree | Caller confirms dependency report and supplies approved remedies | Remove draft nodes and associated placement-local settings, replace or remove inbound draft references as specified, preserve published history |
| Replace definition | New payload kind fits and entitlement is valid | Seal or link new definition revision, update placement pointer, report any equivalence decision needed for rollout |
| Validate | Draft revision and references available | Persist validation summary against digest, including exact key and fault path. Concurrent draft edit invalidates result as a publication input |

Validate structural legality with one traversal and a parent map. Check parent kind, positions, depth and reachability. Build a directed dependency graph separately from the outline using placement prerequisite edges and any transitive blocking parent gates. Detect dependency cycles using a topological walk. An inaccessible requirement can also occur without a cycle when every branch refers to a hidden or unpublished activity, or when its earliest possible availability is at or after the dependent close. Reject cases proven unsatisfiable. Report uncertain dependencies for human review, with exact keys and affected audiences. Repeat publication checks after resolving staged forward references and against the exact frozen dependency set.

## Worked fixture

A course version contains module M, lessons A and B, a math explainer R in A and a quiz Q in B. Duplicating A beneath M creates A2 and R2. The explainer revision can remain shared. Completion for R stays distinct from R2 because progress identity includes enrollment release and occurrence. An in-subtree jump from R to A is rewritten to A2 in the copy. A prerequisite on Q remains pointed at Q. Moving A2 ahead of A changes sibling positions but preserves its key. Publishing version 2 creates exact new placement row IDs for M, A, R, A2, R2, B and Q and preserves the stable keys of all surviving occurrences. An attempt originally started from Q in version 1 still resolves version 1’s exact placement.

| Test | Expected observable result |
| --- | --- |
| A is moved under its own descendant | 422 OUTLINE_CYCLE and no revision advance |
| Staff from a different institution references a private asset by UUID | Same inaccessible response used for an unknown resource and no reference committed |
| Two browsers move B from the same draft revision | First committed request wins. The second returns current revision with 409 DRAFT_CHANGED |
| Source link identifies R but the importer copies A and R | New R links only to mapped copies inside the subtree. Outside links remain explicit |
| Removing lesson A would strand an activity with a completion dependency | Removal preview lists the dependent and requires a replacement or explicit draft rule edit |
