# Feishu Component Selection And Nesting

Use this reference when a Feishu technical document may benefit from blocks beyond headings, paragraphs, lists, tables, code, Callout, and UML Board. It records UI behavior confirmed in an authenticated Feishu Docs session on 2026-08-20. Labels and availability may vary by tenant, so recheck the live menu before relying on a conditional component.

## Evidence Levels

- **Configured:** inserted and its meaningful editor or settings were exercised.
- **Inserted:** inserted and visibly rendered, but not every setting or cross-document behavior was exercised.
- **Menu-confirmed:** the entry and any listed submenu were observed; creation was intentionally not completed.

Do not describe a menu-confirmed component as operationally validated.

## Default Technical-Document Set

Prefer this compact set unless the document has a concrete reason to add more:

| Component | Evidence | Best use | Important constraint |
| --- | --- | --- | --- |
| H1/H2/H3, lists, quote, divider, link | Configured | Narrative structure and native numbering | Keep heading text free of manual numeric prefixes |
| Callout | Configured | Short positioning statement, hard constraint, risk, or status | Long prose, tables, and large payloads reduce its value |
| Table | Configured | Exact mappings, contracts, comparisons, and decision matrices | Set one outer width, then size internal columns by content |
| Code block | Configured | Compact JSON, YAML, SQL, commands, or configuration | Select a language, decide Wrap deliberately, and keep large contracts out of the main path |
| Table of Contents | Inserted | Long documents whose readers benefit from an explicit in-page entry map | The native outline may already be sufficient; if inserted, keep it full-width |
| Equation | Configured | Mathematical scoring, thresholds, and formulas | Uses a LaTeX input editor and renders a native equation block |
| Timeline | Configured | A small number of phases or milestones where chronology is the main relationship | Keep full-width; prefer a comparison table when scope, ownership, and outputs matter more than time |
| UML Board / PlantUML | Configured | Architecture, flow, sequence, state, and ER relationships | Preserve DSL locally; require a clean Feishu preview before Insert and an actual rendered drawing after reload; Board-container existence alone is not validation |

## Conditional Components

Use these only when their behavior is part of the document's purpose.

### Synced Block

**Evidence:** inserted. The block exposes `Not synced yet`, `Share`, copy, and comment controls. An Equation was inserted inside it successfully.

Use it for a centrally owned disclaimer, support policy, or repeated constraint that must remain synchronized across pages. Before creating or sharing one, identify the authoritative owner and decide whether downstream documents should receive future changes automatically. Do not use it merely to avoid copying a paragraph.

### Poll

**Evidence:** configured as an unpublished draft. The editor supports a question, multiple answer options, a deadline, anonymous responses, single or multiple selection, and an explicit `Publish Poll` action.

Use it for RFC decisions or reader feedback only when the document is intentionally interactive. Publishing changes external collaboration state; do not publish a poll without user authorization. A technical design should still state the decision and rationale after consensus rather than relying on the poll as its permanent contract.

### Button

**Evidence:** menu-confirmed. Actions observed: `Open Hyperlink`, `Make a Copy`, and `Follow Doc`.

Use a button only for a primary reader action, such as opening an authoritative runbook or copying a controlled template. Ordinary references should remain links; too many buttons make a design page resemble an application dashboard.

### Templates And Reusable Blocks

**Evidence:** menu-confirmed. The Templates submenu exposed `Reading Notes`, `SWOT Mind Map`, `Meeting Notes`, `Project Plan`, `To-do List`, and `More templates`. Block menus also exposed `Save to My Templates`, and several block types exposed `Save as Sub-doc`.

Treat templates as structure generators, not authoritative content. Inspect every inserted section and remove irrelevant headings. Creating personal templates or sub-documents produces persistent cloud assets and requires authority beyond editing the named page.

### Sheets And Base Views

**Evidence:** menu-confirmed. `Sheets` uses a grid-size selector. Base entries observed: `Grid`, `Kanban`, `Gantt`, `Gallery`, and `Link Existing Base`.

- Use a native table for a static contract or comparison.
- Use Sheets when the page genuinely needs formulas or tabular analysis.
- Use a Base view only for a living dataset, issue tracker, or project-management surface with an identified owner and maintenance process.

