# Project instructions

## Project facts and ownership

- Purpose: TODO: describe the project's responsibility.
- Python version, source root, and tests: TODO: record actual values and paths.
- JavaScript / TypeScript runtime, source root, and tests: TODO: record actual values and paths.
- API/schema ownership and generated-code boundaries: TODO: record the owning source and generation command, if applicable.

## Verification

- Python environment, dependencies, tests, format, lint, and type checks: TODO: record configured commands.
- JavaScript / TypeScript package manager, lockfile, tests, lint, type checks, and build: TODO: record configured commands.
- Cross-language contract checks: TODO: record existing checks, or state that none are configured.

Resolve these entries from configuration before running commands; do not treat
the TODO entries as commands or assume a tool has been configured.

## Python style

These rules apply to Python files; they do not change JavaScript / TypeScript imports.

- Follow the supported Python version, formatter, import sorter, and type checker.
- Use module or direct named imports where clear. Avoid wildcard imports and unnecessary aliases; retain established aliases such as `np` and `pd` and resolve genuine name collisions.
- Keep imports at module scope unless a heavy optional dependency needs lazy loading in its narrow use scope. Prefer the standard library and existing dependencies.
- Keep useful type hints at public interfaces and domain boundaries. Prefer precise types over `typing.Any`; annotations alone do not validate external input.
- Validate external input at its owning boundary, then pass validated values inward without repeating checks for established invariants.
- Prefer readable comprehensions or generators for simple transformations; use ordinary loops for branching, side effects, or early exits. Tuple and iteration unpacking remain idiomatic.
- Use guard clauses, narrow exception handling, and context managers or `try` / `finally` for cleanup. Keep synchronous helpers synchronous.
- Use `snake_case` for new Python fields while preserving existing external aliases, persisted names, and compatibility contracts.

## JavaScript / TypeScript style

These rules apply to JavaScript / TypeScript files; they do not ban Python module imports.

- Follow the configured runtime, module conventions, formatter, lint rules, and TypeScript settings.
- Prefer inferred types for obvious values, explicit types for exports or clarity, and precise types over `any`.
- Prefer `const`, guard clauses, early returns, and readable array transformations. Use filter type guards when narrowing is needed.
- Avoid unnecessary destructuring when qualified access preserves useful context.
- Prefer direct named imports; avoid renamed imports, star namespace imports, and type-position `import("...")` references. An aliased type import is a last resort for an unavoidable name collision.
- Lazily import heavy modules only in paths that need them, with local bindings instead of inline import chains.
- Apply Bun, Effect, Drizzle, and similar framework-specific conventions only where the project already uses those tools.

## Shared contracts

- Keep language rules scoped to their own files. Preserve the documented owner of API schemas, serialized fields, and generated clients.
- Use existing generation commands for generated artifacts. A style preference alone does not authorize a cross-language contract change, migration, or new dependency.

## Source attribution

The language guidance is adapted from the repository's
[Python-first Style Guide](https://github.com/ruicore/codex-skills/blob/2725862f11f3f6b41ecafc75715ae49b66254da8/AGENTS.md#style-guide)
and its cited OpenCode source. Retain the following upstream notice when copying
this template.

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
