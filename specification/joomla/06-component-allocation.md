# Component allocation and Admin View budget

The [component map](component-map.json) allocates every persisted entity in the authored catalogs to one Joomla component, one JCB Admin View definition and one authoritative table. A component handles a small workflow, such as enrollment and release assignments or exam attempts and submissions. The larger domains are service ownership boundaries. The distribution package assembles the components and supplies a compatibility contract. The baseline assigns 240 persisted entities and their 240 Admin View definitions to 66 components. Each component has two to five attached definitions.

This allocation is a design input for the first blueprint build. Its definition keys and proposed SQL names are stable planning identifiers. Bind each definition key to a real GUID after acquisition or authoring and record the result in the build manifest. Inspect generated routes and SQL against the selected compiler before release.

## Budget unit

Count the rows attached to the component by `component_admin_views.addadmin_views`. Each row selects an Admin View through `adminview`. The compiler decodes and sorts the collection, resolves its Admin View data and applies the selected attachment flags. The Admin View's list and item pages are outputs of one definition. A hidden child and a view used only for immutable evidence both consume one slot. Turning off submenu, dashboard and API options changes the exposed surfaces while preserving the attachment. [Component attachment reference](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/reference/component_admin_views.md) · [Compiler Adminviews consumer](https://github.com/vdm-io/Joomla-Component-Builder/blob/408703a857ad937479b1e28de7f693af178dcc83/libraries/vendor_jcb/VDM.Joomla/src/Componentbuilder/Compiler/Model/Adminviews.php)

The hard maximum is five attached definitions per component. A boundary can use fewer when only two or three entities belong together. The baseline also attaches zero Custom Admin Views. Use the standard component dashboard, tabs, task actions and scoped site workspaces for navigation. If an implementation needs a Custom Admin View, revise the allocation and keep the total of Admin Views and Custom Admin Views within five. Check both attachment collections in the imported blueprint. [Component assembly](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/models/component.md) · [Custom Admin View attachment reference](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/reference/component_custom_admin_views.md)

| Counted as one attachment | Presentation of an existing attachment |
| --- | --- |
| A table-owning Admin View, including a table whose generic editing tasks are disabled | Its generated list and item templates |
| An Admin View for the child of a repeated collection | The modal selector for that child or a tab with a related list |
| An Admin View with a private schema and no menu entry | A status or action button on a permitted parent workspace |
| A Custom Admin View attached for a dedicated task, if approved in the allocation | A scoped site view that invokes an owner command |

## Partition algorithm

1. Load all six authored catalogs and build a registry keyed by exact entity name. An entity is separately persisted unless a reviewed catalog change explicitly moves it to a value schema or existing record.
2. Assign each entity to its declared owning domain. For each domain, identify the records that are created, validated or reconciled by one operation. Keep an independently edited normalized child with its editor parent whenever the combined count permits.
3. Place related records together if they share a write lock, lifetime, staff permission boundary or bounded operational workflow. Keep append-only evidence separate from broad CRUD even when attached to the same component. Use a nearby task workflow instead of inventing a new generic menu solely for an evidence table.
4. Split a group at its narrowest stable business boundary before adding a sixth attached definition. For example, separate immutable course publications from live authoring and isolate transfer review from transfer intake. Preserve atomic owner commands across component boundaries within one database transaction where the portable contract requires atomicity.
5. Reserve one immutable component code and one single/list code pair per view. Choose names that remain distinct after compiler sanitization. Use the words corresponding to the planned route codes for the blueprint singular and plural names. For the cmi5 records, spell the digit as a separate word in the planned code because the inspected compiler expands numbers when it derives these names. Reserve the standard dashboard code, case-fold generated class names and check SQL identifiers with the actual database prefix.
6. Verify that every catalog entity occurs exactly once as a table-owning Admin View and that every recognized normalized edit child resolves to its attached view. Generate the reference owner index from the final map.
7. Resolve compile-time blueprint dependencies, runtime owner contracts and optional providers separately. Repeated cross-references in catalog fields produce owner lookups. Keep dependency calls and package readiness checks explicit.

