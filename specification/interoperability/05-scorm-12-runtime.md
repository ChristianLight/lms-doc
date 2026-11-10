# 05. SCORM 1.2 browser runtime and attempt state

## 05.1 Edition and conformance boundary

This profile handles a SCORM 1.2 SCO in a browser. Its public interface is the case-sensitive JavaScript object `API`. A SCO finds this object in its parent window ancestry or permitted opener ancestry. The player installs the object before it starts the SCO. A packaged asset has an entry URL and no SCORM calls. A resource may be reused in several manifest item occurrences. Each occurrence retains its own attempt state, clock and launch policy.

Provide the mandatory runtime and all optional elements described below. Enable the full optional profile by default for new installations. A compatibility profile may disable an optional family for a declared deployment and must return the prescribed unsupported-element results. The player publishes the exact runtime, package and browser profile tested. SCORM 1.2 defines runtime and content aggregation. An optional prerequisite rule supported by a deployment is evaluated against the occurrence identifiers in the manifest and follows that profile. It does not use the SCORM 2004 sequencing engine.

The external wire values are strings even when the internal representation is a number, flag, enumeration or duration. In the tables below, **R** means SCO read only, **W** means SCO write only, **RW** means both and **K** means read-only keyword. **M** marks required LMS support and **O** marks a standard optional LMS element. The decision to expose all O rows belongs to this product profile. Collection parent names serve as address prefixes. Reading a bare collection or group does not serialize an object.

## 05.2 Interface and lifecycle

| Browser call | Argument contract | Successful return | Failed return |
| --- | --- | --- | --- |
| `LMSInitialize("")` | One literal empty string | String `"true"` | String `"false"` |
| `LMSFinish("")` | One literal empty string | String `"true"` | String `"false"` |
| `LMSGetValue(element)` | One exact dot-notation address | String value, including valid `""` | `""` |
| `LMSSetValue(element, value)` | Exact dot-notation address and string value | String `"true"` | String `"false"` |
| `LMSCommit("")` | One literal empty string | String `"true"` | String `"false"` |
| `LMSGetLastError()` | No arguments | Current error code string | Returns the current code without modifying it |
| `LMSGetErrorString(code)` | One error code string | Public label or `""` for an unrecognized code | Never replace the stored last error |
| `LMSGetDiagnostic(code)` | Code string, where `""` selects the current error | Sanitized diagnostic string | Unknown code returns `""` in this profile |

A session begins **new** with no initialized SCO communication. The gateway has already checked enrollment, the immutable package version, occurrence, and an active attempt or authorized review. Its launch snapshot becomes immutable input for the local API instance. A valid Initialize changes **new** to **active** once. Get, Set, Commit and Finish require **active**. A valid Finish invocation ends the SCO-facing communication instance. Return `"true"` only after final data and close are durably confirmed. If Finish returns `"false"`, the 1.2 SCO has entered **finished** and may use diagnostics. Host recovery can reconcile the same terminal envelope and receipt without a second SCO Finish or a new academic attempt. A failed Commit before Finish leaves the outcome uncertain, and this implementation permits a retry while the lease remains valid. A duplicate Initialize and a repeated Finish are outside the normal lifecycle. This profile returns `101` for those redundant calls and `301` for Get, Set and Commit outside active communication. Keep the profile decisions under conformance tests because 1.2 does not enumerate every failure phase as 2004 does.

Each normal call sets last error to `0` on success and to its exact failure code on error. Diagnostics never clear the error. A successful empty string is distinguishable from an invalid read only through `LMSGetLastError()`. Return values are never booleans, thrown exceptions or promises. Keep argument strings and code strings separate from HTTP return codes. Calls are synchronous in the browser and use the durability policy of [secure player design](08-scorm-player-security-and-durability.md). A browser request carrying previously acknowledged mutations is idempotent by session and sequence. A 1.2 API error stays visible to the SCO even if a service layer fault also creates a support incident.

