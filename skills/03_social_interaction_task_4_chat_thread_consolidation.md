---
name: chat-thread-consolidation
description: Use when consolidating a messy message thread into one accurate client-facing status report. Focuses on tracking multi-hop correction chains, reconciling contradictions, computing cascading critical-path impact, and drafting (not sending).
---

# Chat Message Thread Consolidation with Contradiction Detection

## Core Challenge

Producing one accurate status report from a thread where the same metric (progress %, date, budget) was stated, then "corrected," then corrected again — and where some of those "corrections" are themselves still wrong, as a later authority explicitly points out. The harder twist: a late-breaking finding can introduce a brand-new dependency that ripples through the critical path, so the final number is not just "the latest value" but a recomputed chain.

## Solution Strategy

1. **Read every relevant message before settling any number**: Open each message in scope; do not consolidate from previews. A correction, its refutation, or a new dependency can sit in any message. Common mistake: taking the most recent message per metric as canonical and missing that it was rebutted elsewhere.
2. **Build a correction chain per metric, not just the latest value**: For each disputed figure, lay out the full sequence (A said x → A "corrected" to y → B said z, noting A's y is still wrong). The chain reveals which value is actually authoritative. Common mistake: collapsing to "latest = correct" when an intermediate correction was explicitly rebutted.
3. **Weight source reliability, not recency**: When two people disagree, who has ground truth (the implementer, the QA lead, the finance reconciliation) outranks who spoke last. Note explicitly when a "correction" was issued by someone who lacks the authoritative view. Common mistake: treating every correction as equally credible.
4. **Recompute the critical path when a new dependency appears**: A late finding (e.g., a security bug) can add work and create a new blocking edge (e.g., a downstream team must update after the fix). Recompute the end-to-end timeline from scratch rather than adding the delay in isolation. Common mistake: adding the fix duration but missing the cascading downstream task it triggers.
5. **Scope-filter aggressively before reconciling**: Exclude messages about other projects, other teams, or unrelated topics before you start reconciling, so cross-project numbers don't pollute the report. Common mistake: pulling in a same-format message that concerns a different project and reconciling it as if it were a revision.
6. **Save as draft, never send, when the output is for review**: A client-facing report that the user wants to review must be staged as a draft; sending it directly bypasses the review gate. Common mistake: calling send because the report looks finished.

## Decision Points

- **Intermediate "correction" that a later authoritative source calls wrong**: Drop the intermediate as a value, but preserve it in the chain narrative so the reader understands why the final number is trusted.
- **Budget figure from self-report vs. from reconciliation**: Use the reconciled (finance/authoritative) figure as the headline; show how the parts add up rather than presenting the department's self-reported total.
- **Deadline already missed vs. missed by more after the new dependency**: State the new miss magnitude plainly (it grew), and pair it with concrete decision options (extension, cut scope, add resources) rather than just flagging risk.

## Common Failure Patterns

- **Latest-wins collapse**: Taking the most recent statement of each metric as the truth → reporting a value that was explicitly rebutted.
- **Correction-as-truth**: Treating anyone's "correction" as authoritative without checking whether a more reliable source overrode it → propagating a still-wrong number to the client.
- **Isolated delay addition**: Adding a fix's duration to the timeline but ignoring the new downstream edge it creates → understating the slippage.
- **Cross-project contamination**: Reconciling a same-shaped message from a different project into this report → corrupting the numbers.
- **Premature send**: Mailing the report directly instead of saving as draft → stripping the human review gate from a client-bound communication.
- **Self-report over reconciliation**: Leading with the department's own budget/progress number instead of the reconciled figure → sending the client an inaccurate headline.

## Self-Check Questions

- [ ] Did I open and read every in-scope message, excluding out-of-scope (other-project) ones?
- [ ] For each disputed metric, have I laid out the full correction chain rather than just the latest value?
- [ ] Did I note explicitly when an intermediate "correction" was itself rebutted by an authoritative source?
- [ ] Am I using the reconciled/authoritative figure (not a department self-report) as the headline number?
- [ ] When a late finding added work, did I recompute the entire critical path including any new downstream dependency it created?
- [ ] Did I quantify how much the deadline is missed by, and is that number current (after the new dependency)?
- [ ] Did I present concrete decision options tied to the slippage?
- [ ] Did I save the report as a draft rather than sending it?
