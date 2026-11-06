# Evidence and limitations

This library contains optional workflows, executable helpers, and small evaluation
fixtures. No collection-wide improvement over ordinary agent use has been
established. A workflow can be useful for expressing a preference without
improving a model's results on a particular task.

## What each check establishes

| Evidence | Establishes | Does not establish |
| --- | --- | --- |
| Registry, links, version, and public-content checks | Conformance to repository packaging and publication rules | Correct task execution or skill effectiveness |
| Installer and commit-scope tests and demos | Specific observed helper behavior on the tested platform | Automatic authorship attribution, remote trust, or agent adoption of the helper |
| Workflow decision and runtime-plan fixtures | Conformance to defined contracts on synthetic cases | Live tool behavior, a diagnosis, or improvement over a control |
| A controlled task comparison | Differences observed for the recorded tasks, instruction version, model, and tools | Universal benefit, production safety, or cross-model generalization |

The [CI workflow](../.github/workflows/validate-skills.yml) tests helpers and
packaging on Linux and Windows. Inspect the actual run for observed platform
results: adding a matrix is not evidence that both jobs passed. CI does not
run language-model comparisons.

## Current examples

- [Tool demonstrations](tool-demos.md) exercise installation, local-edit
  protection, receipt verification, and staged commit scope in disposable local
  directories. They run real helper entry points rather than a model simulation.
- [Workflow decisions](../evals/workflow-behavior/README.md) check a small
  synthetic response contract. The rationale still needs review.
- [Runtime diagnosis plans](../evals/runtime-diagnose/README.md) check bounded,
  read-only plans. Correct labels are not proof that an investigation was done.
- [Agent legibility trial](../evals/agent-legibility/README.md) prepares an
  ordinary-request, short-instruction, and full-skill comparison. Model runs and
  comparative results are **not yet available** for this public trial.

## How to choose

Use a specific skill when its procedure, tool knowledge, or recurring preference
adds something needed for the task. Prefer a direct request when that communicates
the same requirement adequately. A `portable-candidate` or `stable-workflow` label
is not a recommendation to load it automatically. Select only what you need.

Before recommending a skill on effectiveness grounds, record its exact content,
the control conditions, independent task attempts, actual cost observations, and
outcome grading. Report ties, regressions, missing measurements, and failures.
Do not rewrite fixtures or expected answers to make a treatment win.

## Public evidence boundary

Only independently designed synthetic tasks and reviewed public material belong
in public examples. Private conversations, incident records, code, datasets,
schemas, architecture, and performance measurements are not public evidence.
Replacing identifiers does not establish independence. A private observation
may motivate a hypothesis; public conclusions require independent evidence.
