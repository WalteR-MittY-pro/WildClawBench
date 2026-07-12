---
name: 05-creative-synthesis-task-5-product-launch-video-to-json
description: Use when extracting a structured catalog of items from an event video and turning it into a designed multi-page promotional document. Focuses on disciplined schema extraction, null-handling, and dual artifact coherence.
---

# Event Video to Structured Catalog and Promotional Document

## Core Challenge

The agent must harvest a complete, deduplicated set of discrete items (e.g., products) from a long, unstructured video using only what is shown — extracting only the attributes that are explicitly visible or spoken, marking everything else as null rather than guessing — and then transform the same extracted facts into a polished, multi-page promotional document whose visual content stays faithful to the source. The dual failure mode is hallucinating plausible-but-unseen attributes on one side, and producing a promotional document that drifts from the verified catalog on the other.

## Solution Strategy

1. **Enumerate the full item set before extracting attributes**: Build the complete list of announced items first, applying the inclusion filter (e.g., hardware only, no software/services) strictly, so nothing is missed or double-counted. Common mistake: recording the first few items in detail and losing the later ones.
2. **Treat the schema as a contract with disciplined nulls**: For each attribute, record a value only if it is explicitly shown or stated in the video; use null for anything absent. Prior knowledge about real-world products is NOT a valid source. Common mistake: filling gaps with known specs from training data.
3. **Normalize values to the exact schema vocabulary**: Use the specified units, enums, and casing (e.g., exact color names as spoken, integer prices, category enums). Common mistake: free-form strings or localized spellings that fail schema validation.
4. **Pair each catalog entry with a representative frame**: Capture a clean product image from the video for each item, so the promotional document can reference real rather than fabricated visuals. Common mistake: using placeholder or wrong-product imagery.
5. **Keep the document and the catalog in lockstep**: The promotional document must reflect the same item set, names, specs, and prices as the structured file. Generate one from the other where possible. Common mistake: writing marketing copy that introduces facts not in the catalog, or omits items the catalog contains.
6. **Design the document as marketing, not a data dump**: Use real product images, a coherent visual system, and clear hierarchy across the pages, with each item given meaningful treatment. Common mistake: a plain table or stacked list of specs.

## Decision Points

- **Seen vs. inferred**: When an attribute is ambiguous (e.g., a battery figure shown only briefly, a color name spoken but not clearly), prefer null over a guess unless the evidence is explicit. A null is a neutral miss; a wrong value is a hallucination.
- **Image sourcing for the document**: Extract real keyframes when product shots are clean; fall back to composites or designed placeholders only if no usable frame exists, and never substitute a different product's image.
- **Document generation path**: HTML-to-PDF gives typographic and layout control but risks looking templated; design accordingly. Whatever the path, enforce the exact page-count and page-size constraints.

## Common Failure Patterns

- **Hallucinated specs**: Filling price, chip, battery, or colors from prior knowledge → factual errors against the source.
- **Item omission or duplication**: Missing a briefly-shown product, or counting variants as separate items → catalog set mismatch.
- **Inclusion-filter drift**: Including software/services when only hardware was requested, or vice versa → wrong item set.
- **Schema sloppiness**: Strings where ints are required, wrong enum values, mixed casing → validation failures.
- **Document/catalog drift**: Promotional document names or prices diverging from the JSON → inconsistent deliverables.
- **Placeholder imagery**: Generic stock visuals instead of the actual product frames → document feels fabricated.

## Self-Check Questions

- [ ] Did I enumerate every qualifying item before extracting attributes?
- [ ] Is every attribute value explicitly supported by video evidence, with nulls elsewhere?
- [ ] Did I avoid using prior knowledge to fill any field?
- [ ] Does every entry conform to the schema (types, enums, casing, units)?
- [ ] Did I apply the inclusion filter consistently (e.g., hardware only)?
- [ ] Are the document's item names, specs, and prices identical to the catalog?
- [ ] Does each document image correspond to the product it labels?
- [ ] Does the document meet the page-count and page-size requirements?

## Technical Notes

- Page-size constraints (e.g., A4) and exact page counts are usually hard gates; verify with a PDF library (PyMuPDF/`fitz`) before submitting, since HTML-to-PDF converters can silently add or drop pages.
- For image extraction, sample frames densely around each product reveal and pick the cleanest shot; downscale before encoding to keep API payloads manageable.
