# Side Effect Policy

This document defines the repository-wide side-effect model for `codex-skills`.
It is a safety and classification aid, not a request to rewrite existing skills.

Use the highest side-effect level a skill can reach in normal operation. A skill
may have a safe default mode and a higher-risk optional mode. When that happens,
document both the default level and the higher level that requires stronger
guardrails.

This policy follows the repository contract: preserve current workflow behavior,
keep practice-derived safety rules when they are useful, and add classification
before restructuring.

## Level Summary

| Level | Short meaning | Default confirmation posture |
|---|---|---|
| `none` | No tool, file, network, account, or repository mutation. | Not required. |
| `read-only` | Reads local files, local state, or already available context only. | Not required unless a command may be expensive or sensitive. |
| `local-files` | Creates or edits local files outside a version-control publication step. | Required when the target path is unclear, durable, private, or user-owned. |
| `git-working-tree` | Changes files in a repository working tree, stages, commits, or pushes. | Required for commits, pushes, or broad edits; edits require user intent. |
| `external-api-read` | Reads remote account, service, web, or API state without mutation. | Usually not required after the user asks for that service or live data. |
| `external-api-write` | Mutates a remote service without immediate public publication. | Required unless the user explicitly requested the exact mutation. |
| `publish` | Creates, schedules, queues, exports, or shares externally visible material. | Required, with preview or preflight. |
| `destructive` | Deletes, overwrites, purges, force-updates, or performs hard-to-recover mutation. | Required immediately before action, with target repetition. |

## General Rules

- Classify by the strongest action the skill authorizes, not by the first step.
- Treat optional commands as part of the classification when they are documented
  as normal skill behavior.
- Prefer read-only discovery before mutation when a skill touches a repository,
  account, board, library, database, or publishing surface.
- Keep credentials in environment variables, local credential stores, connector
  auth, or the target tool's approved setup mechanism. Never commit, print, or
  paste credentials into skill files, examples, logs, generated docs, or final
  answers.
- A preview can be a dry-run command, generated input JSON, diff, screenshot,
  preflight summary, schema check, local rendered preview, or concise target
  summary. Use the preview form that best matches the workflow.
- For publish-affecting and destructive operations, confirmation must refer to
  the specific target and action. A vague earlier approval is not enough.
- If rollback is uncertain, say so before acting and choose the lower side-effect
  path when possible.

## `none`

Meaning:

The skill only changes the conversation. It produces analysis, critique, a plan,
or a draft answer without reading private local files, running tools, contacting
services, or writing artifacts.

Examples from this repository:

- `grill-me` can operate at this level when critiquing a user-provided idea
  without inspecting local code.
- `write-a-prd` can operate at this level when it returns a PRD draft in chat and
  does not create a file.

User confirmation:

- Not required.
- Ask only when the skill would otherwise need local evidence, external research,
  or a durable artifact.

Dry-run or preview:

- Not applicable. The response itself is the preview.

Credential handling:

- No credentials should be requested or used.

Rollback or cleanup:

- Not applicable.

Codex must never do automatically:

- Do not silently escalate from pure reasoning into file reads, file writes,
  web/API calls, commits, or publication.
- Do not claim repository evidence was inspected when no read occurred.

## `read-only`

Meaning:

The skill reads local files, repository state, command output, screenshots, or
already configured local services without changing them.

Examples from this repository:

- `database-access-audit` defaults to a read-only audit and explicitly avoids
  business-code edits unless the user asks for fixes.
- `architecture-review`, `agent-legibility-review`, `python-backend-review`, and
  `python-ecosystem-review` normally inspect repository evidence and return
  findings.
- `paper-mcp` begins with board inspection commands such as `get_basic_info` and
  `get_selection`.

User confirmation:

- Not required for normal local repository reads after the user asks for review,
  audit, diagnosis, or inspection.
- Required before running commands that may be expensive, touch live systems,
  connect to production services, or expose sensitive data.

Dry-run or preview:

- Not required.
- For risky validation, preview the command, target environment, and expected
  read-only behavior before running it.

Credential handling:

- Do not request credentials for ordinary local inspection.
- If a read-only check needs authenticated access, prefer existing connector or
  tool auth and avoid printing tokens or raw private payloads.

