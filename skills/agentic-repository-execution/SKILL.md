---
name: agentic-repository-execution
description: Coordinate repository implementation through a master agent that discovers local rules, persists a scoped plan, delegates every production-file change to sub-agents, manages ownership and handoffs, and closes evidence-based validation gates. Use when the user asks for delegated or multi-agent repository execution, a master/sub-agent workflow, staged autonomous implementation, parallel work with conflict control, or strict independent review of agent-written changes.
---

# Agentic Repository Execution

## Purpose

Run repository-changing work as a governed delegation system. Keep the master
agent responsible for understanding, decomposition, dispatch, review, and
validation while sub-agents make every code or production-file change.

Protect against vague oversized assignments, conflicting parallel edits,
context loss between phases, invented capabilities, weak validation evidence,
and a master silently taking over implementation.

## Boundaries

- Use this procedure for implementation work that can be delegated through the
  current runtime.
- Do not use it for a simple answer, translation, isolated read-only question,
  or task where multi-agent governance adds no execution value.
- Do not use it to turn every small task into many assignments. Give a bounded
  low-risk change to one implementation agent when that is the smallest useful
  delegation.
- Do not replace the repository's `AGENTS.md`, task graph, issue tracker,
  durable-memory convention, or user-specified coordination location.
- Do not let the master edit code, tests, configuration, migrations, public
  documentation, or other production deliverables. Allow the master to write
  only coordination artifacts in an approved local convention.
- Do not claim delegated execution when the runtime cannot start sub-agents.
  Report `BLOCKED` instead of letting the master implement as a fallback.
- Do not treat this skill as permission to commit, push, publish, deploy, or
  perform destructive actions. Require the authority applicable to each action.

## Inputs

Infer these inputs from the latest user instruction and repository evidence
before asking:

- target repository, branch, worktree, and requested outcome;
- scope, non-goals, acceptance criteria, and side-effect authority;
- repository instructions, ownership boundaries, public hygiene rules, and
  durable coordination conventions;
- available sub-agent controls, models, reasoning efforts, skills, tools, and
  validation commands;
- dirty-worktree state and files that must not be touched;
- dependencies, risky surfaces, and serial versus parallel work.

Ask only when an unresolved choice would materially change scope, behavior,
target, or authority. Stop when the repository or user requires an input that
cannot be inferred safely.

## Evidence Hierarchy

Resolve conflicts in this order:

1. Follow the user's latest explicit instruction and side-effect boundary.
2. Follow applicable repository instructions and governance files.
3. Trust current code, tests, schemas, configuration, task graphs, and version
   control state.
4. Trust validation output, runtime observations, and generated diffs gathered
   for this task.
5. Use current repository docs, handoffs, decision traces, and existing skills.
6. Use current tool or platform documentation when runtime behavior depends on
   it.
7. Use naming conventions and inference only after checking stronger evidence.

Never let a stale plan, old handoff, model assumption, or remembered skill name
outrank inspected current state.

## Master Contract

Keep these responsibilities with the master:

- interpret the request and maintain scope;
- discover repository rules and available execution capabilities;
- persist and update the execution plan;
- choose task boundaries, order, ownership, and gates;
- dispatch bounded work with complete contracts;
- inspect returned artifacts, diffs, and validation evidence;
- re-dispatch missing or insufficient work;
- perform the final integrated review and report status.

Delegate all implementation and production-file edits. Do not reinterpret a
sub-agent timeout, silence, partial response, or unsupported capability as
permission for the master to write the missing change.

## Workflow

### 1. Discover Before Planning

Inspect the repository root, applicable instruction files, current branch and
worktree state, existing task or memory conventions, relevant skills, tools,
tests, and validation entry points.

Use repository-native code discovery before broad text search when available.
Scan the runtime's actual skill inventory before recommending skills. Never
invent a skill, model, reasoning effort, or tool.

Confirm that sub-agent execution is available. If it is unavailable and the
task requires production changes, stop with `BLOCKED`.

### 2. Persist The Execution Plan

For non-trivial work, write the plan before production changes. Use the
user-specified or repository-defined coordination location. Otherwise, prefer a
simple ignored `.manifest/<task>/execution-plan.md` when the repository permits
it.

Do not create a complex `.manifest` hierarchy silently. If `.manifest` is
tracked, prohibited, or conflicts with local governance, use the existing
agent-memory or task convention instead.

Record goal, scope, non-goals, expected artifacts, task graph, ownership,
validation gates, side-effect boundaries, and current status. Use the plan form
in [execution-templates.md](references/execution-templates.md).

### 3. Size And Decompose The Work

Choose the fewest assignments that preserve clear responsibility and
independent validation. Evaluate behavior risk, change breadth, uncertainty,
integration coupling, file overlap, and side effects.

- Give a small localized change to one implementation agent.
- Split medium work by coherent responsibility, risk, or independently
  verifiable outcome.
- Split large work into discovery or contract work, bounded implementation
  slices, integration, and independent validation.

Do not split by file count alone. Do not give one agent a broad instruction such
as "implement the whole feature" when the work crosses unclear responsibilities
or validation domains.

Read [task-decomposition-and-handoffs.md](references/task-decomposition-and-handoffs.md)
before dispatching medium, large, serial, or parallel work.

### 4. Route And Dispatch

For every assignment, state:

- Goal
- Scope
- Non-goals
- Expected artifacts
- Validation
- recommended model
- recommended reasoning effort
- recommended skills

Also state owned files or surfaces, dependencies, required inputs, side-effect
limits, and the handoff path when relevant.

