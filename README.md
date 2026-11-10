# Learning management system specification

This specification describes an LMS that can author and deliver curriculum, run classes and self-paced courses, mark work, and issue academic records. The domain and data model are implementation-neutral. The Joomla 6 plan maps those requirements onto a concrete package of extensions.

Start with the [scope](docs/scope.md), then use the [domain model](docs/data-model.md) to review entity ownership, relationships, versioning and invariants before creating database fields or views.

| Document | What it defines |
| --- | --- |
| [Scope and architecture](docs/scope.md) | Product boundaries, terminology, actors, access model and institutional capabilities |
| [Domain model](docs/data-model.md) | Entity dictionary, cardinalities, identity, lifecycle and cross-domain invariants |
| [Curriculum and learning delivery](docs/learning.md) | Authoring, libraries, offerings, enrollment, classes, access, progress and completion |
| [Assessment and academic records](docs/assessment.md) | Item authoring, mathematical marking, exams, grading, moderation and report cards |
| [Interoperability and migration](docs/interoperability.md) | Native content migration, SCORM runtime, compatibility profiles and validation |
| [Security and operations](docs/operations.md) | Authorization, accessibility, privacy, reliability, integrations and operational acceptance |
| [Advanced institutional capabilities](docs/advanced.md) | Additional workflows and boundaries for feature expansion |
| [Delivery plan and acceptance](docs/delivery-plan.md) | Build order, migration pilot, decisions and end-to-end release gates |
| [Joomla 6 and JCB implementation](docs/joomla.md) | Extension ownership, admin views, generator boundaries and integration adapters |

This is a first architecture baseline. Each compatibility claim, academic policy and workload target becomes a release commitment when its stated acceptance conditions have been met. The example workflows use synthetic records.
