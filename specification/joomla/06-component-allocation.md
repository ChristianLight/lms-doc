# Component allocation and JCB workspaces

The [component map](component-map.json) groups all persisted catalog entities into Joomla components by responsibility, workflow, authorization and transaction boundaries. Each table-owning Admin View belongs to the component that maintains its source and persistence. A component can expose several staff or learner workspaces. Its natural set of views follows the work it owns.

The current design assigns **249 persisted entities and 249 table-owning Admin Views to 22 components**, with 21 additional Custom Admin Views for identified workflows. The largest component currently has 23 attachments in total. These are observed design counts. There is no fixed minimum, maximum or target count for components or their views. Future allocation changes are reviewed for cohesion, actual build behavior and their impact on authority and dependencies.

This is a pre-implementation allocation. Component codes, proposed table prefixes and JCB definition keys in the map specify the intended first blueprint build. Bind each definition key to its real JCB definition GUID during authoring. The portable entities, field contracts and application GUIDs retain their existing meanings. A future change to an installed table or route requires its own approved migration and verification.

## Group records by responsibility

Start with the existing six owner catalogs. Keep each entity with its declared domain. Examine where authorized users work, which records share a decision or write fence, which keys and views are routinely reused, and which changes need independent lifecycle and deployment. Place the related normalized tables and their editors together when they serve the same aggregate. Retain precise visibility and command permissions inside the component.

| Domain | Cohesive components | Governing distinctions |
| --- | --- | --- |
| Platform | Institution and academic access, protected storage, governance and audit, durable operations, provider connections | Scope and authority, protected custody, privacy approval, retry machinery and remote trust have different responsibilities. The foundation activates together |
| Curriculum | Native curriculum, source authoring | Course drafts, exact placements, reusable content, libraries, assets and publications belong to one native graph. Protected source extraction and assisted proposal evidence require their own review and access |
| Participation | Offerings and admission, classroom operations, learner progress | Capacity, rosters and release assignments share an enrollment lifecycle. Meetings and attendance serve the instructor's class workflow. Learner progress and navigation consume accepted evidence under the effective release |
| Assessment | Item bank, assessment design, assessment delivery, marking and review | Item revisions seal prompts and private rules. Form assembly pins published items and variants. Exam admission, leases, responses and submissions share a write fence. Marking consumes sealed work or another approved evidence source |
| Interoperability | Transfers and exports, package playback, standards connections | Transfer custody and reviewed promotion own the source graph. Package manifest, launch, SCO state and sequencing support one runtime. Institution standards connections have independent protocol capabilities |
| Records | Gradebook, academic documents, programmes and credit, competencies, analytics and intervention | Grade policy and official release remain one result lineage. Issuance and disclosure consume exact decisions. Programme adjudication, competency decisions and learner support retain their own authority |

Every component entry records a purpose, grouping rationale and separation boundary. An academic feature may call several owners and still have one primary workspace. An entity with an independent identity, publication or retention contract retains its own table-owning view. A bounded field value such as a rich-text subtree stays with its existing owner row.

Split a component when a workflow or lifecycle acquires an independent operational purpose, or when separate delivery materially simplifies its authority or release dependencies. Merge closely coupled groups when separation duplicates editors and selectors or turns a single write into a brittle series of calls. Document the practical outcome of the boundary change. When renaming an installed component or view, preserve application GUIDs, version pins and references through its reviewed migration.

## JCB definitions and entry workspaces

JCB's `component_admin_views.addadmin_views` collection attaches the table-owning definitions. Each `adminview` entry resolves its definition and carries menu, dashboard, API and other settings. Generated list and item pages can come from the same definition. Hidden children and evidence records retain their attachment. The inspected Service Directory blueprint demonstrates this model with 24 attached Admin Views. Its configuration is evidence of supported composition. The LMS follows its own ownership and access design. [JCB component attachment reference](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/reference/component_admin_views.md) · [Service Directory attachment source](https://github.com/joomengine/joomla-packages/blob/a0041f0d408ca65ac43796f89a90c88063fe85a8/src/joomla_component/children/160d0efb-6bf0-48eb-8d46-55cf74729501/component-admin-views.json)

Use generated Admin Views for normal record lists, edit forms and managed selectors. Use an attached Custom Admin View when the workflow needs a coherent cross-record task and an ordinary list or form is insufficient. Its definition supplies a workspace, typically with a scoped Dynamic Get or owner service query and explicit actions. For example, publication review compares a frozen draft digest, issue set and dependency coverage. The attendance register uses one exact occurrence and the authorized learner list. Grade release review presents the complete approved set and period closure evidence. These workspaces invoke owner commands through their authorized routes. Their data comes from real existing record owners. [JCB component assembly](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/models/component.md) · [Custom Admin View attachments](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/reference/component_custom_admin_views.md)

