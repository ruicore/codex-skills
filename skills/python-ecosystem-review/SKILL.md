---
name: python-ecosystem-review
description: Review Python repositories by automatically discovering important ecosystem libraries and evaluating concrete library usage against current best practices. Use when Codex needs a review of framework, validation, ORM, migration, dependency injection, async, background job, HTTP client, testing, LLM/agent, observability, or runtime-library integration points. Review-only by default; do not use for broad architecture, generic Python style, full agent-legibility, security, performance, or framework-only reviews.
---

# Python Ecosystem Review

Review one thing: how a Python repository actually uses important ecosystem libraries. Focus on libraries that shape architecture, data flow, validation, persistence, API boundaries, concurrency, background execution, testing, or runtime behavior.

Do not modify code unless the user explicitly asks for fixes. If fixes are allowed, complete the review first, then make only the requested or clearly justified library-usage changes.

## Boundaries

- Do not perform broad architecture review. Discuss architecture only when concrete library usage creates unclear boundaries, lifecycle risk, or cross-library coupling.
- Do not perform broad agent-legibility review. Discuss Codex legibility only when library usage makes integration behavior hard to find, verify, or safely modify.
- Do not perform general Python backend review. Discuss Python fundamentals only when they directly affect a reviewed library's usage.
- Do not review every dependency. Ignore tooling, packaging-only dependencies, formatters, simple utilities, and transitive libraries unless the user asks or the code shows architectural use.
- Prefer automatic discovery. User-specified libraries are priority hints, not required inputs.

## Inputs

Support these optional inputs:

- `priority_libraries`: library names the user wants emphasized.
- `allow_web_research`: whether to check official sources when version-specific claims may be stale; default to true when network access is available or the user asks for current best practices.
- `review_only`: default `true`.

## Discovery Workflow

1. Discover dependency evidence.
   - Inspect `pyproject.toml`, `requirements.txt`, `requirements/*.txt`, `poetry.lock`, `uv.lock`, `Pipfile`, `setup.py`, `setup.cfg`, tox/nox config, Docker files, CI files, and README/deployment notes when relevant.
   - Record declared versions, version ranges, lockfile versions, extras, dependency groups, and runtime/dev separation.
   - Treat mismatches between declarations and lock/runtime files as review evidence.

2. Build the library candidate list.
   - Search imports and integration points, not only dependency files.
   - Use `rg` for imports, decorators, config keys, entrypoints, fixtures, app factories, migration env files, task registration, dependency providers, clients, middleware, plugins, and test helpers.
   - Include libraries used through framework strings, settings, plugin config, CLI entrypoints, or generated migration/task files even when imports are indirect.

3. Classify review priority.
   - `Must review`: libraries that define the app framework, request/response boundary, validation/serialization, ORM/persistence, migrations, task queues, workflow engines, dependency injection, or major runtime lifecycle.
   - `Review if used heavily`: libraries that affect important execution paths when used broadly or at boundaries, such as HTTP clients, Redis clients, cache layers, structured logging, tracing, test frameworks, fixture systems, serialization helpers, or client SDKs.
   - `Ignore unless user asks`: formatters, linters, build backends, packaging-only tools, type checkers used only as tools, tiny utilities, or libraries with trivial localized use.

Use examples as hints, not a closed list:

| Priority | Examples |
|---|---|
| Must review | FastAPI, Django, Flask, Litestar, SQLAlchemy, SQLModel, Tortoise ORM, Pydantic, Alembic, Celery, Dramatiq, RQ, LangChain, LangGraph |
| Review if used heavily | httpx, aiohttp, requests, redis, pytest, structlog, loguru, dependency-injector, opentelemetry, tenacity |
| Ignore unless user asks | black, ruff, isort, build, wheel, twine, packaging-only plugins, small local utility dependencies |

4. Inspect actual usage for each reviewed library.
   - Check imports, public interfaces, adapter layers, app setup, lifecycle hooks, middleware, dependency providers, model/schema definitions, repositories, migrations, clients, tasks, workers, tests, configuration, and error handling.
   - Identify where library concepts cross project boundaries, such as framework objects entering business logic, ORM sessions crossing task boundaries, schemas doubling as domain models, or clients instantiated without lifecycle control.
   - Compare usage against the project's own established patterns before recommending new patterns.

