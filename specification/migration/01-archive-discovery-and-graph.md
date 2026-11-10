# 01. Archive discovery and graph inventory

## 1.1 What the input can prove

A course ZIP can contain an exported course tree and additional files from a source-control checkout. An archive is evidence of bytes and references at capture time. It may contain a selected published tree, detached definitions, older or alternate course runs, private draft overlays, broken references and assets. A file's folder does not establish visibility, ownership, historical provenance or whether a referenced activity was enabled for students.

The read-only pilot established that a wrapped ZIP can use a pointer-style `course.xml`, contain more than one course definition, place full activity bodies inside unit XML, and keep drafts and alternate policy documents beside an otherwise complete selected graph. It also showed that a metadata file can be empty even when the asset directory is populated. The specification below treats these cases separately. Pilot source artifacts and private evidence remain outside the repository.

| Classification | Evidence | Import outcome |
| --- | --- | --- |
| Selected and reachable definition | Approved root and at least one valid structural edge, or the selected root itself | Candidate for the corresponding editable or package projection |
| Inline definition | Recognized child type with its semantic body in its parent XML | Analyze body and type-specific fields. A separate file is unnecessary |
| Resolved external definition pointer | Recognized pointer and an exact valid type/key definition in the correct scope and layer | Candidate with explicitly linked source provenance |
| Missing ordinary definition | A selected pointer expects a supported type but no usable matching definition exists | Block the dependent placement and require source repair or replacement |
| Unavailable extension definition | An extension pointer is present and no local definition is available under the recognized profile | Report recoverable or blocked dependency. The archive alone does not establish whether an installed extension can recover it |
| Unsupported extension with body | A recognizable inline or separate definition is present but the destination does not implement its semantics | Preserve private evidence and explicitly map, reconstruct, integrate, or exclude |
| Detached document | Definition exists outside selected reachability | Inventory under separate detached scope. Do not publish or classify as removable from location alone |
| Alternate run | Another course definition or run policy exists beside the selected descriptor target | Keep as alternate evidence. Assess as a separate requested import only |
| Unresolved draft anchor | Draft owner, anchor key, source layer, or insertion ordering cannot be established | Hold affected draft changes for review. Selected published projection remains independently valid |

A supported activity can still be blocked by grading, rights, accessibility or missing assets. A present extension definition is distinct from a portable implementation of its behavior. A separate attachment or source-system extraction is a new authorized dependency, with its own TransferArtifact and verified source crosswalk.

## 1.2 Quarantine and descriptor selection

1. Create or reuse a quarantined TransferArtifact with exact content digest and approved storage ownership. Assign a separate TransferJob to the requested source and destination. The file name, outer wrapper and archive creation time are descriptive.
2. Inspect archive headers, compression, sizes, path encodings and archive quotas. Reject traversal, path collisions, irregular files and ambiguous duplicate entries. Structural diagnostics alone do not scan executable content, validate binaries or release bytes.
3. Permit a direct `course.xml` or exactly one single wrapper directory for this ZIP profile. Resolve the wrapper as an archive path only. A wrapper resembling a repository name or default branch does not become part of source course identity. Nested archive layers, multiple competing descriptors and unrelated roots require another explicit profile.
4. Parse the descriptor with DTD, entity declarations, external resolution and network access disabled. A pointer descriptor supplies exact organization, course and run tokens and no embedded course outline. Resolve its exact `course/<run>.xml` child. An inline descriptor can carry the outline itself. Parse the target type and reject conflicting repeated identity fields.
5. Record the selected run definition and exact source run scope before looking for content. A second file under `course/` is an alternate run candidate. Even byte-identical children shared with the selected run do not merge the runs or prove that their grading policies are interchangeable.
6. Locate selected run policy under `policies/<run>/`. Parse `policy.json` and `grading_policy.json` independently using duplicate-key and finite-number rules. Do not choose whichever policy file is found first. Preserve alternate run policy as evidence and report missing or contradictory effective settings.
7. Locate `policies/assets.json`, `assets/assets.xml`, `static/`, editorial pages and other declared optional directories independently. A metadata inventory can disagree with the bytes. Require exact referenced files where behavior depends on them. Do not drop static bytes because a metadata document has no entries.

The detection result is part of the transfer plan. A change to selected root or version changes the plan digest, invalidates related approvals and requires a fresh graph and policy comparison.

## 1.3 Typed tree traversal

The first graph pass enumerates source definitions and structural reference edges. The second materializes ContentPlacement occurrences from the selected root and ordered edge path. Counting definitions does not establish occurrence totals, particularly when the same definition appears beneath two parents or a reused subtree has multiple paths from the root.

| Parent shape | Child structure | Semantics |
| --- | --- | --- |
| Course | Ordered chapter children | CourseVersion outline root and first-level ContentPlacement occurrences |
| Chapter | Ordered sequential children | Module-like grouping and reusable or linked structural definition |
| Sequential | Ordered vertical children | Learner-page definition and occurrence |
| Vertical | Ordered activity, HTML, problem or extension children | Page body, typed ActivityVersion or ContentNodeVersion candidates |
| Nested activity body | Response, prompt, assessment, rubric, configuration and other children defined by the type | Type-specific definition grammar. Do not traverse arbitrary nested tags as course outline nodes |
| Unknown or unsupported structural child | Tagged child with original locator and raw source key when supplied | Record as structural issue. Preserve its original ordinal and dependency impact |

For each edge, retain layer, source parent definition, exact child ordinal, declared type, raw key where supplied, pointer or inline representation, and resolution status. An explicit pointer marker is evidence even if the element carries extra attributes. A bare recognized typed child with a key and no body can be a split reference. A keyed child carrying an actual body can be inline. An attribute-only extension is interpreted by its own profile. If pointer and body coexist and disagree, preserve both pieces of evidence and block selection pending review. Do not decide whether an assessment is present by counting the `problem/` or extension directories.

