# Joomla 6 and JCB implementation overview

The detailed implementation contract is under [specification/joomla](../specification/joomla/01-package-and-component-contract.md). Curriculum, participation, assessment, records, interoperability and platform are domain ownership groups. Each group can contain several Joomla components.

The [component map](../specification/joomla/component-map.json) assigns every catalog entity to one component and an attached JCB Admin View. The limit is five attached definitions per component, including hidden child views. A single installable package delivers the compatible components and shared interfaces. The [allocation chapter](../specification/joomla/06-component-allocation.md) specifies the count, physical schema translation, dependency checks and verification.

| Implementation concern | Detailed contract |
| --- | --- |
| Package and component ownership | [Package contract](../specification/joomla/01-package-and-component-contract.md) |
| GUIDs, local IDs, fields, child views and persistence | [Identity and persistence](../specification/joomla/02-identities-forms-and-persistence.md) |
| Joomla users, academic roles, sessions, ACL and routes | [Host identity and access](../specification/joomla/03-host-identity-and-academic-access.md) |
| Nextcloud and Filery | [Collaboration and document adapters](../specification/joomla/04-collaboration-and-document-adapters.md) |
| Agent workflow, JCB generation, installation and release | [Build and release workflow](../specification/joomla/05-agent-build-and-release-workflow.md) |
| Exact entity allocation and view budget | [Component allocation](../specification/joomla/06-component-allocation.md) |

The Joomla implementation uses the portable owner commands for publication, enrollment, submission, marking and academic record issuance. Generated persistence and presentation are connected to those commands wherever a domain invariant requires a controlled transition. The source blueprint, supporting Powers and package dependency manifest remain the maintained build inputs.