5. Verify freshness before strong claims.
   - If the detected version is newer than reliable model knowledge, the API is version-sensitive, or the code uses recently changed/deprecated patterns, check official documentation, changelogs, migration guides, or release notes before making strong claims.
   - Prefer official documentation, official changelogs, official migration guides, and official release notes.
   - Do not rely on generic blog posts for version-specific best-practice claims unless official sources are unavailable.
   - Cite official sources when web research is used.
   - If current verification is unavailable, state the uncertainty and downgrade version-specific claims.

## Review Dimensions

For each important library, evaluate:

- idiomatic usage for the detected version
- compatibility with declared and locked versions
- deprecated APIs, legacy patterns, or migration hazards
- fit with the repository's architecture and local conventions
- clear boundaries between library/framework code and business logic
- lifecycle management for apps, sessions, clients, workers, event loops, connections, and background tasks
- error handling at the correct layer
- explicit configuration and environment assumptions
- test coverage for integration points, not only isolated helpers
- whether usage makes the repository easier or harder for Codex to understand and modify

## Finding Rules

Report findings only when they are concrete and location-backed. Every high-priority finding should include:

- the library or cross-library boundary involved
- the exact file, module, function, class, config, test, or repo-wide location
- the observed usage pattern
- why it matters for correctness, maintainability, operations, or safe modification
- a small, testable recommendation
- the risk if unchanged

Use this priority scale:

- P0: likely correctness, data integrity, deployability, or serious operational failure.
- P1: high-risk library misuse, version incompatibility, lifecycle leak, boundary violation, or missing integration test.
- P2: meaningful maintainability, explicitness, testing, or migration-risk issue.
- P3: low-risk improvement worth noting because it removes a real future trap.

## Cross-library Patterns To Check

When relevant, inspect cross-library boundaries such as:

- web framework response models plus validation/serialization schemas
- ORM session lifecycle plus request dependencies, workers, or tests
- migration metadata drifting from ORM models
- task queues plus database sessions, transactions, retries, and idempotency
- HTTP clients plus async runtime, timeouts, retries, and dependency lifecycle
- workflow engines plus state schemas, persistence, validation, and replay behavior
- test fixtures masking framework, database, task, or client integration failures
- logging/tracing losing request, job, workflow, or external-call context

## Output Format

Use this structure unless the user asks for a different format.

### 1. Dependency Discovery Summary

List detected dependency files and important libraries found. Note major version conflicts, missing lock evidence, or uncertainty.

### 2. Library Review Scope

| Library | Detected Version | Category | Review Priority | Reason |
|---|---|---|---|---|

### 3. High-priority Findings

Include P0/P1/P2 findings here. Omit the table if there are no high-priority findings.

| Priority | Library | Location | Issue | Why it matters | Recommendation | Risk if unchanged |
|---|---|---|---|---|---|---|

### 4. Per-library Review

For each reviewed library:

```markdown
#### <Library Name>

- Detected version:
- Main usage locations:
- Current usage pattern:
- What is good:
- Issues found:
- Best-practice concerns:
- Codex-legibility concerns:
- Recommended changes:
```

### 5. Cross-library Integration Issues

Identify issues involving multiple libraries. If none were found, say so and name the boundaries inspected.

### 6. Explicitness Improvements

List rules or assumptions that should be made explicit in type definitions, schemas, enums, dependency providers, config files, tests, `.manifest`, or documentation.

### 7. Recommended Follow-up Prompts

Provide 3-5 small, low-risk Codex prompts. Each prompt must target one library or one integration boundary, be easy to review and revert, and include a clear acceptance criterion.

Example:

```text
Review the SQLAlchemy session lifecycle used by FastAPI dependencies and background jobs. Acceptance criterion: produce a location-backed finding list and one minimal test or documentation change proposal for any lifecycle gap.
```
