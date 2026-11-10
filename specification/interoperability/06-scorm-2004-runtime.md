# 06. SCORM 2004 runtime editions and data model

## 06.1 Edition binding

The SCORM 2004 API instance is named `API_1484_11` across editions. The instance answers for one delivery of one SCO occurrence on one learner attempt. `cmi._version` returns `"1.0"` for the IEEE data model and does not identify the edition. Select the edition from the parsed PackageVersion before creating the instance. An unknown or ambiguous edition enters review. A configured best-effort fallback remains visibly separate from the supported profile.

| Package profile | Shared base | Edition-specific behavior |
| --- | --- | --- |
| SCORM 2004 2nd Edition | Synchronous API_1484_11, separate completion and success, typed interactions, Simple Sequencing | 4,000-character suspend data SPM. Use the published RTE and ADL addenda for this edition, including the edition's original navigation and XML bindings. |
| SCORM 2004 3rd Edition | Same API and core CMI family | 64,000-character suspend data SPM. Apply the edition's sequencing and navigation rules and its XML completion threshold representation. Its navigation controls are more explicitly standardized than in earlier editions. |
| SCORM 2004 4th Edition | Same API and data model version | 64,000-character suspend data SPM. Adds targeted Jump, cross-SCO `adl.data`, extended global objective mappings, and additional rollup and progress semantics. Completion threshold uses 4th Edition attribute declarations or the legacy compatible element-value representation, under their specific exclusivity rules. |

A v1.3 or 1st Edition-era package is a separately detected legacy profile and remains quarantined for explicit compatibility assessment. This document enumerates the 4th Edition baseline, with edition gates for 2nd and 3rd Edition. Conformance for an older edition requires running its own fixtures and adopting its own runtime, packaging and sequencing rules. Returning `"true"` for Initialize is not sufficient evidence for a whole-edition claim.

## 06.2 Interface state and exact errors

| Call | Contract | Success | Failure |
| --- | --- | --- | --- |
| `Initialize("")` | One empty string. Changes **not initialized** to **running** once. | `"true"` | `"false"` |
| `Terminate("")` | One empty string. Applies final persistence and changes **running** to **terminated** on success. | `"true"` | `"false"` |
| `GetValue(element)` | One case-sensitive dot-notation element. Computes derived status and navigation validity on reads where specified. | Value as string | `""` |
| `SetValue(element, value)` | Two strings. Validates before staging or committing an atomic local mutation. | `"true"` | `"false"` |
| `Commit("")` | One empty string. Commits the accepted data using the edition persistence contract. | `"true"` | `"false"` |
| `GetLastError()` | No arguments. Works in any communication state. | Last code as string | Last code as string |
| `GetErrorString(code)` | Label lookup of a code. Works in any communication state. | Nonempty public label up to 255 characters for known code | `""` for unknown code |
| `GetDiagnostic(code)` | Code lookup with `""` selecting the current error in this profile. Works in any communication state. | Sanitized string up to 255 characters | `""` for unknown code |

A successful normal call sets `GetLastError()` to `"0"`. Diagnostic calls do not change it. Never use data element initialization as the communication initialization flag. A fresh running instance may return `403` for an unset value. A not-yet-initialized instance returns the lifecycle-specific error before it can consult data state. Normative error codes are separate from UI messages, transport statuses and internal diagnostics.

| Operation | Before initialization | While running | After termination |
| --- | --- | --- | --- |
| Initialize | Success or 102 | 103 | 104 |
| Terminate | 112 | Success, 111 for general termination failure, or 391 if implicit persistence fails in the fourth edition | 113 |
| GetValue | 122 | Success or data/model error | 123 |
| SetValue | 132 | Success or data/model error | 133 |
| Commit | 142 | Success or 391 | 143 |
| Diagnostics | Available | Available | Available |

This table assumes a valid signature. For nonempty arguments to Initialize, Terminate or Commit, apply the `201` argument rule and preserve state. The underlying model cannot transition on malformed requests. If several defects are present, use the edition conformance fixture precedence. The primary diagnostic identifies a stable machine condition without leaking the score, answers or credentials.

