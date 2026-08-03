# Database Access Audit Pattern Catalog

Read the relevant sections after discovering the repository's actual persistence primitives and tracing a real caller-to-database path.

## Contents

- [Behavior distinctions](#behavior-distinctions)
- [Search vocabulary](#search-vocabulary)
- [Looped database I/O](#looped-database-io)
- [Object-level batch mutation](#object-level-batch-mutation)
- [Batch delete and soft delete](#batch-delete-and-soft-delete)
- [Batch insert and relation attach](#batch-insert-and-relation-attach)
- [N+1 and implicit lazy loading](#n1-and-implicit-lazy-loading)
- [Unnecessary object loading](#unnecessary-object-loading)
- [Scope isolation](#scope-isolation)
- [Rowcount and partial success](#rowcount-and-partial-success)
- [Transactions](#transactions)
- [Concurrency, constraints, and indexes](#concurrency-constraints-and-indexes)
- [Side effects and derived state](#side-effects-and-derived-state)
- [Empty batch and broad-write guards](#empty-batch-and-broad-write-guards)
- [Raw SQL and dynamic queries](#raw-sql-and-dynamic-queries)
- [Operation-shape decision rules](#operation-shape-decision-rules)

## Behavior Distinctions

Use these terms precisely:

- **Looped database I/O:** each iteration triggers a query, write, lazy load, flush, commit, repository call, driver call, statement, or round trip.
- **Object-level unit-of-work mutation:** code loads objects, mutates them, and relies on flush/save/commit; this may or may not emit one statement per object.
- **Parameterized bulk execution:** the stack executes the same operation with many parameter sets through bulk mappings, batch execution, multi-parameter execution, or an executemany-like facility.
- **Set-based operation:** one database statement targets multiple rows through a predicate, join, subquery, source set, or equivalent database-side operation.
- **Upsert/conflict handling:** insert-or-update, ignore, or merge behavior protected by a database constraint or equivalent conflict mechanism.
- **Lazy-load or implicit I/O:** association, deferred-field, computed-property, proxy, serializer, or collection access triggers database work outside the obvious query site.
- **Transaction:** the atomic database boundary, not a synonym for connection, statement, session, request, or repository method.
- **Connection:** a database communication resource; claim multiple connections only when acquisition evidence proves it.
- **Round trip:** one client-to-database interaction; do not infer it from row-level object mutation.
- **Statement:** a database operation sent for execution; do not equate statements with rows, transactions, connections, or round trips.

## Search Vocabulary

Search project-specific APIs first. Then improve recall with stack-neutral terms such as `batch`, `bulk`, `many`, `list`, `ids`, `update`, `delete`, `insert`, `upsert`, `save`, `add`, `attach`, `detach`, `restore`, `purge`, `archive`, `tombstone`, `member`, `role`, `permission`, `tag`, `link`, `join`, `relation`, `transaction`, `commit`, `rollback`, `flush`, `lock`, `version`, `tenant`, `project`, `organization`, `owner`, `scope`, `deleted`, `status`, `count`, and `returning`.

## Looped Database I/O

Search for awaited or synchronous database, repository, query, save, delete, relation, existence, permission, association, flush, or commit calls inside loops, including nested relation loops.

Judge the actual operation shape. Meaningful O(N) database interaction is normally P1 and may be P0 when it creates correctness, isolation, or atomicity risk. Raise concern for user-controlled or unbounded batches. Treat commit inside the loop as severe because it can create partial success, lost atomicity, prolonged resource use, and difficult recovery. Do not flag loops that only build in-memory inputs before one bulk execution.

## Object-Level Batch Mutation

Search for batch object loads followed by mutation and flush/save/commit, full-entity loads for uniform updates, and required object methods, validators, hooks, or setters.

For uniform values, consider set-based updates only when object-level semantics are unnecessary. For different values, consider stack bulk APIs before complex SQL. Verify whether full objects are required for validation, events, cascades, identity-map behavior, or domain logic and whether the stack batches at flush or emits per-row work before making performance claims.

## Batch Delete And Soft Delete

Search for per-row hard deletes; deleted flags/timestamps; tombstone, archive, recycle, restore, purge, and status/state-machine transitions.

For same-value soft deletion, restore, archive, tombstone, or status transitions, prefer set-based operations only when semantics allow. For hard deletion, inspect foreign keys, cascades, triggers, retention, and invariants. For soft deletion, inspect scope, current state, rowcount, indexes, uniqueness, and restore behavior. Include expected current state in transition predicates when needed to prevent lost or invalid concurrent transitions.

## Batch Insert And Relation Attach

Search for per-row insert/save/add loops, nested many-to-many or membership creation, query-then-insert flows, soft-deleted relation restoration, and attach/detach of tags, roles, permissions, memberships, groups, links, projects, organizations, accounts, or owners.

Check database-backed uniqueness, check-then-insert races, conflict/upsert handling, restoration instead of duplicate creation, duplicate payload IDs, and all-or-nothing versus partial-success response semantics.

## N+1 And Implicit Lazy Loading

Search for association, deferred field, computed property, or proxy access inside loops; serializers, renderers, DTO mappers, and view models that touch unpreloaded relations; list processing that queries children per parent; and async property access that may perform implicit I/O.

Consider eager loading, prefetching, join-based reads, batched child queries, or grouping in memory. Avoid hiding queries in serialization. Confirm with query-count tests, SQL logs, tracing, or integration evidence. When lazy behavior is stack-dependent and unverified, report a possible N+1 with the required validation rather than a confirmed defect.

## Unnecessary Object Loading

Search for full entities loaded only to update/delete, validate existence, check permission, return IDs/counts, or precede a bulk operation.

Push applicable scope and current-state conditions into safe write predicates. Select only IDs or minimal fields when sufficient. Use affected/returned rows to represent missing or forbidden rows only when stack semantics support it. Retain object loading when rich validation, hooks, events, domain behavior, or object-graph consistency requires it.

## Scope Isolation

Inspect batch select/update/delete predicates for tenant, project, organization/account, owner/user, role/permission, soft-delete, and current-state scope.

Do not rely only on payload IDs or an application-memory precheck. If a precheck is followed by an ID-only write, inspect the race window and include scope in the write. For all-or-nothing behavior, compare affected or returned rows with the deduplicated expected set.

## Rowcount And Partial Success

Search for unchecked affected/returned rows; missing, forbidden, invalid-state, already-deleted, or failed IDs; duplicate input; ambiguous partial success; and responses that omit information callers require.

Deduplicate before expected-count comparisons. Enforce all-or-nothing through reliable affected/returned evidence. Make partial success explicit when allowed. Verify whether the current stack reports matched, affected, changed, returned, unavailable, or unreliable row counts, especially for idempotent updates whose rows are already in the target state. Use returned IDs/rows or another safe mechanism when rowcount cannot enforce the contract.

## Transactions

Search for competing commit ownership across handlers/services/repositories/jobs, flush or commit inside loops, external API/file/network/slow computation inside transactions, shared sessions or connections in concurrent work, error paths without rollback or cleanup, and unclear batch atomicity.

Require a clear authoritative transaction boundary for each business operation. Treat commit-in-loop as severe. Evaluate long-held locks, deadlock exposure, rollback cost, and retry/idempotency. Verify stack support before any concurrent sharing.

## Concurrency, Constraints, And Indexes

Search for check-then-insert without database uniqueness/conflict handling; state transitions without expected state/version/timestamp; relation tables without unique keys; unclear soft-delete uniqueness/restore semantics; unsupported high-volume predicates; large ID lists; missing chunking or parameter-limit handling; and lock-heavy purge/delete work.

Prefer database constraints for uniqueness and integrity, conflict handling for expected concurrent creation, and state/version predicates for lost-update prevention. Verify index support. For large work, evaluate chunks, timeouts, background execution, retries, deadlocks, rollback cost, and scheduling.

## Side Effects And Derived State

Search for audit logs, domain/outbox events, caches and permission caches, search indexes, denormalized counters and aggregates, hooks/validators/callbacks/setters/defaults/triggers, notifications/webhooks/messages, and reconciliation or downstream sync jobs.

Do not replace object-level writes with bulk DML unless equivalent side-effect behavior exists. If expected side effects are absent in the current path, evaluate correctness rather than only performance. Every recommendation must explain how required derived state remains consistent. Mark unclear equivalence uncertain and validation-needed.

## Empty Batch And Broad-Write Guards

Search for empty IDs/filters/selectors, conditionally appended predicates, writes that can lose all restrictive conditions, user-controlled filter propagation, early no-op guards, deduplication, batch-size limits, and optional filters that broaden generated queries.

An update/delete/purge/restore/archive path that can execute without a restrictive predicate is P0 unless proved safe. Empty input should normally be a no-op. Verify stack-specific empty-list SQL generation and compare all-or-nothing expectations after deduplication.

## Raw SQL And Dynamic Queries

Search for interpolated, concatenated, formatted, or templated SQL; dynamic table/column/order/filter/operator/JSON-path identifiers; inserted IDs or search/pagination values; and raw paths that bypass shared scope helpers.

Bind user values. Restrict dynamic identifiers through allowlists or safe stack APIs. Preserve scope, rowcount, and partial-success behavior. Require tests and maintainability justification for raw bulk optimization. Treat SQL injection or cross-scope access as P0, but do not flag safe raw SQL merely for being raw.

## Operation-Shape Decision Rules

### Prefer Set-Based Operations

Use when all rows receive the same values; the action is delete, soft delete, transition, detach, restore, tombstone, archive, or purge; batches are meaningful, unbounded, user-controlled, frequent, or hot; actual looped I/O exists; object-level semantics are unnecessary; and equivalent side-effect handling exists.

### Prefer Bulk APIs Or Parameterized Bulk Execution

Use when each row receives different values, batches are moderate, single-statement techniques would add complexity or dialect coupling, per-object logic is unnecessary, and a single statement is not required for correctness or measured performance.

### Keep Object-Level Unit Of Work

Use when batches are small and bounded; paths are low-frequency, internal, administrative, migration-only, or safely chunked jobs; hooks, validation, events, cascades, computed setters, identity-map synchronization, object graphs, or domain behavior matter; bulk DML would bypass required semantics; and no demonstrated performance pressure justifies added complexity.

### Consider Dialect-Specific Single Statements

Consider only for large or frequent latency-sensitive work where measured statement count, round trips, lock time, or latency is a bottleneck; simpler bulk APIs are insufficient; the team accepts dialect coupling; tests cover correctness, edges, and concurrency; and documentation explains the complexity. Do not prescribe syntax until repository evidence establishes the exact stack.