| Code | Meaning in this profile | Reproducible example |
| --- | --- | --- |
| `0` | Successful last normal operation | Empty initial bookmark reads as `""` with `0` |
| `101` | General runtime or lifecycle failure | Durable commit service fails or Initialize is repeated |
| `201` | Invalid argument or unknown element inside the SCORM model | `LMSInitialize("start")` or `LMSGetValue("cmi.core.zip_code")` |
| `202` | The valid base element has no `_children` keyword | `LMSGetValue("cmi.core.student_id._children")` |
| `203` | The valid base element has no `_count` keyword | `LMSGetValue("cmi.core._count")` |
| `301` | Communication is not initialized or no longer active | Read before Initialize |
| `401` | A defined optional element is unavailable or a separate unimplemented model was addressed | Read disabled `cmi.objectives._count` or query `xyz.score` |
| `402` | An attempt was made to set a valid keyword | Set `cmi.core._children` |
| `403` | A read-only leaf was written | Set `cmi.core.student_name` |
| `404` | A write-only leaf was read | Get `cmi.core.exit` |
| `405` | The value fails the leaf type, vocabulary, length or range | Set `cmi.core.score.raw` to `"85%"` |

Use the API error table for invalid data types. Some field examples in the archived runtime book use `205` in that context. The general API error table defines `405` and has no `205` entry. Compatibility fixtures may record the historical ambiguity. Do not expose undocumented numeric codes.

For a supported session, first validate argument shape and parse the exact path. Resolve the declared group or leaf and any legal keyword. Check optional profile availability before checking leaf access. Validate the array index and type. Apply no mutation when validation fails. A noncanonical value like `"Passed"` fails vocabulary validation rather than being repaired. A known optional group is omitted from its parent's supported-children response when disabled.

## 05.3 Data types

| Type | Wire format and acceptance |
| --- | --- |
| CMIString255 | Up to 255 ASCII characters. Preserve significant whitespace. Apply field-specific rules where listed. |
| CMIString4096 | Up to 4,096 ASCII characters and therefore up to 4,096 ASCII bytes. Never silently truncate or rewrite suspend data. |
| CMIIdentifier | Nonempty identifier up to 255 characters without whitespace or unprintable characters. Use an ASCII identifier generated for this profile. The institutional profile name is stored separately. |
| CMIDecimal | Optional leading minus and optional fractional part. Reject currency, commas, percent signs, exponent notation and non-finite values. Store exact decimal text or a lossless numeric value. A permitted blank remains unset rather than zero. |
| CMIInteger | Whole numeric string from 0 through 65,536 as defined in the 1.2 book. Apply tighter field or storage limits where declared. |
| CMISInteger | Signed whole numeric string. Apply the field's tighter range. |
| CMITime | Clock reading in 24-hour `HH:MM:SS` format, with optional one or two decimal digits for seconds. Hours range 00–23. It is a local clock reading without a zone or date. |
| CMITimespan | Elapsed time as `HHHH:MM:SS[.ff]` with 2–4 hour digits, exactly 2 minute and second digits and optional 1–2 fractional digits. Minutes and whole seconds range 00–59. Internal units are integer hundredths of a second. |
| CMIVocabulary | Exact case-sensitive value for the individual field. `""` is permitted only where stated. |
| CMIFeedback | Type-dependent response grammar in §05.6. Preserve original wire text for reporting. |

Unrecognized control characters and unsupported Unicode in strict ASCII strings fail validation. A deployment may expose a Unicode compatibility profile for a specific package. A documented compatibility shim is separate from the conformance profile and cannot silently change the required wire model.

## 05.4 Mandatory core data and package setup

