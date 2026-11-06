# Trace Format

Use the repository's format when one exists. Otherwise this is an optional
starting point, not a set of mandatory headings:

```markdown
# <date> <decision>

trace_privacy_class: local_raw_trace

## Decision And Why

The problem, accepted behavior, important rejected alternative and rationale.
Include required/prohibited behavior and the user's clarified constraint.

## Evidence And Current State

Concrete source locations; current behavior versus the target; implementation
and commit status. Give the date or revision, scope and results of checks that
actually ran. Distinguish historical results, planned checks and blocked work.

## Continuation And Revisit

Affected files, remaining verification and what new evidence or changed
assumption would justify reopening the decision.
```

Combine sections for a narrow decision. Add detail only where omitting it would
hide an important boundary or uncertainty. When updating, identify what changed
and which earlier assumption or validation result no longer applies.

TraceGym is a separate opt-in format; ordinary records need neither its footer
nor an explanation of its absence.
