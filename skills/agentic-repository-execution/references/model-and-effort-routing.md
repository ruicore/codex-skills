# Model And Effort Routing

Use this reference for initial dispatch, re-dispatch, or any unavailable or
observably inadequate model, effort, skill, or tool.

## Contents

- [Discover before selecting](#discover-before-selecting)
- [Capability classes](#capability-classes)
- [Fallback ladder](#fallback-ladder)
- [Effort, skill, and tool substitution](#effort-skill-and-tool-substitution)
- [Timeout, partial evidence, and cost pressure](#timeout-partial-evidence-and-cost-pressure)
- [Routing substitution record](#routing-substitution-record)

## Discover Before Selecting

Before every dispatch or re-dispatch, inspect what the current runtime actually
advertises. Record:

- required capability class;
- selected runtime-advertised model or runtime default;
- supported reasoning effort;
- verified skills and required tools;
- adequate independent Review and Validation path.

A preferred setting is routing guidance, not an entitlement. Never invent,
remember, or hardcode an unavailable model, effort, skill, or tool.

## Capability Classes

### Frontier High-Reasoning

Use the strongest suitable advertised agentic reasoning capability for
ambiguous architecture or contract work, risky cross-cutting change, complex
debugging, security, migration, concurrency, data-integrity review, or subtle
final assurance. Use a high or higher supported effort when missed constraints
have material consequences.

### Balanced Engineering

Use an advertised balanced coding or engineering capability for bounded
implementation with established contracts, focused tests, documentation,
configuration, and remediation from concrete findings. Use medium effort by
default when it is supported and adequate.

### Fast Deterministic Execution

Use an advertised fast or lower-cost capability only for explicit,
independently checkable inventory, metadata, fixture, command, or evidence
collection work with little design judgment. Use low effort only when the
result remains independently verifiable.

Capability classes express task needs; they do not imply that every runtime
offers three distinct models.

## Fallback Ladder

Apply this order without weakening the assignment contract:

1. Choose another advertised setting in the same adequate capability class.
2. Choose an advertised stronger class when available and within existing
   authority and cost policy.
3. Narrow to a genuinely lower-complexity, independently verifiable slice while
   preserving the original risk classification, authority, side-effect limit,
   acceptance criteria, Review/Validation independence, and required proof.
4. Have the Root Master re-dispatch only that bounded slice and require the
   replacement to inspect preserved evidence.
5. Set the affected gate to `BLOCKED` when required capability, independence,
   input, tool, skill, or proof remains unavailable.

Fallback, timeout, silence, partial output, degraded capability, deadline, or
cost pressure never lowers risk, acceptance criteria, authority, side-effect
limits, assurance independence, or required evidence. Never let the Root Master
take over missing production work.

| Required class | Adequate route | Block when |
|---|---|---|
| Frontier high-reasoning | Same advertised frontier class, then an advertised stronger adequate class, then a narrower evidence or specialist slice. | High/Critical reasoning, specialist independence, or proof remains unavailable. |
| Balanced engineering | Same advertised balanced class, an advertised frontier class, then a narrower deterministic slice only when independently checkable. | Remaining work still needs judgment beyond available demonstrated capability. |
| Fast deterministic | Same advertised fast class, an adequate balanced class, then a smaller mechanical slice. | Work contains unresolved design judgment or unavailable evidence interpretation. |

## Effort, Skill, And Tool Substitution

Use the nearest supported effort only when it remains adequate for the same
capability class and evidence contract. Otherwise choose a stronger advertised
class or narrow and re-dispatch.

Treat a named skill or tool as available only after verifying it in the active
runtime. Use a replacement only when it:

- produces equivalent required evidence;
- does not increase side effects;
- remains within current authority;
- preserves required Review and Validation independence.

Otherwise keep dependent gates closed and set the affected gate to `BLOCKED`.
Do not replace a required observation with model assertion or use a more
invasive tool to bypass an unavailable read-only or validation tool.

## Timeout, Partial Evidence, And Cost Pressure

For timeout, silence, partial evidence, or observed degraded capability:

1. preserve verified artifacts and exact runtime evidence;
2. record the missing responsibility or proof;
3. use `FAIL` only when evidence proves noncompliance, otherwise `BLOCKED`;
4. have the Root Master narrow and re-dispatch the smallest missing slice;
5. rerun every assurance gate affected by the new or changed artifact.

Cost pressure is a routing constraint, never an acceptance exception. Prefer
smaller coherent slices and targeted re-dispatch. If authorized capability or
cost cannot satisfy the original contract, leave the gate `BLOCKED`.

## Routing Substitution Record

When an initial preference cannot be used or observed degradation causes
re-routing, record:

```markdown
## Routing Substitution <ID>

- Assignment / affected gate: <task and gate ID>
- Trigger: <unavailable model|effort|skill|tool failure|timeout|silence|partial evidence|degraded capability|cost pressure>
- Original required class and setting: <capability class and advertised preference>
- Runtime evidence: <how availability or inadequacy was observed>
- Replacement or narrowed scope: <advertised setting, equivalent tool/skill, or bounded slice>
- Adequacy rationale: <why original risk, acceptance, independence, and validation remain satisfied>
- Preserved constraints: <risk, authority, side effect, assurance independence, proof>
- Evidence preserved: <artifact, diff, or output paths>
- Dispatch / validation action: <Root Master re-dispatch and gates to rerun>
- Gate state and next condition: <NOT RUN|PASS|FAIL|BLOCKED and exact condition>
```

This record belongs in the execution plan, assignment handoff, relevant gate
record, or approved coordination path. It is not a new gate state or a model
scheduler.