| Code | Adapter result |
| --- | --- |
| `0` | Successful normal call. |
| `101` | General exception outside a more specific code. |
| `102` | Initialization could not complete. The instance remains not initialized. |
| `103` | An Initialize was issued while already running. |
| `104` | Initialize was attempted after a successful Terminate. |
| `111` | General termination failure when no more specific error applies. The instance remains running. |
| `112` | Terminate before Initialize. |
| `113` | Terminate after Terminate. |
| `122` | Read before Initialize. |
| `123` | Read after Terminate. |
| `132` | Write before Initialize. |
| `133` | Write after Terminate. |
| `142` | Commit before Initialize. |
| `143` | Commit after Terminate. |
| `201` | Invalid method arguments that have no more specific defined condition. |
| `301` | General Get failure, including an out-of-bounds packed array index or improper structural keyword. |
| `351` | General Set failure, including sparse writes, forbidden duplicates or immutable identifiers. |
| `391` | Commit failed while running. In the fourth edition, this also applies when Terminate cannot persist the implicit commit, per ADL requirement 5.2.1.1. |
| `401` | Undefined model element. |
| `402` | Defined model element is unimplemented in the selected profile. Required elements cannot be omitted in a conforming edition. |
| `403` | Existing defined element's value has not been initialized. |
| `404` | Write attempted on a read-only leaf or keyword. |
| `405` | Read attempted on a write-only leaf. |
| `406` | Value has the wrong wire type, vocabulary or grammar. |
| `407` | A correctly typed value is outside the declared numeric range. |
| `408` | Required parent identifier, interaction type or other specified dependency is absent. |

## 06.3 Wire types and packed collections

| Wire type | Required behavior |
| --- | --- |
| `characterstring` | Unicode text. Validate and store losslessly, measuring in standard characters rather than UTF-8 byte length. Guard total storage bytes separately. Reject malformed surrogate input at the browser adapter. |
| `localized_string_type` | One optionally language-qualified Unicode value with leading `{lang=<language>}` and text payload. Validate the reserved prefix in its model context, preserve the wire prefix and text, and count the payload against that field's SPM. |
| `language_type` | Edition language-tag grammar, with length SPM where declared. Validate language tags without inferring a learner's identity or changing their institutional locale. |
| `long_identifier_type` | URI-form identifier with SPM 4,000. Preserve identity case, namespace and spelling. Never dereference it. Apply the edition's URI grammar and permit only the profile's opaque identity disclosure. |
| `short_identifier_type` | Short identifier with SPM 250. Apply the edition's restricted grammar and reserved delimiters. Do not split identifiers on unbracketed commas or periods in the 2004 interaction parser. |
| `real(10,7)` | Base-10 real with precision of seven significant digits per RTE §4.1.1.7 and the field-specific range. Keep exact decimal comparisons. Floating point input, decimal lexemes, range checks and permitted precision normalization use the published edition's acceptance rules. Never coerce booleans or null to zero. |
| `time(second,10,0)` | Timestamp using the edition's ISO-8601-derived binding. At least whole-second resolution and support for the edition's required range, including 1970 to 2038. The applicable timestamp binding also allows optional hundredths. Preserve offset when supplied and never substitute duration syntax. |
| `timeinterval(second,10,2)` | Nonnegative period in the edition's ISO-8601 duration syntax, including dates and time components where allowed. Fractional seconds use at most two places under the required profile. Preserve source lexeme and use the published RTE duration accounting rules when aggregating. A month is not interpreted as 30 days by the LMS absent the edition's specified normalization. |
| `state` | Exact case-sensitive vocabulary specified by the element. |
| `count` and `children` | Read-only keywords. Count returns a decimal cardinality string. Children returns a comma-separated list of defined children in stable declaration order. Keyword availability is per model table. |

SPM is the smallest permitted maximum, not a universal prohibition on larger values. Support at least every normative SPM. This implementation uses lossless storage and explicitly documented profile ceilings. When the edition permits acceptance with truncation, the default implementation chooses an explicit Set failure rather than silently losing content if a package exceeds the configured ceiling. Diagnostic reporting can distinguish character limit, collection limit and total job quota. Check each chosen behavior against the edition's conformance requirements.