For a later catalog change, allocate a new entity to a cohesive component only if the actual attached view count stays within five. Moving an installed table to a different component requires a reviewed schema migration that preserves application GUIDs, evidence and references. Update the component map, build manifest and migration acceptance before moving the row owner. A display label change belongs in language strings and leaves table and route identity unchanged. Renaming the compiler-facing singular or plural source field needs the route and schema migration review.

## Map contract

| Field | Meaning |
| --- | --- |
| `manifest_version` | Version of the allocation format |
| `allocation_status` | Planning or verified status of this map. This allocation has design status |
| `package_code` | Required Joomla distribution package for the allocated components |
| `component_admin_view_limit` | Hard upper bound on attachments per component |
| `persistence_policy` | Defaults for application GUID, local key, generated exposure and cross-component reference enforcement |
| `components[].code` | Stable extension code. Its suffix reserves the normal standard dashboard route |
| `components[].domain` | Canonical catalog owner for every attached entity |
| `components[].workspace_entity` | Primary administrator workspace for this component. Site access and roles are supplied by the implementing feature |
| `components[].admin_views[]` | One allocation per independently persisted entity |
| `admin_views[].definition_key` | Stable planning key bound to an actual JCB definition GUID in the build manifest |
| `admin_views[].single_code` and `list_code` | Proposed singular and plural route code to compare with compiled output |
| `admin_views[].table` | Proposed Joomla-prefixed table name. Keep it stable when an approved compiler override is needed |
| `admin_views[].visibility` | `workspace` for the primary submenu entry or `internal` for a related view without default menu or dashboard exposure |
| `components[].custom_admin_views[]` | Empty in this baseline. An approved additional Custom Admin View needs a unique definition key and view code and consumes one slot |
| `normalized_edit_groups[]` | Explicit cases where an editor loads and stages rows backed by a separate attached child Admin View |
| `referenced_components[]` | Owner components inferred from typed fields outside this component. Use these edges to verify runtime compatibility |
| `counts` | Totals recomputed from catalog and allocation data. Counts serve as verification evidence, with the views array as authority |

Use the strict table-owning allocation to avoid shifting child definitions into custom persistence as a way to stay under budget. Non-entity support artifacts such as a migration checkpoint or background task configuration must use the catalog entity that already owns the required semantics, or enter a review as a new record. A scalar or bounded value object already contained in a catalog entity can be stored in its row under the documented type and validation contract.

### Data and attachment translation

The portable record's `id` is the application GUID. Store it in the JCB runtime row's `guid` column. Use the local numeric `id` for internal Joomla Table and edit lookup. API DTOs return the portable identifier. Translate every catalog key, reference and index from portable `id` to physical `guid`. Look up related rows by the typed GUID and scope. An application GUID remains usable after moving data to a Joomla instance with different numeric IDs. [Application identities](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/application-identities.md)

Reserve the compiled Joomla metadata columns listed in the manifest. In the inspected compiler, default field names include `created_by`, `version`, `ordering` and `access`. The compiler handles matching field base names as defaults. Keep the generated metadata on its own contract. Map a portable field that matches a reserved name to the `lms_` prefix, with the identity-to-`guid` exception above. In particular, `lms_created_by` is a Principal GUID, `lms_version` is the catalog version field, and `lms_asset_id` is the curriculum asset identity. Joomla's local `created_by` and `asset_id` retain their platform meanings. Translate unique constraints, joins, projections and data migrations through the same mapping and reject physical name collisions during allocation. [JCB compiler defaults](https://github.com/vdm-io/Joomla-Component-Builder/blob/408703a857ad937479b1e28de7f693af178dcc83/libraries/vendor_jcb/VDM.Joomla/src/Componentbuilder/Compiler/Config.php) · [JCB compiler field resolution](https://github.com/vdm-io/Joomla-Component-Builder/blob/408703a857ad937479b1e28de7f693af178dcc83/libraries/vendor_jcb/VDM.Joomla/src/Componentbuilder/Compiler/Model/Fields.php)

