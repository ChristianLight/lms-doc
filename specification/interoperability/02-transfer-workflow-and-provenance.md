# 02. Transfer workflow and provenance

## 2.1 Record ownership

The interoperability module owns TransferArtifact, TransferJob, TransferRecord, TransferIssue and ExternalObjectMap. Source connector identity is part of a tenant-owned namespace and never inferred from user-supplied host text. Curriculum, assessment and learner record domains own their native projections and accept typed stage and promote commands. Adapters cannot write native persistence directly.

| Record | Identity, indexes and ownership constraints |
| --- | --- |
| TransferArtifact | UUID. Store Institution ID, byte and content fingerprints, original name, size, strict detected MIME, platform-owned StorageObject identity and generation, inspection status, retention deadline, source namespace, uploader Principal and rights status. Unique digest with Institution and storage trust scope. Index status, scan time and expiry |
| TransferJob | UUID and required Institution ID. Exactly one artifact for import and one immutable selection for export. Pin adapter, ruleset, target namespace, actor, idempotency key and plan revision. Index Institution, state and update time |
| TransferRecord | UUID. Uniqueness over job, source scope, object kind, source key and source revision. Retain original source locator, optional parent ID, dependency IDs, source fingerprint, staged target identity and mapped version. Index job and disposition, plus target kind and ID |
| TransferIssue | UUID. References job and optional record. Stable issue code and evidence key are unique per job and source location. Include blocking, warning or information severity, confidentiality, review state, actor and reason |
| ExternalObjectMap | UUID. Unique Institution, namespace, kind, parent scope and external key. Map to canonical identity and owner domain. Retain tombstone status and revision map. Index target kind and ID for reverse reconciliation |
| TransferApproval | UUID. Links job, plan revision, approving Principal, scopes and a digest of reviewed changes. Record mapping or publication approval as separate kinds. Index job, type and time |

Source keys are opaque NFC text with case retained. Scopes are structured tuples rather than string concatenations that allow ambiguous delimiters. Fingerprints capture source version and immutable content. A migration adapter can preserve original XML lexical detail under restricted access, but canonical authoring sees typed content and independently sanitized media. Answer keys and personal data follow the owning module's policy when shown in previews or exports.

## 2.2 Job states and leases

| State | Entered by | Next states | Durable behavior |
| --- | --- | --- | --- |
| `received` | Upload finalization | `quarantined`, `failed`, `cancelled` | Pin exact artifact digest and uploader ownership |
| `quarantined` | Intake worker | `validated`, `failed`, `cancelled` | Isolate raw bytes. Store detection signature, scanner results and quotas |
| `validated` | Adapter worker | `staged`, `failed`, `cancelled` | Store typed source graph and immutable adapter build |
| `staged` | Transformation worker | `awaiting_review`, `failed`, `cancelled` | Store planned owner commands and candidate graph fingerprint |
| `awaiting_review` | Review queue | `approved`, `staged`, `cancelled` | Issues and staging edits are versioned. Any change invalidates prior approvals |
| `approved` | Authorized reviewers | `applying`, `awaiting_review`, `cancelled` | Pins exact plan version and baseline owner revisions |
| `applying` | Promotion coordinator | `applied`, `awaiting_review`, `failed` | Block competing promotions to identical target. Partial staging remains private |
| `applied` | Promotion coordinator | Terminal | Store active plan receipt and reconciliation report |
| `failed` | Worker or coordinator | Terminal | Retain cause, sanitized evidence and restart eligibility |
| `cancelled` | Authorized requester | Terminal | Revoke pending grants and schedule private staging expiry |

Lease claims use a fencing epoch that increases on every reclaim, plus expiry timestamp and worker identity. Default lease is 60 seconds with a 15-second heartbeat. A stale worker may finish local calculations but cannot commit new durable state after its lease epoch changes. Persist checkpoints by source entry and graph partition. A retry uses the same artifact digest, plan idempotency key and stable transfer record identity. A parser version upgrade starts a separate job. Cancelling after promotion has begun sets a request flag and waits for the coordinator to report whether any visible cutover occurred.

## 2.3 Intake and attack controls

1. Require `interoperability.transfer.start` for the owning Institution and declared scope. The operator chooses known namespace or requests one, archive profile or auto-detect, and migration mode. Default mode is dry run.
2. Upload through a private StorageObject registered to the exact Institution, TransferArtifact generation and approved purpose. A multipart session has explicit whole-file and per-part digests, byte offsets, maximum size and expiry. Parts are immutable at the same offset. Repeated identical part writes succeed. Conflicting bytes at one offset fail. Finalize only if offsets fully cover the declared size and the actual overall digest equals the submitted digest.
3. Inspect ZIP central directory and local headers consistently. Reject ambiguous encoding, encrypted entries, symlinks, nonregular entries, duplicates, path traversal and filesystem-normalization collisions. Inspect tar type flags and reject unsafe extended-path or link behavior before extraction. Apply quotas to compressed bytes, actual expanded bytes, entry count, file count, nesting and worker time. A reported file length does not substitute for counting bytes during decompression.
4. Detect profiles by root manifest and schema signature. Enumerate candidate roots without unrestricted recursive extraction. Refuse multiple independently valid roots except when the selected adapter explicitly supports nested packages.
5. Parse XML with DTD and external entities disabled. Use pinned local schemas and disallow schema resolution on the network. Use strict JSON and TOML readers with duplicate-key errors. For every untrusted document set size, token, element depth, recursive reference and table-count limits.
6. Record malware scanner version and outcomes. A scan success is one input to classification. A report of unknown code keeps execution disabled. Store only sanitized snippets in ordinary job logs.
7. Preserve exact originals when retention requires it. Source files containing code, access credentials, learner data or signed external URLs need privileged retrieval and deliberate redaction in review views.
8. Remote media acquisition uses a separate authorized fetch command. Resolve all addresses, block private and metadata networks, validate every redirect, use approved hosts, stream through byte and time limits, and remove sensitive request headers. Store fetched content with its own digest and acquisition time.

