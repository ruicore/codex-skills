---
name: database-access-audit
description: Read-only database access audit for batch operations, looped DB I/O, bulk writes, relation attach/detach, N+1, transactions, scope isolation, rowcount, concurrency, constraints, and indexes across any stack.
---

# Database Access Audit

For fast first-pass triage, use the [Database Access Audit Quick Reference](quick-reference.md). The quick reference is only an entry point; use this full workflow for final audit reports, high-confidence findings, runtime-behavior claims, and any fix recommendations.

## 1. Skill Name And Purpose

Use this skill to audit database access patterns in a repository without assuming a specific language, framework, ORM, database driver, migration tool, or database engine.

Core goals:

- Find inefficient database access in batch interfaces.
- Find uncontrolled looped database I/O and O(N) database interaction.
- Find unsafe or inefficient batch update, batch delete, bulk insert, and upsert implementations.
- Find relation-table attach/detach risks.
- Find N+1 reads, including implicit lazy-load I/O.
- Find missing tenant, project, organization, owner, user, soft-delete, or status scope.
- Find missing rowcount, returned-row, missing-ID, and duplicate-ID handling.
- Find transaction-boundary, atomicity, rollback, and partial-success problems.
- Find concurrency races around check-then-insert, state transitions, and shared sessions or connections.
- Find constraint, index, unique-key, foreign-key, and upsert risks.
- Balance performance, correctness, operational safety, and maintainability.

Default mode is read-only audit. Do not modify business code, stage files, commit, or push unless the user explicitly asks for fixes or publication. If the user asks to "check", "audit", "review", "find", "evaluate", "inspect", or "assess", treat the task as read-only even when obvious fixes are found. Do not modify business code unless the user explicitly asks to fix, patch, edit, refactor, or implement.

## 2. When To Use This Skill

Use this skill when the user asks to:

- Check batch operations.
- Audit database access.
- Check whether code updates, deletes, inserts, or validates one item at a time.
- Check N+1 query risk.
- Perform a read-only review without code changes.
- Review a specific service, repository, module, endpoint, job, or domain.
- Audit batch update, batch delete, bulk insert, bulk upsert, attach, detach, restore, or purge behavior.
- Check whether ORM, query builder, or driver usage is reasonable.
- Check database performance hazards.
- Check tenant isolation, project isolation, organization isolation, authorization scope, or bulk operation safety.

If the user also asks for architecture, Python backend fundamentals, security, or agent-legibility review, keep this skill focused on database access behavior and explicitly separate those other scopes.

## 3. Inputs To Collect Or Infer

Establish these inputs before findings. Infer them from repository evidence when the user does not provide them.

- Audit scope: whole repository, service, domain, repository layer, endpoint, job, migration, model, schema, or test area.
- Execution mode: read-only by default; code changes only if explicitly allowed.
- User-specified technology stack: ORM, database, driver, framework, runtime, migration tool, or deployment target.
- Batch-size bounds: documented maximum, validation limit, paging limit, API limit, job chunk size, or unbounded/user-controlled input.
- Call frequency and exposure: public API, hot path, internal API, admin-only path, job-only path, migration-only path, or test-only path.
- Atomicity requirement: all-or-nothing, best-effort, partial success, retryable batch, idempotent job, or unknown.
- Response semantics: whether missing IDs, forbidden IDs, invalid-state IDs, duplicate IDs, already-deleted rows, or failed rows must be reported.
- Scope model: tenant, project, organization, account, owner, user, role, permission, soft-delete, status, or other access boundary.
- Data lifecycle: soft delete, restore, tombstone, archive, purge, recycle, state machine, versioning, optimistic locking, or audit trail.
- Object semantics: reliance on ORM/unit-of-work events, hooks, validators, computed setters, cascades, defaults, triggers, identity map synchronization, or domain events.
- Observability: available SQL logs, query-count tests, explain plans, benchmarks, metrics, tracing, slow-query logs, or migration/index checks.

When an input cannot be confirmed, record it under "Unknown" and reflect the uncertainty in priority and confidence.

## 4. Scope Control

Use the user's requested scope to control findings.

- If the user specifies a service, module, directory, domain, repository, endpoint, or job, report findings in that scope by default.
- Inspect shared database infrastructure, base repositories, common persistence helpers, models, migrations, tests, and config when needed to understand the stack and conventions.
- Do not report out-of-scope code as a main finding unless it directly affects the requested scope.
- If out-of-scope files were inspected to understand in-scope behavior, list them in Summary under "Evidence inspected".
- If a severe out-of-scope P0 risk is discovered, report it separately under "Out-of-scope but high-risk note" instead of mixing it into main findings.
- If the user requests a whole-repository audit, do not limit findings by scope.

## 5. Technology Stack Inference

Infer the stack from repository-local evidence before judging behavior. If the user explicitly specifies the stack, treat that as the starting point, but still verify it against repository files. Do not silently replace the user's stack with a guess.

Inspect evidence such as:

- Dependency manifests, lock files, package manifests, build configs, runtime images, and task runners.
- Runtime config, env samples, settings modules, container/compose config, deployment config, and CI config.
- Migration directories, generated schema files, migration metadata, and schema snapshots.
- Repository, service, model, entity, schema, query, DAO, gateway, adapter, and persistence code.
- Tests, fixtures, integration test setup, database test harnesses, and query logging configuration.
- Documentation, runbooks, ADRs, comments near persistence code, and local conventions.

