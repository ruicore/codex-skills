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

Freeze the exact publish artifact before accepting its inventory. Appendices, generated schemas, payload examples, and directory listings added after an earlier draft invalidate that earlier manifest. Either run the helper against the assembled reader-facing source or independently reconcile the exact final HTML/fragment set. For a split publication, create one composite ledger; per-fragment counts without a final total are not a completion contract.

The composite ledger should include expected heading counts by level, tables by ordinal and identifying headers, diagram slot-to-DSL mappings, code-block count, a source-derived tail marker for each long code block, temporary placeholders, and deliberately deferred markers.

## 2. Browser And Target Preflight

1. Prefer the Codex in-app browser, load `browser:control-in-app-browser`, and read its runtime documentation before browser actions. Fall back only under the conditions defined in `SKILL.md`, never silently.
2. Open the exact target URL. Confirm title, current content, edit access, and whether it is the initially blank destination supplied by the user.
3. If the page already contains useful content, note the last-modified state and locate Edit History before a broad change.
4. Do not change sharing or permissions as part of publishing unless requested.
5. Reuse the logged-in session without inspecting credentials, cookies, storage, or profile files.

For authorized multi-agent experiments, the coordinator must create pages serially and record one exact URL per worker. Local package preparation and read-only review may run in parallel, but in-app-browser cloud mutation is single-writer and must be serialized even across different target pages. A worker must open only its assigned URL, confirm the expected blank/initial body and unique title, and treat a mismatch as a stop condition. Do not let several workers click `New Docs` concurrently in a shared browser session or infer ownership from the newest untitled page.

After a worker releases the in-app browser, allow the next worker one bounded fresh-state reconnect. If an old worker still cannot reacquire it, use the coordinator or a fresh worker turn on the already assigned URL. Do not poll indefinitely and do not silently switch to Chrome or another surface.

When the supplied target is blank, record that once as standing publication authority and proceed through body insertion, diagrams, tables, cleanup, retries, and history-backed recovery without asking for confirmation at each stage. Reconfirm only when the page is unexpectedly populated, unrelated content could be overwritten, or the requested scope expands beyond that page.

## 3. Native Block Insertion Order

A stable default order is:

1. Insert the complete ordinary body in one rich-text paste: headings, paragraphs, lists, tables, code blocks, and diagram slots.
2. Inspect the full outline and correct H1/H2/H3 semantics after all headings exist. Apply native numbering only when the editor exposes a reliable control.
3. Process every manifest diagram in one diagram pass. Keep each diagram transactional: insert, preview, confirm, delete its slot, and update the ledger before continuing.
4. Convert short positioning text to Callout/quote and create deliberate two-column or Timeline blocks after the main structure is stable.
5. Process every table in one table pass. Establish the shared outer boundary, then apply content-aware internal widths and record `adjusted/total`.
6. Perform editorial search, visual QA, save verification, reload verification, and manifest reconciliation.

This phase-batched order reduces repeated switching between the document editor, UML Board, and embedded Sheet. Do not default to publishing one section through prose, numbering, UML, and table layout before starting the next section. Use that local loop only for a genuinely small patch. If a skeleton is necessary, create semantic headings and sibling component slots only; do not wrap prose or slots inside the numbered heading list.

Keep the diagram pass before the table pass by default. A table-first batch is workable when required, but Sheet state can survive into later navigation. Before opening the first Board, explicitly exit Sheet/full-screen state, re-establish ordinary document focus, discard every saved coordinate, and locate each diagram again from its final-artifact slot.

For block creation, hover the block's left type icon, open its menu, and use `Insert Below`. This is more stable than relying on `/` input. The catalog is context-sensitive: page-root and ordinary blocks expose more options than some nested containers. If a component is absent inside a column or Synced Block, insert it as a sibling instead of forcing unsupported nesting.

The full catalog can include ordinary text, headings, lists, code, Table, Column, Callout, Synced Block, Button, Equation, Templates, Sub-doc, Sheets, Base views, drawing blocks, collaboration blocks, document/project integrations, Timeline, Mermaid, Table of Contents, and external embeds. Read [Component selection and nesting](component-selection-and-nesting.md) before using anything beyond the default technical-document set.

Use rich-text paste for ordinary structure, but never assume a recognized table or code block is visually finished.

### Safe broad-paste transaction

Before a full-body or large-fragment paste:

1. Click the visible empty-body prompt or use the last verified root document block's menu to `Insert Below` and create an ordinary sibling.
2. Type a harmless temporary sentinel to prove where input lands.
3. Confirm that the active editing root is the main document sibling, not a comment composer, list item, Callout, table, code block, Board, or Sheet. A current DOM class such as `.page-block.root-block` may be supporting evidence, but it is not a stable API.
4. Undo or remove the sentinel.
5. Paste the complete HTML fragment once.
6. Immediately verify an early anchor, a tail anchor, and the initial heading/table/code counts before proceeding.

Never target the last or a generic `[contenteditable=true]`; Feishu may place a comment composer after the document body.

One complete-body paste is the default. Split the main body and appendix only when payload size, independent generation, or a demonstrated editor limitation requires it. Insert every later fragment through `Insert Below` as a verified root sibling, repeat the focus probe, and reconcile the complete outline and composite ledger immediately afterward.

## 4. Heading Numbering

