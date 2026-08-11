# TraceGym Metadata For Decision Traces

Read this reference only when a stable trace has reusable workflow, skill-improvement, benchmark, evaluator, or proposal value. The metadata is a structured footer for possible later sanitized derivation; it is not a dataset, sanitized artifact, benchmark item, evaluator, or skill proposal.

## Contents

- [Footer Contract](#footer-contract)
- [Full Metadata Footer](#full-metadata-footer)
- [Compact Metadata Footer](#compact-metadata-footer)
- [Field Rules](#field-rules)
- [Quality And Derivation Boundaries](#quality-and-derivation-boundaries)
- [Improvement Loop Catalog](#improvement-loop-catalog)

## Footer Contract

Include TraceGym metadata only when the conditional gate in `SKILL.md` passes.
When included, append exactly one final section with this shape:

````markdown
## TraceGym Metadata
```yaml
tracegym_metadata:
  ...
```
````

The heading must be exactly `## TraceGym Metadata`. It must be followed immediately by a YAML fence whose opening line is exactly three backticks followed by `yaml`, and that fence must begin with `tracegym_metadata:`. After its closing fence, the trace must contain no non-whitespace content. When `skill_application_evidence` is present, make it the final metadata field. Do not place a second metadata heading, an earlier metadata-looking example, or prose after this footer. If the conditional gate fails, omit the footer altogether.

The templates below show the complete body of that final footer. They are instructional templates in this reference, not metadata attached to this reference.

## Full Metadata Footer

````markdown
## TraceGym Metadata
```yaml
tracegym_metadata:
  schema_version: tracegym.trace.v1
  trace_privacy_class: local_raw_trace
  public_export_candidate: false
  source_capture_skill: decision-trace-writer
  candidate_workflow_skills:
    - <skill-name-or-unknown>
  reusable_workflow_lesson: <one-sentence reusable lesson after redaction>
  sensitive_surfaces:
    - <repo_paths|private_links|customer_data|production_payloads|credentials|none>
  public_sanitization_required:
    required: true
    notes:
      - <what must be removed, generalized, or replaced with a synthetic fixture>
  eval_case_readiness:
    status: <not_candidate|needs_synthetic_fixture|ready_after_sanitization|private_only>
    fixture_strategy: <synthetic_fixture|repo_snapshot|manual_replay|not_applicable>
    objective_success_criteria:
      - <deterministic check or observable success condition>
  evaluator_signals:
    deterministic_checks:
      - <test, schema check, static check, replay, or manual verification candidate>
    human_review_signals:
      - <user clarification or reviewer decision, if any>
    llm_judge_allowed: false
  monthly_skill_proposal_signal:
    action: <update_existing_skill|new_skill_candidate|no_skill_change>
    proposal_strength: <none|weak|medium|strong>
    evidence_needed_before_proposal:
      - <additional traces, validation, or counterexamples needed>
  skill_application_evidence:
    - skill_name: <skill-name>
      role: <primary|supporting|capture|unknown>
      trigger_source: <user_explicit|request_match|repository_rule|agent_selection|workflow_handoff|unknown>
      application_status: <loaded_only|applied|partially_applied|loaded_not_applied|referenced_not_loaded|corrected|misrouted|requested_unavailable|unknown>
      task_outcome: <success|partial|failure|blocked|unknown>
      validation_strength: <none|weak|medium|strong>
      contribution_classification: <supported|corrected|neutral|unknown>
      artifact_sha256: <lowercase-sha256-or-null>
      human_reviewed: <true|false>
```
````

## Compact Metadata Footer

Use this only with Small Decision Mode:

````markdown
## TraceGym Metadata
```yaml
tracegym_metadata:
  schema_version: tracegym.trace.v1
  trace_privacy_class: local_raw_trace
  public_export_candidate: false
  source_capture_skill: decision-trace-writer
  candidate_workflow_skills: [<skill-or-unknown>]
  reusable_workflow_lesson: <one-line lesson>
  sensitive_surfaces: [<repo_paths|private_links|production_payloads|credentials|none>]
  public_sanitization_required:
    required: true
    notes: [<one-line sanitization boundary>]
  eval_case_readiness:
    status: <not_candidate|needs_synthetic_fixture|ready_after_sanitization|private_only>
  evaluator_signals:
    deterministic_checks: [<test/check/review gate>]
    human_review_signals: [<user/reviewer signal or none>]
    llm_judge_allowed: false
  monthly_skill_proposal_signal:
    action: <update_existing_skill|new_skill_candidate|no_skill_change>
    proposal_strength: <none|weak|medium|strong>
    evidence_needed_before_proposal: [<additional evidence or none>]
  skill_application_evidence:
    - skill_name: <skill-name>
      role: <primary|supporting|capture|unknown>
      trigger_source: <user_explicit|request_match|repository_rule|agent_selection|workflow_handoff|unknown>
      application_status: <loaded_only|applied|partially_applied|loaded_not_applied|referenced_not_loaded|corrected|misrouted|requested_unavailable|unknown>
      task_outcome: <success|partial|failure|blocked|unknown>
      validation_strength: <none|weak|medium|strong>
      contribution_classification: <supported|corrected|neutral|unknown>
      artifact_sha256: null
      human_reviewed: <true|false>
```
````

## Field Rules

- Set `trace_privacy_class` explicitly to `local_raw_trace`, `sanitized_trace_seed`, or `public_benchmark_candidate` without collapsing those asset layers.
- Set `public_export_candidate: true` only when the sanitization notes explain how a public-safe derivative could be created from the raw trace.
- Use `candidate_workflow_skills` for the skill that might learn from the case, not automatically for `decision-trace-writer` and not as the primary skill label when another workflow owns the lesson.
- Omit `skill_application_evidence` when no application evidence was observed. Do not infer it from `candidate_workflow_skills`, and do not add a skill merely because it could have helped.
- Treat each array item as the canonical skill-application entry. Keep these exact field names and enums in any downstream envelope; add evidence hashes, privacy, source, or collection time outside the entry rather than translating its semantics.
- Use one `skill_application_evidence` entry per observed skill. Set `skill_name` to the registered skill identifier. Set `role` to `primary` for the workflow that owned the task result, `supporting` for a materially used secondary workflow, `capture` for a post-result persistence workflow such as this skill, or `unknown` when unverified.
- Set `trigger_source` to why the skill entered the workflow: `user_explicit`, `request_match`, `repository_rule`, `agent_selection`, `workflow_handoff`, or `unknown`. Evidence collection such as observing a `SKILL.md` read is not a trigger, and a skill inventory is not proof that the skill entered the workflow.
- Set `application_status` to `loaded_only`, `applied`, `partially_applied`, `loaded_not_applied`, `referenced_not_loaded`, `corrected`, `misrouted`, `requested_unavailable`, or `unknown`. Use `loaded_not_applied` when instructions were read but not used, `referenced_not_loaded` only when a named skill was not read, and `requested_unavailable` only when the requested registered workflow could not be loaded.
- Set `task_outcome` to `success`, `partial`, `failure`, `blocked`, or `unknown` for the same task represented by the entry. Do not borrow an outcome from another application record.
- Set `validation_strength` to `none`, `weak`, `medium`, or `strong` based on performed validation relevant to the task result. This grades the supporting evidence, not the inherent quality of the skill.
- Set `contribution_classification` to `supported` when evidence supports the skill-guided behavior, `corrected` when the guidance or routing was materially corrected, `neutral` when use did not distinguish its effect, or `unknown` when evidence is insufficient. Never turn this classification into a causal percentage, ranking, or maturity change.
- Set `artifact_sha256` to a lowercase SHA-256 only when a stable, permitted artifact was actually hashed; otherwise set it to `null`. A hash does not make private material public-safe or prove causation.
- Set `human_reviewed: true` only after a human reviewed this exact entry's application, outcome, validation, and contribution claims. Keep it `false` for automatic collection. An automatic `loaded_only` entry must also use `role: unknown`, `trigger_source: unknown`, `task_outcome: unknown`, `validation_strength: none`, `contribution_classification: unknown`, and cannot influence maturity recommendations.
- Write `reusable_workflow_lesson` as the lesson that remains after expected redaction, not as a private-project-only fact.
- Use `sensitive_surfaces` and `public_sanitization_required` to name what must be removed, generalized, or replaced.
- Use `ready_after_sanitization` only when replayable evidence is sufficient to construct a task item.
- Prefer deterministic checks for `evaluator_signals`; keep `llm_judge_allowed: false` unless a separately governed downstream workflow changes that policy.
- Use `update_existing_skill`, `new_skill_candidate`, or `no_skill_change` as a signal only. Base `proposal_strength` on evidence quality and repeatability, and record evidence still needed before any skill change.
- Record actual validation honestly. Never upgrade planned, skipped, or blocked validation into performed validation.

`skill_application_evidence` is reusable metadata only. It is not required in ordinary decision traces, and this skill does not aggregate it, score skills, calculate maturity, or update a registry. Any later aggregation or maturity recommendation belongs to a separately governed workflow and must preserve the distinction between observed application, validation strength, and contribution classification.

## Quality And Derivation Boundaries

Do not add false precision to make a trace appear benchmark-ready, archive raw transcripts, copy private production data into fixtures, turn every trace into an eval case, label subjective or unverified reasoning objective, or make the reusable lesson stronger than the evidence.

A separate later workflow may derive a sanitized task, fixture strategy, expected behavior, evaluator signal, or bounded skill proposal from reviewed traces. Keep that derivation separate from trace writing even when metadata makes it easier. This skill does not scan trace directories, sanitize artifacts, build benchmarks, generate datasets, train models, construct evaluators, or create and approve skill proposals.

## Improvement Loop Catalog

Use this catalog only to classify a reusable trace signal:

1. A user correction, operational trace, review finding, debugging result, implementation result, or validation evidence creates a signal.
2. Repository evidence separates an actionable stable finding from expected behavior, noise, or unresolved investigation.
3. User, reviewer, test, or repository evidence settles the relevant constraint.
4. A later task can use the trace as bounded context with an explicit success condition.
5. Implementation changes only the scoped surface while preserving the recorded contract.
6. Repository-appropriate validation records exactly what ran and what did not.
7. A separate workflow may derive a sanitized task and synthetic or replayable fixture.
8. Repeated reviewed evidence may later justify a bounded skill update or proposal.
9. Implementation, validation, or a changed decision updates the durable trace and its metadata.

If the trace cannot guide a future scoped task, validation gate, or skill improvement, prefer purely local memory without metadata, a shorter note, or no durable trace.
