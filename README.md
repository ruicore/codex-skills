# Codex Skills

Reusable AI-assisted engineering workflows for Codex, evolving from a personal practice library toward a public reusable workflow library.

This repository is not a prompt gallery. It is a small operating manual library for repeatable engineering work: diagnosis, code review, architecture review, database access audit, test-driven development, specification writing, PRD-to-issue planning, durable decision traces, reviewed weekly radar ingestion, radar history analysis, external research, visual artifacts, publishing workflows, and tool-specific operations.

The goal is to make AI-assisted engineering more reliable under real project pressure. Each skill defines a workflow that an agent can follow with local repository evidence, explicit validation, and clear boundaries.

The repository should become more reusable by preserving what has worked in real practice, then adding public hygiene, classification, portability notes, examples, metadata, and validation around that behavior. Reusable does not mean universal. Do not generalize, rename, restructure, or rewrite skills just to make the repository look more polished.

This is a personal skill library, not an official OpenAI project.

## What This Is / What This Is Not

This is:

- a practice-derived library of Codex engineering workflows
- a place for concrete operating procedures, guardrails, evidence rules, and validation paths
- a growing public toolkit whose reuse should stay grounded in observed skill behavior
- a repository where personal or tool-specific workflow details can remain when they are safe, classified, and useful

This is not:

- a prompt gallery
- a generic framework for every possible Codex workflow
- a marketing-polished package that hides its practice-derived origin
- a place for secrets, credentials, private customer or project details, private URLs, raw logs, or sensitive identifiers
- a reason to normalize every skill into the same structure before the repository has evidence that the structure fits

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
- researching current AI engineering career signals and content opportunities
- turning sponsorship emails into prioritized brand-deal lead lists
- operating specialized tools such as Buffer, Paper, Readwise, Excalidraw, and genmedia with repeatable guardrails

The skills are intentionally written as operating procedures because the target outcome is repeatable engineering behavior, not clever wording.

## Repository Guides

The repository direction is captured in a small set of docs:

- [docs/repository-contract.md](docs/repository-contract.md) defines the grounded evolution contract.
- [docs/skill-taxonomy.md](docs/skill-taxonomy.md) defines category and maturity labels.
- [docs/public-sanitization.md](docs/public-sanitization.md) defines public repository hygiene.
- [docs/side-effect-policy.md](docs/side-effect-policy.md) defines read, write, publishing, and destructive-operation guardrails.
- [docs/skill-authoring-guide.md](docs/skill-authoring-guide.md) explains how to turn real practice into a skill without premature generalization.

Use these docs to classify, contain, and validate existing behavior. Do not use them as permission for broad directory moves or cosmetic rewrites.

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
- `skills/*/agents/openai.yaml` contains optional discovery metadata; see [docs/agent-metadata.md](docs/agent-metadata.md).
- `skills/*/*.md` contains supporting references, templates, or conventions.
- `skills/*/scripts/` contains helper scripts when a workflow needs one.

Use a skill when the task matches the workflow, not because the skill name sounds related. For example, use `diagnose` when there is a concrete bug or performance regression; use `architecture-review` when the question is about ownership, boundaries, authority, or change surface.

[skills/index.json](skills/index.json) is the machine-readable registry for skill metadata, including category, maturity, side-effect level, supporting files, validation expectations, and portability notes. It is descriptive metadata for the current skill set, not a requirement to move or rewrite directories.

Run the repository validation command after skill, docs, registry, or README changes:

```bash
python scripts/validate_skills.py
```

## Skill Categories

The current category map comes from [docs/skill-taxonomy.md](docs/skill-taxonomy.md) and [skills/index.json](skills/index.json). Categories describe what skills do today; they should not be used to force restructuring.

| Category | Current skills | Primary use |
|---|---|---|
| `core-engineering` | `diagnose`, `tdd` | Implementation, debugging, testing, and feedback loops. |
| `review-audit` | `agent-legibility-review`, `architecture-review`, `database-access-audit`, `grill-me`, `grill-with-docs`, `python-backend-review`, `python-ecosystem-review` | Evidence-first review, critique, architecture assessment, and audit work. |
| `planning-execution` | `prd-to-issues`, `write-a-prd` | Turning ambiguous ideas, requirements, or plans into scoped execution artifacts. |
| `agent-memory` | `decision-trace-writer`, `radar-analysis`, `weekly-radar-ingestion` | Preserving durable context or analyzing stored agent-readable records. |
| `research` | `ai-career-signal-researcher`, `brand-deal-researcher` | Gathering, evaluating, synthesizing, or prioritizing external signals. |
| `tool-ops` | `buffer-publisher`, `genmedia`, `paper-mcp`, `readwise-cli-control` | Operating a specific external tool, local service, CLI, API, or connected account. |
| `visual-artifacts` | `excalidraw-diagrams`, `paper-deck-style` | Creating, editing, or styling visual deliverables. |
| `publishing` | `buffer-publisher`, `brand-deal-researcher`, `genmedia` | Preparing, scheduling, queueing, publishing, or packaging outward-facing artifacts. |

## Skills and Engineering Outcomes

