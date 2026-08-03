# Database Access Audit Triage And Reporting Guide

Read the triage sections for a time-bounded first pass. Read the report sections before delivering any final audit.

## Contents

- [Five-minute triage](#five-minute-triage)
- [Evidence collection checklist](#evidence-collection-checklist)
- [Candidate finding checklist](#candidate-finding-checklist)
- [Report structure](#report-structure)
- [Expanded finding template](#expanded-finding-template)
- [Recommended fix order](#recommended-fix-order)
- [Non-issues](#non-issues)
- [Open questions](#open-questions)
- [Compactness rules](#compactness-rules)
- [Tone and wording](#tone-and-wording)

## Five-Minute Triage

1. Confirm scope and read-only mode unless fixes were explicitly requested.
2. Identify stack facts from dependencies, config, schemas/migrations, persistence code, and tests.
3. Find session/unit-of-work providers, repositories/DAOs, execution wrappers, transaction helpers, and constraint/index definitions.
4. Trace one real caller-to-database path before broad keyword searches.
5. Scan that path for looped I/O, missing scope predicates, commit/flush in loops, unchecked rowcount, relation races, broad-write guards, and N+1 serialization/mapping.
6. Attempt to disprove candidates with bounds, no-op guards, deduplication, bulk APIs, constraints/indexes, required object semantics, and tests/logs.
7. Report only evidence-backed survivors and label unresolved stack behavior validation-needed.

This triage path is orientation, not authority for subtle ORM/runtime claims, high-impact findings, or final fix recommendations. Complete the core workflow and relevant catalog sections before those outputs.

## Evidence Collection Checklist

Inspect as relevant:

- dependency and lock files for ORM, query builder, driver, migration tool, and dialect;
- runtime config, environment samples, containers, deployment config, and test database setup;
- migrations, schemas, indexes, unique keys, foreign keys, constraints, and cascades;
- base repository/DAO/model manager, session, connection, unit-of-work, query, transaction, and retry helpers;
- target endpoints, handlers, jobs, commands, services, repositories, serializers, DTO mappers, and response builders;
- tests and fixtures that expose batch bounds, duplicate/missing/forbidden-ID behavior, transaction ownership, query count, generated SQL, rowcount, or side effects;
- existing SQL logs, traces, explain plans, benchmarks, slow-query notes, operational runbooks, and intentional-debt records.

## Candidate Finding Checklist

For every candidate, capture:

- concrete file, function, and tight line range;
- in-scope, shared-dependency, or out-of-scope-high-risk status;
- pattern and current inferred behavior;
- O(1), O(N), O(N*M), or unknown operation shape;
- code/config/migration/test/runtime/inferred evidence strength;
- safe-no-op, broad-write-risk, stack-dependent, unknown, or not-applicable empty-batch behavior;
- matched/changed/returned/unavailable/stack-dependent/unknown/not-applicable rowcount behavior;
- disproof attempted, counter-evidence inspected, invalidating conditions, and survival status;
- correctness, security, isolation, performance, operational, or maintainability risk;
- simplest safe recommendation and tradeoff;
- whether a single SQL statement is necessary: yes, no, or maybe;
- SQL log, query count, explain, benchmark, migration check, stack documentation, integration test, or no further validation;
- P0/P1/P2/P3 and high/medium/low confidence.

Optional scope, empty-batch, and rowcount fields may be omitted when clearly irrelevant. Include empty-batch and rowcount fields for batch update, delete, restore, purge, and archive findings.

## Report Structure

Use this structure unless the user requests another format:

```markdown
## Summary

- Audit scope:
- Mode: read-only / fixes allowed
- User-specified stack:
- Inferred stack:
- Evidence inspected:
- Information not confirmed:
- Overall conclusion:
- High-priority issue count:
- Out-of-scope but high-risk note:

## Findings

<compact table and expanded or grouped findings>

## Recommended Fix Order

<ordered recommendations>

## Non-Issues / Intentionally Not Flagged

<useful rejected candidates and retained behavior>

## Open Questions

<questions that materially affect priority, confidence, or recommendation>
```

For a small or first-pass scoped audit, start findings with:

```markdown
| Priority | Location | Pattern | Evidence strength | Validation needed |
| --- | --- | --- | --- | --- |
| P0/P1/P2/P3 | file:function | operation shape | code/config/migration/test/runtime/inferred | concrete check / none |
```

## Expanded Finding Template

```markdown
### Finding N - Title

- Priority: P0 / P1 / P2 / P3
- Location: file, function, line range
- Scope status: in-scope / shared dependency / out-of-scope high-risk note
- Pattern:
- Current inferred behavior: looped database round trips / object-level unit-of-work / parameterized bulk execution / set-based operation / possible lazy-load N+1 / unknown
- Estimated operation shape: O(1) / O(N) / O(N*M) / unknown
- Evidence strength: code path confirmed / config confirmed / migration confirmed / test confirmed / runtime confirmed / inferred only
- Empty batch behavior: safe no-op / broad write risk / stack-dependent / not applicable / unknown
- Rowcount semantics: matched rows / changed rows / returned rows / unavailable / stack-dependent / unknown / not applicable
- Evidence:
- Disproof attempted:
- Counter-evidence checked:
- Could be invalid if:
- Survival status: survived / downgraded / rejected
- Risk:
- Recommendation:
- Tradeoff:
- Whether single SQL is necessary: yes / no / maybe
- Validation needed: SQL log / query count test / explain / benchmark / migration check / stack documentation / none
- Confidence: high / medium / low
```

Every expanded finding must make location, scope, access pattern, operation shape, evidence strength, disproof, counter-evidence, survival, runtime certainty, risk, recommendation, maintainability tradeoff, single-SQL necessity, and validation path clear.

## Recommended Fix Order

1. Correctness, security, isolation, and data-integrity risks.
2. Simple set-based improvements for same-value writes and deletes.
3. Relation uniqueness/upsert, soft restoration, and concurrency protection.
4. Different-value batch updates where stack bulk APIs may suffice.
5. Query-count/SQL-log/explain/benchmark observability and batch-size limits.

## Non-Issues

Retain useful rejected candidates when evidence shows bounded or low-frequency work, required object semantics, likely parameterized bulk behavior with validation noted, an over-engineered single-statement alternative, in-memory loop construction followed by one bulk operation, an explicit empty-input no-op, or parameterized/scoped/tested/justified raw SQL.

## Open Questions

Ask only questions that materially affect the audit, such as:

- What is the maximum batch size and is it user-controlled?
- Is the path public, internal, admin-only, job-only, migration-only, or hot?
- Is the operation all-or-nothing, partial-success, retryable, or idempotent?
- How must missing, forbidden, duplicate, already-deleted, and invalid-state IDs behave?
- Which hooks, events, cascades, validators, setters, defaults, triggers, identity-map behavior, caches, indexes, counters, notifications, webhooks, or sync processes are required?
- Are SQL logs, query-count tests, explain plans, benchmarks, slow-query data, or controlled integration environments available?
- What database and driver versions, dialect constraints, parameter limits, and transaction rules apply?

## Compactness Rules

- Expand P0 and P1 findings by default.
- Group P2 and P3 into concise bullets with a counter-evidence phrase unless the user asks for all details.
- Use the full finding template for requests such as full audit, exhaustive, or all findings.
- Group repeated patterns while preserving representative locations.
- Show highest-risk findings first and move lower-risk work under additional findings or follow-up candidates.
- State sampling boundaries; never imply exhaustive coverage from a sample.
- Keep enough evidence to verify every grouped finding without producing a report so large that it hides action.

## Tone And Wording

- Be precise and do not exaggerate.
- Do not call a loop defective without database I/O evidence.
- Do not claim per-object statements, flush batching, driver batching, lazy loading, or multiple connections without proof.
- Distinguish connection, transaction, statement, round trip, row mutation, object mutation, flush, and commit.
- Mark uncertainty and name the needed validation.
- Recommend the simplest safe direction and explain correctness before performance.
- Preserve maintainability when performance evidence is weak.
- Do not claim empty-list behavior or rowcount semantics without stack evidence.
- Judge raw SQL by binding, identifiers, scope, semantics, tests, and maintainability, not by its existence.
- Keep the audit focused on database access risks rather than expanding into a general security review.

End by stating that no business code was modified unless fixes were explicitly authorized and actually made.
