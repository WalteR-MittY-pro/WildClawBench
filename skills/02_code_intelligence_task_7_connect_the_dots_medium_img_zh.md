---
name: 02-code-intelligence-task-7-connect-the-dots-medium-img-zh
description: Use when connecting numbered dots drawn in an image, where coordinates must be extracted by vision/OCR. Focuses on reliable perception-to-coordinate extraction and precise ordered line drawing with no skipped or misread labels.
---

# Ordered Dot-Connection from Visual Input

## Core Challenge

The puzzle lives entirely in an image: numbered dots at unknown pixel positions, labels that may be small or crowded. You must perceive every dot, read every number correctly, map each to a precise (x, y) coordinate, then draw line segments strictly in numeric order. The difficulty is the perception-to-structure pipeline — a single misread, duplicated, or skipped number breaks the whole chain and corrupts the emergent picture.

## Solution Strategy

1. **Extract all (number, coordinate) pairs before drawing anything**: Treat perception as a discrete first phase: detect every dot, OCR its label, record its center pixel. Only once the full ordered set is captured should you start connecting. Common mistake: interleaving perception and drawing, so an early missed dot can't be recovered.

2. **Cross-check count and sequence integrity**: After extraction, verify the numbers form the expected contiguous sequence (1..N) with no gaps, duplicates, or out-of-range values. A hole in the sequence is a perception failure to fix, not to paper over. Common mistake: proceeding with a broken sequence and producing a discontinuous drawing.

3. **Use precise dot centers, not label bounding boxes**: Lines should connect at the dot centroid; using the text bbox or a rough region introduces offset that compounds visually. Common mistake: connecting approximate positions that make the picture look shifted or jagged.

4. **Draw strictly in numeric order, adjacent pairs only**: Connect 1→2→3→…→N with individual segments; do not jump, close loops early, or connect non-adjacent numbers. Common mistake: connecting points out of order or in perceived-spatial order instead of numeric order.

5. **Draw on a copy of the original and save losslessly**: Load the source image, overlay lines, and save as PNG to preserve exact pixels. Common mistake: re-encoding through lossy formats or resizing, which degrades the comparison against ground truth.

## Decision Points

- **Vision/OCR vs programmatic detection**: If dots have a consistent color/shape, detect them programmatically (color thresholding + contours) for robust centroids; fall back to VLM/OCR for reading the numbers. Combine both for best results.
- **Manual coordinate guessing vs systematic extraction**: Always extract systematically; guessing coordinates from a glance guarantees errors at scale.
- **Single VLM call vs iterative verification**: For many dots, verify the extracted list against the image (count, min/max number) before trusting it.

## Common Failure Patterns

- **Skipped/duplicated numbers**: Missing a dot in perception → the sequence breaks and the picture is wrong from that point on.
- **Coordinate offset**: Using label bbox centers instead of dot centers → uniformly shifted or jagged lines.
- **Out-of-order connection**: Connecting by spatial proximity rather than numeric order → a recognizable-but-wrong figure.
- **Lossy re-save**: Writing through JPEG → the output no longer matches ground-truth pixels.
- **Trusting a single pass**: One VLM extraction with no count check → undetected omissions propagate to the final drawing.

## Self-Check Questions

- [ ] Did I extract every (number, coordinate) pair in a discrete perception phase before drawing?
- [ ] Is the extracted sequence complete and contiguous with no gaps or duplicates?
- [ ] Am I using dot centroids, not label bounding boxes, as connection points?
- [ ] Did I connect strictly in numeric order, adjacent pairs only?
- [ ] Did I draw on a copy of the original and save as lossless PNG?
- [ ] Did I verify the dot count and number range against the image before trusting my extraction?
- [ ] Did I visually inspect the result to confirm it forms a coherent figure?

## Technical Notes

- Dot detection via color thresholding (HSV) + contour extraction gives robust centroids; pair each centroid with the nearest OCR'd digit to assign its number.
- Always draw onto a copy of the source and save PNG to keep exact pixel fidelity for visual comparison.
