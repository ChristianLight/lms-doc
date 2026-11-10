# 01. Offerings, sections and academic calendars

An offering runs a single course in a named institutional context. Sections are instructional rosters sharing that offering. Multiple campuses may share approved material through separate offerings. Cross-listing preserves section-specific scope and aliases while learners continue to hold one enrollment in the shared offering.

## Records and boundaries

| Record | Required ownership and relationships | Defaults and invariants |
| --- | --- | --- |
| AcademicPeriod | Institution, optional parent period, code, label, named zone, local date bounds | Child is within parent. Hierarchy acyclic. Unique normalized code within institution |
| CourseOffering | Institution, owning unit, course, period, code, current default course version, zone, mode, state, revision | Course belongs to the institution. Version belongs to course and is published. Unique institution, period and normalized code |
| Section | Offering, section code, title, scope, optional capacity and local zone, state and revision | Unique offering plus normalized code. If capacity absent the section has no lower independent cap |
| LearningGroup | Offering, optional restricting section, code, purpose, membership mode, capacity, state and revision | Unique offering plus normalized code. Default manual managed. Closed group accepts no new members |
| Cohort | Institution, owner unit, code, membership policy and state | Unique institution plus normalized code. Can be used by multiple offerings through explicit roster source grants |
| SectionMembership | Enrollment, Section, effective interval, source and primary flag | Offering IDs must match. Half-open intervals for each pair do not overlap. At most one active primary section |
| GroupMembership | Enrollment, LearningGroup, effective interval and source | Offering IDs must match. A section-restricted group requires active membership in its section |
| CohortMembership | Person, Cohort, effective interval, provenance | Person and cohort belong to the institution. Retain closed intervals for authorization and history |
| Teaching assignment | Principal, role and scope through RoleAssignment, interval and grant provenance | Teacher and assistant grants are separate from learner enrollment and use a named offering, section or group |

Mode is self_paced, teacher_led or blended. Offering states are draft, scheduled, active, closed, archived and cancelled. Scheduling requires a published course, initial calendar revision, authorized owner and capacity policy. Activation additionally requires a valid timetable and teacher role for teacher-led and blended modes. A self-paced offering can activate without section rosters. Close stops new learning and submission unless a published review or explicit extension policy applies. Archive restricts ordinary delivery surfaces and retains academic access through authorized history. Cancel requires a reason and prevents new admissions, submissions and sessions. An offering with valid academic evidence is never physically deleted as a routine closure.

Changes to an active offering are split into explicit metadata, calendar, default publication, scope and state actions. Mutations check the current offering or schedule revision. A transition verifies downstream work and returns a reviewable warning when closing affects active sessions. The default cancels new starts but preserves previously started attempts through their approved effective deadlines. An emergency suspend may deny all activity under a separate capability and recorded reason.

## Calendar semantics

Academic periods describe institutional reporting. Dates use a named IANA zone and local calendar days. Convert local dates to inclusive start and exclusive next-day end instants when enforcing time windows. A calendar revision contains opening, closing, recommended date, due, grace, access and review fields as applicable. Do not derive grade lateness from the end of an academic period. At rollover, close prior admissions and create new offering calendars with their own releases and unique identities.

| Schedule field | Meaning and default |
| --- | --- |
| enroll_open_at | Earliest normal application or admission instant. Null means no lower bound |
| enroll_close_at | Exclusive cutoff for normal applications. Null means no upper bound until offering closure |
| learn_open_at and learn_close_at | Half-open offering-wide participation access. Open can default to activation. End can remain null for evergreen delivery |
| review_open_at and review_close_at | Released-work review independent of new starts. Default opens when results release and remains through authorized records retention |
| registration hold | Explicit controlled enrollment restriction with reason and start/end. Personnel with registrar override can resolve |
| meeting occurrence | Concrete scheduled event with UTC instants, source local wall time and named zone, separately controlled attendance scope |

For an instant submitted as local wall time, reject nonexistent spring-forward times with 422 LOCAL_TIME_GAP and the next valid minute. Ambiguous repeated time requires the chosen UTC offset and stores both candidates in diagnostics. For a relative days policy, use local calendar days and the offering's named zone. If a computed time falls in a gap, choose the first valid minute after it and emit a schedule warning. If ambiguous, choose the later occurrence for deadlines and the earlier for release. This convention keeps planned access windows from shrinking silently. Store the resolved instant and time-zone database version for an issued schedule or attempt. Convert for display with both learner-preferred and authoritative local time where they differ.

Recurring meetings use stable series ID, ordinal or source recurrence ID, series generation revision and explicit exclusions. Materialize the next 120 days or through the series end, whichever comes first. A unique key on series and original occurrence prevents duplicate materialization. Editing one occurrence creates an exception without altering its ID. Editing all future occurrences preserves historical attendance, updates or cancels future materialized rows with revision history, and emits calendar updates. Export [iCalendar](https://www.rfc-editor.org/rfc/rfc5545) with stable UID, sequence and timezone-aware event representations.

## Operating examples

- Two sections share a course offering with capacity 60 and capacity 30 each. The first enrolled student gets the offering release and Section A membership. Moving them to Section B frees A's seat and consumes B's seat without touching the offering seat.
- An evergreen course has no learning close. Activating on November 10 at 09:00 local permits enrollment-relative dates on November 10 and later. An offering-wide mandatory final cutoff can still be added by reviewed calendar revision for future start.
- A local 02:30 appointment on 2026-03-08 in America/New_York is invalid because the local clock jumps forward. The API returns a gap and proposes 03:00. A manually entered 01:30 on 2026-11-01 requires either offset −04:00 or −05:00.
