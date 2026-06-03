# Codex Skills

This is my personal collection of Codex skills. The repository is public so it can also serve as a portfolio of how I structure reusable agent workflows: diagnosis loops, review protocols, specification writing, test-driven development, and durable engineering decision traces.

These skills are written as agent-facing operating procedures rather than public documentation. They are opinionated, tuned for my own Codex usage, and intended to be easy to inspect, adapt, or fork.

This is not an official OpenAI skill library.

## Skills

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
