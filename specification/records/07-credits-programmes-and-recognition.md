# 07 Credits, programme pathways and recognition

## Programme identity and curriculum rules

A Program is an institution-managed credential pathway or course of study. Its stable code, organizational owner and level distinguish it from a course offering. A ProgramRequirementVersion pins effective admission windows, required and elective courses, credit groups, prerequisites, GPA minimum, residence rules, maximum transfer credits, qualification lifetime and approved substitutions. A ProgramEnrollment assigns a Person to one exact requirement version and records entry period, status and optional predecessor. An adviser can model a version transfer before a registrar approves it. Earlier audits and decisions retain their original version.

Typical rules include course completion with a minimum grade, credit total in a course set, elective count, residency credit, minimum programme GPA, mandatory practical competency and a time window for currency. Store typed rules and verified reference IDs rather than executable text. Required and elective groups form a directed acyclic graph bounded to 256 nodes and 8 levels. A nested group can require all children, at least K child outcomes, minimum eligible credits or one named requirement. The policy records whether one credit award may satisfy multiple groups.

The product default requires named core courses and eligible credits once, with no automatic substitution, no minimum GPA unless published, no public verification, no automatic expiry and no external transfer without approval. An institution chooses its own credits, authority and academic thresholds. Credits are exact nonnegative decimal quantities. A credit scale defines units, precision, policy version and conversion rules. A mark percentage cannot convert to credit units without a published award rule.

## Credit awards

A CreditDecision points to exactly one approved basis, either a final grade release or an approved recognition decision. For a course, load the credit value bound to the approved course version and enrollment and apply the course outcome. Default grants all offered credits if course passed and zero if failed. Withdrawn, incomplete and pending do not grant credit. Partial credit requires explicit policy and a separate normalized evidence mapping. Retain both attempted and earned units. Keep institutional and transfer credits separate in the ledger.

An award revision has institution, person, course identity or equivalence group, unit scheme, source references, attempted and earned amount, GPA eligibility, actor, reason and superseded revision. Only one effective decision applies per identified credit source. A course result correction enqueues credit review. Default revocation of credits linked to an invalidated pass requires an authorized replacement decision. The system does not mutate prior issued credentials silently.

A repeat policy chooses how repeated work contributes to earned credit and GPA separately. Compare by institution-approved equivalence identity. Earliest passing means chronological final academic completion and stable record ID tie-break, not intake time. If two previously accepted inputs appear to be the same activity, block duplicate credit and investigate. Keep every source course on the transcript according to transcript policy.

## Recognition and transfer

1. A learner or authorized registrar opens RecognitionRequest for prior study, external credit, demonstrated competency or experience. Provide type, claimed course or requirement, issuing institution and reference, evidence files and consent for verification where required.
2. A verifier checks issuer, learner identity and authenticity through the authorized channel. Restrict evidence access. Credential verification alone does not decide equivalence.
3. A reviewer records outcome mapping, credit units, possible exemption, GPA eligibility, effective dates and a reason. Default externally transferred credit does not affect GPA and local completion displays a separate transfer designation.
4. A different authorized registrar approves an official award. Approval references the immutable evidence snapshot and review revision. The award or waiver is posted once, with traceable provenance and exact scope.
5. An appeal or revocation produces a new decision. Expired competency can require new proof even where previously granted credit remains valid. Review affected programme and document records separately.

A waiver means a requirement is waived. It grants no earned credit unless a distinct credit award approves units. An exemption can replace attendance or delivery requirements without establishing course credit. A substitution allows one named eligible achievement to fulfill a rule. Never infer equivalency based on translated titles.

## Degree and programme audit algorithm

1. Pin Person, ProgramEnrollment, requirement version, credit and competency decision cutoffs, and selected as-of date. Collect effective approved records. Exclude revoked, expired or unresolved facts according to the rule's criteria. A credit award remains historical even when an audit's currency rule excludes it.
2. Resolve explicit requirement waivers and approved substitutions first. Check their scope, dates and whether they confer credits. An override cannot expand beyond the rule and version it names.
3. Assign exact mandatory course matches in rule priority then stable ID order. Default credit assigned to a mandatory group remains unavailable to later groups unless the rule explicitly permits dual use. Within one rule choose eligible equivalence by the configured repeat basis then stable ID.
4. Allocate remaining credit to elective groups. For disjoint eligible pools, rank by academic completion and stable ID, selecting until group threshold is met. For overlapping indivisible credit pools, use bounded constraint search over candidate award allocations, with eligibility and maximum one counting bucket per award unless configured otherwise. Optimize lexicographically by approved rule priority, satisfied required group count, fulfilled credits up to group minimum and stable sorted source keys. Preserve the canonical match set. A configured search bound of 100,000 candidate states prevents expensive automatic allocation. Exceeding the bound yields needs-review with no automatic completion. A reviewer can explicitly assign awards, and the engine validates all constraints against that proposed assignment.
5. Evaluate residency, minimum grade, currency, programme GPA and competency gates. Persist for each requirement the source decision references, used credits, shortfall and reason. A logical group is fulfilled only when its typed rule is satisfied.
6. Produce an audit result of incomplete, satisfied, needs-review or blocked. Issuance still requires authorized qualification approval. The audit can be reproduced from the exact cutoffs and policy.

**Worked example.** A programme requires Algebra 3 credits, Physics 3, a 6-credit science elective group, at least 6 institutional credits and 12 overall credits. The learner has Algebra 3 and Physics 3 locally, Astronomy 3 locally and transferred Chemistry 3. Mathematics waives a zero-credit introductory prerequisite. The audit shows 12 earned credits, 9 residency credits, 3 transfer credits and a satisfied programme. If the 3-credit Chemistry award is later revoked, the audit shows 9 credits, science shortfall 3 and an alert against the existing qualification. The original issue remains historical until reviewed.

**Overlapping example.** Group A needs 3 credits from Chemistry or Astronomy. Group B needs 3 credits from Chemistry only. Chemistry and Astronomy are each 3 credits. Assign Astronomy to A and Chemistry to B. A greedy first-available algorithm would risk an incorrect shortfall. A programme requirement that intentionally permits double use must still apply the 12-credit overall total against distinct earned awards.

## Interfaces

The adviser audit lists each rule, evidence and remaining action. Learners see their own permitted progress and exclusions with plain-language codes. Staff can propose a substitution from authorized candidate evidence, inspect double-use warnings and submit for approval. Show requirement version, evaluation cutoff, credits and status clearly. Model a future course as a planning assumption and label the result hypothetical. A hypothetical plan must never issue a credential or release a grade.
