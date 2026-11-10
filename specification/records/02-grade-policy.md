# 02 Grade policy, categories and scales

## Policy versions

A new offering starts with a draft points-based policy. It has one root category, zero optional credit, no automatic late deduction, manual release, latest eligible submitted attempt, no rounding before mapping, a 50 percent pass threshold and one course-final reporting target. A policy with no counting items cannot publish as a final grade source. An offering may intentionally remain pass/fail completion-only by choosing a published completion-based scale and mapping. A terminal course result cannot be issued for a learner with unresolved required evidence unless an approved incomplete or withdrawal code is recorded.

The version owns the calculation graph, grade item versions and rule parameters. It stores academic period interpretation, grade scale version, assessment selection policy, lateness basis, missing policy, score cap, rounding mode, review gates and result purpose. An offering records a default version. Every enrollment release binds a concrete policy version. Corrections choose the original policy by default. A new policy retroactive to earlier work requires a separate approved reassignment and full impact preview.

| Setting | Default | Valid alternatives |
| --- | --- | --- |
| Category aggregation | Points | Equal items or weighted items, with explicit category contribution |
| Period weighting | No independent period weights | Weighted final using versioned reporting-period totals and basis points |
| Attempt selection | Latest eligible submission. A newer selected pending mark blocks final. | First, highest adjusted ratio, average, or selected by approved decision |
| Higher-is-better assumption | Enabled | Outcome scales have an explicit rank instead of a points comparison |
| Missing before final cutoff | Unresolved | Scheduled provisional zero simulation labeled as a projection |
| Confirmed overdue non-submission | Zero at final calculation | Incomplete pending, explicit excusal, or alternate assessment |
| Submitted but pending marking | Blocks final result | Approved incomplete status without a fabricated numeric mark |
| Inapplicable item | Excluded | No alternative numeric contribution without new applicable evidence |
| Extra credit | Disabled | Optional additive credit with explicit cap and denominator |
| Drop rule | None | Lowest or highest ratio, keep highest, or deterministic one-at-a-time impact |
| Late deduction | Disabled | Fixed percent of max, percent per begun interval, or points per interval |
| Grade visibility | Manual | Auto-release eligible low-stakes items after successful calculation |
| Final release | Registrar approval | Additional two-person approval policy where required |
| Display rounding | Half-up to 2 decimal percentage places | Half-even or truncation at 0 to 4 percentage places |
| Threshold basis | Exact pre-display ratio | Explicit round-before-map mode published before graded work starts |
| Bonus result cap | 100 percent | 100 to 200 percent, or a lower institution cap in ordinary policies |

## Category graph

Use a rooted tree with sibling ordering unique within the version. A group has a mode and reporting points. The root can be unweighted points, weighted category aggregation or a weighted period summary. A parent category can use a child's ratio and declared contribution capacity. A child group earns that capacity multiplied by its calculated ratio. Dropping items inside a child must not silently change the externally declared weight of that child. A points parent with a child must have a declared positive points capacity for the child. An equal parent gives every countable child weight one. Weighted parents require positive configured basis-point weights that sum to 10,000 among ordinary children. Static group membership, contribution capacities and protected required items are validated in the release draft.

The grade tree is bounded to 8 levels, 2,048 total countable items, 256 categories and 128 children per category. Exact arithmetic is performed on bounded integers and rational values. Before publishing, perform a structural evaluation and reject unreasonable graph arithmetic complexity, including expected rational terms beyond the configured computational limit. After publication, a resource limit produces a calculation error with no official result. It cannot quietly replace exact arithmetic with floating point.

Use a separate grade category per purpose when needed. Interim calculations include only evidence with visibility appropriate to the audience and do not inherit final pending semantics. An assessment spanning reporting periods belongs to one grading period based on its configured reporting period binding. Moving a date does not move the assessment to a different period implicitly. An explicitly approved migration must detect existing results in both periods. If final weights combine period totals, every eligible required period must have an approved result or explicit incomplete resolution.

## Grade scales

A GradeScaleVersion specifies a display name, type, default locale, boundary mode, display rule and grading bands. A band has a stable code, locale labels, lower bound inclusive, upper bound exclusive except the final band, optional GPA points, pass state and display sort. For a percentage scale, the intervals cover the full permitted ratio range from zero through the scale's cap, with no gap or overlap. Unbounded bonus is prohibited. An ordinal or status scale provides codes, order and optional passing flag. Numeric arithmetic on ordinal codes is forbidden unless a published conversion maps each allowed code to one explicit normalized value.

The default numeric scale uses fail below 50 percent and pass from 50 percent through 100 percent. The labels and threshold are product defaults. A scale can separately encode letters, honors and GPA points. GPA points belong to a band version or named institutional conversion, not to a display letter. Persist code, approved localized label at issuance and scale version. Changing a label never alters old issued records. Use a separate nonnumeric disposition for incomplete, withdrawn, pending and exempt. These are not grade bands.

## Preview and publish

A course grade policy editor selects a course offering, exact curriculum/delivery release and reference assessments. It renders an accessible tree with move controls in addition to drag handles. Each row shows source, maximum, placement, grading period, rule and ordinary or bonus status. The tester can use synthetic submissions or properly scoped learner evidence. The preview shows denominator changes, hidden material exclusions, rules, attempts affected and effective cutover. It must never expose protected submissions to a user who can design a policy without grade-read permission.

Publishing locks the exact draft hash and assignment plan. Validate all references, weights, scale, schedule, count and deterministic fixtures. Acquire the offering policy guard and compare the proposed parent revision and current draft version. Persist the policy and adoption plan. Activate new enrollment assignments at the approved time. When changing active enrollments, stage all policy assignments and switch a single offering adoption pointer after all staged rows pass. Never activate a partial plan. A policy conflict returns a fresh diff. Worker failure leaves the prior version effective.