Collections use zero-based packed indices. For Get, index less than count must resolve to an existing row and may still return `403` for a valid unset field. Index at or beyond count returns `301`. For Set, index less than count addresses the existing row. Index equal to count can create a row only through a permitted field. Index greater than count returns `351`. Required dependencies are checked on the same staged session snapshot as the current write. A failed Set cannot advance `_count`, consume a duplicate identifier or mutate an existing child. Return version, child and count keywords only on defined parents.

Use an edition-aware lexer for indexed and navigation addresses. It recognizes `{target=...}` as a single address component, even if the identifier contains punctuation. Querying a bare collection is not an implicit request for JSON. Parse response delimiters after path parsing, never through a JavaScript object accessor built from untrusted string segments.

### Time parsing and lossless accounting

Parse a time point as a four-digit year with progressively optional month, day, hour, minute, second, fractional second and offset. Accept the normative year range 1970–2038 and preserve the reported precision. Validate calendar dates and leap years. Hours are 00–23, minutes and seconds 00–59, and a fractional part has at most two digits. An offset uses Z or a signed hour with the documented optional minute part. When no offset is supplied, retain local-time semantics. Do not fabricate a UTC timestamp from a bare year or an undated local zone. Keep server receipt time separately.

Parse a time interval as `P[yY][mM][dD][T[hH][nM][s[.ff]S]]`. Require at least one numeric component. Only the seconds may have a fractional part. The date and time M units are different and become unambiguous at the T boundary. A bare P, a bare PT, negative components and more than two fractional digits are invalid. Leading zeros are legal and significant only to the raw representation. Canonicalize day and smaller units exactly into a time component in hundredths of a second. Keep years and calendar months as separate integer components in the durable ledger. Sum like components and never needlessly collapse them into a single total based on an arbitrary assumed month length. Example. `P1M2DT3H` plus `PT45M` is `P1M2DT3H45M`. Where an external attendance rule requires a scalar number of seconds, use the separately recorded wall-clock interval or the approved calendar reference and retain both projections.

## 06.4 Root CMI and scores

**R** denotes read-only, **W** write-only and **RW** both. An **unset** entry produces `403` until a value exists unless a field-specific default or runtime derivation applies. All rows in this section are part of the 4th Edition CMI profile.

| Element | Access | Value, origin and initialization |
| --- | --- | --- |
| `cmi._version` | R | `"1.0"` for the CMI model. |
| `cmi.completion_status` | RW | `completed`, `incomplete`, `not attempted`, `unknown`. Default `unknown`. Read can be derived by threshold in §06.7. |
| `cmi.completion_threshold` | R | Real [0,1] from the edition-appropriate manifest declaration, otherwise unset. |
| `cmi.credit` | R | `credit` or `no-credit`. Default `credit` for an assigned attempt. |
| `cmi.entry` | R | `ab-initio` for a new learner attempt, `resume` for a resumed attempt, or `""` where the edition's context uses neither indication. |
| `cmi.exit` | W | `time-out`, `suspend`, `logout`, `normal`, or `""`. Session default `""`. |
| `cmi.launch_data` | R | Opaque string SPM 4,000. Initialize from the item's `adlcp:dataFromLMS` when supplied. When absent it is unset and Get returns an empty string with error 403. |
| `cmi.learner_id` | R | Long identifier SPM 4,000. Use the authorized package-scoped opaque learner ID. |
| `cmi.learner_name` | R | Localized display value SPM 250. Use only the learner name or pseudonym granted to the package. |
| `cmi.learner_preference._children` | R | `audio_level,language,delivery_speed,audio_captioning`. |
| `cmi.learner_preference.audio_level` | RW | Real at least 0. Default 1. 0 is mute. |
| `cmi.learner_preference.language` | RW | Language type SPM 250, or blank. Default blank. |
| `cmi.learner_preference.delivery_speed` | RW | Real at least 0. Default 1. 0.5 means half reference speed. |
| `cmi.learner_preference.audio_captioning` | RW | `-1`, `0`, `1`. Default `0`, package default. Negative disables and positive enables. |
| `cmi.location` | RW | Opaque string SPM 1,000, unset initially. A zero-length value can be deliberately set. |
| `cmi.max_time_allowed` | R | Time interval from the manifest's attempt absolute duration limit, otherwise unset. |
| `cmi.mode` | R | `browse`, `normal`, `review`. Default `normal`. |
| `cmi.progress_measure` | RW | Real [0,1], unset initially. Zero is distinct from no measure. |
| `cmi.scaled_passing_score` | R | Real [-1,1], set when the primary objective is satisfied by measure. Uses declared `minNormalizedMeasure` or the standard default of 1 for this threshold rule. Otherwise unset. |
| `cmi.score._children` | R | `scaled,raw,min,max`. |
| `cmi.score.scaled` | RW | Real [-1,1], unset initially. Valid negative values remain negative in raw SCORM evidence. |
| `cmi.score.raw` | RW | Real, no generic [0,100] normalization imposed by the CMI model. Unset initially. |
| `cmi.score.min` | RW | Real supplied lower score bound, unset initially. |
| `cmi.score.max` | RW | Real supplied upper score bound, unset initially. |
| `cmi.session_time` | W | Time interval for the current learner session. The latest accepted Set wins. |
| `cmi.success_status` | RW | `passed`, `failed`, `unknown`. Default `unknown`. May be derived by threshold on read. |
| `cmi.suspend_data` | RW | Opaque string, edition SPM in §06.1. Unset initially in 4th Edition. |
| `cmi.time_limit_action` | R | `exit,message`, `continue,message`, `exit,no message`, `continue,no message`. Default `continue,no message` absent item policy. |
| `cmi.total_time` | R | Time interval aggregated within the current learner attempt. Initial zero. Excludes the currently running session. |

