---
name: 05-creative-synthesis-task-3-product-poster
description: Use when designing an informational product poster from a single product photo. Focuses on extracting real features from the image and translating them into a designed, premium-feel layout.
---

# Feature-Driven Product Poster Design

## Core Challenge

The agent is handed a product photo and a small amount of given copy, and must observe the photo closely enough to extract specific, real product features (materials, craftsmanship, mechanisms, details) — not generic marketing labels — then present those features in a graphically designed poster that reads as intentional design rather than a stacked HTML template. The cognitive load is split between perceptual extraction (seeing what is actually there) and aesthetic translation (making it look designed, not auto-generated).

## Solution Strategy

1. **Extract features from the photo before designing anything**: Spend a dedicated pass observing the actual product — grain, stitching, hardware, compartment layout, strap mechanisms, finish — and record concrete specifics. Common mistake: jumping to layout with only the given copy and generic labels like "Premium Leather."
2. **Treat every feature claim as needing visual evidence**: A feature listed on the poster should be something you actually observed; vague superlatives without specificity read as filler. Common mistake: padding with marketing adjectives that aren't grounded in the photo.
3. **Integrate features visually, not just as text**: Use callouts, lines pointing to the product, close-up crops, or icons that connect each feature to a part of the image. Common mistake: dumping features into plain bordered text boxes stacked vertically.
4. **Design as a poster, not a webpage**: Use composition, intentional whitespace, typographic hierarchy (varied weight and size), color blocks, and creative integration of the product photo. Common mistake: producing a CSS flexbox column that looks like a wireframe.
5. **Hit all required copy elements legibly**: Verify every required text element (brand, name, tagline, price, reference price, CTA) is present, spelled correctly, and not overlapping or clipped. Common mistake: cramming prices together or letting text collide with the image.
6. **Aim for a premium, brand-appropriate feel**: Match the visual register to the product's positioning (luxury goods demand restraint, fine type, considered whitespace). Common mistake: applying a generic tech-startup aesthetic to a heritage product.

## Decision Points

- **Observed vs. given content**: Given copy is the floor; observed features are the differentiator. Spend the bulk of design effort on showcasing observed specifics, since generic copy alone scores as template-quality.
- **Photograph integration**: Decide whether the product photo is a hero (large, dominant) or an anchor (smaller, with callout-driven features around it). Hero works for strong photography; anchor works when features need visual pointing.
- **Generation approach**: Code-rendered (HTML/CSS → image) tends to look templated; image-generation or composite approaches can look more designed but risk distorting the product. Choose based on whether photographic fidelity matters.

## Common Failure Patterns

- **Generic feature labels**: "Premium Leather," "Brass Hardware" with no specificity → reads as boilerplate, not observation.
- **Template-stack layout**: Elements in a single vertical column with thin borders → looks like a first-draft wireframe.
- **Text collisions**: Prices, taglines, and CTAs overlapping or crammed → illegible, unprofessional.
- **Photo drop-in**: Product image pasted into a frame with no creative integration → no relationship between features and the visual.
- **Typographic monotony**: One font, one size, no weight contrast → no hierarchy, no design intent.
- **Dead space**: Large empty regions with no purpose → looks unfinished.

## Self-Check Questions

- [ ] Did I observe the product photo closely and extract specific, real features?
- [ ] Is every feature claim grounded in something visible in the photo?
- [ ] Are features presented with visual integration (callouts, crops, icons), not just text boxes?
- [ ] Is all required copy present, spelled correctly, and legible?
- [ ] Does the layout use composition, hierarchy, and whitespace intentionally?
- [ ] Would a critical art director call this a designed poster, or a stacked template?
- [ ] Does the visual register match the product's positioning (premium vs. casual)?
- [ ] Is the output at the required dimensions?

## Technical Notes

- When rendering via HTML/CSS to an image, be aware graders often penalize "looks like basic HTML" — consider compositing in an image library (Pillow, canvas) or using image generation for backgrounds/textures to escape the template look.
- Exact pixel dimensions are usually enforced as a hard gate; set canvas size explicitly and verify with an image library before saving.
