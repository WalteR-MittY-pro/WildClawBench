---
name: 02-code-intelligence-task-8-link-a-pix-color-zh
description: Use when solving a Link-a-Pix pixel puzzle from an image clue, pairing same-colored same-valued numbers with exact-length paths. Focuses on exact path-length constraint satisfaction, non-crossing global routing, and turning the solved grid into a recognizable picture.
---

# Link-a-Pix Path Routing with Exact-Length Constraints

## Core Challenge

Each clue number (except 1) appears exactly twice, and the two copies must be joined by an orthogonal path whose length — *including both endpoint cells* — equals the number's value. Paths cannot cross or reuse cells. This is a tightly coupled constraint-satisfaction problem: every local routing decision shrinks the space for all remaining pairs, so greedy connections quickly produce boards where the last pairs can't be legally routed. The solver must pair numbers, route paths of exact length, keep cells disjoint, and ultimately yield a recognizable colored picture.

## Solution Strategy

1. **Pair clues by (value, color) before routing**: Each number-color combination has exactly two endpoints; resolve the pairing first, then route. Treat value-1 cells as self-filled and set them aside. Common mistake: routing without first establishing which two cells form a pair.

2. **Enforce exact path length including both endpoints**: A clue value of N means the connecting path covers exactly N cells, endpoints included. Count cells, not steps; off-by-one (counting steps) is the classic error. Common mistake: producing a path of length N-1 or N+1 that still "looks connected."

3. **Route as disjoint-path constraint satisfaction, not independent shortest paths**: Cells may belong to only one path, so routes interact globally. Use search/backtracking that treats cell occupancy as shared state, and backtrack when a later pair becomes unroutable. Common mistake: routing each pair greedily by shortest path and leaving the rest with no room.

4. **Order pairs to reduce dead-ends**: Route constrained pairs first — high values (long paths), pairs with few feasible corridors, or centrally-located endpoints — so the hardest decisions are made while the board is open. Common mistake: routing easy short pairs first and boxing in the long ones.

5. **Fill path cells with the pair's color and render the picture**: Once all pairs are routed, color every covered cell with its path's color and render the full grid; the filled cells should reveal a hidden image. Common mistake: coloring only the path trace or endpoints rather than every covered cell.

6. **Describe the revealed picture from the rendered result**: Generate the filled image, then describe what it depicts based on the actual pixels, not on the abstract clue layout. Common mistake: guessing the subject from clue positions without rendering.

## Decision Points

- **Path length semantics**: Always count cells (endpoints included); a clue N ⇒ N covered cells. Re-derive this from the rules rather than assuming "steps."
- **Greedy vs backtracking search**: Backtracking with shared occupancy is essential because paths interact; pure greedy works only on trivial boards.
- **Pair ordering**: Hardest-first (long paths, tight corridors) minimizes backtracking; easy-first tends to deadlock.

## Common Failure Patterns

- **Off-by-one path length**: Counting steps instead of cells → paths systematically one cell short.
- **Independent shortest-path routing**: Ignoring cell sharing → later pairs become unroutable.
- **Easy-first ordering**: Routing short pairs first → long pairs get boxed out.
- **Incomplete coloring**: Filling only the trace, not all covered cells → the picture never emerges.
- **Describe-without-render**: Guessing the image from clues → description uncorrelated with the actual output.

## Self-Check Questions

- [ ] Did I pair clues by matching (value, color) before routing?
- [ ] Does every path cover exactly its clue-value number of cells, endpoints included?
- [ ] Is routing solved as disjoint-path constraint satisfaction with backtracking?
- [ ] Did I order pairs hardest-first to avoid deadlocks?
- [ ] Did I fill every covered cell (not just the trace) with the pair's color?
- [ ] Did I render the full grid and describe the picture from the rendered pixels?
- [ ] Did I verify no two paths share a cell?

## Technical Notes

- Path length in Link-a-Pix counts cells inclusive of both numbered endpoints: a clue of N requires a path occupying exactly N cells.
- Routes are orthogonal (horizontal/vertical moves only); diagonal moves are illegal. Represent occupancy globally so the router can backtrack on conflicts.
