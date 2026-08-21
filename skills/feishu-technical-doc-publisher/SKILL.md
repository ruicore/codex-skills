---
name: feishu-technical-doc-publisher
description: Turn a local authoritative Markdown design or conclusion into a reader-ready Feishu technical document using the authenticated browser, including editorial restructuring, native blocks, diagrams, table layout, safe cloud editing, and publish verification. Use when the user asks to write, publish, or synchronize a local Markdown technical document to Feishu; do not use for ordinary Markdown editing without Feishu delivery.
---

# Feishu Technical Doc Publisher

Publish a self-contained Feishu technical document for readers who do not share the author's prior conversation context. Preserve a local authoritative source and treat the Feishu page as a reviewed publication surface, not the only copy of the design.

## Purpose

Turn a local engineering conclusion into a durable publication package and a visually verified Feishu document without losing the source of truth, leaking private context, inventing undecided contracts, or damaging existing cloud content.

## When To Use

- The user asks to write, publish, republish, or synchronize a local Markdown technical design to Feishu.
- A discussion-derived engineering document needs reader-first restructuring and native Feishu layout.
- An existing Feishu technical document needs to be reconciled with a maintainable local source and revalidated after edits.

## When Not To Use

- Ordinary Markdown editing, proofreading, or architecture review with no Feishu deliverable.
- Reading a Feishu page without publishing or synchronizing local content.
- Publishing to another document platform whose block model and recovery path differ materially.
- Clearing or replacing a populated target when the user has not authorized that scope.

## Inputs To Infer Or Request

- **Authoritative local source:** infer from the named file or repository convention; stop if multiple conflicting candidates remain.
- **Target Feishu page:** must be explicit before cloud mutation.
- **Publication mode:** infer section-level editing when the user names sections; require explicit authority before replacing an existing populated page.
- **Reader and purpose:** infer from the document and user request, then choose a primary emphasis: general reader narrative, architecture review, implementation contract, or a mixed publication. State material assumptions in the local draft.
- **Reference documents and style constraints:** inspect when the user supplies them; do not copy their business content.
- **Deferred content:** preserve the user's latest instruction exactly, commonly as `待定`.

## Execution Model Gate

Full cloud publication is a high-interaction browser task when it includes UML Board insertion, content-aware table sizing, or recovery from partial edits. Prefer `gpt-5.6-sol` with `high` or `xhigh` reasoning for that mutation phase. An equivalent current frontier model is acceptable only when it can reliably inspect screenshots, reacquire changing UI state, and complete the validation gates below.

Do not use `gpt-5.6-terra` at `medium` reasoning, or a weaker execution profile, for the final Feishu mutation phase. Such a profile may prepare the local package or perform read-only inspection, but it must stop before cloud edits and ask the user to continue with the recommended model/effort. A skill cannot silently change its own model, so state this requirement before beginning the publication mutation.

## Evidence Hierarchy

1. The user's latest explicit instruction, including target and mutation scope.
2. The authoritative local design, current code/schema/specification evidence, and settled local decision records.
3. The current Feishu page after reload and visible browser verification.
4. Repository documentation, publishing records, and prior reader reviews.
5. Reference documents used only for narrative and layout patterns.
6. Inference, clearly labeled and never used to fill an intentionally undecided contract.

## Reference Navigation

Read only the reference needed for the current stage:

| Need | Read |
| --- | --- |
| Turn engineering conclusions into a public-facing narrative, choose sections, remove discussion artifacts, or conduct a no-context reader review | [Editorial workflow](references/editorial-workflow.md) |
| Prepare a publish package, edit Feishu native blocks, size tables, insert PlantUML, recover from unsafe edits, or run cloud verification | [Feishu publishing playbook](references/feishu-publishing-playbook.md) |
| Choose advanced Feishu components, inspect nested menus, or decide whether a synced, interactive, data, project, or embed block belongs in a technical document | [Component selection and nesting](references/component-selection-and-nesting.md) |

For a full local-Markdown-to-Feishu task, read both references before mutating the target page.

## Authority And Source Of Truth

1. Confirm the authoritative local Markdown, target Feishu URL, and whether the user authorized replacing existing cloud content or only editing selected sections.
2. Read repository instructions and relevant local design sources before writing. Distinguish settled decisions, evidence, unresolved items, rejected alternatives, and implementation guesses.
3. Keep a maintainable local publication source. By default, place derived publication artifacts under the repository's existing ignored agent/document area, commonly `.manifest/feishu/<document-slug>/`; follow an existing convention when present.
4. Never make the Feishu page the only source of a diagram DSL, schema, payload, or settled decision.
5. Do not expose local paths, private evidence, secrets, authenticated commands, cookies, tokens, or browser storage in the public document.

## Browser Boundary

Prefer the Codex in-app browser for all Feishu UI work. Load and follow the `browser:control-in-app-browser` skill before browser actions, and reuse an authenticated in-app session when one is available. If the user explicitly requests the in-app browser, that choice is binding.

