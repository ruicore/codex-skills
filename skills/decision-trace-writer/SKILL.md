---
name: decision-trace-writer
description: Preserve settled engineering decisions, findings, and clarified constraints in repository-local records when the user requests persistence or repository rules authorize it. Use after review, diagnosis, or implementation, not as the primary workflow or for global memory.
---

# Decision Trace Writer

Leave enough evidence and reasoning for a future agent to continue without
reopening settled questions. Complete the primary engineering work first.

## Decide Whether To Record

Write only when both conditions hold:

- The user requested persistence or an applicable repository rule authorizes it.
  An existing directory determines placement, not permission. Reuse existing
  authorization without asking again.
- The result has future decision value: a settled finding or constraint, a
  meaningful rejected alternative, or a material change to an existing
  decision's implementation or validation status.

Keep routine details, transient plans, unresolved investigations and unchanged
duplicates in the current response or active work context. A settled decision may
still be unimplemented; say so. Prefer an existing specification or ADR when that
is the right home for the result, rather than creating a parallel authority.

## Inspect And Update

Inspect the relevant current code, tests, specifications and repository rules;
do not rely on conversation memory alone. Separate observed current behavior
from the accepted target, user constraints and labeled inference. Record any
conflict or missing evidence instead of choosing a convenient version.

Search existing records. Update the same decision when its assumptions, status,
validation or revisit conditions change. Create a new record only for a different
decision. Mark superseded assumptions clearly and keep historical test results
tied to their date or revision; an old PASS is not current validation.

## Write The Smallest Useful Record

Follow the repository's language and format. Cover these points without
repeating the same facts under multiple headings:

- **Problem and evidence:** the claim, concrete source locations, and what they
  establish or leave unknown.
- **Decision and rationale:** the chosen behavior, important rejected alternatives
  and the concern behind the user's clarification.
- **Contract:** required and prohibited behavior, invariants and scope boundaries.
- **Status and validation:** what is implemented or committed; which checks ran,
  against what version, with what results; what is planned, skipped or blocked.
- **Continuation and revisit:** affected files, the next useful verification, and
  evidence or changed assumptions that would justify reopening the decision.

Use more detail when needed to preserve a consequential boundary, not merely
because the topic is architectural. Link the canonical specification rather
than copying it. Read [trace formats](references/trace-formats.md) only if a
layout example would help; the [fictional example](examples/export-idempotency-trace.md)
is also optional.

Include `trace_privacy_class: local_raw_trace` for ordinary local records.

## Place And Protect

Use the user-specified path, otherwise the existing trace or repository-local
context convention. If neither exists, propose a simple location in an
interactive session; in a non-interactive task use `decision-traces/` and state
that no convention was found. Do not invent a directory hierarchy.

Name new files `YYYY-MM-DD_HHmm_<decision_slug>_trace.md`. Keep the existing path
when updating a decision.

Never include credentials, secrets or raw session transcripts. Prefer stable
summaries to raw logs or payloads; exclude raw personal/customer data unless
explicitly authorized and necessary for local storage. Keep ignored or private
records unstaged unless the user explicitly includes them. Repository-local
writing does not authorize global memory, publication or derived datasets.

## Optional TraceGym Metadata

For new records, omit TraceGym metadata unless the user or an applicable
repository rule explicitly requests it. A potentially reusable lesson alone is
not a trigger. Do not read its reference or add an omission explanation during
ordinary recording.

If explicitly requested, read [TraceGym metadata](references/tracegym-metadata.md)
and follow its schema. When updating an existing footer, retain accurate fields;
read that reference if affected fields need correction. Do not silently discard
existing metadata or expand it with speculative signals. Sanitized or public
derivatives remain separately authorized work.

## Verify And Finish

Check the saved file, placement, source references, status, privacy and Git state.
Report the path, whether it was created or updated, and checks actually performed.
Do not claim planned checks ran or a draft was saved. If nothing qualifies for
recording, say so briefly without creating a file.

## Source and License

Created by Ray Carter (ruicore). Free and open source under Apache-2.0.

- Source: https://github.com/ruicore/codex-skills/tree/main/skills/decision-trace-writer
- License: [Apache-2.0](LICENSE), included with this skill directory.
