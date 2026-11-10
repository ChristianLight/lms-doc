# Curriculum acceptance scenarios

## CUR-001 — Publication rejects stale independent review

Covers `PublishCourseVersion`, `CourseVersion`, `CourseDraft`.

### Given

- Draft revision 7 approved with digest A.

### When

- Edit a caption to revision 8.
- Attempt publish with revision 7 and digest A.

### Then

- 409 DRAFT_CHANGED.
- No publication or published event.

### Fixture values

```json
{
  "reviewed_revision": 7,
  "current_revision": 8
}
```

## CUR-002 — Duplicate creates independent learning occurrences

Covers `MutateDraftOutline`, `DraftPlacement`, `ContentPlacement`.

### Given

- Parent has lessons A and B. A has one resource R.

### When

- Duplicate A.
- Move its copy ahead of A.

### Then

- Copy and copied child receive two new keys.
- Original and copy share allowed resource revision and retain independent progress.

### Fixture values

```json
{
  "original_children": 2,
  "final_children": 3,
  "new_placement_keys": 2
}
```

## CUR-003 — Three-way propagation preserves local text

Covers `PreviewTemplateMerge`, `ApplyTemplateMerge`, `TemplateMergePlan`.

### Given

- Base core text A and no note.
- Source changes core to B. Target adds note N.

### When

- Preview and apply approved merge.

### Then

- Core B and note N appear.
- Publication remains at prior version until separately approved.

### Fixture values

```json
{
  "base": {
    "core": "A"
  },
  "source": {
    "core": "B"
  },
  "target": {
    "core": "A",
    "note": "N"
  }
}
```

## CUR-004 — Protected concurrent edits require a decision

Covers `PreviewTemplateMerge`, `TemplateMergePlan`.

### Given

- Same protected path has values A, B and C in baseline, source and destination.

### When

- Preview merge.

### Then

- One unresolved conflict, no draft change.

### Fixture values

```json
{
  "baseline": "A",
  "source": "B",
  "destination": "C"
}
```

## CUR-005 — Type mismatch stays quarantined

Covers `FinalizeAssetUpload`, `RecordAssetScan`, `AssetVersion`.

### Given

- Declared image/png upload contains HTML.

### When

- Finalize exact bytes and scan.

### Then

- State rejected and no approved rendition or learner URL.

### Fixture values

```json
{
  "declared": "image/png",
  "detected": "text/html"
}
```

## CUR-006 — Durable publication retry returns same version

Covers `PublishCourseVersion`, `CourseVersion`.

### Given

- Manifest and database transaction committed but client timed out.

### When

- Retry with same idempotency key.

### Then

- Original course version ID and digest returned, one published event.

### Fixture values

```json
{
  "network_failure": "after_commit"
}
```

## CUR-007 — Unresolvable prerequisite blocks publication

Covers `ValidateCourseDraft`, `LearningRuleVersion`.

### Given

- A requires B completed. B requires A completed.

### When

- Validate draft.

### Then

- Report OUTLINE_DEPENDENCY_CYCLE with both affected stable keys.

### Fixture values

```json
{
  "edges": [
    [
      "A",
      "B"
    ],
    [
      "B",
      "A"
    ]
  ]
}
```

## CUR-008 — Preview never creates an attempt

Covers `PreviewCourseDraft`, `ActivityVersion`.

### Given

- Exam draft accessible to author.

### When

- Start simulated learner preview and operate exam controls.

### Then

- UI is explicitly a preview. No official attempt or progress record.

### Fixture values

```json
{
  "audience": "learner",
  "simulate_exam": true
}
```

## CUR-009 — Catalog code normalization and metadata compare-and-swap

Covers `CreateCourse`, `UpdateCourse`, `ArchiveCourse`, `Course`.

### Given

- Unit M is in institution S. Existing catalog code ALG.

### When

- Create ALG-2, update its title from Algebra II to Intermediate Algebra at revision 1, try stale update at revision 1, and archive at revision 2.
- Try to create alg under the same institution.

### Then

- ALG-2 revisions 1, 2 and 3 are visible to authorized staff. Stale update fails. Case-folded ALG collision returns 409 COURSE_CODE_EXISTS.

### Fixture values

```json
{
  "existing_code": "ALG",
  "new_code": "ALG-2",
  "duplicate": "alg",
  "revised_title": "Intermediate Algebra"
}
```

## CUR-010 — Publish independent reviewed draft and read exact manifest