Fall back to another browser surface only when the in-app browser is unavailable, lacks the required authenticated session, or cannot complete the required Feishu operation after a bounded attempt. Before falling back, tell the user the concrete limitation; do not silently switch browser surfaces. If the user required the in-app browser, stop and request direction instead of falling back.

Reuse an already authenticated browser session when available, but never inspect or persist cookies, tokens, passwords, local storage, or profile data. Authentication permits the requested document operation only; it does not authorize editing other pages, changing sharing, deleting unrelated content, or creating extra documents unless the user asked for it.

## Side-Effect Policy

- **Default level:** `local-files` for publication drafts, generated packages, extracted DSL, and publish records.
- **Maximum normal level:** `publish` when the user explicitly asks to write to a named Feishu destination.
- Treat target-page inspection as read-only until the user has requested the cloud edit.
- Preview the local reader-facing draft and generated package before publication. Existing generated files require an explicit `--force`; an existing populated Feishu page requires explicit replacement authority.
- Use only the intended authenticated account and page. Do not expose credentials or private source material.
- Establish Edit History as the cloud recovery path before broad replacement. Do not perform unrelated deletion as cleanup.

## Core Workflow

### 1. Build The Publication Package

- Preserve the authoritative source unchanged unless the user also requested a source edit.
- Create or update a reader-facing draft, publishable Markdown/HTML, extracted diagram DSL, and a short publish result record.
- When useful, run:

```powershell
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir> --dry-run
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir>
```

The script extracts PlantUML fences, generates rich-text-ready Markdown/HTML, records a source hash, and reports editorial warnings. It does not edit Feishu. Diagram slots are local publication markers linked to manifest entries by ordinal/slot ID; their visible wording is not an API and must not be treated as a fixed string.

Use the generated table inventory as a completion checklist. Its width percentages are starting suggestions, not proof of cloud layout. Resolve PlantUML compatibility warnings before insertion, and still require a successful Feishu preview because static checks cannot prove renderer compatibility.

Before cloud mutation, create a publication ledger from the manifest with one pending row per table and diagram. Record identifying headers for tables and the manifest placeholder/DSL path for diagrams. Counts inferred from the visible first screen are not sufficient.

### 2. Rewrite For A No-Context Reader

- Start with background, purpose, scope, and an overview before detailed fields or APIs.
- Choose the reading emphasis before choosing blocks. For a mixed audience, keep a reader-first main path, use only the core diagrams needed to establish flow, and place contract detail after the reader understands ownership and behavior.
- Explain ownership and end-to-end flow before schema and implementation structure.
- Convert conversation-dependent reasoning into stable conclusions. Remove oral estimates, rejected names, superseded options, and phrases meaningful only to prior participants.
- If a section is intentionally undecided, write `待定` rather than inventing a contract from discussion fragments.
- Keep the main path concise. Move large schemas, payloads, and implementation directories to an appendix or sub-document.

Use [Editorial workflow](references/editorial-workflow.md) for the detailed narrative and cleanup gates.

### 3. Choose Native Feishu Blocks Deliberately

- Use native H1/H2/H3 and Feishu numbering. Heading text must not contain hand-maintained numeric prefixes.
- Use Callout or quote blocks only for short positioning statements, hard constraints, or risks. Give a rule one primary expression; do not repeat the same sentence in an opening paragraph, Callout, quote, and table.
- Use native tables for repeated mappings and comparisons; use code blocks for compact payloads and configuration.
- Use a native Table of Contents for long pages only when it improves in-page onboarding; the native outline may already be sufficient. Use Equation for genuine mathematical notation; keep both full-width.
- Keep diagrams, wide tables, Timeline, and long code full-width. Use at most two columns, only for short paired summaries.
- Prefer one visual per relationship: PlantUML for architecture/flow/ER, Timeline for a small phase sequence whose chronology matters, and tables for exact mappings. Start with the smallest set of diagrams that explains the system; add another only when it represents a distinct relationship rather than repeating a table.
- Choose UML rendering style by complexity. Board Style suits simple diagrams with short labels and limited branching; use Classic Style directly for dense branching, high-degree center nodes, or long edge labels.
- Treat Synced Block, Poll, Button, Templates, Sheets/Base views, sub-documents, project cards, and external embeds as conditional capabilities. Read [Component selection and nesting](references/component-selection-and-nesting.md) before using them. Menu visibility alone does not prove stable behavior or authorize creation of persistent cloud objects.
- Expect `Insert Below` to change by container. If a block type disappears inside a column, Callout, or Synced Block, insert it as a sibling rather than forcing unsupported nesting.

### 4. Publish Safely

