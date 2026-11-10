# 10 Reliability, recovery and release acceptance

## Deployment targets and load envelope

These are product planning baselines. Adopt stricter targets only when the measured deployment and operating model support them. A site must record its approved load envelope before enrollment. Availability and performance objectives never permit accepting an uncommitted academic mutation.

| Capability | Initial operating target | Measurement and overload behavior |
| --- | --- | --- |
| Protected lessons and navigation | p95 server response below 500 ms at declared load, excluding large media transfer | Measure origin latency and browser workflow. Serve authorized cached versions. Throttle optional analytics before core reads. |
| Save or submit exam response | p95 durable acknowledgement below 1 s, p99 below 3 s at declared peak | Track save, receipt and conflict rates. Reserve write and worker capacity. If durable acceptance is unavailable, return a retryable response. |
| Score processing | p95 evaluation starts under 30 s for queue-ready deterministic work | Track by class. Keep human marking separate. Pending evaluation cannot become zero or a failed result. |
| Roster sync and collaboration | p95 successful run lag below 15 min for normal updates | Track local desired version and confirmed remote version. Immediate local revocation, visible provider lag. |
| Recovery | Ordinary service RPO 5 min and RTO 4 h. Exam window profile requires no loss of acknowledged exam submissions within the declared failure domain. | Document replication and disaster coverage, test failover and report achieved objectives. If the exam durability target cannot be met, do not schedule high-stakes delivery until the institution approves a tested alternative. |

Reference capacity profiles for an initial benchmark are 200 active learners for a small site, 1,000 simultaneous examinees for an institutional peak, and 10,000 daily active learners for sustained operation. Choose actual concurrency with operator and school. For 1,000 examinees autosaving once every 30 seconds, average save demand is about 34 writes per second. If 400 candidates submit within 20 seconds, peak submission rate is 20 per second. Simulate synchronized timer boundaries and a 2x submission burst of 40 per second with concurrent saves, cache misses and a slow provider. Set test device and network profiles, data volume, read/write mix and job policies in the release record.

Use an indexed transactional core for official records. Start with bounded partitions only when measured cardinality or maintenance windows warrant them. Index institution and offered scope first for tenant queries, then time/status and stable pagination keys. Partition analytics independently. Rebuild projections from owner versions and show stale watermark where users can make decisions. Use backpressure, reserved queue slots and controlled export limits before dropping work. No institution should monopolize shared worker pool. Preserve configurable fair-share with ordered priority within each owner scope.

## Backups and recovery workflow

Use [NIST contingency planning](https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final) as planning guidance. A consistent snapshot covers database, exact object versions, audit anchors, event and receipt checkpoints, configuration, secrets recovery procedure and schema. To support point-in-time recovery, use verified base backup and continuous change log coverage. Protect recovery data and credentials with separate least-privilege custody.

1. Take continuous transaction log coverage and daily verified base or incremental backups. Create signed BackupSet manifest with environment, schema/application versions, data and object horizon, object digest inventory, audit anchor, event checkpoint, encryption key version and recovery test time. Default daily retention is 35 days, subject to approved schedule and holds.
2. On incident declare a recovery owner, incident time and target. Fence old writers, workers and provider dispatch through environment generation, credentials or network. Keep restored system isolated until verification. Preserve compromised backups and evidence according to incident policy.
3. Recover database and stored object versions to a compatible horizon. Validate manifest signature, log continuity and readable keys. Verify institution separation, canonical references, required binaries, and authored and published versions. Missing required bytes block impacted routes and trigger recovery review.
4. Replay accepted durable records, revocations and approved disposal ledger to applicable horizon. Compare official report digests and accepted submission receipts with independent verified evidence. No restored account, contact route, deleted content or queued provider operation may reactivate solely from an older snapshot.
5. Reconcile processing fences, event checkpoints, pending effects and provider acknowledgements. Block unknown remote effects pending evidence. Check stale scheduled tasks and invalidate all old sessions and tickets.
6. Measure actual recovery point and restoration duration. Run synthetic learner sign-in, permitted lesson load, reference exam save and submit, teacher result review, scoped retrieval, privacy and connector no-effect tests in the isolated environment.
7. Require independent readiness sign-off. Reopen core service first and re-enable provider side effects in phases. Retain recovery exercise record and publish a restricted incident report. If recovery falls outside target, record data affected and verified corrective pathway. Do not falsely reconstruct scores or submissions.

Worked example. Incident is 10:05:00 UTC. Verified data horizon is 10:03:30. Observed RPO is 90 seconds. If verified service reopens at 12:10:00, RTO is 2 hours 5 minutes. Ordinary 5-minute/4-hour objectives pass. A high-stakes zero acknowledged submission loss profile also requires independent verification that all accepted submissions after 10:03:30 are durable and were recovered. The numerical ordinary targets do not establish that fact.

## Observability and escalation

| Signal | Initial escalation threshold | Required safe detail |
| --- | --- | --- |
| Durable submit route | Three consecutive 1-minute periods with error rate above 1% or p95 above target during scheduled exams | Availability, receipt and conflict counts and affected service scope. No responses or student names. |
| Audit append | Any missed required commit or broken anchor | Institution stream, first affected sequence and correlation. Restrict underlying evidence. |
| Object scan | Oldest required pending scan above 5 min or any unsafe payload found | Class, safe finding and storage object reference under scoped access. |
| Worker backlog | Exam mark queue oldest above 30 s for 5 min | Registered class, age, total and repeated safe error codes. |
| Connector access drift | Pending removal older than 5 min for protected collaboration or failed reconciliation after agreed window | Desired and acknowledged versions, provider profile and reconciliation status. |
| Backups | No valid daily backup or continuous log break past RPO | Coverage horizon and recovery set reference. Preserve keys and restricted manifest. |
| Privacy case | Approaches 75% of due time or any unverified processor state blocks completion | Scope owner, due time and classified state. Keep protected evidence out of alerts. |

Trace across layers using correlation IDs, limited actor authority and version, job fence and event ID. Do not use raw personal values as metric labels or persist payloads in error trackers. Audit that an affected actor saw a protected academic record only if the policy and required trail justify collecting that fact. Document rollback and forward-recovery steps for deployments. Rehearse schema migrations and large backfills in a representative dataset with active exam and connector traffic.

## Acceptance gates

1. Execute the platform scenarios in the catalog, including invalid actor, actual known cross-institution ID, mutable locale with fixed deadline, replay after lost acknowledgement, and concurrent hold and disposal.
2. Run authorization cases against API, search, counts, export, attachments, scheduled jobs and external callbacks. Assert the denied outcome and the lack of unauthorized side effects. Verify revocation during live stream and while optional messages are queued.
3. Inject storage path traversal, archive bombs, duplicate paths, unsigned or replayed callback, unsafe remote destinations, stalled lease and schema version changes. Check quota, evidence, logs and safe customer-facing outcomes.
4. Complete the accessibility matrix with institution content and representative assistive tools. Test authoring, learning, timed assessment, typed math input and accessible report. Include allowed accommodations and degraded network.
5. Measure approved workload and restore targets using fixtures and realistic live-time failure injection. Verify receipt uniqueness, report reproducibility and operational reopening conditions. No service-level metric overrides institution policy or academic correctness.
6. Review institution retention and privacy policies, processor contracts, support escalation, verified backup, current source compatibility, scope dependencies and launch sign-off. A gap in one capability can be gated off only when the supported workflows remain coherent and the limitation is documented.
