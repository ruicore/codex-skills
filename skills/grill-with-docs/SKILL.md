---
name: grill-with-docs
description: Deep architectural and domain grilling session that stress-tests plans against the current repository's domain language, implementation reality, and local documentation conventions. Use when the user wants to pressure-test a plan, architecture, domain model, workflow semantics, or durable repo knowledge, especially when findings may update repo-local context such as .manifest files, CONTEXT files, or ADRs.
---

# Grill With Docs

Use this skill to turn vague architecture or domain discussion into precise language, validated operational semantics, and carefully maintained repo-local knowledge.

Do not use it for ordinary bug fixes, small code edits, routine PR review, or one-off code tracing unless the user explicitly wants architectural pressure-testing.

## Core Loop

1. Discover the repository's local knowledge system before deep critique.
2. Resolve upstream concepts before downstream mechanics.
3. Ask one major question at a time unless several decisions are tightly coupled.
4. For each major question, explain why it matters, give the recommended answer, and name plausible alternative interpretations.
5. When code can answer the question, inspect the code instead of asking.
6. Pressure-test claims with concrete runtime scenarios: failure, retry, concurrency, partial success, rollback, ownership, and state transitions.
7. Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.
8. After raising objections, run the Self-Challenge Pass before turning them into conclusions or durable knowledge.
9. Persist only stable, validated knowledge. Do not fossilize brainstorming.

## Repository Discovery

Do not assume fixed documentation paths.

First identify semantic roles:

- Agent/repo instructions: examples include `.manifest/AGENTS.md`, `AGENTS.md`, `.ai/*`, `CLAUDE.md`.
- Domain context or glossary: examples include `.manifest/context.md`, `CONTEXT.md`, `docs/architecture/*`, `README` sections.
- Durable knowledge or decisions: examples include `.manifest/knowledge.md`, `docs/adr/*`, `decisions/*`.
- Validation or operational constraints: examples include `.manifest/validation.md`, deployment docs, runbooks, test docs.
- PR/commit conventions: examples include `.manifest/pr.md`, contribution docs.

Prefer pointer files over broad scans. If a repo instruction file says where context belongs, follow that rule.

For repos that use `.manifest`, treat `.manifest` as the default write location for this skill's generated knowledge. Keep all newly created or updated skill context files under `.manifest/` unless the user explicitly asks for public/team docs.

## Documentation Writes

Create or update files lazily, only when there is stable knowledge to preserve.

When writing:

- Follow the repo's existing knowledge structure and naming.
- If `.manifest/AGENTS.md` exists, read it first and obey its routing rules.
- If `.manifest/context.md` exists, use it for orientation, domain language, architecture shape, and reusable implementation patterns.
- If `.manifest/knowledge.md` exists, use it for confirmed decisions, repeated wrong assumptions, and durable behavioral facts.
- If `.manifest/validation.md` exists, use it for runtime validation data, test assets, environment constraints, and verification workflows.
- If the repo instead uses `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/`, use those conventions.
- If no suitable structure exists, propose the smallest repo-local structure before creating it. For personal/local agent knowledge, prefer `.manifest/`.

Do not update public product docs when the stable knowledge is only personal agent context. Do not create ADRs unless the repo already uses ADRs or the user accepts that convention.

## Domain Language Discipline

Treat terminology drift as architectural drift.

When the user uses vague or overloaded terms, stop and clarify. Propose canonical terms and distinguish adjacent concepts explicitly.

If existing docs define a term, compare the user's wording against that definition. Surface contradictions directly:

> Existing context defines cancellation as order-level, but this proposal implies item-level cancellation. Which model is intended?

When a term is resolved, persist it only if it is domain-level and likely to help future work. Avoid implementation trivia in glossary/context files.

## Implementation Reality

Architecture claims must survive contact with code.

When the user states how something works:

- Trace the actual runtime path.
- Name the branch conditions and ownership boundaries.
- Distinguish synchronous acknowledgements from asynchronous payloads.
- Distinguish wrapper/service objects from real external connections.
- Surface doc/code drift as a first-class finding.

If implementation and desired architecture disagree, ask whether the code is wrong, the docs are stale, or the proposal intentionally changes the model.

## Self-Challenge Pass

After raising objections, try to disprove each serious objection with repository evidence.

- Search for counter-evidence in code paths, docs, tests, runtime wiring, context files, ADRs, rollout notes, and explicit user constraints.
- Distinguish objections that survive evidence from objections that are only missing-context concerns.
- Downgrade or remove objections when repository evidence invalidates them.
- Preserve uncertainty instead of overstating doc/code drift, ownership gaps, or semantic conflicts.
- Do not manufacture criticism if the repository evidence supports the proposal.
- Avoid using the same reasoning path to both create and validate the objection without challenge.
- Persist only objections, decisions, or glossary updates that survive this pass or are explicitly accepted by the user as unresolved context.

## Scenario Pressure Tests

Do not leave claims abstract. Test them with concrete scenarios such as:

- duplicate request or duplicate webhook delivery
- timeout followed by late success
- retry after process restart
- concurrent mutation of the same workflow
- partial success and rollback
- missing external asset or unavailable runtime service
- ownership crossing frontend/backend or service boundaries

Use scenarios to force decisions about state, ownership, retries, consistency, and user-visible results.

## Decision Persistence

Use status labels when useful:

- Proposed: exploratory, not durable.
- Validated: accepted and backed by code, docs, tests, or explicit user decision.
- Deprecated: no longer preferred but historically relevant.
- Superseded: replaced by a newer decision.

Suggest an ADR only when all are true:

1. The decision is hard to reverse.
2. It would be surprising without explanation.
3. It reflects a real trade-off among alternatives.

If any condition is missing, prefer a lightweight context or knowledge note.

If the repo uses the bundled formats and they fit the repo convention, use [CONTEXT-FORMAT.md](./CONTEXT-FORMAT.md) or [ADR-FORMAT.md](./ADR-FORMAT.md). Otherwise follow the repo's existing format.

## Portability Notes

- Specific to the author's current workflow: `.manifest/` is a preferred personal agent-knowledge location only when the target repository already defines or accepts it.
- Reusable: repo-convention discovery, evidence-backed domain pressure testing, self-challenge before preserving claims, and stable-knowledge persistence.
- Adapt before reuse: inspect the target repository's instruction files, durable documentation locations, public/private doc boundary, and ADR or context-file conventions before writing.
