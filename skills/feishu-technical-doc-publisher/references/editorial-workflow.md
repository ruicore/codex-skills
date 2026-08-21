# Editorial Workflow

Use this reference before changing the Feishu page when the local source was produced through an extended design discussion or contains implementation-first detail.

## Contents

1. Evidence and decision model
2. Publication artifact model
3. Reader-first narrative
4. Discussion-to-document cleanup
5. Section and visual selection
6. No-context reader review

## 1. Evidence And Decision Model

Build a compact source map before rewriting:

| Class | Meaning | Publication treatment |
| --- | --- | --- |
| Settled decision | The current design contract | State directly and consistently |
| Evidence | Code, schema, runtime behavior, or authoritative product fact | Use to support the decision; do not overclaim beyond it |
| Constraint | Required boundary, compatibility rule, or non-goal | Make visible near the affected flow |
| Unresolved item | A real design choice that remains open | Mark `待定` or place in a clearly named open-items section |
| Rejected alternative | A discarded design considered during discussion | Omit unless the rejection is essential for review or prevents a likely regression |
| Editorial/process note | Instructions about PlantUML, paste order, local paths, or reviewer workflow | Keep only in the local publication package |

When sources conflict, prefer current code/specification and user-confirmed decisions over older drafts. Do not silently merge incompatible versions.

## 2. Publication Artifact Model

Keep these layers distinct:

1. **Authoritative source**: complete local design facts, detailed schemas, evidence, and unresolved questions.
2. **Reader-facing draft**: the complete external narrative, plus local-only diagram fences and insertion notes.
3. **Publish package**: Markdown/HTML optimized for rich-text paste, extracted PlantUML files, and a machine-readable manifest.
4. **Feishu page**: native blocks and final visual layout.
5. **Publish result**: URL, timestamp, source hash, validation, and deferred items.

Cloud-only corrections must be synchronized back to the reader-facing draft. Generated Markdown/HTML can be regenerated; they are not authoritative.

## 3. Reader-First Narrative

The exact outline should follow the document, but a technical design usually reads well in this order:

1. Background: current behavior, missing capability, and why the change matters.
2. Proposal overview: what will change and the central behavior.
3. Goals, scope, non-goals, and current status.
4. Key design decisions and an architecture/data-flow overview.
5. End-to-end flow and the important decision matrix.
6. Ownership and component responsibilities.
7. Configuration/domain/data model.
8. Interfaces and contracts, if settled.
9. Failure behavior, migration or phases, implementation order, and acceptance.
10. Large schemas, payloads, and directories in appendices or sub-documents.

Do not begin with a database table or a multi-page JSON schema unless that is the document's explicit purpose. Each complex section should open with a short orienting paragraph that states its result, without naming it “一句话结论”.

### Choose A Publication Emphasis

Use the reader and review purpose to choose emphasis before selecting Feishu components:

| Emphasis | Lead with | Supporting detail |
| --- | --- | --- |
| General reader narrative | Background, proposal, central product behavior | One or two orientation visuals, then responsibilities and model |
| Architecture review | Concise background, system boundary, data flow | Execution decisions, ownership, trust boundaries, phases |
| Implementation contract | Concise positioning, behavior matrix, authoritative contracts | Payloads, fields, failure semantics, implementation order, acceptance |
| Mixed publication | General-reader narrative as the main path | A small architecture visual set plus contract sections after the flow |

These are editorial emphases, not reasons to create multiple cloud documents. Create separate reader, architecture, or contract views only when the user asks for distinct deliverables or when the audiences truly require different maintenance surfaces.

## 4. Discussion-To-Document Cleanup

Remove wording that assumes the reader attended the design conversation.

| Discussion wording | Reader-facing treatment |
| --- | --- |
| 一句话结论 | 方案概述、结论，或 direct prose without a meta-label |
| 已确认的关键决策 | 关键设计决策 |
| 为什么不是维护 60 份配置 | State the chosen creation/versioning rule without the oral estimate |
| 现有表最小扩展 | 现有表扩展 |
| 本方案不是……而是…… | State the positive capability and scope directly |
| 这里不再拆分…… | Describe the final result semantics only |
| （PlantUML）/【图：……】 | Remove from the public page; keep diagram DSL/insertion notes locally |
| rejected field/table names | Remove unless the rejection itself is an externally reviewed constraint |

Also check for:

- references to “we discussed”, “as agreed”, “the previous version”, or chat turns;
- local drive paths and private wiki/task URLs not intended for readers;
- placeholder counts, temporary names, and speculative implementation details;
- duplicate rules repeated in summaries, matrices, failure tables, and acceptance criteria;
- blank headings, list items, or table cells created by text deletion;
- headings with manual numeric prefixes.

When a user explicitly asks to leave a section undecided, keep the heading and write only `待定`. Do not infer an API or data contract from adjacent discussion.

## 5. Section And Visual Selection

Use the smallest visual that materially improves understanding:

| Relationship | Preferred form |
| --- | --- |
| System ownership, data flow, sequence, state, or ER | Full-width PlantUML/UML Board |
| Exact field, status, phase, or responsibility comparison | Native table |
| Two short parallel responsibilities or product modes | Two columns |
| Two or three delivery phases | Full-width Timeline |
| Short hard constraint, risk, or positioning statement | Callout or quote |
| Compact JSON/config/payload | Code block |
| Large schema or exhaustive payload | Appendix or sub-document |

Avoid using multiple visual systems for the same information. Do not create Kanban, Gantt, Grid, or Base merely because Feishu supports them.

The first screen should contain one positioning statement and, when warranted, one short Callout. Do not restate the same behavior in a paragraph, Callout, quote, and decision table. For a long design, start with the smallest visual set that lets a reviewer explain the system and execution decision; a data-model table is often preferable to a third diagram when both encode the same relationships.

## 6. No-Context Reader Review

Before publishing, ask the document as if the reviewer has no chat history:

- Can the reader explain the problem and proposal after the first screen?
- Are product behavior and implementation mechanism clearly separated?
- Are ownership, source of truth, mutation points, and trust boundaries explicit?
- Can the reader follow the main flow without opening an appendix?
- Does every table or diagram answer a question that prose alone would not answer as well?
- Are failure outcomes distinguishable from transport, conversion, and business-quality outcomes where relevant?
- Are optional and required behavior stated directly?
- Are unresolved items honestly marked rather than filled with plausible detail?
- Can a reviewer find detailed fields and schemas without those details overwhelming the main narrative?
- Is each important rule authoritative in one place, with other sections referencing rather than re-explaining it?

Record review findings locally and fix the reader-facing draft before performing large cloud edits.