| Exact path | Access | Support | Type, initial value and source |
| --- | --- | --- | --- |
| `cmi.core._children` | K | M | CSV of implemented direct names. Full profile returns `student_id,student_name,lesson_location,credit,lesson_status,entry,score,total_time,lesson_mode,exit,session_time`. |
| `cmi.core.student_id` | R | M | CMIIdentifier, stable opaque learner key for the authorized package context. |
| `cmi.core.student_name` | R | M | CMIString255, display name serialized as family then given name when the known profile permits. Use the configured learner-facing display label or pseudonym. |
| `cmi.core.lesson_location` | RW | M | CMIString255, initially `""`, SCO-owned bookmark. |
| `cmi.core.credit` | R | M | `credit` or `no-credit`, default `credit` for assigned learner attempts. Browse and review use the approved mode/credit snapshot. |
| `cmi.core.lesson_status` | RW | M | `passed`, `completed`, `failed`, `incomplete`, `browsed`, `not attempted`. First credit launch defaults to `not attempted`. The runtime book advises SCOs against writing that initial-only status. |
| `cmi.core.entry` | R | M | `ab-initio` on first launch, `resume` on a continued suspended state, or `""` for a later non-suspended reentry. |
| `cmi.core.score._children` | K | M | CSV of score leaves supported by the runtime. Full profile returns `raw,min,max`. The required leaf is `raw`. |
| `cmi.core.score.raw` | RW | M | CMIDecimal in [0,100] or blank, initially `""`. |
| `cmi.core.score.min` | RW | O | CMIDecimal in [0,100] or blank, initially `""`. |
| `cmi.core.score.max` | RW | O | CMIDecimal in [0,100] or blank, initially `""`. |
| `cmi.core.total_time` | R | M | CMITimespan, initially `0000:00:00.00`. At launch it reflects finalized prior session deltas. |
| `cmi.core.lesson_mode` | R | O | `browse`, `normal`, `review`, default `normal` for assigned learners. |
| `cmi.core.exit` | W | M | `time-out`, `suspend`, `logout` or `""`. Session default is blank. |
| `cmi.core.session_time` | W | M | CMITimespan. When absent, this session supplies no SCO-reported time. Last valid value wins within the session. |
| `cmi.suspend_data` | RW | M | CMIString4096, initially `""`. Opaque to the LMS. |
| `cmi.launch_data` | R | M | CMIString4096, launch data declared on the item or `""`. |
| `cmi.comments` | RW | O | CMIString4096, initially `""`. Preserve the latest full value and the restricted audit of accepted changes. |
| `cmi.comments_from_lms` | R | O | CMIString4096, initially `""`. Restricted instructor-provided feedback snapshot. |

The data model reports the SCO-defined interval exactly. Repeated Set calls replace the pending session duration. Repeated commits do not add to `total_time`. On finalization, write one duration ledger row per session and add it once to the persisted total for this SCO occurrence's attempt. Browser presence and package-reported seat time are separate records. A clock that reaches the edition wire limit is surfaced as a diagnostic and a bounded edition read, while the internal ledger preserves the full total. Hours never roll back to zero because a formatted value overflowed.

For a valid review or no-credit browse, use a separate working snapshot and avoid changing official grade evidence. Allow a first no-credit browse display to report `browsed` in its private snapshot. Use authoritative learner display policy to determine whether the actual name is needed. The SCO cannot write its identity, mode, credit, mastery, maximum time or launch data.

## 05.5 Optional objectives, attempt policy and preferences