Native GradeEvidence validates a separate grade contract. A SCO with raw `32`, min `-8` and max `42` offers a 0.8 normalized fraction under a declared raw-range policy. A SCO reporting scaled `-0.2` remains a valid SCORM result, while an institutional grade item may leave it pending review or use a separately configured transform. Never rewrite SCORM state to match the gradebook. Author-approved scoring policy declares precedence among scaled, raw and raw with supplied bounds. A raw value of zero is real evidence.

## 06.5 Comments, objectives and interactions

| Element | Access | Wire data and cardinality |
| --- | --- | --- |
| `cmi.comments_from_learner._children` | R | `comment,location,timestamp`. |
| `cmi.comments_from_learner._count` | R | Collection SPM 250 rows, default 0. |
| `cmi.comments_from_learner.n.comment` | RW | Localized string SPM 4,000. |
| `cmi.comments_from_learner.n.location` | RW | Characterstring SPM 250. |
| `cmi.comments_from_learner.n.timestamp` | RW | Time point. The learner SCO controls its supplied timestamp. Keep server receipt separately. |
| `cmi.comments_from_lms._children` | R | `comment,location,timestamp`. |
| `cmi.comments_from_lms._count` | R | Collection SPM 100 rows, default 0. |
| `cmi.comments_from_lms.n.comment` | R | Localized string SPM 4,000. |
| `cmi.comments_from_lms.n.location` | R | Characterstring SPM 250. |
| `cmi.comments_from_lms.n.timestamp` | R | Time point, assigned by authorized LMS process. |
| `cmi.objectives._children` | R | `id,score,success_status,completion_status,progress_measure,description`. |
| `cmi.objectives._count` | R | Collection SPM 100 rows. Prepopulate manifest objectives where required by the edition. |
| `cmi.objectives.n.id` | RW | Long identifier SPM 4,000. Set once, unique within this collection. Existing pre-populated identity cannot be replaced. |
| `cmi.objectives.n.score._children` | R | `scaled,raw,min,max`. |
| `cmi.objectives.n.score.scaled` | RW | Real [-1,1], unset initially. |
| `cmi.objectives.n.score.raw` | RW | Real, unset initially. |
| `cmi.objectives.n.score.min` | RW | Real, unset initially. |
| `cmi.objectives.n.score.max` | RW | Real, unset initially. |
| `cmi.objectives.n.success_status` | RW | Same vocabulary as top-level success status. Default `unknown`. |
| `cmi.objectives.n.completion_status` | RW | Same vocabulary as top-level completion status. Default `unknown`. |
| `cmi.objectives.n.progress_measure` | RW | Real [0,1], unset initially. |
| `cmi.objectives.n.description` | RW | Localized string SPM 250. |
| `cmi.interactions._children` | R | `id,type,objectives,timestamp,correct_responses,weighting,learner_response,result,latency,description`. |
| `cmi.interactions._count` | R | Collection SPM 250 rows, initially zero. |
| `cmi.interactions.n.id` | RW | Long identifier SPM 4,000. Required before other leaves. Use ordinal for occurrence identity. Allow a duplicate interaction identifier where the edition permits another presentation. |
| `cmi.interactions.n.type` | RW | `true-false`, `choice`, `fill-in`, `long-fill-in`, `matching`, `performance`, `sequencing`, `likert`, `numeric`, `other`. |
| `cmi.interactions.n.objectives._count` | R | Nested collection SPM 10 rows. |
| `cmi.interactions.n.objectives.m.id` | RW | Long identifier SPM 4,000, unique within this interaction's objective links. It may identify an objective not declared in the top-level objective collection. |
| `cmi.interactions.n.timestamp` | RW | Time point. |
| `cmi.interactions.n.correct_responses._count` | R | Nested collection with type-specific SPM from §06.6. |
| `cmi.interactions.n.correct_responses.m.pattern` | RW | Type-dependent correct response pattern. |
| `cmi.interactions.n.weighting` | RW | Real. The runtime records it and does not recalculate the SCO's score. |
| `cmi.interactions.n.learner_response` | RW | Type-dependent learner response wire string. |
| `cmi.interactions.n.result` | RW | `correct`, `incorrect`, `unanticipated`, `neutral`, or real. |
| `cmi.interactions.n.latency` | RW | Time interval. |
| `cmi.interactions.n.description` | RW | Localized string SPM 250. |

