# 01. Bank, authoring and publication

The assessment boundary owns assessment definitions, exact evidence and accepted marks. The academic records boundary chooses how to include accepted evidence in official results. An assessment can be scored without affecting a gradebook. An interaction receives a value. A scoring criterion turns validated evidence into a bounded mark. A rubric describes human judgment with stable criteria and levels. An assessment assembles item versions under an assessment purpose and configuration. A delivery binds one assessment revision to an offering and content placement.

## Scopes and identifiers

An institution may hold several ItemBanks. A bank has an immutable institution, a named owner scope, lifecycle and an optional inherited license default. The owner may be an institution, organizational unit or course. A Course permission grants access to that course's bank when its policy allows it. Access to one offering never grants access to a whole course bank. An explicit bank grant lists operations independently for candidate preview, reading answer keys, drafting, reviewing, publication, read-only reuse and copying. Scoped grants are additive within an institution and never override a revoked Principal. An author copying a published item needs copy permission on the source and create permission on the destination. The copy records source revision and license, starts an independent identity and requires publication in the destination.

An Item belongs to one bank and has a stable UUID. ItemVersion belongs to one Item and stores a positive revision number, lifecycle, canonical locale, approved locale variants, structured rich prompt, source provenance, content digest and identifiers of all interactions, bindings and asset revisions. ItemVersion can be cloned from an earlier revision. An InteractionDefinition key is unique within an ItemVersion. Local keys remain stable where response meaning stays stable. A choice can change display order or wording while retaining an ID if its meaning stays equivalent. Changing an option from `division` to `multiplication` requires a new choice key and prevents transparent regrade against that choice.

Keep source system identifiers in a namespaced transfer mapping. An item reused in two course placements remains one ItemVersion with two uses and separate attempt histories. Imported identities never overwrite a native entity based on title or slug. The source checksum links to exact bytes and deduplicates identical staged input, without conflating packages that use identical labels.

## Stored authoring form

| Record | Owned fields and links | Constraints |
| --- | --- | --- |
| ItemBank | Institution, owner kind and owner ID, normalized name, status, default license, creation actor and time | Unique normalized name per owner. Archive prevents new use. Existing pinned versions resolve. |
| Item | Bank ID, stable key, creation actor, created time, archived time | One bank per Item. Bank movement after publication uses copy, rather than mutating historical scope. |
| ItemVersion | Item ID, revision, parent version, state, draft lock revision, canonical locale, content manifest digest, taxonomy and outcome references, reviewer, release actor and time | Unique item and revision. One editable draft per Item by default. Published content graph is immutable. |
| ItemTranslation | ItemVersion, locale, translated stimulus and labels, translation reviewer, exact option and interaction key projection | Require exactly the canonical interaction IDs and option IDs. Translations may change notation or formatting only where a declared profile permits it. |
| InteractionDefinition | ItemVersion, key, interaction type, response schema version, display order, stimulus reference, locale overlays and safe configuration | Unique version and local key. Input schema and rendering requirements are mandatory. |
| MarkingRuleVersion | Type key, evaluator version, typed expected input, parameters, score bounds, fixture references, build digest | Bind only a compatible evaluator release. Protect rule read access separately. |
| ItemCriterionBinding | ItemVersion, key, one MarkingRuleVersion or RubricCriterion, referenced interaction keys, maximum, missing behavior and dependencies | Unique binding key. Dependencies form a DAG. Every linked interaction belongs to the same ItemVersion. |
| ItemReviewDecision | ItemVersion, draft content digest, actor, decision, category and comment | Approval applies only to the exact digest. A later edit invalidates the approval. |
| RubricVersion | Rubric identity, revision, label, criterion definitions, level model and total | Published revisions immutable. Formal assessment requires bounded points. |
| ItemStimulusVersion | Reusable stimulus identity and revision, media refs, body, locale variants and accessibility metadata | Resolve pinned version, including when underlying assets are replaced. |

The catalog carries required fields, nullability and indexes. Select item versions by bank and state, or by normalized taxonomy and reviewed locale using an authorization-filtered projection. Maintain a narrow key registry for provider-independent type and format identifiers. Do not index private keys or reference answers into course search.

## Author journey and concurrency

