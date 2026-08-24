# Medium editor capabilities: verified baseline

This reference records what was observed in an authenticated Medium editor on 2026-08-24. Treat the live editor as authoritative because the UI can change.

## Verified directly

| Area | Observed behavior |
| --- | --- |
| Draft saving | New stories reached `DraftSaved` and a persistent `/edit` URL. One draft briefly showed `Story could not be saved`, then independently settled to `DraftSaved`; wait and re-read state before retrying. Autosave is not publication. |
| Title and headings | The initial title and typed `#` / `##` shortcuts rendered as `h3`-style blocks. The selection menu exposed a large heading (`h3`) and a small heading (`h4`). |
| Text blocks | Normal paragraphs, unordered lists, and block quotes were inserted successfully. |
| Selection menu | Bold, italic, link, `h3`, `h4`, quote cycling, and highlight were visible. The link field accepted pasted or typed URLs. |
| Insert menu | On an active empty paragraph, clicking the left-side `+` expanded local image, Unsplash, video, embed, code-block, and new-part controls. |
| Local image upload | After expanding the `+` menu, clicking `Add an image` triggered a multi-file chooser. Supplying an absolute local PNG path created a Medium figure and the draft reached `DraftSaved`. |
| Image accessibility | The uploaded figure exposed a caption placeholder and an `Alt text` button. The alt-text dialog accepted a description, and saving it updated the image's accessible name. |
| Image placement | Selected images exposed inset/normal (`imageInsetCenter`), outset/wide (`imageOutsetCenter`), and fill-width (`imageFillWidth`) controls. The buttons did not consistently expose accessible labels. |
| Video | The dialog requested a YouTube, Vimeo, or other video link followed by Enter. No link was submitted during the test. |
| Publication panel | Preview title (100 characters), subtitle (140 characters), estimated read time, topics (maximum five), publication submission, final publish, and schedule controls were visible. |

## Drafting experiment findings (2026-08-24)

These findings are directly observed failure boundaries, not general claims about every future Medium editor version.

- Atomic formatted whole-body insertion preserved headings, a list, and a code block. Medium removed the intentionally empty image-anchor paragraphs, however, so later image backfill landed at the wrong positions. The draft then showed both `DraftSaved` and a persistent `Story could not be saved` banner.
- Media-first drafting followed by text backfill was unsafe. Clicking or visibly focusing an earlier block did not reliably move the contenteditable caret; subsequent text could enter the story title or an image caption.
- Per-block incremental automated typing after media also drifted between blocks. Whole strings containing Markdown headings, repeated list markers, or fenced code did not convert reliably through automated input.
- An alt-text Save action did not always persist on the first attempt. A caption could exist in the figure DOM while its field was not currently visible. Read both values back from the selected figure.
- Explicit-marker replacement was not completed successfully and remains unverified.
- Windows DNS resolution and TCP 443 connectivity to Medium were healthy during the second validation. An unauthenticated HTTP `HEAD` returned 403, which indicated access control rather than broken connectivity. Do not mutate OS DNS, proxy, or network settings when DNS and TCP checks are healthy.
- Clicking a visually empty paragraph after a figure did not reliably move the caret: a multi-character sentinel landed in the title. `ControlOrMeta+End` on the article textbox, followed by DOM re-reading, did place a sentinel in the final paragraph after the figure in the tested UI.
- Multi-character sentinel cleanup with line or word selection was unreliable and left partial text. A subsequent rich section paste preserved an H4, three list items, an H3 repair heading, and paragraphs, but the residual marker degraded its first heading. Zero remaining sentinel occurrences is therefore a hard gate.
- The previously repeated chooser failures were reproduced as premature interactions with Medium's animated insert menu. After tail positioning, the `+` existed in the DOM but was initially hidden at `0 x 0` with a zero transform. It became a visible `32 x 32` control after about 250 ms. After clicking it, the local-image button again remained `0 x 0` until the menu parent gained `is-scaled`; clicking before that state timed out, while waiting for that state opened the chooser successfully. This evidence reclassifies those reproductions as menu-readiness failures rather than authentication, network, or chooser-bridge failures.
- A complete illustrated section-hybrid draft succeeded with two local images, 11 primary headings including the native title, one subtitle, 39 list items, and two code blocks. Reload preserved the structure, captions, and alt text.
- Pasting a header-rich block into a blank editor left the leading `graf--title` empty and inserted the apparent title as an ordinary H3; the tab remained `New story`. The draft required repair. Populate the native title separately, then reload and require an `Editing <title> - Medium` page title (punctuation may vary), an exact leading title block, and no duplicate title in the body.

