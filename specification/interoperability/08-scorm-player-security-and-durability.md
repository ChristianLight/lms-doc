# 08. Secure SCORM launch, sessions and durable saves

## 8.1 Trust zones

Use a dedicated package content domain under a different registrable domain from the LMS, so package code receives no application cookies, parent DOM, service-worker scope or authenticated API client. Allocate a distinct isolated origin or equivalently strong trust boundary for different package versions and incompatible learner or institution sessions. Relative package files and the immediate launcher API remain same-origin within this restricted context. Do not place SCO code directly into the LMS document.

The privileged LMS frame opens a restricted launcher. The launcher exposes only the edition API to a same-origin SCO child or popup. The LMS frame and launcher negotiate a scoped MessagePort after validating both exact origin and window source. Treat the entire package and launcher origin as untrusted even when launcher code is first-party. Same-origin package code can inspect and alter that window. Keep privileged state, credentials and native API calls in the LMS origin or a server authority. The content grant permits only the exact package attempt and occurrence. Once transferred, every message carries launch session ID, epoch, occurrence, protocol version, nonce and monotonically increasing sequence. The server independently checks enrollment and release, authoritative launch lease, grant generation and schema. A message from the SCO context never receives arbitrary DOM access, tool tokens or a cross-domain credential.

Apply Content Security Policy with default-deny network and an explicit approved list of required origins. The content origin can serve only verified archive bytes and bounded launch/runtime actions. Set no app cookies. Use a registered isolated content origin even when package compatibility requires `allow-same-origin` and `allow-scripts` together for the SCO. Add popups only in a separate compatibility profile with opener and top-navigation boundaries tested. Block service workers, unrestricted external navigation, arbitrary storage-sharing, remote script origins, unsolicited device access and privileged clipboard where the browser profile allows. Review specific third-party network requests. An opaque origin alone can break same-origin API discovery, so test isolation and discovery together.

## 8.2 Launch and grants

1. Authenticate the learner via the host and authorize enrollment, ActivityVersion, PackageVersion and placement under the effective EnrollmentRelease. Validate any current examination or prerequisite policy. Package grants carry only the approved minimum identity fields.
2. Select an organization, entry activity and registration according to attempt and sequencing policy. Lock the registration. Resume an eligible active attempt or create exactly one new attempt through a compare-and-swap. Repeated requests with the same key return the same registration.
3. Issue a signed opaque one-time bootstrap credential with a 60-second expiry, audience and claims for Institution, registration, attempt, occurrence, content origin and fencing epoch. Give it to the approved launcher through the authenticated envelope. Never place an LMS cookie or long-lived token in a package URL. Redact bootstrap data from referrers, browser storage, analytics and server logs.
4. Exchange bootstrap credential once for a bounded runtime session grant. Scope write authority to the registration, occurrence and epoch. A stolen grant can attempt operations only for its own active occurrence, activity attempt and lifetime. Apply rate limit and request size controls. A lost redemption response never returns the old token or consumes an additional learner attempt. The authorized host reissues a new writer session and epoch for the same eligible attempt after comparing durable state. The expired content grant cannot use the host recovery route.
5. Load the server snapshot and provide the local runtime adapter before navigating the child to the resource. Link the SCO identity to the authoritative manifest occurrence and its selected PackageActivityAttempt. Resume opens that attempt's state and a new attempt gets its own state record. If preloading fails, keep the asset unlaunched and show a recoverable error.
6. Keep a single writer lease per PackageRegistration by default. Another browser tab can resume after explicit takeover or expiry. Allocate the next epoch for every new writer session and invalidate stale session grants. Read-only inspection of registration state is separate.
7. Check active release, registration state and lease on every durable command. Revoking enrollment or package availability rejects further learner access immediately and does not destroy evidence already accepted.

Capture launch session creation, expiry, takeover, child-ready, lost connection and termination. Ordinary logs contain IDs, origin and error categories. Do not expose responses, suspend data, tokens or answer keys. Distribute sensitive actor data only via the edition-defined fields and institutional privacy profile.

## 8.3 Protocol envelope

