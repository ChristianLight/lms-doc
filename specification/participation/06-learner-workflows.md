# 06. Learner workflow and screen contracts

## From catalog to learning

| Screen | Required state and content | Main actions and authority | Edge states |
| --- | --- | --- | --- |
| Course catalog | Published title, short summary, mode, duration, language, eligibility summary and catalog-approved preview | Browse, filter, open detail, optionally follow | Offering eligibility and visibility evaluated separately from public catalog listing |
| Offering detail | Admission state, scoped application route, timetable zone, dates, accessible participation summary and fees if used | Apply, accept, withdraw application and check waitlist status | Shows next action for pending, waitlisted, full, declined, active or closed. Never exposes other applicants |
| My learning | Active, upcoming and history views, pending review, next action, progress labels and deadlines | Resume, open calendar, read announcements, review released results | A closed offering can show history with no new start controls. Inaccessible offerings are filtered |
| Course player | Outline, current lesson, placement resource controls, exact access state and course-local time | Navigate previous/next, open allowed activity, bookmark, acknowledge, resume | Locked titles use safe explanations. Hidden locations remain absent. Provider failure shows authorized alternatives |
| Activity panel | Learner instructions, start eligibility, submission state and announced timing or review | Start or resume, submit via owning runtime, request accommodation route, open accepted result | Distinguish saving, accepted, pending evaluation, released, returned and expired |
| Review center | Released scores and feedback, approved attempt review, file and rubric access, deadlines for appeals | Read, download allowed evidence, ask for clarification or initiate review | No key or result leaks before release. Historical version shown when relevant |
| Calendar and collaboration | Authorized meetings, date changes, zone, room or document links | Subscribe, join, select participation alternative, read own attendance | Calendar tokens expire or can be revoked. Closed rooms may retain authorized records links |

## Navigation and resume algorithm

Use the effective enrollment release and ordered placements. Build the next and previous list from authorized visible lessons and designated standalone activities. Locked visible entries can be navigated to a safe explanation. Prefer the next currently actionable required placement for the dashboard rather than the next physically ordered locked item. If several are due, rank overdue required actions first, then upcoming required deadlines, then outline order. Optional recommendations never displace an urgent mandatory action.

The current resume record holds exact placement ID, stable key, anchor, locale, media position where applicable, session sequence, source instant, and revision. Default use the latest accepted action from the current session or explicit learner resume choice. Multiple sessions use a compare-and-swap server revision. An old offline session can receive conflict detail and keep its local checkpoint as a selectable alternative. It cannot override an accepted newer position implicitly. Resume locates the current equivalent key after a release change. If no authorized equivalent exists, offer the nearest authorized prior or next item and label the change.

Bookmarks are learner-private and are keyed by offering, stable placement and anchor. They remain listed when the former content is inaccessible, with a generic unavailable status and the ability to remove them. Saved personal labels should not be interpreted as course content, used as evidence or exposed to staff by default.

## Reliability and accessibility

- Render controls with accessible names, keyboard order, visible focus, semantic headings and localizable error text. Announce important state transitions through a polite live region. Avoid forced focus changes on ordinary save.
- Save action state and receipts distinguish device-local pending changes from server-accepted writes. On reconnect, retry stable command IDs and use authoritative result. A browser must never infer completion from its cached form state.
- At a deadline, continue to show the authoritative timer and original time zone. A rejected late submit explains the applicable window and routes to support if permitted. It preserves any eligible recoverable draft under policy.
- Use captions, transcript and accessible media controls where available. Offer documented alternative completion routes without forcing disclosure of a learner's accommodation to classmates.
- Use coarse mobile-friendly outline navigation with keyboard-compatible search. An offline mode can cache permitted reading resources where policy allows, with short-lived authorization and revocation. Consequential submissions and attempts depend on authoritative time and acceptance.

## Learner acceptance sequence

A student follows a course without enrolling and can read only its permitted preview. The student then accepts a waitlist offer and receives the same enrollment and course release after refreshing the confirmation. The first lesson is visible. Its required check-in is scheduled for later and produces a safe locked explanation. After reading the lesson, the student marks it complete twice while one request retries. The course shows one receipt and updates progress once. The student starts a separate quiz, reconnects, resumes the pinned quiz version and later sees only released feedback. An authorized move to another section changes future meeting and due dates. The prior attempt and its applicable dates are still available to the student through the released review view.