The verified illustrated-story workflow is top-to-bottom and section-hybrid: populate the native title first; insert one complete formatted section; add its related image immediately at the verified tail; then establish and verify a new tail paragraph before continuing. A two-image article completed this workflow and survived reload with its structure, captions, and alt text intact.

## Verified local-image procedure

1. Place the caret in an empty paragraph at the intended image position, normally by sending `ControlOrMeta+End` to the article textbox. Poll the live control state until the left-side `+` has nonzero geometry (observed `32 x 32`), is CSS-visible, has a nonzero transform, and its menu parent is active. Do not rely on DOM presence or a generic `isVisible()` result: the inactive control can be present yet remain `0 x 0`.
2. Click that ready `+` button. Poll again until the menu parent includes `is-scaled`, the `Add an image` button has nonzero geometry and a nonzero transform, and no overlapping element owns its center point. Do not use a fixed delay as the success criterion; the observed transition took about 250 ms but live state is authoritative.
3. Only after the image button is interactable, start waiting for the file chooser and immediately click the button. Attach a rejection handler to the wait before clicking so a timeout does not become an unhandled automation error.
4. Supply the authorized file by absolute path. The observed chooser accepted multiple files, but use one file unless a grid is intentional.
5. Wait for a figure containing the uploaded image and for `DraftSaved`; do not treat chooser completion alone as a successful upload. If a save-error banner appears, wait and re-read the editor before retrying. Require the banner to clear.
6. Select the figure, open `Alt text`, enter the accessible description, and save it. Enter the plain caption in the figure's `Type caption for image (optional)` field.
7. Read the image's accessible name and caption back from the live figure. Do not infer success from the dialog closing or from `DraftSaved` alone.

If either readiness stage does not complete, first re-establish the active empty tail paragraph and repeat the sequence once. Record this as a menu-readiness failure. If both controls were demonstrably interactable but the chooser still did not open, record a chooser failure. After two failed attempts, stop. Do not label either case a network failure when DNS and TCP checks are healthy, and do not change OS DNS, proxy, or network settings to recover the editor.

## Verify the active insertion point after media

After an image upload, alt-text edit, caption edit, or layout change:

1. Do not trust a visual click on an empty paragraph after a figure. Attempt tail positioning with `ControlOrMeta+End` on the article textbox, then re-read the DOM.
2. Type one unique printable character absent from the article, such as `⟡`. Confirm it is the sole content of the last paragraph, outside the title, every figure, and every caption, and after the intended preceding block.
3. Remove the character with exactly one Backspace. Confirm zero occurrences remain in the entire article before inserting the next formatted section; this is a hard gate.
4. Do not use Shift+Home, word selection, line selection, or a multi-character marker for cleanup. If verification or recovery fails twice, stop rather than cross an image or continue in an uncertain block.

## Not verified; inspect live before relying on it

- Multi-image layouts. The three single-image placement controls above were observed, but their unlabeled live buttons must be identified from current editor state rather than guessed by position or internal value.
- Functional completion of embed, code-block, and new-part insertion. Their entry points were visible, but the blocks were not inserted in the test.
- A dedicated SEO, canonical URL, or standalone preview control. None was visible in the tested publication panel.

## Safety controls

- `Publish`, `Schedule for later`, and publication `Submit` are terminal actions. They require a fresh, explicit user confirmation immediately before the click.
- Creating or materially editing a cloud draft is also an external write. Follow the active browser-control policy for confirmation.
- Never upload a local file or image without exact user approval. Prefer a text-only draft when visual assets are not approved.
