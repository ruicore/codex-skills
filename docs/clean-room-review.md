# Clean-Room Skill Review

Use this review after a public skill draft exists and before it is committed.
It complements identifier scanning; it does not replace it.

## Reviewer Isolation

The reviewer may inspect only:

- the abstract capability, engineering invariants, authorization boundaries,
  and failure modes;
- the proposed public skill, references, scripts, examples, and fixtures;
- cited public specifications or official documentation.

The reviewer must not receive private source material, a private-to-public
mapping, or an explanation of which employer, customer, project, incident, or
repository motivated the skill. Those records remain under ignored
`.manifest` storage.

If the reviewer needs private context to understand or approve the public
artifact, the review fails.

## Independence Matrix

Review each dimension independently:

| Dimension | Pass condition |
|---|---|
| Domain | The public problem domain is unrelated or demonstrably public. |
| Actors | System and human roles were independently designed. |
| Terminology | Names and concepts do not preserve private vocabulary or a renamed equivalent. |
| Data | Schemas, values, and examples are synthetic or come from cited public specifications. |
| Workflow | Step ordering and state transitions are independently expressed and no distinctive private topology is preserved. |
| Files | Filenames, paths, package structure, and artifact shapes are independently designed. |
| Fixtures | Tests exercise synthetic behavior and contain no private exports, screenshots, logs, or transformed samples. |
| Implementation | Code and prose were written independently and are not copied, translated, or lightly renamed. |

Fail the review when any dimension depends on private provenance or when several
distinctive dimensions align closely enough that name replacement is the main
difference.

## Review Outcome

Choose exactly one outcome:

- `pass`: every dimension is independently justified from the public artifact;
- `rewrite-required`: the capability is valid, but one or more dimensions must
  be independently redesigned;
- `remove`: the useful behavior cannot be separated safely from private
  material;
- `needs-public-source`: a public specification or official source is required
  before the artifact can be justified.

Record only the outcome, reviewed public paths, date, and any public-facing
rewrite requirement. Do not record private provenance in a tracked review.

## Existing Skill Review

Apply the same matrix when reviewing an existing skill. A passing identifier
scan establishes only that known strings are absent. It does not establish
semantic independence. Skills that cannot be established as independent from
the public artifact alone remain `rewrite-required` until rewritten or reviewed
with a safe public source.
