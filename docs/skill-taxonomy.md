# Skill Taxonomy

This document defines a lightweight taxonomy for the existing `codex-skills`
repository.

The taxonomy is descriptive metadata. It does not require moving, renaming,
splitting, merging, or rewriting any skill directory. Use it to describe what a
skill currently does, how mature it is, and what would need to improve before it
is presented as a more portable public workflow.

## Scope

Use this taxonomy when:

- adding README or index metadata for skills
- deciding what examples, validation, or portability notes a skill needs
- reviewing whether a skill is safe for a public repository
- planning small, behavior-preserving improvements to an existing skill

Do not use this taxonomy to justify broad reorganization. A skill can belong to
one primary category and, when useful, one secondary category. Category labels
should not change the skill's trigger, workflow, or non-goals.

## Categories

### core-engineering

Workflow skills for implementation, debugging, testing, and engineering
execution loops.

Current skills:

- `diagnose`
- `tdd`

### review-audit

Evidence-first review and audit workflows that inspect a repository, plan,
implementation, data access surface, or technical decision for risks and
actionable findings.

Current skills:

- `agent-legibility-review`
- `architecture-review`
- `database-access-audit`
- `grill-me`
- `grill-with-docs`
- `python-backend-review`
- `python-ecosystem-review`

### planning-execution

Skills that turn ambiguous intent, product requirements, specifications, or
plans into scoped execution artifacts.

Current skills:

- `prd-to-issues`
- `write-a-prd`

### agent-memory

Skills that preserve durable context for future Codex runs or analyze stored
agent-readable records.

Current skills:

- `decision-trace-writer`
- `radar-analysis`
- `weekly-radar-ingestion`

### research

Skills that gather, evaluate, synthesize, or prioritize external signals.

Current skills:

- `ai-career-signal-researcher`
- `brand-deal-researcher`

### tool-ops

Skills for operating a specific external tool, local service, CLI, API, or
connected account with repeatable guardrails.

Current skills:

- `buffer-publisher`
- `genmedia`
- `paper-mcp`
- `readwise-cli-control`

### visual-artifacts

Skills that create, edit, or style visual deliverables.

Current skills:

- `excalidraw-diagrams`
- `paper-deck-style`

### publishing

Skills that prepare, schedule, queue, publish, or package outward-facing
artifacts.

Current skills:

- `buffer-publisher`
- `brand-deal-researcher`
- `genmedia`

`publishing` is often a secondary category. For example, `buffer-publisher` is
primarily `tool-ops`, but also belongs here because its workflow can create or
schedule public posts.

## Maturity Levels

Maturity describes public-readiness and reuse confidence. It is not a judgment
of usefulness. A low-maturity skill may be valuable because it preserves a real
workflow that should not be generalized yet.

### practice-note

Early extraction from real work, not yet a full skill.

When to use it:

- The workflow came from one concrete task, project, account, or local habit.
- The useful behavior is visible, but triggers, boundaries, validation, or
  public examples are still incomplete.
- The material may be closer to notes, commands, or a playbook than a reusable
  Codex skill.

Public repository hygiene required:

- Remove secrets, tokens, session data, private keys, passwords, and raw
  credential material.
- Replace private customer, employer, project, issue, URL, dashboard, hostname,
  path, and account identifiers with neutral placeholders.
- Do not include raw logs, screenshots, datasets, request bodies, or responses
  that expose sensitive identifiers.
- Mark local assumptions clearly instead of presenting them as general rules.

Before promoting to `personal-skill`:

- The skill has a clear trigger and a concrete outcome.
- The practice-derived steps are sanitized enough for public review.
- The workflow can be followed without access to private context.
- At least one non-goal or boundary is documented when the skill could be
  misused.

What Codex should not change automatically:

- Do not remove specific practice-derived details only because they are local.
- Do not rename the skill or rewrite it into generic advice.
- Do not invent examples, validation, or tool support that did not come from the
  workflow.