A resolved pointer targets `<type>/<key>.xml` only if the exact file exists, its root type is compatible and its own identity does not contradict the pointer. Never retry another type, a case-folded name, a guessed slug or a nearest filename. Follow pointers with a visited-definition index and an active recursion path. The active path detects cycles. Repeat references to already indexed definitions remain separate edges. Materialize a bounded occurrence projection only after inspecting the entire dependency graph. Reject cycles and enforce limits on both definitions and occurrences so a deep reused graph cannot expand without bound.

Use immutable staged digests or bytes for input evidence, and deterministic path order for independent inventory. Preserve declared sibling order rather than path order when projecting learning. A missing edge consumes a source ordinal and remains visible as a blocked dependency. Removing it from inventory would incorrectly improve completeness. An unresolved extension does not create an empty native ActivityVersion.

## 1.4 Published tree, draft overlay and detached material

The published selection follows its own pointer paths and never falls back to private draft files. A draft graph may use layer-local definitions and explicit published fallback only when the supported profile declares it. A matching source type/key in both layers commonly represents two revisions of one definition. Keep two source revision records and a verified published and draft relation. Do not use archive order to choose one.

A draft anchor has an exact source parent location and a nonnegative index. Decode the full location into source organization, course, run, type and key. Require the source scope to match the approved run and the parent to resolve in the selected graph. Group anchored changes by exact resolved parent. Evaluate declared indices in the source overlay model, accounting for draft-only insertions, replacements and unchanged published siblings. Two rows requesting the same raw parent index need review when the archive lacks the ordering context to disambiguate them. Do not choose by filename, XML time, source-control order or arbitrary key order.

A detached published definition may be unused in the selected run, referenced by another run, a formerly placed definition or a dependency missed by the profile. Distinguish these cases when there is evidence. Preserve the manifest and locators, with no active ContentPlacement. An operator can authorize a later import as reusable content with rights and provenance. Detached records are never silent additions to the selected course.

### Worked overlay

An invented course has selected run `spring`, a separate `trial` definition and three published pages `north`, `east`, `west` in that order. The draft archive supplies a new page `yard` with parent `module-a` and ordinal 2, then another draft `patio` with the same parent and ordinal. It also supplies a new definition for `east`. Inventory keeps published order and marks the two competing insertions for review. It associates the second `east` definition with the draft version only. The alternative `trial` root and its policy are separately reportable even if its outline is similar. Resolving the draft insertion does not change the selected published CourseVersion.

## 1.5 HTML, settings and static dependencies

Parse the XML wrapper of an HTML component before resolving its companion. A supported companion locator is an exact, safe name in the appropriate directory and source layer. Append the profile extension once. Preserve inline text and CDATA as inert HTML for typed import, with separate sanitization. If both companion and inline content are declared, validate profile precedence and report content differences. Keep authored page links, iframe origins, captions and binary attachments as typed dependencies rather than parsing URLs out of serialized XML or rewriting raw text wholesale.

Policy settings and course metadata are inputs to candidate native policies. They do not automatically grant enrollment, staff access or publication. Apply documented precedence for a recognized profile. Preserve distinct start, due and release timing, enrollment flags, grade categories, weights and visibility. A private draft can contain staff-only visibility even when the matching published node behaves differently.

Track assets in four independent categories. Inventory physical bytes, metadata entries, authoring references, and independently hosted or embedded resources. A reported static filename does not establish legal reuse or reachability. A verified local asset requires byte, format, safety, accessibility and rights checks before its AssetVersion is released. A remote link can be a media, tool, legacy route or ordinary external target. Resolve origin and deployment explicitly. The inspection tool never makes network requests.

## 1.6 Reviewer controls and acceptance

The review screen exposes format, selected run, graph counts by source layer and disposition, selected versus detached records, exact missing dependency categories, and distinct grading and accessibility findings. Authorized reviewers can inspect restricted locators, compare draft against published, attach a verified replacement artifact and repeat the dry run. A default coverage report uses safe aggregate counts. Course content, private URLs, source keys and archive digests never belong in public project documentation.

Accept the structural plan only when ordinary selected pointers, typed placements and selected policies resolve, or every blocking omission has an explicit approved replacement or exclusion. Use separate denominators for supported editable content, playable packages, present but unsupported activity definitions, unavailable dependencies, and detached archive material. Run canonical comparison twice and verify identical inputs and adapter versions yield the same plan and issue classification. Confirm stable placement order and unchanged published view with draft review active.

Run the repository's [ZIP inventory diagnostic](../../tooling/audit_curriculum_archive.py) against privately stored files before transformation.

```sh
python tooling/audit_curriculum_archive.py /path/to/private/course.zip
python -m unittest discover -s tooling -p 'test_audit_curriculum_archive.py'
```

The default output contains counts and controlled diagnostic codes. Exit 0 means that every requested archive was inventoried, including archives with blocking findings. Exit 1 means a container or descriptor was rejected. Exit 2 means the optional private report could not be written. To request detailed provenance, use `--private-details` with a new absolute report path in an owner-only POSIX temporary directory outside the checkout. The file is created mode 0600 and redacts URL credentials, queries and fragments.

The diagnostic is not an importer, asset scanner, complete markup parser or grading parity proof. It enumerates definitions and source edges rather than fully materialized destination occurrences. It reads supported XML, HTML and policy JSON after directory safety checks. Static and other non-markup entries are inventoried without opening or validating their binary contents. CSS and dynamically generated URLs remain outside its parser profile.