Identify:

- Programming language and execution model.
- ORM, unit-of-work layer, query builder, database client, and raw driver usage.
- Database engine, dialect, server version constraints, and driver/version constraints when discoverable.
- Migration tool and whether constraints/indexes are defined in migrations, models, schema files, or external config.
- Transaction management pattern and authoritative transaction boundary.
- Repository/service layering and which layer owns commit/rollback.
- Model/schema definitions, relation tables, soft-delete conventions, and status conventions.
- Tenant, project, organization, account, owner, user, and permission-scope conventions.
- Primary key, unique key, foreign key, index, partial/filtered uniqueness, and cascade conventions.
- Async/sync execution model and whether sessions, connections, or transactions are safe to share across concurrent tasks.
- Test setup and whether SQL logging, query count assertions, explain plans, or integration tests are available.

Rules:

- Do not use any specific ORM, driver, database, migration tool, language, or web framework as a default premise.
- Use abstract terms such as ORM, query builder, database driver, migration tool, unit of work, identity map, set-based DML, bulk operation, upsert, transaction, statement, and round trip.
- Do not assume how an ORM optimizes object mutation, flush, batching, or lazy loading. Verify through local configuration, versioned documentation, SQL logs, tests, or direct runtime evidence.
- If behavior cannot be confirmed, say "uncertain, needs validation" and name the validation needed.

## 6. Project-Specific Database Access Primitive Discovery

Before broad repository searches, identify the project's actual database access primitives. Use these project-local APIs to search precisely, then use generic terms for recall.

Find:

- Database, session, connection, context, or unit-of-work providers.
- Repository, DAO, gateway, persistence adapter, model manager, or base persistence classes.
- Query execution helpers, command helpers, statement builders, and raw driver wrappers.
- Transaction helpers, retry helpers, locking helpers, and commit/rollback conventions.
- Model, schema, relation, mapping, and persistence adapter locations.
- Migration, schema, index, constraint, and seed-data locations.
- Test database harnesses, fixtures, factories, integration setup, and query logging hooks.
- Soft-delete, status, lifecycle, scope, tenant, project, organization, owner, and permission conventions.
- Project-specific helper names such as require, get, list, save, delete, update, attach, detach, restore, archive, purge, execute, query, flush, commit, rollback, sync, and publish when they wrap database behavior.

After identifying these primitives:

- Search for call sites using project-specific API names before generic keywords.
- Trace from public endpoints, jobs, commands, handlers, services, or repositories into these primitives.
- Distinguish wrappers that only build in-memory objects from wrappers that execute database I/O.
- Record unconfirmed primitives in the Summary under "Information not confirmed".
- If database access primitives cannot be identified, state that clearly and lower confidence for findings based only on naming or inference.

## 7. Evidence Hierarchy

When evidence conflicts, prefer sources in this order:

1. Actual code paths and call relationships.
2. Dependency manifests, runtime config, lock files, build config, and deployment config.
3. Migrations, schema definitions, index definitions, and constraint definitions.
4. Tests, fixtures, factories, and integration setup.
5. SQL logs, query-count tests, explain plans, benchmarks, traces, and metrics when available.
6. Documentation, README, ADRs, runbooks, and comments.
7. Naming conventions and inference.

Rules:

- Do not make a high-confidence finding from function names or comments alone.
- Do not assert that an ORM, query builder, driver, or database client definitely flushes, batches, executes, or lazy-loads in a particular way without runtime evidence, versioned documentation, tests, or repository configuration.
- If runtime behavior is unverified, describe it as "inferred", "possible", or "unknown", and name the validation needed.
- Finding confidence must reflect evidence strength. Code-path confirmation is stronger than naming inference; runtime confirmation is stronger than static assumptions about batching or lazy loading.

## 8. Core Audit Principles

- Do not treat every `for` loop as a defect. The defect is database I/O in the loop body, implicit lazy-load I/O, or another pattern that creates uncontrolled O(N) database interaction.
- Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.
- Prefer single set-based database operations for same-value batch update, soft delete, hard delete, status transition, detach, restore, or archive when object-level semantics are not required.
- For per-row different values, do not automatically force complex single-statement techniques. First evaluate batch size, call frequency, code complexity, database portability, and measured performance.
- For per-row different values, framework-provided bulk APIs, bulk mappings, parameterized bulk execution, or driver-level multi-parameter execution may be sufficient and more maintainable than dialect-specific SQL.
- Object-level ORM mutation does not necessarily mean one immediate statement per object, one connection per object, or one round trip per object. Judge based on actual unit-of-work, flush, batching, driver, and database behavior.
- Bulk update/delete may bypass unit-of-work behavior, hooks, events, cascades, validators, identity-map synchronization, computed setters, or domain invariants. Evaluate correctness before recommending a bulk rewrite.
- Bulk rewrite may bypass or fail to trigger side effects outside the immediate database row mutation, such as audit logs, outbox/domain events, cache invalidation, search-index updates, denormalized counters, notifications, webhooks, permission caches, lifecycle hooks, and downstream sync jobs. Check these before recommending bulk update/delete/insert.
- Batch writes must include tenant, project, organization, owner, user, soft-delete, and status scope in the database operation when those scopes apply.
- If business semantics require all-or-nothing, verify affected row count, returned rows, missing IDs, and duplicate IDs against the deduplicated expected set.
- Relation attach/detach must account for unique constraints, upsert/conflict behavior, concurrent duplicate inserts, duplicate payload IDs, and soft-deleted relation restoration.
- Async or concurrent code must not unsafely share sessions, connections, or transactions across concurrent tasks unless the current stack explicitly supports it.
- Large batches must consider parameter limits, lock scope, index support, chunking, timeout, retry, deadlock, rollback cost, and operational scheduling.
- Recommendations must balance performance with maintainability. Do not propose complex single-statement SQL only because it is "one SQL" when a simpler bulk operation is adequate.