Covers `CreateCourseDraft`, `CreateContentNode`, `SealContentNodeVersion`, `CreateActivity`, `SealActivityVersion`, `SealLearningRuleVersion`, `SubmitCourseDraft`, `DecideCourseDraft`, `PublishCourseVersion`, `GetCoursePublication`, `ArchiveCourseVersion`, `CourseDraft`, `CourseVersion`.

### Given

- A course has no prior version, a reviewer separate from its author and a published assessment definition.

### When

- Create blank draft, create lesson definition and quiz activity, then seal edits and an acknowledgment rule.
- Insert exact versions, validate, submit digest and receive independent approval. Publish then read the exact manifest.
- Archive the publication with active uses acknowledged.

### Then

- Version 1 reflects the approved content and exact assessment binding. Archived version retains readable authorized manifest and cannot be selected as new default.

### Fixture values

```json
{
  "course": "ALG-2",
  "initial_draft_revision": 1,
  "expected_course_publication": 1,
  "reviewer_same_as_author": false
}
```

## CUR-011 — Author withdraws an abandoned fork

Covers `CreateCourseDraft`, `AbandonCourseDraft`, `CourseDraft`.

### Given

- Course has publication version 2 and active learners.

### When

- Fork a draft from version 2, then abandon it with reason obsolete proposal.

### Then

- Fork has matching stable placement keys. Abandon changes only the fork and leaves version 2 and learner records intact.

### Fixture values

```json
{
  "source_version": 2,
  "terminal_draft_state": "abandoned"
}
```

## CUR-012 — Library linked adoption and independent detachment

Covers `CreateLibrary`, `PublishLibraryEntry`, `AdoptLibraryEntry`, `DetachLibraryAdoption`, `LibraryAdoption`.

### Given

- Institution S licenses its fractions explainer for independent copy within S.

### When

- Create library STEM. Publish FRACTIONS revision 1. Adopt linked into lesson L and detach after correcting attribution.

### Then

- The independent definition receives a new logical identity. Provenance retains source revision 1 and linked updates no longer target the detached placement.

### Fixture values

```json
{
  "library_code": "STEM",
  "entry_key": "FRACTIONS",
  "source_version": 1,
  "mode_before": "linked",
  "mode_after": "independent"
}
```

## CUR-013 — Asset permission and emergency withdrawal lifecycle

Covers `InitiateAssetUpload`, `FinalizeAssetUpload`, `RecordAssetScan`, `WithdrawAssetVersion`, `AssetVersion`.

### Given

- A 4096-byte approved media upload belongs to a shared lesson. The exact digest is later identified as compromised.

### When

- Allocate one-use upload, receive and scan exact bytes, publish a reference, then withdraw under authorized reason.

### Then

- Quarantined bytes are inaccessible until approval. Withdrawal denies subsequent authorized delivery while immutable published references and source evidence survive.

### Fixture values

```json
{
  "verified_bytes": 4096,
  "final_state": "withdrawn",
  "references_preserved": true
}
```

## CUR-014 — Hosted media requires a pinned provider revision

Covers `ReserveHostedAssetVersion`, `ApproveHostedAssetVersion`, `AssetVersion`.

### Given

- A teacher has an approved institutional media connection and rights to media key video-11.

### When

- Reserve hosted asset. Try approval when provider reports a moving latest alias. Resolve provider version media-v2-20261110 and retry through the authorized map.

### Then

- Alias fails REMOTE_ASSET_UNPINNED. Immutable provider revision links through ExternalResourceMap. AssetVersion contains no raw remote URL or managed bytes pointer.

### Fixture values

```json
{
  "unacceptable_version": "latest",
  "approved_version": "media-v2-20261110",
  "storage_mode": "externally_hosted"
}
```

## CUR-015 — Protected source intake remains distinct from learner PDF

Covers `ReserveCurriculumSource`, `AuthorizeCurriculumSourceUsage`, `StartSourceExtraction`, `SourceExtractionRun`, `AssetVersion`.

### Given

- Scoped author uploads a 28000-byte PDF and Platform verifies a managed evidence-purpose StorageObject.

### When

- Request private extraction and adaptation, with no learner download or remote provider permission. Queue physical pages 0 and 1. Attempt to bind the original AssetVersion in learner delivery.

### Then

- Authorized extraction accepted. Learner placement validation rejects evidence-purpose asset. Distribution requires a separate content-purpose version and rights.

### Fixture values

