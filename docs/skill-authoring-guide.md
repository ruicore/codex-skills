# Skill Authoring Guide

This guide explains how to turn real engineering practice into a Codex skill
without sanding it into generic advice too early.

A Codex skill in this repository should preserve a repeatable way of working:
the trigger, evidence, sequence, guardrails, validation, and output shape that
made the original practice reliable. The goal is not to make every skill look
the same. The goal is to help a future Codex session do the same kind of work
with less guessing.

Before authoring or revising a skill, read:

- `docs/repository-contract.md`
- `docs/skill-taxonomy.md`
- `docs/side-effect-policy.md`
- `docs/public-sanitization.md`
- the relevant existing `skills/*/SKILL.md` files, references, scripts, and
  examples

Do not edit existing skills while preparing a new extraction note or proposal
unless the issue explicitly asks for that change.

## What Makes A Good Skill

A good skill is an operating aid for one recurring kind of work. It should make
the agent more reliable, not merely more verbose.

Good skills usually have these properties:

- **Concrete trigger:** a future Codex session can tell when the skill applies.
- **Clear non-goals:** the skill says what not to do, especially near adjacent
  responsibilities.
- **Evidence discipline:** the workflow names which sources outrank inference.
- **Step order:** the skill prevents premature fixes, publication, abstraction,
  or mutation.
- **Validation:** the skill defines how confidence is earned.
- **Output contract:** the final deliverable has a predictable shape.
- **Side-effect guardrails:** reads, writes, publication, and destructive actions
  are handled deliberately.
- **Practice-derived detail:** real constraints, commands, examples, and failure
  modes are retained when safe and useful.

Weak skills tend to be generic. Warning signs:

- The same text could apply to almost any repository or task.
- The skill says "be careful", "validate", or "use best practices" without
  naming the evidence or validation path.
- It reads like a checklist of values rather than a workflow a Codex agent can
  execute.
- It removes local details even though those details encode the actual guardrail.
- It broadens the trigger beyond observed use.

## Prompt, Checklist, Workflow, Or Operating Procedure

Use the smallest form that fits the practice.

### Prompt

A prompt is wording that steers a single response.

Use it when:

- the practice is only a tone, framing, or response-format preference
- there is no ordered work sequence
- no tools, files, validation, or side effects are involved

Do not promote a prompt to a skill just because it is reusable phrasing.

### Checklist

A checklist is a set of checks to remember.

Use it when:

- order is not very important
- each item can be independently verified
- the outcome is a review, readiness check, hygiene pass, or final preflight

A checklist can live inside a skill, but by itself it is not enough for work
that requires discovery, sequencing, or validation loops.

### Workflow

A workflow is an ordered sequence that gets from request to result.

Use it when:

- some steps must happen before others
- the agent needs to gather evidence, make decisions, then validate
- the work can branch based on findings
- the result should be repeatable across similar tasks

Most skills in this repository should at least be workflows.

### Operating Procedure

An operating procedure is a workflow plus safety, side-effect, failure, and
handoff rules.

Use it when:

- the skill can mutate files, repositories, accounts, boards, APIs, or public
  surfaces
- the workflow has known failure modes
- credentials, private data, or public repository hygiene are relevant
- the output must be durable, resumable, or reviewable

Tool operation, publishing, ingestion, audit, diagnosis, and repository-changing
skills should usually be operating procedures.

## Required Sections For A Skill

These sections are required for new skill proposals and should be present in a
new `SKILL.md` when the skill is mature enough. Existing skills do not need to
be rewritten just to match this structure.

### Purpose

State the concrete work the skill performs and the outcome it protects.

Good purpose statements answer:

- What kind of task is this for?
- What result should the agent produce?
- What failure does this workflow prevent?

Avoid generic purpose text such as "help with engineering tasks" or "improve
quality".

### When To Use

List observable user requests, task shapes, or repository situations that should
trigger the skill.

Good triggers are specific:

- "user asks to diagnose a bug or performance regression"
- "user asks to audit batch database access"
- "user asks to ingest an approved weekly radar report"

Weak triggers are broad:

- "when working on backend code"
- "when quality matters"
- "when the task is complex"

### When Not To Use

Define boundaries. This protects the skill from becoming a catch-all.

Include:

- adjacent skills or workflows that should handle nearby work
- requests that should remain read-only
- cases where missing inputs should stop the workflow
- situations where the skill would create unsafe or premature side effects

### Inputs To Infer Or Request

List the inputs Codex should infer from local evidence first, then request only
when necessary.

Examples:

- user-requested scope
- target repository, branch, environment, account, board, or service
- read-only versus mutation mode
- available tests, scripts, schemas, examples, or validation commands
- required dates, versions, issue IDs, report status, or artifact paths
- side-effect target and confirmation state

For each input, say whether it can be inferred, must be explicit, or must stop
the workflow when unknown.

### Evidence Hierarchy

State which evidence wins when sources conflict.

A typical repository-facing hierarchy is:

1. User's explicit latest instruction.
2. Actual code paths, scripts, schemas, configs, tests, and committed files.
3. Runtime output, validation results, screenshots, traces, or logs gathered for
   the task.
4. Repository docs, ADRs, runbooks, examples, comments, and README guidance.
5. Tool documentation or external sources when current behavior depends on them.
6. Naming conventions and inference.

Adapt the hierarchy to the skill. For external tools, live API state may outrank
old local notes. For approved report ingestion, the reviewed report may be the
canonical input. For public repository work, sanitization policy outranks a raw
practice note that contains private detail.

Do not let inference outrank checked evidence.

### Workflow

Write the ordered steps the agent should follow.

Good workflow steps are operational:

- inspect specific files or directories
- identify primitives before broad search
- build a feedback loop before fixing
- preview a mutation before calling an API
- run a named validation command
- update an index after writing source files

Avoid steps that only restate values:

- "be thorough"
- "follow best practices"
- "ensure quality"

If the workflow branches, state the branch condition and the next action.

### Validation Requirements

Define what must be checked before the agent claims the work is done.

Validation can include:

- repository tests, linting, schema checks, or `git diff --check`
- dry-run commands or generated input previews
- rendered document, slide, PDF, image, or UI screenshots
- query-count tests, replay scripts, fixtures, or repro loops
- public sanitization review
- manual checks when no automated validation exists

Name skipped checks and why they were skipped.

### Output Contract

Specify what the final answer or artifact must contain.

Examples:

- prioritized findings with file and line evidence
- a PRD or issue pack with required headings
- created file paths and validation results
- a decision trace with context, decision, alternatives, and consequences
- a publish preflight summary with destination, mode, time, and rollback notes

The output contract should make the result reviewable without reading the
agent's hidden reasoning.

### Side-Effect Policy

Classify the skill using `docs/side-effect-policy.md`.

At minimum, state:

- default side-effect level
- maximum side-effect level in normal use
- which user instruction unlocks mutation, publication, or destructive action
- required preview, confirmation, or dry-run
- credential handling rules
- rollback or cleanup expectations

When uncertain, choose the higher side-effect level and add guardrails. Do not
weaken an existing confirmation boundary to make a workflow feel smoother.

### Failure Modes

List known ways the skill can go wrong and what Codex should do.

Useful failure modes include:

- required evidence cannot be found
- validation command is missing, flaky, or unsafe
- input date, version, account, branch, or target is ambiguous
- private data appears in source material
- API authentication fails
- the requested mutation target is locked, disconnected, or wrong
- no correct test seam exists
- the workflow would need a broader behavior change than requested

For each failure mode, say whether to stop, ask the user, downgrade confidence,
produce a read-only report, or continue with a manual validation note.

## Preserving Practice While Removing Sensitive Details

Real practice is the source material. Do not delete concrete workflow details
just because they are personal, local, or tool-specific.

Remove or replace:

- secrets, tokens, API keys, passwords, cookies, and private keys
- private URLs, internal hostnames, dashboards, and issue links
- customer, employer, vendor, account, and project identifiers
- raw private logs, request bodies, responses, screenshots, and datasets
- machine-specific absolute paths in reusable examples

Preserve when safe:

- command shapes
- confirmation boundaries
- validation commands
- directory conventions
- artifact names and expected file shapes
- known failure modes
- local assumptions that explain why the workflow works

Use placeholders that preserve meaning:

- `<repo>` for a repository
- `<ticket_url>` for an issue or ticket
- `<service_name>` for a private service
- `<account_id>` for an external account
- `<internal_hostname>` for a private host
- `<artifact_path>` for a local output

Add portability notes instead of vague rewrites:

```markdown
Portability note: This workflow originally used `<tool_name>` for preview and
dry-run behavior. Future adopters should substitute the equivalent preview step
for their tool, but should keep the preview-before-mutation rule.
```

If a detail cannot be sanitized without losing the workflow, keep it out of the
public repository and narrow the skill to the safe behavior.

## Assigning Category And Maturity

Use `docs/skill-taxonomy.md` for the current category and maturity vocabulary.
Do not invent new labels unless a separate issue updates the taxonomy.

### Category

Pick one primary category based on the skill's actual work:

- `core-engineering`
- `review-audit`
- `planning-execution`
- `agent-memory`
- `research`
- `tool-ops`
- `visual-artifacts`
- `publishing`

Use a secondary category only when it changes how a reader should understand the
skill. For example, a tool operation skill that schedules public posts can be
primary `tool-ops` and secondary `publishing`.

Do not change category to express a future aspiration. Category describes what
the skill currently does.

### Maturity

Assign maturity by evidence, not formatting:

- `practice-note`: extracted from one real task or habit; useful but incomplete.
- `personal-skill`: safe and useful in the author's workflow; adaptation likely.
- `portable-candidate`: mostly reusable, but still needs examples, validation,
  or de-personalization.
- `stable-workflow`: repeatable, validated, bounded, and safe for public reuse.
- `deprecated`: retained for compatibility, not recommended for new work.

A skill can be valuable at `practice-note` or `personal-skill`. Do not promote
it just because it now has headings.

## Deciding Whether Practice Is Ready For A Reusable Skill

Use this readiness test before creating a reusable skill directory.

The practice is probably ready when:

- it has been used more than once, or one use revealed a clearly repeatable
  operating discipline
- the trigger is specific enough for a future Codex session to recognize
- the workflow has an ordered sequence, not only preferences
- the required inputs and stop conditions are known
- the output can be reviewed by another engineer
- side effects and confirmation boundaries are understood
- sensitive details can be sanitized without destroying the workflow
- at least one validation path exists, even if manual

Keep it as an extraction note when:

- it came from one incident and the repeatable part is not yet clear
- the value depends on private project context that cannot be public
- the workflow is mostly commands without trigger, evidence, or validation rules
- the practice overlaps several existing skills and needs classification first
- the only improvement would be generic wording

Use `templates/skill-extraction-note.md` for early practice capture. Use
`templates/skill-proposal.md` when the workflow is ready to discuss as a skill.

## Avoiding Generic Advice

Generic advice sounds correct but does not change agent behavior.

Replace generic advice with operating detail:

| Generic | Better |
|---|---|
| Validate the result. | Run the repository's validation command. If none exists, run `git diff --check` and manually verify links, headings, and placeholders. |
| Be careful with credentials. | Use environment variables or connector auth. Never print, commit, or paste tokens. Replace account IDs with `<account_id>` in examples. |
| Review the code thoroughly. | Identify project-specific primitives first, then search call sites and trace from public entry points. |
| Avoid unsafe changes. | Default to read-only. Require explicit user instruction before file edits, commits, pushes, API writes, publication, or deletion. |
| Produce a useful summary. | Report scope, evidence inspected, findings, validation run, skipped checks, and remaining uncertainty. |

When writing a skill, ask:

- What exact evidence should the agent inspect?
- What should happen first, second, and last?
- What would make this workflow unsafe?
- What must be previewed before mutation?
- What can be validated automatically?
- What should the final answer include?
- Which concrete practice detail am I tempted to delete, and can I sanitize or
  classify it instead?

If the answer is still "follow best practices", the material is not ready for a
skill.