| Exact path | Access | Type, initial value and source |
| --- | --- | --- |
| `cmi.objectives._children` | K | `id,score,status` when the family is enabled. |
| `cmi.objectives._count` | K | CMIInteger, `"0"` initially. Count of initialized rows. |
| `cmi.objectives.n.id` | RW | CMIIdentifier identifying the SCO-owned objective. |
| `cmi.objectives.n.score._children` | K | `raw,min,max` when supported. |
| `cmi.objectives.n.score.raw` | RW | CMIDecimal in [0,100] or blank. |
| `cmi.objectives.n.score.min` | RW | CMIDecimal in [0,100] or blank. |
| `cmi.objectives.n.score.max` | RW | CMIDecimal in [0,100] or blank. |
| `cmi.objectives.n.status` | RW | Same six literals as `cmi.core.lesson_status`. Use `not attempted` when the stored objective has a default status. |
| `cmi.student_data._children` | K | `mastery_score,max_time_allowed,time_limit_action`. |
| `cmi.student_data.mastery_score` | R | CMIDecimal in [0,100], manifest `adlcp:masteryscore` or blank. |
| `cmi.student_data.max_time_allowed` | R | CMITimespan from item manifest maximum time, blank when absent. |
| `cmi.student_data.time_limit_action` | R | `exit,message`, `exit,no message`, `continue,message`, `continue,no message`, or configured default when absent. Default profile uses `continue,no message`. |
| `cmi.student_preference._children` | K | `audio,language,speed,text`. |
| `cmi.student_preference.audio` | RW | Signed integer -1 to 100. -1 is off, 0 means no change, 1–100 raises volume from minimum to maximum. Default 0. |
| `cmi.student_preference.language` | RW | CMIString255 language preference. Blank uses the SCO default. Preserve supplied label according to the 1.2 language field. |
| `cmi.student_preference.speed` | RW | Signed integer -100 to 100. 0 uses the SCO's default. |
| `cmi.student_preference.text` | RW | `-1` off, `0` default, `1` on. Default 0. |

A learner preference changed by the SCO stays in the package attempt. Only a separate authorized accessibility action changes the institutional profile. A package's time-limit action is communicated to the SCO. Independent institutional deadlines use the server's offering and assessment policy, with an explicit grade or attempt status for time enforcement. A package's self-reported session time cannot extend an institutional deadline.

## 05.6 Optional interactions and exact indexing

| Exact path | Access | Type and validation |
| --- | --- | --- |
| `cmi.interactions._children` | K | CSV `id,objectives,time,type,correct_responses,weighting,student_response,result,latency`. |
| `cmi.interactions._count` | K | CMIInteger count. Initially `"0"`. |
| `cmi.interactions.n.id` | W | CMIIdentifier. Preserve both ordinal and identifier. |
| `cmi.interactions.n.objectives._count` | K | CMIInteger count of nested objective references. |
| `cmi.interactions.n.objectives.m.id` | W | CMIIdentifier naming a related objective. |
| `cmi.interactions.n.time` | W | CMITime, event clock time. This is not elapsed time. |
| `cmi.interactions.n.type` | W | `true-false`, `choice`, `fill-in`, `matching`, `performance`, `sequencing`, `likert`, `numeric`. |
| `cmi.interactions.n.correct_responses._count` | K | CMIInteger count of nested patterns. |
| `cmi.interactions.n.correct_responses.m.pattern` | W | CMIFeedback for this row's interaction type. |
| `cmi.interactions.n.weighting` | W | CMIDecimal, supplied weight. |
| `cmi.interactions.n.student_response` | W | CMIFeedback for this row's interaction type. |
| `cmi.interactions.n.result` | W | `correct`, `wrong`, `unanticipated`, `neutral`, or CMIDecimal. `incorrect` belongs to the 2004 vocabulary. |
| `cmi.interactions.n.latency` | W | CMITimespan between presentation and learner response. |

Here `n` and `m` are independent zero-based indices. The adapter materializes packed lists in order. The author-facing rule is that writing a new row at the current count appends it. Writing an existing ordinal updates its leaf. An index beyond the count yields `201` in the strict project profile. Validate the index and interaction type before consuming a slot or appending a leaf. Require an existing or same-journal interaction type before accepting a typed response. A package needing a different write order must declare a tested compatibility policy. Reads of W leaves return `404` even though authorized reporting can read the stored evidence. An unsupported collection is distinguishable from a supported but empty collection.

| Interaction | Learner response and accepted pattern structure |
| --- | --- |
| True-false | One of `0`, `1`, `t`, `f`. The compatibility fixture may accept the historical full words by the first letter rule while preserving the original value. |
| Choice | Comma-delimited individual lower-case letter or digit identifiers, for example `a,c`. A pattern with all choices required can use `{a,c}`. |
| Fill-in | Up to 255 characters of text. Preserve spaces after the first printable character. |
| Matching | Comma-delimited `source.target` pairs of single-character letter or digit identifiers. A pattern can enclose all-required pairs in braces. |
| Performance | Up to 255 characters of free-form task data. |
| Sequencing | Ordered comma-delimited single-character identifiers. The sequence's final order is meaningful. |
| Likert | A single lower-case letter or digit label. A correct pattern may be blank when correctness is inapplicable. |
| Numeric | CMIDecimal learner value. Treat documented pattern variations as adapter-specific fixtures and retain the exact original text. |

