---
name: 02-code-intelligence-task-5-jigsaw-puzzle-hard-zh
description: Use when reassembling a large grid from many rotated, shuffled pieces heavily seeded with decoys. Focuses on scaling exact edge-matching solvers, global constraint satisfaction, and time-bounded search over an exploding combinatorial space.
---

# Large-Scale Jigsaw Reassembly with Heavy Decoys

## Core Challenge

With a big grid, many pieces, many decoys, and several rotations in play, the search space is vast and time is bounded. The difficulty is no longer recognizing a good edge match — it's engineering a solver that filters decoys reliably, recovers every rotation, and finds a globally consistent layout fast enough to finish, while never letting one bad local decision cascade across dozens of cells.

## Solution Strategy

1. **Precompute a full pairwise edge-affinity matrix across all rotations first**: Build the complete cost table (piece × piece × orientation × side) once, up front, so all downstream decisions — decoy filtering, rotation recovery, placement — read from it without recomputation. Common mistake: recomputing edges deep inside the search loop, making runtime explode.

2. **Filter decoys by aggregate non-fit before searching**: A genuine piece has several high-affinity neighbors; a decoy peaks low against every candidate. Rank by best-achievable affinity and discard the global non-fitters first to shrink the search space dramatically. Common mistake: letting decoys enter the placement search and hoping it rejects them — the search then drowns.

3. **Treat rotation recovery as part of the adjacency decision**: The orientation maximizing edge agreement between two pieces simultaneously tells you they're neighbors and how each is rotated; never decouple the two. Common mistake: fixing all rotations up front, which injects wrong orientations into placement.

4. **Solve placement as a single global optimization**: At this scale, any greedy seed-and-grow strategy corrupts a long chain of cells after one error. Use global assignment/backtracking over the precomputed matrix to maximize total edge agreement across the entire grid. Common mistake: growing the layout from a corner or a single seed piece.

5. **Time-box the search and fall back gracefully**: With a hard time limit, prefer a good global heuristic that produces a coherent layout over an exhaustive search that times out. Verify the produced layout by rendering and checking seams. Common mistake: pursuing a perfect solution until the clock runs out, leaving no output.

6. **Enforce exact output counts**: The fixed numbers of rotations and distractors must be matched exactly; a wrong count zeroes a whole dimension. If unsure about a borderline item, still keep the totals correct. Common mistake: rounding or guessing the counts.

## Decision Points

- **Exhaustive search vs heuristic global solver**: Use heuristic global optimization under tight time limits; only go exhaustive when the (filtered) pool is small enough to finish in time.
- **Aggressive vs conservative decoy filtering**: Filter aggressively using aggregate non-fit before placement; a wrongly-kept decoy poisons the search, while a borderline true piece can often be recovered later.
- **Perfect-but-late vs good-and-on-time**: Always ship a coherent rendered assembly within the time budget; a partial-but-valid layout beats a perfect one that never lands.

## Common Failure Patterns

- **Recompute-in-loop scaling**: Scoring edges inside nested search → runtime explodes, timeout with no output.
- **Decoy-contaminated search**: Letting fakes into placement → solver wastes effort and produces corrupted layouts.
- **Greedy chain corruption**: Seed-and-grow from one corner → one misplacement cascades across the grid.
- **Count drift**: Wrong number of rotations or distractors → an entire scoring dimension zeroes out.
- **Timeout-with-nothing**: Chasing perfection past the deadline → no deliverable produced at all.

## Self-Check Questions

- [ ] Did I precompute the full edge-affinity matrix before any search?
- [ ] Did I filter decoys by aggregate non-fit before entering placement?
- [ ] Is rotation recovered jointly with adjacency, not fixed beforehand?
- [ ] Did I use global optimization rather than greedy chain growth?
- [ ] Do my distractor and transforms outputs each have exactly the required count?
- [ ] Did I render and seam-check the assembled image before describing it?
- [ ] Did I produce a valid, deliverable result within the time limit rather than chasing perfection?
- [ ] Is my content description derived from the rendered assembly?

## Technical Notes

- Edge affinity via SSD between border rows/columns across all (orientation, side) tuples; a sharp score gap separates true adjacencies from decoys.
- Apply the inverse of each detected clockwise rotation before placing a piece so it aligns with neighbors.
