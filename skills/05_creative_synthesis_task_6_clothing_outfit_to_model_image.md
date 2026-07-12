---
name: 05-creative-synthesis-task-6-clothing-outfit-to-model-image
description: Use when classifying garments, grouping them into coherent outfits, and generating model images for each outfit. Focuses on visual attribute reasoning, combinatorial matching, and cross-modal consistency.
---

# Garment Classification, Outfit Composition, and Model Image Synthesis

## Core Challenge

The agent must classify a set of garment flat-lays into standardized categories, partition them into complete outfits (one per role, no leftovers, no duplicates) that are aesthetically and contextually coherent, and then generate a model image for each outfit whose gender, garments, and styling faithfully reflect both the original items and the outfit concept. The difficulty compounds across stages: misclassification cascades into broken outfits, which cascade into model images that don't match anything.

## Solution Strategy

1. **Classify every item first, with the required vocabulary**: Assign each garment a standard category (top, trousers, skirt, shoes) plus descriptive attributes (color, fabric, formality, season) before any matching. Common mistake: jumping to outfits with partial classification and missing a role.
2. **Check the partition invariant before accepting any grouping**: Verify each outfit has exactly one item per required role, every source item is used exactly once, and the count of outfits matches the constraint. Common mistake: leaving an item unassigned or reusing one across outfits.
3. **Optimize outfits for holistic coherence, not just role-filling**: Within each outfit, judge color harmony, formality level, seasonal consistency, and gender presentation together; an outfit that fills slots but clashes on any axis is weak. Common mistake: greedy slot-filling that produces technically-complete but incoherent looks.
4. **Lock the outfit definition before generating images**: The model image must depict the exact garments and gender assigned to that outfit; once generation begins, the outfit is frozen. Common mistake: letting the image generator invent garments or drift from the assigned items.
5. **Make each model image a faithful, full-body depiction**: Show the complete outfit on a model of the specified gender, with each garment identifiable and the full figure visible. Common mistake: cropped, partial, or distorted renders where garments can't be verified.
6. **Keep structured data and images strictly paired**: The JSON entry for each outfit must describe the same garments, gender, and style shown in its corresponding model image. Common mistake: editing one artifact and leaving the other stale.

## Decision Points

- **Exact-match vs. best-fit grouping**: When multiple groupings satisfy the partition invariant, pick the one that maximizes pairwise coherence (color/formality/season/gender) across all outfits, not just the first valid partition.
- **Gender assignment**: Infer the intended gender presentation from the garments themselves (cut, styling, category) and keep it consistent between the JSON field and the model image. If ambiguous, choose one and apply it consistently to both artifacts.
- **Generation fidelity vs. artistry**: Prioritize faithful garment reproduction over stylized flair; a beautiful image of the wrong outfit scores worse than a plain image of the right one.

## Common Failure Patterns

- **Misclassification**: Putting a garment in the wrong category → breaks the partition and cascades through every downstream stage.
- **Incomplete partition**: Leaving an item unused or duplicating one → outfits fail the completeness invariant.
- **Incoherent grouping**: Slot-filling without judging harmony → technically complete but aesthetically broken outfits.
- **Generation drift**: The model image showing garments or a gender not in the assigned outfit → image and JSON disagree.
- **Cropped/distorted renders**: Missing lower body, warped proportions, or partial garments → garments can't be verified in the image.
- **Stale pairing**: JSON edited after images were generated (or vice versa) → the two artifacts contradict each other.

## Self-Check Questions

- [ ] Is every item classified into a valid standard category?
- [ ] Does the outfit partition use each item exactly once with the correct count of outfits?
- [ ] Does each outfit have exactly one item per required role?
- [ ] Are outfits coherent across color, formality, season, and gender?
- [ ] Does each model image show the exact garments and gender assigned to its outfit?
- [ ] Is each model image a clear, full-body depiction?
- [ ] Are the JSON descriptions and the model images mutually consistent?
- [ ] Are the required categories and field names used exactly?

## Technical Notes

- Image generation models benefit from explicit, concrete garment descriptions (color, cut, fabric, fastening) in the prompt rather than abstract style words; reference the source flat-lay description verbatim where possible.
- If the generation API supports image-to-image or reference-image inputs, feeding the flat-lays as references dramatically improves garment fidelity over text-only prompts.