The attachment defaults disable generic API, generic export/import and generated site create/edit. Those features require a separate approved runtime contract. Internal Admin Views also disable all menu and dashboard links. A generated route can still be reached directly. Protect authorization at the controller, scoped list query, row query, mutation service and download boundary. Read-only field controls and disabled buttons remain usability settings. Use explicit service commands for append-only evidence, custody changes and approvals. [Admin View configuration and permissions](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/models/admin-views.md)

Bind a separate child Admin View and its Fields before using a normalized subform. Author the same parent GUID relation, child identity and authorization in the parent form and child service. Attach the repeated field as non-database when the child table owns persistence. Install and inspect the matching get and save paths. For a collection with protected history, use the subform to stage inputs and invoke the owner command to commit the exact next revision. A generated replacement action can delete rows omitted by the submitted set and therefore needs the complete parent revision, scope and collection checks before it is eligible to run. [Normalized child tables and handlers](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/normalized-subforms.md)

### Physical uniqueness and scoped references

Separate local database constraints from portable aggregate invariants. Use explicit SQL unique constraints where possible and verify the generated result. A regular JCB field index supports lookup and leaves duplication possible. The course outline's sibling order requires a unique position even when the portable parent is null. Add an owner-managed, non-null physical scope key whose value is `root` for a root placement and the canonical parent placement key otherwise. Use the corresponding draft/publication identity, derived scope key and position in the physical unique constraint. Keep the original parent field nullable. The scope key remains an implementation detail derived from validated owner state and is excluded from public input.

Use a domain owner transaction for conditions that require several rows, including effective interval overlap and one active enrollment release. A cross-component scalar GUID link is a logical relationship validated by the authoritative service in the correct institution and state. Apply same-component physical foreign keys only where migration order, index requirements, nullable behavior and retention allow them. Catalog reference arrays are bounded typed link values. Validate every target, preserve the declared ordering and membership constraints, and avoid substituting a single unchecked string or relying on an unindexed full scan for a required inverse query.

### Wide natural keys and exact comparison

