# LinkedIn Shadow DOM failure reference

Use this reference after normal composer actions reproduce a focus error or a click that leaves the UI unchanged. These are historical observations, not a promise about the current editor or an instruction to use unsupported APIs.

## Recognize the failure

An affected composer used an open Shadow Root hosted by `div#interop-outlet`. The top-level active element was the Shadow Host while the actual focused editor was its `shadowRoot.activeElement`, labeled `Text editor for creating content`.

Observed symptoms included:

- `Active element is no longer the expected input target` during text entry.
- `fill`, typing, paste, or key presses failing or making no change.
- `Next`, `Add media`, `Dismiss`, or `Save as draft` reporting a successful click without advancing the UI.

When the current browser tool supports read-only DOM inspection, use it to distinguish the host from the focused inner editor. Otherwise inspect the available accessibility state and screenshots. Do not claim a Shadow DOM root cause from a generic failed click alone.

## Recover through supported actions

1. Re-read the current browser tool documentation and observe the live composer. Use supported focus, text-entry, and click actions that can reach the exact intended control. Stop on ambiguous targets or an unexpected dialog.
2. For an image post, the Feed-level `Photo` control historically opened uploads outside the affected Shadow Root. Use it only if returning there will preserve the current draft and the selected tool supports the upload operation.
3. If the tool documents a file-chooser event, register its waiter before clicking and handle rejection. Otherwise use its documented upload action. A file-chooser or CDP API from an older runtime must not be assumed available.
4. After a failed attempt, inspect what changed before retrying. A verified no-op can be retried through another supported action within the same authorization. If a targeted recovery still fails or the outcome is uncertain, preserve the draft and report the exact failed control and missing capability.

Older tooling successfully used CDP to target shadow-root buttons and `document.execCommand("insertText")` to preserve editor semantics. Those observations explain the failure boundary; they are not a current fallback recipe. Do not inject those mutations, build an alternate bridge, or assign `innerHTML` or `textContent` merely because ordinary input failed. Visible DOM changes can disagree with the editor's saved framework state.

LinkedIn also historically accepted a share URL plus commentary before the Shadow DOM composer mounted. Do not use that as an automatic bypass or add dummy URLs: it can create an unintended link preview, and putting draft text in a navigation URL changes where it may be recorded.

## Verify text, media, and persistence

LinkedIn has represented each input line as a paragraph and blank lines as `<p><br></p>`. A flattened `innerText` value can therefore contain extra newlines. Compare all logical paragraphs with the intended text, normalizing only that representation and platform line endings. Do not accept a prefix match. Use supported read-only inspection or visible review; do not mutate the document to make comparison easier.

Verify media independently. Historical signals included a `Remove media` button and an image named `Image preview`, `View image`, or the uploaded filename; use the current visible content rather than hard-coding those labels as universal requirements.

Saving has used a `Dismiss` action followed by a distinct `Save as draft` prompt. Observe the intermediate prompt before proceeding. Never broaden an ambiguous selector to `Post` or combine unobserved state transitions into one action.

After the save confirmation, reopen the `Draft:` entry and repeat full text and media checks. The confirmation historically arrived several seconds after composer closure. If persistence cannot be verified, say so rather than treating the closed composer as success.

Draft troubleshooting does not authorize publication. Existing authorization for the same draft action remains valid during supported technical retries; changes to the content, audience, destination, or requested action require their own scope decision.
