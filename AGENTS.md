# Public Repository Boundary

Everything tracked by this repository, including examples, tests, commit
messages, file paths, and Git history, must be safe for unrestricted public
distribution.

Private work repositories, employer or customer systems, conversations,
tickets, logs, screenshots, datasets, and internal documents may be used only
to identify general capabilities, engineering invariants, authorization
boundaries, and failure modes. They are not source material for public content.

When private practice informs a skill:

- use a clean-room implementation written from the abstract capability;
- use neutral or synthetic domains, actors, data, fixtures, and examples;
- do not copy, translate, lightly rename, or structurally mirror private code,
  prose, schemas, workflows, topology, filenames, identifiers, or artifacts;
- never include employer, customer, internal product, repository, service,
  issue, host, URL, account, or environment identifiers;
- retain public third-party product names only when they are necessary to use
  the public tool or API correctly;
- keep private source material and private identifier lists under ignored local
  storage, never in a commit.

Before committing, run
`python scripts/validate_skills.py --require-denylist`. Before pushing,
configure the repository hook with `git config core.hooksPath .githooks` and
maintain the private local denylist at
`.manifest/public-hygiene-denylist.txt`. The pre-push check must inspect every
commit being introduced to the remote, even when the final tree no longer
contains the prohibited material.

Tracked public content must be regular UTF-8 text. Do not add symlinks, screenshots, PDFs,
archives, Office documents, databases, dumps, or other binary assets. If a
future public skill genuinely requires a generated media asset, establish a
separate reviewed allowlist and metadata-cleaning workflow before adding it.

If public safety cannot be established without relying on private context,
exclude the material and ask the user for direction. Do not weaken or bypass a
public-hygiene check to complete a commit or push.

<!-- OPENCODE_STYLE_GUIDE_START -->
## Style Guide

