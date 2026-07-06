---
name: decision-trace-writer
description: Preserve stable engineering decisions as agent-facing traces, including architecture tradeoffs, debugging findings, review outcomes, user-clarified constraints, and SkillOpt-ready extraction metadata.
---

# Decision Trace Writer

Write a local, durable decision trace that lets a future Codex instance understand what happened, why it mattered, what constraints were clarified, what decision was made, and what work remains.

The trace is not a public user document. Treat it as agent-facing project memory. Follow the current repository's durable-memory convention instead of assuming one.

When a trace is worth preserving, also make it useful as future skill-improvement data: include enough structured signals for later extraction into a task, eval case, benchmark fixture, or SkillOpt-style training example. Do not create a trace only to produce training data.

Example: [export idempotency decision trace](examples/export-idempotency-trace.md).

## Worth Recording Gate

When this skill is invoked, first decide whether a durable trace is worth writing or updating. Do not create a trace only because the skill triggered.

Record a durable trace when at least one of these is true:
- the user explicitly asks to preserve context for future Codex runs, agent memory, or durable local guidance
- a stable engineering decision, finding, or constraint has been clarified and future agents are likely to need it
- local evidence confirmed, weakened, or disproved a review claim, bug hypothesis, or architecture concern in a way that should not be re-litigated
- the decision rejects an obvious alternative that a future agent might otherwise reintroduce
- the decision affects architecture boundaries, integration contracts, user-facing behavior, correctness, data integrity, migrations, evaluations, or cross-surface behavior
- implementation or validation changed the status of an existing decision trace
- the session revealed a reusable agent-workflow signal, such as a repeated failure mode, missing validation gate, better decomposition boundary, or corrected skill behavior

Do not write a durable trace when the work is only:
- a routine implementation detail with no new reusable decision
- a transient task plan, TODO list, meeting-style summary, or chat recap
- an unresolved investigation where the facts are still changing
- a duplicate of an existing trace with no changed decision, status, validation, or revisit trigger
- something a final response, inline code comment, active issue, or ordinary project document can capture more clearly
- raw training data, raw transcript archival, or unreviewed conversation dumping

If the answer is "not worth recording," stop using this skill for the task and briefly state why no durable trace was created. If the answer is borderline in an interactive session, explain the tradeoff and ask or propose before creating a new trace.

## Not For

Do not use this skill for:
- ADRs intended for human readers
- implementation plans or task breakdowns
- meeting notes
- brainstorming artifacts
- tech debt registries
- unresolved investigations
- raw Codex transcript dumps
- benchmark datasets without a stable decision, finding, or reusable workflow signal

Use this skill only when a decision, finding, or constraint is stable enough to preserve. If the investigation is still open, record what is known in the active work context instead of creating a durable decision trace.

This skill does not replace formal ADRs. If the repository already has ADRs, a decision trace may serve as agent-facing evidence or implementation context for an ADR. If the decision changes public architecture, public APIs, integration contracts, or team-level policy, recommend updating the formal ADR or human-facing documentation as well.

## Repository Convention Discovery

Before choosing a trace location or format, inspect the current repository for local conventions. Useful signals include:
- `AGENTS.md`
- `README.md`
- `docs/`
- `adr/`
- `context/`
- `.agents/`
- `.codex/`
- `.manifest/`
- existing decision, finding, trace, architecture, benchmark, eval, or agent-memory directories

Choose placement in this order:

1. If the user explicitly specifies a trace location, use that.
2. Else, if the repository has an existing trace, decision, or findings convention, follow it.
3. Else, if the repository has agent-memory or repo-context conventions, place the trace there.
4. Else, in interactive sessions, ask or propose before creating a new convention.
5. Else, in non-interactive sessions, use a conservative fallback such as `decision-traces/` and record that it was chosen because no local convention was found.

Do not create or enforce repository structures just because they appear in this skill. Never silently create complex directory hierarchies. Examples such as `.manifest/decision-traces/` are local conventions only when the current repository already defines them or the user explicitly requests them.

## Portability Rules

- Do not import examples from another project into this skill.
- Do not mention project-specific classes, services, products, domains, or directories unless they are placeholders or explicitly discovered in the current repo.
- Do not turn one repository's convention into a global rule.
- Prefer placeholders over concrete names in the skill itself.
- Concrete names belong inside generated trace files for the current repository, not inside the reusable skill.
- SkillOpt-oriented metadata must describe reusable task/eval signals without leaking private repository specifics beyond the trace location's privacy boundary.

## Portability Notes

