# Example: Saved Filter Tracer Bullet

## Example User Request

"Use TDD to add saved filters to the task board. Start with the API behavior; the UI can come later."

## Relevant Context

- Fictional app: `TaskHarbor`.
- The public API already has endpoints for listing tasks with query filters.
- The requested first behavior is saving a named filter and loading it later for the same user.
- The repository has an integration test suite that can call the HTTP API with a test user.

## How The Skill Should Proceed

1. Confirm the public interface and priority behavior before coding.
2. List behavior tests, not implementation tasks.
3. Start with one tracer-bullet test through the public API: create a saved filter, then retrieve it for the same user.
4. Run the test and confirm it fails for the expected reason.
5. Add the minimal implementation needed for that single behavior.
6. Run the test again and get to green before adding another behavior.
7. Repeat for the next behavior, such as user isolation or duplicate-name handling.
8. Refactor only after green tests, then rerun the affected tests.

## Expected Output Shape

- Short TDD plan listing prioritized behaviors.
- Per-cycle notes: `RED`, `GREEN`, and optional `REFACTOR`.
- Test file and command used for each cycle.
- Final verification command.
- Any deferred behaviors or open interface questions.

## Validation Or Review Notes

- Tests should call the public API instead of private repository methods.
- Each cycle should introduce one failing behavior test and one minimal implementation.
- Refactors should not change observable behavior, and tests should run after each refactor.

## Common Mistakes The Skill Prevents

- Writing all saved-filter tests before any implementation.
- Mocking internal persistence when the public behavior depends on real storage integration.
- Adding UI, sharing, or analytics behavior before the current test requires it.
- Refactoring while the test suite is still red.
