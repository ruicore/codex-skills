# Editorial Workflow

Use when authoring or restructuring a technical document for Feishu. Choose depth by
the reader's task, while keeping the same facts and authorial position.

## Contents

1. Evidence and source boundaries
2. Review design
3. Implementation document
4. Mixed audiences and paired documents
5. Author voice
6. Visual structure
7. Completion checks

## 1. Evidence and source boundaries

Separate these before drafting; a compact local note is enough when the sources are complex.

| Source material | Treatment |
| --- | --- |
| Goal or selection criterion | Retain the reason for choosing the approach, separately from its feature scope |
| Confirmed design decision | State the intended behavior directly |
| Current implementation or runtime evidence | Describe only the behavior and scope actually established |
| Required constraint | Keep visible where it affects the design |
| Unresolved choice or untested assumption | State the uncertainty and its consequence; use `待定` when deliberately deferred |
| Example or suggested value | Keep its illustrative status; do not turn it into a fixed requirement |
| Rejected option | Include only when its tradeoff helps the current decision |
| Discussion or publishing instructions | Keep outside the reader-facing article |

Current code establishes current behavior; it does not invalidate an explicitly
proposed future change. A design decision does not prove implementation or acceptance.
Resolve conflicting sources before publication rather than silently mixing them.

When compressing or splitting substantial source material, make a short local
coverage note for the goals and constraints whose loss would change the proposal
or its implementation. Map each to its destination, an intentional omission with
reason, or an unresolved conflict. Use only the consequential items; a small edit
does not need a separate matrix. Recheck this note against the finished drafts,
not only their outlines. A feature list does not substitute for selection goals.

Keep a maintainable reader-facing local source, generated publication package and
publish result. A source hash or inventory describes that version only. Synchronize
cloud refinements back to the local source before later republication.

## 2. Review design / 评审稿

The main path lets a reviewer judge whether to adopt the proposal and what must be
resolved before committing to it. Lead with the proposed behavior and the problem it
addresses. Include background only to the extent needed to understand that choice.

Useful groupings are goals and scope, selected approach, architecture and key
decisions, then acceptance and open risks. Adapt them to the article; do not require
every heading or create a chapter for every implementation concern.

### Choose what stays

| Reader's question | Keep in the review path | Place in implementation detail when it does not change the decision |
| --- | --- | --- |
| What changes for users? | Main behavior, scope and important constraints | Screen-by-screen instructions |
| Why this approach? | Material alternatives, reason for selection and evidence limits | Discarded experiments and conversation history |
| How does it work? | Ownership, system boundaries, authoritative data and main flow | Complete endpoint, field, file and port inventories |
| Can it work at the required scale? | Dependencies, resource assumptions, limiting factors and validation needed | Exact tuning knobs and deployment commands |
| What happens when it fails? | Consequential loss, isolation, recovery and completion guarantees | Every retry branch and cleanup operation |
| What still needs a decision? | Unresolved choice, consequence and next evidence needed | Routine implementation choices left to the implementer |

Names such as a protocol, storage mechanism or resource policy belong in the main
path when they materially affect feasibility or risk. Do not remove them merely
because they are technical. Conversely, avoid moving a complete contract into the
review body just to prove that implementation has been considered.

Combine related mechanisms into concise implementation highlights. Use keywords for
routine steps; explain the choices and failure boundaries that matter. Preserve a
requested complete architecture diagram as a navigational reference, even when long.

### Make open risks useful

Distinguish an undecided design choice from a test still needed. State the affected
outcome and what would resolve it; give a recommendation or owner when supported.
Do not invent owners, dates, benchmark targets or a settled choice. Avoid an exhaustive
risk checklist unrelated to this proposal.

An unfinished implementation item is not automatically a review decision. A missing
endpoint path, response field or internal tuning value usually belongs with the
implementation owner. Escalate it into the review path only when it changes the
proposal, requires cross-team agreement, or creates a material feasibility or release
risk. Do not copy the implementation document's entire unresolved-items inventory
into a review risk table; summarize the consequence and link to the detailed work.

A proof of concept supports only what it exercised. Lower bandwidth, higher capacity,
lower latency or production readiness remain hypotheses until the relevant comparison
or acceptance evidence exists. Include a meaningful validation direction when exact
targets remain open, rather than inventing numbers.

## 3. Implementation document / 执行稿

Start with concise positioning and the agreed design, then organize detail by the
work an implementer must complete. Preserve the precision needed to build and verify
it; removing ports, configuration or failure semantics merely to shorten this mode
can make it unusable.

Include the applicable contracts, not a universal inventory:

- Component responsibilities, inputs, outputs and the authoritative state.
- Interface or configuration mappings where known: direction, purpose, required
  values, ownership and compatibility. Distinguish examples from fixed requirements.
- Preconditions, lifecycle, readiness, completion and resource ownership.
- Failure effects, recovery boundaries and cleanup that matter to correct operation.
- Observable verification and remaining decisions that block execution.

Match the precision to the assignment. An implementation design may leave wire
schemas unresolved and identify that dependency. An operational runbook needs known
commands, environment preconditions and expected results. Do not fabricate commands
or turn a design proposal into an apparently verified runbook.

