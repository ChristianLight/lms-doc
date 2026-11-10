# Identities, generated forms and persistence

## Four identity layers

| Layer | Purpose | Persistence rule |
| --- | --- | --- |
| JCB definition GUID | Identifies a blueprint Field, Admin View, Power or other definition | Preserve when reusing the same definition. Allocate a new definition identity for an independent adaptation |
| Application GUID | Identifies a course, learner enrollment, item, attempt or record | Immutable, unique within its typed owner and stable through import/export |
| Joomla local integer ID | Supports local Table, controller and asset relationships | Generated locally and never assumed portable across installations |
| Business or external key | Catalog code, course run code or source-system key | Scoped uniqueness and mutable policy independent of the application GUID |

New application relationships use GUIDs while preserving numeric primary keys for Joomla's normal row handling. Relationship selectors, filters, query joins and input validation treat these values as strings. A supplied UUID must resolve in the correct typed table and institution. It cannot be accepted because the same string exists in an unrelated table. The JCB identity workflow requires checking the actual generated uniqueness constraints and save lifecycle. [Application identities](https://github.com/joomengine/skills/blob/main/packages/workflows/application-identities.md)

The [GUID relationship and ACL chapter](08-guid-relationships-selectors-and-acl.md) specifies the actual JCB field metadata, owner table/title/key mapping, selection and New/Edit modal behavior, save-time checks and the host-account-to-attempt linkage. Component regrouping changes proposed table ownership and routes; it does not change the canonical academic GUID or authorize remapping an existing learner to another identity.

## GUID creation and import

A new interactive row allocates its application GUID once before any dependent child is created. A retried command binds to the same staged GUID through its receipt. An authorized import may preserve a valid incoming GUID if the source ownership and collision rules permit. Otherwise the importer allocates a destination GUID and writes an ExternalObjectMap record before resolving references.

The generated save path must distinguish omitted, explicit null, malformed, duplicate and changed GUID values. Inspect the target compiler's normalization order before relying on a later save hook to see the caller's original input. Capture and validate original mutation input at the supported controller/model boundary when an import-preservation rule requires it. Never restore an arbitrary submitted GUID after a generic generated normalization step without validating uniqueness, ownership and authorization.

For edits, preserve the stored GUID. A canonical case normalization can retain identity if the UUID parser confirms equivalence. A different nonempty identity is rejected. Save as Copy allocates new logical identities according to the domain's copy policy and maps its owned children. It must not accidentally adopt the original parent's attempts, enrollments or released results.

## Field mapping

| Logical field | JCB and database mapping | Required checks |
| --- | --- | --- |
| UUID | Immutable application GUID string with explicit unique index | Installed uniqueness, canonical parser, same-scope reference validation |
| Exact decimal score | Bounded DECIMAL or canonical decimal text with owner arithmetic | No binary floating-point conversion, defined scale, range and rounding |
| Instant | UTC timestamp with adequate fractional precision | Read/write round trip, policy time zone stored separately |
| Effective local schedule | Local date/time, zone, resolution rule and resulting UTC instant | Ambiguous and nonexistent local time handling |
| Enumeration | Defined scalar vocabulary | Server rejects unsupported values and upgrades preserve old meanings |
| Typed JSON value | JSON or text containing validated versioned payload | Decode limits, schema validation, output encoding and digest where pinned |
| Foreign identity | Indexed scalar application GUID | Typed target, institution, existence, access and deletion rules |
| Revision token | Monotonic integer or owner-issued opaque value | Conditional update and concurrent-save tests |
| Immutable evidence | Insert-only record exposed through authorized task operations | Generated edit, publish, trash and delete routes disabled or guarded |
| Private file reference | AssetVersion or accepted submission reference | Owner authorization at download, immutable version and retention |

A readonly control does not make a field immutable. A hidden field does not protect a relationship. Enforcement lives in the owner command and database constraint where possible, and every entry path calls that command.

## Normalized collection editors

A repeated editor that persists child rows needs a real child Admin View, attached database fields, a parent GUID relation, and the complete get/save dependency graph. The ordinary normalized subform workflow performs collection replacement. Its omitted-child and malformed-collection behavior must be accounted for by domain validation before persistence. [Normalized subforms](https://github.com/joomengine/skills/blob/main/packages/workflows/normalized-subforms.md)

For an LMS full-collection edit, validate the complete input and parent revision before applying any row removal. Verify every existing child belongs to the submitted parent and institution. Allocate identities for new rows, preserve allowed existing identities, reject duplicates, validate ordering and enforce maximum collection size. Apply the parent and child changes in the owner's transaction so a later child failure cannot leave a partial roster, outline or rubric.

A field omitted from a PATCH request means preserve that collection. An explicit empty array means remove all editable children only if the command allows it and no protected dependency prevents removal. A malformed value fails validation. Never normalize malformed input to an empty collection at the application boundary. A deletion request involving published or referenced evidence becomes a retirement or new-version operation under the domain rules.

## Generated CRUD and academic commands

Use generated CRUD for records whose lifecycle is ordinary mutable administration, such as descriptive catalog metadata or a draft vocabulary. Configure accepted fields, forms and permissions explicitly. For publication, enrollment activation, submission sealing, grade posting or report issuance, route the task to the corresponding domain service. The generated save controller must not bypass this transition by changing the status column directly.

Importers, webservice routes, scheduled tasks and administrative repair screens call the same services. Where a generated route cannot enforce the command's semantics, disable that route and expose a specific operation. Do not expose raw state, marking-rule, answer-key, receipt or audit tables through a generic automatically generated API.

## Query construction

Use Dynamic Get for normal list/detail retrieval when it can express the required relations, filters and projections. Bind institution, principal and authorized scope from trusted context. User-supplied filters can narrow the permitted set and cannot replace the scope filter. Add owner query services when a calculation or authorization rule cannot be expressed safely in a generated query.

Inspect generated joins for duplicate rows and accidental exclusion when optional relationships are absent. Gradebook and roster pages require bounded pagination and stable ordering. Counts use the same authorization predicate as the listed rows. Download and export queries apply the same release and privacy rules as the interactive screen.

## Persistence acceptance

1. Create two institutions with overlapping course codes and distinct GUIDs. Confirm selectors and API routes cannot cross their scopes.
2. Import the same course graph twice into a site whose numeric IDs differ from the source. Confirm stable GUID relationships and a replay receipt.
3. Submit a stale parent revision while another editor changes an outline. Confirm the stale save cannot purge the newer child rows.
4. Attempt to change a stored GUID through administrator, API and import entry points. Confirm the declared preservation or rejection behavior.
5. Copy a course draft and verify new identities for copied definitions and placements with retained lineage.
6. Attempt to edit a published ItemVersion or issued GradeResultRevision through a generated model route. Confirm the owner requires a new revision.
7. Compile twice from the same maintained blueprint and compare schema and dependency resolution. Persisted fixes must survive regeneration.