Rollback or cleanup:

- Clean up only temporary files created by inspection tools, and only if they are
  in a scratch location or clearly generated during the task.

Codex must never do automatically:

- Do not modify business code, generated artifacts, repository docs, database
  state, account state, or board state under a read-only request.
- Do not connect to production databases or run migrations as validation.

## `local-files`

Meaning:

The skill creates, edits, downloads, renders, or imports files on the local
machine without committing or publishing them. The files may be scratch outputs,
generated artifacts, ignored local context, receipts, previews, or user-requested
documents.

Examples from this repository:

- `excalidraw-diagrams` creates `elements.json`, `.excalidraw` files, preview
  images, and sometimes a Markdown index.
- `genmedia` saves downloaded media and JSON receipts under `outputs/`.
- `decision-trace-writer` can create local agent-facing decision traces when the
  repository has a convention or the user asks for durable context.

User confirmation:

- Required when the target path is unclear, the file may contain private
  context, the write is durable agent memory, or the user did not clearly ask
  for an artifact.
- Not required when the user asks for a concrete artifact and the skill writes
  only expected generated files in a conventional or scratch output location.

Dry-run or preview:

- Required when overwriting an existing file or writing into a user-owned
  non-scratch location.
- Recommended for generated visual artifacts through local previews, screenshots,
  or rendered output checks.

Credential handling:

- Do not store credentials in generated files.
- If a local setup file must reference credentials, use environment-variable
  names or placeholders, not real values.

Rollback or cleanup:

- Preserve generated deliverables unless the user asks to remove them.
- Remove temporary scratch files when they are not part of the deliverable.
- If an overwrite occurred, restore from the known prior content only when that
  content was captured safely and the user asks for rollback.

Codex must never do automatically:

- Do not delete generated files unless the user asks or they are disposable files
  in a temporary scratch location.
- Do not write private conversation, raw logs, secrets, account IDs, or
  credential material into durable local artifacts.
- Do not invent a new complex repository convention just to place one local file.

## `git-working-tree`

Meaning:

The skill modifies a version-controlled repository working tree or performs Git
operations such as staging, committing, branch creation, pushing, or opening a
pull request.

Examples from this repository:

- `weekly-radar-ingestion` writes reviewed reports, metadata, themes, indexes,
  validates them, then commits ingestion-related files when appropriate.
- `decision-trace-writer` may write traces into a repository convention, but it
  must not stage or commit ignored/private agent-facing traces unless the user
  explicitly asks.
- Any skill that edits `SKILL.md`, references, scripts, examples, README, or
  docs in this repository reaches this level.

User confirmation:

- File edits require user intent to edit, implement, create, or update.
- Staging, committing, pushing, force-pushing, creating PRs/MRs, and changing
  branches require explicit user instruction or the repository workflow already
  established for the task.
- When the user asks only to evaluate, inspect, review, or assess, stay
  read-only.

Dry-run or preview:

- Required before broad rewrites, mass formatting, generated updates across many
  files, migrations, or risky mechanical changes.
- Diffs are the normal preview before committing. Validation output is the normal
  confidence check after editing.

Credential handling:

- Do not commit secrets, private URLs, private customer/project data, raw logs,
  or sensitive identifiers.
- Check public sanitization expectations before adding examples, references, or
  generated artifacts.

Rollback or cleanup:

- Keep user changes intact. Never revert unrelated dirty work.
- If a change needs rollback, revert only the files and lines changed for the
  current task, and explain what was reverted.
- Commit only scoped files. Push only when requested or clearly part of the task.

Codex must never do automatically:

- Do not run `git reset --hard`, destructive checkout, force-push, or branch
  deletion without explicit instruction.
- Do not stage unrelated changes.
- Do not commit ignored/private agent memory unless the user explicitly asks.
- Do not rename, split, merge, or restructure skills for polish alone.

## `external-api-read`

Meaning:

The skill reads remote state from an external API, connected account, web
service, or live source without changing that remote state.

Examples from this repository:

- `buffer-publisher` reads Buffer account, organization, channel, post, and
  daily-limit state before any mutation.
- `readwise-cli-control` can search Reader documents, list documents, get
  details, export documents, and search highlights.