## 9. Required Behavior Distinctions

Use precise language in findings:

- Looped database I/O: each iteration triggers a database round trip, statement execution, lazy load, flush, commit, repository call, or driver call.
- Object-level unit-of-work mutation: code loads objects, mutates them, and relies on a unit of work, flush, save, or commit. This may or may not become one statement per object.
- Parameterized bulk execution: a driver, ORM, or query builder executes the same operation with many parameter sets, often described as bulk mappings, batch execute, multi-parameter execution, or executemany-like behavior.
- Set-based single-statement operation: one database statement targets many rows through a predicate, join, subquery, common source set, or equivalent database-side set operation.
- Upsert/conflict handling: insert-or-update/ignore/merge behavior protected by a database constraint or equivalent conflict mechanism.
- Lazy-load or implicit I/O: reading an association, computed property, serializer field, proxy, deferred field, or collection triggers database access outside the obvious query site.
- Transaction: the atomic database boundary. Do not confuse it with a connection, statement, session object, request, or repository method.
- Connection: a database communication resource. Do not claim "many connections" unless the code or runtime evidence shows connection acquisition per operation.
- Round trip: a client-to-database interaction. Do not equate row-level object mutation with round trips unless verified.
- Statement: a database operation sent for execution. Do not equate statements, rows, transactions, connections, and round trips.

## 10. Patterns To Search For

Start with the project-specific primitives discovered above. Search for their call sites and trace actual execution paths. Then use stack-neutral terms to improve recall. Useful generic search terms include `batch`, `bulk`, `many`, `list`, `ids`, `update`, `delete`, `insert`, `upsert`, `save`, `add`, `attach`, `detach`, `restore`, `purge`, `archive`, `tombstone`, `member`, `role`, `permission`, `tag`, `link`, `join`, `relation`, `transaction`, `commit`, `rollback`, `flush`, `lock`, `version`, `tenant`, `project`, `organization`, `owner`, `scope`, `deleted`, `status`, `count`, and `returning`.

### 10.1 Looped Database I/O

Search for:

- Awaited or synchronous database calls inside loop bodies.
- Repository get/update/delete/save calls inside loops.
- Query execution inside loops.
- Flush or commit inside loops.
- Delete, insert, save, add, attach, detach, or relation writes inside loops.
- Nested loops that construct and persist relation rows.
- Per-item existence checks.
- Per-item permission checks.
- Per-item association lookups.

Judge:

- If every iteration triggers a database round trip, the finding is usually P1, or P0 when it creates correctness, security, or atomicity risk.
- If batch size is unbounded or user-controlled, priority increases.
- If commit occurs inside the loop, treat it as severe because it can cause partial success, lost atomicity, longer connection use, and difficult error recovery.
- If the loop only constructs in-memory data and a bulk operation occurs after the loop, do not flag it as looped database I/O.

### 10.2 Object-Level Batch Mutation

Search for:

- Querying a batch of objects, looping over them, mutating fields, and relying on flush/save/commit.
- Loading full entities only to update a uniform field.
- Calling object methods, validators, hooks, or setters before commit.

Judge:

- If all rows receive the same value, recommend considering set-based update unless object-level semantics are required.
- If each row receives a different value, consider bulk APIs or keeping unit-of-work mutation before recommending complex single-statement SQL.
- Check whether full object loading is needed for business logic, validation, events, cascades, or identity-map behavior.
- Verify whether the current stack batches flushes or emits one statement per row before making performance claims.

### 10.3 Batch Delete And Soft Delete

Search for:

- Per-row hard delete in a loop.
- Per-row assignment of deleted flags, deleted timestamps, status fields, tombstones, archive markers, recycle markers, or restore markers.
- Batch purge, archive, recycle, restore, status transition, or state-machine transitions.

Judge:

- Prefer set-based update for same-value soft delete, restore, tombstone, archive, or status transition when object-level semantics are not required.
- For hard delete, check foreign keys, cascades, triggers, retention policy, audit requirements, and business invariants.
- For soft delete, check tenant/project/org scope, rowcount, current status, deleted-state condition, indexes, uniqueness semantics, and restore behavior.
- For status transitions, prefer including expected current status to avoid concurrent overwrite or invalid state transition.

### 10.4 Batch Insert And Relation Attach

Search for:

