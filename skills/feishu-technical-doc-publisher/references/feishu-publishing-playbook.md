# Feishu Publishing Playbook

Use this reference for the operational path from a reviewed local draft to native Feishu blocks and for post-publication visual QA.

## Contents

1. Prepare the package
2. Browser and target preflight
3. Native block insertion order
4. Heading numbering
5. Table layout
6. PlantUML/UML Board
7. Safe incremental editing
8. Recovery
9. Reload verification
10. Publish result record

## 1. Prepare The Package

Run the bundled helper from the skill directory or with its absolute path:

```powershell
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir> --dry-run
python scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir>
```

It produces:

- `<stem>.publish.md`: source with PlantUML fences replaced by visible insertion markers;
- `<stem>.publish.html`: standard HTML suitable for opening and rich-text copying;
- `diagrams/diagram-XX.puml`: one file per PlantUML fence;
- `publish-manifest.json`: source SHA-256, output paths, counts, and editorial warnings.

Review warnings before publishing. The helper does not decide whether a numbered heading or `待定` is correct, and it never edits the source or Feishu.

The first command previews planned files and existing-path conflicts. The write command refuses to overwrite generated files; use `--force` only after confirming that the output directory is the intended generated-publication location.

If the project already has a more specific generator that assembles appendices or authoritative schemas, prefer it. Preserve its source boundaries and still apply the QA gates below.

## 2. Browser And Target Preflight

1. Prefer the Codex in-app browser, load `browser:control-in-app-browser`, and read its runtime documentation before browser actions. Fall back only under the conditions defined in `SKILL.md`, never silently.
2. Open the exact target URL. Confirm title, current content, edit access, and whether the user authorized replacing it.
3. If the page already contains useful content, note the last-modified state and locate Edit History before a broad change.
4. Do not change sharing or permissions as part of publishing unless requested.
5. Reuse the logged-in session without inspecting credentials, cookies, storage, or profile files.

## 3. Native Block Insertion Order

A stable order is:

1. Insert or paste the ordinary body: headings, paragraphs, lists, tables, and code blocks.
2. Convert headings to the intended native H1/H2/H3 levels and enable native numbering.
3. For each manifest diagram, insert it at its slot through UML Board, verify the inserted block, and only then remove the entire visible slot block.
4. Convert short positioning text to Callout/quote and create any deliberate two-column or Timeline blocks.
5. Adjust every table's outer and inner widths, using the generated table inventory as an `adjusted/total` checklist.
6. Perform editorial search, visual QA, save verification, and reload verification.

For block creation, hover the block's left type icon, open its menu, and use `Insert Below`. This is more stable than relying on `/` input. The catalog is context-sensitive: page-root and ordinary blocks expose more options than some nested containers. If a component is absent inside a column or Synced Block, insert it as a sibling instead of forcing unsupported nesting.

The full catalog can include ordinary text, headings, lists, code, Table, Column, Callout, Synced Block, Button, Equation, Templates, Sub-doc, Sheets, Base views, drawing blocks, collaboration blocks, document/project integrations, Timeline, Mermaid, Table of Contents, and external embeds. Read [Component selection and nesting](component-selection-and-nesting.md) before using anything beyond the default technical-document set.

Use rich-text paste for ordinary structure, but never assume a recognized table or code block is visually finished.

## 4. Heading Numbering

- Heading content contains only its semantic title: `结果可信边界`, not `9.0 结果可信边界`.
- Enable the native numbered-list option on heading blocks so Feishu generates `9`, `9.1`, `9.2`, and later renumbers on insertion or deletion.
- A native number is separately clickable and exposes `Continue numbering`, `Restart numbering`, and `Customize numbering value`.
- After paste, inspect every heading level and the left outline. Rich-text import may recognize `1. Title` but preserve `9.1 Title` as literal text.
- Use exact document Find/Replace for repeated manual prefixes. Never use global `Ctrl+A` to repair headings.

## 5. Table Layout

Feishu may import a correct table with every column near 100 px, causing one-character Chinese wrapping and a large unused right side. Treat layout as a required publishing stage.

The table block menu exposes `Header Row`, `Header Column`, and `Distribute Columns`. Use the header toggles to encode semantics. `Distribute Columns` equalizes widths and is useful only as a starting point when columns contain similarly short values; content-aware manual sizing remains required for most technical tables.

### Outer width

- Tables may be wider than body paragraphs.
- Within one document, prioritize a consistent left and right boundary for all major tables, even when their column counts differ.
- Enter table full-screen mode, determine the common outer right boundary, and drag the last used column to that boundary before adjusting internal dividers.
- Exit full-screen and compare adjacent tables in the document view.