Do not infer a new objective when a SCO stores an interaction's objective identifier. The top-level objective table and per-interaction objective links have separate row identities. If the package revises an allowed leaf, preserve the edit in the accepted mutation journal where retention permits it. Third-party answer keys and response values are excluded from normal event payloads.

A new interaction row is created through its `id`. An interaction response or pattern depends on `type`, which itself depends on `id`. Objectives are similarly identified by a set-once `id`. Satisfy all dependencies before changing the store. When a slot is uninitialized and its parent row exists, return `403` where the edition does not define a default. A packed array append beyond a supported ceiling is `351`, while a lexically invalid input is `406`.

## 06.6 Typed response grammar

The literals `[,]`, `[.]` and `[:]` are tokens, not informal punctuation. `{case_matters=true}` and `{order_matters=false}` are reserved metadata when admitted by the type. `{lang=...}` is parsed only where the grammar admits a localized string. Parse once into typed tokens for validation, retain the original wire value for Get, and never compute learner grades by interpreting a package's pattern as executable code.

| Type | Learner response | Pattern wire shape and minimum supported pattern capacity |
| --- | --- | --- |
| `true-false` | `true` or `false` | Same vocabulary. One pattern at index 0. |
| `choice` | Set of short identifiers with SPM 36 separated by `[,]`. Empty set valid where the learner response binding permits it. Identifiers unique and ordering insignificant. | Same shape. Support at least 10 distinct sets. Reject duplicates including reordered equivalent sets. |
| `fill-in` | Ordered array with SPM 10 localized strings of SPM 250 characters each, delimited by `[,]`. | At least 5 patterns. Each pattern contains one or more localized values. Optional case sensitivity defaults false and optional order sensitivity defaults true. |
| `long-fill-in` | One localized string SPM 4,000. | At least 5 patterns, each one localized string. Optional case sensitivity defaults false. |
| `likert` | One short identifier. | One pattern at index 0. The platform does not impose meaning on the identifier. |
| `matching` | Bag of at least 36 source-target pairs. `[.]` separates the two identifiers and `[,]` separates pairs. Pair order is insignificant. | At least 5 patterns, each a bag of one or more complete pairs. An identifier can recur across pairs. |
| `performance` | Ordered collection of step records with optional step label and optional answer, at least one present. Use `[.]` between label and answer, retaining delimiter for an omitted side. Use `[,]` between records. Answer is a literal SPM 250 or a numeric value. Support at least 250 learner step records. | At least 5 patterns with support for at least 125 step records each. Optional `order_matters` defaults true. A step answer can be a literal or a numeric range. |
| `sequencing` | Ordered array of short identifiers separated by `[,]`, SPM 36. Repetition may be meaningful. | At least 5 distinct ordered arrays. Do not treat permutations as duplicates. |
| `numeric` | One real. | One inclusive range pattern at index 0. `1.9[:]2.1` is bounded. `[:]2.1` has no lower bound, `1.9[:]` has no upper bound, and `[:]` has neither. Equal bounds require the exact value. |
| `other` | Free Unicode characterstring, SPM 4,000. | At least 5 patterns of free Unicode text, SPM 4,000 each, per the 4th Edition RTE requirements. |

