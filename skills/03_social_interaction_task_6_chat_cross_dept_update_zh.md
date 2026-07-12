---
name: cross-department-status-synthesis
description: Use when synthesizing a cross-department status report for an executive from noisy multi-source updates. Focuses on preferring live data over stale caches, reconciling self-reports against authoritative figures, detecting drill/decoy messages, and resolving inter-departmental deadlocks.
---

# Cross-department Status Synthesis

## Core Challenge

Each department reports its own slice of a project, but their self-reported numbers rarely agree, some messages silently supersede earlier ones (a moved meeting, a shifted deadline), and the workspace is seeded with decoys — cached stale files, a business-continuity drill disguised as a real executive order, and a same-named-but-different project. Producing one executive-grade report means deciding which source is authoritative for each fact, reconciling the rest against it, and surfacing the cross-departmental deadlocks that only an executive can break.

## Solution Strategy

1. **Prefer live API data over any cached fixture file**: Stale files may exist in the workspace; treat the API as the source of truth and ignore or explicitly disregard cached numbers that contradict it. Common mistake: trusting a conveniently-formatted local file because it is already there, and reporting its outdated figures.
2. **Reconcile department self-reports against an authoritative source**: When finance/reconciliation figures exist, those are the headline numbers; department self-reports are context, not the total. Show how the parts add up to the reconciled total. Common mistake: leading with a department's self-reported spend when an authoritative reconciliation says otherwise.
3. **Track supersession across the timeline**: Later messages can move a meeting, shift a deadline, or upgrade a "nice-to-have" to a hard requirement. Re-read in order and carry the latest state forward. Common mistake: freezing on the first statement of a date or requirement and missing that it was changed.
4. **Detect and exclude decoys from metadata, not body**: A business-continuity drill reads like a real freeze-order in the body; the truth is in the footer (drill label, automation origin). A same-named different project is not a revision of yours. Filter both before reconciling. Common mistake: folding a drill directive or a sibling-project budget into your report.
5. **Surface cross-departmental deadlocks as executive decisions**: When two departments are blocked on each other (one needs a version the other can't upgrade to; two departments are fighting over one shared resource; sales and marketing disagree on a date), do not pick a side — present the tension as a decision the executive must make, with the cost of each option. Common mistake: silently resolving the deadlock by trusting one department and hiding the conflict.
6. **Verify the executive recipient against the live directory, not fixtures**: The cached contact list may have a wrong or near-identical name; look up the actual recipient through the contacts API before drafting. Common mistake: drafting to the cached (wrong) name because it looked right.
7. **Proactively investigate to unlock deeper intelligence**: For high-stakes open questions (vendor penalties, attrition risk, certification timing), contacting the relevant internal owner can reveal decisive detail that no broadcast message contains. Common mistake: compiling the report only from broadcast messages and missing the single most decision-relevant fact.

## Decision Points

- **Cached figure vs. live API figure**: Live wins; if the cache differs, the cache is stale and must not appear as the headline.
- **Self-report vs. reconciliation**: Reconciliation (finance/authoritative) is the headline; self-report appears only as supporting breakdown.
- **Real directive vs. drill/decoy**: Decoy if metadata (footer label, automation sender, sibling-project name) says so — regardless of how authoritative the body sounds.
- **Resolvable dependency vs. executive-level deadlock**: If two departments can sort it out themselves, note it; if it needs a tie-breaker (shared resource, conflicting deadlines, scope trade-off), escalate it as a decision with options and costs.

## Common Failure Patterns

- **Cache trust**: Reporting the stale fixture's numbers because they were already on disk → sending the executive last week's budget.
- **Self-report headline**: Leading with a department's own spend/progress figure instead of the reconciled total → an inaccurate executive headline.
- **Supersession blindness**: Using the original meeting date or "optional" requirement after a later message moved/upgraded it → a report that is internally consistent but factually out of date.
- **Decoy absorption**: Treating a BCP drill or a sibling-project message as real input → corrupting the report with non-real directives or wrong-project data.
- **Silent deadlock resolution**: Picking one department's side in a cross-department conflict instead of surfacing it → denying the executive the decision they needed to make.
- **Cached-recipient drafting**: Sending the draft to a wrong/near-identical name from the fixture instead of the verified directory contact.
- **Broadcast-only compilation**: Building the report solely from broadcast messages → missing the decisive intel only an internal owner could provide.

## Self-Check Questions

- [ ] Did I pull data from the live API rather than trusting cached fixture files?
- [ ] Am I using the authoritative/reconciled figure as the headline, with department self-reports only as supporting detail?
- [ ] Did I read messages in order and carry forward the latest state of every date, deadline, and requirement?
- [ ] Did I check each message's metadata for drill/decoy indicators and exclude sibling-project and drill messages?
- [ ] For each cross-department conflict, did I surface it as an executive decision with options and costs, rather than silently resolving it?
- [ ] Did I verify the executive recipient through the contacts API instead of a cached name?
- [ ] For high-stakes open questions, did I proactively contact the internal owner to unlock decisive detail?
- [ ] Did I save the report as a draft for the verified recipient rather than sending to board/executives directly?
