---
name: 04-search-retrieval-task-5-fuzzy-search
description: Use when a target must be identified from partial clues across paper and code repositories. Focuses on conjunctive candidate filtering, cross-source verification, and avoiding premature commitment.
---

# Fuzzy Multi-Constraint Entity Identification

## Core Challenge

The user remembers a target vaguely — a method family, an author surname, an era, a popularity threshold — spread across two different registries (e.g., academic papers and code repos). No single clue is decisive, and only the conjunction narrows to one entity. The agent must gather a candidate set from the vaguest clue, then filter by the harder-to-search clues rather than searching for all clues at once.

## Solution Strategy

1. **Search on the rarest/most-specific clue first**: Pick the clue most likely to return a small candidate set (e.g., a distinctive method family) and query that, not the common clue (a surname). Common mistake: starting with the common clue and drowning in false matches.
2. **Build a candidate set, do not search for the final answer**: The goal of early queries is to enumerate plausible candidates, not to land on the one. Common mistake: phrasing queries as if expecting a single hit.
3. **Apply offline-verifiable clues as filters**: Once you have candidates, check the easily-verified clues (author surname, era, repo stars) by direct inspection rather than by more searches. Common mistake: re-searching each clue independently and never intersecting.
4. **Cross-reference the two registries**: Match each paper candidate to its code repository and verify the repository-side constraints (star count, existence). Common mistake: confirming the paper but never checking the repo, or vice versa.
5. **Confirm identity, not just similarity**: The final pick must satisfy every clue, not most clues. List each clue and the evidence it holds before committing. Common mistake: picking the candidate that feels right without checking the one constraint it might miss.
6. **Prefer original sources for verification**: Star counts and author order come from the repo and paper themselves, not from summaries. Common mistake: trusting a secondary ranking site for the star count.

## Decision Points

- **Which clue to search first**: Rank clues by selectivity — a distinctive technical phrase is more selective than a common surname or a year. Search the most selective first.
- **When candidates are many**: If the first query returns dozens of candidates, tighten with the next-most-selective clue in the same query before enumerating.
- **When only one candidate survives most clues but fails one**: Re-verify the failing clue from a primary source; if it truly fails, restart with a broader candidate set rather than force-fit.

## Common Failure Patterns

- **Common-clue-first**: Searching the surname → hundreds of false hits, candidate set unusable.
- **Single-source confirmation**: Identifying the right paper but never checking the repo constraint, or vice versa → wrong entity that half-matches.
- **Premature commitment**: Locking onto the first plausible candidate without checking all clues → fails the one constraint ignored.
- **Secondary-source trust**: Accepting star counts or authorship from an aggregator → stale or wrong data.
- **Clue-averaging**: Picking a candidate that satisfies "most" clues but misses one hard constraint → wrong answer on a conjunctive task.

## Self-Check Questions

- [ ] Did I search on the most selective clue first rather than the most memorable one?
- [ ] Did I build a candidate set instead of expecting a single hit?
- [ ] Did I apply each offline-verifiable clue as a filter on the candidate set?
- [ ] Did I cross-reference BOTH registries (e.g., paper AND repo) for the survivor?
- [ ] Does my final pick satisfy EVERY clue, with evidence for each?
- [ ] Did I verify popularity/authorship from primary sources, not aggregators?
- [ ] If a candidate failed one clue, did I discard it rather than rationalize?