- Per-row insert/save/add in loops.
- Nested loops generating many-to-many, membership, link, tag, role, permission, or association rows.
- Patterns that query existing rows and then insert missing rows.
- Soft-deleted relation restore logic.
- Attach/detach operations for tags, roles, permissions, memberships, groups, links, projects, organizations, accounts, or owners.

Judge:

- Check for a database-backed unique constraint protecting relation uniqueness.
- Check for check-then-insert races when concurrent requests can insert the same relation.
- Check whether bulk insert, conflict handling, upsert, or restore-on-conflict is appropriate.
- Check whether soft-deleted relation rows should be restored instead of inserting duplicates.
- Check whether duplicate payload IDs are deduplicated before write.
- Check whether response semantics clearly express all-or-nothing or partial success.

### 10.5 N+1 Read Queries And Implicit Lazy Loading

Search for:

- Relationship, association, deferred field, computed property, or proxy access inside loops.
- Serializers, response builders, template renderers, DTO mappers, or view models that access unpreloaded associations.
- Service-layer loops that access model relationships after querying a list.
- Async code where property access may trigger implicit database I/O.
- List endpoints that query parent rows then query child rows one parent at a time.

Judge:

- Consider eager loading, prefetching, join-based reads, batched child queries, or grouping associated rows in memory.
- Avoid moving implicit queries into serialization layers where they are hard to count or test.
- Prefer a query-count test, SQL log, or integration test to confirm N+1 risk.
- If lazy-loading behavior is stack-dependent and unverified, mark the finding as possible N+1 with validation needed.

### 10.6 Unnecessary Object Loading

Search for:

- Loading full entities before update/delete when only IDs, rowcount, or scope checks are needed.
- Loading full rows to validate existence.
- Loading unnecessary fields for permission checks.
- Query results used only for IDs or counts.
- "Require objects" helpers called before a bulk operation.

Judge:

- Push tenant, project, organization, owner, soft-delete, and status conditions into the update/delete predicate when safe.
- Query only IDs or minimal fields when existence or authorization evidence is enough.
- Use affected row count, returned rows, or equivalent result metadata to detect missing or forbidden rows when the stack supports it.
- Keep object loading when object-level semantics, rich validation, or domain behavior genuinely requires it.

### 10.7 Tenant, Project, Organization, And Scope Isolation

Search batch select/update/delete operations for:

- Tenant scope.
- Project scope.
- Organization/account scope.
- Owner/user scope.
- Role or permission scope.
- Soft-delete conditions.
- Status/current-state conditions.

Judge:

- Batch writes must not rely only on payload IDs when scope applies.
- If a pre-check verifies scope and a later write uses only IDs, check the race window and whether the scope is also in the write predicate.
- User-provided IDs should be scoped in the database operation, not only in application memory.
- All-or-nothing behavior requires comparing affected rows or returned rows to the deduplicated expected set.

### 10.8 Rowcount And Partial Success

Search for:

- Batch update/delete after which affected rows or returned rows are not checked.
- Batch requests that do not handle missing IDs.
- Duplicate IDs in payloads that are not deduplicated or reported.
- Ambiguous partial-success behavior.
- Responses that omit failed IDs, updated IDs, deleted IDs, skipped IDs, or missing IDs where callers need them.
- All-or-nothing semantics that are not enforced.

Judge:

- Deduplicate request IDs before comparing expected and affected counts.
- Compare affected rows, returned rows, or equivalent result metadata to expected rows when all-or-nothing is required.
- Distinguish not found, forbidden, already deleted, invalid state, and duplicate input when business semantics require it.
- If partial success is allowed, ensure response and documentation make that clear.
- Do not assume rowcount always means "changed rows".
- Some stacks report matched rows, affected rows, changed rows, returned rows, or unknown rowcount differently.
- For idempotent updates, "already in target state" may complicate rowcount interpretation.
- If correctness depends on rowcount, verify current stack semantics through documentation, tests, SQL logs, returned rows, or controlled integration tests.
- When rowcount is unreliable or unavailable, recommend returned IDs/rows or another safe alternative.

### 10.9 Transactions

Search for:

- Repository-layer commits when service-layer transactions also exist.
- Mixed transaction ownership between handlers, services, repositories, jobs, and helpers.
- Flush or commit inside loops.
- Long transactions that include external API calls, file I/O, network I/O, slow computation, or user callbacks.
- Concurrent tasks sharing a session, connection, transaction, or unit-of-work object.
- Error paths without rollback, cleanup, or idempotent retry behavior.
- Batch operations whose atomicity is unclear.

Judge:

- One business operation should have a clear transaction boundary.
- Commit inside a loop is usually severe.
- Long transactions increase lock duration, deadlock risk, rollback cost, and operational fragility.
- Verify whether the current stack permits concurrent use of the same session, connection, transaction, or unit-of-work object.

### 10.10 Concurrency, Constraints, And Indexes

Search for:

- Check-then-insert without database uniqueness or conflict handling.
- State transitions without expected current state, version, timestamp, or optimistic-lock condition.
- Relation tables without unique keys.
- Soft delete plus uniqueness semantics that are undefined or mismatched with restore behavior.
- Batch predicates without supporting indexes.
- Large `IN` lists or equivalent multi-ID predicates.
- Bulk operations without chunking or parameter-limit handling.
- Purge/delete operations that may hold locks for a long time.

