# Decision Trace Formats

Read this reference when choosing the trace's section structure or checking whether the result is actionable. Adapt headings to the repository language and convention.

## Expanded Trace

Use this structure for decisions affecting architecture, public behavior, integration contracts, high-risk correctness, data integrity, migrations, evaluation meaning, or cross-surface contracts.

```markdown
# <YYYY-MM-DD> <short decision title>

## Background

Describe the task, review suggestion, bug report, or implementation question that triggered the trace.

## Problem

State the concrete technical problem, failure chain, or ambiguity.

## Evidence And Source Analysis

Record:
- whether the issue came from a user report, review comment, architecture assessment, failing test, observed behavior, or code reading;
- exact files, functions, specifications, tests, or configs involved;
- which claims local evidence confirmed, weakened, disproved, or left uncertain.

## Clarified Constraints

List the user-facing or system behavior, architecture boundaries, repository rules, operational assumptions, testing principles, compatibility requirements, and migration boundaries that shaped the decision.

## User Follow-Up Signals

Summarize important user follow-ups and the design concern they expose, such as risk tolerance, public contract impact, recoverability, observability, simplicity, or the boundary between testability and production behavior.

## Decision Process

For each important alternative, state what it solves, its cost or complexity, any mismatch with constraints, and why it was accepted or rejected.

## Final Decision

State the engineering contract future agents must preserve:
- required behavior;
- prohibited behavior;
- invariants;
- conditions that justify revisiting the decision.

## Implementation Or Continuation Shape

Describe affected files, expected before/after behavior, tests or validation to run, and local documentation or specifications to update.

## Current Status

State whether the decision is unimplemented, implemented but uncommitted, committed, blocked, or awaiting follow-up. Include actual validation results and distinguish them from planned checks.

## Revisit Triggers

Record future evidence or conditions that would justify reopening the decision.

## Privacy Class

State `trace_privacy_class: local_raw_trace` for the normal repository-grounded trace. Use `sanitized_trace_seed` or `public_benchmark_candidate` only when this file is a separately authorized derived artifact that satisfies that layer's publication gate. Keep this section even when TraceGym metadata is omitted.

## TraceGym Data Capture

Add the metadata block only when the reusable-signal gate passes, and keep its privacy class consistent with the standalone Privacy Class section. Otherwise state `TraceGym metadata omitted: <reason>` without removing the standalone classification.
```

## Small Decision Mode

Use a compact trace when the decision is narrow, evidence is simple, impact is low, and fewer than ten bullets can capture it without hiding an important contract. Include only:

- problem;
- evidence;
- clarified constraint;
- final decision;
- validation;
- revisit trigger;
- explicit privacy class, normally `trace_privacy_class: local_raw_trace`;
- compact TraceGym metadata only when a reusable skill or eval signal exists.

Do not use compact mode for any high-impact surface listed under Expanded Trace.

## Actionability Review

Before finishing, ensure a future agent can answer:

- What exact problem was being solved?
- What did code, tests, configuration, or specifications prove?
- What did the user clarify?
- Why was the chosen solution preferred over the obvious alternative?
- What behavior must not be reintroduced?
- What validation defines success, and what actually ran?
- What remains unresolved?
- What evidence would justify revisiting the decision?
- When metadata is present, which workflow skill could learn from the trace and whether a deterministic eval is plausible?

Replace vague claims such as "improve reliability" with the concrete behavior boundary, invariant, validation mechanism, and forbidden regression.
