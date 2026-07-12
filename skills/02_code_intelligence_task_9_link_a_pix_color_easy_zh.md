---
name: 02-code-intelligence-task-9-link-a-pix-color-easy-zh
description: Use when solving a Link-a-Pix pixel puzzle from a structured data file pairing clues by value and color. Focuses on trusting the provided structured source, exact-length disjoint path routing, and turning the solved grid into a recognizable picture.
---

# Link-a-Pix Solving from Structured Clue Data

## Core Challenge

The puzzle's clue data (positions, values, colors) is handed to you in a structured file, removing the perception burden. What remains is the core constraint-satisfaction problem: pair identical (value, color) clues, route each pair along an orthogonal path of exact cell-length, keep all paths disjoint, and fill the covered cells to reveal a hidden image. The trap is treating pathfinding as independent shortest-paths — they interact, because a cell can belong to only one path.

## Solution Strategy

1. **Trust and parse the structured data as ground truth**: Read the clue file directly (positions, values, colors) rather than re-deriving them from the image. The image is a reference; the JSON is the source of truth. Common mistake: OCR-ing the image and introducing errors when clean data was provided.

2. **Pair clues by (value, color); handle 1-cells separately**: Each non-1 clue value-color pair has exactly two endpoints; resolve pairings first. Value-1 cells are self-filled and excluded from routing. Common mistake: routing before establishing endpoint pairs.

3. **Enforce exact path length including both endpoints**: A clue value of N means the path covers exactly N cells, endpoints included — count cells, not steps. Off-by-one is the canonical bug. Common mistake: producing N-1 or N+1 cell paths that still look connected.

4. **Route as disjoint-path constraint satisfaction with backtracking**: Cell occupancy is shared global state; a route that's locally valid may block a later pair. Search/backtrack over the whole board, not pair-by-pair greedily. Common mistake: routing each pair by shortest path and stranding the rest.

5. **Order pairs hardest-first**: Route the most constrained pairs first — long paths, tight corridors, central endpoints — while the board is open. Common mistake: clearing easy short pairs first and boxing in the long ones.

6. **Fill every covered cell with its path's color, then render and describe**: Color all cells along each path with that pair's color, render the full grid, and describe the revealed image from the actual pixels. Common mistake: coloring only endpoints or the trace, so the picture never emerges.

## Decision Points

- **Structured data vs image**: Always parse the structured clue file as ground truth; consult the image only to sanity-check or to describe the final picture.
- **Greedy vs backtracking**: Backtracking with shared occupancy is essential because paths interact; greedy shortest-paths works only on trivial boards.
- **Pair ordering**: Hardest-first minimizes backtracking and avoids terminal deadlocks.

## Common Failure Patterns

- **Re-perceiving clean data**: OCR-ing the image when a JSON is provided → needless transcription errors.
- **Off-by-one path length**: Counting steps instead of cells → systematically short paths.
- **Independent shortest-path routing**: Ignoring cell sharing → late pairs unroutable.
- **Easy-first deadlock**: Routing short pairs first → long pairs get boxed out.
- **Trace-only coloring**: Filling just the line, not all covered cells → picture incomplete.

## Self-Check Questions

- [ ] Did I read clue positions/values/colors from the structured file as ground truth?
- [ ] Did I pair clues by matching (value, color) and set 1-cells aside?
- [ ] Does every path cover exactly its clue-value number of cells, endpoints included?
- [ ] Is routing solved as disjoint-path constraint satisfaction with backtracking?
- [ ] Did I order pairs hardest-first to avoid deadlocks?
- [ ] Did I fill every covered cell (not just the trace) with the pair's color?
- [ ] Did I render the full grid and describe the picture from the rendered pixels?
- [ ] Did I confirm no two paths share a cell?

## Technical Notes

- Path length counts cells inclusive of both numbered endpoints: a clue of N ⇒ N covered cells; routes are orthogonal only (no diagonals).
- Keep a global occupancy grid so the router can detect conflicts and backtrack; the JSON's `rows`/`cols` define the grid extent.
