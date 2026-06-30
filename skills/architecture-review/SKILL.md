---
name: architecture-review
description: General-purpose architecture review for any code repository. Use when Codex needs to assess concept ownership, authoritative sources, module boundaries, architecture decisions, architecture drift, duplicated concepts, scattered rules, hidden assumptions, over-engineering, architectural change surface, or phased refactor planning. Do not use for ordinary code review, testing review, implementation review, framework review, style review, or narrow bug diagnosis unless the user explicitly asks for architecture assessment.
---

# Architecture Review

Review repository architecture from local evidence. The goal is to identify what concepts exist, who owns them, where authority lives, which boundaries matter, where responsibilities are unclear, and what small architectural improvement would reduce future change cost.

Do not modify code during review unless the user explicitly asks for implementation. If the user asks for both review and changes, complete the architecture review first, then make only the agreed or clearly requested changes.

Example: [notification preferences boundary review](examples/notification-preferences-boundary.md).

## Scope

Architecture review is about ownership, authority, boundaries, concept consistency, architecture decisions, drift, and change surface.

It is not:

- code review focused on bugs, style, or local implementation quality
- testing review focused on coverage strategy or test design
- language or framework review focused on idioms, performance, or ecosystem practices
- general maintainability review unless the issue changes ownership, authority, boundaries, or concept lifecycle
- agent-legibility review focused on making future agent tasks easier outside an architectural concern

## Core Principles

- One concept should have one authoritative location.
- Important concepts need both a clear owner and a canonical source.
- A module should have one primary reason to change.
- Boundaries should preserve meaning, not only separate files.
- Rules should live with the concept owner or be explicitly delegated.
- Architecture decisions should remain traceable from rationale to implementation.
- Drift matters when implementation no longer follows the repository's stated or implied architecture.
- Change surface is architectural when one concept change requires many unrelated modules to change.
- Do not recommend abstraction unless it reduces real duplication, clarifies ownership, or narrows a boundary.
- Do not repeatedly report intentional architecture debt as a new defect; record its rationale and retirement condition.
- Prefer local evidence over intended architecture: inspect code, docs, configs, generated artifacts, runtime wiring, validation signals, and recent diffs when relevant.
- Every finding is a hypothesis. Before reporting it, actively attempt to disprove it. A finding should only survive if the available repository evidence does not invalidate it.

## Review Process

Follow this order. Do not jump to recommendations before building the architecture map.

1. Read local architecture evidence.
   - Inspect top-level structure, package boundaries, entrypoints, build/config files, generated or vendored areas, and major integration points.
   - Read local guidance if available: architecture docs, ADRs, specs, contribution docs, runbooks, and decision records.
   - Treat docs as evidence to compare against code, not as unquestioned truth.

2. Build a concise architecture map.
   - Identify major modules, what each appears to own, and which boundaries separate transport, persistence, orchestration, domain rules, presentation, infrastructure, policy, and external integrations.
   - Record main data/control flow only where it explains ownership or boundaries.

3. Identify important concepts and authorities.
   - List recurring domain nouns, state concepts, lifecycle concepts, external actors, resources, policies, and data shapes.
   - For each important concept, identify its owner, authoritative source, and places it is redefined, translated, validated, mutated, persisted, or removed.
   - Flag authority conflicts where multiple files, modules, schemas, configs, or docs appear canonical for the same concept.

4. Review boundaries and lifecycle ownership.
   - Ask what each module owns, what it should not own, and what would cause it to change.
   - Check whether concept meaning stays consistent across layers, packages, generated artifacts, services, and external integrations.
   - Flag boundary drift such as persistence owning lifecycle decisions, transport layers owning core rules, shared utilities becoming hidden domain owners, or adapters redefining internal concepts.

5. Detect architectural risks.
   - Duplicated concepts: repeated status groups, mappings, validation rules, defaults, policy checks, lifecycle transitions, or schema assumptions.
   - Scattered rules: a rule that can only be understood by reading several call sites or call order.
   - Hidden assumptions: invariants implied by defaults, defensive branches, comments in unrelated files, generated artifacts, or undocumented data contracts.
   - Over-engineering: abstraction, compatibility layers, generic helpers, or configuration that obscures ownership without proven variation.
   - Architecture drift: implementation that conflicts with documented or clearly implied architecture decisions.

6. Assess architectural change surface.
   - Ask how many modules must change for one important concept change, such as a new state, provider, workflow step, domain field, policy, validation rule, or integration.
   - Treat large change surface as architectural only when it reveals fragmented ownership, unclear authority, or excessive coupling.

7. Run the Finding Disproof Pass.
   - Challenge each candidate finding with counter-evidence before reporting it.
   - Reject, downgrade, or preserve uncertainty when local rationale, ownership evidence, tests, or scope limits weaken the claim.

