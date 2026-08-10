# Runtime/Diagnose visible protocol evaluator

This package evaluates structured, read-only Runtime diagnosis plans against a
small set of synthetic, visible fixtures. It is standalone: it needs only this
directory and a caller-supplied directory containing one JSON plan per fixture.

It is a protocol evaluator, not production proof and not an independent model
benchmark. A passing result shows that a plan satisfies the documented typed
contract for these synthetic cases; it does not establish a real incident's
cause or validate a repair.

## Contract

Each plan must use `diagnosis_plan/v1` and be named `<case-id>.json`. The plan
must separate observations from inferences, state identity and freshness
status, record correlation handling, list the minimum evidence, and propose
only permitted read operations. Confirmed causes, confirmed repairs, and
mutation operations are rejected by the evaluator.

The `loopback-health-identity-gap` fixture demonstrates an important boundary:
a successful health response alone does not establish which runtime produced
it. When identity metadata is incomplete, the plan must retain an unknown
identity, state the visibility gap, avoid cause or repair conclusions, and ask
for a further read-only observation.

## Run

The evaluator rejects an output location that resolves to this package or any
of its descendants, before it creates a directory or writes a report. Use an
external output location:

```powershell
python scripts/evaluate.py --plans <plan_directory> --output <output_file>
```

The report is canonical JSON and includes a content digest so repeated runs
with the same inputs produce identical output.

## Validate

```powershell
python -m unittest discover -s tests -v
python scripts/public_hygiene.py --root .
```
