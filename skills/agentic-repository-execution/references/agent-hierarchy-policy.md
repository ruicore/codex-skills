# Agent Hierarchy Policy

Use this reference to enforce a single delegation control plane, one-level
agent hierarchy, and bounded discovery of work without worker-created agents.

## Contents

- [Authority model](#authority-model)
- [One-level hierarchy](#one-level-hierarchy)
- [Delegation Request](#delegation-request)
- [Master disposition](#master-disposition)
- [Interaction with gates and escalation](#interaction-with-gates-and-escalation)
- [Continuity and failure handling](#continuity-and-failure-handling)

## Authority Model

Keep agent creation and assignment authority exclusively with the Root Master,
acting as the control plane. Only the Root Master may:

- create an agent;
- dispatch or re-dispatch an assignment;
- assign, transfer, merge, or narrow ownership;
- update the authoritative task graph, dependencies, and gates;
- close or replace an assignment after reviewing its evidence.

Do not interpret this authority as permission for the Master to edit code,
tests, configuration, migrations, public documentation, or another production
deliverable. Keep the Master's file writes limited to approved coordination
artifacts. Delegate every production-file edit to a bounded peer agent.

## One-Level Hierarchy

Keep delegation depth at exactly one. Treat every implementation worker,
reviewer, validator, specialist, and remediation agent as a peer dispatched
directly by the Root Master.

Forbid every dispatched agent from:

- creating, spawning, dispatching, or re-dispatching another agent;
- asking another worker to take over its production responsibility;
- changing its own ownership boundary or another agent's ownership;
- redefining the hierarchy, task graph, dependencies, or gates;
- presenting an informal collaboration as an authoritative assignment.

Make one bounded worker the default for a small coherent task. Do not create
extra assignments, approvals, or handoffs merely because delegation exists.

## Delegation Request

Permit a dispatched agent to submit a Delegation Request when discovery reveals
a coherent responsibility that should be owned by another peer. Require the
request to contain all of these fields:

- **Discovery and reason:** what new work was found and why it matters.
- **Proposed coherent responsibility:** one outcome suitable for one peer.
- **Independence from current scope:** how it differs from the requester's
  assignment and why splitting preserves responsibility.
- **Dependencies and start condition:** inputs, predecessors, and the exact
  condition under which the peer may begin.
- **Required capability:** the expertise, tools, or execution class needed.
- **Recommended execution:** runtime-verified model, reasoning effort, and
  verified skills, or the runtime default when selection is unavailable.
- **Proposed ownership and conflicts:** writable and read-only surfaces,
  prohibited overlap, integration owner, and known dirty-worktree conflicts.
- **Expected artifact:** exact files, findings, or evidence to return.
- **Validation:** commands, checks, expected evidence, and validation owner.
- **Impact if denied or deferred:** consequence for the root objective and
  affected task branch.
- **Current work state:** what continues and what pauses while the request is
  pending.

Submit the complete form from
[execution-templates.md](execution-templates.md). Do not create the proposed
agent, reserve ownership, or start its work before Master approval and dispatch.

## Master Disposition

Make the Master inspect the request against the current plan, ownership map,
dependencies, runtime capabilities, and user authority. Record exactly one
disposition:

- **Approve:** accept a coherent peer responsibility.
- **Deny:** reject work that is unnecessary, out of scope, unsupported, or
  already owned.
- **Merge:** combine it with an existing assignment whose owner can complete it
  without losing coherence.
- **Narrow:** reduce it to the smallest justified responsibility.
- **Defer:** postpone it until a named dependency, gate, or authority condition
  is satisfied.

Before an approved assignment starts, make the Master update the task graph,
ownership, dependencies, start condition, and validation gates. Then make the
Root Master create and dispatch the new peer with a complete dispatch contract.
Do not let the requesting worker perform either step.

## Interaction With Gates And Escalation

Treat a Delegation Request as a control-plane proposal, not as:

- human escalation or a request for user approval;
- a Decision Request about material business, architecture, data, security, or
  side-effect semantics;
- a fifth Evidence Gate state;
- evidence that a gate is automatically `BLOCKED`;
- permission to expand scope or authority.

Keep the four gate states unchanged: `NOT RUN`, `PASS`, `FAIL`, and `BLOCKED`.
Route material semantic or authority uncertainty through the existing Decision
Escalation and Stop Policy. A request for another agent cannot resolve or bypass
that uncertainty.

## Continuity And Failure Handling

When the proposed responsibility is independent from the requester's current
slice, continue all already authorized work. When it is a necessary dependency,
pause only the affected slice and continue genuinely independent work. Record
`BLOCKED` only when required evidence, capability, input, or authority cannot be
obtained or verified under the existing gate policy.

If the Master denies, merges, narrows, or defers the request, preserve completed
evidence and issue any changed responsibility through a new or updated Master
dispatch. Never let a worker silently absorb out-of-scope production work or
transfer its assigned responsibility to another agent.