The HTTP runtime endpoint operates on one occurrence and one launch session. The local JavaScript facade implements its edition's method names, synchronous return strings and error state. Its browser-to-server protocol carries buffered typed mutations and does not expose SCORM API names as native application authority.

```json
{
  "protocol": 1,
  "registration_id": "019571a4-f8af-7ab1-8b7a-337194762001",
  "launch_session_id": "019571a4-f8af-7ab1-8b7a-337194762002",
  "occurrence_id": "019571a4-f8af-7ab1-8b7a-337194762003",
  "epoch": 4,
  "base_state_revision": 7,
  "first_sequence": 19,
  "mutations": [
    {"sequence": 19, "element": "cmi.location", "value": "review-2"},
    {"sequence": 20, "element": "cmi.completion_status", "value": "completed"},
    {"sequence": 21, "element": "cmi.score.scaled", "value": "0.85"}
  ],
  "finalize": false
}
```

The request carries an idempotency key outside its body and server-issued runtime authorization. Validate exact increasing contiguous sequence numbers, model revision, canonical element syntax, byte quotas, write access and edition-specific types. Require no more than 256 mutations and 256 KiB per normal batch. A separately tested profile can allow higher safe bounds for valid interactions or large suspend data. The same session must preserve every accepted value when recovery spans multiple batches.

```json
{
  "registration_id": "019571a4-f8af-7ab1-8b7a-337194762001",
  "state_revision": 8,
  "accepted_through_sequence": 21,
  "commit_id": "019571a4-f8af-7ab1-8b7a-337194762004",
  "session_status": "active",
  "outcome_status": "pending_policy_projection"
}
```

One transaction locks registration, launch session, and SCO attempt state in that order. It checks epoch and base revision, validates each mutation under edition rules, records each accepted sequence and digest, creates the commit receipt, updates the current snapshot and accepted sequence, and writes evidence to the outbox. Session navigation state and cross-attempt shared stores use their own validated scopes. Return success after transaction commit. If one mutation fails, the whole batch fails. The server returns a sanitized detail with the rejected sequence and element, not the learner value. Exceeding quotas returns retry guidance only when the payload can safely split. Termination requires final mutations and lifecycle close to be accepted together.

## 8.4 Synchronous API and server durability

`SetValue` validates immediately and updates the session cache. `GetValue` reads the same current cache, including buffered writes that have not yet reached a durable receipt. Both return edition-defined strings. The facade eagerly sends pending batches in the foreground and maintains a durable acknowledged prefix. This does not create fictitious success for a later commit. The normative conformance profile declares which connection and browser behavior meets its persistence requirements.

The strict remote profile returns successful Commit only if the server has acknowledged the exact prefix or a separately verified transport obtains that receipt before the synchronous call returns. An empty prefix still checks API lifecycle and prior failure state. Browser message passing and asynchronous fetch cannot provide this acknowledgment during the same JavaScript call. The WHATWG XMLHttpRequest contract does not permit a nonzero timeout on synchronous Window XHR. Do not adopt Window XHR or block the browser main thread as a portability strategy. Use the confirmed-prefix transport as the browser baseline and verify common immediate Set and Commit sequences before claiming a strict package profile. A package requiring an immediate durable reply without a supported transport is outside this browser profile. It receives the edition failure and an accessible host recovery path. A queued request, sendBeacon Boolean or local journal is never a server receipt.

Finish and Terminate require the exact finalization receipt in addition to an acknowledged mutation prefix. Capture the terminal request and prevent new unconfirmed writes from being merged over a pending close. A 1.2 Finish failure ends the SCO-facing instance, with host reconciliation available. A fourth-edition 2004 Terminate that fails implicit persistence returns 391 and leaves the SCO-facing instance running. If the first request later proves durably closed, a valid terminal retry can return its original receipt and transition the local instance without creating a second closure. Ordinary requests that would mutate a pending or closed backend attempt receive the relevant edition failure.