## 2.4 Identity resolution and three-way comparison

Map by the tuple of Institution, source namespace, object kind, stable parent scope and external key. Stable parent scope uses the source offering or course identity when IDs repeat across runs. Do not substitute a file name, title, locale, content digest, temporary mount path or opaque target URL for source identity.

For each record, call the currently observed source fingerprint `S_new`, last accepted source fingerprint `S_last`, prior promoted target fingerprint `T_last`, and current target fingerprint `T_now`.

| Condition | Resolution |
| --- | --- |
| No map | Propose new canonical identity, unless reviewed explicit adoption exists |
| `S_new = S_last` and `T_now = T_last` | Retain map and suppress writes |
| `S_new = S_last` and `T_now != T_last` | Retain local changes and report an informational divergence |
| `S_new != S_last` and `T_now = T_last` | Propose new target revision from source |
| `S_new != S_last` and `T_now != T_last` | Require merge, source rebase, destination fork, or acknowledged exclusion |
| Source key absent from subsequent artifact | Mark retirement candidate only if the export is an authoritative full snapshot |
| Map target missing or archived | Block new binding pending authorized reconciliation |

Retain both base and proposed versions for a merge. Resolve repeated inputs using deterministic source tuple ordering. A merge can approve distinct source fingerprints for content and marking rules. An item change that affects maximum score or evidence requires grade-owner approval even when the text edit is harmless. Never merge active attempt evidence by replacing its pinned definition. Source record count, mapped record count and issue count must reconcile.

## 2.5 Publication transaction

1. Snapshot destination versions, active publications and protected references. Build a graph of planned owner commands. Validate target definitions first and relationships second to allow forward references.
2. Apply owner commands under one database transaction when modules share a transaction boundary. Otherwise write private staging with a release gate. Track owner receipts and job-plan ID. Commands must be idempotent and compensable before the visible release pointer changes.
3. Revalidate baseline revisions and reviewer authority immediately before promotion. Use compare-and-swap on both job plan and the target revision. If either changed, move to `awaiting_review` and retain staged evidence.
4. Publish only after verifying every required relationship and native domain invariant. For a multi-owner staged plan, a single release barrier exposes the staged generation after all owner receipts arrive. Read projections include only activated generations.
5. Persist external mapping receipts and audit outbox entries in the same transaction as the release barrier. Downstream workers reconcile by job and plan revision.
6. Post-release changes use native correction, archival or new publication commands. History and attempts remain pinned to their original content and grading definition. Rollback may point future offerings to an earlier approved generation and never edits historical evidence.

## 2.6 Remediation and UI

The review inbox groups issues by course, library, source locator and severity. Suggested remediation shows an authorized preview, original and candidate type, expected loss, effective user impact, and any dependency on another issue. The operator can assign a reviewer, attach replacement media, explicitly map a source reference, approve a non-blocking loss or re-run. An unsupported marking rule, absent mandatory asset, unresolved prerequisite, invalid signature, or privacy-relevant unknown extension cannot be dismissed as a cosmetic exception. Reclassifying a blocking issue requires the owner to supply a valid alternative and re-run the affected records.

Import preview includes equivalent source and destination screen states, keyboard path, alt text, captions, assessment response fixtures and policy differences. Hide protected solutions from an operator without assessment-answer authority. Announce progress changes, preserve focus when refreshing issue lists, provide filterable sortable tables, and export loss reports as accessible CSV or JSON. Status pages show both last heartbeat and authoritative state so a delayed worker does not look complete.

| Code | Standard operator action |
| --- | --- |
| `PACKAGE_PATH_REJECTED` | Obtain a freshly exported archive with valid paths |
| `SCHEMA_UNSUPPORTED` | Choose an allowed profile or obtain a supported export |
| `DEPENDENCY_MISSING` | Attach source library or asset with provenance |
| `SCORING_PARITY_FAILED` | Assign assessment reviewer and approve a verified replacement rule |
| `TARGET_REVISION_CHANGED` | Review latest destination state and rebase the transfer plan |
| `IDEMPOTENCY_CONFLICT` | Use a new operation key only after confirming the intended new input |
| `SOURCE_RIGHTS_UNVERIFIED` | Record approved reuse evidence or replace the affected object |
| `SCOPE_ACCESS_DENIED` | Use an actor with authority for this exact target scope |

Acceptance tests include archive bombs, header disagreement, mixed-case asset collisions, invalid JSON duplicate keys, namespace impersonation, cyclic prerequisite references, order-independent ID allocation, changes made between approval and promotion, expired lease fencing and side-effect replay. See `catalog.json` for command and payload contracts.
