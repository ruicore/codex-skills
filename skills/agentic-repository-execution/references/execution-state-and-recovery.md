# Execution State And Recovery

Use this reference for non-trivial serial work whose current ownership, gate
position, or safe recovery point would otherwise be ambiguous after interruption.

## Contents

- [Activation](#activation)
- [Authority and update rules](#authority-and-update-rules)
- [Minimal snapshot contract](#minimal-snapshot-contract)
- [Valid JSON example](#valid-json-example)
- [Consistency invariants](#consistency-invariants)
- [Recovery procedure](#recovery-procedure)
- [Artifact authority](#artifact-authority)
- [Explicit non-goals](#explicit-non-goals)

## Activation

The Root Master may create
`<coordination-root>/execution-state.json` when one or more of these conditions
apply:

- work has two or more serial phases;
- a later peer must consume an earlier handoff;
- several assignments and gates make recovery ambiguous;
- re-dispatch, interruption, or context compaction is reasonably likely;
- a stopped task or branch must resume later.

Keep the snapshot optional. Do not create it for a small coherent task that one
implementation peer and independent Validation can complete without a serial
recovery boundary.

## Authority And Update Rules

The Root Master is the only authoritative writer. Workers, reviewers,
validators, and remediation peers return artifacts and proposed state inputs;
they do not update the authoritative snapshot.

Rewrite one valid JSON document after a control-plane boundary:

- plan acceptance;
- dispatch, re-dispatch, ownership, or dependency change;
- inspected handoff or expected artifact;
- Evidence Gate change;
- Decision Request, Stop Record, routing substitution, timeout, or partial
  result that changes the safe continuation point;
- task stop, resume, or completion.

Increment `revision`, write a UTC `updated_at`, and identify `updated_by` on
every update. Give a replacement owner a new assignment ID and retain the old
assignment as `stopped`.

Assignment lifecycle and Evidence Gates are separate. An assignment may be
`active`, `handoff_ready`, or `complete` while its assurance gate remains
`NOT RUN`. An implementer cannot mark its own gate `PASS`.

## Minimal Snapshot Contract

Required top-level fields:

| Field | Meaning |
|---|---|
| `schema_version` | Portable document shape, initially `1.0`. |
| `task_id` | Stable repository-task identifier. |
| `plan_path` | Path to the authoritative Markdown execution plan. |
| `revision` | Monotonically increasing snapshot revision. |
| `updated_at` | UTC ISO-8601 time of the latest Root Master update. |
| `updated_by` | Root Master identity or stable role label. |
| `task_state` | Bounded lifecycle plus authority reference. |
| `assignments` | Ownership and lifecycle facts needed for recovery. |
| `artifacts` | Paths and provenance for plans, handoffs, decisions, evidence, and outputs. |
| `gates` | Authoritative four-state Evidence Gate snapshot. |
| `recovery` | Last reconciled checkpoint and required recovery reads. |

`task_state` requires:

- `status`: `planned`, `active`, `stopped`, or `complete`;
- `active_assignment_ids`: current assignment IDs, or an empty array;
- `authority_ref`: the plan section or artifact defining current scope and
  side-effect authority.

Each `assignments[]` item requires:

- `id`, `role`, and `owner_id`;
- `state`: `planned`, `active`, `handoff_ready`, `complete`, or `stopped`;
- `start_gate_ids`;
- exact `writable_surfaces`;
- `artifact_refs`;
- `handoff_ref`, or `null`.

Each `artifacts[]` item requires:

- `id`;
- `kind`: `plan`, `handoff`, `decision_request`, `stop_record`,
  `routing_substitution`, `validation`, or `output`;
- exact `path`;
- `produced_by`;
- `verified_by_gate_ids`.

Each `gates[]` item requires:

- `id`;
- `state`: exactly `NOT RUN`, `PASS`, `FAIL`, or `BLOCKED`;
- `evidence_owner_id`;
- `evidence_refs`;
- UTC `checked_at`, or `null` for `NOT RUN`;
- `remaining_uncertainty`: `none` or one explicit gap.

`recovery` requires:

- `checkpoint_id`;
- `verified_gate_ids`;
- `resume_assignment_ids`;
- exact `required_reads`;
- `decision_request_refs`;
- `stop_record_refs`.

The resume list is not a dispatch queue. The Root Master must recheck capability,
ownership, worktree state, authority, and start gates before dispatch.

## Valid JSON Example

```json
{
  "schema_version": "1.0",
  "task_id": "repository-change",
  "plan_path": ".coordination/repository-change/execution-plan.md",
  "revision": 3,
  "updated_at": "2030-01-15T09:30:00Z",
  "updated_by": "root-master",
  "task_state": {
    "status": "active",
    "active_assignment_ids": ["T2"],
    "authority_ref": ".coordination/repository-change/execution-plan.md#risk-and-authority"
  },
  "assignments": [
    {
      "id": "T1",
      "role": "implementer",
      "owner_id": "implementation-peer",
      "state": "complete",
      "start_gate_ids": [],
      "writable_surfaces": ["src/component"],
      "artifact_refs": ["A1"],
      "handoff_ref": "A1"
    },
    {
      "id": "T2",
      "role": "validator",
      "owner_id": "validation-peer",
      "state": "active",
      "start_gate_ids": ["G1"],
      "writable_surfaces": [],
      "artifact_refs": ["A1"],
      "handoff_ref": null
    }
  ],
  "artifacts": [
    {
      "id": "A1",
      "kind": "handoff",
      "path": ".coordination/repository-change/handoffs/implementation.md",
      "produced_by": "T1",
      "verified_by_gate_ids": ["G1"]
    }
  ],
  "gates": [
    {
      "id": "G1",
      "state": "PASS",
      "evidence_owner_id": "root-master",
      "evidence_refs": ["A1"],
      "checked_at": "2030-01-15T09:25:00Z",
      "remaining_uncertainty": "none"
    },
    {
      "id": "G2",
      "state": "NOT RUN",
      "evidence_owner_id": "validation-peer",
      "evidence_refs": [],
      "checked_at": null,
      "remaining_uncertainty": "independent validation is in progress"
    }
  ],
  "recovery": {
    "checkpoint_id": "implementation-accepted-before-validation",
    "verified_gate_ids": ["G1"],
    "resume_assignment_ids": ["T2"],
    "required_reads": [
      ".coordination/repository-change/execution-plan.md",
      ".coordination/repository-change/handoffs/implementation.md"
    ],
    "decision_request_refs": [],
    "stop_record_refs": []
  }
}
```

The example deliberately records `T2` as `active` while `G2` is `NOT RUN`.
Lifecycle status does not prove liveness or open a dependent gate.

## Consistency Invariants

1. The file parses as one object with a supported `schema_version`.
2. `revision` increases on every Root Master update.
3. Every referenced assignment, artifact, and gate ID exists.
4. Every required artifact path is readable, or its gate is `BLOCKED`.
5. Every `recovery.verified_gate_ids` item names a `PASS` gate.
6. Every resume candidate has all `start_gate_ids` at `PASS`.
7. Active assignments do not have overlapping writable surfaces.
8. `handoff_ready` or `complete` never changes a gate by itself.
9. Use `FAIL` only for inspected noncompliance and `BLOCKED` for unavailable
   required evidence, capability, input, or authority.
10. The snapshot never widens plan scope, ownership, side effects, or authority.

Do not put subjective handoff confidence in execution-state. Confidence is
navigation metadata, not evidence, lifecycle, or a gate.

## Recovery Procedure

After a new session, Root Master replacement, timeout, silence, or compaction:

1. Read current repository instructions and the Markdown plan first.
2. Parse the snapshot and note its revision and updater.
3. Read every `recovery.required_reads` path.
4. Inspect the current working tree, actual artifacts, diffs, and evidence for
   every recorded `PASS`.
5. Reconcile conflicts through the skill's Evidence Hierarchy.
6. Treat `active` as historical ownership state, not proof of a live agent.
7. Preserve verified artifacts and stop an absent or replaced assignment.
8. Have the Root Master create a new bounded assignment for only the missing
   responsibility.
9. Resume only when start gates remain `PASS`, ownership is conflict-free,
   runtime capability is adequate, and authority still covers the action.
10. Increment and rewrite the snapshot before dispatch.

If the file is missing or invalid, reconstruct it from current repository
evidence, the plan, handoffs, Decision Requests, Stop Records, validation
outputs, and runtime controls. Never reconstruct `PASS` without inspecting its
required evidence. Use `NOT RUN` only when no attempt occurred; use `BLOCKED`
when required attempted proof cannot be recovered.

## Artifact Authority

| Artifact | Purpose |
|---|---|
| Execution plan | Normative scope, graph, ownership, risk, authority, gates, and stops. |
| Execution-state snapshot | Current machine-readable recovery index; never widens the plan. |
| Phase handoff | Detailed work, decisions, author checks, risks, and next instructions. |
| Decision Request / Stop Record | Existing material-decision and resume evidence. |
| Actual files, diff, tests, and runtime output | Strongest task-local proof after user and repository authority. |

The plan answers what may happen. The snapshot answers where execution stands
and what must be read. A handoff answers what a phase returned.

## Explicit Non-Goals

Do not turn execution-state into a ledger, append-only log, database, daemon,
scheduler, heartbeat, liveness monitor, event bus, auto-dispatch queue,
cross-repository control plane, or workflow service.
