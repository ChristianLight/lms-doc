# 06 Report cards, transcripts and official documents

## Report card versus transcript

A ReportCard describes one learner and reporting period. It can contain current or interim released course grades, report comments, attendance summaries, competency statements and planned follow-up where authorized. A Transcript is a durable educational record. It contains eligible final course grades, official credits, programme awards and grade-point summaries according to institution policy. It excludes staff-only evidence, internal analytics and draft grade calculations. A learner's downloadable progress summary is separately labeled unofficial.

A ReportTemplateVersion or TranscriptTemplateVersion fixes version, locale, field schema, layout, classification and allowed data. ReportCardRevision and TranscriptRevision each contain an immutable structured document snapshot and content digest. An issued revision additionally records issuer, issue time, purpose, authorized release entries, normalization labels and rendered asset digest. A generated PDF is an output. The structured record and issuance event supply authoritative data and provenance. An issuer-defined, public revocable verification identifier may be allowed under an approved privacy policy.

| Record | Relationships | Required behavior |
| --- | --- | --- |
| ReportCard | Institution, Person and AcademicPeriod, report type | Stable identity across replacements |
| ReportCardRevision | Card, prior revision, template version, grade and evidence cutoff, approved comments and attendance | Immutable staged and issued snapshot |
| Transcript | Institution, Person, transcript profile | Stable series identity |
| TranscriptRevision | Transcript, template version, final GradeReleaseEntry, CreditDecision and programme award IDs | Durable issuance with purpose and cutoff |
| RecordDocumentArtifact | Exactly one issued report or transcript revision, mime type, AssetVersion and digest | Restricted download and digest verification |
| RecordDocumentStatusEvent | One document revision, issue/replacement/void state, actor, time, reason | Append-only public verification effect |
| AcademicCommentRevision | Person, offering or report card, period, author and audience | Separately approved and snapped at issue |

## Building the snapshot

1. Choose person, purpose, academic period or transcript cutoff, locale and pinned template. Resolve active permitted grades and periods through release pointer queries. For final records use only accepted final or correction release entries.
2. Build a structured snapshot in deterministic order by academic period, offering and stable code. Include grade codes and display labels approved at issuance, local institutional catalog code and title, original offering identity, attempted/earned credit and sanctioned disposition.
3. For report cards, add published comments and attendance by approved policy. Explicitly distinguish no register, excused absence and zero absences. Respect restricted comment and accommodation visibility. Add grade legend and reporting window.
4. For transcripts, apply repeat and transfer rules to GPA and credit independently. Store each course row with credit inclusion and GPA inclusion reasons. Add programme, date and qualifications awarded and any authorized prerequisite certificates.
5. Validate snapshot, stage artifacts and preview. Render complete accessible HTML with reading order, captions, correct header associations and a plain structured download. Where PDF is offered, validate tagging, reading order, language, fonts, pagination and logical page headers.
6. An authorized issuer approves the specific snapshot and artifact digests. Recheck whether input pointer revisions or recipient policy changed. Issue once with a unique external verification identifier where enabled. Notify via authorized delivery.
7. Replacement keeps earlier revision and issues a new one. An issuer records whether old verification becomes superseded or void. Never replace old artifact bytes by serving a new PDF under an old digest or public identifier.

Record batches use a snapshot per learner. Large report-card runs can issue eligible independent learner reports without leaking partial work. A worker marks failed rendering as an error and retryable without changing the approved structured input. A changed template or input requires a new revision. Grade-release suppression updates future previews, not historical documents. Correct a delivered report by replacement and disclose status on a verification request.

## Transcript grade-point calculation

Use GPA only when the institution enables a named GPA scale and GradeScaleVersion defines mapping or a conversion policy. Default is credit-weighted. For each GPA-eligible course, multiply GPA points by attempted GPA credits. Sum quality points and divide by total GPA credits. Use exact ratio and configured display rounding. An excluded or pass/fail credit-bearing course can add earned credits without adding GPA denominator. A failed course can add GPA denominator and zero quality points without adding earned credits. Zero eligible GPA credits returns absent, not 0.00.

Default repeat rule is all transcript attempts shown, GPA counts all graded attempts and credit for a repeated course identity is awarded once, selecting the earliest successful eligible attempt for credit. Configured alternatives may use latest or highest for GPA, within an explicit equivalence group. A change applies through revised policy scope and recalculation, with old issued snapshots preserved. Do not silently merge courses based on title.

| Course | Credits attempted | Grade points | Credits earned | Quality points |
| --- | ---: | ---: | ---: | ---: |
| Algebra | 3 | 4.00 | 3 | 12 |
| History | 4 | 3.00 | 4 | 12 |
| Laboratory pass/fail | 2 | Excluded | 2 | Excluded |
| Biology failed | 3 | 0.00 | 0 | 0 |

GPA is 24 divided by 10 or 2.40. Earned credits are 9. Total attempted credits shown can be 12 while the GPA denominator is 10. If Biology is repeated with 3 credits and 3.00 grade points, all-attempt GPA becomes 33 divided by 13 or 2.54. A latest-only GPA policy yields 33 divided by 10 or 3.30. Repeat policies must disclose which calculation applies.

## Requests, disclosure and verification

A learner requests an unofficial or official copy. A registrar controls approval and recipient routing. Delegates require an effective authorization that explicitly permits educational record disclosure. External destination scope includes recipient organization, purpose, approved profile and expiration. Use authenticated downloads or an approved secure delivery channel. Do not send the document as a routine notification attachment. Artifacts use short-lived download URLs after a fresh authorization check. Verify issuer, current status and approved claims without exposing full transcript or a searchable learner directory. Rate-limit verification by credential namespace and caller.

Represent transfer formats separately. OneRoster Gradebook exchanges line items and grades in supported profiles. A PESC transcript profile can exchange official postsecondary records when required. Provide deterministic mapping reports for terms, grades, codes, credits and local additions. Reject or flag unsupported values rather than treating an exchange acknowledgment as official issuance.

- [OneRoster Gradebook Service](https://www.imsglobal.org/spec/oneroster/v1p2/gradebook/info)
- [PESC College Transcript](https://pesc.org/college-transcript/)
