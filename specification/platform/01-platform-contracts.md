# 01 Platform contracts and ownership

The platform subsystem owns institution boundaries, identities and actor authorization, shared safety and operations records, and controlled infrastructure. Its tables serve domains through contracts. Only the owner of an academic record may apply a state transition to it.

| Concern | Authoritative owner | Platform contribution | Prohibited shortcut |
| --- | --- | --- | --- |
| Academic identity | Platform for Person | Stable institutional identity and protected contacts | Do not identify a learner by login name, email, or one external identifier |
| Authentication | Institutional host or configured provider for credential verification | Principal, validated assertion, subject binding, current authorization epochs | Do not create a local password merely because a roster references a person |
| Curriculum | Curriculum for courses, assets and versions | Scope resolution, stored binary transport, scan and retrieval custody | Storage keys do not publish or replace a content revision |
| Enrollment and progress | Participation for offerings, enrollments and progress | Person and academic period reference, access checks, routed integration | Connector cannot write a membership row directly |
| Attempts and marks | Assessment and grading owners | Acceptance reliability, fenced computation and audit context | Queue operators cannot adjust score or reset an exam |
| External providers | Provider for its service data | Authority rules, desired state, evidence and idempotent sync | Room membership or messages cannot become academic enrollment or grading authority |
| Official academic records | Grading and records domain | Restriction, protected audit, retention coordination and recovery evidence | Technical administrator or hosted identity administrator gets no automatic grade access |

## Durable record conventions

1. Every entity in [the platform catalog](catalog.json) uses an opaque UUID. Treat it as an identifier. An institution root is its own scope ID. Record keys and scoped uniqueness always include institution where required by the invariant.
2. Record times use UTC timestamps with offsets accepted at input and normalized to UTC at storage. Record precision is at least milliseconds. Comparisons use stored database precision. Date-only schedules use the recorded calendar zone and a half-open interval. Never compare time using display strings.
3. Logical requiredness in the catalog describes persisted records. Request schemas separately describe input. The server supplies IDs, clocks, epochs, counts and versions. Optional payload keys have only the semantics a command declares. An absent key in a partial update means leave unchanged. Explicit null must be admitted by the schema and approved by policy.
4. Active and historical representations are distinct. Existing grade, schedule and material references remain pinned to original revisions. Close, deactivate, revoke and archive are lifecycle operations. Deletion belongs to an approved retention workflow.
5. Cross-domain references are validated against canonical records in the same institution and relevant scope. Where an owner lives in another service, verify the exact version with a trusted owner contract. Do not accept scope or authorization claims from untrusted caller data. Store trusted scope projections with version and review them on changes.
6. Transactional ownership can initially share one data store. Mutation, audit or durable event and idempotency outcome commit together. Across independent stores, coordinate through intent and evidence states, owner commands, and an outbox. A retry completes an incomplete operation without reporting an unverified result.
7. Treat secrets, identity evidence, clinical or safeguarding information, answer keys, submitted work, and unpublished grades as separate data classes even when stored together. Restrict access at the field and record level.
8. Institution and scope are server-derived for cache, search, export and pagination. Use explicit maximum query sizes, query allowlists, and stable keyset pagination. Counts use the same authorized predicate as rows.

## HTTP contract

The versioned reference in the catalog uses HTTP. Native host operations can expose equivalent input, preconditions and outcomes. APIs return errors as [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) and use [HTTP conditional requests](https://www.rfc-editor.org/rfc/rfc9110.html#name-preconditions) for versioned changes.

| Detail | Default | Enforcement |
| --- | --- | --- |
| Version | Strong ETag `"v<version>"` for versioned representations | Require If-Match for edits and declared transition actions. Never use If-Match `*` to bypass review. |
| Idempotency | Required for replayable side effects. Client key has 16–128 URL-safe characters. | Scope by institution, authenticated Principal, operation and canonical target. Compute SHA-256 over normalized request and preconditions. Return original outcome on identical retry only if current actor still has response visibility. |
| Validation | Closed request objects and bounded lists. | Reject duplicates for fields that require uniqueness. Normalize declared identifiers before checking collisions. Reject oversized input before expensive work. |
| List queries | Default 25, maximum 100. | Sign cursor containing typed sort key, filter digest, authorization epoch, institution, Principal and expiry. Default cursor lifetime 15 minutes. Use `(stable_sort_key, id)` as keyset. |
| Audit trace | Correlation ID accepted only in validated trace context or generated server-side. | Return correlation ID as a response header. Retain original correlation for committed retries, with optional new per-request trace. |
| Authorization failure | Return 404 for cross-institution or forbidden enumeration. | Return 403 when the requester is already authorized to know the resource exists and an operation is disallowed. Return 401 for failed authentication without resolving target. |
| Stale or missing version | 412 for mismatch and 428 for absence when required. | A worker action that carries its own fence can use fence and target version as the precondition instead of a user ETag. |

Example of a stale role change after revocation.

```http
POST /v1/platform/institutions/00000000-0000-4000-8000-000000000001/role-assignments/00000000-0000-4000-8000-000000000119/approve
Content-Type: application/json
If-Match: "v3"
Idempotency-Key: qQk7VMmAMiA4YQqGXyW5

{"reason":"Reviewed assistant assignment for one section"}
```

```http
HTTP/1.1 412 Precondition Failed
Content-Type: application/problem+json
X-Correlation-Id: 00000000-0000-4000-8000-000000000220

{
  "type": "urn:lms:problem:version-mismatch",
  "title": "Resource changed",
  "status": 412,
  "code": "VERSION_MISMATCH",
  "detail": "Review the current assignment before retrying."
}
```

Protect user sessions from cross-site requests and unsafe credential persistence. Give untrusted package and file origins no same-origin access to the application. Apply cookie flags, application security controls, and logs according to [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).
