# Evidence And Validation

Read this reference when a Feishu issue contains screenshots, attachments, logs, downloaded projects, customer data, or a request to reproduce or validate behavior.

## Rendered Bug Work-Item Evidence

Treat the rendered work-item title or name as the primary scope and symptom. Feishu Project work-item types and templates can use different field names for the same diagnostic role, so map visible evidence into semantic slots while preserving the original field label or narrative source:

- **Version and environment baseline:** version, build, commit, branch, deployment, hardware, configuration, or readable version-screenshot evidence, separated by owning component when multiple components participate.
- **Trigger and execution path:** reproduction steps, user action, job, scene, configuration combination, timing, or other conditions that reach the reported path.
- **Observed outcome:** error, missing or incorrect output, crash, latency, state transition, log event, or other reported failure signal.
- **Expected outcome and acceptance:** the intended behavior or exact signal that would prove reproduction or repair. Keep this separate from the observed outcome; mark it missing when it is not stated.
- **Supporting evidence:** relevant descriptions, logs, files, screenshots, comments, links, and lifecycle information.

`测试版本：` / `复现步骤：` / `结果：` is one known template pattern, not a required contract. Other bug templates may expose the same roles through labels such as software version, version screenshot, problem description, job or scene, key logs, or key files, or combine several roles in narrative text. Do not report a semantic slot as missing merely because one candidate label is absent.

Do not assume a flattened API description contains image evidence. Do not infer screenshot content from its URL or thumbnail.

## Discover Template Fields Progressively

Start with the rendered title, work-item type or template when visible, section headings, non-empty field labels, and the smallest relevant narrative. Build a compact candidate map from original labels to the diagnostic slots above, then open only the screenshots, comments, attachments, or structured fields needed to resolve the remaining slots.

Use read-only structured Feishu Project tools to cross-check visible labels, values, and metadata when useful, but do not request every custom field or use an `_all` query by default. An unfamiliar template is a reason to inspect its visible structure first, not to bulk-collect the entire work item. A request for complete issue evidence means complete evidence relevant to the reported bug and its lifecycle, not every unrelated business or administrative field.

### Resolve Image- And File-Valued Fields

For every diagnostically relevant rendered field, record one of these states before deep diagnosis: scalar value, explicit empty state, resolved media value, unresolved media value, or sensitive exclusion. Apply this to any field that can carry baseline, trigger, observed-outcome, expected-outcome, log, or configuration evidence, regardless of the template's field name.

A field label followed by no flattened text is not an explicit empty state when the rendered value area contains or may contain an image, file, preview, canvas, or other media node. Associate media with a field through its rendered field container, nearby visible label and value region, structured field membership, or another authoritative page relationship. Do not rely on a filename, `alt` text, URL shape, source order, or image dimensions alone; custom-field media may expose none of them.

Open resolved field media at a readable size and extract only the evidence needed for the issue brief. If ownership remains ambiguous after bounded inspection, record the field as unresolved with the exact coverage gap. A baseline-related unresolved media field blocks code-ref selection just as an unreadable version string does. Sensitive fields remain excluded under the rules below rather than being opened merely to complete the inventory.

Treat fields whose labels or values indicate passwords, temporary access codes, remote-control credentials, tokens, private contact details, or other secrets as sensitive before reading their full value. Do not request or expand them unless their content is strictly necessary and separately authorized. If a read-only source returns such a value incidentally, redact it immediately; do not print, persist, index, or include it in the issue brief. Record only that a sensitive field exists and whether it is relevant to a blocked validation step.

## Comments And Remarks

Treat the Chinese `评论/备注` tab and the English `Comments` tab as localized labels for the same evidence surface. Prefer a tab-role or exact visible-text locator that supports the active locale. Do not rely on `tabKey=comment`, an anchor, a comment-count button, or the requested URL alone: Feishu may still render the Description tab. After selecting the tab, confirm the active state from the rendered comment list, its empty state, or an equivalent visible signal.

If the comments surface exists, collect all available issue evidence before deep diagnosis:

- author and rendered timestamp;
- comment text, lists, links, mentions, reply target, and edited state when exposed;
- embedded images or files in their rendered order;
- the association between each embedded artifact and its owning comment.

