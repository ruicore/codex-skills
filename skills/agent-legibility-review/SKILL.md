---
name: agent-legibility-review
description: Review how easily a future coding agent can find the right edit points, recognize authoritative sources, and discover constraints and downstream effects. Use for an explicit agent-legibility or agent-navigability review, rather than ordinary code review.
---

# Agent Legibility Review

Assess whether a future agent can make a realistic requested change without
choosing the wrong edit point, trusting the wrong source, or missing a related
obligation. Keep recommendations proportionate to that risk.

Start from the user's tasks or choose a few representative changes when the
request is broad. Follow the repository's actual navigation aids and tooling.
Choose the investigation depth and order that fit the task; a repository-wide
inventory is useful only when it helps answer the question.

Useful questions, where relevant:

- Can the agent find the implementation and the place that actually owns the rule?
- Are editable sources distinguishable from generated output, adapters, and
  historical guidance?
- Can the agent discover configuration precedence, cross-file contracts, and
  downstream consumers before making the change?
- Do nearby tests, names, docs, or navigation tools expose the necessary context?

A useful finding connects repository evidence to a specific likely mistake and
its consequence. Before reporting it, check whether an existing entry point,
test, convention, or tool already resolves the apparent ambiguity. Keep a
possible trap distinct from an observed failure. Length, indirection, repeated
representations, or missing prose alone do not establish a problem.

Prefer the smallest improvement that would prevent the mistake. A pointer, a
test, or a clearer source relationship may be enough; structural changes need
a concrete benefit. If a question requires a new architectural decision, explain
the tradeoff rather than turning the review into an unsolicited redesign.

Present actionable findings with their locations, likely mistakes, supporting
evidence, and proportionate fixes. Mention consequential uncertainty and the
scope actually inspected. Adapt the format to the findings: scores, category
coverage, and a fixed number of issues are unnecessary. No findings is a valid
result. Keep a review read-only unless implementation is requested.

## Source and License

Created by Ray Carter (ruicore). Free and open source under Apache-2.0.

- Source: https://github.com/ruicore/codex-skills/tree/main/skills/agent-legibility-review
- License: [Apache-2.0](LICENSE), included with this skill directory.