1. A bank administrator creates a bank and delegates scoped author, reviewer and publisher capabilities. The bank management screen shows inherited roles, explicit grants and permitted copy destinations. The platform audit trail records grant creation and revocation.
2. The author chooses a supported type or a blank composite. Create the Item and draft version in one transaction, with idempotency keyed by bank and request ID. Display tabs for prompt, responses, marking, translations, accessibility, preview and usage. A draft created from a published version starts with existing stable interaction keys.
3. The author edits through a draft ETag. Save atomically validates structural syntax and ownership of every referenced asset. Draft save can accept an incomplete answer key and reports blocking issues. The publishing validator must require complete keys, valid domains and fixtures. A stale save returns `412` with the latest draft token and changed section names. It does not merge private rule payloads automatically.
4. A separate protected rule editor shows answer keys and exact grading fixtures. A test console can exercise correct, partially correct, false-positive, malformed, empty, variant and boundary cases. A learner preview uses the candidate serializer and synthetic attempt IDs. Preview never writes a live submission or emits grade evidence. Preview principals need read access to the displayed material and separate permission to reveal answer explanations.
5. The reviewer receives a frozen digest covering metadata, translations, prompt blocks, assets, evaluator versions, private criteria and fixtures. The review screen shows a structured diff, usage count, unsupported transfer capabilities and open warnings. A request for changes reopens authoring against the same draft ID and new version token. Approval freezes the reviewed graph. Use different Principal IDs for author and approver on exams by default. A controlled institutional policy may permit same-principal publication for low-risk formative materials with recorded reason.
6. Publication serializes on Item ID and approves the graph as one logical transaction. Recheck reviewer authority, digest, dependency status and legal capability. Allocate the next published sequence, update the current publication pointer and outbox record. A competing publisher whose digest is stale receives a conflict. An idempotent retry returns the original publication ID.
7. Staff can withdraw a version from new selection with a reason. Affected deliveries report a dependency warning. Existing in-progress attempts keep their resolved form unless a safety suspension is authorized for the delivery. Submitted attempts remain reproducible. A true purge follows retention controls and material license obligations, preserving redacted tombstones where required.

## Publication gates

Validate depth and count limits before traversing graphs. Enforce up to 64 interactions per item, 128 criterion bindings and 100 choice options per interaction by default. Bound the public prompt forest to 2,048 nodes at depth 16 and 256 KiB total normalized public content. A rubric criterion may have ordered score levels, explicit free point entry or a feedback-only maximum of zero with at most one zero-point level. A free-point criterion declares whole or fractional steps, inclusive min/max and descriptive guidance. Detect duplicate, missing or orphaned keys. Require prompts and labels visible to assistive technologies, alt text or a declared decorative asset, keyboard alternatives for manipulatives, transcript or text-equivalent media requirements, and contrast verified in the actual presentation. A publish audit distinguishes automated lint from human accessibility review.

Version the locale normalization and rendering profile. A translated expression may use comma decimal notation but stores the same typed semantics. Apply an explicit fallback chain from requested locale to base language to approved canonical locale. Formal deliveries may require translation availability for selected learner groups and block the start if no approved fallback exists. Candidate previews show the effective locale and fallback disclosure.

Fixture execution requires distinct expected outcomes and unique fixture keys. An evaluator whose fixture passes on the default variant and fails a declared sample is rejected. A published assessment pins the scorer and unit registry builds. A security revocation blocks new evaluation work under a revoked build and leaves submitted evidence pending an approved replacement review.

## Bank retention

Published item versions and their protected marking definitions follow the longest applicable retention of live or historical dependent deliveries. Delete unused abandoned draft graphs only after the draft retention interval and any legal hold checks. Deletion of a bank record means archive and revoke future access. Private key access and use are auditable. Deleting a staff account preserves the principal identifier on earlier publications and moderations subject to the institution's anonymization policy.

## Author acceptance examples

| Case | Concrete expected result |
| --- | --- |
| Concurrent draft edits | D42 at ETag `"d7"` receives two different saves. The first becomes `"d8"`. The second returns 412 and creates no partial criteria. |
| Review invalidated by a changed asset | Approval of digest `h1` pins an image version. Replacing the image in a new draft yields `h2`. Approval of `h1` cannot publish `h2`. |
| Cross-bank copy | Source bank permission permits read-only reuse but denies copy. A copy request fails before creating destination item identity. |
| Language mismatch | Canonical choices A and B are reversed visually in the translation but retain keys and marks. Dropping B from a formal translation blocks publication. |
| Used revision withdrawn | Withdrawal blocks new selection. Candidate who started with the revision can resume the pinned form and the record remains searchable by authorized reviewers. |
