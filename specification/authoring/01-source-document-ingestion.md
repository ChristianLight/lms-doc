# 01. Source document custody, extraction and provenance

A source document is an authoring input. Its original bytes and extraction output stay in protected storage. Publishing the course makes selected learning objects and approved assets available to learners. A PDF reading or handout for learners is a separate publication decision with its own asset revision, accessibility review, rights and retrieval controls. The two can share verified bytes if retention and custody allow separate role-bound resource records.

## 1.1 Ingestion entry points

| Intake | Existing owner and contract | Result |
| --- | --- | --- |
| Standalone source PDF | Curriculum reserves an `AssetVersion` under authoring-source purpose through Platform `StorageObject`. Use `ReserveCurriculumSource`, `FinalizeAssetUpload` and `RecordAssetScan` | Exact approved source version, protected from learner delivery |
| PDF inside an imported archive | Interoperability scans `TransferArtifact`, validates package paths and size, and records the exact source entry in the transfer manifest | An approved source copy can be reserved with its own `AssetVersion` and points back to the archive digest and entry path in protected provenance |
| Learner reading or handout | Curriculum approves a learner-deliverable asset after accessibility, license and audience checks | Typed document activity or resource points to that exact approved version. Course publication carries only this authorized reference |
| New PDF revision | Existing asset receives a new immutable version and digest, with separate extraction | Earlier extraction and derivative lineage remain tied to the exact former version. Adoption of changes goes through a draft diff and review |

Default accept one PDF of up to 50 MiB and 500 pages per extraction run. Also cap page dimensions at 28,800 points per axis, decoded render at 24 million pixels per page, per-page parser CPU at 20 seconds and raster or OCR CPU at 90 seconds. Apply the smaller configured Platform upload and execution limit. Allow an institution to select a page range or reviewed larger profile. Preserve the original total page count and mark unprocessed pages distinctly. Never present an excerpt as the whole source.

1. Authenticate the operator and resolve institution, owning unit and intended course or library scope.
2. Reserve the asset with the Platform evidence purpose through the dedicated authoring-source command. Record the uploaded file name separately from normalized object keys. Detect type by bytes and parser checks.
3. Measure and verify digest, scan and seal the exact storage object. Reject unsupported, malformed, encrypted or active documents under the default policy. A password-protected PDF requires a separately authorized, rights-reviewed source acquisition flow. Keep any secret out of command payloads, tool prompts and logs.
4. Load rights and handling constraints. Verify processing authority before sending page content to an extractor or model. Rights for analysis, adaptation, verbatim republication, sharing figures, learner download and export are independent.
5. Start extraction under a pinned parser, renderer, OCR and segmentation profile. Queue one bounded task per page or small batch. Page operations carry run ID, zero-based physical page index, exact source digest, tool build and lease.
6. Seal a protected extraction manifest containing page metadata, ordered regions, coverage, conflicts, known gaps and extract digest. Select or re-run individual pages through a new extraction revision. Keep any earlier reviewed version available under its retention policy.

Reject external network fetches, attached executable files, embedded scripts, automatic launch, form submission and provider calls in parsing and rendering workers. Treat a standard hyperlink as text or a candidate safe link after validation. Never follow it during source extraction. Treat content, extracted annotations, file metadata and text that looks like an instruction as untrusted source data. A PDF action never grants the agent permission or changes its task. Use isolated, bounded worker processes, private scratch, verified binaries, no network by default and restricted materialized file paths. A rendering timeout quarantines that page attempt and marks its scope incomplete.

## 1.2 Rights, processing and disclosure

| Right | Default | When enabled |
| --- | --- | --- |
| Read for private extraction | Denied pending named uploader or delegated attestation | Exact source version can be processed inside approved infrastructure |
| Send to a remote OCR or agent provider | Denied | Authorized provider, jurisdiction, retention and redaction policy are recorded before dispatch |
| Adapt concepts and generate original instruction | Denied pending approval | Agent can create clearly marked derivative teaching content within approved scope |
| Publish derivative learning objects | Denied pending separate permission | Publication and distribution check exact authorized audience even when adaptation was approved |
| Reuse a quotation, table, page crop, figure or extracted graphic | Denied pending explicit per-purpose right | Publish only the accepted scope and required attribution |
| Distribute original learner PDF | Denied | Create separate learner asset revision under approved audience, locale and publication rights |
| Export assets or derivatives beyond institution | Denied | Resolve export format and recipient authorization and include required notices |

