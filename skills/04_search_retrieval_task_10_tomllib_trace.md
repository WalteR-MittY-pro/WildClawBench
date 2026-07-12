---
name: 04-search-retrieval-task-10-tomllib-trace
description: Use when a standard-library addition and its introducing change must be traced under a tight search budget. Focuses on traceable evidence chains, query efficiency, and graceful abandonment when the budget is exhausted.
---

# Traceable Provenance Search Under Budget

## Core Challenge

The agent must produce two facts (what version added a feature, and which specific change introduced it) backed by a complete, reproducible evidence chain — each piece of evidence named with its source title, key claim, and URL — while staying inside a small search cap. The added rigor is that the agent must explicitly abandon rather than guess if the chain cannot be completed in budget.

## Solution Strategy

1. **Plan the evidence chain before the first query**: Decide which two or three source pages would, between them, prove both facts, then query toward those pages. Common mistake: searching reactively and assembling the chain afterward.
2. **Prefer the canonical changelog and the canonical VCS as your two anchors**: A "what's new" page proves the version; the merge commit/PR proves the change. Two anchors often suffice for two facts. Common mistake: relying on blog restatements that prove neither authoritatively.
3. **Make each query count double**: Phrase queries so a single result page can yield both the version and the change reference. Common mistake: narrow queries that answer only one fact.
4. **Harvest fully, then decide**: Read everything relevant on a page before issuing the next query; the second fact is frequently co-located with the first. Common mistake: leaving a page after the first fact and re-querying for the second.
5. **Record provenance as you go, not at the end**: For every search, log the exact query and a one-line finding immediately; the evidence chain is built incrementally. Common mistake: reconstructing the chain from memory and mangling URLs.
6. **Abandon honestly when the budget is exhausted**: If the chain cannot be completed within the cap, explicitly state "Unable to confirm" rather than guessing. Common mistake: fabricating an unverified fact to appear complete.

## Decision Points

- **One search vs. two for a two-fact provenance**: Try a single broad query first (changelog-style); if it yields only the version, spend the second on the VCS. Two well-targeted searches is the realistic optimum.
- **Confirmatory re-search vs. acceptance**: If a page states both facts clearly with citations, accept it; do not burn budget re-confirming.
- **When the budget is nearly gone and one fact is missing**: Abandon rather than infer — an explicit "Unable to confirm" beats a guessed fact that breaks the chain.

## Common Failure Patterns

- **Reactive searching**: Querying without a plan → burns budget on low-yield pages.
- **Chain reconstruction at the end**: Rebuilding evidence from memory → wrong URLs, lost claims, unverifiable chain.
- **Single-source over-reliance**: Trusting one secondary page for both facts → no authoritative provenance.
- **Guessing to fill a gap**: Inventing the missing fact to look complete → breaks traceability.
- **Budget-blindness**: Losing count of searches and exceeding the cap → penalty even if the facts are right.

## Self-Check Questions

- [ ] Did I plan which source pages would anchor each fact before searching?
- [ ] Does each query aim at a primary/canonical source capable of answering multiple facts?
- [ ] Did I harvest every relevant fact from each page before the next query?
- [ ] Did I log query + finding for every search as it happened?
- [ ] Does every evidence item carry source title, key claim, and URL?
- [ ] Is my search count within the stated budget, and stated explicitly?
- [ ] If I could not complete the chain, did I explicitly say "Unable to confirm" rather than guess?

## Technical Notes

- "What's new in X.Y" pages in standard-library docs typically name both the version and the feature's introducing change/PEP in one place; scan the whole page before re-searching.
- Change/PR numbers must be verified against the project's own VCS view, not a forum引用; confirm the identifier type (PR vs. issue vs. commit) on the page that states it.