Use Site Views for the native learner player, assessment player, classroom, review and issued record surfaces. A component can compose related administrator views, tabs, dashboards and site entry points around its workflow. The map lists the deliberate entries. A hidden child remains available through its approved related form or service. Expose the minimum practical navigation through menus, task workspaces and contextual links.

### Map contract

| Field | Meaning and verification |
| --- | --- |
| `manifest_version`, `allocation_status`, `package_code` | Version of this map format, design or verification status, and planned distribution package identity |
| `components[].code` and `domain` | Stable component code and the catalog domain of all attached persisted entities |
| `purpose`, `grouping_rationale`, `separation_boundary` | The coherent work, reasons for grouping and the authority or lifecycle left to other owners |
| `workspaces[]` | Stable component-local key, display label, entry kind and target, workflow and applicable access description |
| `workspaces[].entry_kind` and `entry` | `admin_view` names the owned entity, `custom_admin_view` names an attached custom view code, and `site_view` names a proposed site view code |
| `admin_views[]` | One allocation per persisted entity. Includes stable planning definition key, proposed singular/list route and table. Visibility identifies a deliberate workspace or internal record view |
| `custom_admin_views[]` | Attached task or review workspace definitions with unique keys, route codes and purposes. They use the authoritative tables allocated to existing Admin Views |
| `normalized_edit_groups[]` | The intended normalized editors, their same-owner attached child records and the authoritative mutation path |
| `referenced_components[]` | Exact typed catalog relationship graph. Consumers use it to identify owner lookups and investigate dependencies |
| `provided_contracts[]` and `required_components[]` | Versioned services a component provides and requirements for baseline readiness |
| `host_requirements`, `activation_sets`, `feature_dependencies` | Package and host assumptions, grouped readiness barriers, and capability-specific dependencies and profiles |
| `counts` | Descriptive totals derived from the allocation. They can change with a reviewed component grouping or catalog change |

### Native permissions and related views

Configure JCB view permissions for their actual scope. The Admin View `addpermissions` implementation flags distinguish record, whole-view or both levels. Field attachments also provide editing, access and view settings. Apply the corresponding Joomla ACL declarations, then check current academic authority at each list, selector, row, command and download. A teacher with component access may only see their assigned offerings. Permission to author an item cannot reveal private scorer inputs, and a general roster operator cannot approve a grade.

Internal views disable default menu and dashboard links. The baseline attachment settings disable generic API, generic export/import and generated front-end editing. A purpose-built protected route may expose an authorized operation. Validate direct route requests and modal title lookups, including guessed row GUIDs. Filter both the result set and count to the allowed academic scope. Keep internal columns such as answer keys, admission evidence, unreleased grades and protected source locators out of ordinary projections. [JCB Admin View configuration](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/models/admin-views.md)

For a normalized subform, attach the actual owner child Admin View and Fields, and use the correct parent GUID relation. The inspected recipe uses a non-database parent field and paired get/save handlers. The parent form may stage a full validated edit, but the owner command checks complete scope, expected revision, child ownership, immutable evidence and permitted removals before committing. A missing PATCH field preserves existing children. A supplied empty set removes rows only under the documented operation and policy. [JCB normalized subforms](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/normalized-subforms.md)

Use the owner modal's exact select route, label lookup and GUID key for a managed relationship. The native assessment design component, for example, may select an approved item version through the item bank owner. The target picker checks current bank and institution scope, and exposes a label and exact allowed GUID. The submitter's owner revalidates the selection and its version before writing. Enable New or Edit only when the intended actor can invoke the approved mutation. An immutable item version uses selection or inspection and a separate version-authoring path. Same-component and cross-component selector routes both require installed tests. [JCB modal relationships](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/modal-relationships.md)

## Persistence, scope and transactions

