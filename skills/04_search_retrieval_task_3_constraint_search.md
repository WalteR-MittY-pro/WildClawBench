---
name: 04-search-retrieval-task-3-constraint-search
description: Use when a multi-attribute filter may have no item satisfying every constraint. Focuses on detecting infeasibility and ranking near-miss candidates rather than forcing a false positive.
---

# Over-Constrained Search with Infeasibility Detection

## Core Challenge

The user supplies a large conjunction of attributes and assumes one item satisfies all of them, but the real product space rarely does. The agent must detect that no single item meets every constraint, resist the urge to hallucinate or force a match, and instead surface the candidates that satisfy the most constraints — being honest about which constraints each one misses.

## Solution Strategy

1. **Enumerate the constraint set explicitly**: List every attribute the user named as a checkable predicate. Common mistake: mentally collapsing the list and forgetting one constraint during evaluation.
2. **Treat "no full match" as a live hypothesis**: From the start, assume the conjunction may be infeasible, and design your check to confirm or refute that. Common mistake: assuming a perfect match exists and stopping at the first candidate that looks close.
3. **Verify each candidate against every constraint individually**: Produce a per-constraint scorecard for each candidate, not a gestalt impression. Common mistake: saying "this phone basically fits" without checking each spec.
4. **Rank by satisfied-constraint count, then by importance**: When no full match exists, order near-misses by how many constraints they meet, weighing hard constraints above nice-to-haves. Common mistake: ranking by brand familiarity or a single headline spec.
5. **State infeasibility explicitly and justify each near-miss**: Tell the user no item satisfies all constraints, then present the closest options with the exact constraint(s) each violates. Common mistake: hiding the infeasibility and presenting near-misses as if they fully qualify.

## Decision Points

- **Hard vs. soft constraints**: If the user implies some constraints are mandatory (e.g., a specific chipset) and others are preferences, rank by hard-constraint satisfaction first. If the user gives no priority, treat all constraints equally weighted.
- **How many near-misses to present**: Present several (not one) so the user can trade off which constraint to relax; a single recommendation hides the trade-off.
- **Stale or rumored specs**: When a spec is unconfirmed, mark it as uncertain in the scorecard rather than counting it as satisfied.

## Common Failure Patterns

- **False-positive forcing**: Declaring a product "meets all requirements" when it actually misses one or two → confidently wrong.
- **Constraint amnesia**: Dropping a constraint partway through evaluation → near-miss ranked higher than it deserves.
- **Single-candidate tunnel vision**: Latching onto the first plausible option → no comparative basis, and often a worse coverage of constraints.
- **Hidden infeasibility**: Recommending near-misses without stating that no full match exists → user misled into thinking one qualifies.
- **Spec-source conflation**: Mixing specs from different variants or regions of the same product → false constraint satisfaction.

## Self-Check Questions

- [ ] Did I list every constraint and check each candidate against every one?
- [ ] Have I explicitly determined whether any single item satisfies the full conjunction?
- [ ] If none does, did I state that clearly up front?
- [ ] Does each recommended candidate come with the specific constraint(s) it violates?
- [ ] Did I rank candidates by number of constraints satisfied, not by familiarity?
- [ ] Did I distinguish verified specs from rumored or variant-dependent ones?
- [ ] Did I present multiple near-misses so the user can choose which constraint to relax?
