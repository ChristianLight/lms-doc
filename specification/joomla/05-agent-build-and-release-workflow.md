# Agent build and release workflow

## Build inputs

An implementation task selects a bounded vertical slice and lists its portable entity, command, event, permission and scenario IDs. It also names the exact Joomla target, current production JCB target, PHP/database compatibility range, destination repositories and component allocation. The accepted input is a coherent feature, such as authoring and publishing a lesson for one offering, that can be compiled, installed and exercised through its normal entry points.

Resolve reusable Fields, Admin Views, Dynamic Gets, Layouts, Templates, Joomla Powers and Super Powers before creating new definitions. Use the maintained repository discovery and model-specific identity rules. Keep reusable definition provenance and dependency order. A missing dependency is an explicit build issue, and a compiler success notice cannot override an unresolved class or Power reference. [JCB request-to-extension workflow](https://github.com/joomengine/skills/blob/main/workflows/request-to-extension.md)

## Maintained sources

| Artifact | Source authority | Verification |
| --- | --- | --- |
| Components and views | Complete JCB blueprint graph | Import and reopen expected fields and relationships |
| Ordinary fields and layouts | Reused or independently adapted model definitions | Identity, dependency and target compatibility checks |
| Domain algorithms | Cohesive authored PHP classes maintained as supporting source | Unit/contract tests and actual consuming component |
| Generated output | Compiler artifact derived from maintained sources | Syntax, namespace, loader, route, SQL and asset checks |
| Database migrations | Ordered maintained migration definitions | Fresh install and upgrade from each supported prior version |
| Runtime configuration | Deployment profile and secret references | Readiness checks and least-privilege provider tests |
| Compatibility fixtures | Versioned synthetic and authorized private test corpus | Exact profile, expected outcomes and fixture digests |

Generated files can be inspected to diagnose behavior. A lasting correction is applied to the authoritative blueprint, Power or compiler integration, followed by regeneration. Record the source-to-artifact relationship so a later build does not lose a one-off installed patch.

## Build steps

1. Validate the domain catalogs and generated API/entity references. Resolve cross-domain naming and invariants before creating fields.
2. Prepare the component allocation around cohesive concepts, workflows and authority. Account for every attached Admin View and any useful Custom Admin Views without a view-count threshold. Specify the visible workspaces, internal schema/evidence views, GUID owner relationships, mandatory service dependencies and optional feature requirements.
3. Acquire the selected reusable definitions and inspect the persisted JCB records. Record imported definition revisions and all required supporting models.
4. Author the domain-specific fields, relations, queries, forms and task entry points. Configure JCB's native attached-field permissions, Admin View permissions, menu visibility and GUID selector metadata. Verify owner modal return values as well as consumer fields. Include localization strings, routing and allowed API fields; add only the academic scope and lifecycle guards the generated machinery does not express. See [selectors and ACL](08-guid-relationships-selectors-and-acl.md).
5. Implement the owner command services and connect actual callers. Use the core framework and reusable Powers where they satisfy the contract.
6. Compile with the selected JCB target. Inspect emitted PHP, autoloading, SQL, XML manifests, assets and entry-point registration.
7. Install on a clean disposable Joomla instance and run the selected end-to-end scenarios. Exercise both administrator and site workflows where supplied. Verify the [dependency readiness and activation barriers](09-component-dependencies-and-lifecycle.md), including missing mandatory services, an unavailable optional provider, denied direct routes and cross-component GUID selection.
8. Upgrade from the prior supported package with representative stored data. Verify GUIDs, immutable versions, receipts, grants and academic record lineage.
9. Rebuild from the maintained sources and repeat the critical acceptance slice. Compare dependency closure and artifact manifests.
10. Produce the installable package, maintained editable blueprint, supporting source references and verification report for review.

## Custom algorithms

The LMS requires algorithms beyond generated persistence. These include content graph validation, version rollout, eligibility and date resolution, attempt finalization, math evaluation, grade aggregation, SCORM state and sequencing, and record issuance. Each algorithm has a defined caller, input contract, output contract, owner, failure behavior and fixtures. Do not add an abstraction solely to wrap an already sufficient generated operation.

For a math evaluation worker, the Joomla owner creates a bounded job with exact input digests and registered evaluator identity. The worker returns validated results. For a grade aggregation, the owner calculates from the selected evidence and pinned policy with exact arithmetic. For a package runtime, the Joomla command grants an isolated session and accepts only constrained runtime mutations. Supporting services can run outside a PHP request while preserving the same owner and contract semantics.

## Worker runtime

Joomla scheduled tasks provide an entry point for bounded worker batches. Use a reliable deployment scheduler or supervisor to invoke the worker under the declared service identity. Claim jobs with leases and fencing tokens. Store retry attempts and next eligible time. A timed-out worker cannot commit after a replacement has acquired a newer lease.

A job queue has separate classes for interactive grading, publication/import, provider synchronization and bulk reporting so a large archive does not block an exam submission. Queue limits, batch sizes and fairness are configuration with validated bounds. Submission durability is synchronous with the authoritative transaction even when marking occurs asynchronously. Workers report lag, failure, retry, lease loss and accepted output counts.

## Release gates

| Gate | Evidence required |
| --- | --- |
| Source integrity | Model identities, complete dependency graph, catalog validation and generated-reference consistency |
| Compilation | Compiler target, successful build, resolved classes and no unknown required dependencies |
| Installation | Clean install, schema checks, service construction and expected enabled extensions |
| Functional workflow | User-role journeys through real forms, course player, assessment, records and adapters |
| Concurrency | Duplicate request, stale revision, deadline race, lease loss and uncertain provider response cases |
| Security and privacy | Scope denial, protected data projections, upload handling, private downloads and audit behavior |
| Accessibility | Keyboard and assistive-technology cases on authored content and timed forms |
| Migration | Fixture inventory, faithful supported mappings, exception report and repeat import |
| Upgrade | Preserved identities/history and resumable schema changes from supported versions |
| Recovery | Restored database, objects and secrets with reconciled submissions and issued records |
| Release packaging | Versioned manifests, dependency ranges, reproducible source references and rollback instructions |

## Reporting execution state

The verification report distinguishes executed and passed checks from failed checks, unavailable environment stages and design requirements awaiting implementation. Record exact failures with a minimal reproduction and owner. A fixture expected to be unsupported passes only if the application rejects it with the declared classification and recovery route. Silently dropping content or changing marks fails migration acceptance.

A release is suitable for an institutional pilot when the institution's selected course, assessment and record workflows pass in the deployed environment. A wider release adds the additional capability and load profiles it has tested. Keep the capability manifest machine-readable so installers, authors and importers can determine whether the required feature is available before activating it.
