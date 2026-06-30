# Example: Export Idempotency Decision Trace

## Example User Request

"Preserve the decision we just made: export retries must be idempotent by operation ID, not by filename."

## Relevant Context

- Fictional product: `ReportForge`.
- A failed CSV export can be retried by a background worker.
- Local evidence shows filenames can be regenerated after a template rename.
- The user clarified that duplicate files are worse than a retry that reuses the same operation result.
- The repository has no formal ADR for this narrow behavior, but it has an agent-facing `decision-traces/` convention.

## How The Skill Should Proceed

1. Apply the worth-recording gate: this is stable retry semantics that future agents are likely to need.
2. Inspect local evidence before writing: export job code, retry tests, worker config, and existing decision trace format.
3. Search existing traces to decide whether to update an existing trace or create a new one.
4. Write a concise trace in the repository's existing trace location.
5. Separate facts from interpretation: code evidence, user clarification, rejected filename-based idempotency, and final operation-ID contract.
6. Include current status, validation run or not run, and revisit triggers.
7. Verify the trace exists, is readable, and does not include raw private logs or identifiers.

## Expected Output Shape

- Trace title with date and focused decision name.
- Problem, evidence, clarified constraint, final decision, validation, and revisit trigger.
- Concrete local file references discovered in the current repository.
- Brief final response stating the trace path and validation performed.

## Validation Or Review Notes

- The trace should not be created if the decision is unresolved or already captured without changes.
- If the trace directory is ignored or private, do not stage it unless the user explicitly asks.
- Do not claim tests passed unless they were actually run.
- Avoid raw payloads, customer names, tokens, or private operational logs.

## Common Mistakes The Skill Prevents

- Saving a chat recap instead of a durable engineering decision.
- Creating a new repository convention when one already exists.
- Recording private logs or sensitive identifiers in a version-controlled trace.
- Reintroducing filename-based idempotency in future retry work.
