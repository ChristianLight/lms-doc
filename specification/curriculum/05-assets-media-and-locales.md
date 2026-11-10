# 05. Assets, media and localization

## Asset ingestion and use

An Asset is the durable logical resource. Each immutable AssetVersion records institution, Asset ID, revision, byte digest, byte count, detected media type, typed storage or provider reference, safe display filename, original filename for provenance, rights policy, state, creator and scan decision. Content references pin a specific AssetVersion. Managed bytes reference an exact Platform-owned StorageObject and StorageScanResult. Externally hosted media references an exact Platform-owned ExternalResourceMap under an authorized IntegrationConnection. The platform owns byte reservation, measured digests, scans, retrieval and credential use. The curriculum owner applies the verified result to publication eligibility. A provider that cannot guarantee a pinned version cannot supply a required immutable asset. Two versions may share bytes in internal deduplicated storage while keeping independent rights, access decisions and metadata. Digest lookup is internal and authorization precedes existence disclosure.

| Phase | State | Validation and commit |
| --- | --- | --- |
| Initiate | awaiting_upload | Reserve bounded bytes, type expectation, institution and one-use upload intent. Enforce the platform purpose cap. Default 50 MiB for documents and images or 2 GiB for managed media |
| Receive | quarantined | Store under a randomized object key. Compute digest and bytes independently of client. Verify size and declared purpose |
| Scan | scanning | Run malware detection, type sniffing, bounded archive and structural safety checks appropriate to type. Timeout leaves quarantined |
| Accept | approved | Persist verified metadata and safe derivatives. An approved version may be referenced by drafts and publications subject to rights |
| Reject or withdraw | rejected or withdrawn | Record machine reason and human detail. Reject access immediately and retain protected evidence under the applicable retention policy |

Serve documents from approved storage using authenticated requests or short-lived signed access. The signed claim binds institution, principal or authorized session, offering and placement where relevant, asset version, rendition, purpose and expiry. Default lifetime 5 minutes, renewable through a fresh authorization check. Active revocation or highly sensitive content requires a check on each download or ranged request. Use safe content type, content disposition and no MIME sniffing. Preview formats use a sanitized derivative or isolated origin. Thumbnails, extracted text and captions inherit equivalent visibility.

Referenced approved versions survive content edit and asset replacement. Removing an asset blocks deletion while any active or retained publication, submission or export requires it. The object collector checks reference count and durable hold under a lock or compare-and-swap, marks a tombstone, then deletes bytes asynchronously. Unexpected missing storage is a service failure, not an empty document or a reason to reassign version identity.

## Hosted version verification

A hosted candidate reserves its AssetVersion before resolving remote data. The intended provider key is untrusted. Ask the platform to resolve it under a registered same-institution connection. The platform creates an ExternalResourceMap with local type AssetVersion and its exact ID, provider version, verification and approved retrieval state. An asset owner uses the returned verified mapping and expected provider version to approve publication eligibility. Reject a provider alias that changes independently of the pinned version. If the provider does not support immutable revisions, use a licensed managed copy or another approved resource. Keep the pending version and related job visible to authors. A retry cannot create a second visible version.

## Video and audio

Media metadata records playback provider, registered remote reference or asset version, approved duration, player capabilities, captions with locale and kind, transcript and audio description links, poster and alternative resource. For remote playback, token issuance stays on the server and checks audience before redirect. Client iframes load from the integration allowlist. If authorized media fails, report unavailable with a transcript or alternative pathway when configured. An unavailable required video remains pending unless an accepted equivalent completion signal arrives.

Use [WebVTT](https://www.w3.org/TR/webvtt1/) for timed text where supported. Validate nonnegative timestamps, end after start and bounds against declared duration. Allow overlapping cues where the track format and purpose permit. Captions describe dialogue and relevant sounds. Transcripts remain navigable as text. Audio description is reviewed when key visuals convey necessary material. Learners can select speed, captions and audio tracks with a keyboard and screen reader. Default no autoplay.

The participation service calculates watch coverage from accepted intervals. It stores media position for resumption separately. The player's renderer sends source, session, start, end and sequence. It cannot award learning completion directly.

## Locale selection and translation review

Accept valid BCP 47 language tags and normalize canonical case and preferred subtags. Store explicit locale and content version with each translation variant. Course settings declare default locale and required publication locales. Display fallback records remain audit-visible.

1. Consider a permitted learner locale preference, then offered locale priorities, then course default.
2. For each request, find exact locale then use [RFC 4647](https://www.rfc-editor.org/rfc/rfc4647) lookup within eligible variants.
3. If the locale policy allows fallback and lookup fails, use the default locale variant. Label that display language. Use the proper HTML language and direction attributes.
4. A required assessment translation or mandated curriculum locale must have an approved variant before publication or release to that audience. An assessment attempt stores the delivered variant as part of its frozen context.
5. Captions, transcripts, text alternatives and activity instructions follow separate declared availability. A translated page does not imply translated supporting material.

A translator submits a variant against its exact source revision. The system distinguishes machine suggestion, in review, approved, stale and rejected. A source edit marks related variants stale based on changed block IDs and affected translatable fields. Prior approved course versions continue to resolve their pinned variant. The new draft review shows the changed source side by side and requires validation of placeholders, links, caption tracks, math labels and right-to-left controls.

## Failure fixtures

| Input | Outcome |
| --- | --- |
| A file extension says PNG and the received file contains active HTML | Quarantine and report declared/detected mismatch, without rendering active content |
| A signed video URL for learner A is used after that session loses access | Short-lived access expires and refresh fails. Protected playback revokes ongoing segmented access where configured |
| Published lesson requests French Canadian with approved French and English variants | RFC lookup uses French and displays it as the actual locale |
| Spanish is required for a graded activity but only instructions are approved | Publication or targeted release is blocked until the complete required variant is approved |
| A transcript is selected as the equivalent activity | The learner can acknowledge the transcript and satisfy the same configured criterion via an accepted completion signal |
