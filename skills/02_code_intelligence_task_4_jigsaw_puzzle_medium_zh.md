---
name: 02-code-intelligence-task-4-jigsaw-puzzle-medium-zh
description: Use when reassembling a larger grid image from shuffled, rotated pieces mixed with many distractors. Focuses on combinatorial edge matching, global layout search, and exact rotation recovery as piece count grows.
---

# Scaled Jigsaw Reassembly under Combinatorial Growth

## Core Challenge

As the grid and piece pool grow (more cells, more distractors, more rotations), the number of candidate neighbor pairings explodes, so ad-hoc or manual matching becomes both slow and unreliable. The challenge is moving from "spot the obvious fit" to a systematic, automated solver that filters decoys by edge incompatibility, recovers every rotation, and finds a globally consistent placement — because at this scale one greedy error propagates across many cells.

## Solution Strategy

1. **Automate edge scoring for all piece pairs and orientations up front**: Precompute a pairwise edge-match matrix across all four rotations before any placement decision, so search operates on a complete cost table rather than re-evaluating. Common mistake: re-scoring edges inside a nested loop, blowing up runtime.

2. **Distractors are the pieces with no strong neighbor anywhere**: With more decoys present, rank pieces by their best achievable edge-match score; true pieces have several high-scoring neighbors, distractors peak low on every side. Common mistake: keeping borderline pieces because they faintly resemble one true piece.

3. **Recover rotation jointly with adjacency**: The best-scoring orientation between two pieces is evidence both for *whether* they're neighbors and *how* each is rotated; treat orientation and placement as one decision. Common mistake: fixing orientations first, then placing, which propagates rotation errors.

4. **Solve placement as global optimization, never greedy chaining**: At larger grids, greedily snapping best neighbors from a seed virtually guarantees a corrupted layout. Search for the cell-and-orientation assignment maximizing total edge agreement across the whole grid. Common mistake: filling the grid row-by-row from the top-left corner.

5. **Respect exact output counts for every dimension**: The number of rotated pieces and distractors is fixed; producing a different count nullifies that entire dimension even if most individual items are right. Common mistake: guessing counts or omitting/adding entries.

6. **Render and self-verify before describing**: Assemble the chosen pieces (after derotation) into the full image, confirm seam continuity, and describe content only from the rendered whole. Common mistake: trusting the placement table without rendering it.

## Decision Points

- **Full pairwise precompute vs on-demand scoring**: Precompute when the pool is small enough to fit in memory; it makes the search phase fast and consistent.
- **Search algorithm**: Prefer global/best-fit assignment (or backtracking with the edge-cost matrix) over greedy; accept greedy only if a post-hoc full-seam check passes.
- **Count enforcement**: Always emit exactly the stated number of distractors and transforms; if uncertain about one item, still keep the total correct.

## Common Failure Patterns

- **Greedy propagation at scale**: One wrong early snap → tens of cells corrupted downstream.
- **Manual/visual matching**: Eyeballing pairings at a larger pool → missed adjacencies and wrong rotations.
- **Distractor under/over-counting**: Emitting the wrong number → the whole dimension scores zero.
- **Orientation-then-placement**: Fixing rotations independently → wrong orientations lock in wrong placements.
- **Describe-without-render**: Guessing the picture from the grid table → description detached from the actual image.

## Self-Check Questions

- [ ] Did I precompute pairwise edge scores across all four rotations before placing anything?
- [ ] Are distractors identified by global non-fit (no strong neighbor), not by appearance?
- [ ] Did I solve placement as a global optimization rather than greedy chaining?
- [ ] Does my distractor list and transforms map each have exactly the required count?
- [ ] Did I recover each piece's rotation jointly with its adjacency?
- [ ] Did I render the assembled image and verify seam continuity before describing it?
- [ ] Is my description grounded in the rendered assembled image?

## Technical Notes

- Precompute edge agreement as SSD between border rows/columns for all ordered (piece, orientation, side) tuples; the resulting matrix drives both distractor filtering and placement search.
- Apply the inverse of each detected clockwise rotation before placing a piece in the grid so its content aligns with neighbors.
