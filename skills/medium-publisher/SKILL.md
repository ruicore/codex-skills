---
name: medium-publisher
description: Create, edit, verify, or publish Medium stories through an authenticated browser. Use for Medium delivery and editor failures, not generic blog writing.
---

# Medium Publisher

Prepare the requested Medium story and verify its saved state. Drafting, publishing, scheduling, submitting to a publication, and sharing are distinct actions.

## Browser and authority

- Use the browser tools available in the session and their current documentation. With `mcp__cua_repl`, follow its documented entry point and returned runtime instructions; do not require a separately named Browser skill. Honor the user's selected browser and account. If none was specified, follow the tool's documented selection rules.
- Do not assume CDP, page JavaScript mutations, rich clipboard insertion, or file-chooser listeners are available. Use supported actions only. When a required operation is unavailable, preserve completed work and report the missing capability without inventing a bridge or silently switching browser surfaces.
- Reuse the authenticated session without inspecting authentication storage or credentials. If sign-in is unavailable, ask for access in the selected browser.
- Existing authorization continues for the requested cloud draft, edits, assets, and technical retries of the same action. Do not ask again merely because an editor action needs a retry. Follow applicable tool policy; ask when content, destination, audience, assets, or the requested action would exceed the authorized scope.
- A draft request does not authorize publication, scheduling, submission, or sharing. An explicit request for one of those actions can authorize it within its stated scope; this skill does not require an extra confirmation solely because the final control is reached. Check an uncertain outcome before retrying to avoid duplicate drafts or publications.

## Prepare the story

Identify the requested mode, intended story, text, assets, and destination from the conversation. Keep an authoritative local source when useful for a substantial article; a small existing-draft correction does not require a separate document. Preserve an unrelated existing story or draft.

Before entering text or uploading an asset, check its content, captions, alternative text, filenames, metadata, and links for credentials or unintended private information. Prepare sanitized material where needed; ask only if the disclosure or change in meaning exceeds the user's instructions.

Read [editor capabilities](references/editor-capabilities.md) when working in the editor, especially for illustrated stories or a failing control. Read [layout guidance](references/layout-recommendations.md) only when layout choices, image constraints, or distribution eligibility matter. Historical controls and limits must be checked against the live editor before relying on them.

## Draft workflow

1. Create or open the authorized story. Populate its native leading title separately: a heading pasted with body text can look like a title while leaving the actual title empty.
2. For text-only stories, a supported formatted insertion may be suitable. For illustrated stories, work from top to bottom: insert a complete section, add its related image at the verified tail, then establish the next paragraph. Do not backfill text across existing images unless the insertion point is established; visible focus has not reliably positioned the caret.
3. Use the current native formatting controls or a documented formatted-input action. Whole strings containing Markdown headings, list markers, or fenced code have not converted reliably through automated input.
4. Add only in-scope visuals or embeds. For local images, establish an active empty paragraph and verify both the `+` control and expanded image control are interactable before using the tool's supported upload action. The detailed historical readiness and caret checks are in the editor reference; no file-chooser or DOM API is assumed available.
5. After media, caption, alt-text, or layout changes, verify the insertion point before adding more text. If the current tool cannot establish it, stop further insertion rather than risk writing into the title or caption.
6. Inspect save confirmations and error banners together. `DraftSaved` has appeared alongside `Story could not be saved`; wait and re-read the state before retrying. Autosave is not publication.
7. Reload and verify the saved story: native title identity, absence of a duplicate body title, headings, paragraphs, lists, code, image order, links, captions, and alt text. Read actual saved values back rather than trusting a closed dialog or successful tool call.

If a required media or formatting operation fails, preserve the usable draft and identify the incomplete requirement. A text-only draft may be useful progress but is not a completed illustrated-story request. Report observed capabilities separately from unverified ones.

## Publication workflow

1. Check that the requested action and intended content, destination, topics, audience, and schedule are covered by the existing authorization. Resolve material omissions or changes before executing; do not repeat an already settled approval.
2. Inspect the live publication settings. The editor has exposed preview title, subtitle, topics, publication submission, `Publish`, and `Schedule for later`; controls and limits can change. Do not claim SEO, canonical URL, or other settings are available without seeing them.
3. Use a supported action to publish, schedule, or submit only as requested. A draft-only task ends at the verified draft.
4. Verify the resulting URL and publication, schedule, or submission state. If the result is uncertain, inspect existing state before any retry rather than risking a duplicate.

Do not use publication as an editor troubleshooting experiment or as part of skill maintenance. After recovery, an already authorized publication may continue with the checks above. If distribution or reach is part of the request, consult current Medium guidance through the layout reference and do not promise eligibility or misrepresent authorship.

## Failure handling

- Inspect the actual UI state after a failed action. A targeted supported recovery can continue under the same authorization. Stop after two failed recoveries of the same menu or insertion-point failure, or earlier if the draft state becomes uncertain.
- Distinguish an inactive menu, unavailable upload API, chooser failure, and save failure. Do not infer a network fault from an editor failure or change system DNS/proxy settings to repair the editor.
- Report the exact unsupported action or access barrier and the work that remains. Do not fall back to historical CDP, DOM mutation, or undocumented clipboard recipes.
