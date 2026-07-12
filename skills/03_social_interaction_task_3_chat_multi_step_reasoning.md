---
name: multi-step-chat-feasibility-reasoning
description: Use when assessing feasibility of a deal/proposal from a messy multi-party chat trail. Focuses on reconstructing how requirements evolved, separating hard blockers from workarounds, and flagging governance/authority conflicts and unverified intel.
---

# Multi-step Chat Feasibility Reasoning

## Core Challenge

A high-stakes business question ("can we actually deliver this?") must be answered from a chat trail in which requirements mutate over days, different experts raise different objections, an executive overrides those objections, and some of the "facts" are unverified rumors. Sound reasoning means reconstructing the timeline, separating the truly infeasible from the merely expensive, and refusing to let executive pressure erase compliance blockers.

## Solution Strategy

1. **Reconstruct the requirement timeline before judging feasibility**: Sort every message chronologically and trace how each requirement (scope, deadline, discount, SLA) changed hands and changed value. Common mistake: reading messages independently and treating an early, superseded requirement as still in force.
2. **Separate hard blockers from modifiable items**: A hard blocker cannot be satisfied by any available path (wrong platform, missing approval, impossible timeline); a modifiable item has a workaround at some cost or delay. State each explicitly. Common mistake: lumping everything as "risky" without distinguishing what is genuinely impossible.
3. **Trace every commitment to its approval authority**: For each promise made to a client (discount level, SLA, on-prem, support hours), identify which internal role actually must sign off, and whether that approval has been obtained. Common mistake: treating an executive's verbal "yes" as satisfying a policy that requires written sign-off from a different role.
4. **Cost out the workarounds, including hidden multipliers**: When a middle-tier fix exists (a connector, a phased delivery, an offshore vendor), compute its real cost accounting for scale multipliers (e.g., per-site licensing, dual regions) and prerequisites (security review, pilot data). Common mistake: quoting the single-site or best-case price while ignoring the doubling the architecture requires.
5. **Label intel confidence and refuse to launder rumors**: Competitive tips, vendor reliability hearsay, and second-hand claims must be marked unverified and never presented as established fact. Common mistake: repeating a rumor as a data point to strengthen the recommendation.
6. **Call out governance risk when an executive overrides experts**: When a leader demands expedited review or claims authority to waive a process, name the residual risks that the expedited path leaves unchecked, and require written acknowledgment. Common mistake: silently complying with the override and burying the unreviewed risks.

## Decision Points

- **"Not feasible as-is" vs. "feasible if modified"**: Lead with the as-is verdict (usually infeasible), then enumerate the specific modifications (phasing, alternative tech, reduced scope, delayed dates) that would make it feasible, each with its cost.
- **Executive verbal authorization vs. written policy**: When they conflict, the policy governs; surface the gap as a deadlock with named options (delay, reduce scope, escalate for exception) rather than picking one silently.
- **Verified technical fact vs. unverified competitive rumor**: Present the former as constraint, the latter as context-with-uncertainty, never blended.

## Common Failure Patterns

- **Timeline flattening**: Treating the final message as the only state, or the first as canonical → missing how the deal shifted and which version each stakeholder believes.
- **Blocker dilution**: Listing every concern as an equal "risk" → hiding the one item that makes the deal impossible no matter the money.
- **Approval laundering**: Accepting an executive override as satisfying a written-approval or sign-off requirement → building a proposal that is non-compliant on its face.
- **Best-case costing**: Quoting a workaround at single-site / single-instance price → understating cost by the architecture's real multiplier.
- **Rumor laundering**: Repeating unverified competitive intel as fact → distorting the recommendation and creating liability.
- **Pressure compliance**: Softening or omitting blockers because an executive said to proceed → producing a feasibility report that is not actually a feasibility report.

## Self-Check Questions

- [ ] Did I sort the messages chronologically and trace how each requirement changed value and owner?
- [ ] Have I explicitly distinguished hard blockers (no path exists) from modifiable items (path exists at a cost)?
- [ ] For each client-facing commitment, did I identify the role that must approve it and whether that approval is in hand?
- [ ] Did I flag any case where an executive's verbal authorization does not satisfy a written/policy requirement?
- [ ] Have I costed each workaround at its real scale (per-site, per-region, with prerequisites), not the headline price?
- [ ] Did I label every piece of competitive/vendor intel with its confidence level, and avoid presenting rumors as fact?
- [ ] Does my assessment state plainly whether the proposal is feasible as-is, and if not, what specifically would need to change?
- [ ] Did I avoid sending any outgoing messages — this was analysis only?
