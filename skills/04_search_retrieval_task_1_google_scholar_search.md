---
name: 04-search-retrieval-task-1-google-scholar-search
description: Use when finding a relationship chain between two entities connected through indirect intermediaries. Focuses on BFS graph traversal across an unbounded, implicit-edge collaboration network.
---

# Collaborator Network Pathfinding

## Core Challenge

Finding the shortest connecting chain between two nodes in a graph whose edges are implicit and must be discovered incrementally. Each hop requires fetching a fresh page and parsing co-authors, so the graph expands combinatorially with no complete visibility. The agent must balance exploration breadth against the practical cost of each retrieval.

## Solution Strategy

1. **Anchor both endpoints first**: Pull and parse the immediate collaborator sets of the two target nodes before any traversal. Common mistake: starting BFS from one end with no notion of what the other end looks like, causing unbounded expansion.
2. **Treat co-authorship as undirected edges**: Each paper's author list is a clique; every co-author is a one-hop neighbor. Common mistake: only following "first author" links and missing the bulk of edges.
3. **Bi-directional BFS**: Expand the frontier from BOTH endpoints simultaneously and check for intersection at each depth. This roughly squares the per-step yield versus single-direction search. Common mistake: depth-first wandering that produces long chains and never terminates at the optimum.
4. **Prioritize high-degree / high-overlap candidates**: Within a frontier, expand nodes whose own collaborator lists are likely to intersect the opposing frontier (e.g., prolific researchers, shared institutions). Common mistake: exploring the lowest-hanging leaf first.
5. **Verify each hop with a shared artifact**: Every edge in the returned chain must be backed by an actual co-authored work you can cite. A "connection" without a paper is not an edge. Common mistake: inferring a link from name similarity or affiliation overlap.
6. **Stop at the minimum depth**: Once any chain is found at depth N, do not pursue depth N+1 chains. Continue only if multiple shortest chains are requested. Common mistake: collecting many chains of varying length and failing to identify which is shortest.

## Decision Points

- **Name ambiguity in the network**: When an intermediate name appears common, disambiguate by affiliation, co-author cluster, or profile page before accepting the edge. Choose to reject the hop if you cannot confirm identity.
- **Depth budget vs. completeness**: If no chain appears within a few hops, decide whether to widen breadth (more candidates per level) or deepen — widening is usually cheaper because the graph is sparse and dense only around hubs.
- **Multiple shortest chains**: If the task asks for "the shortest chains" (plural), after finding the first minimum-length chain, exhaustively expand all nodes at the same depth boundary to collect all equal-length paths.

## Common Failure Patterns

- **Single-direction DFS drift**: Following one collaborator thread deep into the network → returns a long non-optimal chain or never reaches the target.
- **Unverified edges**: Asserting a connection based on inferred collaboration → chain breaks when graded against actual paper records.
- **Missing the immediate intersection**: Not checking whether A and B share a direct co-author at depth 0 → returns a longer chain than necessary.
- **Name-string collapse**: Treating two distinct people with the same name as one node → false shortcuts that fail verification.
- **Premature termination**: Stopping at the first found chain without confirming it is shortest → loses points even though a valid chain exists.

## Self-Check Questions

- [ ] Have I extracted the full co-author sets of BOTH endpoints before traversing?
- [ ] Am I expanding the frontier from both ends and checking for intersection?
- [ ] Is every edge in my proposed chain backed by a real, citable co-authored work?
- [ ] Have I confirmed each intermediate node is the person I think (not a namesake)?
- [ ] Have I checked that no shorter chain exists at a shallower depth?
- [ ] If multiple shortest chains are requested, have I collected all equal-length paths?
- [ ] Did I record the chain as an ordered sequence of distinct nodes from start to end?

## Technical Notes

- Profile pages may paginate or lazy-load collaborator lists; ensure "Show all" / co-author tabs are fully expanded before treating the neighbor set as complete.
- Author names appear in varied romanizations and orders; match on stable identifiers (profile user IDs) where possible, not display strings.