8. Produce findings and a phased refactor plan.
   - Prioritize issues by correctness risk, authority conflict, boundary erosion, drift, and change cost.
   - Recommend the smallest useful architectural improvement.
   - Favor changes that can be reviewed one concept or boundary at a time.
   - Separate new findings from known or intentional architecture debt.

## Finding Heuristics

Use these checks to decide whether something is an architecture finding:

- Ownership: Can two places both change or define the same concept?
- Authority: Which source should reviewers trust when sources disagree?
- Boundary: Did a module take responsibility for a concept owned elsewhere?
- Meaning: Does a concept keep the same meaning when it crosses a boundary?
- Lifecycle: Are create, validate, transform, transition, persist, and remove responsibilities owned coherently?
- Rule location: Does a rule live with the concept owner, or is it scattered across callers?
- Decision consistency: Does implementation still follow documented or clearly implied architecture decisions?
- Change surface: Would one concept change require broad edits because ownership is fragmented?
- Abstraction fit: Does an abstraction clarify ownership or hide it?
- Debt lifecycle: Is a known architecture compromise documented with rationale and a retirement condition?

Avoid turning local implementation concerns into architecture findings unless they affect ownership, authority, boundaries, concept lifecycle, architecture drift, or change surface.

## Finding Disproof Pass

Generate candidate findings first, then validate them adversarially before reporting them.

For each candidate:

- Search for counter-evidence in code ownership, docs, ADRs, tests, runtime wiring, generated artifacts, and recent local conventions.
- Ask whether this is intentional architecture debt with rationale and a retirement condition.
- Ask whether the issue is actually a local implementation concern rather than architecture.
- Check whether a single authoritative owner or source was missed.
- Check whether apparent duplication is necessary boundary translation rather than conflicting authority.
- Check whether the proposed abstraction would reduce ownership ambiguity or merely add indirection.
- Downgrade or reject findings when counter-evidence is strong; preserve uncertainty when the repository evidence is incomplete.
- Avoid letting the same reasoning path both create and validate the finding without challenge.

When useful, list rejected candidates under "Known Architecture Debt" or "Non-Issues / Intentionally Not Flagged" instead of reporting them as findings.

## Priority Scale

- P0: Architectural issue can cause severe correctness, security, data integrity, deployability, or operational failure and needs immediate attention.
- P1: High-impact authority, ownership, boundary, hidden-rule, drift, or change-surface issue likely to cause regressions or block important work.
- P2: Meaningful concept duplication, scattered-rule, lifecycle, or boundary issue worth scheduling soon.
- P3: Low-risk architecture clarification, documentation, or small structural cleanup.

## Output Format

Use this structure unless the user asks for a different format. Keep it concise; omit sections with no meaningful findings.

### Executive Summary

- architecture health
- biggest architectural risks
- smallest useful improvement

### Architecture Map

- major modules and responsibilities
- key concepts and owners
- authoritative sources
- important boundaries
- major architecture decisions and drift, if any

### Findings

Use a table:

| Priority | Location | Issue | Architectural reason | Smallest useful action | Risk if unchanged |
|---|---|---|---|---|---|
| P0/P1/P2/P3 | file/module/function/doc or repo-wide | concrete issue | ownership, authority, boundary, lifecycle, drift, or change-surface reason | targeted action | likely consequence |

Every finding must cite a concrete location or clearly state that it is inferred from repository-wide structure.

### Concept And Boundary Notes

Use only when it adds signal beyond the findings:

- duplicated concepts or scattered rules
- authority conflicts
- hidden assumptions
- unclear lifecycle ownership
- boundary drift

### Change Surface

For important concepts, state what would need to change and why the surface is large or small. Keep this focused on architectural coupling, fragmented ownership, or unclear authority.

### Known Architecture Debt

List only deliberate, documented, or accepted architecture debt that would otherwise be repeatedly reported:

- debt
- rationale
- retirement condition

### Non-Issues / Intentionally Not Flagged

Use only when it prevents repeated false positives. Briefly list candidate findings rejected by the disproof pass and the evidence that invalidated them.

### Refactor Plan

- Phase 1: smallest low-risk ownership, authority, or boundary clarification
- Phase 2: structural consolidation that needs broader validation
- Phase 3: longer-term architecture direction, only if supported by evidence

For each phase, name expected blast radius, validation needs, and rollback shape when non-trivial.

## Quality Bar

- Findings must be architectural, not ordinary implementation nits.
- Findings must be evidence-backed. Say what was inspected and what remains uncertain when evidence is incomplete.
- Findings must survive the Finding Disproof Pass; do not report candidates invalidated by local rationale, ownership evidence, tests, or scope limits.
- Prefer targeted ownership, authority, boundary, or concept-lifecycle fixes over broad rewrites.
- Do not recommend compatibility aliases, re-exports, adapters, or migration layers unless real consumers or rollout constraints justify them.
- Do not include technology-specific rules unless they come from the current repository's own docs or code.
- For non-trivial recommendations, identify likely owner, expected blast radius, validation needs, and rollback shape.
