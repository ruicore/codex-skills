# Example: Notification Preferences Boundary Review

## Example User Request

"Review the architecture around notification preferences. I suspect rules are scattered, but do not change code yet."

## Relevant Context

- Fictional product: `BeaconDesk`, a team support inbox.
- Preferences can be changed in account settings, imported from an admin policy, and read by an email worker.
- Local docs say account settings owns user preferences.
- Code search shows preference defaults in the web app, API validators, worker config, and a migration.

## How The Skill Should Proceed

1. Stay read-only unless the user later asks for changes.
2. Inspect local architecture evidence: docs, settings UI, API routes, worker wiring, migrations, tests, and recent diffs if relevant.
3. Build a concise architecture map for settings, policy import, persistence, and notification delivery.
4. Identify the authoritative source for preference defaults and lifecycle rules.
5. Treat each possible issue as a hypothesis and actively search for counter-evidence.
6. Distinguish necessary boundary translation from conflicting authority.
7. Report only architecture findings: ownership, authority, boundary drift, lifecycle ambiguity, or change surface.

## Expected Output Shape

- Executive summary with architecture health and smallest useful improvement.
- Architecture map naming major modules and authority sources.
- Findings table with priority, location, issue, architectural reason, smallest useful action, and risk.
- Non-issues or known debt when candidate findings were disproved.
- Phased refactor plan scoped by concept or boundary.

## Validation Or Review Notes

- Every finding should cite a concrete file, module, doc, config, test, or repo-wide structure.
- If docs intentionally delegate defaults to the worker, the finding should be rejected or downgraded.
- Recommendations should consolidate authority only when evidence shows real duplication or drift.

## Common Mistakes The Skill Prevents

- Reporting ordinary code style or test coverage issues as architecture findings.
- Recommending a new abstraction before proving duplicated authority.
- Treating documentation as truth without comparing it to runtime wiring.
- Repeating known, documented debt as a fresh defect.
