# Joomla package and component contract

## Implementation boundary

The portable specification defines academic behavior. This implementation uses Joomla 6 for the website, authentication, sessions, extension lifecycle, form infrastructure, routing and baseline permissions. JCB maintains the blueprint records and supporting PHP source from which the extensions are generated. The host adapter must preserve the portable command semantics through administrator forms, site forms, scheduled tasks and web service requests.

Record the exact Joomla, PHP, database, JCB compiler, skill repository and supporting Power revisions for each build. Choose supported production versions at implementation time and test against those versions. A source reference in this document identifies inspected behavior and is not a fixed future runtime requirement. Resolve the maintained build workflow through [JoomEngine Skills](https://github.com/joomengine/skills).

## Domain ownership and cohesive components

Curriculum, participation, assessment, records, interoperability and platform are portable ownership domains. Joomla components assemble related concepts, administration and services within those domains. Component boundaries follow a coherent responsibility and useful deployment boundary. There is no fixed view count, component count or target range. Five, ten, twenty or more views can belong together when they support the same responsibility. A small component is justified by its role and reuse rather than by an attachment quota.

The [allocation chapter](06-component-allocation.md) explains each proposed grouping, its workspaces, its authoritative records and the reasons to keep neighboring responsibilities separate. The [component map](component-map.json) inventories every attachment and proposed table. Counts describe that design and must be recomputed after a change; they are not acceptance thresholds. The map does not alter the six portable owner catalogs or create additional academic service authorities merely because records share an extension.

Assign a physical table managed through JCB to one attached Admin View and one component. Related child tables require their own view definitions under the normalized subform workflow. A parent JSON field is appropriate for a bounded value object such as an expression AST or captured policy payload when independent lookup and lifecycle are unnecessary. It is inappropriate for an independently addressed attempt, enrollment, membership, grade revision or source mapping.

The component partition is produced from the finalized domain catalogs. Evaluate these concerns together.

1. Keep each mutable aggregate, its directly edited children and the administration needed to complete its workflow together. Drafts, versions and review records may share a component while retaining different lifecycle rules.
2. Give a component a responsibility that staff and implementers can explain independently of table count. Permit multiple normal list/edit workspaces and add a Custom Admin View when a task needs a combined projection or explicit command workflow.
3. Keep immutable evidence ledgers under their owner domain and expose authorized task operations or read views. A larger component does not make its audit, attempt or issued-result rows ordinarily editable.
4. Split where optional deployment, distinct authority, reuse, release cadence or operational behavior creates a meaningful boundary. Keep the relationship contract explicit when a split is justified.
5. Keep cross-component relationships as immutable application GUIDs with declared typed owner lookups, selector metadata, scope checks and save-time validation. A read join or modal selection does not grant mutation authority over the target owner.
6. Deliver a compatible distribution package with explicit mandatory services, optional capabilities and readiness gates. Distinguish the data reference graph from the install/activation graph; document coordinated activation where mandatory services genuinely depend on one another.

A field schema or logical record may be implemented as an immutable JSON value within an owner row when the catalog identifies it as a value object. That mapping must preserve the schema, size limits, query requirements and version identity. Changing the mapping from a separate entity to an embedded value requires an explicit architecture decision based on its semantics, query needs and lifecycle.

Use JCB's generated administrator lists, forms, permissions, links and selection machinery as the baseline user interface. View permissions distinguish workspaces in the same component; attached-field permissions distinguish editable or visible values within a form. Domain services add institutional scope, revision and lifecycle validation where required. See the concrete [GUID relationship and ACL contract](08-guid-relationships-selectors-and-acl.md).

## Shared library

The shared LMS library contains contracts and cross-cutting mechanisms that have multiple actual consumers. These include UUID serialization, actor and scope context, exact decimal score values, command receipts, event envelopes, typed errors and provider interfaces. Academic owners implement their own domain services. Avoid a shared repository layer that can mutate every domain's tables without its command rules.

Use Joomla's extension dependency injection pattern for service construction. A component registers its owner services and dependencies through its service provider. A caller obtains the required public contract from the booted extension or a documented adapter, without assuming that another component's child container is the global container. [Joomla extension containers](https://manual.joomla.org/docs/next/general-concepts/dependency-injection/extension-child-containers/)

## Component registration artifact

Each component's build manifest records the following fields.

| Field | Meaning and check |
| --- | --- |
| Component code | Stable `com_` name, globally unique in the package |
| Domain owner | One of the authoritative domains in the specification |
| Attached Admin Views | Complete table-owning definition GUID list and descriptive count, including internal views |
| Custom Admin Views | Task/read workspace definitions, source queries, permitted commands and descriptive count |
| Responsibility and workspaces | Cohesive purpose, intended staff journeys, visible view permissions and rationale for independent installation |
| Physical tables | Owner table names, schema version and relationship fields |
| Site views | Learner or staff entry points and the owner commands they invoke |
| Task screens | Operational screens such as publication, submission review or import approval |
| Required library interfaces | Contract names and compatible major versions |
| Required components | Mandatory service codes, contract/API/schema requirements and readiness reasons |
| Optional features | Capability-specific components and approved provider profiles; fail/disable behavior when unavailable |
| Activation set | Coordinated readiness boundary for genuine mutual dependencies; prerequisite sets form a DAG |
| Referenced components | Derived GUID owner graph for query, selector and reconciliation planning; not automatically installation prerequisites |
| Plugins | Named webservice, task, user lifecycle or provider adapters with purpose |
| Schema migrations | Ordered, repeatable upgrade steps with checkpoint and recovery behavior |
| Runtime claims | Supported Joomla/PHP/database targets and verification evidence |
| Source provenance | Blueprint and Power revisions, dependency locks and compiled artifact digest |

Reserve the standard dashboard's generated component name and check generated class paths for collisions before naming views. Visible labels can change through language strings while component and view codes remain stable. A renamed view route requires a compatibility mapping when stored links or bookmarks already use it.

## Installation sequence

The package preflight checks host versions, enabled required extensions, database capabilities, write locations, migration state and current package version. Install shared interfaces and stage component schemas according to the [dependency and lifecycle contract](09-component-dependencies-and-lifecycle.md). Order activation sets by their mandatory prerequisites; stage the members of a mutual set before activating its services together. A cycle in the data-reference graph alone requires no such grouping. Register optional adapters after the owner contracts they call and keep their capabilities disabled until their own checks pass. Apply schema changes and populate required reference records with stable application identities. Build the JCB-maintained permission definitions and initial role templates without granting educational record access to every registered user.

After schema installation, run readiness checks that resolve cross-component service construction, one synthetic scope decision and one receipt transaction. Enable site write entry points only when all mandatory checks pass. Keep detailed diagnostics in an administrator-only readiness screen. A partial install must identify the completed component and migration checkpoints, allowing a safe resume or rollback according to each migration's contract.

These dependency and readiness rules are application requirements maintained through JCB's supported packaging, installer and service authoring surfaces. A Joomla package manifest alone does not enforce arbitrary application service compatibility or coordinated readiness. Verify the emitted manifests and hooks on the selected compiler and Joomla releases rather than assuming their presence.

Uninstall preserves academic records by default. A destructive data purge is a distinct, explicitly authorized operation with retention and legal-hold checks, export options and a completion receipt. Removing an optional chat adapter stops synchronization without deleting the enrollment or grade record. Removing a required component is blocked while dependent components remain active unless a reviewed package removal workflow coordinates the change.