| Skill | Engineering outcome | What it protects against |
|---|---|---|
| <nobr><code>diagnose</code></nobr> | Builds a fast feedback loop before fixing bugs. | Guessing, unverified fixes, missing regression tests. |
| <nobr><code>tdd</code></nobr> | Drives implementation through behavior-focused red-green-refactor slices. | Brittle tests, implementation-coupled tests, speculative code. |
| <nobr><code>architecture&#8209;review</code></nobr> | Reviews ownership, authority, boundaries, drift, and change surface. | Scattered rules, duplicated concepts, unclear module responsibility. |
| <nobr><code>database&#8209;access&#8209;audit</code></nobr> | Reviews database access patterns across stacks with read-only, evidence-first scope control. | Looped DB I/O, unsafe bulk writes, N+1 queries, missing scope predicates, transaction drift, and unverified rowcount assumptions. |
| <nobr><code>agent&#8209;legibility&#8209;review</code></nobr> | Finds repository navigation risks for future coding agents. | Hidden conventions, conflicting docs, ambiguous task entry points. |
| <nobr><code>grill&#8209;me</code></nobr> | Applies direct senior-engineer critique to plans and implementation choices. | Weak assumptions, vague tradeoffs, under-specified risks. |
| <nobr><code>grill&#8209;with&#8209;docs</code></nobr> | Grounds critique in local repository docs and decision records. | Generic advice that ignores project-specific constraints. |
| <nobr><code>python&#8209;backend&#8209;review</code></nobr> | Reviews Python backend fundamentals across typing, async, config, logging, packaging, and tests. | Backend regressions caused by ecosystem or maintainability blind spots. |
| <nobr><code>python&#8209;ecosystem&#8209;review</code></nobr> | Checks important third-party library usage and integration boundaries. | Misused dependencies, version drift, unsafe ecosystem assumptions. |
| <nobr><code>write&#8209;a&#8209;prd</code></nobr> | Turns rough ideas into structured product or engineering briefs. | Ambiguous requirements and unreviewable implementation starts. |
| <nobr><code>prd&#8209;to&#8209;issues</code></nobr> | Splits a brief into scoped, dependency-aware execution issues. | Horizontal task splitting, untestable tickets, unclear sequencing. |
| <nobr><code>decision&#8209;trace&#8209;writer</code></nobr> | Records durable technical decisions for future readers and agents. | Repeated rediscovery of settled constraints and rationale. |
| <nobr><code>weekly&#8209;radar&#8209;ingestion</code></nobr> | Ingests Ray-reviewed weekly AI Systems Engineering Radar reports into durable signal records. | Treating approved reports as drafts, losing reasoning, and unstructured long-term agent memory. |
| <nobr><code>radar&#8209;analysis</code></nobr> | Mines reviewed AI signal radar history for monthly reviews, quarterly synthesis, theme analysis, and idea candidates. | Unsupported trend claims, summary drift, and analysis detached from reviewed repository evidence. |
| <nobr><code>ai&#8209;career&#8209;signal&#8209;researcher</code></nobr> | Researches AI systems engineering career signals, market demand, and portfolio opportunities. | Hype-driven learning plans, popularity-only evidence, and recommendations detached from backend engineering reality. |
| <nobr><code>brand&#8209;deal&#8209;researcher</code></nobr> | Converts sponsorship and paid-promotion emails into researched, prioritized lead lists. | Missing real opportunities, duplicate follow-ups, weak fit scoring, and unverified brand claims. |
| <nobr><code>buffer&#8209;publisher</code></nobr> | Operates Buffer accounts, channels, ideas, drafts, queues, and scheduled posts through the GraphQL API. | Accidental publishing, wrong-channel posts, missing preflight checks, and unsafe social-post mutations. |
| <nobr><code>excalidraw&#8209;diagrams</code></nobr> | Creates polished editable Excalidraw diagrams from text descriptions and structured plans. | Unclear diagram scope, inconsistent visual style, and non-editable one-off visuals. |
| <nobr><code>genmedia</code></nobr> | Uses the genmedia CLI to discover, inspect, run, and manage fal.ai model endpoints. | Invented endpoint IDs, schema guessing, credential leakage, and untracked generated media. |
| <nobr><code>paper&#8209;deck&#8209;style</code></nobr> | Guides minimal, spacious, high-end Paper slide deck design. | Crowded slides, text-heavy decks, mismatched section styles, and weak visual hierarchy. |
| <nobr><code>paper&#8209;mcp</code></nobr> | Edits open Paper boards through the local Paper MCP server with inspection and screenshot verification. | Fragile UI automation, unverified board edits, raw node-ID leakage, and accidental destructive canvas changes. |
| <nobr><code>readwise&#8209;cli&#8209;control</code></nobr> | Searches, exports, organizes, and automates Readwise or Reader through the official CLI. | Browser-auth dead ends, missing source links, raw result dumps, and unconfirmed library writes. |

## Design Principles

- **Workflow over prompt:** a useful skill defines steps, evidence, checkpoints, and validation.
- **Local evidence first:** repository docs, code, tests, configs, and runtime behavior outrank generic best practices.
- **Bounded scope:** each skill should do one kind of engineering work well.
- **Observable outcomes:** a skill should produce a review, test, issue plan, decision trace, or verified fix.
- **Validation before confidence:** claims should be backed by tests, repro loops, source inspection, or explicit uncertainty.
- **Practice is signal:** personal or project-derived details can encode real guardrails; sanitize, classify, or add portability notes before deleting them.
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
- keep [skills/index.json](skills/index.json) aligned when public skill metadata changes
- run `python scripts/validate_skills.py` after changes that touch skills, docs, registry metadata, or README links

Because these are practice-derived workflows, treat them as examples of agent operating design rather than universal best practices. Improve reuse incrementally: preserve behavior first, sanitize public-facing content, classify current maturity, and generalize only after repeated repository evidence supports it.
