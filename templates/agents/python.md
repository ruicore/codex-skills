# Project instructions

## Project facts

- Purpose: TODO: describe the project's responsibility.
- Supported Python version: TODO: confirm from project configuration.
- Source, tests, and generated-code boundaries: TODO: record actual paths.

## Verification

- Environment and dependency tool: TODO: record the existing tool.
- Test command: TODO: record the smallest relevant command.
- Format, lint, and type-check commands: TODO: record configured commands.

Resolve these entries from configuration before running commands; do not treat
the TODO entries as commands or assume a tool has been configured.

## Python style

- Follow the configured Python version, formatter, import sorter, and type checker. Preserve public API names, external aliases, and persisted schema names.
- Use `import module` for useful qualification or `from module import name` for clear direct imports. Avoid `from module import *` and unnecessary aliases; retain established aliases such as `np` and `pd` or resolve genuine name collisions.
- Keep imports at module scope unless an expensive optional dependency needs lazy loading in its narrow use scope. Prefer existing dependencies and the standard library.
- Keep useful type hints on public functions, domain boundaries, and non-obvious values. Avoid redundant annotations on obvious local assignments and use precise types instead of `typing.Any` where practical.
- Validate untrusted input using the project's existing validation layer. After validation, avoid repeating `isinstance`, `hasattr`, or key checks for already-established internal invariants.
- Prefer readable comprehensions and generator expressions for simple transformations; use ordinary loops for branching, side effects, or early exits. Tuple and iteration unpacking remain idiomatic.
- Use guard clauses and simple conditional expressions where clear. Keep descriptive intermediate names when they improve understanding.
- Keep `try` / `except` scopes narrow and catch expected exception types. Use context managers or `try` / `finally` for cleanup; keep synchronous helpers synchronous.
- Use `snake_case` for new Python identifiers and model fields according to project conventions. A style preference alone does not justify a compatibility change or database migration.

## Source attribution

The language guidance is adapted from the repository's
[Python-first Style Guide](https://github.com/ruicore/codex-skills/blob/2725862f11f3f6b41ecafc75715ae49b66254da8/AGENTS.md#python)
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