Do not treat avatars, reaction icons, application chrome, or unrelated page assets as comment evidence. Rich-text DOM snapshots may contain the comment text while omitting embedded images. Inspect image nodes within each comment container and use their ancestry, rendered position, dimensions, and surrounding comment context to distinguish evidence from decoration.

For comment-embedded images, prefer a browser media download that exposes a completed download event and a real local path. A dynamic Feishu comment page may omit these images from a page-assets inventory, so inventory-based acquisition is an option, not the only allowed mechanism. Do not navigate directly to or persist signed media URLs merely to download the image.

Store every captured comment under the same verified ignored or external issue root used for other private artifacts. Write a normalized, sanitized index that maps author display name, rendered time, text, reply relationship, ordinary links, and image filenames; do not persist a raw structured response merely to preserve the comments. Use stable local image names based on comment order or rendered timestamp. Download every image proven to belong to a comment, verify that it is non-empty and decodable, record its real format and dimensions, and inspect enough actual content to rule out thumbnails, avatars, placeholders, or unrelated assets. State whether all rendered comments and comment images were captured; if lazy loading, pagination, permissions, or service limits prevent complete capture, report the exact coverage and blocker.

When Feishu displays a comment badge or structured comment count, compare it with the number of distinct rendered comments actually captured. If the counts differ, make bounded attempts to scroll the comment container to both ends and activate a visible load-more or pagination control, then recount after the surface becomes stable. Do not invent missing comments or loop indefinitely. Preserve all three signals when available: displayed count, structured returned count and continuation metadata, and rendered captured count. A mismatch remains an explicit coverage gap unless a rendered explanation accounts for it.

## Activity And Work Progress

Treat `操作记录` and `Activity Log` as localized labels for the activity surface, and `工作进展` and `Work Progress` as localized labels for the progress surface. Inspect them when the user asks for complete issue evidence or when status, ownership, attachment, title, relation, or workflow history could change the diagnosis.

- Preserve rendered timestamps, actors, field or role names, old and new values, and linked-item names when present.
- Keep separate activity rows even when Feishu emits both a field-level event and a work-item-level event for one status transition.
- Record the number of rendered rows and whether pagination, lazy loading, filters, or an inaccessible older range limit coverage. Do not label visible rows as the complete history without a coverage signal.
- Treat an explicit empty state such as `No data yet` as evidence; do not infer missing progress from an unselected or still-loading tab.
- Store a concise activity index when it materially helps reconstruction. Do not recursively fetch linked work items by default; preserve their identifiers and names, then expand only when requested or necessary for the issue path.

When a read-only structured activity source is available, preserve three separate coverage signals: browser-rendered rows or explicit empty state, actual records returned by the structured source, and its `total` / `has_more` / continuation metadata. A rendered `No Result` does not erase returned API records; `total=0` does not erase a non-empty record array; and `has_more=false` only says there is no exposed continuation signal, not that every historical event is proven complete. If these signals disagree, write a sanitized row-level activity index with actor, rendered or returned time, module or field, old/new summary, and the discrepancy. A selected tab that is merely blank is a coverage gap, not an empty state.

## Local Artifact Handling

Discover the repository's ignored local evidence location. For processing service, the default candidate is `.manifest/issue-artifacts/<issue-id>/`; other repositories may use different names.

Before writing private evidence, verify that the proposed path is actually ignored by Git, for example with `git check-ignore`. A candidate directory name is not proof. If the path is not ignored, use another verified ignored local root or an external temporary directory. Do not edit `.gitignore` merely to store issue evidence unless the user separately authorizes that repository change.

Unless the user explicitly requests an access-only or download-capability check, or explicitly says not to download, persist the investigation evidence locally by default:

1. Create an issue-specific directory under the verified ignored or external evidence root. Record the acquisition time and, when exposed, the observed work-item update time.
2. Save a sanitized issue brief with the original field-label or narrative provenance for each semantic slot.
3. Save a normalized, sanitized index for every captured comment, download every non-sensitive image proven to belong to a Description or comment, and download every diagnostically relevant non-sensitive image-valued custom field. Do not limit Description or comment image retention to evidence already judged relevant; its value may emerge during later analysis.
4. Inventory every visible attachment with its source surface, filename, type, declared size, and acquisition state. Download attachments that can materially support reproduction, diagnosis, or validation. For a large, blocked, or clearly non-diagnostic attachment that is not downloaded, retain its metadata and the reason instead of pretending acquisition was complete.
5. Save a sanitized activity or work-progress index whenever those surfaces were inspected and materially affect the lifecycle account.
6. Preserve stable local names, byte lengths, real formats, dimensions or archive integrity, and SHA-256 when inexpensive. Keep a mapping from page evidence to final local files.
7. Reuse an already verified artifact when size or checksum matches. When the live work item has changed, retain a new acquisition record or run-specific snapshot instead of silently overwriting the prior evidence.
8. If saving, downloading, or opening fails, say exactly what was not retained and ask the user to provide it when it is required for diagnosis.

Retain final evidence by default. Automatic cleanup applies only to exact task-created staging files and bundle directories after promotion and validation; it never deletes the verified issue brief, comment index, final images, final attachments, or validation metadata.

This skill never modifies the Feishu issue or publishes evidence. Downloading evidence, a local-code implementation request, or any other task authority does not permit issue fields, status, comments, attachments, relations, work progress, or forms to be changed.

The read-only boundary is remote-only. The verified local evidence root is a writable investigation workspace: create and update briefs, indexes, snapshots, hashes, validation records, and organized final artifacts there as needed. Keep those writes scoped to the issue root, preserve provenance, and do not confuse local evidence maintenance with authority to mutate Feishu.

Never persist or expose cookies, tokens, authorization headers, credentials, customer identifiers unnecessary to the diagnosis, full authenticated commands, complete page HTML, or unfiltered structured API responses. Keep necessary private evidence in ignored local storage. Durable summaries and indexes should be concise and sanitized.

## Acquire Complete Evidence Efficiently

Before downloading, build a compact inventory from the rendered page and, when available, selectively queried read-only structured Feishu Project tools: relevant scalar fields, diagnostically relevant image- or file-valued custom fields, every Description or narrative image, every comment page and comment-owned image, activity coverage, progress state, all visible attachments and declared sizes, and linked-item identifiers. Use the rendered page as authority for visual content and ownership; use structured results to cross-check counts and metadata. Do not expand unrelated or sensitive fields merely to make the inventory exhaustive.

In the Codex in-app Browser, prefer a `pageAssets` inventory plus an exact `bundle` selection for relevant custom-field media, Description images, and visible attachments when that capability observes them. It creates a task-specific temporary bundle and avoids contention in a shared Downloads directory. Do not bundle every image or select by broad URL shape alone. Establish ownership from at least one authoritative association: exact resource membership in a structured field, ancestry inside the rendered custom-field/Description/comment/attachment container, or an exact visible filename tied to that container. Then bundle only those asset IDs.

The returned `directoryPath` and `manifestPath` are authoritative. On current Windows Codex builds they commonly resolve under the system temporary directory in a shape such as `<system-temp>/browser-use/assets/<bundle-id>/`, with asset-ID filenames plus `manifest.json`; treat that shape as an observed convention, not a fixed contract. Record and clean the exact returned paths only.

Independent in-app Browser workers may run `pageAssets` acquisition concurrently when each owns a separate tab or control handle, an exact assigned issue, a distinct returned bundle directory, and a distinct final issue root. Keep at most one bundle operation outstanding per tab. If the runtime reuses a bundle path, returns a shared Downloads path, or leaves asset ownership ambiguous, stop parallel acquisition and serialize the affected downloads.

Page assets can contain application icons, avatars, chrome, cached resources, or hidden content whose URL resembles issue evidence. Keep a small sanitized rejected-assets decision list when filtering is non-obvious: local candidate name or stable inventory ID, real format and dimensions when inspected, observed page role, and rejection reason. Do not persist signed URLs, tokens, headers, or unrelated binary assets merely to make the rejection auditable.

For paginated structured results, record both the actual returned count and pagination metadata. Continue while a real next-page token or `has_more` signal exists. If `total`, returned count, `has_more`, or token availability disagree, preserve the discrepancy and stop according to the actual continuation signal; never claim the metadata total was retrieved merely because `_all` was requested.