- Specific to the author's current workflow: generated traces are agent-facing project memory and may live in repo-local private or ignored locations.
- Reusable: the worth-recording gate, local convention discovery, privacy redaction, create-vs-update rule, trace-to-validation loop, and SkillOpt-ready extraction block.
- Adapt before reuse: choose the target repository's durable-memory location, language, review policy, version-control rules, benchmark policy, and train/validation/test split rules before writing or committing traces.

## Create vs Update

Update an existing trace when the same decision evolves, implementation status changes, validation results are added, revisit triggers are clarified, or the SkillOpt extraction signal becomes more precise.

Create a new trace when the problem, decision axis, affected surface, or stable constraint is materially different.

Do not create duplicate traces for the same decision just because a later Codex session revisits it. If unsure, search existing traces first and record why a new trace was created.

## Privacy and Redaction

- Do not copy secrets, credentials, tokens, private keys, customer data, or sensitive personal data into traces.
- Summarize sensitive context instead of pasting raw logs, raw payloads, private messages, or confidential excerpts.
- Redact identifiers unless they are necessary for reproducibility.
- Prefer stable technical facts over raw conversation excerpts.
- If a trace location is version-controlled, be especially conservative.
- Do not store raw Codex session transcripts in the trace. Store compact summaries and stable evidence references instead.
- If a future benchmark or SkillOpt task would require private fixtures, mark it as private-only and do not imply it can be published.

## Core Workflow

0. Decide whether a durable trace is warranted.
   Apply the Worth Recording Gate before inspecting placement or writing files. If no trace is warranted, do not continue the trace-writing workflow.

1. Read local truth first.
   Inspect the relevant local context files, code, tests, diffs, logs, and prior trace files before writing. Do not reconstruct the decision only from conversation memory.

   If local evidence is incomplete:
   - state what was inspected
   - state what remains unknown
   - never invent code references
   - never fabricate file paths
   - never claim validation that was not performed

2. Separate facts from interpretation.
   Distinguish:
   - the original issue or review claim
   - the source evidence that confirms or weakens it
   - constraints already present in specs/code
   - constraints clarified by the user
   - the final decision and why it follows from those constraints

3. Preserve the user's follow-up questions.
   User pushback often reveals the real design axis. Record not only the answer, but what the question implied:
   - risk tolerance
   - system semantics
   - operational cost
   - test-vs-business-code boundary
   - whether correctness, recoverability, observability, or simplicity is the priority
   - whether the case exposes a reusable skill failure, eval gap, or benchmark candidate

4. Make the trace actionable.
   The trace must let a future agent implement or continue the work without re-litigating the same decision. Include concrete files, behavior boundaries, rejected alternatives, validation expectations, and current status.

5. Add SkillOpt-ready extraction metadata when the trace can become future skill-improvement data.
   The metadata should be compact, redacted, and machine-readable enough for later mining. It should not replace the human-readable trace.

6. Respect repository privacy and version-control rules.
   If the chosen trace location is ignored, private, or agent-facing, do not stage or commit it unless the user explicitly asks. Mention this distinction when relevant.

## What To Capture

Use these sections by default, adapting names to the project language:

```markdown
# <YYYY-MM-DD> <short decision title>

## 背景

Describe the task, review suggestion, bug report, or implementation question that triggered the trace.

## 问题本身

State the concrete technical problem. Include the failure chain or ambiguity if there is one.

## 问题来源分析

Record where the issue came from:
- user report, review comment, architecture assessment, failing test, production behavior, or local code reading
- exact files/functions/specs involved
- which parts were confirmed, weakened, or disproven by local evidence

## 已明确约束

List constraints that shaped the decision:
- user-facing or system behavior
- architecture boundaries
- repo-local rules
- operational assumptions
- testing principles
- compatibility or migration boundaries

## 用户追问暴露的关注点

Summarize important user follow-ups and what they imply. Do not merely quote the user. Explain the design signal.

Example:
- The user asked whether duplicate work can be discarded. This means the key decision is not generic concurrency correctness, but whether the duplicate operation changes the `<public API contract>` or only wastes resources.
- The user rejected a runtime branch introduced only for test convenience. This makes testability subordinate to preserving the real `<behavior boundary>` or `<system invariant>`.

## 决策过程

Explain the alternatives considered and why each was accepted or rejected.

For each important option, include:
- what it would solve
- cost or complexity
- mismatch with constraints, if rejected
- why the chosen option is the best fit now

## 最终决策

State the decision as an engineering contract that future agents should preserve.

Include:
- required behavior
- prohibited behavior
- invariants to preserve
- conditions that justify revisiting the decision

Write this section to prevent future agents from reintroducing rejected solutions.

## 解决方案

Describe the implementation shape:
- files to change or changed
- expected behavior before/after
- tests or validation to add/run
- local documentation or specs to update

## 当前状态

Record whether this is:
- decision only, not implemented
- implemented but not committed
- committed
- blocked
- needs follow-up

Include validation results if already run.

## 后续边界

Record future triggers that would justify revisiting the decision.

## SkillOpt 数据捕获

```yaml
schema_version: codex_skills.trace.v1
trace_kind: <decision|debugging|review_outcome|implementation_outcome|validation_outcome|architecture_boundary>
source_session:
  raw_transcript_stored: false
  summary_only: true
  privacy_level: <public_safe|repo_private|sensitive_private>
  redaction_notes:
    - <what was summarized or redacted>
