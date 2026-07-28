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
- <risk, mitigation, and condition that blocks progress>
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