Adapted from [OpenCode's Style Guide](https://github.com/anomalyco/opencode/blob/bcd713e2b71b433474d99fb1d29900c492c319a3/AGENTS.md#style-guide) at commit `bcd713e2b71b433474d99fb1d29900c492c319a3`. Existing repository-specific architecture, compatibility, formatting, and lint requirements take precedence where they are more specific; this guide does not authorize unrelated refactors or dependency changes. Language-specific sections apply only to the corresponding files.

### General Principles

- Keep simple logic in one function unless composition, reuse, or a clearly named domain concept makes extraction useful. Do not extract single-use helpers preemptively.
- Validate unknown input once at the boundary that owns it. Pass validated models or typed values inward; do not defensively revalidate values already guaranteed by a schema, constructor, or established internal contract.
- Before adding complexity for a speculative or vanishingly unlikely race or security edge case, explain the concrete failure mode, likelihood, and complexity cost to the user and get their buy-in. Do not silently expand scope for theoretical robustness.
- Avoid unnecessary exception handling. Catch only when recovery, cleanup, or boundary-level error translation is needed; keep the protected scope narrow and do not silently swallow errors.
- Reduce unnecessary temporary variables and unpacking. Inline a value used only once when that improves readability; retain names that clarify domain meaning, units, ownership, or a complex expression.
- Prefer guard clauses and early returns over deeply nested branches or unnecessary `else` blocks. Prefer assigning values once over repeated reassignment when the result remains clear.
- When a function has several validation branches or supporting details, make the main function read as the happy path and put the supporting details in small, nearby helpers. Extract real concepts, not trivial expressions; keep helpers below the main function when that improves readability.
- Keep synchronous parsing, validation, and option building synchronous. Add comments for non-obvious constraints and surprising behavior, not for obvious assignments or control flow.

### Python

These rules apply to Python files. Follow the repository's supported Python version, formatter, import sorter, type checker, and existing library conventions.

#### Imports (Python)

- Use `import module` when qualified access preserves useful context, or `from module import name` for clear direct imports. Both are normal Python; do not ban module imports as if they were JavaScript star imports.
- Avoid `from module import *` and unnecessary import aliases. Retain established ecosystem or repository aliases such as `np` and `pd`; use an alias when a real name collision requires it.
- Keep imports at module scope by default. Import a heavy optional dependency inside the narrow function or branch that needs it when lazy loading is required; do not make all imports lazy.
- Prefer the standard library and existing dependencies. Use `pathlib`, `json`, and context managers where appropriate; do not add a new dependency just to follow a style preference.

```python
import json
from pathlib import Path


def read_journal(directory: Path):
    with (directory / "journal.json").open(encoding="utf-8") as stream:
        return json.load(stream)
```

#### Types and Validation (Python)

- Keep useful type hints on public functions, domain boundaries, and non-obvious values as required by the repository's type checker. Straightforward local assignments usually do not need redundant annotations; do not remove useful annotations merely to reduce their count.
- Prefer precise types, protocols, typed dictionaries, or existing validated models over `typing.Any`. Use syntax supported by the repository's Python version.
- Validate untrusted input with the project's existing validation layer. After validation, do not repeat `isinstance`, `hasattr`, or dictionary-key checks for internal values whose invariants are already established. Type hints alone do not validate external input at runtime.

#### Variables, Iteration, and Unpacking (Python)

- Prefer readable comprehensions or generator expressions over `map` / `filter` chains for simple transformations. Use ordinary loops when side effects, branching, early exits, or clarity make them the better choice.
- Prefer direct attribute access when unpacking adds no clarity. Normal tuple unpacking, iteration unpacking, and direct named imports remain idiomatic.
- Prefer assigning values once and simple conditional expressions when clear. Do not force a complex expression just to eliminate a descriptive intermediate name.

```python
names = [item.name for item in items if item.enabled]
limit = configured_limit if configured_limit is not None else default_limit

for key, value in settings.items():
    apply_setting(key, value)
```

#### Control Flow and Helpers (Python)

- Prefer guard clauses and early returns over an unnecessary `else` after `return` or `raise`.
- Keep `try` / `except` blocks narrow and catch the specific expected exceptions. Prefer context managers or `try` / `finally` for resource cleanup; do not wrap successful-path logic in broad exception handlers without a concrete recovery policy.
- Use `async def` only when asynchronous work or an existing interface requires it. Keep synchronous helpers synchronous.

```python
def status_label(enabled: bool) -> str:
    if not enabled:
        return "disabled"
    return "enabled"


def load_thing(payload):
    config = require_config(payload)
    metadata = read_metadata(payload)
    return create_thing(config, metadata)
```

`require_config` and `read_metadata` represent real validation or parsing concepts; keep their implementations near the caller instead of extracting trivial expressions into more helpers.

#### Model and Database Fields (Python)

- Use `snake_case` for Python identifiers and new model or database fields according to the repository's conventions.
- Preserve existing external field aliases, persisted column names, public APIs, and compatibility contracts. A style change alone does not justify renaming an existing schema or adding a migration.

### JavaScript / TypeScript

These rules apply only to JavaScript and TypeScript files and their matching frameworks.

#### Types, Runtime, and Iteration (JavaScript / TypeScript)

- Avoid the `any` type when a precise type is available. Rely on type inference when possible; add explicit annotations or interfaces when exports or clarity require them.
- Prefer functional array methods (`flatMap`, `filter`, `map`) over `for` loops; use type guards on `filter` to maintain type inference downstream.
- In projects that already use Bun, use Bun APIs such as `Bun.file()` when appropriate. Do not introduce Bun into another runtime for this rule.
- When the project already uses a self-export pattern in `src/config`, follow it for new config modules, for example `export * as ConfigAgent from "./agent.js"`.

#### Destructuring (JavaScript / TypeScript)

Avoid unnecessary destructuring. Use dot notation to preserve context.

```ts
// Good
obj.a
obj.b

// Bad
const { a, b } = obj
```

#### Imports (JavaScript / TypeScript)

- Never alias imports. Do not use `import { foo as bar } from "..."` or renamed imports like `resolve as pathResolve`.
- Never use type-position `import("...")` references such as `Schema.declare<import("@opencode/plugin/effect/plugin").Plugin["effect"]>`. Only when two imports genuinely collide on a name and no other option exists, an aliased type import (`import type { Plugin as PluginDefinition } from "..."`) is permitted as a last resort — still strongly preferred not to.
- Never use star imports. Do not use `import * as Foo from "..."` or `import type * as Foo from "..."`.
- If a namespace-style value is needed, import the module's own exported namespace by name, for example `import { Project } from "@opencode/core/project"`, then reference `Project.ID`.
- Prefer dynamic imports for heavy modules that are only needed in selected code paths, especially in startup-sensitive entrypoints. Destructure dynamic import bindings near the top of the narrowest scope that needs them so they read like normal imports. Avoid inline chains such as `await import("./module").then((mod) => mod.value())` or `(await import("./module")).value()`. Keep branch-specific imports inside the branch that needs them to preserve lazy loading.

#### Variables (JavaScript / TypeScript)

Prefer `const` over `let`. Use ternaries or early returns instead of reassignment.

```ts
// Good
const foo = condition ? 1 : 2

// Bad
let foo
if (condition) foo = 1
else foo = 2
```

#### Control Flow (JavaScript / TypeScript)

Avoid `else` statements. Prefer early returns.

```ts
// Good
function foo() {
  if (condition) return 1
  return 2
}

// Bad
function foo() {
  if (condition) return 1
  else return 2
}
```

#### Effect (Only Where Already Used)

- In Effect generators, bind services to named variables before calling methods. Do not use nested service yields such as `yield* (yield* Foo.Service).bar()`.
- Do not return `Effect` from helpers unless they actually perform effectful work. Synchronous parsing, validation, and option building should stay synchronous.
- Prefer Effect schema helpers such as `Schema.UnknownFromJsonString` and `Schema.decodeUnknownOption` over manual `JSON.parse` wrapped in `Effect.try` when parsing untrusted JSON strings.

#### Schema Definitions (Only Where Drizzle Is Already Used)

In projects using Drizzle, use snake_case for new field names so column names do not need to be redefined as strings. Preserve existing public APIs, persisted names, and compatibility contracts.

```ts
// Good
const table = sqliteTable("session", {
  id: text().primaryKey(),
  project_id: text().notNull(),
  created_at: integer().notNull(),
})

// Bad
const table = sqliteTable("session", {
  id: text("id").primaryKey(),
  projectID: text("project_id").notNull(),
  createdAt: integer("created_at").notNull(),
})
```

<details>
<summary>Upstream license notice (OpenCode, MIT)</summary>

```text
MIT License

Copyright (c) 2025 opencode

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

</details>
<!-- OPENCODE_STYLE_GUIDE_END -->
