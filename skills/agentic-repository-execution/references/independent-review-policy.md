# Independent Review Policy

Use this reference before choosing the assurance path or dispatching Review and
Validation for repository changes.

## Contents

- [Role boundaries](#role-boundaries)
- [Assurance paths](#assurance-paths)
- [Risk thresholds](#risk-thresholds)
- [Medium-risk review waiver](#medium-risk-review-waiver)
- [Medium-risk role merge](#medium-risk-role-merge)
- [Revision and remediation rule](#revision-and-remediation-rule)
- [Task-splitting anti-patterns](#task-splitting-anti-patterns)
- [Handoff confidence](#handoff-confidence)

## Role Boundaries

### Implementation

The implementer owns production edits and author checks: focused tests, lint,
type checks, builds, local inspection, and diff checks. Call these **author
checks** or **implementation evidence**, never independent Validation.

The implementer may not Review or Validate the same artifact or revision.

### Independent Review

Independent Review is a read-only adversarial correctness assessment. The
reviewer inspects the current files and actual diff, challenges the change
against scope and authoritative contracts, and searches for missed consumers,
semantic drift, unsafe assumptions, compatibility breaks, and
counter-evidence.

### Validation

Validation is an independent, reproducible evidence check of the exact current
artifact. The validator executes or reproduces the required tests, builds,
schemas, dry-runs, runtime observations, rendered checks, or manual acceptance
checks and verifies their provenance.

Use `FAIL` when inspected evidence proves noncompliance. Use `BLOCKED` when
required proof cannot be obtained or verified.

### Root Master Final Review

The Root Master closes control-plane integration after all required gates pass.
That final review is not Independent Review and cannot replace a required peer
review.

For Low-risk work only, the Root Master may own independent Validation when the
check is read-only, reproducible, within current capability, and requires no
production edit. The Master must inspect the exact artifact and evidence rather
than accept the implementer's report.

## Assurance Paths

Use only:

1. `Implementation -> Validation`
2. `Implementation -> Independent Review -> Validation`

Both end with Root Master final integrated review. Represent Review and
Validation with ordinary Evidence Gates using exactly `NOT RUN`, `PASS`, `FAIL`,
or `BLOCKED`. Only `PASS` permits dependent work.

## Risk Thresholds

| Risk | Default assurance path | Separation and exception |
|---|---|---|
| Low | `Implementation -> Validation` | Normally omit a reviewer. Validator differs from implementer; eligible Root Master Validation is allowed. Raise risk or add Review when discovery exposes semantic ambiguity, hidden consumers, weak acceptance evidence, or higher consequence. |
| Medium | `Implementation -> Independent Review -> Validation` | Reviewer and validator may be one independent peer only under the merge rule. Review may be waived only when every waiver condition is recorded. |
| High | `Implementation -> Independent Review -> Validation` | Reviewer and validator must be different peers. No waiver or merge. |
| Critical | `Implementation -> Independent Review -> Validation` | Reviewer and validator must be different peers. No waiver or merge; existing authority and recovery rules still govern live or destructive action. |

Unavailability, deadline, cost, apparent simplicity, or implementer confidence
never reduces risk or assurance requirements. A genuinely independent narrower
slice may be classified separately when its scope and consequence are actually
lower.

## Medium-Risk Review Waiver

Waive Independent Review only when all five conditions are recorded in the
plan with current evidence:

1. The authoritative behavior or contract is explicit and unchanged.
2. The change is internal and reversible or recoverable within current
   authority, with no public API, compatibility, security, permission,
   credential, schema, migration, data-integrity, concurrency, external-write,
   live, or destructive consequence.
3. Owned and affected consumers are discoverable and bounded.
4. Strong independent Validation can reproduce acceptance and detect credible
   failure modes.
5. Exact contract, consumer, and validation evidence is cited together with
   remaining uncertainty.

If any condition is missing, use the default assurance path. Implementer author
checks alone never justify the waiver.

## Medium-Risk Role Merge

One independent peer may Review and then Validate Medium-risk work only when:

- the peer had no implementation, remediation, or production-edit role;
- the assignment has one bounded domain and no High/Critical surface;
- the peer can perform both semantic challenge and reproducible checks;
- Review occurs first, then Validation, against an unchanged artifact;
- separate gate records state each role's question, evidence, check, and result;
- the plan explains why another peer would duplicate evidence rather than add
  an independent capability.

Never merge the roles for High or Critical risk, when repository or user rules
require separation, or when the roles need different expertise or environments.

## Revision And Remediation Rule

If a reviewer or validator edits a production file, that peer becomes an
implementer for the changed revision. Re-dispatch every affected Review and
Validation gate to other eligible peers.

When remediation changes a reviewed or validated artifact, rerun affected
downstream assurance gates against the new revision. Never inherit `PASS` from
an older artifact.

## Task-Splitting Anti-Patterns

Do not split:

- by file count, such as assigning source and tests to different implementers
  when one behavior owner should make and author-check the coherent change;
- by desired agent count, token budget, or a wish to show parallelism;
- into separate Medium-risk reviewer and validator assignments when both would
  repeat the same read-only evidence and the merge rule is fully satisfied;
- by starting Review against an unfinished mutable implementation;
- by letting an integrator change production artifacts after Review and reuse
  the old assurance gates;
- by assigning Review or Validation to the implementer;
- by relabeling the Root Master final review as peer Review.

Split by coherent responsibility, stable contract phase, specialist risk, or a
genuinely different evidence question. Tests normally remain with the
implementation owner for author feedback; independent acceptance Validation is
a separate assurance responsibility.

## Handoff Confidence

A Phase Handoff may include:

```markdown
## Confidence
- Level: high|medium|low
- Basis: <verified author evidence and exact remaining gaps>
```

Confidence is navigation metadata only. It is not evidence, assignment state,
an Evidence Gate, or permission for dependent work. It never replaces
Independent Review or Validation and does not belong in execution-state.