The rights attestation pins institution, source version, rights policy version, authorized actions, recipients and export profiles where applicable, approver, effective interval and protected evidence receipt. An authority owner can withdraw rights through scoped policy or AssetVersion withdrawal. Recheck before extraction, dispatch, draft apply, publication and export. A later authority change can block future reads, new derivatives, publication or export without rewriting prior academic provenance. Student annotations, names or other personal data require approved redaction and handling before content is made available to an agent.

## 1.3 Page coordinate contract

Each page record carries original physical page index, printed label if available, page rotation, effective crop box, PDF user-unit scale, raster dimensions, tool version and affine transforms. Use the physical page index for identity. Printed numbers can repeat or be absent. Display the original page index as a one-based ordinal and show the printed label separately.

Store canonical region coordinates as integer milli-points in the visually upright cropped page, top-left origin with positive axes right and down. Store [x0, y0, x1, y1] half-open, with x0 less than x1 and y0 less than y1. Transform every polygon corner before taking the canonical bounding box. Clip against page extent after outward rounding. Keep the extraction page-to-render and render-to-page affine transform so a reviewer sees the same area at any resolution. Coordinates returned by different tools may already incorporate rotation. Normalize from the tool's declared coordinate frame exactly once.

The following formula applies to unrotated PDF lower-left coordinates after subtracting the effective crop origin and converting by the page user-unit scale. W and H are the effective crop width and height in points.

| Clockwise page rotation | Canonical point before milli-point conversion | Canonical page width and height |
| --- | --- | --- |
| 0 | (X, H − Y) | W, H |
| 90 | (Y, X) | H, W |
| 180 | (W − X, Y) | W, H |
| 270 | (H − Y, W − X) | H, W |

For crop [10, 20, 210, 120] and user unit 1, W is 200 and H is 100. A source box [30, 50, 70, 70] has crop-local corners spanning X 20–60 and Y 30–50. With 90 degree rotation its canonical box is [30000, 20000, 50000, 60000] and upright page extent is 100000 by 200000 milli-points. A reviewer overlay at 144 DPI uses the inverse mapping or two pixels per point and encloses raster pixels [60, 40, 100, 120] on that rendering. Floor start edges and ceil end edges for stable coverage.

