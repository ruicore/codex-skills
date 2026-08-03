# TraceGym Metadata For Decision Traces

Read this reference only when a stable trace has reusable workflow, skill-improvement, benchmark, evaluator, or proposal value. The metadata is a structured footer for possible later sanitized derivation; it is not a dataset, sanitized artifact, benchmark item, evaluator, or skill proposal.

## Full Metadata Block

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
```

## Compact Block

Use this only with Small Decision Mode:

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
```

## Field Rules

- Set `trace_privacy_class` explicitly to `local_raw_trace`, `sanitized_trace_seed`, or `public_benchmark_candidate` without collapsing those asset layers.
- Set `public_export_candidate: true` only when the sanitization notes explain how a public-safe derivative could be created from the raw trace.
- Use `candidate_workflow_skills` for the skill that might learn from the case, not automatically for `decision-trace-writer` and not as the primary skill label when another workflow owns the lesson.
- Write `reusable_workflow_lesson` as the lesson that remains after expected redaction, not as a private-project-only fact.
- Use `sensitive_surfaces` and `public_sanitization_required` to name what must be removed, generalized, or replaced.
- Use `ready_after_sanitization` only when replayable evidence is sufficient to construct a task item.
- Prefer deterministic checks for `evaluator_signals`; keep `llm_judge_allowed: false` unless a separately governed downstream workflow changes that policy.
- Use `update_existing_skill`, `new_skill_candidate`, or `no_skill_change` as a signal only. Base `proposal_strength` on evidence quality and repeatability, and record evidence still needed before any skill change.
- Record actual validation honestly. Never upgrade planned, skipped, or blocked validation into performed validation.

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
