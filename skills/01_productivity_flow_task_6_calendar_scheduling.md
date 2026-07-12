---
name: 01-productivity-flow-task-6-calendar-scheduling
description: Use when scheduling prioritized meeting requests against an existing calendar under hard constraints (availability, caps, blocked windows) and soft preferences. Focuses on hard-constraint absolutism, priority-weighted optimization over greedy assignment, and schedule/reject consistency.
---

# Constraint-Satisfying Meeting Scheduling with Priority Optimization

## Core Challenge

The core difficulty is that hard constraints are absolute — a single violation zeros the entire result — while the optimization layer (maximizing total scheduled priority weight) rewards global reasoning over greedy slot-filling. Agents fail by treating constraints as soft, by scheduling the first available slot for each request and thereby blocking a higher-priority request later, or by producing a schedule and a rejection list that disagree about what was actually placed. The cascading nature of scheduling decisions (one placement eliminates slots for many others) makes local greedy choices systematically suboptimal.

## Solution Strategy

1. **Treat every hard constraint as a zero-tolerance gate**: Lunch breaks, attendee unavailability windows, daily per-attendee meeting caps, required-attendee presence, preferred-window containment, and no double-booking are all hard; violating any one forfeits the whole submission. Enumerate and check each constraint explicitly per scheduled event. Common mistake: treating the daily cap or lunch break as a soft preference, which zeros the result.
2. **Preserve existing events untouched**: The output calendar must include every original event (matched by summary, time, and attendees); never modify, split, or delete them. Common mistake: rewriting the calendar and dropping or altering original events.
3. **Optimize for total priority weight, not request count**: When not all requests fit, the objective is maximizing the sum of priority weights of scheduled requests; a single high-priority meeting can outweigh several low-priority ones. Common mistake: greedily scheduling as many requests as possible regardless of priority.
4. **Account for shared resources globally before assigning**: Each attendee is a shared resource with a daily cap and an availability calendar; a placement consumes capacity for every required attendee simultaneously. Build the global capacity/availability view first, then assign. Common mistake: per-request local checks that ignore capacity already consumed by earlier assignments.
5. **Keep the schedule and the rejection list strictly consistent**: Every request is either scheduled exactly once or appears exactly once in the rejection list; no request is both, none is neither, and none is double-scheduled. Common mistake: scheduling a meeting but also listing it as unscheduled, or omitting unscheduled requests entirely.
6. **Give each rejection a valid, specific reason**: Rejection reason codes must come from the allowed set, and the reason text should identify the binding constraint (which attendee, which window, which cap). Common mistake: a generic reason code with no explanation, or an invented code outside the allowed set.
7. **Respect duration and window containment exactly**: Each scheduled meeting's duration must equal the requested duration, and (when window-only scheduling is enforced) it must fit entirely inside a preferred window. Common mistake: shortening a meeting to make it fit, which fails the duration check.

## Decision Points

- **Greedy vs optimizer**: For non-trivial batches, prefer a constraint solver or a priority-sorted assignment with backtracking over first-fit greedy; greedy misses global optima when high-priority requests compete for the same slot.
- **Preferred-window flexibility**: Only schedule outside preferred windows if the request explicitly allows flexibility; otherwise window-containment is a hard constraint.
- **Reason-code selection**: Pick the most specific applicable code (e.g., attendee unavailability vs a generic conflict) so the rejection is diagnostic.

## Common Failure Patterns

- **Soft-constraint drift**: Treating a hard constraint as preferential → one violation zeros the whole submission.
- **Greedy slot-filling**: Scheduling requests in arrival order → a low-priority request consumes the only slot a high-priority request could use, lowering the achievable priority weight.
- **Capacity blindness**: Per-request availability checks that ignore the daily cap already consumed → cap violations across the day.
- **Schedule/reject inconsistency**: A request both scheduled and rejected, or missing from both → coverage-consistency check fails and zeros the result.
- **Original-event mutation**: Editing or dropping original events while adding new ones → preservation check fails.
- **Invented reason codes**: Using a free-text reason code not in the allowed set → reason-code validity fails.

## Self-Check Questions

- [ ] Did I enumerate and explicitly check every hard constraint for each scheduled event?
- [ ] Does the output calendar preserve every original event byte-for-byte conceptually (summary, times, attendees)?
- [ ] Did I optimize for total scheduled priority weight rather than request count?
- [ ] Did I build a global capacity/availability view before assigning any meeting?
- [ ] Is every request either scheduled exactly once or rejected exactly once, with no overlap?
- [ ] Does each rejection carry an allowed reason code and a specific binding-constraint explanation?
- [ ] Does every scheduled meeting match its requested duration exactly?
- [ ] When window-only scheduling is enforced, does every meeting fit entirely inside a preferred window?

## Technical Notes

- Parse iCalendar with line unfolding first (continuation lines start with space/tab); naive line-by-line parsing corrupts folded properties.
- Model time zones explicitly using the constraint file's declared timezone; comparing naive local times across zones produces phantom conflicts or missed conflicts.