Treat collection cardinality rules, duplicate detection and type errors independently. For a valid existing interaction and type, a second numeric correct response row fails `351`. A numeric pattern with nonnumeric bounds fails `406`. A repeated choice set at another row fails `351` after comparing parsed identifier sets. Preserve original data for valid writes and preserve the prior committed value on failure. Obtain exact behaviors for over-SPM and ambiguous delimiters from the edition conformance vectors.

## 06.7 Derived completion and success

Run the following independent function for completion and success on a Get and on the corresponding pinned attempt tracking projection. Store the raw SCO-reported status separately. This project persists derived results as separate versioned evidence instead of replacing the original values.

```text
derive(threshold, measure, explicit_status, meets, misses):
    if threshold is absent:
        return explicit_status if explicitly set else "unknown"
    if measure is absent:
        return "unknown"
    return meets if measure >= threshold else misses

completion = derive(completion_threshold, progress_measure,
                    explicit_completion, "completed", "incomplete")
success = derive(scaled_passing_score, scaled_score,
                 explicit_success, "passed", "failed")
```

| Inputs | Completion | Success |
| --- | --- | --- |
| Threshold 0.80, measure 0.80, scaled passing score 0.75, scaled score 0.74 | Completed on equality | Failed |
| Threshold 0.80, missing measure, explicit completed, passing threshold absent, explicit failed | Unknown under threshold rule | Failed as explicitly set |
| No threshold, measure 1, no explicit completion, passing threshold 0.70 and no scaled score, explicit passed | Unknown | Unknown under threshold rule |
| Threshold 0, measure 0, passing threshold -0.50, scaled score -0.40 | Completed | Passed |

A threshold applies only when the edition's manifest mapping actually initializes it. 4th Edition `completedByMeasure=true` uses the declared or default `minProgressMeasure`. With false the RTE threshold is unset. A legal 3rd Edition text value in a 4th Edition package can be supported through the documented compatibility form when the 4th Edition attributes are absent. Never convert an absent or unset threshold to zero.

## 06.8 Navigation and shared stores

| Element | Access | Values |
| --- | --- | --- |
| `adl.nav.request` | RW | Initially `_none_`. Values are `continue`, `previous`, `exit`, `exitAll`, `abandon`, `abandonAll`, `suspendAll`, or `_none_`. Targeted choice is `{target=item-id}choice`. 4th Edition also supports `{target=item-id}jump`. |
| `adl.nav.request_valid.continue` | R | `true`, `false` or `unknown`. |
| `adl.nav.request_valid.previous` | R | Same tri-state vocabulary. |
| `adl.nav.request_valid.choice.{target=item-id}` | R | Same tri-state vocabulary, evaluated for a particular manifest occurrence. |
| `adl.nav.request_valid.jump.{target=item-id}` | R | Same vocabulary, 4th Edition only. |
| `adl.data._children` | R | `id,store` in the 4th Edition shared-store model. |
| `adl.data._count` | R | Number of declared stores available in the activity context, collection SPM 250. |
| `adl.data.n.id` | R | Declared URI-form store ID, SPM 4,000. |
| `adl.data.n.store` | Conditional R/W | Opaque Unicode string SPM 64,000. Read and write access are independently manifest-gated. Valid unset reads return `403`. |

