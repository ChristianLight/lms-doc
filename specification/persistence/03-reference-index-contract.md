# Native relationship indexes and publication bindings

## Authoritative values and derived relationships

The native content model owns editable prose, typed interactions, exact asset references and placement selectors. A renderer reads the authorized owner projection. A database relation index provides bounded queries such as “which retained versions use this asset?” and “which course placements bind this internal link?” It does not replace the typed source, create permissions or turn an imported path into an application identity.

The Platform catalog defines two records. `ContentReferenceSet` proves that an exact source and context have been completely inspected under a versioned projection profile. `ContentReference` represents one typed relationship in that complete generation. A source with no outgoing references still has a ready set, count zero and the canonical empty-collection digest. Absence of rows cannot establish absence of dependencies.

| Record | Identity and key | Purpose |
| --- | --- | --- |
| ContentReferenceSet | Application GUID; unique institution, source kind, exact source version and non-null context key | Complete coverage, source/graph digests, generation, projection profile and operational revision |
| ContentReference | Derived row GUID; unique set, generation and semantic-key digest | Typed target columns, source diagnostic pointer, publication requiredness and fragment |
| Original native owner | Its existing record and revision identity | Editable values, history, visibility, publication and retention authority |

The projection is required for the declared publication and retention workflows. A complete authoritative locked scan may substitute when repairing an unavailable index. A stale projection cannot silently become an optional check during asset deletion or course publication.

## Source resolver registry

Dispatch `source_kind` through an installed allowlist with fixed code, tables and schema versions. Never interpolate a submitted entity name into SQL. The initial source families are ContentNodeVersion, ActivityVersion, ItemVersion, ItemTranslation, ItemStimulusVersion, MarkingRuleVersion, RubricVersion, LearningRuleVersion, InteractionDefinition and ItemFeedbackRule. Some kinds yield no outgoing references under a particular schema. They still produce coverage evidence when included in the census.

Each resolver supplies the exact source ID, institution, canonical reference-bearing digest, visibility class, retained/publication state, immutable-version or mutable-draft concurrency token, accepted schema profile and extraction function. It identifies the parent aggregate to fence. For an interaction or translation row, the parent item version controls approval and information disclosure. Protected feedback and answer-related assets must be included in dependency integrity while remaining invisible to ordinary learners and unauthorized authors.

The registered schema declares reference-bearing locations. It is insufficient to recursively collect every UUID-shaped string: a distractor may contain a number, a quoted identifier may be ordinary text, and a stable placement key has different semantics from a ContentPlacement row ID. Unknown schema revisions block this projection. Do not accept a partial set produced by skipping unfamiliar fields.

Direct approved HTTPS links remain typed editorial URL values, subject to URL and content security policy. A managed provider relationship uses ExternalResourceMap only when a real approved provider mapping exists. The index must not create fake provider objects for every public website link. URLs with credentials, source assessment answers, raw PDF text and imported customer locators do not belong in these index rows.

## Stable semantic keys

Use a source-local typed reference key where the schema provides one. Otherwise the profile derives a key from locale, stable containing block or interaction identity, relation role, canonical target identity and fragment. Canonicalize the tuple with a length-delimited encoding. For repeated indistinguishable edges, number occurrences within the identical semantic tuple rather than within the whole paragraph. Reordering unrelated paragraphs or changing a display label then leaves unrelated keys unchanged.

The `reference-projection/1` profile uses ASCII semantic keys. Its entries digest is SHA-256 of RFC 8785 canonical JSON encoded as UTF-8, with no whitespace or trailing newline, containing the array of rows sorted lexically by `reference_key`. Each row is `[reference_key, relation, target, anchor_or_empty, required_for_publication]`. An exact target is its lower-case canonical UUID; a deferred selector is `[placement_key, "same_course_version"]`. The row grammar contains only arrays, strings and booleans, so RFC 8785 number serialization cannot vary here. Preserve valid Unicode strings without extra slash or Unicode escapes and reject ill-formed scalar sequences. Booleans use JSON `true` or `false`. A missing anchor is the empty string. The empty collection is exactly `[]`. Row GUIDs, generation counters and diagnostic pointers are excluded from this semantic digest; source and graph digests separately pin their authoritative context.

An RFC6901 `field_pointer` records where the current normalized payload carries the relation. It is diagnostic evidence and can change after an edit. It is not the persisted semantic key and is not used for external source crosswalk matching. A reference-key digest supports bounded database indexes; compare the complete key before treating a collision as equality. A collision with unequal complete values is an integrity error, not an opportunity to merge rows.

The source version plus complete generation is the boundary of this derived identity. Moving a link to another owner or creating a new publication need not preserve a derived row GUID. It must preserve the canonical content/placement identities required by the authoring and migration models. No learner bookmark, assessment attempt or external object map should point at a ContentReference row.

## Two contexts

### Definition context

The non-null context key is the literal `definition`. Placement and course-version columns are absent. An exact asset, package, assessment, native content or managed provider reference resolves to its typed version. A course-relative internal link retains a bounded `placement_selector` containing a stable placement key and `same_course_version` context. The anchor is stored once in the top-level reference field.

A reusable definition can therefore remain independent of a course that adopts it. It does not acquire a global link target from whichever course happened to import it first. Definition extraction validates the selector shape and owner schema; it cannot establish whether every later use contains that target.

### Placement context

The context key is the exact source ContentPlacement GUID. The set pins its CourseVersion, graph digest, matching ready definition set and definition generation. The source placement's transitive dependency closure must include the exact indexed source version: for an assessment item this includes the published assessment and pinned item or pool relationship, rather than a direct content-node comparison alone.