Use tables for exact mappings and a sequence or state diagram for critical transitions.
Keep long schemas and exhaustive examples in a linked detail section. Do not replace
essential contracts with vague phrases such as “handle appropriately” or “ensure
reliability.” Separate request receipt from business completion where they differ.

Preserve established authorization, ownership, data movement and completion boundaries
when shortening an integration description. “Reuse the existing service” may replace
routine API detail, but not the known division of responsibility. Keep only the
undecided portion marked as unresolved rather than deferring an entire known contract.

## 4. Mixed audiences and paired documents

For a single mixed-audience page, keep a review path first and place implementation
references after it. Do not force both readers through the full detail inventory.
Keep authorization limited to the pages and sections the user requested.

When separate review and implementation pages exist:

- Let each page stand on its own for its reader, with a link explaining what the
  companion covers. Link to specific sections when that helps navigation.
- Preserve the same terminology, boundaries, decisions and implementation status.
  Keep each detailed contract authoritative in one place rather than copying it all.
- Before simplifying, check which unresolved technical items affect feasibility,
  capacity, data loss, safety or rollout. Those still need a concise review-level
  statement; a link to a detail article does not make a buried decision visible.
- Reconcile changes that affect both pages within the authorized scope. If one page
  is read-only, record the inconsistency and required update rather than editing it.

Do not assume the supplied articles are perfect templates or that all their prose
was written by the user. Extract useful structural choices and follow explicit voice
preferences without attributing collaborative or generated text to the user.

## 5. Author voice

Write the artifact as its author, from the user's position. Prefer concrete component
subjects; use `我们` naturally for a team decision when it fits. Do not force every
sentence into first person or impersonate another named person.

| Process-oriented wording | Author-facing replacement |
| --- | --- |
| 按你的要求，我会把方案调整为…… | State the selected design directly |
| 我们刚才确认了…… | State the current decision and its scope |
| 同事的示例说明…… | Identify relevant evidence or an attributable source when needed |
| 为了让审核者理解，下面介绍…… | Explain the relationship directly |
| Codex 已验证…… | Give the verified result and its limits; keep tool provenance in the local record when irrelevant |

Preserve necessary citations and actual collaborator ownership. Remove the process
story, not credit, uncertainty or evidence. Never claim that the author personally
performed an action that was not established.

Use conclusion-first, concrete sentences and short paragraphs. Split distinct ideas
with paragraph breaks; use lists for parallel items. Avoid generic claims of being
robust, flexible or scalable without explaining the relevant mechanism or limit.
Give each rule one primary expression rather than repeating it in an opening,
Callout, diagram, table and conclusion. Do not add sections just to fill a template.

## 6. Visual structure

Choose the visual from the question it answers, then choose the Feishu component.

| Question | Useful form |
| --- | --- |
| How do the candidate approaches differ? | Aligned comparison lanes or a short comparison table |
| Where does data originate, and who handles it? | Architecture/data-flow diagram with labeled boundaries and arrows |
| In what order does a critical interaction occur? | Sequence or short flow diagram |
| What can this object become? | State diagram with meaningful transition labels |
| Which exact value maps to which behavior? | Native table |
| What needs attention or a decision? | Short risk/decision paragraph or Callout |

Keep diagram labels concise and put supporting explanation next to the diagram.
Use a consistent reading direction, normally top to bottom for flows, with aligned
layers, parallel peers and visible ownership boundaries. Distinguish control flow
from data flow when both exist. Check arrow direction and labels, not just appearance.

A summary diagram, focused interaction and full reference architecture can coexist
when they answer different questions. Avoid drawing the same chain repeatedly.
When the difficult relationship is parallel actors, an ownership handoff or recovery,
show that relationship rather than adding another linear success path. Conversely,
an exact mapping can remain a table; diagram quantity is not a coverage measure.
Keep wide diagrams full-width; do not force a complete reference architecture into a
small summary card or split it without a reading path.

Match editability to the collaboration need. A rendered DSL diagram is suitable
when discussion targets the whole diagram. For per-component comments or edits,
use independent native shapes, text and connectors. A Board containing a single
image or grouped render is insufficient. Preserve a local semantic diagram source
and check actual single-component interaction before calling it editable.

## 7. Completion checks

Read the draft without the chat history and use the checks for its selected mode:

| Review design | Implementation document |
| --- | --- |
| Can the reader explain the proposal and why it is chosen? | Can the reader locate the responsibilities and contracts needed for the assigned work? |
| Are consequential constraints, assumptions and open decisions visible? | Are preconditions, lifecycle, failure behavior and completion distinguishable? |
| Can feasibility and the required validation be assessed without opening a field inventory? | Are the available mappings precise enough, and are blocking unknowns explicit? |
| Does each visual make a relationship easier to judge? | Can behavior be verified without interpreting a chat transcript? |

For either mode, check author voice, evidence limits, contradictions across related
documents, protected sections and requested diagrams. Reconcile the consequential
source items with their actual locations, and confirm that shortening did not turn
an established boundary into an unspecified implementation detail. Fix content before freezing
the publication package. Publication save/reload checks remain a separate requirement;
good prose does not prove a successful cloud edit.