Verify the ignored evidence root and available disk space once before bulk acquisition. Download small Description and comment images first, then larger attachments. Use one download event per asset, copy the completed artifact to a stable issue-specific name, and validate it immediately. Reuse a verified existing final artifact when its expected size or checksum matches instead of downloading it again.

Prefer a task-unique staging root under the resolved system temporary directory, for example `<system-temp>/codex-feishu-issue-debugger/<issue-id>/<run-id>/`, whenever the download mechanism supports choosing its destination. Resolve and record the absolute path before use; the example name is a convention, not permission to delete a broad temporary directory.

If the browser can only place completed files in a general Downloads directory, treat only the exact path returned by the current download event as a staging file. Copy it into the verified evidence root, validate the final artifact, then delete that exact browser source file by default. Keep a sanitized index mapping page evidence to local files, and report requested, completed, failed, unverified, and cleaned counts.

Keep a per-issue sanitized acquisition ledger even when all transfers succeed. Record requested, bundled or downloaded, promoted, rejected, failed, unverified, cleaned staging files, cleaned staging directories, and any retained path whose ownership was uncertain. Counts must distinguish image- or file-valued custom fields, Description/comment media, visible attachments, final evidence, page chrome, and temporary manifests.

Treat a general browser Downloads directory as shared mutable staging. Keep only one outstanding download across the coordinated investigation whenever any worker writes there. Finish the completed-download event, promotion, validation, cleanup, and post-cleanup stability recheck before starting the next browser download. Issue-specific final directories prevent final-name collisions but do not make concurrent writes to a shared Downloads directory safe.

Guard automatic staging cleanup with all of these conditions:

1. The source path was created by the current run or returned by its specific completed-download event; filename or modification time alone is insufficient.
2. Resolve source and destination to distinct absolute paths. The destination must remain inside the verified issue evidence root.
3. The final file exists and matches the source or expected byte length. When a checksum is available or inexpensive, require it to match; also complete format-specific validation such as image decoding or archive integrity.
4. Delete only the exact source file with a literal path. Never use a glob, unresolved environment variable, recursive deletion, parent Downloads directory, workspace root, or shared temporary root.
5. Before promotion or deletion, require the completed source file to remain unchanged across a short bounded stability window: observe the same path, length, and last-write state at least twice after the completed-download signal. If it is still changing, wait only within the task's bounded download timeout and treat it as incomplete if it never stabilizes.
6. After deleting, recheck after another short bounded stability window, not only immediately. Confirm that the exact source remains absent and the final artifact still passes validation. If a file reappears at the same path with different size, checksum, or write identity, treat it as a new object with unproven ownership; do not delete it under the old download's authority. Remove a task-specific staging directory only after its known files are gone, it remains empty across the recheck, and its containment is proven.

If validation or promotion fails, do not publish a final filename. Delete exact task-created failed staging files by default after recording the failure, unless a retry or resumable transfer is still active or the user explicitly asks to retain them. If ownership or path containment cannot be proven, leave the file in place and report it instead of guessing. Never delete a pre-existing file, a user-provided artifact, a verified final artifact, or an unrelated browser download.

## Download Images And Attachments

Keep the rendered page in the selected authenticated browser as the authority for what belongs to the issue. Prefer the Codex in-app Browser; use a native external browser only under the fallback conditions in `SKILL.md`. After discovering a relevant image or attachment, prefer that browser's own completed-download path so Feishu handles session access and multipart transport without exposing credentials.

- For relevant image-valued custom fields and rendered Description or comment images, prefer a browser media download that waits for the download event and obtains the completed local path. A page-asset bundle remains a useful alternative when it actually observes the dynamic asset. Confirm the file is non-empty and inspect its real format and content; a successful click or URL alone is insufficient.
- For relevant video evidence, first validate the container and decodability at bounded positions. Then create a concise timestamped event index for the business sequence that matters, such as action start, first incorrect state, refresh, and recovery. Arbitrary first/middle/last frames prove decodability, not the reported behavior; if event indexing is not completed, mark the video semantics unverified.
- For Feishu Project attachments visible on the page, first use the attachment link through the same browser download-event flow. This may return a fully assembled file even when the attachment service describes it as multipart.
- Use an attachment capability such as `get_download_url` only when browser-native downloading cannot materialize the file and a downloader can accept transient secrets without exposing them to a shell, process arguments, command history, logs, traces, files, or output. Never interpolate a temporary download URL or signature header into a terminal command. A security-policy rejection of such a command is not evidence of insufficient Windows or browser permission; do not ask the user to weaken local security settings. If no safe credential-handling downloader is available, report the blocker and ask the user to download or provide the file.
- Treat any returned URL, file signature, authorization header, token, or expiry value as transient secret material: do not print it, persist it, place it in a trace, or include it in a command or final answer.
- If the browser presents a download or account permission prompt, pause for the user unless they already gave narrow permission for that prompt. Do not change browser or account permissions silently.