Do not add Kanban, Gantt, Gallery, or a spreadsheet merely to make a technical design more visual.

### Collaboration And Document Management

**Evidence:** menu-confirmed. Entries observed: `Person`, `Group Card`, `Docs`, `Task List`, `OKR`, `Poll`, `Date Reminder`, `Info Collector`, `Calendar event`, `Meeting Agenda`, `Sub-page List`, and `Wiki Space Updates`.

Use Person/Docs references for ownership and authoritative dependencies. Use Task List, reminders, forms, calendars, or agendas only when the page also owns an active collaboration workflow. `Sub-page List` is useful for a deliberately managed documentation hub, not a single design page.

### Project And External Integrations

**Evidence:** menu-confirmed.

- Jira submenu: `Jira Issue`, `Jira Filter`.
- Feishu Project submenu: `Table of views`, `Details card`.
- Embed catalog observed: Douyin, Bilibili, Youku, iQIYI, Jimeng AI, Figma, Mockitt, Canva, Jcode, CodePen, Feishu Survey, Jinshuju, Airtable, Baidu Maps, and AutoNavi Maps.

Embed only an authoritative, permission-compatible artifact whose live state benefits the reader. Prefer an ordinary link when an embed adds authentication, third-party availability, data residency, or long-term maintenance risk. Do not create or connect external project objects during ordinary publication unless explicitly requested.

## Context-Sensitive Menus And Nesting

The `Insert Below` catalog is context-sensitive. Do not assume that a component visible at the page root can be nested in every container.

Confirmed example: inside a Synced Block, the menu still allowed basic text, Todo, Image, Video or File, Table, Callout, Equation, and drawing components, but did not expose Column, another Synced Block, Button, Templates, Sub-doc, or Base components. This prevents some recursive or externally coupled compositions.

Apply these rules:

1. Decide the outer layout before inserting specialized blocks.
2. Keep Table of Contents, Timeline, Mermaid, UML Board, Sheets, Base views, wide tables, and long code full-width.
3. Use columns only for short paired summaries; do not place a specialized editor in a narrow column.
4. Avoid more than one semantic container layer. `Column -> short Callout` can be useful; `Column -> Synced Block -> interactive widget` is usually hard to read and maintain.
5. If a desired item disappears from `Insert Below`, exit the current container and insert it as a sibling. Do not work around the restriction by creating unrelated cloud objects.
6. Recheck the final page at normal viewing width. A block that edits correctly in full-screen mode may still be unreadable in the document.

## Deep Menu Paths Worth Knowing

- Heading or text block -> `Align and Indent`: left, center, right, increase indent, decrease indent.
- Heading or text block -> `Color Options`: text color, background color, reset.
- Callout icon: searchable emoji picker with categories.
- Callout block menu: can change the internal text style and expose `Synced Block`, `Save as Sub-doc`, and `Save to My Templates` actions.
- Table block menu: `Header Row`, `Header Column`, and `Distribute Columns`.
- Table creation: a row-by-column grid picker.
- Code block toolbar: language search/selection, `Wrap`, and `Copy`.
- Button submenu: `Open Hyperlink`, `Make a Copy`, `Follow Doc`.
- Templates submenu: reading notes, SWOT mind map, meeting notes, project plan, and to-do list.
- Draw -> `More 1.0`: another path to Mind Map, Flowchart, and UML Diagram; prefer the current first-level entries unless the old path is required.
- UML Board menu: Theme, Mermaid Diagram, and PlantUML Diagram.

`Distribute Columns` equalizes a table and is only a starting point for uniformly short data. It is not a substitute for content-aware column sizing.

## Publication Safety

- Menu visibility does not authorize creating persistent Base, sub-document, template, project, survey, or integration objects.
- Poll publication, Synced Block sharing, and external integrations are collaboration mutations separate from writing the named page.
- During exploration, leave a poll unpublished and do not share a Synced Block unless that state change is explicitly requested.
- Record which conditional components were inserted and which were only inspected. Recheck them after reload because plugin blocks can load after the surrounding document reports that it is saved.
- If a conditional component does not materially improve reader understanding, remove it from the final technical document even if the editor supports it.