```json
{
  "expected_bytes": 28000,
  "page_indices": [
    0,
    1
  ],
  "storage_purpose": "evidence",
  "approved_purposes": [
    "private_extract",
    "adapt"
  ],
  "learner_bind_allowed": false
}
```

## CUR-016 — Rotated PDF page evidence is exact and repeatable

Covers `CommitSourceExtractionPage`, `SealSourceExtraction`, `GetSourceExtractionSummary`, `ReadSourceRegion`, `SourceRegion`, `SourceExtractionRun`.

### Given

- One selected page with crop [10,20,210,120], user unit 1 and clockwise rotation 90 degrees.

### When

- Fenced page worker submits source box [30,50,70,70] twice with same digest. Independent reviewer accepts exact recognized region and seals. Staff read region then open authorized evidence.

### Then

- One accepted receipt and region set. Canonical upright bounds [30000,20000,50000,60000]. Safe summary excludes raw source. Unauthorized caller gets generic unavailable.

### Fixture values

```json
{
  "crop_pt": [
    10,
    20,
    210,
    120
  ],
  "rotation": 90,
  "source_box_pt": [
    30,
    50,
    70,
    70
  ],
  "canonical_box_mpt": [
    30000,
    20000,
    50000,
    60000
  ],
  "unique_page_receipts": 1
}
```

## CUR-017 — Sealed source correction preserves old lineage

Covers `StartSourceExtraction`, `CommitSourceExtractionPage`, `SealSourceExtraction`, `SourceExtractionRun`, `SourceRegion`.

### Given

- Prior exact source evidence mistook − for a hyphen. A candidate points to prior sealed region.

### When

- Start correction run with exact predecessor and revised review manifest. Commit corrected page and seal.

### Then

- New run and corrected region have new identities. Earlier source reference and affected candidate remain auditable. Changed claim requires renewed review.

### Fixture values

```json
{
  "prior_method": "ocr",
  "correction_method": "transcription",
  "prior_link_retained": true
}
```

## CUR-018 — Authoring workflow applies a reviewed complete subset

Covers `StartCurriculumAuthoringRun`, `RecordCurriculumAuthoringStage`, `RecordSourceDerivationLinks`, `ReadAuthoringRun`, `ReviewCurriculumAuthoringRun`, `ApplyCurriculumAuthoringSelection`, `ReadSourceDerivationTrace`, `CurriculumAuthoringRun`, `SourceDerivationLink`.

### Given

- Exact draft revision 7 and approved source state. One exercise contains enough input, another is missing its rate.

### When

- Start run, seal staged candidates and exact protected lineage. Independent reviewer selects dependency-closed complete subset. Apply at expected revision 7 and reconcile owner receipts.

### Then

- The complete item and linked lesson become authorized draft changes. Missing-rate item remains blocked. Source answer metadata stays staff-only. No publication or offering activation.

### Fixture values

```json
{
  "initial_draft_revision": 7,
  "available_inputs": [
    "elapsed_time"
  ],
  "unresolved_input": "fill_rate",
  "official_attempts_created": 0
}
```

## CUR-019 — Stale stage and cancellation do not overwrite owner history

Covers `RecordCurriculumAuthoringStage`, `ApplyCurriculumAuthoringSelection`, `CancelCurriculumAuthoringRun`, `CurriculumAuthoringRun`.

### Given

- Worker effect A committed a draft change, lost acknowledgement and lease expired. Later worker observes receipt.

### When

- Retry A with old fence. Cancel future effects. Read current owner receipt and run history.

### Then

- Old worker fails AUTHORING_FENCE_EXPIRED. Existing effect reconciles once. Run canceled, prior authorized draft output preserved.

### Fixture values

```json
{
  "effect_commit": "before_timeout",
  "old_fence": 3,
  "current_fence": 4,
  "duplicate_owner_writes": 0
}
```

## CUR-020 — Provider rights are checked before page dispatch

Covers `AuthorizeCurriculumSourceUsage`, `StartSourceExtraction`, `ReadSourceRegion`, `SourceExtractionRun`.

### Given

- Human approved private_extract for selected region and no external_process. A worker requests hosted OCR.

### When

- Attempt hosted extraction then switch to approved local isolated profile.

### Then

- Hosted request denied before sending bytes. Local can proceed. A page with mixed answer and teaching regions is shown only to an authorized reviewer or redacted crop view.

### Fixture values

```json
{
  "requested_remote_ocr": true,
  "bytes_disclosed_before_approval": 0,
  "fallback": "local_isolated"
}
```
