---
name: linkedin-publisher
description: Create, edit, verify, or publish LinkedIn posts through an authenticated browser. Use for LinkedIn delivery or composer failures, not generic social copy.
---

# LinkedIn Publisher

Prepare the requested LinkedIn draft or post, preserving its text, media, audience, and publication authority.

## Browser and authority

- Use the browser tools actually available in the session and read their current instructions. With `mcp__cua_repl`, follow its documented entry point and returned runtime documentation; do not require a separately named Browser skill. Honor the user's selected browser and account. If no browser was specified, use the tool's documented selection rules.
- Do not assume CDP, page JavaScript mutations, clipboard insertion, or file-chooser listeners are available. Use only actions supported by the selected tool's current documentation. If a required action is unavailable, report the missing capability and the remaining work rather than recreating an old bridge or switching browsers silently.
- Reuse the signed-in session without inspecting authentication storage or credentials.
- Existing authorization continues for the requested draft creation, edits, media, and technical retries of the same action. Do not ask again merely because the tool or editor needs another attempt. Follow any applicable tool policy; ask when the content, destination, audience, assets, or action would exceed the authorized scope.
- Draft authorization does not authorize posting. An explicit publication request can authorize posting within its stated scope; do not impose an additional confirmation solely because this skill loaded. Before any uncertain retry, check whether the draft or post already exists to avoid duplication.
- Inspect the Feed-level `Start a post` control for an existing `Draft:` preview. LinkedIn may restore that draft instead of creating an isolated one. Preserve an unrelated draft unless the user has authorized editing or replacing it.

## Prepare the payload

Use the user's requested length and style. A teaser should identify its useful finding and link to the full article; a self-contained post may need more detail. The live composer and current [LinkedIn Help](https://www.linkedin.com/help/linkedin/answer/a528176) determine platform limits.

Before entering text or uploading media, check the actual payload, including alternative text, filenames, screenshots, metadata, and link previews, for credentials or unintended private information. Use an appropriate sanitized asset when needed. Ask only when sanitization or disclosure would require a choice outside the user's instructions. A local file's location does not establish that it is suitable for publication.

## Draft workflow

1. Identify the intended text, media, link, audience, and whether the request ends at a draft or a published post.
2. Open LinkedIn Feed in the selected signed-in browser and inspect any existing draft before starting.
3. Prefer the visible `Start a post` flow for text-only posts. For images, the Feed-level `Photo` flow has avoided composer-specific upload failures. Use a currently documented upload action with the authorized local file; do not assume a file-chooser API exists. If the tool documents an event waiter, register it before the triggering click and handle rejection.
4. Enter the text, attach the intended media, and set the authorized audience and alternative text. After each action, inspect the resulting state rather than treating a successful tool call as proof.
5. Save the draft through the current visible controls and reopen it to verify persistence. If publication is authorized, continue to the publication checks below.

If the composer rejects input or a button becomes a no-op, read [the Shadow DOM failure reference](references/shadow-dom-workaround.md). Preserve the draft and report a precise blocker when supported actions cannot complete the task. Do not leave test text, dummy URLs, duplicate media, or an unintended link preview.

## Verification and publication

Before saving or posting, verify:

- The full logical body matches the intended source, allowing only platform line-ending representation differences.
- The intended media, alternative text, audience, and link preview are present, with no unintended disclosure.
- The current action matches the user's authorization. An enabled `Post` button alone is not authority to click it.

A transient editor match is not persistence proof. After saving, look for the save confirmation (historically `Draft successfully saved.`), reopen the draft, and repeat the content and media checks.

For an authorized publication, use the supported `Post` interaction and verify the resulting post or publication confirmation and URL. Composer closure alone does not establish success. If the outcome is uncertain, inspect the feed or existing post before retrying; do not risk creating a duplicate. A different supported technical action for the same authorized result does not itself require fresh confirmation.

Report the resulting draft or post, verification performed, and any remaining limitation. Do not use publication as a troubleshooting experiment or as part of skill maintenance or a draft-only request. After recovery, an already authorized publication may continue with the checks above.
