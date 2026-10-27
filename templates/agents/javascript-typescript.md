# Project instructions

## Project facts

- Purpose: TODO: describe the project's responsibility.
- Supported runtime and version: TODO: confirm the configured runtime.
- Source, tests, and generated-code boundaries: TODO: record actual paths.

## Verification

- Package manager and lockfile: TODO: record the existing tool and lockfile.
- Test command: TODO: record the smallest relevant command.
- Format, lint, type-check, and build commands: TODO: record configured scripts.

Resolve these entries from configuration before running commands; do not treat
the TODO entries as commands or assume a tool has been configured.

## JavaScript / TypeScript style

- Follow the configured runtime, formatter, lint rules, module conventions, and TypeScript settings. Preserve public APIs and persisted or external field names.
- Use inference for obvious values and explicit types for exports or clarity. Prefer precise types over `any`; validate unknown external input at its owning boundary.
- Prefer `const`, guard clauses, and early returns over unnecessary reassignment or `else` blocks.
- Prefer readable `map`, `filter`, and `flatMap` transformations; use type guards when filtering needs to preserve useful TypeScript narrowing.
- Avoid unnecessary destructuring when qualified access preserves useful context.
- Prefer direct named imports. Avoid renamed imports, `import * as`, and type-position `import("...")` references. Use an aliased type import only for a genuine name collision that cannot be resolved more clearly.
- When a namespace-like value is needed, use the module's own exported namespace if available, following existing module conventions.
- Lazily import a heavy module only in the code path that needs it. Bind the imported values near the beginning of that narrow scope instead of using inline import chains.
- Use Bun or framework-specific helpers only when the project already uses that runtime or framework. Follow existing export and schema patterns without introducing new dependencies for style alone.

## Source attribution

The language guidance is adapted from the repository's
[Python-first Style Guide](https://github.com/ruicore/codex-skills/blob/2725862f11f3f6b41ecafc75715ae49b66254da8/AGENTS.md#javascript--typescript)
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
