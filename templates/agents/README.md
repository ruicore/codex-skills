# Global defaults and project instruction templates

Use these files when starting a new project, rather than copying an old
repository's paths, commands, and exceptions. They are instruction templates,
not installable skills, and `scripts/install_skill.py` does not install them.

## Choose the layer

| File | Purpose | Destination |
| --- | --- | --- |
| [global-style.md](global-style.md) | Short language-neutral personal style defaults | A section in the active Codex home's `AGENTS.md` |
| [python.md](python.md) | Python conventions and project facts | New project's root `AGENTS.md` |
| [javascript-typescript.md](javascript-typescript.md) | JavaScript / TypeScript conventions and project facts | New project's root `AGENTS.md` |
| [mixed.md](mixed.md) | Python first, then separately scoped JavaScript / TypeScript conventions | New project's root `AGENTS.md` |

The global defaults contain the common style rules. Project templates add
language-specific guidance and verified project facts without copying that
global block into every repository. A machine without those global defaults
will not inherit them merely because it has a project template.

## Set up global style once

1. Locate the active Codex home: `CODEX_HOME` when set, otherwise `~/.codex`.
2. Read its existing `AGENTS.md` and `AGENTS.override.md`, if present.
   A nonempty global override takes precedence over the normal global file;
   reconcile an intentional override instead of assuming both files load.
3. Merge the complete block from [global-style.md](global-style.md) into the
   existing global `AGENTS.md`. Preserve unrelated instructions. If the
   `PERSONAL_STYLE_DEFAULTS` markers already exist, replace that block once
   rather than appending a duplicate. Review any local edits before replacing it.
4. Start a new Codex session and ask it to identify its instruction sources.
   Verify that the intended global file and the project's instructions appear.

This is a deliberate configuration edit, not a symlink to this checkout or an
automatic update. Pulling this repository does not change global instructions.
The public file contains only the style block, not a copy of a user's full
global configuration.

## Start a new project

1. Choose the template matching the code the project will own. Use the mixed
   template when both Python and JavaScript / TypeScript are part of the project.
2. Save a copy as `AGENTS.md` at the new repository root. Check that the
   destination does not already exist; merge into an existing file instead of
   overwriting it. Keep the attribution and embedded MIT notice with the copy.
3. Resolve every TODO from real project configuration: supported runtimes,
   source and generated-code ownership, package managers, and verification
   commands. Omit irrelevant checks or state what is not configured; do not
   invent commands. Ask for unresolved project choices when necessary.
4. Remove language or framework rules that do not apply. Keep any necessary
   project-specific overrides explicit, with normal formatting enforced by
   the project's existing tools.
5. Start a new session in the project and verify which instruction files load.
   No other repository needs to be rewritten as part of this setup.

For an existing project that keeps guidance under `.manifest/` or another
off-path directory, preserve its established entry point. A nested file is not
automatically discovered from the repository root merely because it is named
`AGENTS.md`; use an explicit root-file reference when that guidance must be read
from the root. Avoid a second conflicting copy of the same rules.

## Maintenance

Edit the global style source here and deliberately merge it into the active
global file when its defaults change. Update language templates when those
conventions change. Existing project copies are snapshots: changes here do not
silently propagate to them, and project-specific exceptions remain local.

These are opinionated defaults. Global style does not override a repository's
more specific instructions, formatter, architecture, or compatibility contracts.
This template addition does not replace the library's existing `AGENTS.md`.

See the official [AGENTS.md documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
for instruction discovery, global overrides, and project layering.