The system can optionally emit image fragment coordinates or import standard OCR layout metadata. Its canonical physical PDF page locator remains the source of truth. See the [PDF Association tagged PDF reference](https://pdfa.org/resource/tagged-pdf-q-a/), [coordinate transformation discussion](https://pymupdf.readthedocs.io/en/latest/app3.html) and [Media Fragments](https://www.w3.org/TR/media-frags/).

## 1.4 Extraction and page review

| Page or region signal | Extractor behavior | Review action |
| --- | --- | --- |
| Healthy text layer and semantic tags | Retain raw Unicode, glyph span geometry, tag ancestry and probable logical order. Compare tags to rendered layout | Review headings, reading sequence, footnotes, captions and field layout. Flag mismatches rather than assuming tags are accurate |
| Digital text without dependable structure | Derive lines, columns and block candidates from geometry. Separate running headers and repeated footers. Preserve original order and logical-order proposal | Verify inter-column order and any cross-column callout |
| Scan or failed Unicode mapping | Render upright and OCR with selected language packs. Retain word boxes, raw OCR, normalized text and engine confidence when available | Review low-confidence spans, mathematical signs, units, proper names and inferred characters |
| Mixed digital and image page | Use valid text spans and selectively OCR raster-only regions. Match overlapping boxes and text variants without counting both | Mark disagreements as alternatives. Reviewer selects or transcribes correct span |
| Tables and forms | Capture row, column, spans, header associations, typed values, cells with exact regions, continuation relation and source footnotes | Confirm alignment, units, empty vs zero, headers, formulas and multi-page joins. Required ambiguous cells block reuse |
| Figures and diagrams | Store occurrence geometry, optional raw image reference, rendition and nearby caption association. Distinguish same image reused at different placements | Record rights, meaningful alt text and long description. Recreate diagrams only from approved evidence and compare |
| Mathematics | Preserve displayed glyphs, image overlay and candidate semantic expression. Capture scripts, delimiters, intervals, radicals, fraction lines and sign variants | Compare accessible rendering to source pixels. Confirm expression and any mathematical domain or units independently |

Unicode extraction and OCR each preserve raw output and reviewed transcription separately. Normalize text through an explicit versioned transform log for Unicode composition, ligatures, whitespace and line-wrap changes. Do not silently change negative signs, decimal punctuation, symbols or meaningful hyphenation. Capture every material region's method, confidence when supplied, reading order, exact normalized text or asset digest, conflict state, source geometry and disclosure classification. A mixed page shard inherits its most restrictive region. A weaker scope receives an independently approved redacted rendition or no source object. An engine score is a triage hint. Default flag OCR confidence below 800 on a 0–1000 scale when supplied by the selected profile. Treat missing confidence as unknown. Independently review every region supplying a consequential numeric, mathematical or answer-key claim.

Page-level rows in the protected manifest store engine metrics, covered areas, skipped layers, parser warnings and output state `ready`, `needs_review`, `unavailable` or `excluded`. Select an original glyph span, OCR span or reviewed transcription as the accepted reading. Record exact reviewer decision and resulting digest. Exclude page numbers and repeated layout decoration from lesson text unless they carry educational meaning. Keep their coordinates for reproducibility. Recognized text and layout can be exchanged as [ALTO](https://www.loc.gov/standards/alto/). Semantic math output follows the supported [MathML Core](https://www.w3.org/TR/mathml-core/) or typed source notation profile.

## 1.5 Record and concurrency boundaries

| Record | Identity and relationship | Mutation and query rules |
| --- | --- | --- |
| `SourceExtractionRun` | Exact source AssetVersion, institution, approved rights attestation, profile and configuration digest, selected page set, PlatformJob, protected extraction manifest and digest | Unique institution and canonical run fingerprint covering source version, profile, rights, page set, predecessor and any correction manifest. A planned rerun under a changed profile receives a new run. Index by source and state. Lease and stage compare-and-swap govern jobs |
| `SourceRegion` | Exact extraction run, physical page index, stable region identity, ordered ordinal, upright crop geometry, kind, method, confidence and accepted evidence payload digest | Unique run, page and ordinal. Index run and page for inspection. Region text, crops and alternate readings remain protected. Reviewed corrections create a sealed extraction revision and exact new affected region identities |
| `SourceDerivationLink` | Candidate, released learning version or exact component path, and one or more exact source region IDs with relationship type | Unique exact target version, target path, region and relationship type. Index forward and reverse to show provenance, withdrawal impact and changed source review |
| `CurriculumAuthoringRun` | Institution, target CourseDraft, exact accepted extraction run IDs, job, stage, revision, plan and candidate manifest, rights and approval fingerprints | Unique request fingerprint within actor and target. Candidate output may change while draft stays unmodified. Sealed stage payloads remain inspectable and replay-safe |

Operational retry key includes exact input and profile digests, physical page or batch range, stage and tool contract version. Same key and same canonical input return the existing authorized receipt. Same key and changed input return a conflict. If a worker crashes after writing a result but before acknowledgement, restore by output receipt and exact digest. Reject writes from expired leases and double publication of a page ordinal. A partially processed source remains visible with a deterministic coverage report. Required pages or regions that lack reviewed evidence cannot support eligible claims. Source erasure, retention holds and record custody follow the Platform policy and downstream reference inventory.

See the [agent workflow](02-agent-curriculum-production.md), [quality gates](03-review-quality-and-publication.md), and [task contract](authoring-task.schema.json).