A compatibility profile may stage recoverable data into browser storage and retry the network while the authorized launcher remains open. It must disclose the persistence difference and does not call a locally queued write a server-confirmed commit. A same-task Set and Finish on a stock browser cannot synchronously confirm a new network operation through this async bridge. This remains an explicit playback feasibility gate, even if host recovery works after the fact. Local storage reachable to package code is recovery data, with the same validations applied before server acceptance. Browser or session loss can clear it. Closing the window is not proof of successful save, completion or termination.

## 8.5 Retry, recovery and state

| Condition | Authoritative outcome |
| --- | --- |
| Identical key and bytes after an acknowledgment is lost | Return original receipt and state revision. No duplicated evidence or time |
| Same idempotency key with changed payload | Reject `IDEMPOTENCY_CONFLICT` and audit key reuse |
| Payload prefix already accepted under a different key | Return authoritative accepted sequence after checking matching stored mutation digests. Changed bytes at same sequence are conflict |
| Gap or stale base revision with current epoch | Reject and return authorized snapshot metadata and last sequence. Rebase only unsent changes after comparing cache and exact accepted prefix |
| Prior tab submits after takeover | Reject `LAUNCH_EPOCH_STALE`. Do not merge its cache automatically |
| Browser closes before committing | Keep durable prefix only. Mark session interrupted at expiry and expose recovery notice if partial unsaved state is known |
| Package writes terminal status in an intermediate commit | Record raw progress evidence. Native grade release still obeys activity and gradebook policy |
| Successfully closed session repeats Terminate or Finish | API state machine returns edition result. Server never duplicates the finalized session receipt or time |
| Enrollment revoked or version withdrawn | Revoke grant and reject further commits while preserving evidence, review and formal results under policy |

Represent 1.2 and fixed-unit 2004 durations as exact integer milliseconds plus the original wire value. For a legal 2004 duration with years or calendar months, retain calendar components separately from exact fixed elapsed units. Sum components and fixed units losslessly for the edition wire total. Report a native fixed-duration projection only when its conversion is exact or under an explicitly approved calendar-aware projection. A session reports a duration for the active session. Store the latest valid declared duration until session closes, then add exactly once to the registration total. Replayed commits and replacement duration values do not accumulate. The finish receipt is the authority for total time. If a timeout closes an interrupted session, record which reported duration was credited and policy version. Do not replace SCO-declared duration with page-open time silently.

For example, accepted sequence 18 and state revision 7 precede sequence 19 through 21. The server commits revision 8 and sends a receipt lost by a network retry. Repeating the same key returns revision 8 and time remains 0 while the session is active. A subsequent close stores session time 126,000 milliseconds and updates total once. A stale old-tab write at epoch 3 fails. Native grade evidence is projected from the accepted runtime state using the immutable policy mapping, and an asynchronous projection crash retries from the outbox.

## 8.6 User interface and conformance tests

The learner launch screen shows package name, resume or start action, load and failure state, durable save state, accessible host-owned exit control and privacy notice for approved external origins. The host status distinguishes saved, saving, retry needed, read-only conflict, and unknown unsaved changes. Screen readers receive concise updates. Exit offers retry and reports what is durable. An examination with required completion never relies on a transient progress message.

The operator inspector shows package edition, policy, launcher and browser version, exact manifest occurrence, latest server revision, accepted prefix, last API error category, storage mode and runtime flags. High-risk operations such as granting a remote origin and replacing a locked package require separate authority and audit. No operator uses the learner preview endpoint to update authoritative outcomes.

Test origin confusion, wrong window, forged nonce, stale grant, cross-institution lookup, resource traversal, attempted parent access, unauthorized cross-origin fetch, slow network, replay, partial-batch rejection, power loss after persistence before response, concurrent tab takeover, state resumption, disabled browser storage, missed unload, and loss of connection during Terminate. Verify synchronous behavior and score projection using edition-specific reference tests before documenting conformance.

- [WHATWG XMLHttpRequest specification](https://xhr.spec.whatwg.org/#the-open()-method)
- [ADL 2004 fourth-edition testing requirements](https://adlnet.gov/assets/uploads/SCORM_2004_4ED_v1_1_TR_20090814.pdf)
- [ADL SCORM 1.2 run-time environment](https://xml.coverpages.org/SCORM-12-RunTimeEnv.pdf)
