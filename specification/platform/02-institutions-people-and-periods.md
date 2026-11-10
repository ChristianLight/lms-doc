# 02 Institutions, people and academic periods

## Structure

| Model | Ownership and lifecycle | Minimum protected relationships |
| --- | --- | --- |
| Institution | The provisioning control plane creates one root in active state. A reviewed suspension closes interactive services. Closure preserves controlled academic records workflows. | One institution to many units, people, periods, principals and configured providers. |
| OrganizationUnit | Active on creation. Archive only after active child units and operational ownership are accounted for. | Every non-root unit has one parent in the same institution. A root has no parent. |
| AcademicPeriod | Draft, open, closed, archived. A reviewed reopening is available from closed. | An optional parent encloses the child interval. The offering domain relates offerings to periods. |
| Person | Active, inactive, restricted, pseudonymized. Academic relations belong to Person. | One institution to many people. One Person to zero or more human Principals and protected contacts. |
| PersonContact | Pending until proof or approved manual verification. Verified contacts may be revoked. | Each contact belongs to one Person. Shared addresses may occur across people. |

## Organization tree operations

Store each unit's parent. A closure index can persist `(institution_id, ancestor_id, descendant_id, distance)` with unique ancestor and descendant pairs, including each unit's self entry at distance zero. A supported recursive query can replace that index if load tests pass. The authoritative tree version is the Institution authorization epoch.

1. For a move, show old and proposed parent, all moved descendants, affected inherited grants, offering counts, unresolved external relationships and current epoch.
2. Require an authorized administrator and approved impact evidence pinned to that epoch. Acquire institution hierarchy lock before resolving current parents. Reject an ancestor chain containing the moving node and a resulting maximum depth above 16.
3. Update the unit and closure projection, increment institution epoch, and append the audit and organization change event in the same commit. Preserve the prior evaluated path in evidence. Use current path for subsequent access.
4. If a child is concurrently moved or an affected grant is edited, the existing preview is stale. Return a precondition error and require a fresh preview. Do not apply a stale scope diff.
5. Archival requires no active child units or unassigned active offerings in that scope. Historical staff grants and reports still resolve their original identifiers.

Example. Department D is under Faculty F1 and holds course C. An inherited faculty grant for A covers C at epoch 7. Moving D to F2 at epoch 8 immediately makes A's inherited result invalid. A direct grant on C, if present and currently active, still grants only its declared capabilities. A display name change has no effect on scope keys.

## Academic scheduling

Use inclusive starts and exclusive ends for date ranges. An academic year from 1 January through 31 December 2027 is `starts_on=2027-01-01` and `ends_before=2028-01-01`. A child term ending `2028-01-01` is contained if its beginning is on or after the parent start. Two different tracks can use overlapping sibling dates. Period identity, date boundaries, and calendar timezone are independent fields.

- Opening allows new associations. Closing prevents new active offering associations. Existing published deadlines and report snapshots retain their exact original settings.
- The close screen lists open assessments, unfinalized results and unfinished offerings. Policy blocks closing by default when a pending official release requires the period to remain open. An authorized exception includes the specific dependency, approved procedure and reviewer. Such exception does not release or discard pending records.
- Reopening a closed period after official reports were issued requires an independent registrar review. Corrections to results still use grade correction workflows and new report revisions. Direct date edits after opening require a new version with a before-and-after report rather than silent changes.
- A scheduling screen displays the timezone and the inclusive civil dates to the operator. Preview shows calculated boundaries and flags invalid or ambiguous instant inputs as described in chapter 07.

## Person onboarding and offboarding

1. A registrar looks up by authorized stable identifier, then creates or verifies the institutional Person. A CSV or SIS import uses the canonical command and a reviewed mapping. If two identities have similar names, preserve them and send potential duplicates to records review.
2. Create Principals only when a confirmed host account, identity invitation, or service needs interactive access. A learner may have enrollment and an academic record before any account is activated. Create no implicit credentials or role assignments.
3. Link a human Principal to exactly one Person. For institutional service actors, verify named owner, purpose and expiration by policy, and keep `person_id` absent. Restrict each service to its approved classes or commands.
4. Registration, approved name corrections and contact verification use separate screens. The default directory projects ID, display name, state and version, with personal evidence and family contact outside directory queries.
5. When disabling an academic Person, bump linked Principal epochs and fence their interactive jobs. Send desired removal work to collaboration or roster providers. A provider timeout does not keep the local account active. Existing grades, attempts and enrollment history remain attributed.
6. Deactivating a Principal for credential compromise does not mark the Person withdrawn or remove enrollment. A verified second Principal may keep access if policy permits. Activation rechecks current enrollments, role grants and restrictions.
7. Duplicate identities with conflicting official records require controlled registrar remediation. Record aliases or a verified supersession in the institutional records workflow. Do not silently move historical attempts or official reports to another UUID. If an authoritative correction is required, keep attribution and correction evidence.

## Screens and checks

| Screen | Authorized actions | Required state and messages |
| --- | --- | --- |
| Institutions | View and filter state. Request suspend, reopen or close with evidence. | Separate institution status from connector health. Show academic preservation and last recovery verification. |
| Organization tree | Navigate hierarchy, add unit, preview move and archive. | Parent selection excludes descendants. Present before and after inherited authority in a keyboard-operable list. Announce stale review conflict. |
| Academic periods | Add draft dates, preview containment, open, close or request reopening. | Use textual date and zone labels. Show dependency blockers and never imply a closed term deleted its courses. |
| Person directory | Scoped search, registration, policy-authorized display corrections. | No raw contact disclosure. Flag possible duplicate for authorized review. Results excluded by policy have no count or existence side channel. |
| Person profile | View current display and localization values. Open contact verification and list account states. | Pending, verified and revoked are distinct. Show masked destinations, expiration and retry. |
