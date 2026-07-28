# Model And Effort Routing

Use this reference when preparing dispatches. Route by task capability first,
then map the capability to settings that the current runtime actually exposes.

## Discovery Gate

Before naming a model or reasoning effort:

1. Inspect the current runtime's available model and effort controls.
2. Honor an explicit user or repository requirement when it is available.
3. Exclude unavailable, deprecated, or merely remembered settings.
4. Record `runtime default (selection unavailable)` when the runtime does not
   expose selection.

Do not hardcode a model name into reusable plans or templates as if every Codex
runtime provides it.

## Capability Classes

### Frontier High-Reasoning

Prefer the strongest available agentic reasoning model for:

- ambiguous architecture or contract work;
- risky cross-cutting changes;
- complex debugging with competing hypotheses;
- security, migration, concurrency, or data-integrity review;
- final validation where subtle counter-evidence matters.

Use a high or higher supported effort when the cost of a missed constraint is
material. Do not use maximum effort automatically; justify it from task risk and
uncertainty.

### Balanced Engineering

Prefer a balanced coding or engineering model for:

- bounded implementation with established contracts;
- focused tests, adapters, documentation, or configuration;
- small-to-medium changes with clear local validation;
- remediation after a validator gives concrete findings.

Use medium effort by default when available. Raise effort for integration
ambiguity; lower it for deterministic mechanical work.

### Fast Deterministic Execution

Prefer a fast, lower-cost available model for:

- narrow inventory or metadata updates;
- mechanical fixture generation with explicit schemas;
- repeatable command execution and evidence collection;
- simple validation reruns whose interpretation is unambiguous.

Use low effort only when the assignment remains independently checkable and
contains little design judgment.

## Routing Checks

For each dispatch:

- state the capability class;
- name the selected runtime-advertised model or runtime default;
- name only a supported effort value;
- explain the choice in one sentence;
- list fallbacks that are actually available, if needed;
- keep acceptance and validation independent of model identity.

Never use model prestige as a substitute for task decomposition or evidence.
If no available model is adequate for a high-risk task, mark the assignment
`BLOCKED` or reduce its scope instead of weakening the gate.
