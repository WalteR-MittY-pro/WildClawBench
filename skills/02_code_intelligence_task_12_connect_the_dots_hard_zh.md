---
name: 02-code-intelligence-task-12-connect-the-dots-hard-zh
description: Use when connecting many color-grouped numbered dots extracted from an image, then recognizing the emergent figure. Focuses on robust large-scale perception (color grouping + numbering), scalable ordered line drawing, and gestalt recognition from a noisy rendering.
---

# Large-Scale Grouped Dot-Connection and Pattern Recognition

## Core Challenge

At scale (hundreds of dots, multiple color groups), the perception pipeline is the bottleneck and failure point: every dot must be detected, color-grouped, numbered, and assigned a precise coordinate, then connected in per-group numeric order. A few missed or mis-grouped dots won't crash the pipeline but will deform the emergent figure. The secondary challenge is recognizing what the connected lines depict, accepting that localization noise is inevitable and the gestalt must be read from the rendered result.

## Solution Strategy

1. **Detect dots programmatically by color, not by eye**: Use color thresholding (HSV) and contour detection to find every dot and its centroid robustly; assign each to a group by its color. Common mistake: relying on VLM/visual counting at scale, which drops or duplicates dots.

2. **Group by color, then read the per-group number sequence**: Within each color group, OCR/assign the numeric label of every dot; verify each group's labels form a complete contiguous sequence. Common mistake: numbering dots across groups or skipping sequence-integrity checks per group.

3. **Connect strictly within each group, in numeric order**: For each color group, draw segments 1→2→3→…→N between adjacent numbers; never bridge across groups or skip numbers. Common mistake: connecting by spatial proximity instead of per-group numeric order.

4. **Use precise centroids and draw on a lossless copy**: Connect dot centers (not label boxes), overlay on a copy of the original, and save as PNG to preserve pixels for comparison. Common mistake: connecting label bounding-box centers or re-saving through lossy encoders.

5. **Accept perceptual noise and read the gestalt from the rendered image**: With hundreds of dots, a few localization errors are unavoidable; the figure is still recognizable in aggregate. Describe what the *rendered* lines depict, not what you assume the dots should form. Common mistake: refusing to describe because the drawing isn't pixel-perfect, or describing from the clue layout instead of the result.

6. **Time-box perception vs recognition**: Perfect detection of every dot may not be feasible under the time limit; invest enough in detection that the figure is recognizable, then describe from the rendering. Common mistake: over-investing in perception until no time remains to render and describe.

## Decision Points

- **Programmatic detection vs VLM perception**: Prefer programmatic color-based detection for robustness at scale; use a VLM only to assist with reading small labels or to sanity-check counts.
- **Perfect detection vs sufficient detection**: Aim for sufficient detection such that the emergent figure is recognizable; pursue perfection only if time allows, since missing outputs (description/image) are scored as failures.
- **Group boundary ambiguity**: Resolve a dot's group by its color clustering, not by spatial location; a misgrouped dot corrupts that group's chain.

## Common Failure Patterns

- **Scale-induced perception loss**: Relying on visual/VLM counting for hundreds of dots → dropped/duplicated numbers corrupt the chains.
- **Cross-group connection**: Bridging numbers across color groups → wrong figure segments.
- **Spatial-order connection**: Linking dots by proximity rather than per-group numeric order → a plausible-but-wrong picture.
- **Coordinate offset**: Using label bbox centers instead of dot centroids → uniformly jagged lines.
- **Refuse-to-describe**: Withholding a description because the drawing is imperfect → the recognition score is lost even when most lines are correct.

## Self-Check Questions

- [ ] Did I detect dots programmatically by color rather than counting visually?
- [ ] Did I group dots by color and verify each group's number sequence is complete and contiguous?
- [ ] Did I connect strictly within each color group, in numeric order?
- [ ] Am I using dot centroids (not label boxes) and saving losslessly?
- [ ] Did I render the result and read the figure from the rendered image?
- [ ] Did I still produce a description even if detection is slightly noisy?
- [ ] Did I balance time between perception and producing the required outputs?

## Technical Notes

- HSV color thresholding + contour extraction robustly separates color groups and yields centroids; pair each centroid with its OCR'd number, then sort within group.
- Draw onto a copy of the source and save PNG to retain exact pixels; describe the figure from the rendered output since partial noise still yields a recognizable gestalt.
