# 06. Authoring screens, agent operations and staged imports

## Screens and interaction contracts

| Screen | Key information | Authorized actions | Failure and recovery |
| --- | --- | --- | --- |
| Course catalog administration | Code, title, owner, visibility, versions, enrollment use, search filters | Create, edit metadata, fork, archive and view publication history | Duplicate code highlights field. Archive preview lists retained offerings |
| Outline editor | Tree positions, required flags, validation status, selected revision and type | Add, reorder, duplicate, replace, remove, undo and link to library | Stale write preserves local changes, offers reload and displays conflict location |
| Activity and resource editor | Typed fields, dependencies, localized variants, preview, validation paths | Save exact revision, attach approved assets, create translation, inspect version diff | Missing plugin or resource disables publication and explains the exact blocking reference |
| Library and template manager | Shared scope, entry versions, usage count, rights, update differences | Publish, adopt, propose distribution, resolve and detach | Permissions can hide private usages. Conflict choice is mandatory before applying |
| Assets and media | Scan state, rights, accessibility tracks and publication references | Upload, approve, replace by revision, withdraw and create accessible derivatives | Quarantine never previews executable files. Retryable scan failure is visible |
| Review and publication | Manifest digest, learner preview, errors, warnings, change impact | Submit, request changes, approve, publish and archive | Publication reruns validation and invalidates changed approval |
| Import review | Staged source hierarchy, mapped destination, warnings, provenance | Correct mappings, replace unsupported items, select proposed edits and apply to draft | Commit can fail without partially changing the draft. Retain the staged report for correction |

Outline reorder supports explicit keyboard move commands and a move-to dialog, in addition to optional drag and drop. Scope badges use text in addition to color. Errors link to controls or expose the key that could not be resolved. Long-running jobs provide status, progress and durable links to reports. Avoid triggering repeated announcements on every minor polling update.

Learner preview accepts section, simulated instant, locale, capability profile and draft revision. Use synthetic enrollment context. A preview banner is persistently visible and exposed to assistive technology. A teacher can preview expected answers only with assessment author or answer-key access. No official attempts, submissions, attendance, progress, communications or provider memberships may be created. A learner preview suppresses staff-only answers and metadata.

## Agent and human command contract

Use the same authenticated, validated commands for human and agent authors. A service principal has only explicitly scoped course and library capabilities. It can prepare drafts and review requests. A human holding the required publishing permission approves consequential changes. A single operation carries an idempotency key and expected revision. Keep request provenance, actor principal, generated or imported status, source attribution and reviewer decision. Do not require internal model prompts to be exposed to learners.

An agent batch stages a bounded ordered list of changes, default 200 operations and 2 MiB per request. Validate against a preview copy and report per-operation key, before and after digests, inferred dependencies and warnings. A caller selects all-or-nothing or named subset apply. For subset apply, the server rejects omissions that strand referenced keys and verifies the preflight digest for the chosen subset. Every applied operation is independently inspectable through the draft change history. Abandoning a batch preserves approved course publications.

## Staged import workflow

1. Transfer verifies format, archive safety, checksums and readable source locations. It creates the staged source map and source identifiers.
2. Curriculum maps course hierarchy, assets, language variants, links and typed activities into candidate draft entities. Unresolved or untrusted elements remain in a staging manifest with disposition, source pointer and blockers.
3. Author selects create new course, fork new draft or patch an existing draft. Patch mode requires explicit expected draft revision and known external identity map. A candidate collision may update an existing mapped key, create an independent occurrence or be skipped after review.
4. Validate the selected patch and pin the staged manifest digest. A duplicate with identical source identity, content and target mapping returns the existing staged/apply result.
5. Apply in a curriculum transaction. Imported revisions and placements appear only in the draft. Return a mapping with current version pointers and unmapped items. Ownership and grading references follow their domain contracts.
6. Publish through normal review. Retain provenance and exact transfer version. A rollback of the draft produces a new draft revision, with existing published course versions unchanged.

## Acceptance walkthrough

An author imports a shared algebra unit containing rich text, a PDF, a video and a versioned quiz. The staging report shows the exact four mappings, two missing video captions and an unresolved grading rule in the imported quiz. The author replaces the quiz through the assessment editor, adds caption tracks and sees each import blocker resolved at its source location. The new outline uses distinct placement keys for the rich text and quiz. A reviewer previews the student surface, author answer preview and alternate locale. The agent proposes one explanation revision in the meantime. The system invalidates the reviewer’s old digest and displays the one changed block. After approving the new digest, publication returns an immutable version and shows the separate offering activation action.
