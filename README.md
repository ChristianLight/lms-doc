# Learning management system build specification

This repository defines a platform-neutral learning management system for schools, colleges, universities and independent study. It specifies the academic data model, authoring and delivery workflows, assessment and marking rules, institutional records, interoperability, access controls and operational behavior. A separate implementation contract maps the design to Joomla 6 and Joomla Component Builder.

The detailed specification is under [specification/](specification/README.md). Its six domain catalogs contain field definitions, constraints, state transitions, permissions, command and event contracts, concrete examples and acceptance scenarios. The [generated reference](reference/README.md) exposes the entity dictionary, JSON Schemas, OpenAPI document and scenario lists from those catalogs.

## Read the design

| Area | Start here | Contract source |
| --- | --- | --- |
| System rules | [Specification contract](specification/architecture/01-specification-contract.md), [ownership](specification/architecture/02-ownership-and-dependencies.md), [command and event protocol](specification/architecture/03-command-and-event-protocol.md) | Cross-domain rules |
| Identity and operations | [Institution and identity foundations](specification/README.md#platform) | [Platform catalog](specification/platform/catalog.json) |
| Curriculum | [Outline and identities](specification/curriculum/01-outline-and-identities.md) | [Curriculum catalog](specification/curriculum/catalog.json) |
| Participation | [Offerings and calendars](specification/participation/01-offerings-and-academic-calendar.md) | [Participation catalog](specification/participation/catalog.json) |
| Assessment | [Item banks and authoring](specification/assessment/01-bank-authoring.md), [mathematics](specification/assessment/03-math-evaluators.md) | [Assessment catalog](specification/assessment/catalog.json) |
| Academic records | [Authority and model](specification/records/01-authority-and-model.md), [grade calculation](specification/records/03-grade-calculation.md) | [Records catalog](specification/records/catalog.json) |
| Exchange and migration | [Format profiles](specification/interoperability/01-format-profiles-and-native-archive.md), [course and library adapters](specification/interoperability/03-olx-library-adapters.md) | [Interoperability catalog](specification/interoperability/catalog.json) |
| SCORM | [1.2 runtime](specification/interoperability/05-scorm-12-runtime.md), [2004 runtime](specification/interoperability/06-scorm-2004-runtime.md), [sequencing](specification/interoperability/07-scorm-sequencing.md) | Runtime profiles and interoperability catalog |
| Joomla and JCB | [Package contract](specification/joomla/01-package-and-component-contract.md), [component allocation](specification/joomla/06-component-allocation.md) | [Component map](specification/joomla/component-map.json) |
| Existing curriculum migration | [Graph discovery](specification/migration/01-archive-discovery-and-graph.md), [identity and link resolution](specification/migration/02-identity-allocation-and-link-resolution.md), [assessment extraction](specification/migration/03-assessment-and-prose-extraction.md) | Transfer records, typed edges, scoped crosswalks and owner receipts |
| Relational persistence and rendering | [Structured storage](specification/persistence/01-relational-content-storage.md), [MySQL/MariaDB](specification/persistence/02-mysql-mariadb-physical-contract.md), [reference indexes](specification/persistence/03-reference-index-contract.md), [Joomla runtime](specification/joomla/07-runtime-composition-and-format-boundaries.md) | Canonical native data, exact versions and typed relationships |
| PDF and agent authoring | [Source ingestion](specification/authoring/01-source-document-ingestion.md), [agent production](specification/authoring/02-agent-curriculum-production.md), [portable handoff](specification/authoring/04-portable-agent-handoff.md) | Protected evidence, proposed drafts, verification and reviewed owner apply |

The original architecture summaries remain under [docs/](docs/scope.md). The detailed owner contracts and catalogs govern implementation. A host can map them to its own language, database and framework while preserving the public identities, academic invariants and versioned behavior.

The editable native model is independent of an archive or delivery format. The default delivery export selects the verified SCORM 2004 fourth-edition profile; SCORM 1.2 is an explicit compatibility choice. Native editable backup is a separate operation. [Export capability and round-trip rules](specification/migration/06-export-projections-and-round-trips.md) require exact versions, rights and loss reports, and block unsupported grading or answer-confidentiality behavior.

Private curriculum archives are research inputs outside this repository. The specifications describe structural patterns and generalized implementation requirements. All committed example curriculum, question fixtures and authoring evidence are independently invented. The [read-only audit tool](tooling/audit_curriculum_archive.py) inspects local archives without importing or publishing them; its findings and any detailed reports remain private unless separately authorized.

## Build from a complete workflow

Select a workflow and its acceptance cases, resolve its entities and permission contexts, and implement its owner commands through the intended user interface. Include interrupted requests, stale revisions, invalid transitions and unauthorized access in that slice. An assessment implementation must preserve the exact delivered form and accepted submission. An academic-record implementation must reproduce each issued result from its evidence and policy.

For Joomla, use the component map to allocate every persisted entity and its attached Admin View. Each component has at most five attached definitions, including hidden child views. The ownership domains contain multiple small components delivered as a compatible package. Joomla account services and baseline ACL combine with the application's academic scopes. Nextcloud and Filery integration contracts are described in the [provider adapter chapter](specification/joomla/04-collaboration-and-document-adapters.md).

## Verify and regenerate

Use Python 3.11 or newer and Node.js for the JavaScript fixture runner.

```sh
python -m pip install -r tooling/requirements.txt
python tooling/specification.py validate
python tooling/specification.py check
python specification/assessment/verify-golden-vectors.py
python specification/records/verify-grade-vectors.py
python specification/interoperability/fixtures/verify-fixtures.py
node specification/interoperability/fixtures/verify-runtime-fixtures.js
python specification/interoperability/fixtures/verify-export-projections.py
python specification/migration/fixtures/verify-assessment-fixtures.py
python tooling/verify_reference_contracts.py
python tooling/test_audit_curriculum_archive.py
python specification/authoring/verify-authoring-proposal.py self-test
```

After changing an authored catalog, rebuild its references and check the resulting diff.

```sh
python tooling/specification.py build
python tooling/specification.py check
```

The validators check structured contracts, examples, ownership, permission scopes, component allocation and generated-reference consistency. The fixture runners check their stated deterministic examples. Runtime installation, real-browser package behavior, production load, institutional migration fidelity and formal standards conformance require the implementation tests defined in the chapters.
