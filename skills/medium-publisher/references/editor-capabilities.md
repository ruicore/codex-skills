# Medium editor capabilities and failure boundaries

These observations come from earlier authenticated editor checks. Treat the current editor and browser tool documentation as authoritative; a historically successful interaction does not establish that the present tool supports it.

## Observed platform behavior

| Area | Historical observation |
| --- | --- |
| Draft saving | Stories reached `DraftSaved` and a persistent `/edit` URL. A draft could temporarily show `Story could not be saved` at the same time; wait and inspect both states before retrying. Autosave is not publication. |
| Title and headings | The native leading title is distinct from body headings. The selection menu exposed large and small heading controls, represented as `h3` and `h4`. |
| Text blocks | Paragraphs, lists, quotes, links, and formatted code could persist, but whole-string Markdown shortcuts did not reliably convert during automated input. |
| Insert menu | An active empty paragraph exposed a left-side `+` for images, Unsplash, video, embed, code-block, and new-part controls. |
| Image accessibility | Figures exposed captions and an `Alt text` control. A closed Save dialog did not always prove the value persisted; read it back. |
| Image placement | Selected images exposed inset/normal, outset/wide, and fill-width choices. Controls could lack accessible labels; do not infer their meaning from position or an internal value. |
| Publication panel | Preview title and subtitle fields, estimated read time, topics, submission, publish, and schedule controls were visible. Historical limits were 100 title characters, 140 subtitle characters, and five topics; check the current editor before relying on them. |

## Writing order and native title

Formatted whole-body insertion preserved text structure but removed empty image-anchor paragraphs. Later image backfill could therefore land at the wrong position. Media-first drafting followed by earlier text backfill and repeated typing after media both produced caret drift into a title or caption.

The demonstrated illustrated-story approach was to populate the native title first, insert one complete section, add its image at the verified tail, and establish a new tail paragraph before continuing. The resulting structure, captions, and alt text survived reload. Apply this ordering only through actions supported by the current tool.

A header-rich block pasted into an empty editor once left `graf--title` empty while inserting a convincing body H3. Verify the native title, the story's page identity after reload, and the absence of a duplicate body title. Exact tab-title punctuation and class names are diagnostic clues, not universal selectors.

## Image upload readiness

1. Establish an empty paragraph at the intended location. Verify that the `+` is interactable, not merely present in a DOM snapshot. In the affected UI it initially had zero geometry and became active after an animation.
2. Open the menu and verify that the local-image control is interactable. An expanded menu could still have a zero-size image button during its animation. Use supported live state or visual inspection, not a fixed delay as proof.
3. Use the current tool's documented upload operation. Only if it documents a file-chooser listener should one be registered before the click, with rejection handled. The old listener API is not assumed available. If no supported upload path exists, report that limitation rather than injecting an upload or building a bridge.
4. Require the intended image in a figure and a consistent saved state. Chooser completion alone is not an uploaded or saved image.
5. Add captions and alt text within the authorized scope, then read their saved values back from the figure. Verify their persistence after reload.

The historical menu parent used `is-scaled` to indicate readiness. Read-only DOM inspection may help when the current tool allows it, but neither that class nor an exact geometry is required across editor versions.

If readiness fails, re-establish the empty paragraph and retry once through supported actions. Distinguish menu readiness from a missing upload capability or a chooser failure. Stop after two failed recoveries or sooner when the insertion location is uncertain. Do not treat such failures as a reason to change network settings.

## Insertion point after media

After an image, caption, alt-text edit, or layout change, verify where new text will land. A visible click below a figure has not reliably moved the contenteditable caret. A documented end-of-document key action followed by inspection has helped in past tooling, but key names and targeting must come from the current tool.

When a caret probe is needed and ordinary text entry/removal is supported within the authorized draft, use one unique printable character absent from the article. Verify it is the sole content of the intended final paragraph, outside the title, figures, and captions. Remove it with the supported single-character delete action and confirm no occurrence remains before continuing. Do not use a multi-character marker or broad line/word selection: partial cleanup previously contaminated a heading. If the tool cannot verify both placement and removal, do not use this probe.

Stop after two failed recoveries rather than inserting more content at an uncertain location. Explicit-marker replacement remains unverified and is not a default recovery path.

## Capabilities to inspect live

- Unlabeled image placement buttons and multi-image layouts must be identified from current state, not guessed by position.
- Seeing an embed, code-block, or new-part menu item does not prove its operation has completed successfully.
- SEO, canonical URL, and a standalone preview field were not found in the historical panel; do not claim they exist or are absent today without inspection.
- Rich insertion, file chooser events, CDP, and page JavaScript mutation are separate tool capabilities. A historical editor success authorizes none of them by itself.

## Authorization and outcome checks

Continue the user's authorized draft edits and same-action technical retries without repeated confirmation. Drafting, publishing, scheduling, submission, and sharing remain distinct: execute only the action and content within the user's scope, and resolve material changes before proceeding. Follow the active tool's policy when it imposes an additional requirement.

Check for an existing draft, saved change, or published result before retrying an action with an uncertain outcome. Final verification requires the saved artifact, not only a transient DOM match or a success string. Do not publish during editor diagnosis or skill maintenance.
