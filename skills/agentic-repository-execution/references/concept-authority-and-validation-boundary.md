# Concept Authority And Validation Boundary

Use this gate before planning or implementation when a change crosses component
boundaries or handles extensible schemas, configuration, messages, or payloads
whose semantics may be owned elsewhere.

The gate prevents a component from becoming an accidental second source of
truth merely because it stores, transports, exposes, or validates data.

## When To Run

Run the gate when any of these conditions apply:

- data or configuration crosses a service, package, process, plugin, provider,
  or other ownership boundary;
- a schema, field set, enum, variant, or cross-field rule is expected to evolve
  independently of the component being changed;
- multiple components are about to model or validate the same semantic rules;
- a component that stores or forwards a payload is also being asked to
  interpret its internal meaning;
- adding a new valid variant may require edits across several unrelated
  components.

Omit the gate for a localized change whose concept owner, canonical source, and
validation responsibility are already explicit and unchanged.

## Required Authority Map

Record:

```markdown
## Concept Authority And Validation Boundary

- Concept or data shape: <what is crossing the boundary>
- Authoritative owner: <component or actor that owns its meaning and evolution>
- Canonical source: <schema, contract, code, generated artifact, or decision>
- Current component responsibility: <create|interpret|store|route|expose|other>
- Consumer responsibility: <what downstream consumers own>
- Treatment: <opaque|partially interpreted|fully interpreted, with rationale>
- Generic boundary validation: <syntax, envelope, size, identity, security, or other locally owned invariants>
- Owner-defined semantic validation: <where field, enum, combination, and lifecycle rules are enforced>
- Duplicate representations: <locations and necessity, or none>
- New-variant change simulation: <components that must change when the owner adds one valid variant>
- Gate: <NOT RUN|PASS|FAIL|BLOCKED>
```

Use only the four standard Evidence Gate states. Do not introduce `N/A`; omit
the gate entirely when it is not triggered.

## Decision Checks

### Authority Check

Determine which source wins when local models, schemas, documentation, and the
owning component disagree. A convenient local representation is not an
authoritative source unless ownership evidence makes it one.

### Opaque-Payload Check

When a component only receives, stores, routes, exposes, or validates data
against a canonical schema, it should not infer or freeze internal domain
semantics. It may still enforce the generic transport, security, tenancy,
identity, size, and persistence invariants it owns.

Partial interpretation is valid only when the interpreted subset is explicitly
owned by the component or forms a documented boundary contract. Record that
subset; do not let it expand implicitly.

### Duplicate-Rule Check

Search for copied dynamic field sets, enums, defaults, conditional combinations,
cross-field rules, and lifecycle semantics. Require each duplicate to be one of:

- a generated artifact derived from the canonical source;
- a necessary boundary translation with an explicit owner and compatibility
  contract;
- an independently owned invariant whose meaning only appears similar;
- a defect to remove before or within the authorized task.

Defensive validation alone is not sufficient justification for duplicating
fast-changing semantics.

### New-Variant Change Simulation

Ask what must change when the authoritative owner adds one valid field, enum
value, configuration variant, provider, protocol variant, or equivalent
extension.

The change surface should normally remain within the owner, canonical contract,
generated artifacts, and consumers that genuinely interpret the new meaning.
If passive stores, routers, or unrelated services must be edited, treat that as
evidence of boundary leakage unless a public compatibility or safety invariant
requires it.

## Gate Result

Mark `PASS` only when:

- the authoritative owner and canonical source are explicit;
- generic validation is separated from owner-defined semantic validation;
- opaque and interpreted portions are named and justified;
- duplicate representations are absent or evidence-backed;
- the new-variant simulation has a responsibility-aligned change surface.

Mark `FAIL` when current evidence proves these conditions are violated and the
violation is within the authorized remediation scope. Mark `BLOCKED` when the
required owner, source, contract, or decision cannot be established.

On `FAIL`, narrow the remediation to restore authority and validation
boundaries, then rerun the gate. On `BLOCKED`, pause dependent implementation and
use the Decision Request or Stop Record workflow. Do not encode an unresolved
ownership choice in production code as a temporary default.

## Disproof Pass

Before rejecting a duplicate representation or interpreted boundary, look for
counter-evidence:

- the component may own a security, public compatibility, or persistence
  invariant that requires local enforcement;
- the representation may be generated rather than independently maintained;
- the apparent duplication may be an explicit translation between different
  contracts;
- rollout or offline-operation constraints may require a versioned snapshot.

Record the evidence and bounded responsibility when one of these applies. The
goal is one clear semantic authority, not the removal of necessary boundary
validation.