Several portable unique keys include full strings whose permitted UTF-8 length exceeds a direct composite index. Examples include `ExternalIdentity.issuer`, `ExternalObjectMap.source_namespace`, `PackageResourceFile.path` and the SCORM shared-data store key. The supported InnoDB index width depends on row format and page size. Install preflight must inspect the actual engine configuration. Keep the full catalog lengths and avoid truncating a unique key to a display prefix. [MySQL InnoDB index limits](https://dev.mysql.com/doc/refman/8.0/en/innodb-limits.html) · [MariaDB DYNAMIC row format](https://mariadb.com/docs/server/server-usage/storage-engines/innodb/innodb-row-formats/innodb-dynamic-row-format)

For an equality key too wide for the supported database profile, store the authoritative fields and one physical `BINARY(32)` SHA-256 key digest in the same row. Prefix the digest input with the ASCII token `lms.key.v1` and a two-byte unsigned big-endian field count. Serialize the tuple in the exact order declared in the logical key. Emit byte `0x00` for an allowed null. For a present string, emit `0x01`, its four-byte unsigned big-endian UTF-8 byte length, then its bytes. Apply only the owner-defined canonicalization before encoding. Examples include canonical UUID text and the exact, case-sensitive normalized package path. A logical key that intentionally permits distinct nulls uses a nullable digest or a separate applicability guard instead of forcing those values to collide.

Create a unique index on the digest for the specific logical key, with an independently indexed owner scope for list operations. Resolve equality lookups with the same digest and compare the full authorized tuple before returning an identity. On a unique violation, use a savepoint or follow-up scoped lookup to determine whether this is an exact duplicate. Treat a differing full tuple with the same digest as a physical integrity conflict and stop the affected mutation. Never merge identities on digest alone. Build preflight lists every translated key and checks generated constraints with boundary-length fixtures on each supported engine. A key requiring range ordering retains a separately designed orderable index.

For an existing table, add the digest column, dual-write it from the owner, and backfill in deterministic bounded batches. Scan conflicts with full tuple comparisons. Quarantine true duplicates for authorized reconciliation. Activate the uniqueness constraint and enforce non-null digests for applicable rows before routing lookups through the new index. An interrupted migration remains resumable by the same physical row key.

### Install order and dependency cycles

The typed runtime owner graph can contain a cycle. A course activity can point to an assessment version, while an assessment delivery resolves an offering and content placement. Establish schema readiness in phases.

1. Load the contracts library and platform identity bootstrap.
2. Install all component schema artifacts with academic mutations disabled. Apply same-component physical constraints after dependent local tables exist. Keep cross-component logical reference checks out of pre-install SQL.
3. Verify every referenced component code and service interface after all required schemas exist. Wire service adapters lazily so one component's constructor does not have to recursively boot the full owner graph.
4. Apply approved seeds and backfills. Verify hard constraints, installed table names, attachment counts, migration checkpoints, scope tests and required indexes.
5. Activate the required components as one compatible set. Register optional provider capabilities independently. A missing optional adapter leaves dependent features unavailable and keeps native academic workflows active.

An owner may update tables in several of its components through one command. Use the same connection, transaction manager, tenant scope and lock order for that command, and include its canonical receipt and outbox in the transaction. Avoid performing internal cross-component mutations as network calls. Use durable events for other owners and providers when the portable workflow does not require atomic creation. Introducing multiple databases changes the applicable architecture and requires review of the command semantics.

| Command or work unit | Table boundary | Required consistency |
| --- | --- | --- |
| Publish course version | Drafting and published release components | Lock and revalidate the approved draft. Insert the frozen release and all placement rows before acknowledging publication. |
| Accept a reserved seat | Admissions and enrollment components | Revalidate the reservation, capacity and enrollment uniqueness. Commit the enrollment, source grant and initial release according to the participation command. |
| Submit assessment attempt | Attempt component and platform durability | Fence the editor, accept one terminal submission, write the manifest digest and record the evaluation request in the same commit. |
| Apply package navigation | Package runtime and sequencing components | Persist the occurrence and objective changes with the cursor and navigation receipt. Replay returns the stored decision. |
| Import reviewed curriculum | Transfer and owning domain components | Promotion goes through the receiving owner commands. Reconcile each committed owner effect against the exact transfer record and receipt. |
| Release grade revision | Academic Records components | Verify moderation and policy preconditions, then persist the release and its authorized visibility boundary before returning success. |

## Composition of user workflows

Provide a small set of front-end navigation entries for learners, teachers and registrars. A workspace links to its owning component with the correct institution, actor and resource context. It can display read projections that combine other owners' authorized outputs. Every mutation and sensitive read resolves again at the owner. The number of table-owning definitions is independent of the number of navigation items.

| User experience | Routing and composition | Owner checks |
| --- | --- | --- |
| Course authoring | A draft workspace in `com_lmsoutlines` links to the reusable content and asset selectors and shows the approved publication preview | Load and save the exact draft revision. Select only approved definitions the author can use. Publish through the curriculum command that writes `com_lmspublications` |
| Teacher's class workspace | An offering context in `com_lmsofferings` links to scoped roster, calendar, meetings and class updates | Reauthorize the teacher for the offering, section or group on every owner query and command |
| Learner course player | A progress and curriculum read surface renders the exact enrollment release and redirects an assessment launch or a package launch to its owner | Validate availability, applicable placement, prerequisites, current academic permission and the learner's exact release |
| Assessment player | `com_lmssittings` renders the admitted attempt and uses focused commands for draft response, saving, submission and recovery | Resolve server deadlines, writer lease, admission and exact form revision for each write |
| Staff marking | A work queue in `com_lmsmarking` links to the scoped submission projection. Grade evidence and candidate feedback are separate owner operations | Verify assignment, blind marking policy, exact evidence revision and actor permission. Apply moderation before any required release |
| Curriculum migration | A transfer job in `com_lmstransfers` links to the review workspace and the resulting owner resource | Verify archive rights, exact transfer plan and actor scope. Keep native drafts and approved packages in their owners |
| Package runtime inspector | The admin workspace displays the launch and durable commit receipts and links to the isolated learner player for approved previews | Apply separate permissions to package contents, learner state, sequence diagnostics and preview creation |

### Cross-component selectors

A managed selector opens the target owner's actual modal route. Change the selection link, title lookup, GUID key and optional create/edit actions together when moving a target out of the current component. For example, the outline editor selects an approved reusable node version through the target component using `option=com_lmscontent&view=content_node_versions&layout=modal&tmpl=component&titleKey=guid`. That route is a proposed blueprint output. Verify the actual generated route and its configured access behavior before enabling it. The owner issues a scoped selection context tied to the requesting principal and draft. The selector uses that context to return an allowed display label and GUID. The curriculum command revalidates the selected record and tenant on save.

Enable New or Edit only for relationships where an authorized mutable target is the intended operation. A published ContentNodeVersion can be selected or inspected through the relevant permission. The authored content workspace creates its replacement revision through the owner workflow. If the reusable selector's title lookup can expose a restricted row, replace the lookup or constrain it through the target owner. Test selecting, clearing, expired context, cross-tenant IDs, direct edit links and stale source revision. [JCB modal relationship recipe](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/modal-relationships.md)

Use stable links between workspaces instead of duplicating authoritative editors. For example, an assessment row opens the curriculum placement preview in its owner and a roster row opens authorized grades through the records owner. Default internal definitions to no menu entry. Group the components under a small institutional navigation tree using the host's menu permissions and approved custom dashboard links. Verify the compiled Joomla menu structure with a course teacher, site administrator and learner.

## Allocation validation and release evidence

The static check compares the design map to the catalogs through `tooling/validate_components.py`. It checks the proposed table length against the baseline database prefix budget of 12 characters. Deployment readiness checks the actual database prefix and identifier limit. Fail if a domain is omitted, an entity is missing or appears twice, the same component owns more than five attached definitions, a view is placed under a different domain, a table or definition key is duplicated, or a generated route code would shadow the standard dashboard. Fail when a normalized edit child is missing, has no typed link to its parent, or belongs to a different component under this allocation. Recompute the external owner graph and count summary rather than taking the declared totals on trust.

The build check uses the selected release's imported blueprint and compiled package. Resolve the planned view definition key to the JCB GUID. Read the owning component attachment data and confirm that its set and count match the manifest, including hidden views. Confirm Custom Admin View count independently. Inspect the exact installed schemas, table/route names, local ID and application GUID columns, unique keys, normalized child relations and generated menu/API flags. Record a discrepancy against its owning blueprint and regenerate.

| Fixture | Expected result |
| --- | --- |
| Add a sixth attachment with submenu and dashboard disabled | Validation rejects the component before packaging |
| Add a second Admin View for an existing table in a sibling component | Validation rejects duplicate table ownership |
| Remove the child Admin View while retaining the parent's subform | Validation rejects the incomplete normalized edit graph |
| Map a view list route onto the standard dashboard name | Name validation fails and the route is corrected before compiling |
| Insert two root placements at the same position in one course version | Database constraint or atomic owner validation rejects the duplicate |
| Save an internal view through a guessed URL as an unscoped teacher | The endpoint denies the request before exposing or changing a row |
| Install the same curriculum into two sites with different Joomla row IDs | Application GUID relations resolve to the same logical entities |
| Interrupt publication after staging draft and placement writes | Neither a partial publication nor its acknowledgement is visible |
| Remove one required component during a package upgrade | Readiness stays closed and identifies the unresolved owner contract |
| Retry navigation after the server committed and the client timed out | Existing navigation receipt is returned with the original decision |

## Delivery sequencing

Start with the smallest complete curriculum-to-result vertical slice. The allocation describes the target system and allows an early package to deliver a supported subset by declaring its capabilities and omitting unbuilt components from the pilot installer. The pilot manifest identifies the exact set that is enabled and its dependency closure. Build, install and verify each slice through real administrator and site routes before making the full package available.