`adl.nav.request` stages one last valid request for this communication session. It never launches a different SCO during Set. The sequencer consumes a normal exit request after successful Terminate, using current durable tracking state. If `cmi.exit` is `suspend`, it does not process the pending normal navigation request and performs the appropriate suspension procedure. Resume does not replay the old request. Get of request validity is a dry-run against a read snapshot and can be `unknown` when the engine cannot determine it yet. Later state changes require a fresh validation at execution. Start and Resume All belong to the player command boundary and are not write values for `adl.nav.request`.

Build the `adl.data` array from the selected item's declared mappings, preserving manifest order and exact identifiers. A SCO cannot add entries or choose a store by arbitrary path. Reading a write-only mapping is `405` and writing a read-only mapping is `404`. The same internal store may have a different ordinal in a different SCO. Map by scoped store ID, not the ordinal. Process the organization's lifetime declaration for persistence across attempts. The fourth edition default retains the learner's tree store across learner attempts. When `adlcp:sharedDataGlobalToSystem` is false, initialize a new store for the new attempt on the activity tree. Any explicitly approved wider sharing remains scoped to the same learner and Institution and uses a registered scope key. Shared store write locks or version tokens prevent lost updates. A permitted cross-registration reader must receive the current authorized store value. Where the browser adapter cannot maintain that guarantee synchronously, serialize overlapping store access under the authorized scope or hold that package outside the tested strict profile. Never reuse one learner's shared store in another learner's launch.

## 06.9 Persistence and launch policy

A PackageRegistration pins an immutable PackageVersion and CourseOffering placement. The sequencing engine creates a PackageActivityAttempt for a new learner attempt. Each PackageLaunchSession binds to exactly one occurrence and attempt. Resume attaches to an existing suspended attempt and reconstructs the running read cache from authorized durable state. A fresh activity attempt within the same registration starts with edition defaults. Its PackageScoState is keyed by activity attempt, so a prior attempt at the same manifest occurrence remains historical. Review and browse use distinct non-credit attempts and working snapshots. A package cannot use `cmi.mode` writes to obtain credit or change review policy.

Close one communication session at most once. Verify the final monotonic commit batch before posting the last session duration and before evaluating downstream navigation. The successful persistence watermark binds to session, activity attempt, revision and exact mutation sequence. The pending navigation request is session state and is never copied into a fresh session. A lost response can be replayed and receives the same result. A stale token cannot clear a newer launch, increase seat time or publish grades. Use [the player durability design](08-scorm-player-security-and-durability.md) for how synchronous calls cross an asynchronous storage boundary.

On navigation away without a final SCO call, take the last accepted session interval that is present in the durable journal and mark the session outcome with the real disconnect or abandonment cause. Do not infer a submitted exam, successful Terminate or a new completed result from a tab closing. Add the time delta once even if several close signals arrive. Keep official elapsed time, SCO-reported time and browser diagnostics separate.

## 06.10 Verification traces

| Trace | Inputs and ordered calls | Observable outcome |
| --- | --- | --- |
| R04-001 | Before Initialize, Get `cmi.mode`, Set `cmi.location`, Commit and Terminate. Then Initialize twice. Finish with Terminate, then Get, Set and Commit. | Codes 122, 132, 142, 112, then 0 and 103, then 0, 123, 133 and 143. All normal successful returns are strings. |
| R04-002 | In a running fresh 4th Edition attempt, read location, set location to blank, read again. Attempt to read session time and set total time. | First empty read gives 403. Second gives 0 with exactly the same empty string. The W and R violations give 405 and 404. |
| R04-003 | Set row 0 learner response before ID, then set ID, try response before type, set type numeric, write response `1.95` and pattern `1.9[:]2.1`. Try pattern index 1. | Both missing dependencies produce 408. Successful valid fields round-trip. Additional numeric pattern produces 351 and leaves the correct-response count at 1. |
| R04-004 | Set row 2 when count is 1. Try unknown `cmi.foobar`. Set scaled score `"nan"`, then `"1.001"`. | Returns false and codes 351, 401, 406 and 407 respectively, with no mutation or ghost collection entry. |
| R04-005 | With completion threshold 0.80 and progress 0.80, explicit incomplete, passing score 0.75, scaled score 0.74 and explicit passed, read statuses. | Read completed and failed, while raw explicit states remain separately available for authorized audit. |
| R04-006 | Stage `{target=next}choice`, set exit `suspend`, commit and terminate. | Persist current SCO state, suspend the tree as appropriate, ignore pending normal choice, and restore current occurrence on a permitted resume. |
| R04-007 | Two SCOs map the same declared store with different ordinals. First writes under manifest permission, second has read-only access, third learner has its own launch. | Second sees value by store identity and cannot write. Third cannot read first learner's store. |
| R04-008 | Submit a valid 4,001-character suspend value under each edition's default guaranteed envelope. Submit a valid 64,000-character value in 3rd and 4th Edition. | 3rd and 4th Edition support the full 64,000. A 2nd Edition profile may explicitly reject a value above its published 4,000 SPM. It never silently claims the same profile. |
| R04-009 | Send accepted session times `PT30.50S` and `PT1M4.25S` with duplicate commits, terminate, resume and close after `PT15.75S`. | After first close total is 64.25 seconds, after second total is 80.00 seconds. Commit retransmission adds no time. |
| R04-010 | Force a transient storage outage during Commit and Terminate. Retry with the exact sequence after recovery. | Codes 391 and 111 until storage recovers. Communication stays running and only one terminal receipt and time delta are persisted. |