### Internal width

Allocate width by content, not equally:

1. Give scenario names, technical field names, phases, and compound statuses enough width to remain one line or at most two.
2. Make short enums, booleans, counts, and versions narrow.
3. Give explanation, reason, and handling columns the remaining width.
4. Do not change the established outer width while moving internal dividers.

Useful starting points, not fixed rules:

- short label + long explanation: `20–25% / 75–80%`;
- long scenario + handling: `34–40% / 60–66%`;
- category + conclusion + reason: `18% / 28% / 54%`;
- long scenario + short reference + result + boolean: `35% / 16% / 28% / 21%`.

If the last column is not visible in full-screen mode, reduce the table zoom before dragging; the viewport edge is not necessarily the table edge. If a formula bar shows content but the document cell looks empty, clear local formatting or copy formatting from a healthy peer cell before assuming data loss.

### Table completion gate

The generated manifest inventories every Markdown table and provides a suggested content-based percentage per column. Use it to locate and size each cloud table; the suggestion is a starting point, not an automatic Feishu setting.

- Adjust every table, not only an early, middle, and late sample.
- Record `adjusted/total` in the publish result. The only acceptable exception is a table whose equal-width columns are genuinely appropriate; record that decision explicitly.
- Compare all major tables in document view for a common outer left/right boundary.
- Reopen each table at normal viewing width and confirm that labels do not wrap one character per line, explanation columns receive the remaining space, and large unused right-side gaps are gone.
- If even one table remains at an unreviewed default layout, the visual publication gate is incomplete.
- Treat each table as a transaction and record its ordinal, identifying headers, representative cell-content check, adjustment method, outer-boundary result, and document-view visual check. `Autofit Column Width` or `Distribute Columns` is an action, not evidence of the final layout.
- If the imported table looks blank, verify headers and sample cells before changing widths. Missing or invisible content is a publication failure, not a layout state to count as adjusted.
- After the last table, navigate back through the document and visually compare all table outer boundaries. If a table is still visibly narrow, leaves a large unused right area, or wraps a short label vertically, keep its status `required` rather than counting it as adjusted.

## 6. PlantUML And UML Board

Open `UML Diagram`. This first opens a blank Board and its template panel; the PlantUML entry is not in that initial template list. In the Board's left floating toolbar, open the nine-dot/More menu and select `PlantUML Diagram`. Paste the extracted `.puml`, preview, choose a style, and insert.

Do not search the top-right document overflow menu or `More Templates` for PlantUML, and do not conclude that the feature is unavailable from those panels. Prefer semantic text/role locators after each menu opens. When a semantic locator is unavailable, take a fresh screenshot immediately before the single coordinate action; never chain coordinates learned from an earlier layout state.

### Diagram slot contract

- A local source or generated publication draft may contain a human-readable slot such as `图位 01`, an HTML comment, or another clearly temporary block. The exact sentence is not fixed and must never be used as the workflow contract.
- The generated manifest maps each slot ID/ordinal to its retained DSL path. Locate diagrams from that mapping, not by assuming a filename embedded in the visible prose.
- Keep the slot until the corresponding diagram has rendered in the Feishu modal, been inserted, and been confirmed in the intended document position.
- Delete the entire slot block after insertion. Do not edit fragments of the sentence, which can leave suffixes or formatting debris.
- Before completion, search for every manifest placeholder value plus generic temporary-marker forms such as `图位`, `发布占位`, local diagram extensions, and insertion-instruction language. Expected result: zero public remnants.

### Renderer compatibility gate

Feishu may embed an older PlantUML renderer than the current upstream release. The generated manifest flags a small set of known portability risks, but only the Feishu modal preview is authoritative.

Before clicking `Insert`:

1. Resolve every generated compatibility warning or document why it is safe.
2. Confirm the preview contains the intended diagram, not a PlantUML version/sponsor error image or `Syntax Error` panel.
3. Prefer established syntax supported by the displayed Feishu renderer. For decision flow, use activity-diagram `if / then / else / endif`; do not declare a standalone `diamond` node.
4. If the preview fails, fix the DSL or choose a simpler supported diagram type. Never insert the error preview as a placeholder.

### Choose style by diagram complexity

Board Style is editable but has a different layout engine from PlantUML Classic. Use it for simple diagrams with short labels, limited branching, and no high-degree center node. Choose Classic Style initially when the diagram has several branching paths, long edge labels, a dense center, or a layout whose primary value is faithful PlantUML rendering.

When Board Style is otherwise desirable, make one bounded correction pass:

