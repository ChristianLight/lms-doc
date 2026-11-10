# 03 Authentication and account binding

## Host contract

The host or configured identity provider verifies credentials, applies institutional authentication strength, rotates its sessions and reports current account status. The LMS receives a trusted, validated authenticated context containing issuer, subject, authentication time, audience or client binding, session identity when available, authentication assurance where configured, and token or assertion expiry. Never allow browser-supplied identity claims to act as that context. Privileged operators, privacy reviewers and release authorities default to multi-factor authentication. Provide a phishing-resistant method for privileged roles where supported, and require it under the institution's high-assurance profile. See [NIST SP 800-63B-4](https://csrc.nist.gov/pubs/sp/800/63/b/4/final).

Each institution publishes an immutable InstitutionPolicyVersion that pins approved session bounds and privileged authentication. Select the current effective version when authenticating and applying sensitive policy. An immediate change to privileged policy increments authorization epoch in the approval transaction. A future effective revision is selected at its approved instant. Bound caches by that activation and compare the currently effective revision even if an invalidation worker is delayed. Privileged sessions then requalify or terminate. A ServicePrincipalProfileVersion separately pins non-interactive command and worker mandate, scope, credential reference, owner and end time.

For OpenID Connect, configure issuer discovery, expected client, redirect and signature algorithms. Verify signature, issuer, audience, any authorized party requirement, expiration, nonce and provider rules using [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html). Authorization code flows use a random state and sender-bound verifier where supported. Fail closed when key validation, account status or issuer discovery cannot be established. Do not fetch arbitrary issuer URLs from untrusted tokens.

Two issuers can both return subject `user-42`. Store the exact trusted issuer with the subject. Pairwise subjects may differ between two registrations at the same issuer. Include the configured connection context in uniqueness and never merge by email. Compute the subject HMAC over length-delimited canonical fields using an institution-controlled key. Preserve opaque encrypted subject only where needed for provider reconciliation and fingerprint rotation. Do not case-fold or trim provider subject values.

## Login and session access

1. Verify the provider assertion or obtain equivalent trusted host context. Confirm provider connection is enabled and its configuration is current.
2. Resolve verified ExternalIdentity in the institution and identify the mapped active Principal. Reject unlinked and suspended principals. A human principal requires an active Person for normal interactive access.
3. Bind a short-lived session to institution, Principal, current Principal and Institution authorization epochs, authentication time and assurance. Default 30 minutes idle and 12 hours absolute for interactive academic sessions. The institutional profile may tighten or deliberately extend the learner session to cover exam timing. Recheck active exam state and server timing on reconnect.
4. Each protected request checks current epochs and current temporal grants. If a session carries old permission data, discard it and refresh context. Revoked or disallowed sessions require reauthentication. A cached role decision never outlives the earliest expiry or mandatory policy refresh.
5. Require recent authentication for identity links, contacts, emergency approval, sensitive exports and administrative credential changes. Default recent window 10 minutes. A user may complete a permitted step-up without losing an assessment draft. Session and epoch checks still govern the action.
6. Session cookies are Secure and HttpOnly with appropriate SameSite policy. Apply anti-CSRF protection to browser-authenticated writes and avoid access tokens in URLs or logs. A provider callback with a validated state follows the adapter-specific permitted flow.

## Verified external account link

1. The user opens the own-account page under recent verified session and chooses an approved provider. The server creates a VerificationChallenge scoped to Principal, provider, client, target version and initiating session. Default expiry is 15 minutes. Avoid open redirects by looking up a named return route.
2. On callback, validate provider response and browser/session binding. Resolve exact issuer and subject from verified context, then present masked account identity for confirmation where permitted.
3. Consume the one-use proof and insert the verified mapping under a uniqueness constraint. Lock Principal so a concurrent unlink or suspension invalidates a stale proof.
4. A valid subject already mapped to another actor returns `SUBJECT_ALREADY_BOUND`. Evidence goes to authorized review without identifying the other user to the requesting party. Concurrency can produce one winner only.
5. Unlink requires current mapping version, recent verified authentication and another allowed recovery route, unless already suspended by authorized security. Bump Principal epoch, revoke sessions, and retain a tombstone according to identity retention.
6. A provider outage denies new unverified authentication. An existing authorized session may continue according to its local validity and approved institutional failover policy. Never turn provider failure into a bypass.

## Verification and contact changes

Verify one contact without changing Principal identity, account recovery policy or role. Issue a short-lived challenge to the selected verified route or use approved institution evidence for physical mail. Store a keyed proof digest, limit attempts to five, consume it atomically and expire it using server time. Use a generic initiation response to prevent identity or address enumeration. A revoked destination cancels pending verification and disallows future optional delivery. Store email domain in normalized form and preserve local-part semantics. Do not assume mail provider aliasing rules. Shared family contact is valid for independently verified people.

## Operator and account screens

| Screen | Behavior |
| --- | --- |
| Sign-in and recovery | Show provider name, accessibility-compliant instructions and generic failed authentication feedback. Preserve an accessible route for approved account recovery. |
| Active account links | Show provider, verified time and masked identity. Show clear effect of unlink. Deny removing the last recoverable route unless authorized policy suspends the account. |
| Identity reconciliation | Show separately authorized evidence of issuer, mapping history, duplicate reason and current Person. Keep raw subject outside unprivileged directory. |
| Service Principal administration | Show granted profile, accountable owner and last successful use. Require approval before changing scope. Revoke and rotate credentials through secret custody. |