candidate_skills:
  - <skill name likely to benefit from this trace, or unknown>
triggering_signal:
  kind: <user_correction|review_claim|bug_hypothesis|failed_validation|architecture_drift|implementation_result|operational_constraint>
  summary: <one-sentence signal>
reusable_lesson: <what future agents should learn>
affected_surfaces:
  - <code/doc/test/config surface or placeholder>
required_behavior:
  - <behavior future agents must preserve>
prohibited_behavior:
  - <behavior future agents must not reintroduce>
validation:
  performed:
    - command_or_check: <exact command/check/review, or none>
      result: <passed|failed|not_run|blocked|manual_confirmed>
  not_performed:
    - <important validation not run and why>
evaluator_signals:
  deterministic_checks:
    - <test/schema/static check/manual reproduction candidate>
  human_review_signals:
    - <user clarification/reviewer outcome, if any>
  llm_judge_allowed: <false|true_with_human_review>
benchmark_candidate:
  usable_as_eval_case: <true|false|needs_fixture>
  suggested_split: <train_candidate|validation_candidate|test_candidate|do_not_use>
  fixture_requirements:
    - <repo state/input files/mocks/data needed to replay>
  success_criteria:
    - <objective check for task success>
  failure_modes_to_test:
    - <regression or bad behavior this case should catch>
```
```

## Small Decision Mode

For small fixes or low-impact decisions, write a compact trace instead of expanding every section. Include only:
- problem
- evidence
- clarified constraint
- final decision
- validation
- revisit trigger
- compact SkillOpt data capture block, only if the trace exposes a reusable skill/eval signal

Use this mode when the decision is narrow, the evidence is simple, and an expanded trace would add noise. When a decision can be captured in fewer than 10 bullets, prefer Small Decision Mode. Do not use it when the decision affects architecture boundaries, user-facing behavior, integration contracts, high-risk correctness, data integrity, migration behavior, evaluation meaning, or cross-surface contracts.

Compact SkillOpt block for Small Decision Mode:

```yaml
skillopt_signal:
  schema_version: codex_skills.trace.v1
  candidate_skills: [<skill or unknown>]
  triggering_signal: <one-line signal>
  reusable_lesson: <one-line lesson>
  validation_gate: <test/check/review that proved or should prove it>
  usable_as_eval_case: <true|false|needs_fixture>
  suggested_split: <train_candidate|validation_candidate|test_candidate|do_not_use>
  privacy_level: <public_safe|repo_private|sensitive_private>
```

## SkillOpt Dataset Capture Rules

SkillOpt-ready metadata is a structured footer for future extraction. It is not itself the dataset.

Use the metadata to make later mining possible:
- `candidate_skills` identifies which skill might learn from the trace, such as `diagnose`, `tdd`, `architecture-review`, `database-access-audit`, or `decision-trace-writer`.
- `triggering_signal` records what made the trace useful: user correction, review finding, failed validation, architecture drift, implementation result, or operational constraint.
- `required_behavior` and `prohibited_behavior` become candidate instructions or regression assertions.
- `validation.performed` records what actually ran. Never upgrade planned validation into performed validation.
- `evaluator_signals` describes how a future eval could judge success. Prefer deterministic checks over LLM judging.
- `benchmark_candidate.usable_as_eval_case` should be `true` only when the trace contains enough replayable evidence to build a task item.
- `suggested_split` is only a suggestion. Default to `train_candidate` unless a human deliberately curates the case for validation or test.
- `test_candidate` should be rare. Do not assign a case to test just because it is high quality; held-out test cases must be curated and protected from repeated optimizer exposure.
- `fixture_requirements` should say what must exist to replay the case: repo snapshot, branch, failing test, input file, mock API, local data fixture, or manual reproduction steps.

