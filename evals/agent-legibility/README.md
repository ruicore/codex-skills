# Agent legibility: three-condition pilot

Status: **prepared, not run**. No model-effectiveness result is claimed.
The generator and fixture tests are software checks, not respondent attempts.

Question: does the complete `agent-legibility-review` add useful findings beyond
an ordinary review request or a short instruction expressing the same perspective?

## Conditions and scope

| Condition | Input |
| --- | --- |
| A | Ordinary review task |
| B | Same task plus one short instruction about edit points, authority, and consumers |
| C | Same task plus the complete current skill text |

The three small repositories are independently written synthetic poetry and
star-chart examples. They include conflicting documentation, a missed consumer,
and a negative case whose navigation is already explicit. They do not reproduce
any private project's domain, schema, workflow, code, or incident. Small fixtures
can create ceiling effects and are not a representative industry benchmark.

## Prepare packets

From this directory, choose a new external output directory:

```text
python -B prepare_trial.py --output <external-new-directory> --seed 17 --repeats 2
python -B -m unittest discover -s tests
```

The default produces 18 independent attempts (3 cases, 3 conditions, 2 repeats)
in a seeded shuffled order. A packet contains only `task.md` and `workspace/`.
`operator/` holds the assignment key, scoring reference, source commit, registry
version, skill SHA-256, and prompt/fixture hashes. Every attempt starts as
`not_run`. Do not give respondents the source repository, this document,
`fixtures.json`, other packets, or `operator/`.

The preparer writes files only. It does not call a model, install a skill, manage
credentials, set a model, or promise that the caller's environment is isolated.

## Run protocol

1. Freeze task, skill, rubric, and conditions before the first attempt. Record
   any uncommitted source differences; the recorded content hash is authoritative
   for the treatment, and the source commit alone may not reproduce local edits.
2. Use fresh independent sessions with the same exact model, reasoning setting,
   tool access, read-only constraints, and tool-call budget (24 calls per attempt).
   Give each respondent only its packet. No previous reports or shared memory.
3. Inspect the actual session context. Inherited global skills, repository rules,
   hidden instructions, or cached findings can contaminate A and B. Record and
   control them equally; if isolation cannot be established, stop the comparison
   and report the limitation rather than a clean treatment effect.
4. The operator follows the seeded order. Capture the report and actual start/end
   timestamps, model/effort, input/output tokens when available, tool calls,
   failed calls, budget exhaustion, and human interventions. Unavailable cost
   values remain null. Agent self-reported elapsed time is not a measurement.
5. Give an independent grader anonymous reports and the rubric, without condition,
   prompt, or assignment key. Respondents see their own instructions, so they are
   not blinded. Report wording can reveal treatment; note suspected unblinding.

Do not silently retry an unfavorable attempt. Record failures and any repeated
attempts separately. Discarding an attempt requires a stated technical reason
unrelated to whether its answer helps the skill. No production or private data
is needed. Model runs must have their own authorized execution environment.

## Grade and interpret

For each rubric item assign 0 (absent/wrong), 1 (partially supported), or 2
(correct mechanism, concrete location, and consequence). Score only actionable
navigation findings, not verbosity or familiar keywords. Credit a correct
no-finding conclusion on the negative case. Separately count unsupported
findings, missed required items, unnecessary structural changes, and invented
runtime or test claims. Freeze any extra finding's validity before unblinding.

Compare within each case across repeated attempts. Report per-case scores and
failure counts alongside cost observations; do not collapse quality and cost
into an unexplained overall score. B vs A tests the extra perspective; C vs B
tests the extra package text. A tie, regression, or inconclusive result is valid.
Two repetitions are a pilot, not statistical evidence of general superiority.

Publish reviewed synthetic inputs, exact prompt/skill hashes, anonymized reports,
grades, failures, and limitations before making a result claim. Do not export
raw session logs, local paths, account data, or private tool context. Review all
artifacts and new commit history for public safety before committing them.
