# Codex Skills

Reusable AI-assisted engineering workflows for Codex.

This repository is not a prompt gallery. It is a small operating manual library for repeatable engineering work: diagnosis, code review, architecture review, database access audit, test-driven development, specification writing, PRD-to-issue planning, durable decision traces, reviewed weekly radar ingestion, and radar history analysis.

The goal is to make AI-assisted engineering more reliable under real project pressure. Each skill defines a workflow that an agent can follow with local repository evidence, explicit validation, and clear boundaries.

This is a personal skill library, not an official OpenAI project.

## Why This Exists

I use Codex as an engineering partner, not only as a code generator. The work that benefits most from reusable skills is the work where consistency matters:

- turning vague requests into scoped implementation plans
- debugging with a reproduce, minimize, instrument, fix, and regression-test loop
- reviewing architecture using repository-local evidence
- auditing database access patterns without assuming a specific stack
- preserving decisions so future work does not rediscover the same constraints
- keeping TDD practical and behavior-focused
- converting product or engineering briefs into executable issue plans
- ingesting reviewed AI systems radar reports into durable agent-readable memory
- analyzing reviewed radar history for monthly, quarterly, theme, and idea-mining reports

The skills are intentionally written as operating procedures because the target outcome is repeatable engineering behavior, not clever wording.

## Install

Copy the skill directory you want into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/diagnose ~/.codex/skills/
```

Then review the copied `SKILL.md` before relying on it in another repository. Some skills include supporting notes or scripts; keep those files with the skill directory.

## Use

Each skill is self-contained:

- `skills/*/SKILL.md` contains the main workflow.
- `skills/*/agents/openai.yaml` contains optional discovery metadata.
- `skills/*/*.md` contains supporting references, templates, or conventions.
- `skills/*/scripts/` contains helper scripts when a workflow needs one.

Use a skill when the task matches the workflow, not because the skill name sounds related. For example, use `diagnose` when there is a concrete bug or performance regression; use `architecture-review` when the question is about ownership, boundaries, authority, or change surface.

## Skills and Engineering Outcomes

| Skill | Engineering outcome | What it protects against |
|---|---|---|
| <nobr><code>diagnose</code></nobr> | Builds a fast feedback loop before fixing bugs. | Guessing, unverified fixes, missing regression tests. |
| <nobr><code>tdd</code></nobr> | Drives implementation through behavior-focused red-green-refactor slices. | Brittle tests, implementation-coupled tests, speculative code. |
| <nobr><code>architecture-review</code></nobr> | Reviews ownership, authority, boundaries, drift, and change surface. | Scattered rules, duplicated concepts, unclear module responsibility. |
| <nobr><code>database-access-audit</code></nobr> | Reviews database access patterns across stacks with read-only, evidence-first scope control. | Looped DB I/O, unsafe bulk writes, N+1 queries, missing scope predicates, transaction drift, and unverified rowcount assumptions. |
| <nobr><code>agent-legibility-review</code></nobr> | Finds repository navigation risks for future coding agents. | Hidden conventions, conflicting docs, ambiguous task entry points. |
| <nobr><code>grill-me</code></nobr> | Applies direct senior-engineer critique to plans and implementation choices. | Weak assumptions, vague tradeoffs, under-specified risks. |
| <nobr><code>grill-with-docs</code></nobr> | Grounds critique in local repository docs and decision records. | Generic advice that ignores project-specific constraints. |
| <nobr><code>python-backend-review</code></nobr> | Reviews Python backend fundamentals across typing, async, config, logging, packaging, and tests. | Backend regressions caused by ecosystem or maintainability blind spots. |
| <nobr><code>python-ecosystem-review</code></nobr> | Checks important third-party library usage and integration boundaries. | Misused dependencies, version drift, unsafe ecosystem assumptions. |
| <nobr><code>write-a-prd</code></nobr> | Turns rough ideas into structured product or engineering briefs. | Ambiguous requirements and unreviewable implementation starts. |
| <nobr><code>prd-to-issues</code></nobr> | Splits a brief into scoped, dependency-aware execution issues. | Horizontal task splitting, untestable tickets, unclear sequencing. |
| <nobr><code>decision-trace-writer</code></nobr> | Records durable technical decisions for future readers and agents. | Repeated rediscovery of settled constraints and rationale. |
| <nobr><code>weekly-radar-ingestion</code></nobr> | Ingests Ray-reviewed weekly AI Systems Engineering Radar reports into durable signal records. | Treating approved reports as drafts, losing reasoning, and unstructured long-term agent memory. |
| <nobr><code>radar-analysis</code></nobr> | Mines reviewed AI signal radar history for monthly reviews, quarterly synthesis, theme analysis, and idea candidates. | Unsupported trend claims, summary drift, and analysis detached from reviewed repository evidence. |

## Design Principles

- **Workflow over prompt:** a useful skill defines steps, evidence, checkpoints, and validation.
- **Local evidence first:** repository docs, code, tests, configs, and runtime behavior outrank generic best practices.
- **Bounded scope:** each skill should do one kind of engineering work well.
- **Observable outcomes:** a skill should produce a review, test, issue plan, decision trace, or verified fix.
- **Validation before confidence:** claims should be backed by tests, repro loops, source inspection, or explicit uncertainty.
- **Reusable but not universal:** these skills encode opinions and defaults; adapt them before using them in a different engineering culture.

## Example Workflow

Vague task:

> "This API sometimes returns the wrong result. Can you fix it?"

Repeatable skill-driven flow:

1. Use `diagnose` to build a deterministic feedback loop: failing test, replay script, CLI fixture, or HTTP request.
2. Reproduce the exact symptom and capture the failure mode.
3. Generate ranked, falsifiable hypotheses before changing code.
4. Add targeted instrumentation that maps to one hypothesis at a time.
5. Convert the minimized repro into a regression test at the correct seam.
6. Fix the bug and rerun both the regression test and the original repro.
7. If the bug exposed unclear ownership or poor test seams, use `architecture-review` to identify the smallest boundary improvement.
8. If the fix requires a broader change, use `prd-to-issues` to split follow-up work into verifiable slices.
9. Use `decision-trace-writer` when an important tradeoff or constraint needs to be preserved.

The value is not that the agent receives a better phrase. The value is that the work becomes inspectable, repeatable, and easier to resume later.

## Maintenance

This repository is versioned informally through Git history. When changing a skill:

- keep the skill focused on its original engineering outcome
- update supporting notes when workflow assumptions change
- prefer concrete examples over broad advice
- remove stale instructions rather than layering exceptions
- test scripts or templates locally when they are part of the workflow

Because these are personal workflows, treat them as examples of agent operating design rather than universal best practices.
