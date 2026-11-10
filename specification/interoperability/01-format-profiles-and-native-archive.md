# 01. Format profiles and native curriculum archive

## 1.1 Independent capabilities

A system declares each direction and version it implements. A declaration includes exact edition, active capability keys, required integration dependencies, reference fixtures, and unsupported behavior. Keep the supported matrix in configuration and expose it to transfer operators before they upload. Archive detection reports its evidence independently of policy that allows a format.

| Profile identifier | Ingress | Egress | Result |
| --- | --- | --- | --- |
| `lms.curriculum/1` | Required | Required | Editable curriculum graph with explicit version and identity scope |
| `olx.course/1` | First-party migration adapter | Deferred | Editable drafts and separately registered packages |
| `olx.library.legacy/1` | First-party migration adapter | Deferred | Editable Library, entries and versioned definitions |
| `olx.library.archive/1` | First-party migration adapter | Deferred | Editable Library and separate published/draft snapshots |
| `scorm/1.2` | Validation and playback | Profiled generator | A PackageVersion and assigned registration |
| `scorm/2004.2`, `scorm/2004.3`, `scorm/2004.4` | Edition-specific validation and playback | Profiled generator | A PackageVersion with explicit CAM, RTE and sequencing scope |
| `qti/2.1`, `qti/3.0.1` | Optional version profiles | Optional version profiles | Editable item and assessment subset with fidelity report |
| `common-cartridge/1.3` | Optional | Optional | Outline, content resources and scoped references |
| `lti/1.3` | Tool callback and services | Launch and services | Access to registered external ActivityVersion |
| `oneroster/1.2` | Configured source authority | Configured destination policy | Roster, resource or gradebook exchange |
| `xapi/2.0`, `cmi5/quartz` | Optional record and launch bridges | Optional statement delivery | Scoped activity evidence in an LRS |

Do not enable a legacy profile by recognizing a similar namespace. A manifest can parse as XML while violating a profile's schema or runtime contract. Store the detected signature and the verification result separately. Policy records a compatibility disposition of `strict`, `review_only`, or `unsupported`. Only strict and explicitly approved review-only imports can reach editable private staging. Playback always requires an approved package runtime profile.

The interoperability catalog defines the internal control-plane commands and normalized payloads. Adapters that expose an external standard implement that standard's endpoint shape, media type, token and field names independently. For example an AGS adapter accepts the standard numeric score fields and sends the internal grade-evidence command with canonical decimal strings. SCORM JavaScript methods are also distinct from the internal HTTP batch contract.

## 1.2 Native envelope version 1

A native transfer is a ZIP archive with exact case-sensitive root path `manifest.json`, UTF-8 JSON without duplicate object keys, and zero or more referenced files. There must be no wrapper directory, encrypted entries, executable archive attributes, duplicate paths, or unlisted files other than `manifest.json` and its detached signature if enabled. The envelope is independent of a storage implementation. Default limits are 10,000 declared entries, 1 GiB compressed input, 4 GiB expanded input, 100 MiB per JSON document and 50 MiB per object file. Limit exceptions require authorized per-job approval before extraction.

| Manifest field | Type and cardinality | Validation |
| --- | --- | --- |
| `format` | Required string | Exact `lms.curriculum` |
| `version` | Required integer | Exact 1 |
| `artifact_id` | Required UUID | Identifies this exported envelope independently of content |
| `created_at` | Required RFC 3339 date-time | UTC canonical serialization. Time is descriptive rather than an ordering authority |
| `source_namespace` | Required absolute URI string, 1 to 512 characters | Assigned immutable namespace. Import operator grants authority to claim it |
| `root_refs` | Required array, one to 1,000 distinct record keys | Every root targets an object record in the same manifest |
| `required_capabilities` | Required array of distinct lowercase versioned tokens, default empty | Unknown token blocks import before object creation |
| `optional_capabilities` | Required array of distinct lowercase versioned tokens, default empty | Unknown token creates a report item and preserves safe data for re-export |
| `objects` | Required array of object records, one to 10,000 | Each carries kind, identity key, revision, file, SHA-256, size and references |
| `assets` | Required array of asset records, zero to 10,000 | Each carries key, safe file path, digest, size, media type and rights disposition |
| `extensions` | Optional object keyed by reverse domain names | Preserve inert values subject to size, privacy and schema checks |