Judge:

- Use database constraints to protect uniqueness and data integrity where possible.
- Use conflict handling or upsert-like behavior when concurrent creation is expected.
- Include expected state or version conditions to avoid lost updates.
- Verify indexes support high-volume batch predicates.
- For large operations, consider chunking, timeout, background job execution, retry strategy, deadlock handling, and operational scheduling.

### 10.11 Side Effects And Derived State

Search for:

- Audit log, event, domain-event, or outbox publishing around persistence operations.
- Cache invalidation, materialized cache refresh, permission cache refresh, or authorization cache invalidation.
- Search index synchronization or document indexing.
- Denormalized counters, statistics, aggregates, rollups, or materialized derived state.
- Lifecycle hooks, validators, callbacks, computed setters, defaults, triggers, or domain services.
- Notifications, webhooks, emails, messages, queue publishes, or downstream sync jobs.
- Background jobs that reconcile, sync, backfill, or repair data after writes.

Judge:

- If object-level writes trigger these side effects, bulk DML cannot directly replace them unless an equivalent side-effect mechanism exists.
- If the current batch operation should trigger side effects but does not, evaluate it as a correctness risk, not only a performance issue.
- Recommendation must state how audit logs, events, caches, search indexes, counters, notifications, webhooks, permission caches, lifecycle hooks, and downstream sync jobs stay consistent.
- If side-effect behavior is unclear, mark it as "uncertain, needs validation" rather than assuming the object-level path and bulk path are equivalent.

### 10.12 Empty Batch, Missing Predicate, And Broad Write Guards

Search for:

- Empty batch IDs, filters, selectors, or criteria.
- Conditionally appended WHERE, filter, scope, or predicate clauses.
- Update, delete, archive, purge, restore, or status operations that may become broad writes when filters are empty.
- Batch operations without a restrictive predicate.
- User-controlled filters that must enter database conditions.
- Empty input handling such as early return or explicit no-op.
- Duplicate ID deduplication.
- Maximum batch-size validation.
- Generated predicates that broaden when optional filters are absent.

Judge:

- Bulk update/delete/purge/restore/archive without a restrictive predicate is P0 unless proven safe.
- Empty batch should normally be no-op, not broad update/delete.
- If empty `IN`/list predicate behavior is stack-dependent, mark it uncertain and require validation.
- Do not assume empty list behavior is safe across frameworks, drivers, query builders, or databases.
- For all-or-nothing operations, compare expected count after deduplication.

### 10.13 Raw SQL And Dynamic Query Safety

Search for:

- Raw SQL strings.
- String interpolation, concatenation, formatting, or templating used to build SQL.
- Dynamic table names, column names, order-by fields, filter names, operators, or JSON paths.
- User-provided IDs, filters, search terms, sort fields, pagination params, or JSON fields inserted into queries.
- Raw SQL paths that bypass repository scope helpers or shared persistence guards.

Judge:

- User values should be parameter-bound, not string-concatenated.
- Dynamic identifiers should use allowlists or safe framework APIs.
- Raw SQL must preserve tenant, project, organization, user, soft-delete, authorization, rowcount, and partial-success semantics.
- If raw SQL is used for bulk optimization, verify tests and clear maintainability justification.
- SQL injection or cross-scope raw query risk is P0.
- Do not flag raw SQL merely because it is raw SQL; judge parameterization, scope, semantics, tests, and maintainability.

## 11. Severity Classification

Use priority to communicate risk and urgency, not personal preference.

### P0 - Must Fix

Use for correctness, security, data-corruption, cross-tenant, or severe atomicity risk:

- Batch write lacks tenant, project, organization, owner, or authorization scope.
- Code can modify or delete data across tenants or scopes.
- Check-then-insert lacks database uniqueness and can create duplicate data under concurrency.
- Commit inside a loop causes partial success when business semantics require atomicity.
- Batch update/delete does not verify rowcount or returned rows when all-or-nothing is required.
- Concurrent tasks unsafely share a session, connection, transaction, or unit-of-work object.
- Hard delete can break foreign keys, cascade expectations, retention rules, or business invariants.
- Bulk update/delete/purge/archive/restore can execute without a restrictive predicate because of empty filters or conditional predicate construction.
- Raw SQL or dynamic query construction allows user-controlled SQL injection or cross-scope access.

### P1 - Should Fix

Use for clear scalability, performance, or operational risk:

- Loop performs one query or write per item.
- Same-value batch update mutates objects one by one without a semantic reason when batch size is meaningful, unbounded, user-controlled, hot-path, or confirmed to cause O(N) database interaction.
- Batch soft delete updates one object at a time for meaningful or unbounded batches without requiring object-level semantics.
- Relation attach/detach writes one row at a time when batch size is meaningful.
- List endpoint has confirmed or highly likely N+1 behavior.
- Update/delete loads many full objects unnecessarily.
- Batch predicate lacks index support for expected scale.
- Missing batch-size limit for a user-controlled high-volume batch operation.

### P2 - Conditional

Use when the right choice depends on size, frequency, stack behavior, or maintainability:

- Per-row different-value batch update.
- Small, bounded, low-frequency, admin-only operation.
- Object-level update depends on unit-of-work, validation, event, hook, cascade, computed setter, identity map, or domain behavior.
- Current framework or driver may already provide bulk optimization.
- Replacing clear object-level code with a single statement would reduce readability or strongly couple code to a dialect without proven need.
- Rowcount semantics are unclear but only affect low-risk or idempotent behavior.

### P3 - Observability, Tests, And Hardening

Use for supporting improvements:

- Missing query-count test.
- Missing SQL logging for the audited path.
- Missing explain plan or index verification.
- Missing documented batch-size assumption for a low-risk or internal path.
- Missing slow-query monitoring or tracing.
- Missing benchmark or load test for high-volume paths.
- Missing test for empty batch, duplicate IDs, and maximum batch size.

## 12. Decision Rules

### Prefer Set-Based Operation When

- All target rows receive the same values.
- Operation is batch delete, soft delete, status transition, detach, restore, tombstone, archive, or purge.
- Batch size is unbounded, user-controlled, or large.
- Path is public, hot, latency-sensitive, or repeatedly executed in jobs.
- Current implementation clearly performs looped database I/O.
- Operation does not rely on object-level hook, event, cascade, validation, identity-map, computed-setter, or domain behavior.
- Equivalent side-effect handling exists for audit logs, events, caches, indexes, counters, notifications, webhooks, permission caches, lifecycle hooks, and downstream sync jobs.

### Prefer Bulk Mappings, Parameterized Bulk Execution, Or Framework Bulk APIs When

- Each row receives different values.
- Batch size is moderate.
- Single-statement techniques would be much more complex or dialect-coupled.
- Per-object business logic is not needed.
- Code needs clearer bulk intent than object mutation.
- A single SQL statement is not necessary for correctness or measured performance.

### Keep Object-Level Unit-Of-Work When

- Batch size is small and clearly bounded.
- Operation is low-frequency, internal, admin-only, migration-only, or job-only with safe chunking.
- Object-level validation, event, hook, cascade, computed setter, identity-map synchronization, or domain behavior is required.
- Complex object graph consistency matters.
- Bulk DML would bypass important business semantics or side effects.
- There is no actual performance pressure and the current code is clear.

### Consider Dialect-Specific Single-Statement Techniques Only When

- Batch size is large.
- Endpoint or job is frequent or latency-sensitive.
- SQL count, round trips, lock time, or latency is already a measured bottleneck.
- Simpler bulk APIs are insufficient.
- The team accepts database-dialect coupling.
- Tests cover correctness, edge cases, and concurrency-sensitive behavior.
- Comments or documentation explain why the complex technique is needed.

Do not hardcode a recommendation for any specific database syntax in this skill. Refer to "dialect-specific single-statement technique" unless the current repository's stack and evidence justify a concrete recommendation.

## 13. Finding Disproof Pass

Before reporting findings, run an explicit disproof pass. Generate candidate findings first, then challenge each candidate with repository evidence before assigning priority.

For each candidate finding:

- Search for counter-evidence in code, tests, migrations, configs, docs, local conventions, runtime semantics, and intentional debt notes.
- Reject the candidate when counter-evidence invalidates the risk.
- Downgrade the candidate when the risk depends on unconfirmed scale, runtime behavior, stack semantics, or business contract.
- Preserve uncertainty instead of overstating conclusions; say what evidence would prove or disprove the issue.
- Avoid using the same reasoning path to both create and validate the finding. Re-check through a different path such as caller tracing, tests, configuration, schema/migration evidence, logs, or documented conventions.
- Put useful rejected candidates under "Non-Issues / Intentionally Not Flagged" so future reviewers do not repeat the same false positive.

Concrete database-access disproof checks:

- A loop is not a defect unless database I/O, lazy loading, flush, commit, repository call, query-builder execution, or driver execution occurs inside the loop.
- Object-level mutation is not automatically inefficient; check whether the unit of work, ORM, query builder, driver, or database batches work at flush, save, execute, or commit time.
- Raw SQL is not automatically unsafe; check parameter binding, identifier allowlists, tenant/project/user scope preservation, rowcount/returned-row behavior, tests, and maintainability justification.
- A set-based rewrite is not automatically better; check whether it would bypass hooks, events, validators, cascades, audit logs, outbox/domain events, cache invalidation, search indexing, counters, notifications, webhooks, permission caches, lifecycle hooks, or downstream sync jobs.
- Missing rowcount is not automatically severe; check all-or-nothing semantics, idempotency, stack rowcount behavior, returned rows, missing-ID reporting, and the business contract.
- N+1 is not confirmed unless relationship access, deferred fields, serialization, rendering, or computed properties actually trigger implicit I/O, or SQL logs, query-count tests, tracing, or runtime evidence show repeated queries.
- Empty input behavior must be verified before claiming broad-write risk. Check early returns, no-op guards, predicate generation, empty-list semantics, duplicate-ID handling, and maximum batch-size validation.

Use survival status consistently:

- `survived`: evidence supports the risk after counter-evidence checks.
- `downgraded`: a real concern remains, but priority or confidence is reduced by counter-evidence or uncertainty.
- `rejected`: repository evidence invalidates the candidate; do not report it as a finding.

