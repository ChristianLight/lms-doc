# Collaboration and document adapters

## Provider roles

Nextcloud supplies the selected collaboration service. Filery supplies the selected document-management integration. The LMS owns the academic context that authorizes membership and evidence. A provider adapter projects approved scope to the provider and records remote state. It does not create an alternative gradebook or authority for examination eligibility.

Use IntegrationConnection for the provider configuration and ExternalIdentity for linked remote accounts. ExternalResourceMap identifies the provider room, group or file resource associated with an LMS scope. SyncRun and SyncChange record planned and applied changes. Provider credentials are stored through the deployment's secret mechanism and referenced by credential identity, with rotation and revocation recorded separately from academic entities.

## Nextcloud capability discovery

At connection setup, verify the configured HTTPS origin and discover server and app capabilities. Record the supported Talk API version, participant operations and available identity/provisioning capabilities. Refresh this record after provider upgrades or a capability hash change. A failed discovery leaves the connection inactive with an actionable diagnostic.

For a deployment supporting Talk API v4, the conversation API is rooted at `/ocs/v2.php/apps/spreed/api/v4`. Group conversations use room type 2. Participant additions target `/room/{token}/participants` with an identified participant and supported source. Capability discovery and the exact supported API version govern optional features. [Talk conversations](https://nextcloud-talk.readthedocs.io/en/latest/conversation/) · [Talk participants](https://nextcloud-talk.readthedocs.io/en/latest/participant/)

Provisioning is a separate authority. Existing accounts may be linked without granting the adapter global user-creation rights. If the institution authorizes account/group provisioning, use the supported Provisioning API and the required OCS request headers, and inspect both HTTP and OCS status. Limit the service account to the provider authority it needs. [Nextcloud provisioning](https://docs.nextcloud.com/server/stable/admin_manual/configuration_user/user_provisioning_api.html)

## Classroom room workflow

1. A teacher creates or activates an offering or section with collaboration enabled by policy.
2. The participation transaction records a CollaborationSpaceLink request containing the stable scope ID, permitted provider connection, room visibility policy and desired staff/learner membership revision.
3. The adapter claims a creation job with a stable request key. It checks existing mappings and provider state before creating a room.
4. It creates a group conversation under the approved owner account, records the remote token and creation receipt, and applies permitted staff moderator roles.
5. It resolves linked learner accounts and applies the approved member set. Unlinked accounts become per-member pending issues. They do not disappear silently from the result count.
6. It reads the provider membership state to confirm convergence and records the observed provider revision or digest.
7. The LMS displays the room link only to currently authorized members, together with a safe pending or degraded status where appropriate.

The room display name is descriptive. Its stable mapping uses the LMS scope and provider resource ID. Renaming a class does not create another room. An uncertain create response requires lookup or reconciliation before another create request. If the provider offers no reliable deduplication or metadata lookup, retain a manual reconciliation issue rather than multiplying rooms.

## Membership changes

Compute desired membership from current effective enrollment, section/group membership, teaching assignments and collaboration policy. A change event carries the source revision. The adapter ignores an older revision after it has applied a newer desired set. Staff-added provider participants are governed by an explicit authority rule. Either the LMS fully owns the room membership, or the integration distinguishes provider-managed participants that must be retained.

Do not interpret a transient empty roster read as an instruction to remove everyone. A full snapshot includes a successful source watermark and completeness marker. A partial feed contains explicit additions/removals. Apply removals only when their authority and effective time are established. Reconcile roles independently from membership so a learner cannot remain a moderator after a teaching assignment ends.

An enrollment suspension changes LMS access at its authoritative effective time. Remote revocation is retried and visible to authorized staff until confirmed. An institution that requires immediate provider revocation must define an outage policy, such as disabling the provider connection or restricting the room until membership converges. This policy does not erase prior authorized messages.

## Chat, conferencing and recordings

The course player links or embeds only provider surfaces supported by the approved browser/security profile. Authentication and third-party cookie behavior are tested on supported browsers. If an embedded surface cannot establish a safe session, open the authorized provider experience using its supported route.

Store LMS references to a conversation or recording with the relevant offering, activity and rights metadata. Provider chat content stays in its authorized provider unless an explicit archival workflow requests a permitted export. A recording used as course material becomes a versioned asset reference with captions, duration, ownership and access policy. A recording used as assessment evidence needs the same immutable capture rule as any other submission.

## Filery adapter contract

The existing Filery installation and its actual interface determine the transport and endpoint mapping. The portable adapter contract below is complete at the LMS boundary. The implementation must bind each operation to verified Filery behavior and pass the listed acceptance cases before enabling the integration.

| Operation | Input | Required output and behavior |
| --- | --- | --- |
| Discover capabilities | Connection and authorized service identity | Supported lookup, upload, version, share, revoke and immutable-read capabilities |
| Resolve document | Provider resource ID and requester context | Stable resource identity, current version, type, byte size and allowed actions |
| Request upload | Owner scope, filename, type, byte limit and request key | Authorized upload session with limits and expiry |
| Finalize upload | Upload identity, actual size and digest | Verified document version or explicit validation error |
| Grant access | Resource/version, permitted principal or group, rights and expiry | Provider grant identity and confirmed rights |
| Revoke access | Grant identity and effective reason | Confirmed revocation or retryable pending receipt |
| Fetch immutable version | Resource/version and evidence purpose | Authorized bytes with digest and stable version, or an unsupported-capability result |
| Capture submission | Selected document version and assessment context | LMS-owned immutable evidence reference and capture receipt |
| Reconcile | Desired grant/resource mapping and prior receipt | Applied, already-applied, divergent or unresolved state with exact items |

A missing immutable-read capability requires an authorized byte capture before accepting academic evidence. A read link can remain a live learning resource but must not be silently treated as a frozen submitted document. Preserve source resource/version identifiers in the evidence provenance so an authorized reviewer can explain where the captured work came from.

## Document and video transport

A browser must not receive a provider-wide service credential. Use a scope-bound short-lived access grant or the provider's supported user authorization. The LMS checks the requested asset or evidence context before issuing a grant. A file URL contains no grade key or unrelated learner identity. External URLs are validated against the approved origin and provider policy before server-side fetching.

For Nextcloud file operations, record the file identity and ETag/version behavior exposed by the installed WebDAV profile. An ETag identifies a representation for conditional access and is not by itself a guarantee that historical bytes will remain retrievable indefinitely. Capture the accepted version where long-term reproducibility requires it. [Nextcloud WebDAV](https://docs.nextcloud.com/server/stable/developer_manual/client_apis/WebDAV/basic.html)

## Adapter acceptance

| Case | Expected result |
| --- | --- |
| Provider times out after room creation | Retry resolves the existing room or opens a reconciliation item, with no duplicate room accepted |
| Learner lacks a linked provider identity | Enrollment remains active and the collaboration membership issue is visible |
| A section membership changes twice before sync | Final provider membership reflects the highest authorized source revision |
| Teacher manually adds a guest | The configured membership authority determines whether to retain, remove or review that participant |
| Remote revocation fails | Native access follows the authoritative LMS state and staff see pending provider revocation |
| A document changes after submission | Review and grading use the accepted immutable version or captured bytes |
| A file is too large or fails scanning | Submission remains incomplete with a precise recoverable error and no accepted evidence receipt |
| A provider credential is rotated | New operations use the new credential identity and in-flight retries remain reconcilable |
| A user attempts an unrelated file ID | The adapter denies the request before issuing any provider access grant |
| A room or document is deleted remotely | The LMS retains academic provenance and displays a repairable missing-resource state |
