---
name: 02-code-intelligence-task-3-jigsaw-puzzle-zh
description: Use when reassembling an image from shuffled, rotated puzzle pieces mixed with distractors. Focuses on pixel-level edge matching to distinguish true pieces from decoys and on recovering each piece's rotation before placement.
---

# Jigsaw Reassembly with Distractors and Rotation

## Core Challenge

You receive more pieces than the grid needs, some rotated, some entirely fake. The decoys look stylistically identical to real pieces (same source image, same palette), so content similarity is useless. The only reliable signal is *exact pixel continuity across shared edges* — real neighbors match near-perfectly, fakes never do. The challenge is exploiting that signal to filter, derotate, and place simultaneously.

## Solution Strategy

1. **Reject semantic similarity; demand pixel-edge continuity**: Distractors share the source image's style, so color histograms and content embedding will not separate them. Compare the actual border pixel rows/columns between candidate neighbors with a difference metric (SSD/correlation); true neighbors match almost exactly. Common mistake: clustering pieces by overall appearance and treating the largest cluster as the solution.

2. **Detect rotation by trying all four orientations per edge pair**: A piece's correct orientation is the one that makes its edges match neighbors. For each candidate adjacency, compute edge agreement across 0/90/180/270 and keep the best. Common mistake: assuming a canonical orientation up front, which misaligns everything downstream.

3. **Distractors reveal themselves by global non-fit**: A true piece has high edge-match scores on multiple sides with several other true pieces; a distractor matches *nothing* well on any side. Use "matches nothing well" as the filter criterion, not "looks different." Common mistake: keeping a piece because it loosely resembles one neighbor.

4. **Solve placement as global optimization, not greedy chaining**: Greedy "best neighbor" chaining propagates a single early mistake across the whole grid. Instead, search for the assignment of pieces (and orientations) to grid cells that maximizes total shared-edge agreement. Common mistake: building the grid greedily from one corner.

5. **Validate the assembled image, then describe it**: After placing pieces, render the full image and check internal-edge continuity visually/programmatically; only describe content once the assembly is coherent. Common mistake: describing the image from memory of individual pieces rather than the assembled whole.

## Decision Points

- **Edge metric (SSD vs correlation)**: SSD on raw pixel values is simplest and works for exact-cut puzzles; use normalized correlation if lighting varies. Both should give true pairs a dramatically better score than fakes.
- **Greedy assembly vs global search**: At small grids greedy may work, but the moment distractors are present, prefer global/best-fit search to avoid cascading errors.
- **How many rotations to test**: Always test all four (0/90/180/270) per edge pair unless the puzzle explicitly guarantees no rotation.

## Common Failure Patterns

- **Style-based filtering**: Treating pieces with similar color/texture as likely-correct → distractors (cut from the same image) survive.
- **Fixed-orientation assumption**: Skipping rotation search → a rotated true piece becomes an unplaceable "distractor."
- **Greedy corner-starting**: Committing the first piece's neighbors before validating global fit → one misplacement corrupts the entire row/column.
- **Count-mismatch blind spot**: Outputting the wrong number of distractors/transforms → entire dimensions score zero even when most items were correct.
- **Describing from fragments**: Guessing the final image from individual pieces → inaccurate description that doesn't match the assembled result.

## Self-Check Questions

- [ ] Am I filtering distractors by edge-match failure rather than visual/style similarity?
- [ ] For every kept piece, did I test all four orientations against its neighbors?
- [ ] Did I search for a globally consistent layout rather than chaining greedily?
- [ ] Does my distractor list have exactly the required count?
- [ ] Does my transforms map list exactly the rotated pieces, with correct inverse rotations applied before assembly?
- [ ] Did I render and visually verify the assembled image is coherent across seams?
- [ ] Did I describe the image from the assembled result, not from memory of pieces?

## Technical Notes

- For pixel-edge matching, compare the last row/column of one piece against the first row/column of its candidate neighbor; SSD near zero (and a sharp gap to the next-best pair) is the hallmark of a true adjacency.
- To "derotate," apply the inverse of the detected clockwise rotation (e.g. rotate_270 detected → rotate +90 to restore) before placing into the grid.
