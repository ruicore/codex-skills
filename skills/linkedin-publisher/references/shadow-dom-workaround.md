# LinkedIn Shadow DOM workaround

Use this reference only after the normal LinkedIn composer flow has reproduced the `#interop-outlet` focus or click failure.

## Confirm the failure

Read the page state without changing it:

```javascript
const host = document.querySelector("#interop-outlet");
const deep = host?.shadowRoot?.activeElement;

({
  hostExists: Boolean(host),
  shadowMode: host?.shadowRoot?.mode,
  topActive: document.activeElement?.id,
  deepActive: deep?.getAttribute("aria-label"),
  contenteditable: deep?.getAttribute("contenteditable"),
});
```

The known failure signature is:

```text
topActive  = interop-outlet
deepActive = Text editor for creating content
```

The browser believes the host is focused while LinkedIn correctly focuses the inner editor according to Shadow DOM semantics.

## Text-only posts with an intended link

LinkedIn can prefill commentary before the Shadow DOM editor mounts:

```text
https://www.linkedin.com/feed/?shareActive=true
  &url=<encoded-destination-url>
  &shareUrl=<encoded-destination-url>
  &text=<encoded-post-text>
```

Use this only when the post is intentionally sharing that URL. LinkedIn will attempt to create a link preview. Do not use a dummy or invalid URL in a real draft: it may leave an unwanted preview state or dead link.

The `text` parameter without a valid shared URL did not reliably open the composer in the tested UI.

## Image plus text: verified fallback

### 1. Upload from outside the Shadow Root

Navigate to LinkedIn Feed and use the Feed-level `Photo` button. It remains in the normal document and reliably opens the file chooser.

Start `waitForEvent("filechooser")` before clicking `Photo`, attach a rejection handler immediately, and upload the absolute local path. Verify that the media editor shows the intended filename or preview.

Do not rely on `Add media` inside the affected composer; it may report a successful click without opening the chooser.

### 2. Advance the media editor

If the visible `Next` button is a no-op, use the tab's documented CDP capability to query the open Shadow Root and click exactly one enabled `Next` button.

Before acting, assert:

```javascript
const root = document.querySelector("#interop-outlet")?.shadowRoot;
const buttons = [...(root?.querySelectorAll("button") || [])]
  .filter(button => button.getAttribute("aria-label") === "Next");

({ count: buttons.length, disabled: buttons.map(button => button.disabled) });
```

Proceed only when `count === 1` and the button is enabled. Stop on zero or multiple matches.

### 3. Insert text through editor semantics

Do not assign `innerHTML` or `textContent`. LinkedIn's editor maintains framework state and applies Trusted Types and structured paragraph behavior; raw assignment can produce a visually changed DOM that is not represented in the saved post.

Instead, focus the real editor, select its existing contents, and use the native editing command:

```javascript
const root = document.querySelector("#interop-outlet")?.shadowRoot;
const editor = root?.querySelector(
  '[aria-label="Text editor for creating content"]',
);

if (!editor) throw new Error("LinkedIn editor not found");

editor.focus();

const selection = window.getSelection();
const range = document.createRange();
range.selectNodeContents(editor);
selection.removeAllRanges();
selection.addRange(range);

document.execCommand("insertText", false, approvedText);
```

When constructing a CDP expression, serialize `approvedText` with `JSON.stringify`. Do not interpolate unescaped text into executable source.

This command was verified to create LinkedIn paragraph nodes and hashtag nodes and to survive saving and reopening the draft.

### 4. Verify logical text

LinkedIn represents every input line as a paragraph. Blank lines become `<p><br></p>`, while `innerText` can appear to contain extra newlines. Compare the logical content instead:

```javascript
const logicalText = [...editor.children]
  .map(paragraph => paragraph.innerHTML === "<br>" ? "" : paragraph.innerText)
  .join("\n");
```

Require `logicalText === approvedText` after normalizing only platform line endings. Do not accept a prefix check for publication.

Verify media independently through both of these signals when available:

- Exactly one `Remove media` button.
- An image whose accessible name is `Image preview`, `View image`, or the expected filename.

### 5. Save and prove persistence

Use the exact composer `Dismiss` button to open the save prompt. Assert that exactly one `Save as draft` button exists, then activate it.

In the 2026-08-25 composer, normal browser clicks for both `Dismiss` and `Save as draft` were visible but became no-ops under the confirmed Shadow DOM failure signature. When that exact failure is reproduced and draft saving is authorized, use the documented CDP capability to click these buttons one at a time:

1. In the open Shadow Root, require exactly one button whose accessible label or trimmed text is `Dismiss`, then click it and re-read the root.
2. Require exactly one `Save as draft` button in the resulting prompt, then click it and wait for the success toast.
3. Stop on zero or multiple matches, a disabled target, or any unexpected dialog. Never broaden either selector to `Post` or another action.

Do not combine the two clicks into one expression. The save prompt is an intermediate state that must be observed before the second mutation.

Wait for:

```text
Draft successfully saved.
```

The toast can arrive several seconds after the composer closes. Reopen the `Draft:` entry through `Start a post`, then repeat the exact logical-text and media checks.

## Safety boundaries

- Lower-level page actions directly modify the unsent draft. Disclose their use in the final response.
- Match exact accessible labels and require exactly one target before every lower-level click.
- Never select or click `Post` as part of diagnosis, draft creation, or fallback testing.
- Do not leave dummy URLs, test strings, duplicate media, or invalid link-preview warnings in the final draft.
- If LinkedIn changes its DOM, stop rather than broadening selectors until the new state has been inspected.