### Browser SCO interaction probe

Invoke this function with the API instance found by the synthetic 4th Edition SCO. Run it against an empty attempt with no configured completion or passing threshold. A harness sets up the authorized session and checks the persisted interaction after Terminate. The test contains no production answer material.

```javascript
function runScorm2004InteractionProbe(api) {
  function expect(method, args, result, code) {
    const actual = api[method](...args);
    const lastError = api.GetLastError();
    if (actual !== result || lastError !== code) {
      throw new Error(`${method} returned ${String(actual)} with error ${lastError}`);
    }
  }

  expect("Commit", [""], "false", "142");
  expect("Initialize", [""], "true", "0");
  expect("GetValue", ["cmi._version"], "1.0", "0");
  expect("GetValue", ["cmi.interactions._count"], "0", "0");
  expect("SetValue", ["cmi.interactions.0.learner_response", "1.95"], "false", "408");
  expect("SetValue", ["cmi.interactions.0.id", "urn:fixture:measurement"], "true", "0");
  expect("SetValue", ["cmi.interactions.0.type", "numeric"], "true", "0");
  expect("SetValue", ["cmi.interactions.0.correct_responses.0.pattern", "1.9[:]2.1"], "true", "0");
  expect("SetValue", ["cmi.interactions.0.correct_responses.1.pattern", "1.8[:]2.2"], "false", "351");
  expect("SetValue", ["cmi.interactions.0.learner_response", "1.95"], "true", "0");
  expect("GetValue", ["cmi.interactions.0.learner_response"], "1.95", "0");
  expect("SetValue", ["cmi.interactions.0.result", "correct"], "true", "0");
  expect("SetValue", ["cmi.completion_status", "completed"], "true", "0");
  expect("Terminate", [""], "true", "0");
  expect("Commit", [""], "false", "143");
  return "SCORM 2004 interaction probe passed";
}
```

## 06.11 Normative references

- [ADL SCORM 2004 4th Edition Run-Time Environment v1.1, archived text](https://www.scribd.com/document/39419891/SCORM-2004-4ED-v1-1-RTE-20090814)
- [ADL SCORM 2004 4th Edition Testing Requirements](https://adlnet.gov/assets/uploads/SCORM_2004_4ED_v1_1_TR_20090814.pdf)
- [ADL SCORM 2004 3rd Edition Run-Time Environment, archived copy](https://lms.technology/for/scorm/2004/3rd_edition/standards/SCORM_RunTimeEnv.pdf)
- [ISO/IEC TR 29163-3, 3rd Edition Run-Time Environment v1.1](https://webstore.iec.ch/en/publication/11388)
- [SCORM 2004 2nd Edition archived books and addenda](https://lms.technology/SCORM20042_index.html)
- [ADL SCORM 2004 4th Edition conformance test suite](https://github.com/adlnet/SCORM-2004-4ed-Test-Suite)