## 14. Validation Safety

- Default audit mode is static and read-only.
- Do not connect to production databases.
- Do not run migrations, destructive commands, write scripts, data repair scripts, benchmark jobs, load tests, or backfills unless the user explicitly authorizes that action.
- Prefer static code inspection, local tests, dry-run mechanisms, existing logs, test databases, fixtures, and already captured query-count data.
- If validation requires executing code and there is any risk, state what would be run, against which environment, and why before running it.
- EXPLAIN, benchmark, and query-count guidance must be safe and scoped. Avoid expensive production operations, broad table scans, locks, or data mutation.
- When unsure whether a command touches live data, do not run it. Ask for confirmation or recommend a safe validation plan instead.

## 15. Fix Mode Guardrails

This skill is audit-first. If the user later asks for fixes, apply these guardrails:

- Propose a phased plan before modifying code unless the requested fix is small and unambiguous.
- Fix P0 correctness, security, and data-isolation issues before performance-only P1/P2 issues.
- Prefer the simplest safe set-based operation or bulk API change.
- Do not introduce dialect-specific single-statement SQL unless justified by scale, hot-path behavior, or measured bottleneck.
- Do not perform broad DAL/repository rewrites unless explicitly requested.
- Preserve tenant scope, rowcount semantics, transaction boundary, side effects, hooks, events, caches, indexes, counters, and object-level business behavior.
- State the intended operation-shape change for each fix, such as looped DB I/O to set-based operation, or object-level mutation to bulk API.
- Add or recommend tests for empty batch, duplicate IDs, missing IDs, forbidden IDs, partial success, all-or-nothing behavior, concurrency-sensitive relation attach, and query count when applicable.

## 16. Required Audit Workflow

1. Confirm the user-requested scope and whether the audit is read-only.
2. Apply scope control. Keep main findings limited to the requested scope unless the user asks for whole-repository audit.
3. Identify the repository technology stack from local evidence without assuming a framework.
4. Note user-specified ORM, database, framework, driver, or dialect, then verify it against repository files.
5. First discover project-specific database primitives and persistence conventions.
6. Perform targeted searches using those primitives and trace actual call paths.
7. Use broad generic search terms only after targeted searches to improve recall.
8. Search batch APIs, repositories, services, endpoints, jobs, and persistence helpers.
9. Search for loop plus database I/O patterns.
10. Search batch update, delete, insert, upsert, attach, detach, restore, archive, purge, and status transition logic.
11. Check empty batch, missing-predicate, optional-filter, duplicate-ID, and maximum-batch-size behavior.
12. Search raw SQL and dynamic query construction for parameterization, scope preservation, and bulk optimization justification.
13. Search relationship access, serializers, response builders, mappers, templates, and computed fields for N+1 risk.
14. Search transaction boundaries, commits, flushes, rollbacks, session/connection lifecycle, and concurrent execution.
15. Search tenant, project, organization, owner, user, soft-delete, and status scope conditions.
16. Search rowcount semantics, returned-row handling, missing-ID handling, duplicate-ID handling, and partial-success behavior.
17. Search side effects and derived state such as audit logs, outbox/domain events, caches, search indexes, counters, notifications, webhooks, permission caches, hooks, and sync jobs.
18. Search constraints, unique keys, foreign keys, indexes, migrations, and schema definitions.
19. Generate candidate findings with scope status, empty-batch behavior, rowcount semantics, current behavior, operation shape, evidence strength, certainty, risk, simple fix direction, whether single SQL is necessary, maintainability tradeoff, validation needed, priority, and confidence.
20. Run the Finding Disproof Pass on each candidate before reporting it.
21. Reject, downgrade, or preserve uncertainty based on counter-evidence.
22. Group repeated surviving findings before final output so recurring patterns do not hide the highest-risk issues.
23. Separate out-of-scope P0 risks under "Out-of-scope but high-risk note".
24. Output a read-only report unless the user explicitly asked for code changes.
25. If fixes are requested, apply Fix Mode Guardrails before modifying code.

## 17. Required Report Format

Use this structure unless the user explicitly requests another format.

### Summary

- Audit scope:
- Mode: read-only or fixes allowed
- User-specified stack:
- Inferred stack:
- Evidence inspected:
- Information not confirmed:
- Overall conclusion:
- High-priority issue count:
- Out-of-scope but high-risk note:

### Findings

Use this format for each finding:

```markdown
### Finding N - Title

- Priority: P0 / P1 / P2 / P3
- Location: file, function, line range
- Scope status:
  - in-scope / shared dependency / out-of-scope high-risk note
- Pattern:
- Current inferred behavior:
  - looped database round trips / object-level unit-of-work / parameterized bulk execution / set-based operation / possible lazy-load N+1 / unknown
- Estimated operation shape:
  - O(1) / O(N) / O(N*M) / unknown
- Evidence strength:
  - code path confirmed / config confirmed / migration confirmed / runtime confirmed / inferred only
- Empty batch behavior:
  - safe no-op / broad write risk / stack-dependent / not applicable / unknown
- Rowcount semantics:
  - matched rows / changed rows / returned rows / unavailable / stack-dependent / unknown / not applicable
- Evidence:
- Disproof attempted:
- Counter-evidence checked:
- Could be invalid if:
- Survival status:
  - survived / downgraded / rejected
- Risk:
- Recommendation:
- Tradeoff:
- Whether single SQL is necessary:
  - yes / no / maybe
- Validation needed:
  - SQL log / query count test / explain / benchmark / migration check / stack documentation / none
- Confidence:
  - high / medium / low
```