Resolve each same-course selector against stable placement keys in that exact course graph. Store the resulting exact target ContentPlacement identity and validated anchor. A required selector with zero or multiple candidates blocks publication. An exact target placement from another course version is rejected. Cross-course linking needs a separately specified capability and independent target access, rather than an unreviewed fallback to a similarly named unit.

The binding refresh checks the ready definition set and generation under its commit fence. Matching source digests are insufficient if a projection-profile change or repair produced a newer definition generation. Rebuilding a definition set invalidates dependent placement bindings until the new generation has been consumed.

## Typed target constraints

Each ContentReference has one `relation` discriminator and exactly one matching target column. For example, `asset` requires `asset_version_id` and forbids package, placement and other alternatives. `placement_selector` requires its selector object and forbids exact target columns. Missing alternatives are omitted in the API and represented as SQL NULL only where the physical schema requires it; they do not enter a logical unique key.

The catalog's cross-field `schema_rules` are included in generated JSON Schemas. The host must translate applicable discriminator rules into physical CHECK constraints or equivalent owner validation in the same transaction, and test them on both supported database engines. References to actual rows use typed GUID columns with indexes and same-institution validation. The polymorphic source kind/version pair resolves through fixed owner code; a universal GUID lookup or arbitrary-table join is prohibited.

Retain independent target indexes for assets, exact placements, assessments, packages, managed resources and native definitions. Reverse queries join through the set and require the current ready generation. A course graph check also pins course version and graph digest. The set's institution and source authority constrain the query before pagination or counts.

## Refresh and invalidation

`RefreshContentReferenceSet` is a trusted owner/reconciliation command, not a generic editor for relation rows. The request selects an authorized source and expected digests; the service obtains actual content from the registered owner. The caller does not submit arbitrary relationships to manufacture a dependency, suppress an existing reference or obtain access to a target.

1. Authorize the source, target context and registered worker or owner invocation. Receipt replay repeats authorization.
2. Read the source and graph optimistically to discover the complete lock set. Include target retention fences, source aggregates, relevant graph and definition generation.
3. Acquire all required locks in the shared deterministic order used by reference creation and target retirement. Re-read the source, graph and retained-source census. If the needed lock set changed, release and restart; do not append out-of-order locks to an existing transaction.
4. Extract each schema-declared relation. Check unique semantic keys, pointer validity, target family, institution and retained version. Resolve placement selectors where appropriate.
5. Compare expected source/graph tokens and set revision. Prepare one complete generation, including zero entries. The baseline has an explicit per-source reference limit; overflow returns a classified error and never truncates content.
6. Replace the active generation and store count, sorted entries digest, profile and ready state in one transaction with its outbox record. Bindings also pin the exact definition generation. A failed or interrupted replacement cannot publish a partial ready receipt.

`InvalidateContentReferenceSet` runs within the source mutation transaction or an authorized repair. It marks affected definition and placement sets stale and advances their revisions. Owner publication and destructive retention checks then fail closed until refresh succeeds. A remote-service deployment must provide an equivalent publication barrier; asynchronous delivery without a barrier does not preserve this invariant.

The shared order applies to ordinary author edits, imports, agent-applied drafts, reimports, target withdrawal and purge. A deadlock or serialization victim retries the entire fenced operation with bounded backoff and the same request identity. Do not replay only the final index insert after losing the source transaction.

## Retirement and the complete census

A reverse index answers which indexed versions point at a target. It cannot prove that every retained source was indexed. Before a destructive action, the target owner obtains an authoritative census of all relevant retained reference-bearing source versions and publication contexts, including hidden drafts, protected marking rules and archived history. Each requires a current complete set or an equivalent locked source scan.

With the target retention fence held, recheck for newly created sources and references. A concurrent creator needs the same fence, so it either commits before the census and is included, or observes retirement afterward and fails. If source discovery changes the planned lock set, restart safely. Broken, stale, unsupported or missing coverage blocks purge and creates a reconciliation task.

Withdrawal from learner use and deletion of historical bytes are different operations. An institution can withdraw a resource while retained attempts, evidence or issued records still require its immutable version. Do not delete such bytes merely because no currently open course displays the resource.

## Diagnostics and privacy

`ReadContentReferences` supports an authorized human or service viewing an exact ready generation. It does not require service-only refresh authority. Recheck source visibility and protected field classes, then check each target disclosure. Suppress an entire relationship when even its existence is protected. An `unavailable` indication is allowed only where the viewer may know that the reference exists. Cursor tokens and total counts must not reveal hidden rows.

`FindContentDependencies` is a set-level reverse lookup. Filter individual relationships by source and field visibility first, then deduplicate by exact set ID and generation. One authorized source set using an asset twice produces one result. Order by source kind, source version, context key, set ID and generation, with a cursor bound to the authorized target and generation selection. A changed selection invalidates the cursor. A filtered empty result is not proof that the target is unused.

The user-facing inspector can show semantic reference key, source field location, relation family and permitted target label. It must not copy private source XML, answer keys, PDF snippets or credentials. A valid GUID in a query confers no additional authority. The underlying Admin Views remain read-only diagnostics managed by JCB, with owner commands responsible for changes.

## Verification

The repository provides original synthetic contract vectors for valid exact targets, empty coverage, required placement context and mixed-target rejection. These verify schema rules, not database locking. Implementation acceptance separately exercises simultaneous reference creation and purge, source edits during rebuild, definition generation changes with unchanged source bytes, empty versus missing sets, stale generation pagination, protected relation suppression and restore/rebuild from authoritative snapshots.

Run the same concurrent cases with different physical row IDs, mixed database collations and explicit rollback. Compare canonical GUID relationships and complete receipts. A rebuild is successful only when the source census, current set generations and exact relation counts reconcile without consulting rendered HTML as authority.
