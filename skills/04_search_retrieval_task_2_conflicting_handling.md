---
name: 04-search-retrieval-task-2-conflicting-handling
description: Use when a local reference corpus may be outdated and must be reconciled against live web sources. Focuses on conflict detection, recency arbitration, and source-authority weighting.
---

# Local-vs-Web Information Conflict Resolution

## Core Challenge

A trusted local corpus holds a rule whose answer conflicts with current authoritative sources, and the agent must not merely pick one but reason about which source governs. The difficulty is recognizing that "the file says X" is not the same as "X is currently correct," and that legal/regulatory/factual content has a temporal validity that must be checked externally.

## Solution Strategy

1. **Read the local source first to extract the governing rule**: Identify which local provision actually applies to the question, including its citations and effective dates. Common mistake: ignoring the local corpus entirely and answering from general knowledge.
2. **Flag every local rule as possibly stale**: Treat each cited rule's currency as an open question, not a given. Common mistake: assuming the local file is authoritative because it was provided.
3. **Verify against the freshest authoritative web source**: Locate the currently-in-force version of the rule and compare effective dates and text. Common mistake: comparing against a secondary blog post rather than the official gazette/standard body.
4. **Resolve conflicts by authority and recency, not by familiarity**: When local and web disagree, prefer the source that is both more authoritative (official publisher) and more recent (latest amendment). Common mistake: averaging or hedging between the two instead of picking the governing one.
5. **State the final conclusion as a single answer**: After resolving, commit to the answer the governing source supports and explain why the conflict fell the way it did. Common mistake: presenting both values and leaving the decision to the reader.

## Decision Points

- **When local and web agree**: Cite the local source for the reasoning and the web source for confirmation; no conflict to resolve.
- **When local is older but the rule has not been amended**: The local text is still good law/fact; verify the absence of amendment rather than assume staleness.
- **When sources disagree on a date-sensitive quantity** (e.g., a limitation period): The effective date of the controlling amendment is decisive — trace which amendment was in force at the relevant event date.

## Common Failure Patterns

- **Blind local trust**: Reading the provided file and outputting its value verbatim → wrong answer when the rule has since changed.
- **Blind web trust**: Ignoring the local file and answering from a generic web summary → wrong when the question hinges on a specific local provision.
- **Hedge-and-defer**: Listing both candidate answers without resolving → no usable conclusion.
- **Recency without authority**: Picking the newer source just because it is newer, when it is actually a secondary commentary and the older source is the primary law.
- **Event-date misalignment**: Applying the current rule to a past event, or a past rule to a current event, when the rule changed in between.

## Self-Check Questions

- [ ] Did I read and extract the specific governing rule from the local corpus?
- [ ] Did I identify the effective date of the local rule and check whether it has been amended?
- [ ] Did I verify against an official, authoritative web source (not a secondary summary)?
- [ ] When local and web conflicted, did I explicitly state which governs and why?
- [ ] Did I anchor my final answer to the rule in force at the time of the relevant event?
- [ ] Did I commit to a single final answer rather than presenting alternatives?

## Technical Notes

- Legal/regulatory pages often have a "version history" or "effective date" field; check it before trusting the displayed text as current.
- When the event spans an amendment boundary, the rule in force at the event date (not today) usually governs — confirm which date is legally operative.