Only when browser-native download is unavailable and a safe fallback exposes multipart metadata:

1. Honor the server-provided `is_multipart` flag, part indexes, and byte ranges.
2. Replace the exact part placeholder in the download URL with each listed part index; do not guess the placeholder shape or part numbering.
3. Download parts into unique files under the verified ignored or external evidence root.
4. Check that each part length equals `end_byte - start_byte + 1` and keep parts in index order.
5. Assemble into a task-unique temporary file without modifying the individual evidence parts.
6. Verify the assembled size and, when available, its checksum. For archives, run an integrity check before extraction.
7. Publish the final local filename only after assembly and validation succeed; retain or remove partial files according to the user's cleanup authority.

When the user only asks whether downloading is possible, a successful small image download plus a real first-part transfer can establish access and multipart mechanics. Label that result as a capability check, not a complete attachment download. Do not claim the full archive is available, intact, or extractable until every part has been downloaded, assembled, and validated.

When the full attachment is required for diagnosis, complete and verify the full transfer unless disk, time, permission, or service limits block it. Report the exact completed scope and blocker rather than silently substituting a partial artifact.

## Build the Timeline Before Naming a Cause

For logs and screenshots, align:

- wall-clock timestamps and timezone;
- project/job/action switches;
- configuration writes and reloads;
- pipeline construction, reuse, cleanup, and eviction;
- model loading, removal, and re-add;
- background tasks and delayed callbacks;
- the exact error or warning;
- service/process restarts.

Map important events to code locations and owners. Do not infer causality from proximity alone.

## Prefer Real Issue Data Carefully

Use issue-provided project data, configurations, logs, and history when they can exercise the reported path. Keep them out of tracked source unless the user explicitly approves a sanitized fixture.

For private validation, prefer an ignored issue-specific script or test over changing an unrelated public test. If a stable synthetic fixture can prove the same contract without private data, prefer it for long-term regression coverage.

Do not change a failing expectation merely because it fails. Inspect fixture construction, randomness, runtime dependencies, and the implementation contract first.

## Validation Ladder

Report the strongest layer actually completed:

1. **Rendered evidence:** issue fields and screenshots were read.
2. **Static code evidence:** the relevant commit-specific entrypoint and call path were inspected.
3. **Focused contract check:** a narrow test or script proved the local invariant.
4. **Real-project replay:** the downloaded issue project or historical data exercised the path.
5. **Integrated runtime:** frontend/backend/algorithm interaction ran in the required mode.
6. **Field-equivalent validation:** the relevant GUI, GPU, provider, hardware, configuration, and workload matched the reported environment.

State unavailable layers and their blockers. Syntax checks, compilation, imports, and mocked tests do not prove a real GUI/GPU issue is resolved.

## Acceptance Signals

Convert the issue result into a concrete signal before reproduction. Examples include a particular recovery warning after real eviction, one and only one pipeline initialization per lifecycle, a non-empty unified inference result matching serial behavior, or a product-facing error before a third-party exception.

Do not require unstable identifiers such as environment-derived hashes unless the issue explicitly makes them part of the contract. Require the ordering and state transition that make the signal meaningful.

## Durable Notes

Store reusable generic rules in the repository's durable knowledge location only when requested or required by repository rules. Store issue-specific evidence, decisions, validation limits, and revisit triggers in an issue trace when requested.

Exclude incidental operations, raw transcripts, raw customer logs, credentials, and unproven attribution. A durable record should preserve the smallest evidence-backed lesson that reduces future investigation cost.
