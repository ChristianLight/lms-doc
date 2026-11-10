# Joomla package and component contract

## Implementation boundary

The portable specification defines academic behavior. This implementation uses Joomla 6 for the website, authentication, sessions, extension lifecycle, form infrastructure, routing and baseline permissions. JCB maintains the blueprint records and supporting PHP source from which the extensions are generated. The host adapter must preserve the portable command semantics through administrator forms, site forms, scheduled tasks and web service requests.

Record the exact Joomla, PHP, database, JCB compiler, skill repository and supporting Power revisions for each build. Choose supported production versions at implementation time and test against those versions. A source reference in this document identifies inspected behavior and is not a fixed future runtime requirement. Resolve the maintained build workflow through [JoomEngine Skills](https://github.com/joomengine/skills).

## Domain groups and component budget

Curriculum, participation, assessment, records, interoperability and platform are ownership domains. A domain may contain multiple Joomla components. The implementation budget is at most five attached JCB Admin View definitions per component. Count hidden child views and internal record views when applying this budget. A visible workspace can be a custom screen composed from several domain operations, but hiding a view does not remove its blueprint or schema ownership.

Assign a physical table managed through JCB to one attached Admin View and one component. Related child tables require their own view definitions under the normalized subform workflow. A parent JSON field is appropriate for a bounded value object such as an expression AST or captured policy payload when independent lookup and lifecycle are unnecessary. It is inappropriate for an independently addressed attempt, enrollment, membership, grade revision or source mapping.

The component partition is produced from the finalized domain catalogs. Use these rules in order.

1. Keep each mutable aggregate and its directly edited children in one component where its five-view budget permits.
2. Keep immutable evidence ledgers under their owner domain and expose task-specific operations rather than ordinary edit/delete actions.
3. Split a domain at a cohesive business boundary when its persisted entities exceed the view budget.
4. Keep cross-component relationships as immutable application GUIDs with explicit owner lookups and scope validation.
5. Group components into a single installable package so operators receive a compatible set.
6. Publish package-level dependency versions and perform install/upgrade readiness checks before enabling academic writes.

A field schema or logical record may be implemented as an immutable JSON value within an owner row when the catalog identifies it as a value object. That mapping must preserve the schema, size limits, query requirements and version identity. Changing the mapping from a separate entity to an embedded value requires an explicit architecture decision. It cannot be an incidental shortcut used to satisfy the view count.

## Shared library

The shared LMS library contains contracts and cross-cutting mechanisms that have multiple actual consumers. These include UUID serialization, actor and scope context, exact decimal score values, command receipts, event envelopes, typed errors and provider interfaces. Academic owners implement their own domain services. Avoid a shared repository layer that can mutate every domain's tables without its command rules.

Use Joomla's extension dependency injection pattern for service construction. A component registers its owner services and dependencies through its service provider. A caller obtains the required public contract from the booted extension or a documented adapter, without assuming that another component's child container is the global container. [Joomla extension containers](https://manual.joomla.org/docs/next/general-concepts/dependency-injection/extension-child-containers/)

## Component registration artifact

Each component's build manifest records the following fields.

| Field | Meaning and check |
| --- | --- |
| Component code | Stable `com_` name, globally unique in the package |
| Domain owner | One of the authoritative domains in the specification |
| Attached Admin Views | Complete definition GUID list with count at most five |
| Physical tables | Owner table names, schema version and relationship fields |
| Site views | Learner or staff entry points and the owner commands they invoke |
| Task screens | Operational screens such as publication, submission review or import approval |
| Required library interfaces | Contract names and compatible major versions |
| Required components | Dependency codes and compatible versions |
| Plugins | Named webservice, task, user lifecycle or provider adapters with purpose |
| Schema migrations | Ordered, repeatable upgrade steps with checkpoint and recovery behavior |
| Runtime claims | Supported Joomla/PHP/database targets and verification evidence |
| Source provenance | Blueprint and Power revisions, dependency locks and compiled artifact digest |

Reserve the standard dashboard's generated component name and check generated class paths for collisions before naming views. Visible labels can change through language strings while component and view codes remain stable. A renamed view route requires a compatibility mapping when stored links or bookmarks already use it.

## Installation sequence

The package preflight checks host versions, enabled required extensions, database capabilities, write locations, migration state and current package version. Install shared interfaces and owner components in dependency order. Register optional adapters after the owner contracts they call. Apply schema changes and populate required reference records with stable application identities. Build the permission definitions and initial role templates without granting educational record access to every registered user.

After schema installation, run readiness checks that resolve cross-component service construction, one synthetic scope decision and one receipt transaction. Enable site write entry points only when all mandatory checks pass. Keep detailed diagnostics in an administrator-only readiness screen. A partial install must identify the completed component and migration checkpoints, allowing a safe resume or rollback according to each migration's contract.

Uninstall preserves academic records by default. A destructive data purge is a distinct, explicitly authorized operation with retention and legal-hold checks, export options and a completion receipt. Removing an optional chat adapter stops synchronization without deleting the enrollment or grade record. Removing a required component is blocked while dependent components remain active unless a reviewed package removal workflow coordinates the change.
