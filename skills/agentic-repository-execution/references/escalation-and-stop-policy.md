# Escalation And Stop Policy

Use this reference to classify uncertainty and risk, enforce worker and master
authority, resolve Decision Requests, and stop only the scope made unsafe by an
unresolved decision.

## Contents

- [Uncertainty classification](#uncertainty-classification)
- [Risk classification](#risk-classification)
- [Authority boundary](#authority-boundary)
- [Decision escalation](#decision-escalation)
- [Blocking uncertainty and stop protocol](#blocking-uncertainty-and-stop-protocol)
- [Evidence Gates and human escalation](#evidence-gates-and-human-escalation)
- [Examples](#examples)

## Uncertainty Classification

Classify the decision, not the worker's confidence or the apparent task size.

### Routine uncertainty

Continue without escalation when all of these are true:

- inspected evidence or a stable repository convention supports one reliable
  choice;
- the choice stays inside the assignment and the user's existing authority;
- the result is reversible and low-impact;
- the choice does not alter an authoritative contract or user-visible meaning.

Examples include following an established naming pattern, choosing the local
test helper already used by adjacent tests, or adjusting an internal
implementation detail with unchanged behavior. Record the choice only when it
constrains later work or would otherwise be hard to reconstruct.

### Material uncertainty

Pause the affected slice and send a Decision Request when multiple reasonable
options remain and the choice may affect any of these surfaces:

- architecture ownership or component responsibility;
- public API, compatibility, protocol, or user-visible semantics;
- data model, integrity, retention, backfill, or migration behavior;
- security, trust, identity, permissions, or credential handling;
- external side effects, publication, deployment, or live state;
- irreversible or difficult-to-recover behavior;
- the worker's assigned scope, owned surface, or side-effect limit.

Material uncertainty is not permission to make the least disruptive guess.

### Blocking uncertainty

Treat uncertainty as blocking only after the master checks the Evidence
Hierarchy and still lacks the evidence or authority required to choose safely.
Set the affected gate to `BLOCKED`, persist a Stop Record, and request one
specific human decision. Do not label a routine judgment `BLOCKED`.

## Risk Classification

Classify each assignment by the highest credible consequence of an error. Risk
changes execution intensity, never authority. Low risk does not mean the action
is authorized, and Critical risk does not prohibit work that is explicitly
authorized and adequately controlled.

| Level | Typical examples | Required execution intensity |
|---|---|---|
| Low | Localized test, internal refactor with established behavior, narrow docs or metadata edit | One bounded owner, focused validation, master diff review |
| Medium | Multi-file behavior change, shared configuration, non-public integration seam, dependency update within an existing policy | Explicit contract and rollback, stronger tests, serial ownership for shared files, independent review when semantics are not obvious |
| High | Public API or compatibility, schema or migration, authentication or permissions, external writes, concurrency or data-integrity behavior | Discovery or contract phase first, strongest suitable reasoning, independent specialist review, explicit stop conditions, layered validation |
| Critical | Destructive or irreversible mutation, production migration or deletion, trust-boundary redesign, credential or key handling, change whose failure can corrupt shared state broadly | Whole-task preflight, explicit human authority where required, isolated execution, rollback or recovery proof, independent review and validation before dependent work |

Raise the level when uncertainty, blast radius, irreversibility, or validation
difficulty increases. Use the level to:

1. choose slice size and serial versus parallel ownership;
2. route to an adequate available capability and reasoning effort;
3. require independent review or specialist validation;
4. define stop gates before mutation;
5. decide whether a shared blocker stops one branch or the whole task.

Do not lower the level because a preferred model, reviewer, test environment, or
deadline is unavailable. Reduce scope or record `BLOCKED` instead.

## Authority Boundary

### Worker

A worker may make routine implementation judgments inside its explicit
assignment and side-effect limit. A worker must not independently:

- expand scope or take ownership of an unassigned surface;
- change public API, compatibility, protocol, or user-visible semantics;
- change data-model, integrity, retention, backfill, or migration semantics;
- change security, trust, identity, permissions, or credential boundaries;
- introduce a dependency, service, platform, or infrastructure requirement;
- perform a higher side-effect action than the dispatch authorizes.

When any item becomes necessary or plausibly affected, pause the slice and send
a Decision Request.

### Master

The master may resolve a Decision Request only when stronger evidence supports
the choice and the user's original authorization already covers it. Record the
evidence, decision, constraints, and affected gates, then re-dispatch the
bounded work.

The master may not grant itself or a worker new scope, public-contract freedom,
data or security authority, infrastructure authority, or a higher side-effect
level. Deadlines, convenience, sunk work, and a desire to report completion are
not authority.

### Human

Ask the human only for the missing decision or authority that materially blocks
safe progress. State concrete options and risks. Do not ask the human to approve
routine repository-conforming choices, rerun ordinary validation, or operate
every Evidence Gate.

## Decision Escalation

1. Stop mutation on the affected slice while preserving verified artifacts.
2. Inspect enough current evidence to explain why the decision is not routine.
3. Complete a Decision Request using the form in
   [execution-templates.md](execution-templates.md). Emit or persist every field
   before the escalation is accepted or handed to the master. Prefer a safe
   coordination location; when none exists, output the complete record in the
   worker response. Stating that a request should be created is not completion.
4. Keep dependent work closed; allow only genuinely independent, safe work.
5. Make the master inspect the cited evidence and the Evidence Hierarchy.
6. If existing evidence and authority support one option, record the bounded
   resolution and re-dispatch with updated constraints.
7. If evidence or authority is still missing, apply the stop protocol.

Do not let a worker present a completed speculative implementation as the
Decision Request. A reversible spike may be authorized as read-only or isolated
evidence gathering, but it must not silently become the production decision.

## Blocking Uncertainty And Stop Protocol

When escalation cannot be resolved:

1. Complete a Stop Record using the form in
   [execution-templates.md](execution-templates.md). Emit or persist every field
   before the master treats a decision-related gate as `BLOCKED`. Persist it at
   a safe coordination location readable by the next agent; when none exists,
   output the complete record in the master response. Stating that a Stop
   Record should be created is not gate or stop closure.
2. Only after that complete record is available, set the affected Evidence Gate
   to `BLOCKED`; do not add a fifth state.
3. Stop dependent mutation and validation that would rely on the unresolved
   decision.
4. Ask the human the single smallest question that supplies the missing
   evidence or authority.
5. Resume only after recording the answer, confirming its authority, and
   updating the plan, dispatch, and affected gates.

Apply these completion requirements only to material and blocking decision
escalation. Routine uncertainty and ordinary validation `FAIL` handling do not
require a Decision Request or Stop Record.

Use **whole-task STOP** when the blocker affects:

- the root objective or target;
- a shared authoritative contract or assumption;
- data integrity or migration correctness;
- security, trust, identity, or permission boundaries;
- irreversible behavior or destructive scope;
- every branch through a shared schema, dependency, configuration, or generated
  source of truth.

Use **branch STOP** when the affected dependency branch can be isolated and
other work has disjoint ownership, stable inputs, existing authority, and no
chance of laundering the unresolved decision into shared output. Record which
branches may continue and why.

## Evidence Gates And Human Escalation

Evidence Gates are sequencing controls: execute within existing authority,
collect the required proof, and permit dependent work only on `PASS`. They do
not require a human before normal execution.

Human escalation is an authority or decision path used only when material
uncertainty remains unresolved after master review. A gate may be `BLOCKED`
because that escalation is pending, but the two mechanisms are not synonyms.

Keep the four states unchanged:

- `NOT RUN`: validation has not been attempted;
- `PASS`: required evidence is verified;
- `FAIL`: evidence proves noncompliance;
- `BLOCKED`: required evidence, capability, input, or authority cannot be
  obtained or verified.

## Examples

- A neighboring module establishes the formatter and naming pattern: routine;
  follow it and continue.
- Two internal helpers are equally suitable but behavior and ownership stay
  unchanged: routine; choose the repository-consistent option.
- A fix can preserve an old public response or adopt a cleaner incompatible
  shape: material; pause and send a Decision Request.
- A migration needs a retention or backfill rule absent from code and user
  authority: blocking after master review; `BLOCKED` and whole-task STOP when
  all implementation depends on that schema.
- One optional adapter needs a new external dependency, while unrelated tests
  have stable inputs and disjoint ownership: stop that dependency branch;
  continue only the independent tests.
