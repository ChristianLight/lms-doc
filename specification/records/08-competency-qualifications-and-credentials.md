# 08 Competencies, qualifications and credentials

## Framework and alignment

A CompetencyFrameworkVersion includes a stable framework code, issuer, version, locale, source identifier, taxonomy metadata and bounded hierarchy. A Competency has stable identity inside that framework. A CompetencyVersion fixes text, parent relationships, evidence scale and prerequisite edges. Domain-specific proficiency codes can include emerging, developing, proficient and advanced. A framework declares both order and numeric mapping if it supports numeric arithmetic. Cyclic descriptive cross-references can be allowed while prerequisite and rollup edges must be acyclic.

A CompetencyAlignment pins exact framework version, competency version and evidence source. Example sources are rubric criterion, item, activity, released course result, prior-recognition decision and observed task. Type marks support demonstrates, supports or prerequisite. An alignment states what source data can be interpreted and what scale conversion applies. Alignments do not infer achievement simply because a teacher tagged content. Ingest only authorized evidence with proven source and learner relationship.

A CompetencyEvidence record stores Person, optional Enrollment, competency version, observed ordinal level, observation time, approved record time, source revision and acceptance state. Multiple assessors can supply evidence. The same source revision can count once for a competency in a calculation. Correction events supersede the earlier evidence without erasing it. Evidence can have expiry or allow only named contexts.

## Aggregation policy

The default competency policy is most recent eligible observation with a published mastery threshold. Sort by effective observation instant, accepted source sequence and stable evidence ID. Exclude expired or revoked evidence and data from unapproved sources. Keep no evidence distinct from lowest skill. A submitted but unreviewed demonstration never changes a learner's official mastery.

Optional policy modes include minimum N recent demonstrations, consecutive demonstrations above threshold, or required criterion minimum. Minimum-N tests independence by source family and accepted timestamp window. Criteria mode requires each named approved rubric criterion, then selects the minimum mapped level. Each policy sets permitted source types, lookback days, minimum and maximum sample count and precedence. When insufficient evidence exists, state is developing or insufficient according to approved minimum evidence semantics. Do not average ordinal codes without an explicit numeric scale conversion.

**Worked example.** A safety competency requires two independent demonstrations at level 3 or above within 180 days. Observation A is level 3 at day 10, B level 4 at day 30 and a retest B correction level 2 at day 31. A and corrected B are two distinct demonstrations but only one satisfies threshold. Status is developing. A new independent practical C at level 3 on day 40 gives two qualifying observations. At day 221, A and C are older than 180 days. The new review can show expired and retains the prior achieved decision.

Document boundary rule precisely in policy. For a lookback duration D, accept observations where observed_at is at most as_of and strictly greater than as_of minus D. Expiry starts when now reaches expiry_at. For a fixed programme expiry date use the organization's time zone and store the corresponding UTC boundary. Do not reinterpret date-only institutional settings on a worker's local clock.

## Qualification issuance

QualificationDecision pins an approved ProgrammeAuditResult, programme requirement version, Person, approver, decision timestamp, optional expiry and effective status. The default requires a satisfied audit, no unresolved formal hold and registrar approval. A programme adviser can recommend but cannot approve their own reviewed exception where separation of duties applies. Qualification approval and credential issuance are distinct operations. The institution may record the award before it generates a document or portable credential.

A CredentialDefinitionVersion declares issuer identity, achievement type, title, language, allowed claims, expiry policy, verification mode and optional signature profile. A Credential references the exact qualification or competency decision and definition version. Status events are issued, suspended, reinstated, revoked, expired and superseded, with explicit allowed transitions. Default revocation is terminal. If a credential was revoked in error, issue a replacement with its own stable ID. Expiry can be evaluated by an as-of query while an event records institutional confirmation and downstream notification.

For a signed credential, use an approved signature profile, pinned verification method, issuer-controlled key management, rotation and a status mechanism. Preserve the data needed to verify historical signatures until policy ends that retention. Do not include unnecessary identifiers or evidence files in a signed public payload. A verification response returns only authorized minimal data, public status, issuer and expiry when approved. Submit opaque verification proof in the declared Credential-Verification header to keep it out of query strings, redirects, referrer data and analytics. Institution controls whether verification is authenticated, opaque-link based, signed-exchange based or disabled. Avoid indexed public searching by learner name.

## Renewal and correction

1. A policy can open renewal before expiry. Default renewal is staff- or learner-initiated, no automatic enrollment. A configured scheduler creates one proposal per prior qualification and renewal window.
2. Renew using a new ProgramEnrollment or a versioned competency evaluation. A newer version of requirements must be assigned by approved policy. Keep the former award and identify it as the predecessor.
3. Reuse eligible evidence only if renewal policy permits and evidence still meets currency. New assessment attempts are distinct. The system never rolls forward an expired mastery state as current.
4. Approve a new award and issue a new Credential when requirements pass. A correction after issuance creates an impact review. Decide whether to leave unchanged, suspend, revoke or replace under institutional policy.
5. Propagate status to authorized external recipients using an idempotent outbox. External provider outage leaves local status authoritative. Record acknowledgment and support reconciliation.

**Worked example.** A qualification expires on 30 June and opens renewal 30 calendar days before expiry. The learner renews on 20 June under requirement version 3. The earlier award under version 2 remains valid according to issuer policy until its expiry or approved supersession. A duplicate 20 June issuance command returns the same new credential. It does not reactivate or extend the version 2 credential.

## Exchange profiles

- [Competencies and Academic Standards Exchange](https://www.1edtech.org/standards/case) exchanges academic standards and competency frameworks. Validate identifier and relationship mapping.
- [Open Badges](https://www.1edtech.org/standards/open-badges) represents individual achievements. Keep credential subject disclosure policy independent.
- [Comprehensive Learner Record](https://www.1edtech.org/standards/clr) bundles achievements. Export only the explicitly approved profile and recipient data.

Support one exact tested edition of each chosen profile. Publish mapped and unsupported fields. External import produces evidence subject to acceptance. It cannot grant a local award until authorized policy approves it.