- `genmedia` can search models, inspect schemas, check pricing, poll job status,
  and search documentation.
- `ai-career-signal-researcher` uses live external browsing or current market
  data when currency matters.

User confirmation:

- Not required when the user asks to inspect that account/service or asks for
  current/live data.
- Required when access would use a personal account the user did not name, when
  the source may contain sensitive personal data, or when the query could be
  expensive.

Dry-run or preview:

- Not usually required.
- Use bounded queries, pagination, and concise summaries instead of dumping raw
  private results.

Credential handling:

- Use existing connector auth, environment variables, local keychain, or tool
  setup. Never print, paste, or commit tokens.
- If authentication fails, ask the user to refresh credentials through the
  appropriate local or connector flow.

Rollback or cleanup:

- Not applicable to remote state because no mutation should occur.
- Remove temporary local exports if they contain private account data and are not
  needed as deliverables.

Codex must never do automatically:

- Do not mutate remote state while performing an external read.
- Do not dump raw account data, private messages, full exports, or large payloads
  into public docs or final answers.
- Do not scrape around an auth failure or switch to another personal account
  without user direction.

## `external-api-write`

Meaning:

The skill changes remote state through an API or connected tool, but the result
is not immediately public-facing publication. This includes creating private
drafts, ideas, library items, tags, board nodes, uploads, or account-scoped
records.

Examples from this repository:

- `buffer-publisher` can create Buffer Ideas and draft posts. Its workflow
  defaults unscheduled content to an Idea, uses `preview-post` before post
  creation, and requires explicit confirmation for higher-risk post mutations.
- `readwise-cli-control` can create Reader documents, move documents, add tags,
  and create highlights.
- `paper-mcp` can write HTML into an open Paper board and place images.
- `genmedia upload` uploads local files or remote URLs to the fal.ai CDN.

User confirmation:

- Required unless the user explicitly requested the exact remote mutation.
- Required before changing readonly mode to allow writes.
- Required before editing remote account/library/board records when the request
  started as analysis, search, or review.

Dry-run or preview:

- Required when the API or helper supports dry-run, preview, generated input
  JSON, screenshot verification, or preflight summaries.
- For Buffer-like workflows, preview the organization, channel, service, text,
  assets, mode, and time before post-affecting writes.

Credential handling:

- Use the minimum credential surface required by the tool.
- Never expose API keys in command output, generated docs, scripts, examples, or
  final responses.
- Prefer environment variables or local secure stores such as keychain-backed
  setup when a skill already supports them.

Rollback or cleanup:

- Know whether the remote object can be edited, archived, deleted, or restored
  before creating it.
- Record returned IDs only in the active task context unless they are safe and
  necessary for a deliverable.
- If a mistaken write occurs, stop and report the target, operation, and known
  cleanup option before making further changes.

Codex must never do automatically:

- Do not convert read-only account inspection into writes.
- Do not write to locked, disconnected, ambiguous, or wrong target accounts,
  channels, boards, or libraries.
- Do not upload local private files unless the user identified them as intended
  inputs.

## `publish`

Meaning:

The skill creates, schedules, queues, exports, shares, or otherwise makes
material externally visible. This includes immediate publishing, scheduled
publishing, queueing content for future publication, generating public/shareable
links, opening PRs/MRs, pushing public branches, or publishing generated media or
documents to an external service.

Examples from this repository:

- `buffer-publisher` can add posts to a Buffer queue, schedule posts with
  `customScheduled`, or publish immediately with `shareNow`. Its existing safety
  practice requires preview or preflight and explicit confirmation for
  publish-affecting actions.
- `excalidraw-diagrams` can export a browser-openable Excalidraw share URL.
- `genmedia` can run hosted model jobs and upload media to external services; if
  the output or upload is shared publicly, classify the action as `publish`.
- Repository workflows that push branches or create public PRs/MRs also reach
  this level.

User confirmation:

- Required immediately before publication, scheduling, queueing, sharing, push,
  or PR/MR creation unless the user's latest instruction explicitly asked for
  that exact action.
- Confirmation must name the destination and mode, such as channel, service,
  due time, branch, remote, PR target, or share destination.

