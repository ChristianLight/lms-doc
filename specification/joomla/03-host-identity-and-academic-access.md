# Host identity and academic access

## Joomla identity mapping

A Joomla user account supplies authentication and host session identity. Map its local user ID, serialized as the stable provider subject within the Joomla identity connection, to a Principal through ExternalIdentity. A Principal can be associated with the institutional Person used by the LMS. Preserve the distinction because a person can have multiple authentication providers and an account can act in several institutional contexts. Service principals use separately managed credentials and have no implicit learner identity.

Account linking requires an authenticated provider subject or an approved administrative identity decision. Do not merge records on matching display names or email alone. When a host account is blocked, deny new LMS actions and invalidate active grants under the platform's session policy. Preserve authorized historical academic records under their retention rules. Deleting the host account triggers a reviewed unlink/anonymization workflow and cannot cascade through grades or issued reports.

## Access decision

The application first checks the applicable Joomla action permission and then the domain's academic scope and state. For a teacher editing an offering schedule, the decision includes the authenticated principal, institution, requested action, active teaching assignment, offering or section scope, policy and expected revision. A teacher's membership in a general Teachers group does not identify which class they teach.

Joomla's asset rules provide inherited allow/deny actions, and extensions must call the authorization API. Site-wide Super Users have unrestricted host privileges. That role is a trusted operational boundary with access to the installation and its data. Academic separation governs ordinary application roles and audited operational procedures, and cannot provide secrecy from an administrator controlling the host or database. [Joomla permissions](https://manual.joomla.org/docs/next/general-concepts/acl/acl-permissions/)

| Joomla capability | Academic check that still applies |
| --- | --- |
| Access the component administration interface | Institution and staff scope for every listed row |
| Create an ordinary record | Allowed parent, institutional boundary, valid lifecycle and field allowlist |
| Edit a record | Owner revision, active assignment, editable fields and state |
| Configure component options | Operational configuration rights, separate educational record permissions |
| View a site page | Enrollment, publication, prerequisites, release window and record visibility |
| Download an asset | Authorized context, immutable version and applicable retention/access policy |
| Run an export | Approved purpose, population scope, data classification and download-time permission |

## Role templates

Create narrowly scoped role templates for learner, guardian/observer, teacher, teaching assistant, author, publisher, examiner, marker, moderator, registrar, institution administrator and auditor. A template lists available permissions. An assignment binds a principal to an effective scope and interval. Institutions can narrow these templates or create a local role through an authorized policy version.

Avoid one Joomla group per learner, offering or question bank. Use host groups for coarse capabilities and application grants for the potentially large academic scope graph. This keeps host group administration comprehensible and lets enrollment changes affect the relevant course without modifying unrelated site permissions.

Staff front-end workspaces use the same authorization rules as administrator workspaces. A marker can receive a queue and a blind script view without access to full student profiles. A guardian can review a specifically permitted learner record without receiving teacher or registrar capabilities. Preview permissions are separate from enrollment and generate synthetic progress only.

## Session and anti-forgery rules

Use the host's session lifecycle and anti-forgery token checks for authenticated browser mutations. The LMS command still checks actor scope and object state after token validation. GET requests do not mutate academic state. Authenticated webservice requests use an approved token mechanism mapped to a service or human principal and a declared API scope.

Long-running exam state belongs to the assessment attempt and its server deadlines. It does not reside only in PHP session memory. When authentication expires, preserve accepted responses and restore the permitted attempt after reauthentication under the same learner identity. An authentication refresh cannot reset the timer, create an additional attempt or change the captured question variant.

Cache authorization decisions only with a revocable scope/version key and short documented lifetime. Changes to block status, teaching assignments, enrollment, answer-release policy or role grants invalidate the applicable cache. Sensitive commands re-check current authoritative state even when the page was rendered earlier.

## Routes and identifiers

Routes may use human-readable aliases for navigation but resolve the immutable GUID through its owner. A route includes or derives the offering context where the same activity appears more than once. The domain validates that the placement belongs to the learner's effective release. A deep link never bypasses the course access decision.

Register component routers through the supported extension service provider mechanism. Keep canonical URL generation in one owner route contract, including links used by exports, notifications and imported content rewriting. A renamed course title changes its display alias without changing the underlying record identity. [Component routers](https://manual.joomla.org/docs/next/general-concepts/routing/access-component-router-class/)

## Permission acceptance

Test direct links and raw requests in addition to hidden buttons. A denied user should receive no answer key, private file URL or unposted score in page source, embedded JSON, autocomplete results, export downloads or cached fragments. Test teacher access across two sections, staff access across institutions, former enrollment access, delegated marking and revocation during an open session. Verify that a server-rendered form cannot submit fields beyond the command's allowlist by adding them manually.