- Inspect the target page and its current structure before changing it. When existing content matters, note the page title and last-modified state and know how to reach Edit History.
- Prefer block-level operations and `Insert Below`. Use rich-text paste for ordinary headings, lists, tables, and code; insert extracted PlantUML diagrams separately through UML Board.
- Process every diagram as an atomic transaction: locate its manifest slot, insert and validate the diagram, return to the document, confirm the rendered block is in the intended position, then delete that entire slot block. Never leave a local insertion instruction or filename in the public page.
- Complete an individual outer-width and content-aware column-width pass for every table in the generated inventory. Sampling representative tables is insufficient for publication completion. Clicking an autofit/distribute command is not completion until the resulting widths are visually checked in document view.
- In the PlantUML modal, do not click `Insert` unless the preview shows the intended diagram with no syntax-error panel. A Board block existing in the document is not evidence that its diagram rendered.
- Never use global `Ctrl+A` in the Feishu document, code block, or table editor. It can select and overwrite the entire document.
- Use native Find/Replace only for narrowly scoped, exact replacements. After removing text, delete empty headings, numbered items, and table formatting left behind.
- Do not change sharing, permissions, comments, or unrelated pages unless explicitly requested.

Use [Feishu publishing playbook](references/feishu-publishing-playbook.md) for the stable insertion, table, diagram, and recovery procedures.

### 5. Validation Requirements

Verify the published page as a reader, not merely as an editor:

- the first screen explains why the document exists and what it proposes;
- the outline is coherent and Feishu numbering is continuous;
- every inventoried table retains its headers and representative cell content, was individually adjusted, shares the document's chosen outer boundary, and allocates internal columns by content; an empty-looking or default equal-width import is incomplete unless the content and uniform sizing are both intentionally correct;
- every diagram rendered successfully in the Feishu preview and remains a real diagram after insertion and reload, with no syntax-error image, overlapping labels, or duplicate board objects;
- unresolved sections say `待定` and no invented detail appears;
- process-only phrases, local paths, diagram placeholders, and removed field names do not remain;
- the page reports `Saved to cloud`.

Reload the page and repeat targeted checks. A successful paste or visible save indicator before reload is not sufficient proof.

Reconcile the manifest transactionally: `content-verified and adjusted tables == manifest tables`, `rendered diagrams == manifest diagrams`, and `remaining manifest placeholders == 0`. If any equality fails, publication is incomplete regardless of how much prose was successfully pasted.

Feishu may virtualize off-screen blocks after reload. Verify the outline, then use native Find plus targeted anchor navigation or scrolling to inspect representative early, middle, and tail sections; a first-screen snapshot does not prove that the full document survived.

### 6. Synchronize And Record

After cloud refinements, update the maintainable local publication source so a later republish does not restore stale wording. Record:

- target URL and publication time;
- local source and generated artifact paths;
- diagrams inserted and the retained DSL paths;
- table layout completion as `adjusted/total`, including any explicit exceptions;
- diagram render completion as `rendered/total`, including the Feishu preview and reload check;
- representative sections visually checked;
- exact cloud-save/reload verification performed;
- any intentionally deferred content.

Report only validation actually performed.

## Output Contract

Return or link:

- the Feishu page, when publication was authorized and completed;
- the maintainable local reader-facing source;
- the generated publish package and retained diagram DSL;
- the publish result record;
- executed validation, skipped checks, deferred sections, and any recovery action.

Do not claim cloud completion when only local artifacts were prepared.

## Failure And Recovery Rules

- If the target content is unexpectedly missing, duplicated, or broadly replaced, stop editing. Open Edit History, restore the nearest known-good revision, reload, and verify the full outline before reapplying scoped changes.
- Use Board Style for simple editable diagrams. For dense branching, high-degree center nodes, or long edge labels, choose Classic Style up front. If a Board attempt remains unreadable after one bounded simplification pass, switch to Classic rather than repeatedly rewriting a sound diagram to fit the Board layout engine.
- Feishu's embedded PlantUML may lag the current release. Prefer established syntax and treat the modal's displayed renderer as authoritative. Do not use standalone `diamond` declarations for decisions; use activity-diagram `if / then / else / endif` or supported structural nodes. If preview fails, fix or replace the DSL before insertion.
- Do not infer that Feishu lacks PlantUML because it is absent from the initial UML template panel or a top-right overflow menu. In the opened Board, use the left floating toolbar's nine-dot/More menu, then choose `PlantUML Diagram`. Reacquire the current screenshot and semantic labels at each menu boundary; do not replay stale coordinates through several changing menus.
- Do not silently substitute draw.io, Graphviz, or static images for requested native UML. If the documented PlantUML entry still cannot be reached after one fresh-state retry, leave the local slot intact, make no substitute cloud insertion, and report that diagram publication is incomplete.
- If a table cannot show all used columns after width adjustment, reduce the table zoom or reopen full-screen editing; do not mistake the viewport edge for the table boundary.
- If the user has not authorized overwriting a populated target, do not clear it. Prepare local artifacts and request that authority.
- If authentication is missing in the selected browser, stop and ask the user to sign in there; do not bypass it through another account or browser.

## Before Finishing

Confirm that the local source and publication artifacts exist, the target URL is correct, the document survives reload, every table and diagram passed its explicit layout/render gate, the outline and representative prose were inspected, no sensitive data was published, deferred content is explicit, and the final response links both the Feishu page and the maintainable local source. If any table or diagram remains unchecked or broken, report publication as incomplete rather than downgrading it to a skipped representative check.
