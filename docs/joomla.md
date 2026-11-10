# Joomla 6 and JCB implementation overview

The detailed implementation contract is under [specification/joomla](../specification/joomla/01-package-and-component-contract.md). Curriculum, participation, assessment, records, interoperability and platform are domain ownership groups. Each group can contain several Joomla components.

The [component map](../specification/joomla/component-map.json) assigns every catalog entity to one component and an attached JCB Admin View. Components group cohesive responsibilities, related administration and useful reusable services. They may contain multiple normal workspaces, child views and Custom Admin Views; there is no fixed view-count or component-count limit. A distribution package delivers compatible components and shared interfaces. The [allocation chapter](../specification/joomla/06-component-allocation.md) explains the grouping, physical schema translation and descriptive inventory.

| Implementation concern | Detailed contract |
| --- | --- |
| Package and component ownership | [Package contract](../specification/joomla/01-package-and-component-contract.md) |
| GUIDs, local IDs, fields, child views and persistence | [Identity and persistence](../specification/joomla/02-identities-forms-and-persistence.md) |
| Joomla users, academic roles, sessions, ACL and routes | [Host identity and access](../specification/joomla/03-host-identity-and-academic-access.md) |
| Nextcloud and Filery | [Collaboration and document adapters](../specification/joomla/04-collaboration-and-document-adapters.md) |
| Agent workflow, JCB generation, installation and release | [Build and release workflow](../specification/joomla/05-agent-build-and-release-workflow.md) |
| Exact entity allocation and responsibility grouping | [Component allocation](../specification/joomla/06-component-allocation.md) |
| GUID target tables, modal selection, workspace queries and native field/view permissions | [Relationships and ACL](../specification/joomla/08-guid-relationships-selectors-and-acl.md) |
| Mandatory services, optional providers, installation and coordinated upgrades | [Dependencies and lifecycle](../specification/joomla/09-component-dependencies-and-lifecycle.md) |

The Joomla implementation uses the portable owner commands for publication, enrollment, submission, marking and academic record issuance. Generated persistence and presentation are connected to those commands wherever a domain invariant requires a controlled transition. The source blueprint, supporting Powers and package dependency manifest remain the maintained build inputs.

Use JCB's built-in field and view permission settings and Joomla's generated administration first. The application adds the academic scope and lifecycle checks that these host controls cannot infer. Cross-component selectors declare the target component, table, title and GUID key; saves resolve the selected GUID in the authoritative owner and current institutional scope. Data references, mandatory installation requirements and optional feature requirements are separate relationships with separate checks.
