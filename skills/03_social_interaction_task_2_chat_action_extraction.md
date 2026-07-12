---
name: chat-action-item-extraction
description: Use when pulling actionable to-dos out of a noisy chat inbox. Focuses on separating real obligations from noise, tracking superseded deadlines, inferring implicit due dates, and respecting read-only boundaries.
---

# Chat Message Action Item Extraction

## Core Challenge

A chat backlog contains genuine commitments, outdated duplicates, and pure noise (newsletters, spam, announcements) interleaved together. The difficulty is pragmatically inferring what actually obligates the user — including deadlines that were never stated outright but follow from other people's stated plans — while discarding both noise and stale superseded information.

## Solution Strategy

1. **Read every message in full before judging any of them**: Open each message rather than inferring from previews, because the action item (or its deadline) often lives in a reply thread or a later message. Common mistake: triaging from summaries and missing items hidden in message bodies.
2. **Classify each message as obligation, information, or noise**: Obligations have an actor (often the user), a verb, and often a deadline; newsletters, vendor spam, and broadcast announcements do not, even when they use words like "update" or "required." Common mistake: treating any message containing deadline-like words as an action.
3. **Track deadline supersession across the timeline**: When the same task is mentioned with different dates, the latest statement of the deadline is the current one; the earlier date is stale and must not be reported. Common mistake: listing every deadline variant and presenting the old one as current.
4. **Infer implicit deadlines from other people's dependencies**: If someone says "I'll proceed on Wednesday with my best guess unless I hear otherwise," that creates a Tuesday end-of-day deadline for you — even though no one named that date. Common mistake: only capturing explicitly-stated dates and missing deadline-by-inference.
5. **Carry rich detail for each item, not just the headline**: A real action item includes who assigned it, what specifically is needed, the deadline, and any sub-conditions (e.g., a prerequisite or a contact to loop in). Common mistake: extracting the task label but dropping the qualifiers that determine whether it's done right.
6. **Never take write actions during a read-only extraction**: Sending, posting, or replying is out of scope; the task is to surface what the user owes, not to discharge it. Common mistake: "helpfully" replying to someone while compiling the list.

## Decision Points

- **Explicit deadline vs. inferred deadline**: Include both, but mark inferred ones as derived from another person's stated plan so the user understands the reasoning.
- **Updated deadline vs. original**: Always use the most recent statement; if you mention the history, frame the old date explicitly as superseded.
- **Genuine request vs. informational FYI**: Ask whether inaction by the user would let someone down or break a commitment — if not, it is information, not an action.

## Common Failure Patterns

- **Preview triage**: Acting on subject lines / previews without opening messages → missing action items buried in bodies or threads.
- **Noise promotion**: Lifting newsletter "action required" marketing language or vendor outreach into the to-do list → inflating the list with non-obligations.
- **Stale deadline reporting**: Repeating the first-mentioned deadline after it was extended → the user believes they have less time than they do, or loses trust in the list.
- **Implicit-deadline blindness**: Only recording dates someone typed out → missing the hardest, most binding deadlines (the ones other people's schedules impose).
- **Detail stripping**: Recording "do the report" without the risk-assessment and resource-estimate qualifiers → work that technically ticks the box but misses the spec.
- **Scope creep into sending**: Replying or posting during extraction → violating the read-only contract and creating side-effects the user can't review.

## Self-Check Questions

- [ ] Did I open and read the full body of every message, not just previews or summaries?
- [ ] Have I excluded newsletters, vendor spam, and broadcast announcements from the action list?
- [ ] For each task mentioned more than once, am I reporting only the latest (superseding) deadline?
- [ ] Did I look for deadlines implied by other people's stated plans, not just explicitly typed dates?
- [ ] Does each action item include who, what, when, and any sub-conditions or prerequisites?
- [ ] Did I avoid any write/send/post action — this was extraction only?
- [ ] If a task had its scope changed mid-thread, does my item reflect the updated scope (e.g., new sub-deliverables or a different contact)?