Read [model-and-effort-routing.md](references/model-and-effort-routing.md) before
recommending execution settings. Name only models and effort values advertised
by the current runtime. If selection is unavailable, record the runtime default
instead of inventing a value.

Use the dispatch form in
[execution-templates.md](references/execution-templates.md). Treat the
recommendations as routing guidance, not as claims that unavailable settings
can be selected.

### 5. Execute With Ownership And Handoffs

Run independent assignments in parallel only when their write ownership does
not overlap and neither depends on the other's unreviewed output. Prefer serial
work when agents would edit the same file, change the same contract, or consume
the same evolving state.

Require a handoff at every serial phase boundary. Make the next agent read the
previous handoff before starting. Require each handoff to list completed work,
changed artifacts, decisions, validation results, remaining risks, and exact
next instructions.

Do not use chat memory as the only handoff for durable multi-stage work.

### 6. Hold Evidence Gates

Use exactly four gate states:

- `NOT RUN`: no validation attempt has occurred; keep the gate closed and do
  not start dependent work.
- `PASS`: verify all required evidence; only this state permits dependent work
  to start.
- `FAIL`: evidence proves that a requirement is unmet; keep the gate closed,
  assign narrow remediation, and revalidate.
- `BLOCKED`: required evidence cannot be obtained or verified, or a required
  capability or input is missing; keep the gate closed, resolve the blocker or
  re-dispatch, and revalidate.

Apply this model to every gate in the linked references and templates. Choose
`FAIL` only when verified evidence proves noncompliance; choose `BLOCKED` when
the required evidence cannot be obtained or verified. Do not introduce another
gate state. Inspect the actual files and diff; do not accept a completion claim
by itself.

If an agent does not return, returns partial work, crosses scope, or supplies
insufficient evidence:

1. record `FAIL` when evidence proves noncompliance, otherwise record `BLOCKED`;
2. preserve usable evidence;
3. narrow the missing responsibility;
4. re-dispatch that bounded responsibility;
5. rerun affected validation.

Never count absent evidence as success. Never widen a re-dispatch merely to
avoid another coordination step.

### 7. Perform The Master Final Review

After every assignment gate is `PASS`, inspect the integrated working tree and
verify:

- requested behavior and artifacts are present;
- scope and non-goals were preserved;
- no parallel ownership conflict or unreviewed overwrite remains;
- repository tests and required checks passed;
- checks in `NOT RUN` or `BLOCKED` are explicit;
- public files contain no credentials or private identifiers;
- no unrelated user change was staged, reverted, or overwritten;
- commit, push, publication, deployment, and destructive boundaries remain
  within explicit authority.

Keep the final gate closed when integrated evidence is incomplete, even if every
individual agent reported success.

## Validation

Define observable gates before implementation starts. Use repository-native
tests, linting, type checks, builds, schema validation, dry-runs, rendered
previews, or manual inspection appropriate to each artifact.

Require each gate record to contain:

- expected evidence;
- exact command or manual check;
- owner;
- result: `NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`;
- artifact or output location;
- remaining uncertainty.

Rerun integration checks after combining parallel work. Run diff and
scope-boundary review even when automated tests succeed. State every skipped
check and why.

## Output Contract

Return a concise completion report containing:

- outcome: `COMPLETED`, `PARTIAL`, or `BLOCKED`;
- delegated assignments and ownership;
- files or artifacts changed;
- validation commands and results;
- non-`PASS` gates, risks, and skipped checks;
- side effects performed and explicitly not performed;
- exact next action when work remains.

Keep durable execution artifacts at the approved coordination location. Do not
include hidden reasoning, raw credentials, private payloads, or unsupported
success claims.

## Side-Effect Policy

Default to `read-only` discovery and planning. Reach at most
`git-working-tree` in normal use, and only after the user requests repository
implementation. Delegate working-tree edits; preview broad changes through the
plan and inspect the diff before closure.

Require separate explicit authority for staging, committing, branch changes,
pushing, PR or MR creation, deployment, publication, and destructive action.
This skill does not grant those permissions. Preserve unrelated dirty work and
never place credentials in dispatches, handoffs, logs, public files, or final
reports.

## Failure Modes

- **No sub-agent capability:** record the affected gate as `BLOCKED`; do not let
  the master implement.
- **No safe coordination location:** use the existing repository convention or
  ask when placement materially affects version control or privacy. Record
  `BLOCKED` when no safe location can be resolved.
- **Ambiguous target or authority:** record `BLOCKED`, stop before mutation, and
  request the missing decision.
- **Unavailable recommended model, effort, skill, or tool:** reroute using only
  current capabilities and record the substitution. Record `BLOCKED` if no
  adequate capability remains.
- **Overlapping parallel ownership:** pause the conflicting assignment, inspect
  the shared state, record the affected gate as `BLOCKED`, then serialize or
  redefine ownership.
- **Missing handoff:** record `BLOCKED` and request or reconstruct the handoff
  from verified artifacts through a bounded agent task.
- **Agent timeout or incomplete evidence:** record `BLOCKED`, narrow and
  re-dispatch; do not infer completion.
- **Validation failure:** record `FAIL`, assign diagnosis or remediation, and
  rerun the failed and integration checks.
- **Private data in artifacts:** stop publication or registration, sanitize the
  public surface, record the affected gate as `FAIL`, and revalidate.
- **Scope expansion discovered:** preserve completed in-scope work, record
  `BLOCKED`, and ask for new authority before expanding.
