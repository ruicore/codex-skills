# Task Decomposition And Handoffs

Use this reference for medium or large tasks, parallel assignments, serial
phases, or any task whose ownership is unclear.

## Size The Task

Score the work qualitatively across these axes:

- behavior risk: localized, contract-affecting, or safety-critical;
- breadth: one owned surface, several modules, or repository-wide;
- uncertainty: known implementation, discovery needed, or unresolved design;
- integration: isolated, shared boundary, or multi-system;
- validation: one focused check, several layers, or live/manual evidence;
- side effects: working tree only, external mutation, publication, or
  destructive action.

Use the smallest structure that keeps ownership and validation credible:

- **Small:** one implementation agent plus master review.
- **Medium:** a few responsibility-based assignments, parallel only where
  ownership is disjoint.
- **Large:** explicit discovery or contract phase, bounded implementation
  slices, integration, and independent validation.

Do not create assignments merely to increase agent count.

## Define A Good Assignment

Make one agent accountable for one coherent outcome. Ensure the assignment can
be understood without the full conversation and validated without trusting the
agent's assertion.

Split when:

- different components have stable, disjoint ownership;
- one risk needs independent specialist review;
- a contract must be established before implementation;
- validation requires independence from the implementer;
- a phase produces inputs required by the next phase.

Do not split when:

- two agents would edit the same file or authoritative schema concurrently;
- one change is too small to justify a handoff;
- a horizontal split would obscure end-to-end behavior;
- the second assignment exists only to restate or format the first.

## Control Ownership

For each assignment, declare:

- owned files, directories, modules, or external surfaces;
- shared read-only inputs;
- prohibited files and unrelated dirty state;
- dependency and start condition;
- merge or integration owner;
- validation owner.

Avoid parallel edits to shared indexes, lockfiles, generated manifests, public
contracts, migrations, or central configuration. Serialize those changes or
give one agent sole ownership.

## Build The Task Graph

Represent dependencies as "must be available before starting or validating,"
not merely "related to."

Use parallel execution only when:

- prerequisites are already stable;
- write ownership is disjoint;
- agents do not consume one another's unreviewed output;
- integration checks can detect conflicts after completion.

Use serial execution when a downstream agent needs an upstream decision,
artifact, schema, test seam, or verified change.

## Require Handoffs

At every serial boundary:

1. make the upstream agent write the handoff;
2. inspect the handoff and referenced artifacts;
3. make the downstream agent read it before acting;
4. include the handoff path in the downstream dispatch;
5. keep the next gate closed if the handoff is missing or contradicted by the
   working tree.

Require the handoff to include:

- completed scope and incomplete scope;
- files or artifacts changed;
- decisions and assumptions;
- exact validation commands and results;
- remaining risks and known failures;
- repository and side-effect state;
- exact instructions for the next agent.

Treat the handoff as a navigation aid, not as stronger evidence than the actual
files, diff, and validation output.

## Recover From Failure

If an assignment times out, goes silent, or returns weak evidence:

1. preserve verified artifacts already produced;
2. mark the affected gate `BLOCKED` or `FAIL`;
3. isolate the smallest missing outcome;
4. re-dispatch that outcome with a tighter ownership boundary;
5. require the replacement agent to read any valid handoff or current artifact;
6. rerun downstream and integration validation.

Do not ask one replacement agent to redo every completed assignment unless the
evidence proves the prior outputs unusable.