An object record has required `key`, `kind`, `revision`, `path`, `sha256`, `byte_length`, and `references`. A key matches `^[a-z][a-z0-9_-]{0,31}/[A-Za-z0-9._~-]{1,128}$` within the artifact, independent from its canonical UUID. A revision is an opaque case-sensitive string of 1 to 128 characters. Kind is a registered canonical entity or an approved namespaced extension. A reference contains a relation code, the target record key or external identifier, and its target revision when pinned. Fields `key` and `external` are mutually exclusive. All required references must resolve within the same Institution. A packaged reference may not cross from content to any student record entity.

Asset records use `key`, `path`, `sha256`, `byte_length`, `media_type`, and `rights`. Rights enumerates `institution_owned`, `licensed`, `restricted`, and `unknown`. Restricted bytes require a destination policy decision. Unknown rights block release where the asset is required. Two asset records can refer to the same verified bytes through distinct logical paths and access scopes. All paths use a slash and normalized Unicode NFC. Reject absolute paths, Windows separators, drive letters, empty segments, dot segments, NUL, and any encoded separator. Match exact decoded paths without guessing case.

A CourseVersion root declares its Course identity, a release-independent version label, ordered ContentPlacement records, pinned ActivityVersions and prerequisite relations. A Library root contains reusable entry versions and approved metadata. ItemVersion documents carry safe prompt content, interaction shape and accessibility metadata. Scoring and expected responses live in separate protected records referenced by key. The export policy includes these records only when the publisher has export-answer authority. An export profile intended for learners replaces all such references with a redacted capability and cannot be reimported as a fully gradeable course.

## 1.3 Integrity and serialization

1. Read `manifest.json` with strict UTF-8 and duplicate-key detection. Verify schema and profile before expanding referenced bytes.
2. Validate canonical relative paths, set membership, collision policy, counts, lengths, and quotas.
3. Hash each referenced file as read, check byte length and lowercase 64-digit hexadecimal SHA-256, then move exact bytes to a private content-addressed store. Keep compressed and expanded bytes under their own digest where they differ.
4. If signature policy is enabled, require a detached signature on RFC 8785 canonicalized manifest bytes. Resolve the signer only from configured trust roots. Validate algorithm and trusted key ID and reject expired or revoked trust. A valid signature gives provenance for signed bytes and no publication permission.
5. Allocate identities for all declared records, build graph edges, validate referential integrity and compare source and target revisions. Keep semantically significant raw fields available for audit and round-trip under access controls.
6. Use canonical JSON for JSON content fingerprints. Decimal points, percentages and grade thresholds are canonical decimal strings of up to 18 digits and six fractional places unless the owning domain specifies tighter precision. Reject negative zero and exponent notation for these data. Store IEEE binary floats only where a standard protocol requires them.
7. A native re-export keeps source object keys and versions wherever their authority is intact. Archive byte equality is optional since compression, entry ordering and creation time may vary. Verify graph semantic equivalence, published projection equality, and each asset digest.

## 1.4 Version negotiation

A recognized minor optional capability absent from the target raises a loss issue. A new envelope major version receives `UNSUPPORTED_FORMAT_VERSION`. A new canonical object revision never overwrites a historic published revision. Extension payloads are inert and untrusted throughout import, preview and export. An upgrade to the adapter repeats parse into a new staging job with its own parser fingerprint and never silently reuses an old approved mapping.

| Input | Outcome |
| --- | --- |
| Valid native manifest with no optional capabilities | Process via declared v1 graph contract |
| Required capability `assessments.algebra/2` unavailable | Blocking issue on root. Authoring remains unchanged |
| Unknown optional `presentation.notes/3` | Preserve safe typed data and publish report. Ignore for learner rendering |
| Altered asset length 550 with original manifest length 549 | Quarantine integrity failure, even if displayed preview appears identical |
| UUID already owned by a different Institution | Generate destination identity and retain only an external provenance alias where allowed |
| ZIP containing `files/x.html` and `FILES/X.html` | Reject on deployment-wide case-fold collision policy before exposure |

## 1.5 UI and operator evidence

Transfer operators see declared format, direction, supported features and required review before starting. The detail screen shows format signature, archive digest, adapter revision, export permission profile, issue count and object counts without displaying protected key data. Use separate actions for raw archive download, issue evidence, projected curriculum preview, and reviewer decisions. Each action checks scoped permission and has an accessible keyboard path. An unknown format shows safe metadata and guidance for obtaining an expected export. Attach a machine-readable inventory with per-kind counts and the exact source artifact digest to the operator's review.

- [JSON Canonicalization Scheme](https://www.rfc-editor.org/rfc/rfc8785.html)
- [UUIDs](https://www.rfc-editor.org/rfc/rfc9562.html)
