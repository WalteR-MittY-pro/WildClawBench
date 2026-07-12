---
name: 05-creative-synthesis-task-10-social-poster-multi-crop
description: Use when adapting a single designed poster into multiple platform-specific aspect ratios. Focuses on content-aware cropping that preserves the subject while hitting exact ratio targets.
---

# Multi-Platform Smart Crop of a Designed Poster

## Core Challenge

The agent must take a single poster composition and reframe it into several very different aspect ratios (square, vertical-fullscreen, portrait) while keeping the primary visual subject intact and the composition aesthetically natural in each. The geometric reality is that a single source cannot losslessly satisfy wildly different ratios, so the agent must make principled trade-offs about what to preserve and what to sacrifice per target — a content-aware decision, not a mechanical center-crop.

## Solution Strategy

1. **Analyze the source composition before cropping**: Identify the primary visual subject, secondary information zones, and any text or logos that must not be cut. Map where the visual "weight" sits in the frame. Common mistake: applying center-crops blindly and decapitating the subject.
2. **Know the exact target ratio for each platform**: Use the precise standard ratios (square, vertical-fullscreen, portrait) and treat them as hard constraints with tight tolerance. Common mistake: approximating ratios and failing the tolerance check.
3. **Crop per-target, not per-template**: Each aspect ratio needs its own reframing decision because the lossy region differs; a crop window that works for portrait may fail for vertical-fullscreen. Common mistake: deriving all crops from one anchor.
4. **Preserve the primary subject above all else**: The subject must remain fully visible and identifiable in every crop; secondary elements are the candidates for sacrifice. Common mistake: keeping marginal content and clipping the focal point.
5. **Verify each output is a clean crop, not a stretch**: Dimensions must come from cropping (preserving aspect), never from resizing or distorting the source. Common mistake: resizing to force a ratio, which distorts the image.
6. **Visually confirm composition quality per crop**: After generating, inspect each output for awkward edges, cut-off text, or unbalanced framing, and re-anchor if needed. Common mistake: trusting the math and shipping a crop with a halved logo or clipped headline.

## Decision Points

- **Subject vs. ratio when they conflict**: When the subject's own aspect ratio is incompatible with the target (e.g., a wide subject into a vertical frame), decide whether to include surrounding context to fill the frame or to crop tighter and accept some subject cropping — prioritize keeping the identifiable core of the subject.
- **Anchor selection**: Use the subject's centroid as the default anchor, but bias toward keeping critical text/logos in-frame even if that off-centers the subject slightly.
- **Tolerance**: Hit the target ratio as exactly as possible; do not budget for tolerance by being sloppy, since some graders apply strict checks.

## Common Failure Patterns

- **Blind center-crop**: Cropping to the geometric center regardless of content → subject clipped or off-frame.
- **Ratio approximation**: Outputting "roughly" the right ratio → fails strict tolerance checks.
- **Stretch/resample distortion**: Resizing to force a ratio → visibly distorted image.
- **One-anchor-fits-all**: Deriving every crop from the same window → some targets lose the subject.
- **Clipped text/logos**: Cropping through headlines or brand marks → unprofessional, information lost.
- **Edge awkwardness**: Crop boundaries that bisect visual elements unnaturally → looks accidental.

## Self-Check Questions

- [ ] Did I analyze the source to find the primary subject and protected zones before cropping?
- [ ] Does each output match its target aspect ratio as exactly as possible?
- [ ] Is the primary subject fully visible and identifiable in every crop?
- [ ] Are critical text and logos intact in all outputs?
- [ ] Did I crop (not resize/distort) to achieve each ratio?
- [ ] Did I make an independent framing decision per target?
- [ ] Did I visually inspect each crop for edge quality and composition?
- [ ] Are all required output files present and non-trivial in size?

## Technical Notes

- Compute the crop window arithmetically from the source dimensions and the exact target ratio, then apply with an image library (Pillow) — never resize to change aspect ratio.
- For vertical targets where the source is landscape, decide deliberately between tight subject crop (less context) and padded inclusion (more context, smaller subject); both are valid but only one matches the poster's intent.