1. Replace a high-degree center node with two or three semantic path nodes.
2. Move long text from central edges to downstream edges or dedicated nodes.
3. Insert `\n` in long labels and combine parallel request/response descriptions when that preserves meaning.
4. Replace deeply nested activity `if/else` with explicit components/diamonds and one-way branches.
5. Keep diagrams to roughly 8–12 primary nodes where possible.
6. Check fit-to-screen and 70–100% zoom for text overlap, lines crossing labels, and unclear branch direction.

If the diagram remains unreadable after that pass, select Classic Style. Do not repeatedly distort a sound architecture or execution model merely to satisfy the Board layout engine.

### Insertion behavior

`Insert` adds a new board object; it does not reliably replace the old one. Zoom out after reinsertion, identify duplicate objects, delete only the obsolete object, then return to the document and verify the embedded board.

After reload, navigate to every diagram and visually confirm the drawing still renders. An embedded Board container, block id, expected width, or comment button does not prove the PlantUML content rendered successfully.

For each diagram, use this transaction:

1. Navigate to the manifest slot and open that block's `Insert Below` menu.
2. Select `UML Diagram`; wait for the Board to finish opening.
3. Open the left-toolbar nine-dot/More menu and select `PlantUML Diagram`.
4. Paste the mapped DSL, inspect the preview, and choose Board or Classic Style by complexity.
5. Click `Insert`, return to the document, and visually confirm the drawing is directly associated with the intended section.
6. Delete the whole slot block through its block menu.
7. Search the manifest placeholder and local diagram filename; both must return zero matches.

Keep public captions semantic. Do not show `PlantUML`, DSL instructions, or local insertion markers in the final page.

## 7. Safe Incremental Editing

- Prefer block menus, exact Find/Replace, cell-level table edits, and local section replacement.
- Never issue `Ctrl+A` in the document, code block, or table editor. Focus can escape the intended block and select the full page.
- When replacing a code block, insert a new code block, paste the complete validated content, verify it, and only then delete the obsolete block.
- In table cells, select the exact cell, enter cell-edit mode when needed, and verify the row after pressing Enter. Do not infer paste success from keyboard completion.
- After removing a field or concept, search the whole page for the field name and its human-readable alias. Check tables, diagrams, payloads, failure scenarios, implementation order, and acceptance criteria.
- When a browser-upload and an edge-upload path have different trust boundaries, keep separate headings. If one path is not designed, leave it as `待定` rather than copying the other path's rules.

## 8. Recovery

If a broad selection or paste overwrites the document:

1. Stop further editing immediately.
2. Open Edit History.
3. Choose the nearest revision known to contain the complete outline and body.
4. Restore it and reload the page.
5. Verify title, early sections, late appendices, representative tables, and diagrams before reapplying changes.
6. Reapply only scoped edits, starting with the maintainable local draft.

Do not attempt to reconstruct a long document from the remaining visible fragment when a known-good revision exists.

## 9. Reload Verification

Before declaring completion:

- wait for `Saved to cloud`;
- reload the page;
- confirm the document title and first/background section;
- open the outline and check heading levels and continuous numbering;
- navigate to the last appendix/API section to prove the tail survived;
- use Find for removed field names, process-only phrases, diagram markers, and local paths;
- inspect every inventoried table for the common outer width and readable internal widths, and reconcile the `adjusted/total` count;
- inspect every diagram for an actual rendered drawing, syntax-error images, overlap, and duplicate board objects, and reconcile the `rendered/total` count;
- search every manifest diagram placeholder and generic placeholder/instruction patterns; all must be absent from the public page;
- confirm code blocks contain the intended full payload/schema rather than a partial paste;
- verify deliberately undecided sections contain only the agreed placeholder, commonly `待定`.

Feishu may virtualize off-screen content after reload. Use the outline to prove the full heading structure, then combine native Find with targeted anchor navigation or scrolling to verify representative early, middle, and tail content. Do not treat the currently rendered DOM or first viewport as proof that the full document survived.

A `0 / 0` Find result after enough UI settling is useful evidence. Reacquire the Find input after the panel rerenders; do not trust a stale locator or a result read immediately after changing the query.

## 10. Publish Result Record

Record a compact local result:

```markdown
# <document title>: Feishu publish result

- Target: <url>
- Published at: <timestamp and timezone>
- Source: <path and SHA-256>
- Generated package: <path>
- Cloud state: Saved to cloud, reloaded
- Tables adjusted: <adjusted/total, common boundary, explicit exceptions>
- Diagrams rendered: <rendered/total, DSL paths, preview and reload result>
- Representative prose sections checked: <names>
- Targeted searches: <terms and results>
- Deferred: <items or none>
```

Do not include credentials, cookies, raw browser state, or private content unnecessary for future maintenance.