- Heading content contains only its semantic title: `结果可信边界`, not `9.0 结果可信边界`.
- Complete the body and confirm every heading in the outline before changing numbering. Do not number headings while publishing sections one by one.
- Enable Feishu-native numbering only when the current editor exposes a reliable heading-number control. If it does not, leave headings unnumbered; never add manual numeric prefixes or test list shortcuts against an uncertain document cursor.
- A native number is separately clickable and exposes `Continue numbering`, `Restart numbering`, and `Customize numbering value`.
- After paste, inspect every heading level and the left outline. Rich-text import may recognize `1. Title` but preserve `9.1 Title` as literal text.
- Use exact document Find/Replace for repeated manual prefixes. Never use global `Ctrl+A` to repair headings.
- Do not build a skeleton as `<ol><li><h2>Title</h2><p>body or slot</p></li></ol>`. It can number the body and component slots as nested list items. A useful skeleton contains headings only; body and slots remain ordinary sibling blocks, and numbering is deferred.

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

### Preferred numeric-width path

When the embedded Sheet exposes a `Column Width ... Pix` menu, it is usually faster and more repeatable than divider dragging:

1. Scroll the table far enough below the floating document toolbar that the column-letter row is unobstructed. If the embedded document view does not expose the numeric-width menu, enter Sheet full-screen mode; do not assume the menu exists in both views.
2. Click a cell once to activate the embedded Sheet. The first click or right-click may only activate it; reacquire the UI and verify that the column menu is actually open before typing.
3. Decide the common outer-width budget and target pixel width for each used column from the manifest percentages.
4. Set columns from rightmost to leftmost so expanding earlier columns does not push an unprocessed right-side header out of the viewport.
5. Right-click the column-letter header, select the exact numeric `Column Width ... Pix` item rather than `Autofit Column Width`, enter the target number, then click that same numeric menu item to commit. `Enter`, `Tab`, clicking outside, or repeated stepper clicks may not commit reliably.
6. Recheck the table's outer boundary, headers, and representative cells in document view before marking it adjusted.

Only type when the numeric width input is visibly present. A wrong focus can edit a selected cell or header instead of the width. If the numeric menu is absent, use full-screen divider dragging. `Autofit Column Width` is useful for short label columns, but applying it to long explanation columns can make the table excessively wide; give those columns the remaining shared-width budget instead.

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

For a repeated diagram pass, use this stable interaction rhythm:

- leave the previous Board's focus before using the document outline; if the outline changes its URL/hash but does not scroll, press `Esc` once, reacquire the current state, and retry;
- paste the complete DSL in one clipboard operation rather than typing it incrementally;
- after pasting, click the preview area or otherwise move focus out of the code editor so Feishu starts rendering;
- allow the preview to settle before judging it. `Insert` can remain disabled briefly, and an immediate screenshot can still show the default example;
- after the first successful diagram, reuse the same semantic sequence, but continue to reacquire menus and never replay a chain of stale coordinates.

After returning from each Board, immediately compare the adjacent heading and its outline entry with the expected title from the final artifact. A rendered diagram can coexist with accidental Board chrome text in the surrounding document. Perform the same comparison after reload; search for generic editor-chrome pollution, using strings such as `Add Icon` or `Add Cover` only as examples rather than a fixed protocol.

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
4. If Classic preview also fails, fix the DSL or choose a simpler supported diagram type. If only Board Style reports a syntax or converter-compatibility error for otherwise sound PlantUML, switch to Classic after one bounded attempt rather than repeatedly deleting valid DSL or distorting the model. Never insert an error preview as a placeholder.

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
4. Choose Board or Classic Style by complexity, paste the mapped DSL, move focus to the preview, wait for rendering, and inspect the result.
5. Click `Insert`, return to the document, and visually confirm the drawing is directly associated with the intended section.
6. Delete the whole slot block through its block menu.
7. Compare the adjacent heading and outline entry with the final artifact, then search the manifest placeholder and local diagram filename; all must pass before marking the diagram complete.

Keep public captions semantic. Do not show `PlantUML`, DSL instructions, or local insertion markers in the final page.

## 7. Safe Incremental Editing

- Prefer block menus, exact Find/Replace, cell-level table edits, and local section replacement.
- Treat every return from Find, Board, Sheet, full-screen mode, or the outline as a new layout state. Reacquire the intended block and its current bounding box before clicking; a changed URL hash or coordinates captured before the transition do not prove that the document scrolled to the target. If the wrong embedded component activates, press `Esc`, recapture the current UI, and retry once from the exact source-derived anchor.
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

For an initially blank target assigned to this publication, the original authorization covers this restore-and-retry sequence; do not pause for another confirmation. Do not attempt to reconstruct a long document from the remaining visible fragment when a known-good revision exists. Ask for direction only when no safe revision exists or unrelated content would be affected.

## 9. Reload Verification

Before declaring completion:

- wait for `Saved to cloud`;
- reload the page;
- confirm the document title and first/background section;
- open the outline and check heading levels; when native numbering is enabled, also check that it remains continuous;
- navigate to the last appendix/API section to prove the tail survived;
- use Find for removed field names, process-only phrases, diagram markers, and local paths;
- inspect every inventoried table for the common outer width and readable internal widths, and reconcile the `adjusted/total` count;
- inspect every diagram for an actual rendered drawing, syntax-error images, overlap, and duplicate board objects, and reconcile the `rendered/total` count;
- search every manifest diagram placeholder and generic placeholder/instruction patterns; all must be absent from the public page;
- confirm code blocks contain the intended full payload/schema rather than a partial paste;
- for every long code block with an independent scroll container, scroll inside the block to a source-derived tail marker and confirm its closing structure; outer page height, the next heading's visibility, and code-block count alone do not prove completeness;
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
- Headings/code blocks reconciled: <counts by level, code total, long-block tail checks>
- Representative prose sections checked: <names>
- Targeted searches: <terms and results>
- Deferred: <items or none>
```

Do not include credentials, cookies, raw browser state, or private content unnecessary for future maintenance.
