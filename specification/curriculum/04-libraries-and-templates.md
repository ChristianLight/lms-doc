# 04. Content libraries and managed template propagation

## Library reuse and scope

A library belongs to an institution and optionally an owning unit. It has a unique normalized code, sharing mode, license policy and role grants. A library entry has a stable ID, library, item key, kind, definition identity and metadata. Its published versions pin a ContentNodeVersion, ActivityVersion or reusable outline fragment. A collection is a named ordered list of entries with no duplicated position. Search indexes include normalized title, language, type, owner and learning alignment and apply source ACL before showing results.

An adoption stores source entry version, destination draft or template link, stable destination placement key, adoption mode, source digest and consent to local edits. Linked adoption can receive proposed updates. A detached copy creates independent IDs and stores provenance. Either mode records asset and library rights. A public description can advertise an entry without providing authority to copy its bodies or assets. Revoking future reuse leaves existing pinned dependencies resolvable under the approved license and withdrawal policy.

## Blueprint and consumer contracts

A template is a published course-shaped outline or fragment with a normalized template key and version history. Every distribution identifies the immutable base template publication, target draft and source-to-destination placement mapping. One destination key may have only one active managed parent. Authors can use independent template fragments in different areas as long as protection scopes never overlap. Template cycles are invalid.

| Field group | Default ownership | Merge behavior |
| --- | --- | --- |
| Structural location and order | Template | A template move is a candidate change. Local moves conflict if both source and local position changed |
| Core body and core objectives | Template | Protected by default in managed distribution. A local change is a conflict and must be explicitly approved or detached |
| Local explanatory note and examples slot | Destination | Preserve when the template leaves it unchanged. Removing a containing template placement is a conflict |
| Due dates and roster | Offering | Excluded from template distribution unless the template declares suggested, unbound schedule offsets |
| Answer keys, assessment rule and active runtime | Assessment | Carry approved assessment version references only. Verify recipient permissions and reassess rollout compatibility |

Protection is evaluated per JSON Pointer or structural aspect. Default protected fields include payload, requiredness, prerequisite rule and structural presence. Local schedule, display aliases and named extension points are editable. An override requires a capability and writes a decision with target path, prior and new values or their digests, justification, approver and expiry where applicable.

## Three-way update algorithm

The merge compares B, the last adopted template baseline, S, the newly published template source, and D, the current destination draft.

1. Normalize identifiers through the adoption map. Compare exact typed fields and content digests, exclude runtime state and resolve asset permissions.
2. For each keyed occurrence and field, if S equals B retain D. If D equals B accept S. If S equals D keep the matching value. For unequal changes record a conflict and leave D untouched in the planned draft until resolved.
3. Represent add and delete as distinct changes. A source delete conflicts with local edits, outside references or dependent local content. A destination delete conflicts when the source changed the deleted occurrence.
4. Merge parent keys and sibling ordering separately. Reject a resulting cycle. For compatible moves, order new siblings by mapped template order followed by destination-only siblings anchored to their nearest surviving predecessor. Concurrent incompatible reorders require an explicit full sibling list.
5. Review conflicts with field-level base, source and destination values. Protected fields default to source after reviewer approval. Local fields default to destination after reviewer confirmation. Structural deletes require all inbound references resolved.
6. Apply to a target draft with its expected revision. Atomically update the draft and adoption baseline, record choices and emit a template distribution event. Previous publications and offerings continue to pin earlier content until publication and explicit activation.

Avoid cross-institution leakage through previews. If the caller loses access during merge, replace detailed source values with an unavailable indicator, stop commit and preserve the destination draft. A batch distribution to twenty courses creates independent target merge plans. A failure in one course leaves the other nineteen unaffected and visible in the job report.

## Worked cases

| Case | B | S | D | Resolution |
| --- | --- | --- | --- | --- |
| New copy edit | original | correction | original | Adopt correction |
| Local note | absent | absent | note | Retain note |
| Protected course text | paragraph A | paragraph B | paragraph C | Require a reviewed conflict resolution |
| Removal with local dependencies | lesson L | absent | lesson L with local link | Stop apply for L until the link is removed or moved |
| Assessment reused twice | one version 3 adoption | version 4 | two linked placements | Propose version 4 at each mapped placement independently, preserve the two keys and separate attempt contexts |
| Lost asset rights | shared asset accessible | shared asset inaccessible | earlier licensed digest | Flag publication blocker for new adoption. Existing retention depends on the prior rights decision |

Offer separate buttons for use linked, copy independently, view affected courses, propose update, resolve conflict, detach and publish a reviewed draft. Show update availability and version provenance in both authoring and library listings. A screen reader announces conflict row count and each changed field's context. Avoid exposing private destination titles when listing cross-unit usages.
