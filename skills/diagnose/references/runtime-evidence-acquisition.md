# Runtime Evidence Acquisition

Use this protocol to establish what the current runtime actually did before
promoting a code-level explanation into a runtime conclusion. Apply it in both
Full and Bounded Diagnosis Mode; it does not grant mutation authority.

## 1. Fix the authority boundary

Write down two sets before collecting evidence:

- **Allowed observations:** the environments, time ranges, records, endpoints,
  processes, and stores the user authorized for read-only inspection.
- **Mutations requiring separate authority:** restarts, request replays, state
  changes, traffic changes, new logs or probes, debugger attachment, database
  writes, deployments, and configuration changes.

Prefer an already available read-only sensor. Do not turn missing visibility
into permission to instrument or exercise a production system. In Bounded
Diagnosis Mode, stop at a verification plan when the next discriminating probe
would cross the boundary.

## 2. Inventory sensors by question

Select the smallest sensor set that can distinguish the active hypotheses.
Never log everything and search later.

| Question | Possible authorized sensors |
| --- | --- |
| What is running and accepting traffic? | process/service inventory, PID, executable/command, listening port/socket, load-balancer or service routing state |
| What was deployed and loaded? | build/commit/version endpoint, image or package digest, startup record, redacted config fingerprint |
| What happened for this operation? | targeted application/access log, browser console/network or HAR, `run_id`, `request_id`, `trace_id` |
| What persisted or crossed a boundary? | read-only database/audit query, queue metadata, provider request/callback record |
| Which workload emitted the evidence? | container/pod/task identity, orchestrator state/logs, host, PID, instance label |
| Where was time spent or failure introduced? | trace span, metric/profile already available, timestamped boundary records |

Record a sensor as absent instead of silently substituting a weaker source.
Code, tests, configuration, and deployment manifests describe possible or
intended behavior; they do not prove which running instance handled an event.

## 3. Bind evidence to a runtime identity

Capture an identity tuple from the strongest available sources:

```text
environment/host or workload
PID, container, pod, task, or process identity
start_time
executable/command and listening endpoint
build, commit, image, package, or version
redacted config fingerprint
```

Use `unknown` for fields that cannot be observed. Do not copy secrets into a
fingerprint: canonicalize the relevant non-secret configuration or hash a
sanitized representation. A filename, repository checkout, expected image tag,
or human statement about a restart is not a runtime identity by itself.

For a claimed restart, compare the before/after PID or workload identity and
`start_time`, then check the listener or routing target. Verify that no old or
zombie process still owns the port and that the expected build/config identity
belongs to the replacement. If those checks are impossible, preserve the
restart as a claim rather than an observation.

## 4. Correlate and check freshness

Define the time window and time zone before joining artifacts. Prefer explicit
offsets or UTC, while preserving the source time zone when conversion could be
ambiguous.

Join evidence using the strongest available keys in this order:

1. `trace_id` and span identity;
2. `request_id`, operation ID, or provider correlation ID;
3. `run_id`, job ID, transaction ID, or a synthetic test marker;
4. a bounded timestamp, route, instance identity, and non-sensitive request
   attributes when no correlation ID exists.

Do not merge records solely because their messages look similar. For every log,
trace, metric, or query result, check collection time, event time, instance
identity, file rotation or retention boundary, and whether the source is still
current. Label old logs, superseded instances, cached responses, and pre-restart
records as stale instead of mixing them into current-instance evidence.

## 5. Preserve the minimal redacted evidence bundle

Keep only what another agent needs to reproduce the reasoning:

```text
question or hypothesis being tested
authority and environment boundary
time window and time zone
runtime identity tuple
sensor/source and collection time
correlation identifiers, redacted where needed
minimal observation or aggregate
artifact path or content hash for larger evidence
redactions applied
visibility gaps and next discriminating evidence
```

Use hashes or bounded extracts for large artifacts. Remove credentials, tokens,
cookies, personal data, raw customer payloads, and unrelated records. State the
provenance of each observation; do not imply that generated summaries are raw
runtime evidence.

## 6. Classify visibility gaps

Assign exactly one primary class to each missing material observation:

- `unavailable`: the environment does not expose or retain the evidence.
- `unauthorized`: the evidence may exist, but current user authority does not
  permit access or collection.
- `unsupported`: current tools cannot safely collect, decode, or correlate the
  evidence even though the environment and authority may allow it.

For each gap, name the blocked conclusion, the minimum next artifact or probe,
and whether it would require more access, a new tool, or a mutation. Keep the
conclusion at hypothesis level until the gap is resolved; never convert a
visibility gap into fabricated runtime certainty.
