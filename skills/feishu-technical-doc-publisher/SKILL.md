---
name: feishu-technical-doc-publisher
description: Publish or synchronize local Markdown technical documents to a named Feishu page, with native diagrams, table layout, and reload verification. Use for Feishu delivery, not ordinary Markdown editing or read-only document access.
---

# Feishu Technical Doc Publisher

Keep a maintainable local source and publish a self-contained Feishu document for
readers who do not share the conversation context. Preserve deliberately undecided
content as `待定` or the user's chosen marker.

## Scope and authority

- Establish the authoritative local source, exact target page, and requested edit
  scope before cloud mutation. Do not replace a populated page without authority
  covering its existing content.
- When the user assigns an initially blank page for publication, that request
  covers ordinary editing, diagram insertion, table sizing, corrections, and
  recovery through Edit History throughout the task. Do not ask again for each
  stage. Reassess only when unrelated content, a new destination, sharing changes,
  or another material boundary appears.
- Preserve the authoritative source unless its revision is in scope. Keep derived
  drafts, DSL, manifests, and publish records in the repository's established local
  document area. Cloud content must not become the only copy of the design.
- Follow current user decisions over older drafts; distinguish existing behavior
  from intended contracts. Do not copy private paths, credentials, or unrelated
  evidence into reader-facing content.

## Browser capabilities

Use the current documented UI tool, such as `mcp__cua_repl`, and read its returned
documentation before acting. Honor an explicit browser choice; otherwise prefer
an available Codex in-app browser. Use that tool's prescribed entrypoint for a
mentioned tab, known tab, or new destination. Do not require an absent legacy
browser skill or assume CDP, arbitrary page evaluation, native desktop control,
file-chooser APIs, or hidden application interfaces exist.

For `cua_repl`, initialize with exactly one documented entrypoint call and inspect
the returned state. Use only APIs available on the selected browser/tab. DOM-only
tabs require their documented locators rather than native input wrappers. Re-read
state after actions and take a fresh screenshot before a coordinate action.

Cloud editing requires a usable current-state view, a supported insertion method,
and the ability to inspect the rendered result. Choose execution capabilities by
those requirements, not a fixed model name. If the required operation is unavailable,
complete the local package and report the precise blocked step. A missing login is
not permission to switch accounts or bypass authentication. Reuse the signed-in
session without reading cookies, credentials, storage, or browser profiles.

Parallelize local preparation and review; serialize mutations in a shared browser
session. Assign an exact page URL to each editing worker and verify its title and
initial content before the first write. Never infer ownership from the newest
untitled page or selected tab.

## Load details when needed

| Task | Reference |
| --- | --- |
| Rewrite conclusions for readers, remove conversation artifacts, choose a main narrative and appendices | [Editorial workflow](references/editorial-workflow.md) |
| Generate the package, paste native blocks, size tables, insert PlantUML, recover or verify publication | [Publishing playbook](references/feishu-publishing-playbook.md) |
| Use components beyond headings, prose, tables, code, Callout and UML Board; inspect nesting constraints | [Component selection and nesting](references/component-selection-and-nesting.md) |

Read the playbook before cloud publication. Load editorial or advanced-component
guidance only when that work is needed.

## Publication workflow

1. Freeze the reader-facing source, including any generated appendix. Use the local
   helper below or an established project generator; derive the manifest from the
   exact final payload. Multiple paste fragments need one reconciled ledger.
2. Inspect the target and establish Edit History before broad replacement. For a
   blank page, prove the main-document root focus with a harmless type-and-undo
   probe, then paste the complete ordinary body using a supported rich-text method.
   Do not target a generic or last `contenteditable`; it may be a comment composer.
3. Check the full outline, then process diagrams and tables in separate passes.
   Each diagram is atomic: find its slot, insert and preview, verify its location
   and adjacent heading, then delete the entire slot block. Adjust every table's
   outer width and content-aware columns; do not count an autofit click as proof.
4. Prefer native headings and numbering when supported. Keep body and diagram slots
   as ordinary sibling blocks, not children of a numbered-heading skeleton. Use
   `Insert Below` when a container does not support the desired nested component.
5. Save, reload, and reconcile the full ledger. Update the maintainable local source
   after cloud wording refinements so later publication does not restore stale text.

```powershell
python <skill-directory>/scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir> --dry-run
python <skill-directory>/scripts/prepare_feishu_publish.py <source.md> --output-dir <publish-dir>
```

Use an existing runtime with the Python `markdown` package. The helper only writes
local files; `--force` replaces generated files in the specified output directory.
Its schema-3 manifest inventories the final HTML, headings by level, visible code
blocks, diagrams, table layout, and source-derived code tails. See the playbook for
field compatibility and the configurable long-block threshold. A local render
does not prove that Feishu preserved that structure or rendered PlantUML correctly.

## Fragile operations

- Never use global `Ctrl+A` in a Feishu document, code block, or table editor;
  focus can escape and select the whole document. Prefer scoped block operations.
- Find PlantUML inside the opened UML Board's left-toolbar More/nine-dot menu,
  not the initial template panel. Reacquire the UI at every menu boundary.
- Use Board Style for simple diagrams and Classic Style for dense branching or
  long labels. After one bounded Board compatibility/layout correction, prefer
  Classic rather than repeatedly distorting valid DSL. Insert only a successful
  preview; do not silently substitute a static image for requested native UML.
- After broad accidental replacement, stop editing, restore the nearest known-good
  Edit History revision, reload and verify before retrying. On the assigned blank
  page this is covered by publication authority. Stop for direction if recovery
  cannot protect unrelated pre-existing content.

## Completion

After `Saved to cloud` and reload, verify the outline and heading levels, every
inventoried table's content and layout, every diagram's rendered drawing and
position, all visible code-block counts, and long or independently scrollable
code blocks through their tail markers and closing lines. Feishu virtualizes
off-screen blocks: combine outline, native Find and targeted navigation rather
than treating a first-screen snapshot as the full document.

Require zero temporary diagram slots, local paths or editing instructions in the
public page. Keep intentionally deferred markers. Reconcile adjusted/total tables,
rendered/total diagrams and heading/code totals with the exact final manifest;
unchecked or broken items make publication incomplete.

Return the Feishu page, maintainable local source and package, and a compact publish
record with actual verification, recovery actions, deferred items and blockers.
Distinguish local preparation from completed cloud publication.