The LMS stores the SCO's provided result. The native assessor does not compute a new interaction mark from the reported response or pattern. These patterns can reveal answers. Only instructor roles permitted to see assessment evidence may read them outside the isolated package.

## 05.7 Termination and result rules

1. Verify the commit ledger, attempt revision, active fencing token and authorized occurrence. Apply the final journal in ordinal order. Reject conflicting payloads for an already used sequence key.
2. Compute elapsed time from the last valid session time. Add its delta at most once. Capture `cmi.core.exit` and close the communication session. The database stores raw package state, projected attempt state and one versioned evidence event as distinguishable records.
3. Apply status rules to a valid normal credit attempt. Preserve explicitly reported status. For the case where the SCO never sets status and the current credit attempt still has the initial `not attempted` value, follow the 1.2 finish default of `completed`. A no-credit browse cannot publish official completion. If the package suspended without reporting status, preserve the attempt's suspension and resume data separately from whatever the edition displays for the raw lesson status.
4. For a credit attempt with both valid manifest mastery and SCO raw score, the project's declared 1.2 behavior evaluates raw score against mastery at normal Finish. Equality passes. The threshold comparison uses exact decimal values. Without a configured threshold preserve the explicit status or applicable finish default. Review-only sessions preserve official records. Preserve both SCO-reported and effective RTE status for explanation.
5. Set the occurrence's next entry indicator from its first-launch flag and last terminal exit. `suspend` resumes the same attempt with its bookmark and suspend data. Other exits produce blank on a later reentry of the same occurrence, unless an explicitly authorized fresh attempt creates its own first entry. Retry rules never erase historical registrations.

A published grade policy converts 1.2 normalized raw score directly into a fraction of 100 by default. Optional min/max do not imply renormalization. A teacher can approve an exceptional known-package mapping and pin that policy revision for the entire offering. A blank score creates no numeric evidence. Completion, pass/fail and grading evidence are emitted independently. Score normalization cannot convert browse traffic into an assessed attempt.

| Raw lesson status | Default LearningProgress projection | Default success projection |
| --- | --- | --- |
| `not attempted` | Not started | Unknown |
| `incomplete` | In progress | Unknown |
| `browsed` | Viewed for review | Unknown |
| `completed` | Complete | Unknown |
| `passed` | Complete | Passed |
| `failed` | Complete by the 1.2 combined status interpretation | Failed |

A failed SCO may not have displayed every page. A course-level rule can require a passed result or additional native evidence before declaring course completion. This rule is separate from the edition's meaning of failed.

## 05.8 Executable acceptance traces

Use a synthetic SCO mounted in both iframe and allowed popup launchers. The test harness evaluates the following ordered JavaScript calls and checks exact return strings plus the authoritative persistence ledger.

