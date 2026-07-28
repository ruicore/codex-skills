# Example: Concept-Owned Package Migration

## Example User Request

"Refactor this working backend's broad application and persistence modules into
clear concept-owned packages. Preserve behavior and do not change public APIs or
database migrations."

## Baseline

```text
application/
  records.py        # queries, validation, lifecycle, tags, audit
  upload_jobs.py    # provisioning, idempotency, status mapping

infrastructure/db/
  models.py         # identity, projects, records, uploads, events
```

The existing tests pass. File length drew attention to the hotspots, but the
ownership map shows the real problem: each file has several independent reasons
to change and several distinct consumer groups.

## Target Ownership

```text
application/
  records/
    contracts.py
    queries.py
    validation.py
    lifecycle.py
    tags.py
    audit.py
  upload_jobs/
    contracts.py
    idempotency.py
    provisioning.py
    service.py

infrastructure/db/
  models/
    identity.py
    projects.py
    records.py
    uploads.py
    events.py
    __init__.py
```

The target is acceptable only if each module becomes the authoritative owner of
the named capability. The package `__init__.py` may preserve verified public
imports, but it must not become a second implementation owner.

## Migration Sequence

1. Run the existing focused and full tests.
2. Split persistence declarations by concept while preserving metadata
   discovery and verified import surfaces.
3. Move one application capability at a time, starting with pure queries and
   contracts before lifecycle operations.
4. Update real consumers and run focused tests after every cutover.
5. Delete the old implementation as each capability moves.
6. Reorganize tests by public workflow only when the existing test layout
   obscures behavior ownership.
7. Run full tests, lint, formatting, type checking, packaging, import, and schema
   discovery checks.

## Evidence Of Completion

- The original broad modules are deleted or reduced to justified public facades.
- No capability has two active owners.
- Public APIs, errors, persistence metadata, and migrations remain unchanged.
- New tests do not assert private module names.
- Before/after evidence describes ownership and change surface, not only LOC or
  folder count.

## Invalid Variants

- Moving every function into a separate file without concept ownership.
- Creating `common.py` for code shared by unrelated capabilities.
- Leaving all behavior in the old module and importing it through new facades.
- Adding permanent wrappers without verified consumers or retirement criteria.
