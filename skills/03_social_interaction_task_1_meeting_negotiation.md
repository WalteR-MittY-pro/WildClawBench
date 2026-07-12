---
name: multi-round-meeting-negotiation
description: Use when coordinating a meeting across multiple people via back-and-forth messages. Focuses on reconciling conflicting availability, timezone conversions, decoy filtering, and preserving authority-set constraints over participant preferences.
---

# Multi-round Meeting Time Negotiation

## Core Challenge

Coordinating a single meeting across several busy people requires fusing partial, noisy, sometimes contradictory availability data that arrives in waves — while a hidden authority constraint (set by the original requester, often in an offhand postscript) must outrank the majority preference of the participants who reply later.

## Solution Strategy

1. **Extract the original requester's full intent before reaching out**: Capture duration, deadline, attendee list, and any buried preferences (postscripts, asides, footers). Common mistake: skimming the initial request and missing a one-line constraint that overrides everything downstream.
2. **Authenticate every message against expected senders**: Verify the sender domain/address matches the actual requester before acting. Common mistake: acting on a look-alike address or a plausible-but-unrelated request because the topic sounds similar.
3. **Normalize all availability to a single reference frame before comparing**: Convert every participant's stated times to one common timezone (note who travels or works remotely), then compute overlaps. Common mistake: comparing raw local times across zones and landing on a slot that excludes someone.
4. **Flag and clarify contradictions before proposing a time**: When one participant's message contains an internal inconsistency (free block vs. a conflicting commitment in a postscript), ask them to reconcile it rather than guessing. Common mistake: picking the more convenient reading and discovering the conflict after booking.
5. **Treat a new hard conflict as a re-compute trigger, not a delete trigger**: When a participant reveals a blocking event, slide the meeting around the conflict — never delete or modify their other calendar entries to force a fit. Common mistake: "solving" an overlap by removing data instead of finding a valid window.
6. **Re-assert the authority constraint at confirmation time**: When participants request changes (different room, different time) that contradict the original requester's spec, the original spec wins. Common mistake: caving to the loudest late-arriving voice and overwriting the boss's instruction.

## Decision Points

- **Contradiction in a reply vs. simple ambiguity**: Internal contradiction (same message says two incompatible things) → pause and clarify before proposing. Mere vagueness → propose and let them correct.
- **Participant counter-request vs. authority instruction**: When they conflict, follow the authority's original instruction and inform the participant, rather than silently switching.
- **Which day to propose**: After normalizing all times to one zone and reconciling conflicts, compute the actual overlap duration per day; only days whose overlap meets the required duration are viable, regardless of which day "feels" best.

## Common Failure Patterns

- **Decoy absorption**: Acting on a same-topic message from a different/look-alike sender → scheduling the wrong meeting or emailing the wrong people.
- **Timezone blindness**: Comparing local times without conversion → proposing a slot outside someone's actual availability, or missing the only valid day.
- **Optimistic overlap**: Assuming a window is big enough without subtracting known conflicts → booking a meeting that runs into a participant's hard stop.
- **Conflict-resolution by deletion**: Deleting or editing a participant's calendar entry to remove a clash → destroying real data and masking the real problem.
- **Late-arriving consensus override**: Letting a majority of participants change a detail the original requester pinned → producing an outcome the requester didn't want.

## Self-Check Questions

- [ ] Did I capture every constraint from the original requester, including footers, postscripts, and offhand notes?
- [ ] Have I confirmed the sender of each message is who I think it is (domain/address match)?
- [ ] Did I ignore or defer any request that isn't from the actual authority on this task?
- [ ] Have I converted every participant's availability to one common timezone before computing overlaps?
- [ ] Did I flag and ask about any message that contains an internal contradiction?
- [ ] When a new conflict surfaced, did I re-compute rather than delete someone's calendar entry?
- [ ] Did I verify the proposed window satisfies the required duration for ALL participants, after conflicts?
- [ ] At confirmation, did I preserve the original requester's pinned preferences against participant counter-requests?