Dry-run or preview:

- Required. Use the strongest available preview: rendered content, post input
  JSON, local screenshot, diff, preflight summary, share target, schedule time,
  or dry-run mutation input.
- For scheduled content, convert local time to a concrete UTC ISO-8601 time when
  the API requires UTC and show the converted value before sending.

Credential handling:

- Use existing authenticated tools only for the intended destination.
- Do not expose tokens, account IDs beyond what is necessary, private URLs, or
  unpublished content in public docs.

Rollback or cleanup:

- Identify whether the action can be edited, unscheduled, deleted, unpublished,
  closed, or reverted before acting.
- For scheduled or queued posts, keep enough safe target information to support
  cancellation or edits.
- For Git publication, know the branch and remote before pushing and avoid
  force-push unless the user explicitly requests it.

Codex must never do automatically:

- Do not use immediate publish modes such as Buffer `shareNow` unless the user
  explicitly asks to publish immediately.
- Do not schedule, queue, or push to an ambiguous target.
- Do not publish private, unsanitized, credential-bearing, or user-unreviewed
  content.
- Do not treat a draft request as permission to publish.

## `destructive`

Meaning:

The skill deletes, overwrites, purges, removes, force-updates, disables, or
otherwise performs hard-to-recover mutation. Destructive actions may be local,
Git-based, database-related, or external-service operations.

Examples from this repository:

- `buffer-publisher` supports `delete-post`, but requires repeating the target
  post ID, receiving explicit user confirmation, and using the CLI's `--yes`
  confirmation flag.
- `paper-mcp` warns that deleting Paper nodes changes board data and requires
  immediate user confirmation before deletion.
- `genmedia` references commands that can remove installed skills or overwrite
  initialized files; these should be treated as destructive when used.
- `database-access-audit` explicitly forbids migrations, destructive commands,
  data repair scripts, load tests, and backfills unless the user authorizes that
  action.

User confirmation:

- Always required immediately before the action.
- Repeat the exact target, scope, and operation. For example: post ID, node
  selection, file path, branch, remote, table/database, account, or installed
  skill name.
- Do not rely on broad approval from earlier in the conversation.

Dry-run or preview:

- Required when available.
- If no dry-run exists, provide the safest available preview: target listing,
  diff, backup path, command without execution, affected count estimate, or
  screenshot of the target selection.

Credential handling:

- Do not use credentials with broader permissions than necessary.
- Do not store destructive-operation credentials or resulting raw logs in the
  repository.

Rollback or cleanup:

- Establish rollback before action when feasible: backup, revert plan, remote
  undo path, branch recovery, exported copy, or explicit statement that rollback
  is not available.
- After action, verify the target state and report what changed.
- If rollback is impossible or uncertain, say that before seeking confirmation.

Codex must never do automatically:

- Do not delete, purge, force-push, hard reset, overwrite, remove installed
  skills, run migrations, run backfills, repair data, or delete external records
  without immediate explicit confirmation.
- Do not compose destructive filesystem commands from unverified computed paths.
- Do not broaden a destructive target beyond the user's named scope.
- Do not continue with additional destructive actions after an unexpected result.

## How To Classify A Skill

Use this checklist when adding metadata, reviewing a skill, or deciding what
safety language a skill needs:

1. What is the strongest action the skill can perform in normal use?
2. Does the default workflow stay lower risk than optional commands? If yes,
   document both default and maximum levels.
3. Does the skill only answer in chat, read local evidence, write local files,
   modify a Git working tree, call external APIs, publish, or delete/overwrite?
4. What exact user phrase should unlock mutation, publication, or destructive
   action?
5. Is a dry-run, preview, diff, screenshot, generated input JSON, or preflight
   summary available?
6. Where do credentials come from, and how does the skill prevent printing or
   committing them?
7. What private data could appear in outputs, examples, logs, receipts, or final
   answers?
8. What is the rollback or cleanup path if the action is wrong?
9. What must Codex refuse to do automatically, even when the tool technically
   supports it?
10. Does the classification preserve the existing workflow semantics, or is it
    accidentally changing behavior?

When uncertain, choose the higher side-effect level and add a portability or
safety note rather than weakening an existing guardrail.
