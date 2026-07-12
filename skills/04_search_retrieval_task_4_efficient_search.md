---
name: 04-search-retrieval-task-4-efficient-search
description: Use when a multi-hop factual lookup is capped at a small search budget. Focuses on query packing, dual-target retrieval, and evidence-chain construction under scarcity.
---

# Budgeted Multi-Hop Search

## Core Challenge

Two related facts must be found (e.g., a version number and its associated pull request) using as few searches as possible, ideally two. The skill is designing queries that retrieve both facts from overlapping sources and never wasting a query on a sub-question that a richer query would have answered in passing.

## Solution Strategy

1. **Map the dependent hops before searching**: Identify which fact unlocks the next (e.g., version first, then the PR that landed in that version) and which facts can be co-located. Common mistake: searching blindly without modeling the dependency.
2. **Pack multiple sub-answers into one query**: Phrase each query so a single authoritative page (changelog, PR list, "what's new") yields several facts at once. Common mistake: issuing one query per sub-question.
3. **Target primary sources first**: Official docs, changelogs, and the project's own issue tracker collapse multiple hops into one page. Common mistake: landing on aggregator sites that answer only one sub-question.
4. **Extract both facts from a page before re-searching**: When a page loads, harvest everything relevant before deciding the next query — often the second fact is already there. Common mistake: reading for one answer and missing the adjacent one.
5. **Stop the moment the chain is complete**: Once both facts are sourced, terminate; do not "confirm" with extra queries. Common mistake: burning the budget on redundant verification.
6. **Record query + finding per search**: Maintain a running log so the final evidence chain is built as you go, not reconstructed afterward. Common mistake: losing the query-to-finding mapping at write-up time.

## Decision Points

- **Broad-versus-narrow first query**: A broad query (e.g., "what's new in version X") can answer both hops if the version is already known; a narrow query is safer when the version itself is unknown. Prefer the broad one when you have a strong version hypothesis.
- **When two facts live on different source types**: If one fact is in docs and the other in the VCS, accept that two searches are needed and make each query maximally productive rather than trying to force one search.
- **Re-query vs. infer**: Never infer a fact you can verify within budget; if the page strongly implies but does not state the fact, and you have budget, spend one query to confirm.

## Common Failure Patterns

- **One-query-per-fact rigidity**: Treating each sub-question as a separate search → exhausts the budget on a two-fact problem.
- **Aggregator traps**: Landing on a secondary site that answers half the question → needs a second trip to the primary source anyway.
- **Confirmation overkill**: Re-searching to "make sure" after the chain is already complete → wastes budget that scoring penalizes.
- **Lost query log**: Forgetting which query produced which finding → cannot reproduce the evidence chain.
- **Premature inference**: Asserting the second fact from memory or implication without a source → unsupported claim in the chain.

## Self-Check Questions

- [ ] Did I model the dependency between the facts before the first search?
- [ ] Does each query target a primary source likely to answer multiple facts?
- [ ] Do I harvest every relevant fact from each page before issuing the next query?
- [ ] Is my query count at or near the minimum (ideally two for a two-fact lookup)?
- [ ] Did I stop searching as soon as both facts were sourced?
- [ ] Does each evidence item include source title, key claim, and URL?
- [ ] Did I explicitly state the total search count and each query used?

## Technical Notes

- A single "what's new in X" or release-notes page often contains both the version and the linking PR; always scan the whole page before re-searching.
- PR numbers and version numbers are easily confused with issue numbers; verify the identifier type against the page that states it.
