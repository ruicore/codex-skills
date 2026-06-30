# Database Access Audit Quick Reference

Use this for a first-pass database access triage when time is tight. It does not replace the full `SKILL.md` workflow. Escalate to the full workflow before making high-confidence claims, reporting subtle ORM behavior, or recommending code changes.

## 5-Minute Triage Path

1. Confirm scope and mode: repository area, endpoint/job/service, and read-only unless fixes were explicitly requested.
2. Identify the stack from local evidence: dependency files, config, migrations/schema, repository layer, and tests.
3. Find the database access primitives: session/unit-of-work providers, repository/DAO helpers, query execution wrappers, transaction helpers, and migration/index locations.
4. Trace one real path from caller to database operation before using broad keyword searches.
5. Scan for the highest-risk operation shapes: looped database I/O, missing scope predicates, commit/flush inside loops, unchecked rowcount, relation attach/detach races, and N+1 serialization or mapper paths.
6. Run a quick disproof pass: look for bounds, early returns, deduplication, existing constraints/indexes, bulk APIs, object-level semantics, and tests/logs that invalidate the candidate.
7. Output only evidence-backed findings. Mark unresolved ORM/driver behavior as validation-needed instead of confirmed.

## First Files/Evidence To Inspect

- Dependency and lock files for ORM, query builder, driver, migration tool, and database dialect.
- Runtime config, env samples, container files, and test database setup.
- Migration/schema/index/constraint definitions.
- Base repository, DAO, model manager, session, connection, or unit-of-work helpers.
- Target endpoints, jobs, commands, services, repositories, serializers, DTO mappers, and response builders.
- Tests and fixtures that show batch limits, duplicate-ID behavior, missing-ID behavior, transaction boundaries, query logging, or query-count assertions.
- Existing SQL logs, traces, explain plans, benchmarks, slow-query notes, or operational runbooks when available.

## Common High-Risk Patterns

- Database calls, repository calls, lazy relationship access, flush, or commit inside item loops.
- User-controlled or unbounded batch inputs without maximum size, chunking, or operational guardrails.
- Batch update/delete/restore/archive/purge without tenant, project, organization, owner, user, soft-delete, or status scope when those scopes exist.
- Same-value batch writes implemented as per-object mutations without a confirmed semantic need.
- Check-then-insert relation attach logic without a database-backed uniqueness or conflict strategy.
- Relation detach/attach paths that ignore duplicate payload IDs, soft-deleted relation restoration, or concurrent requests.
- Missing affected-row, returned-row, missing-ID, forbidden-ID, duplicate-ID, or partial-success handling where all-or-nothing semantics are expected.
- Hard delete or bulk DML that may bypass cascades, hooks, events, audit logs, outbox events, cache invalidation, search indexing, counters, notifications, webhooks, permission caches, or lifecycle behavior.
- List responses, serializers, mappers, templates, or computed properties that may trigger N+1 reads.
- Optional-filter or empty-input paths that could remove restrictive predicates.
- Concurrent tasks sharing a session, connection, transaction, or unit-of-work object without stack support.
- Raw SQL or dynamic query construction without clear parameter binding, identifier allowlists, scope preservation, and tests.

## What Not To Assume About ORM/Driver Behavior

- Do not assume object-level mutation means one SQL statement, one round trip, one transaction, or one connection per object.
- Do not assume a unit-of-work flush batches work unless local configuration, versioned docs, tests, SQL logs, or runtime evidence confirms it.
- Do not assume a bulk update/delete is safer; it may bypass hooks, validators, cascades, identity-map synchronization, domain events, defaults, triggers, or side effects.
- Do not assume relation access is lazy or eager without checking mapping configuration, query options, serializer behavior, or SQL logs.
- Do not assume `rowcount` means changed rows, matched rows, or reliable rows across drivers without validating the current stack.
- Do not assume empty `IN` or empty-list behavior is safe or unsafe without checking generated SQL, guards, or stack documentation.
- Do not assume raw SQL is unsafe merely because it is raw; judge parameter binding, scope, tests, and maintainability.
- Do not equate connection, transaction, statement, round trip, row mutation, flush, commit, and object mutation.

## When Runtime Validation Is Required

Runtime validation is required before a confident claim when static evidence cannot prove:

- Query count, N+1 behavior, lazy-load behavior, flush batching, driver batching, or round-trip count.
- ORM/unit-of-work behavior for object-level mutation, cascades, hooks, events, validators, identity-map synchronization, defaults, or triggers.
- Generated SQL for empty inputs, optional filters, `IN` clauses, bulk APIs, upserts, or dynamic predicates.
- Rowcount, returned-row, changed-row, or matched-row semantics for the current driver/database.
- Index usage, lock scope, query plan, timeout risk, parameter limits, or batch-size performance.
- Concurrency behavior for check-then-insert, state transitions, relation attach/detach, shared sessions/connections, or retries.

Keep validation safe: use local tests, test databases, SQL logs, query-count checks, explain plans, existing traces, or dry-run mechanisms. Do not connect to production databases, run migrations, mutate data, benchmark broadly, or run load tests without explicit authorization.

## Minimal Output Skeleton

```markdown
### Summary

- Audit scope:
- Mode: read-only / fixes allowed
- Inferred stack:
- Evidence inspected:
- Information not confirmed:
- Overall conclusion:

### Findings

| Priority | Location | Pattern | Evidence strength | Validation needed |
| --- | --- | --- | --- | --- |
| P0/P1/P2/P3 | file:function | looped DB I/O / scope / rowcount / relation / N+1 / transaction / index | code/config/migration/runtime/inferred | SQL log / query count / explain / stack docs / none |

### Finding 1 - Title

- Priority:
- Location:
- Current inferred behavior:
- Evidence:
- Disproof attempted:
- Counter-evidence checked:
- Risk:
- Recommendation:
- Validation needed:
- Confidence:

### Non-Issues / Intentionally Not Flagged

- Reviewed but not flagged because:

### Open Questions

- Question:
```

## Escalation Path To Full Workflow

Escalate from this quick reference to the full `SKILL.md` workflow when:

- The audit scope is broad, user-facing, security-sensitive, or cross-module.
- Any finding could be P0 or high-impact P1.
- The recommendation would change transaction boundaries, bulk operation shape, relation semantics, side effects, constraints, indexes, or API response semantics.
- ORM, driver, database, migration, or runtime behavior is uncertain.
- The code path relies on hooks, events, cascades, validators, identity maps, defaults, triggers, domain events, cache invalidation, audit logs, outbox records, counters, notifications, webhooks, or downstream sync.
- The output needs the full report template, priority model, disproof pass, recommended fix order, non-issues, and open questions.

Use the full workflow for final audit reports. Use this quick reference to get oriented quickly and to avoid the most common false positives.