- Do not promote it based on formatting alone.

### personal-skill

Useful and sanitized, but still tied to the author's workflow.

When to use it:

- The skill is safe to publish and useful in the author's normal Codex work.
- It may depend on personal defaults, preferred tools, local operating style, or
  a specific account/service setup.
- Reuse by another person is possible, but adaptation is expected.

Public repository hygiene required:

- Keep all private identifiers and credential material out of the repository.
- Label account-specific, machine-specific, or service-specific assumptions.
- Prefer placeholders and portability notes over private examples.
- Keep mutation, publishing, and external-account operations behind explicit
  confirmation rules.

Before promoting to `portable-candidate`:

- Required inputs, expected outputs, and important non-goals are documented.
- Local assumptions are separated from required workflow behavior.
- The skill has at least one reusable example, checklist, script, or validation
  path that does not depend on private data.
- The skill's behavior has been used or reviewed enough to show the workflow is
  not a one-off note.

What Codex should not change automatically:

- Do not de-personalize by deleting the operating discipline that makes the
  skill work.
- Do not broaden the trigger beyond observed use.
- Do not change external-tool behavior or confirmation semantics without an
  explicit issue.
- Do not split the skill just because it has local details.

### portable-candidate

Mostly reusable, but still needs examples, validation, or de-personalization.

When to use it:

- The skill has clear triggers, non-goals, and a repeatable workflow.
- Most steps can be used in other repositories or accounts with limited
  adaptation.
- Remaining gaps are concrete: missing examples, weak validation, stale local
  assumptions, or incomplete public metadata.

Public repository hygiene required:

- Public examples must be synthetic, neutral, or scrubbed.
- Tool commands must avoid real account IDs, private hostnames, and durable
  machine-specific paths unless explicitly marked as local setup examples.
- Validation scripts must not require private services by default.
- Any required secrets must be referenced as environment variables or connector
  setup, never embedded values.

Before promoting to `stable-workflow`:

- The skill has stable trigger language and explicit non-goals.
- The workflow has validation: tests, dry-runs, linting, schema checks, review
  checklist, replay fixture, screenshot inspection, or another concrete
  verification method appropriate to the skill.
- At least one example shows the expected input and output shape.
- Public hygiene has been reviewed after the latest substantive change.
- The skill's behavior is documented well enough that a future Codex run can
  apply it without reconstructing hidden context.

What Codex should not change automatically:

- Do not promote by adding boilerplate sections that are not connected to real
  behavior.
- Do not introduce a shared schema across skills unless multiple skills already
  need the same fields.
- Do not rewrite mature workflow steps for style consistency only.
- Do not move support files into new folders unless a separate issue asks for
  that structure.

### stable-workflow

Reusable Codex engineering workflow with clear triggers, non-goals, validation,
and examples.

When to use it:

- The skill is safe for public reuse and has a proven, repeatable operating
  procedure.
- A Codex agent can determine when to use it, what not to do, what evidence to
  collect, and how to validate the result.
- Support files such as examples, references, scripts, or metadata are aligned
  with the main `SKILL.md`.

Public repository hygiene required:

- Re-check hygiene whenever examples, scripts, references, or generated
  artifacts are updated.
- Keep validation commands and expected outputs free of private data.
- Document required external credentials as setup requirements only.
- Remove stale private assumptions instead of layering exceptions around them.

Before changing within `stable-workflow`:

- Confirm the change preserves the skill's documented behavior, or explicitly
  mark it as a behavior change in the issue or PR.
- Update examples, references, validation, or README/index entries when the
  public skill surface changes.
- Run available validation and state any skipped checks.
- Keep compatibility notes when changing trigger language or output shape.

What Codex should not change automatically:

- Do not expand the skill into adjacent responsibilities without repeated
  evidence.
