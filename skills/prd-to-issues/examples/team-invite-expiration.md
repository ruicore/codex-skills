# Example: Team Invite Expiration Issue Plan

## Example User Request

"Convert this PRD into execution issues: team invites should expire after seven days, admins can resend expired invites, and users should see a clear expired-invite message."

## Relevant Context

- Fictional product: `CollabPad`.
- Existing invite creation and acceptance flows already work.
- The PRD includes non-goals: no bulk resend, no custom expiration period, and no audit-log UI.
- The target output is a JSON issue plan for coding agents, not direct GitHub issue creation.

## How The Skill Should Proceed

1. Extract product goal, workflows, non-goals, constraints, and acceptance criteria.
2. Identify implementation surfaces: invite model, acceptance API, admin resend action, user-facing expired state, tests, and rollout notes.
3. Create only necessary foundation work, such as adding an expiration field if no existing timestamp can support the behavior.
4. Split the rest into vertical slices that produce testable behavior.
5. Make dependencies explicit and acyclic.
6. Preserve blocking open questions instead of converting them into assumptions.
7. Output valid JSON only unless the user requests another format.

## Expected Output Shape

- JSON object with `project`, `summary`, `assumptions`, `open_questions`, `risks`, `issues`, and `recommended_sequence`.
- Issues with IDs such as `ISSUE-1`, each containing scope, out-of-scope, acceptance criteria, verification, dependencies, parallelization guidance, complexity, work areas, and PRD references.
- Recommended sequence grouping parallelizable issues after shared dependencies.

## Validation Or Review Notes

- The JSON should parse cleanly.
- Every dependency should reference an existing issue ID.
- The dependency graph should be acyclic.
- Each issue should include at least one acceptance criterion and one verification step.
- The plan should not create broad cleanup or final-QA issues without specific criteria.

## Common Mistakes The Skill Prevents

- Creating one issue per layer, such as "database", "backend", and "frontend", without deployable behavior.
- Adding bulk resend or custom expiration because they sound adjacent.
- Hiding unresolved policy decisions as assumptions.
- Adding artificial dependencies that block safe parallel work.