| Trace | Calls and return expectations | Durable result |
| --- | --- | --- |
| R12-001 lifecycle | Get `cmi.core.entry` before Initialize returns `""`, code 301. Initialize empty returns `"true"`. Get entry returns `"ab-initio"` and code 0. | One authorized launch session and one initialized communication state. |
| R12-002 keyword and access | Set `cmi.core._children` returns `"false"`, code 402. Set `cmi.core.student_name` returns `"false"`, code 403. Read `cmi.core.exit` returns `""`, code 404. | No protected value or collection metadata changes. |
| R12-003 resume and time | Set times `00:04:30.25` then `00:05:10.50`, bookmark `exercise-4`, suspend data `p=4&k=B`, exit `suspend`, then commit twice and finish. | Next launch is `resume`, bookmark and bytes match, and total is `0000:05:10.50`. A later finalized `00:02:15.25` gives `0000:07:25.75`. |
| R12-004 exact mastery | Raw `"70.00"`, mastery `70`, normal credit Finish. Repeat with raw `"69.99"` and explicit `completed`. | First passes, second fails. Preserve the raw numeric values and original explicit status. |
| R12-005 successful blank | Initialized fresh SCO reads `cmi.core.score.raw`. Then reads `cmi.no_such_leaf`. | Both return `""`. First yields code 0, second 201. Diagnostic call preserves code 201. |
| R12-006 interactions | Create row 0 as matching, record `a.b,c.d`, result `wrong`, and one correct pattern. Then try result `incorrect`. | First result persists, wrong-edition literal fails 405, interaction count remains one. Learner API cannot read the W result leaf. |
| R12-007 optional elements | Disable objectives in a diagnostic profile. Get `cmi.objectives._count`. Test `_count` on supported `cmi.core`. | First is 401, second 203. Neither should be represented as a legal zero count. |
| R12-008 quota and gaps | Write a 4,096-character ASCII suspend value, then try a 4,097-character value. Attempt to append row 4 when interaction count is 1. | The first payload round-trips, the oversized Set fails 405, and the array gap fails without creating placeholders. |
| R12-009 crash after commit | Commit bookmark and time, lose tab before Finish, and recover the authorized durable prefix through the host. | Bookmark remains recoverable. No Finish is inferred and the clock delta is credited only under interrupted-session policy. |
| R12-010 uncertain Finish | Finish reaches the server but the synchronous receipt is lost. The SCO sees false and requests diagnostics. The owning host reads the terminal receipt. | SCO API is terminal. Host displays the confirmed close without a second Finish or repeated time credit. |

### Browser SCO smoke probe

Run this script from the fixture SCO document in a fresh normal-credit 1.2 launch with the full optional profile. Let the fixture runner capture its return or thrown error through its existing browser test bridge. The script performs real state mutations and should use a disposable learner registration.

```javascript
function runScorm12SmokeProbe() {
  let context = window;
  let api = null;

  for (let depth = 0; depth < 20 && context; depth += 1) {
    try {
      if (context.API) {
        api = context.API;
        break;
      }
      context = context.parent === context ? context.opener : context.parent;
    } catch (error) {
      throw new Error("Fixture API discovery crossed an unauthorized origin", { cause: error });
    }
  }

  if (!api) throw new Error("SCORM 1.2 API unavailable");

  function expect(method, args, result, code) {
    const actual = api[method](...args);
    const lastError = api.LMSGetLastError();
    if (actual !== result || lastError !== code) {
      throw new Error(`${method} returned ${String(actual)} with error ${lastError}`);
    }
  }

  expect("LMSGetValue", ["cmi.core.entry"], "", "301");
  expect("LMSInitialize", [""], "true", "0");
  expect("LMSGetValue", ["cmi.core.entry"], "ab-initio", "0");
  expect("LMSSetValue", ["cmi.core.score.raw", "70.00"], "true", "0");
  expect("LMSSetValue", ["cmi.core.score.raw", "70%"], "false", "405");
  expect("LMSSetValue", ["cmi.suspend_data", "p=4&k=B"], "true", "0");
  expect("LMSSetValue", ["cmi.core.exit", "suspend"], "true", "0");
  expect("LMSCommit", [""], "true", "0");
  expect("LMSFinish", [""], "true", "0");
  return "SCORM 1.2 runtime probe passed";
}
```

## 05.9 Normative and conformance references

- [ADL SCORM 1.2 Run-Time Environment, October 2001, archived copy](https://xml.coverpages.org/SCORM-12-RunTimeEnv.pdf)
- [ADL SCORM 1.2 Conformance Requirements, archived copy](https://lms.technology/for/scorm/1.2/standards/SCORM_1.2_ConformanceReq.pdf)
- [AICC standards documentation index](https://lms.technology/AICC_index.html)