Every finding must explain:

- The concrete location.
- The scope status when scope is not obvious.
- The access pattern.
- The estimated operation shape and evidence strength.
- Empty-batch behavior and rowcount semantics for batch update, delete, restore, purge, or archive findings.
- The disproof attempted, counter-evidence checked, and why the finding survived or was downgraded.
- The inferred runtime behavior and whether it is confirmed.
- The risk to correctness, security, performance, operation, or maintainability.
- The recommended direction, not necessarily a patch.
- The complexity and maintainability tradeoff.
- Whether a single SQL statement is actually necessary.
- What evidence would validate or disprove the finding.

### Recommended Fix Order

Order by value and risk:

1. Correctness, security, data isolation, and data-integrity risks.
2. Simple set-based improvements for same-value batch writes and deletes.
3. Relation-table upsert, uniqueness, soft-restore, and concurrency protection.
4. Conditional per-row different-value updates where bulk APIs may be enough.
5. Observability, query-count tests, SQL logging, explain checks, benchmarks, and batch-size limits.

### Non-Issues / Intentionally Not Flagged

List useful rejected candidates or reviewed areas that should not be changed now, with reasons such as:

- Batch size is bounded.
- Path is low-frequency or admin-only.
- Object-level semantics are required.
- Current stack likely performs parameterized bulk execution, with validation noted.
- A single-statement rewrite would be over-engineering.
- Code performs in-memory loop construction followed by one bulk operation.
- Empty input is explicitly handled as safe no-op.
- Raw SQL is parameterized, scoped, tested, and justified for the current bulk path.

### Open Questions

List maintainer questions that materially affect the audit:

- Maximum batch size.
- Public, internal, admin-only, or job-only exposure.
- All-or-nothing requirement.
- Partial-success contract.
- Required handling of missing, forbidden, duplicate, already-deleted, or invalid-state IDs.
- Reliance on hook, event, cascade, validator, computed setter, default, trigger, or identity-map behavior.
- Available SQL logs, query-count tests, explain plans, benchmarks, or slow-query data.
- Database version, driver version, dialect constraints, and parameter limits.

The optional finding fields `Scope status`, `Empty batch behavior`, and `Rowcount semantics` may be omitted when clearly irrelevant. Include them for batch update, delete, restore, purge, and archive findings.

## 18. Output Compactness And Grouping

- For small or first-pass scoped audits, start with a compact summary table of findings.
- Expand only P0 and P1 findings by default.
- For P2 and P3, provide grouped bullets unless the user requests exhaustive detail.
- If the user asks for "full audit", "exhaustive", or "all findings", use the full finding template.
- Include disproof fields for expanded findings. For low-priority grouped items, summarize the counter-evidence check in one phrase unless the user asks for exhaustive detail.
- Group repeated findings by pattern when many files show the same issue.
- Expand P0 and P1 findings by default with enough detail to act.
- Summarize P2 and P3 findings unless the user asks for exhaustive detail.
- If there are many findings, show top findings first and put lower-risk items under "Additional Findings" or "Candidates For Follow-Up".
- Do not produce a huge report that hides actionable items.
- Include enough location evidence for each grouped finding so the reader can verify representative call sites.
- State sampling boundaries when the audit is not exhaustive.

## 19. Tone And Wording

- Be precise and do not exaggerate.
- Do not say a `for` loop is itself wrong.
- Do not say object-level mutation definitely emits one SQL statement per object unless verified.
- Do not say unit-of-work flush, executemany-like behavior, or driver batching definitely occurs unless verified.
- Do not claim code opens many connections unless the connection lifecycle evidence proves it.
- Clearly distinguish connection, transaction, round trip, statement, row mutation, flush, commit, and object mutation.
- Prefer concrete, actionable findings over vague "might be a problem" language.
- Mark unconfirmed behavior as uncertain and name the validation needed.
- Recommend the simplest safe change first.
- Explain correctness tradeoffs before performance rewrites.
- Avoid pushing dialect-specific single-statement SQL when a simpler set-based or bulk API option is enough.
- Preserve maintainability when performance evidence is weak.
- Do not claim empty `IN`/list behavior is unsafe unless verified.
- Do not claim rowcount means changed rows unless verified.
- Do not claim raw SQL is unsafe merely because it is raw SQL; judge parameterization, scope, and tests.
- Do not expand the audit into a general security review beyond database access risks.

## 20. Final Deliverable

When using this skill, deliver a read-only audit report by default. The final response must include:

- Files, modules, endpoints, jobs, migrations, schemas, tests, and configs inspected.
- Inferred or user-specified stack, with unconfirmed parts called out.
- Prioritized findings in the required format.
- Recommended fix order.
- Non-issues or intentionally retained object-level patterns when relevant.
- Open questions that block stronger conclusions.
- A clear statement that no business code was modified, unless the user explicitly allowed fixes and fixes were made.
