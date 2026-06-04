# Codex Skills

This is my personal collection of Codex skills. The repository is public so it can also serve as a portfolio of how I structure reusable agent workflows: diagnosis loops, review protocols, specification writing, test-driven development, and durable engineering decision traces.

These skills are written as agent-facing operating procedures rather than public documentation. They are opinionated, tuned for my own Codex usage, and intended to be easy to inspect, adapt, or fork.

This is not an official OpenAI skill library.

## Why This Exists

I use Codex as an engineering partner, not only as a code generator. These skills capture the parts of engineering work that should be repeatable:

- turning vague product or engineering requests into scoped execution plans
- debugging with a disciplined reproduce, minimize, instrument, and regression-test loop
- reviewing architecture and implementation decisions with repository-local context
- preserving decisions in durable notes so future agents do not rediscover the same constraints
- keeping test-driven development practical without turning tests into brittle ceremony

The skills are intentionally written as operating procedures because the goal is reliable behavior under real project pressure, not a polished prompt gallery.

## Skills

- `agent-legibility-review`: a framework-agnostic repository review workflow for finding AI-agent navigation risks, hidden rules, duplicated authorities, and ambiguous ownership.
- `architecture-review`: a repository architecture review workflow focused on ownership, authoritative sources, boundaries, drift, and phased refactor planning.
- `diagnose`: a disciplined reproduce, minimize, hypothesize, instrument, fix, and regression-test loop for hard bugs and performance regressions.
- `decision-trace-writer`: a workflow for preserving stable engineering decisions as durable, agent-facing traces.
- `grill-me`: a direct senior-engineer critique mode for plans, designs, implementations, PRs, and technical decisions.
- `grill-with-docs`: a deeper architecture and domain review workflow grounded in repository-local docs and conventions.
- `prd-to-issues`: a converter from PRDs or implementation briefs into scoped, sequenced execution issues.
- `tdd`: a test-driven development workflow with supporting notes on tests, mocking, interface design, refactoring, and deep modules.
- `write-a-prd`: a workflow for turning rough ideas or engineering requests into structured PRDs and implementation-ready specs.

## Layout

- `skills/`: Codex skill directories.
- `skills/*/SKILL.md`: the main instructions for each skill.
- `skills/*/agents/openai.yaml`: optional metadata for discovery and UI presentation.
- `skills/*/*.md`: supporting references, templates, and conventions used by a skill.
- `skills/*/scripts/`: optional helper scripts used by a skill.

The repository root is intentionally small so additional Codex-related assets can be added beside `skills/` later without obscuring the skill definitions.

## Use

Each skill is self-contained. To reuse one, copy the relevant directory under your Codex skills path and review its `SKILL.md` before relying on it in a different repository or workflow.

Because these are personal workflows, treat them as examples of agent operating design rather than universal best practices.

## Example Workflows

- Use `write-a-prd` to turn a rough implementation idea into a decision-ready product or engineering brief.
- Use `prd-to-issues` to split that brief into sequenced implementation issues with explicit validation.
- Use `tdd` when a change needs a tight test-first loop.
- Use `grill-with-docs` before merging architecture-heavy changes that depend on repository conventions.
- Use `decision-trace-writer` after important tradeoffs are settled so future work has a stable reference.
