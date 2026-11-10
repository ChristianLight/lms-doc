# 06 Secure storage, scanning and binary delivery

## Boundary and default limits

The owning domain creates and publishes AssetVersion, a submitted attachment or official export. The platform owns StorageObject reservation, scanner verdict, private delivery and provider reconciliation. A filename, hash or storage location never changes domain visibility. Keep provider media versions immutable from the LMS perspective or block publication when provider cannot guarantee pinned bytes.

| Purpose | Initial maximum | Expected behavior |
| --- | --- | --- |
| Native content document or image | 50 MiB per file | Allowlisted detected type, sanitized markup and images as appropriate, and malware scan. |
| Learner attachment | 25 MiB per file and 100 MiB per submission | Require current attempt or assignment upload permission. Preserve bytes by exact submission revision. |
| Official export and protected evidence | 250 MiB | Generate privately. Recheck collection authority and audit. Force safe download where possible. |
| Imported package | 500 MiB compressed, 2 GiB total extraction, 10,000 entries, no nested automatic extraction | Package adapter can further tighten. Reject traversal, symlinks, unsupported paths or expansion beyond configured budget. |
| Managed media | 2 GiB per approved object | Pinned provider version, approved content type and access route, independent streaming bandwidth policy. |

Above limits are default product profiles. A higher institution policy must include storage quota, scan and import capacity review. Enforce absolute configured caps at ingress and during stream or extraction. Check expected and observed bytes separately. Quarantine reservations expire after 24 hours, per-upload credentials after 15 minutes, and rejected object storage after seven days unless held.

## Upload and publish

1. Resolve resource owner, version, permission, remaining quota and media policy. An upload reservation allocates bounded bytes and an opaque key under private quarantine. The client sends the declared size and media type. Treat both as claims.
2. Supply scoped one-object upload capability with expiration. Use streaming limits at the upload gateway or provider policy. A single-object token permits upload only and cannot enumerate or read the bucket.
3. Finalize by validating the backend version and measured digest, byte count, current ownership and reservation. A wrong version or digest prevents publication. Expired or canceled reservations are quarantined until cleanup.
4. A fenced worker scans the exact digest and records engine, ruleset and policy version. Reject type mismatch, malformed archive, active unsafe markup and malware. Timeout or scanner outage stays quarantined and retries with approved budget. An old verdict never applies to a changed object.
5. Owner links the exact clean object version to its resource through its publication or submission workflow. Clean binary availability alone does not authorize reading. If the owning resource changed while scanning, revalidate eligibility and attach through the new owner decision.
6. Revocation prevents new retrieval immediately at the authorized gateway. Mark affected linked activities degraded and queue review. Preserve evidence and retention duties.

Archive paths are normalized before writes. Reject absolute names, dot segments, invalid encoding, symbolic links, repeated normalized paths, drive prefixes, control characters, cross-platform ambiguous names and prohibited archive nesting. Validate checksums and upper bounds during decompression. Disable XML DTD and external entity resolution. Authoring content goes through a context-aware sanitizer. Imported executable packages run in a dedicated untrusted runtime with explicit capability bridge. Do not apply native markup rules to a package by simply serving its original scripts in the application origin. See [OWASP file upload guidance](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html).

## Retrieval

Authorize at issue and redemption. Default ticket expires after five minutes and earlier at principal, grant or resource authorization boundary. Bind ticket to Principal, Institution, object ID and version, purpose and current authorization epochs. Deliver raw token through a protected response and accept it in the dedicated `X-LMS-Access-Ticket` header for API calls. The authenticated Principal is independently resolved from the bearer or trusted host session. An access ticket alone cannot establish identity. If a browser-native media player requires URL credentials, use a gateway route with short-lived scoped handle, referrer suppression and redacted logs. Require authenticated principal proof at retrieval. The catalog authorization endpoint requires the ticket header and accepts the standard `Range` header. It returns a short-lived body reference for the trusted gateway after access evaluation. The public ticket route streams the associated bytes after repeating the current authorization check, rather than disclosing the internal body reference. It responds with 200 for a complete object, 206 for a permitted range, 416 for an invalid range, or the corresponding scoped error.

Use a gateway with current domain checks for submissions, assessment answer assets, exports and evidence. Once bytes were delivered, revocation cannot retract a prior local copy. For streaming, reauthorize new range requests and periodically stop active streams under revocation policy. HTTP range requests default to one normalized range, maximum 8 MiB per segment, safe 416 response for an invalid range and no cross-object inference. Set verified media type, no-sniff, attachment disposition for unsafe rendering contexts, and no-store for private responses. A direct provider signed URL is acceptable only for explicitly approved lower-risk material where residual access until expiry is accepted and documented.

Map file purpose to response states. Learners see uploading, saved in quarantine, scan pending, rejected with safe reason, and ready. Teachers see dependency changes without the protected learner payload. A keyboard-operable retry resumes the authorized upload or starts a new reservation. A lost finalization acknowledgement returns the existing receipt without changing owner history.
