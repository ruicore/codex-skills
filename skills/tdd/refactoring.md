# Refactor Candidates

After TDD cycle, look for:

- **Duplication** → Extract function/class
- **Long methods** → Break into private helpers (keep tests on public interface)
- **Shallow modules** → Combine or deepen
- **Feature envy** → Move logic to where data lives
- **Primitive obsession** → Introduce value objects
- **Existing code** the new code reveals as problematic

## Behavior-Preserving Refactor Checklist

Use this checklist when structure changes but public behavior should not.

### Contract Freeze

- [ ] Existing focused tests are GREEN, or pre-existing failures are recorded.
- [ ] Public APIs, errors, side effects, persistence, events, serialization, and
      ordering guarantees are identified.
- [ ] Characterization tests are added only for material behavior that lacks a
      public test anchor.

### Green-To-Green Slice

- [ ] One coherent responsibility and its consumers are selected.
- [ ] The responsibility is moved without adding behavior.
- [ ] Callers and imports are cut over.
- [ ] Focused tests pass.
- [ ] Old ownership is removed before the next slice.

### Cutover

- [ ] No duplicate implementation remains.
- [ ] Compatibility wrappers exist only for verified consumers and have a
      retirement condition.
- [ ] Tests verify public behavior rather than the new internal layout.
- [ ] Full relevant tests and project quality checks pass.
- [ ] Skipped or unavailable checks are reported.
