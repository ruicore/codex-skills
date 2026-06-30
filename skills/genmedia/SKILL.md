---
name: genmedia
description: >
 Use the genmedia CLI to search, inspect, run, and manage 1200+ fal.ai model
 endpoints. Trigger when the user mentions "genmedia", "fal CLI", or asks to
 "search models", "run a model", "fetch schema", "check pricing", "upload to
 fal", "queue async job", "track request", or any direct interaction with the
 fal.ai endpoint catalog. This is the foundational skill. Every other
 fal.ai-related skill in this repo executes its work through genmedia
 commands. Use `--json` whenever the output will be parsed by an agent.
---

# genmedia CLI: fal.ai endpoint runner

`genmedia` is the agent-first CLI for fal.ai. It works in a terminal for humans (pretty output) and equally well for agents (structured JSON when piped or with `--json`). All other skills in this repo call `genmedia` for execution, they do not wrap the fal.ai HTTP API directly.

For the full command surface (every flag, every option, every example), see [references/full-reference.md](references/full-reference.md).

## Local setup notes

- If a shell cannot find `genmedia`, try running commands with `PATH="$HOME/.local/bin:$HOME/.genmedia/bin:$PATH"`.
- Keep fal credentials in `genmedia setup`, `FAL_KEY`, or a local `.env`; never write API keys into skill files, scripts, logs, or generated docs.
- Save generated media and JSON receipts into a local `outputs/` folder unless the user names another destination.
- If the user has a local editing mini app, set its path as `[YOUR_MINI_APP_DIR]` and its URL as `[YOUR_MINI_APP_URL]`. When the user asks for images, videos, edits, variants, or anything meant to be inspected visually, run genmedia locally and import the downloaded outputs into that app if available.

## Optional mini app handoff

When the user says to use genmedia for an image/video/media prompt, treat the mini app as the working surface:

1. Interpret the user's prompt and pick an appropriate fal endpoint. Search models if the endpoint is not obvious, verify the endpoint, and inspect the schema before running.
2. Run `genmedia` locally with `--json` and `--download`, saving media and a JSON receipt under `outputs/`.
3. Import the downloaded files into the mini app grid with `scripts/import-to-mini-app.mjs`.
4. Make sure the app is running at `[YOUR_MINI_APP_URL]`; restart it if needed.
5. Reply with the local app link and a short note about what was added. The goal is that the user can immediately click, preview, edit, use as a reference, generate more variants, or save the outputs as Elements.

Use this helper after a genmedia run:

```bash
node "$HOME/.codex/skills/genmedia/scripts/import-to-mini-app.mjs" \
  --app-dir "[YOUR_MINI_APP_DIR]" \
  --prompt "the user prompt" \
  --endpoint-id "fal-ai/example" \
  --model-name "Model Name" \
  --category "text-to-image" \
  --receipt "./outputs/run.json" \
  ./outputs/image_0.png
```

If the user asks to edit an image already in the grid, use that asset as an input/reference, run the right genmedia edit model, then import the edited result back into the same grid. If the user asks for more options, generate more variants and import them as new grid items. If the user asks to save outputs as Elements, use the mini app's Elements UI or POST to `/api/elements` with the imported asset IDs returned by the helper.

## Critical rules

1. **Always use `--json` when an agent will read the output.** Pretty mode is for humans only.
2. **Never invent endpoint IDs.** Use `genmedia models "<query>"` to discover, `genmedia models --endpoint_id <id>` to verify.
3. **Inspect schema before running.** `genmedia schema <endpoint_id> --json` shows the exact field names. Guessed flags fail with 422.
4. **Save files with `--download`, not curl.** The CLI handles authentication, naming, and file format detection.
5. **Use `--async` for long-running generation.** Image work usually completes inline; video/audio/3D usually need queue + status polling.

## Command index

| Command | Purpose |
|---------|---------|
| `genmedia setup` | Configure API key, output mode, auto-update |
| `genmedia models <query>` | Search the catalog (or `--category`, or `--endpoint_id`) |
| `genmedia schema <endpoint_id>` | Inspect inputs/outputs (compact or `--format openapi`) |
| `genmedia run <endpoint_id> --<param> <value>` | Execute a model |
| `genmedia status <endpoint_id> <request_id>` | Poll an async job (with `--result`, `--logs`, `--cancel`, `--download`) |
| `genmedia upload <path-or-url>` | Upload a local file or remote URL to the fal.ai CDN |
| `genmedia pricing <endpoint_id>` | Check cost per call |
| `genmedia docs <query>` | Search fal.ai documentation |
| `genmedia init` | Install the default skill bundle into `.agents/skills/` or `.claude/skills/` |
| `genmedia skills <list|install|update|remove>` | Manage installed agent skills |
| `genmedia version` / `genmedia update` | Check or apply CLI updates |

## Quick patterns

### Run a model and download the result

```bash
genmedia run fal-ai/flux/dev \
 --prompt "a cat on the moon" \
 --download "./out/{request_id}_{index}.{ext}" \
 --json
```

### Async + poll

```bash
SUBMIT=$(genmedia run fal-ai/veo3.1 --prompt "a dog running" --async --json)
REQ=$(echo "$SUBMIT" | jq -r '.request_id')
genmedia status fal-ai/veo3.1 "$REQ" \
 --download "./out/{request_id}_{index}.{ext}" \
 --json
```

### Upload then run

```bash
URL=$(genmedia upload ./photo.jpg --json | jq -r '.url')
genmedia run fal-ai/nano-banana-pro/edit \
 --image_urls "$URL" \
 --prompt "make the sky stormy" \
 --download "./out/{request_id}_{index}.{ext}" \
 --json
```

### Discover when the user names a fuzzy task

```bash
genmedia models "background removal product image" --json
genmedia models --category text-to-video --limit 5 --json
genmedia docs "webhook callbacks" --json
```

## Setup (first-time only)

If `genmedia` is not installed:

```bash
curl https://genmedia.sh/install -fsS | bash # Linux / macOS
irm https://genmedia.sh/install.ps1 | iex # Windows PowerShell
genmedia setup --non-interactive --api-key "$FAL_KEY"
```

For full setup details (output modes, auto-update, `.env` loading) see [full-reference.md](references/full-reference.md).

## Portability Notes

- Specific to the author's current workflow: optional mini app handoff uses local `[YOUR_MINI_APP_DIR]` and `[YOUR_MINI_APP_URL]` placeholders plus the bundled import helper.
- Reusable: schema-first endpoint execution, JSON output for agents, async polling, authenticated downloads, and credential non-disclosure rules.
- Adapt before reuse: configure genmedia installation, fal credentials, output directories, optional app import paths, and any local media-inspection workflow.