- Do not collapse it into another skill for taxonomy neatness.
- Do not remove examples or validation unless replacing them with stronger
  equivalents.
- Do not treat stable as frozen; small evidence-backed improvements are allowed.

### deprecated

Retained only for historical compatibility.

When to use it:

- A skill has been superseded, is unsafe to recommend, depends on retired tools,
  or remains only so older references do not break.
- New work should use another skill or no skill.

Public repository hygiene required:

- Deprecated material must still be safe to publish.
- Add a clear replacement or reason for retention when known.
- Remove or neutralize stale commands that could cause harmful mutations.
- Keep enough context for historical compatibility, but avoid preserving private
  operational detail.

Before promoting out of `deprecated`:

- The skill has a current owner or use case.
- Unsafe or stale behavior has been removed or explicitly guarded.
- Replacement guidance is updated.
- The skill re-enters the lifecycle no higher than `personal-skill` unless it
  already has current validation and examples.

What Codex should not change automatically:

- Do not delete deprecated skills without an explicit issue.
- Do not silently redirect triggers to another skill.
- Do not modernize deprecated workflows opportunistically.
- Do not keep sensitive historical material for compatibility.

## Initial Maturity Map

This map is a starting point for repository maintenance. It should be updated
only when a concrete change improves or reduces a skill's public readiness.

| Skill | Primary category | Secondary category | Current maturity |
|---|---|---|---|
| `agent-legibility-review` | `review-audit` |  | `portable-candidate` |
| `ai-career-signal-researcher` | `research` | `agent-memory` | `personal-skill` |
| `architecture-review` | `review-audit` |  | `portable-candidate` |
| `brand-deal-researcher` | `research` | `publishing` | `personal-skill` |
| `buffer-publisher` | `tool-ops` | `publishing` | `personal-skill` |
| `database-access-audit` | `review-audit` |  | `portable-candidate` |
| `decision-trace-writer` | `agent-memory` | `planning-execution` | `personal-skill` |
| `diagnose` | `core-engineering` |  | `portable-candidate` |
| `excalidraw-diagrams` | `visual-artifacts` |  | `personal-skill` |
| `genmedia` | `tool-ops` | `publishing` | `personal-skill` |
| `grill-me` | `review-audit` | `planning-execution` | `portable-candidate` |
| `grill-with-docs` | `review-audit` | `agent-memory` | `personal-skill` |
| `paper-deck-style` | `visual-artifacts` |  | `personal-skill` |
| `paper-mcp` | `tool-ops` | `visual-artifacts` | `personal-skill` |
| `prd-to-issues` | `planning-execution` |  | `portable-candidate` |
| `python-backend-review` | `review-audit` |  | `portable-candidate` |
| `python-ecosystem-review` | `review-audit` |  | `portable-candidate` |
| `radar-analysis` | `agent-memory` | `research` | `personal-skill` |
| `readwise-cli-control` | `tool-ops` | `research` | `personal-skill` |
| `tdd` | `core-engineering` |  | `portable-candidate` |
| `weekly-radar-ingestion` | `agent-memory` | `research` | `personal-skill` |
| `write-a-prd` | `planning-execution` |  | `portable-candidate` |

No existing skill is marked `stable-workflow` yet because this repository does
not currently apply a consistent metadata, example, and validation standard
across skills. No existing skill is marked `deprecated` by this document.

## Maintenance Rules

- Prefer updating this document after observing real maintenance needs, not
  before.
- A taxonomy change should preserve skill behavior unless the issue explicitly
  requests a behavior change.
- Category changes should cite the skill's current trigger and workflow, not a
  desired future identity.
- Maturity promotion should be tied to concrete evidence: examples, validation,
  clearer non-goals, safer public hygiene, or repeated successful use.
- Maturity demotion is appropriate when a skill accumulates stale private
  assumptions, unsafe commands, missing validation, or unclear triggers.
- Do not reorganize `skills/` as part of taxonomy maintenance.