Do not let SkillOpt metadata corrupt trace quality:
- Do not add fake precision to make a trace look benchmark-ready.
- Do not create raw transcript archives.
- Do not copy private production data into fixtures.
- Do not make every trace an eval case. Some traces are only agent memory.
- Do not mark a case as objective if it depends only on subjective preference or unverified reasoning.
- Do not make an optimizer-facing lesson stronger than the evidence supports.

## Quality Bar

A good trace is specific enough that a future agent can answer:

- What exact problem were we solving?
- What did the code/spec prove?
- What did the user clarify?
- Why did we choose this solution instead of the obvious alternative?
- What behavior must not be reintroduced?
- What tests or validation define success?
- What remains unresolved?
- Which skill, if any, could learn from this trace?
- Could this become a deterministic eval case, or is it only agent memory?

Avoid generic summaries like "we decided to improve reliability." Write the concrete contract: "`<affected behavior>` must preserve the existing `<behavior boundary>`; validation should use a fake, fixture, harness, benchmark, or review path that respects that boundary instead of adding a runtime-only bypass."

For SkillOpt metadata, avoid vague labels like "good for training." Write the extraction signal: "This case can become a `diagnose` eval because the future agent must reproduce before fixing, add a regression check, and avoid reintroducing `<bad behavior>`; success can be checked by `<test command>` and absence of `<forbidden diff/log/config>`."

## Trace -> Task -> Validation -> Skill Loop

Use traces as structured improvement artifacts, not passive documentation. The reusable self-improvement loop is:

1. Signal or correction.
   A user correction, operational trace, review trace, debugging trace, implementation trace, or validation evidence identifies a possible improvement.

2. Structured evidence.
   Local evidence separates actionable findings from expected behavior, noise, or unresolved investigation.

3. Reviewed finding.
   The evidence becomes a stable finding after the user, reviewer, tests, or repository facts clarify the constraint.

4. Scoped task.
   The finding becomes a bounded Codex task with the relevant repo surface, prior trace, local conventions, and explicit success condition.

5. Implementation.
   Codex changes only the scoped `<affected surface>` and preserves the trace's required behavior, prohibited behavior, and invariants.

6. Validation or eval.
   Validate with the mechanism appropriate for the repository and affected surface. Validation may be automated tests, evals, type checks, build checks, manual reproduction, benchmark comparison, migration dry-run, preview inspection, documentation review, or reviewer confirmation. State exactly which validation was performed and which validation was not performed. If validation is skipped or blocked, record that honestly.

7. Dataset extraction.
   If the trace has enough replayable signal, convert it later into a task item, fixture requirement, expected behavior, and evaluator signal. Keep this extraction separate from the trace file unless the repository has an explicit benchmark convention.

8. Skill update.
   Use the extracted pattern to propose a bounded skill edit. Accept the edit only if it improves or preserves the relevant validation gate.

9. Updated durable trace.
   After implementation, validation, or a changed decision, update the trace with current status, validation results, any new revisit triggers, and any changed SkillOpt metadata.

Apply the same idea locally:
- user correction or review finding becomes the signal
- the chosen `<trace directory>` preserves evidence and decision context
- `<validation mechanism>` or repository-appropriate checks become the validation gate
- SkillOpt metadata preserves the future extraction interface
- ambiguous product choices route back to the user instead of being forced into code or training data

The trace is useful only when it can become input to a scoped future task with validation gates. If it cannot guide future work, validation, or skill improvement, prefer a shorter note or no durable trace.

## Trace Placement

Prefer the repository's existing durable-memory convention. If no convention exists, ask or propose in interactive sessions. In non-interactive sessions, use a simple local directory such as `decision-traces/` and record that no convention was found. Never silently create complex directory hierarchies.

Example paths:

```text
<trace directory>/YYYY-MM-DD_HHmm_<decision_slug>_trace.md
decision-traces/YYYY-MM-DD_HHmm_<decision_slug>_trace.md
```

Preserve hour and minute in new trace filenames to avoid same-day collisions and keep chronological order clear. Use a focused slug based on the decision. Mention `.manifest/decision-traces/` only when the current repository already uses it or the user asks for it.

## Before Finishing

Verify:
- the trace file exists and is readable
- the trace includes user clarification, not only assistant reasoning
- code/spec/test references are concrete
- current status matches reality
- ignored files are not accidentally staged
- SkillOpt metadata, if present, is compact, parseable, redacted, and does not claim validation that was not performed
- `suggested_split` is conservative and does not treat ordinary session-derived data as held-out test data without curation