The portable identity maps to a runtime `guid` column. Joomla's local numeric `id` remains the host Table and edit key. Resolve application relationships using the typed GUID and approved institution or object scope. Map compiler-reserved semantic columns through the declared `lms_` translation. Reserve each component's standard dashboard code before choosing singular and list codes. Check generated paths after compiler sanitization, and verify actual SQL identifier lengths with the deployment prefix. [JCB application identities](https://github.com/joomengine/skills/blob/e7b8723397811772c85358e72ce91ab594785748/packages/workflows/application-identities.md) · [MySQL/MariaDB physical contract](../persistence/02-mysql-mariadb-physical-contract.md)

Create explicit unique constraints for catalog keys. The outline uses owner-derived `sibling_scope_key`, either `root` or `parent/` followed by the exact draft parent key or published parent occurrence GUID. The parent relation stays nullable. This preserves root and child position uniqueness through a non-null scope key. Cross-component typed GUID references are logical by default and validated by their owners. A proposed physical foreign key needs compatible scope, installation ordering, retention and cleanup semantics.

### Wide natural keys and exact comparison

Some logical unique keys include strings whose permitted lengths exceed the supported database index width. Preserve the full source tuple. For a wide equality key, derive an indexed `BINARY(32)` SHA-256 value from the exact ordered canonical tuple. Prefix the digest input with ASCII `lms.key.v1` and a two-byte unsigned big-endian field count. Encode an allowed null as byte `0x00`. Encode a present string as `0x01`, four-byte unsigned big-endian UTF-8 length, and exact bytes. Apply only the owner's canonicalization. A key whose policy permits independent nulls uses a nullable digest or an applicability guard.

Compare the full authorized tuple after digest lookup and on unique violation. A different full tuple with the same digest raises an integrity conflict. Preserve exact bytes and scope for a reviewed diagnosis. A wide equality digest does not provide range ordering. Add separate supported indexes for scoped listings. During migration, backfill in bounded resumable batches, reconcile exact conflicts and only then activate the new constraint and lookup. [MySQL index width limits](https://dev.mysql.com/doc/refman/8.4/en/create-table.html) · [MariaDB InnoDB row format](https://mariadb.com/docs/server/server-usage/storage-engines/innodb/innodb-row-formats/innodb-dynamic-row-format)

### Owner command examples

| Workflow | Primary boundary | Required consistency |
| --- | --- | --- |
| Publish a course | Native curriculum | Lock the approved draft, validate its dependency pins, write the exact publication graph and coordinate ready reference coverage before acknowledging |
| Accept a reserved seat | Offerings and admission | Recheck capacity, reservation and learner eligibility. Commit enrollment, source grant and effective release according to the command |
| Submit an assessment | Assessment delivery | Check deadline and lease, accept one sealed submission and commit evidence, receipt and outbox atomically |
| Mark accepted evidence | Marking and review | Use exact submission or permitted alternative evidence and immutable criteria. Enforce actor scope and a separate official grade release |
| Apply package navigation | Package playback | Bind exact registration, occurrence, sequencing and accepted commit state. Store the navigation result and receipt under the same command |
| Approve an import or assisted plan | Transfer or source authoring with receiving owner | Preserve the frozen plan and scope. Invoke the native owner for authoritative writes and reconcile exact results |
| Release an official result | Gradebook | Recheck exact accepted evidence, moderation and policy. Publish official visibility and its revision together |

When an operation spans components within one owner transaction, use the same database connection, lock order, actor and scope. Do not split a consistency boundary into remote calls solely because its tables are maintained by different blueprint components. A true provider or service boundary uses its documented durable handoff and reconciliation.

## Dependencies and feature readiness

Review the catalog graph, service requirements and enabled capabilities separately. A typed reference records where an owner lookup can occur. A required service contract is needed to open the component's baseline write path. A feature may additionally require a selected component, adapter, provider profile or verified runtime. Install schema and registrations before resolving cross-component services. The institution foundation opens behind a shared readiness barrier to support its local issuer and trusted scope dependencies. Resolve service adapters lazily when applying the dependency plan. [Component dependencies and lifecycle](09-component-dependencies-and-lifecycle.md)

For example, a native lesson does not require a SCORM player or remote collaboration provider. Native assessment marking requires the sealed attempt owner. Approved manual, package and external evidence have their own gates and can use the evidence owner without the native assessment chain. An official report that cites released grades needs the gradebook service. A competency or qualification credential can use its own approved evidence profile. SCORM export requires its generator and projection validation, independently of package playback. A provider-backed file, room or tool remains unavailable until its exact connection and rights are ready. Native roles and records stay authoritative when an optional remote feature is disabled.

## Allocation and installed acceptance

The validator reconciles the map with all owner catalogs and checks component, entity, definition, table and route identities. It verifies that workspace entries resolve, normalized edit groups keep typed attached children, and runtime contracts and feature requirements point to declared compatible providers. It checks that readiness dependencies outside an activation set resolve without an unhandled cycle. It derives descriptive counts from the actual map.

| Fixture | Expected result |
| --- | --- |
| Open a component with many related views | Build and installation preserve its legitimate attachment set and role-scoped workspaces |
| Duplicate a persisted table owner or reuse a conflicting route | Validation rejects the conflicting allocation |
| Remove a normalized child attachment while retaining the editor | Validation identifies the incomplete editor and table graph |
| Open an internal view or modal by guessed URL | The owner denies unauthorized scope before returning a label, count or row |
| Compare native and provider-specific feature profiles | A required provider gates only its authorized feature. Core curriculum and native learning remain available |
| Compile from a clean supported JCB authoring install | Every planned attached definition resolves to a real JCB GUID. The compiled schema, routes, selectors and tasks match the approved blueprint |
| Install with different local numeric row IDs | Application GUID references, version pins, source mappings and evidence remain correct |
| Interrupt a publication or sealed attempt write | The owner retains one consistent result or an authorized retry state with its exact receipt contract |

Choose a first pilot by supported workflows and proven dependencies. The complete design can be delivered incrementally through compatible feature profiles. Verify each selected path through its normal administrator, task and learner surfaces before including it in an institution's release.
