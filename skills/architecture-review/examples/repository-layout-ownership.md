# Example: Repository Layout Ownership Review

## Example User Request

"Review this working backend's layout before we split its largest modules. Focus
on concept ownership and boundaries; do not change code yet."

## Relevant Context

- The repository has clear top-level layers such as `api/`, `application/`,
  `domain/`, and `infrastructure/`.
- Inside those layers, broad modules own several independent capabilities.
- One application module handles queries, validation, lifecycle transitions,
  tags, and audit recording.
- One persistence module declares models for identity, projects, datasets,
  uploads, and events.
- Existing public tests pass and define behavior that a later refactor must
  preserve.

## How The Skill Should Proceed

1. Treat file size and flat directories as investigation signals, not findings.
2. Map each important concept, current owner, authoritative rules, callers, and
   validation surface.
3. Separate cohesive deep modules from modules with independent reasons to
   change.
4. Ask whether a future agent can identify the correct edit owner and likely
   consumers from the current architecture.
5. Design boundaries by concept or lifecycle ownership, not by arbitrary line
   ranges.
6. Reject a package split if it only adds folders, generic helpers, re-exports,
   or indirection while the original module remains the real owner.
7. Recommend an ordered migration only when each target boundary has a clear
   owner, contract-preservation requirement, and validation path.

## Expected Output Shape

- Architecture map with current concepts, owners, authorities, and change
  surfaces.
- Findings that distinguish architecture problems from navigation-only
  legibility issues.
- Target ownership map rather than a folder-count goal.
- Phased refactor plan with cutover, deletion, validation, and rollback notes.

## Candidate Finding That Should Survive

The application module owns query behavior, lifecycle transitions, validation
retry, tags, and audit recording. Those capabilities have different callers,
rules, and reasons to change. A concept-owned package could narrow authority and
change surface while retaining a stable public facade.

## Candidate Findings That Should Be Rejected

- "The file is over 1,000 lines, therefore split it." Length alone is not an
  architectural reason.
- "The layer needs more subdirectories." Folder count does not prove ownership.
- "Create `common.py` for shared helpers." A generic bucket can make authority
  less clear.
- "Keep the old module as a permanent compatibility wrapper." Preserve that
  surface only when real consumers or rollout constraints require it.
