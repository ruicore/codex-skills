# Execution Templates

Copy and adapt only the forms needed by the repository. Keep them in an existing
coordination convention or a simple ignored task directory; do not create a
complex hierarchy merely to host templates.

## Execution Plan

```markdown
# <task> Execution Plan

## Goal
<observable outcome>

## Scope
- <included responsibility>

## Non-goals
- <excluded responsibility>

## Evidence and constraints
- User authority: <read/edit/commit/push/deploy boundary>
- Repository rules: <paths inspected>
- Current state: <branch, dirty files, relevant versions>
- Available capabilities: <sub-agents, tools, skills, validation>
- Risk classification: <Low|Medium|High|Critical and why>
- Authority boundary: <worker/master limits>

## Gate states
- `NOT RUN`: not attempted; do not start dependent work.
- `PASS`: required evidence verified; dependent work may start.
- `FAIL`: evidence proves a requirement is unmet; remediate and revalidate.
- `BLOCKED`: required evidence cannot be obtained or verified; resolve or
  re-dispatch and revalidate.

Only `PASS` permits dependent work to start.

## Task graph
| ID | Owner/surface | Depends on | Mode | Gate |
|---|---|---|---|---|
| T1 | <responsibility> | none | serial/parallel | NOT RUN |

## Expected artifacts
- <path or result>

## Validation gates
| Gate | Evidence | Owner | Status |
|---|---|---|---|
| G1 | <command/check and expected result> | <agent/master> | NOT RUN |

## Risks and stop conditions
- <risk, mitigation, affected gate, and branch/whole-task stop condition>
```

## Sub-agent Dispatch

```markdown
# Dispatch <ID>: <title>

Goal:
<one coherent outcome>

Scope:
- <owned work>

Non-goals:
- <explicit exclusions>

Expected artifacts:
- <exact files, outputs, or findings>

Validation:
- <exact commands or manual checks>
- <evidence the agent must return>

Ownership:
- Writable: <files/directories/surfaces>
- Read-only/shared: <inputs>
- Do not touch: <unrelated or conflicting surfaces>

Dependencies and inputs:
- <prior artifact or handoff path>
- Read the prior handoff before starting: <yes/no>

Side-effect limit:
<read-only/local-files/git-working-tree; explicitly excluded higher actions>

Risk and authority:
- Risk: <Low|Medium|High|Critical with consequence>
- Worker may decide: <routine choices inside the assignment>
- Must escalate: <material decisions or surfaces outside worker authority>
- Stop condition and scope: <condition; branch|whole task>

Recommended execution:
- Capability class: <frontier high-reasoning|balanced engineering|fast deterministic>
- Model: <runtime-advertised model|runtime default (selection unavailable)>
- Reasoning effort: <supported value|runtime default>
- Skills: <verified available skills or none>
- Rationale: <one sentence>

Handoff:
- Write to: <path or response contract>
- Include completed work, files changed, decisions, validation results, risks,
  and exact next instructions.
```

## Phase Handoff

```markdown
# <phase> Handoff

## Completed
- <verified outcome>

## Incomplete or blocked
- <remaining outcome and reason>

## Files and artifacts
- `<path>`: <what changed or what it proves>

## Decisions
- <decision, evidence, and downstream constraint>

## Decision requests and stops
- <Decision Request or Stop Record path, affected gate, and current scope>

## Validation
- `<command or check>`: NOT RUN|PASS|FAIL|BLOCKED
  - Evidence: <result or artifact>

## Repository and side-effect state
- Branch/worktree: <state>
- Performed: <edits or other authorized effects>
- Not performed: <commit, push, publish, deploy, destructive action>

## Risks
- <remaining uncertainty>

## Next agent instructions
1. Read <required files>.
2. Own <bounded surface>.
3. Preserve <invariant/non-goal>.
4. Run <validation>.
```

## Decision Request

Use this when a worker encounters material uncertainty. Keep the affected slice
paused until the master records a bounded resolution or applies the stop
protocol.

```markdown
# Decision Request <ID>: <short title>

- Decision needed: <the exact choice>
- Why unresolved: <why current evidence does not establish a routine choice>
- Evidence checked: <files, tests, schemas, runtime output, or rules>
- Options and risks:
  1. <option and consequence>
  2. <option and consequence>
- Recommendation: <preferred option, evidence, and residual uncertainty>
- Authority required: <existing authority that covers it, or missing authority>
- Affected gate: <gate ID and current state>
- Stop scope while pending: <slice|dependency branch|whole task and why>
- Safe independent work: <bounded work that may continue, or none>
- Human question if master cannot resolve: <one concrete question>

## Master resolution

- Decision: <selected option, or unresolved>
- Evidence and authority: <why the master may decide, or what remains missing>
- Constraints and re-dispatch: <updated boundary and assignment, or none>
- Gate update: <NOT RUN|PASS|FAIL|BLOCKED and reason>
```

## Stop Record

Use this only after the master cannot resolve material uncertainty from
available evidence within existing authority.

```markdown
# Stop Record <ID>: <short title>

- Blocking decision: <the exact unresolved decision>
- Why unresolved: <missing evidence or authority>
- Evidence checked: <sources inspected by worker and master>
- Options and risks: <remaining options and consequences>
- Recommendation: <safest supported path, or none>
- Authority required: <specific missing authority, or evidence owner>
- Affected gate: <gate ID set to BLOCKED>
- Stop scope: <dependency branch|whole task>
- Dependent work stopped: <task IDs or surfaces>
- Safe independent work: <task IDs and why they remain independent, or none>
- Persisted artifacts: <plan, Decision Request, logs, or evidence paths>
- Human question: <single concrete clarification required to resume>
- Resume condition: <answer/evidence plus plan, dispatch, and gate updates>
```

## Gate Record

```markdown
## Gate <ID>: <name>

- Owner: <agent or master>
- Expected evidence: <artifact and result>
- Validation: `<command>` or <manual check>
- Status: NOT RUN|PASS|FAIL|BLOCKED
- Observed result: <concise evidence>
- Remaining uncertainty: <none or explicit gap>
- Follow-up dispatch: <ID or none>
```

## Master Final Review

```markdown
# Final Review

- Outcome: COMPLETED|PARTIAL|BLOCKED
- Scope preserved: NOT RUN|PASS|FAIL|BLOCKED
- Expected artifacts present: NOT RUN|PASS|FAIL|BLOCKED
- Integrated diff reviewed: NOT RUN|PASS|FAIL|BLOCKED
- Required validation gate: NOT RUN|PASS|FAIL|BLOCKED
- Handoffs complete: NOT RUN|PASS|FAIL|BLOCKED
- Ownership conflicts resolved: NOT RUN|PASS|FAIL|BLOCKED
- Public sanitization checked: NOT RUN|PASS|FAIL|BLOCKED
- Unrelated user changes preserved: NOT RUN|PASS|FAIL|BLOCKED
- Authorized side effects only: NOT RUN|PASS|FAIL|BLOCKED
- Non-PASS gates and next action: <details>
```

Omit a final-review check when it does not apply. Do not introduce another gate
state.
