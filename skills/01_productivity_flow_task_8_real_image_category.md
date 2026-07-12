---
name: 01-productivity-flow-task-8-real-image-category
description: Use when sorting a batch of heterogeneous images into a fixed set of named category folders, where the mapping is evaluated by best one-to-one folder-to-class matching. Focuses on boundary-case disambiguation, full-batch coverage with no duplicates, and folder-name exactness over invented labels.
---

# Partitioning an Image Batch into Fixed Category Folders

## Core Challenge

The core difficulty is that the five categories overlap at their boundaries (a chart screenshot could be "charts" or "UI"; a medical diagram could be "documents" or "medical"), so accuracy depends on consistent disambiguation heuristics rather than objective thresholds. The evaluation is a best one-to-one matching between the folders you create and the ground-truth classes, which means folder-name exactness, full coverage with no duplicates, and consistent tie-breaking all matter — a single misplaced boundary image is one error, but an empty or duplicated folder collapses the whole matching.

## Solution Strategy

1. **Use the exact folder names provided; never invent labels**: The evaluation matches folders to classes by name first and by content as a fallback; renaming a folder to something descriptive breaks the name match and forces the grader into content-based matching that may not recover. Common mistake: using descriptive names like "medical" instead of the required positional/numbered names.
2. **Ensure exactly the required number of folders, no more**: Extra folders reduce the achievable matching and missing folders break the one-to-one assignment; create precisely the specified folder set. Common mistake: creating a "misc" or "unsure" sixth folder for boundary cases.
3. **Place every image exactly once, preserving original filenames**: Full coverage with no duplicates and no extra files is graded; an image left out or copied into two folders both count against you. Common mistake: leaving images in the archive root or duplicating an image across folders when unsure.
4. **Classify by primary subject matter, not secondary attributes**: Decide the dominant content of each image (what the image is *of*, not what it *contains a fragment of*) so that boundary cases resolve consistently. Common mistake: routing a photo that happens to contain text into the documents category because text is visible somewhere.
5. **Resolve boundary cases with a fixed priority rule and apply it uniformly**: When a chart appears inside a UI screenshot, or a medical diagram is also a document, pick the same category every time using a deterministic rule (e.g., intent/domain over format), so the partition is internally consistent. Common mistake: resolving similar boundary cases differently across the batch, which scatters one true class across multiple folders.
6. **Actually look at each image rather than classifying from filename or metadata**: Filenames in these batches are deliberately uninformative; only visual inspection yields correct labels. Common mistake: grouping by filename prefix or file-size heuristics.
7. **Keep the output tree flat and free of stray files**: Only the required category folders and the moved images should exist; no thumbnails, logs, or extracted-archive leftovers. Common mistake: leaving extraction artifacts or a metadata sidecar in the results directory.

## Decision Points

- **UI screenshot containing a chart**: Classify by the screenshot's nature (a UI capture) rather than the chart fragment, unless the chart is the primary, full-frame subject.
- **Medical/scientific diagram that is text-heavy**: Prefer the medical/science category when the content is domain-specific imagery (X-rays, formulas, paper figures), and the documents category only when the image is primarily prose.
- **Synthetic vs photographed**: Rendered 3D objects and UI captures go to the synthetic/UI bucket even if they depict a realistic scene; photographs of real scenes go to the natural-photos bucket.

## Common Failure Patterns

- **Folder-name drift**: Inventing descriptive folder names → name-based matching fails and the folder-to-class mapping has to be inferred from content.
- **Extra "unsure" folder**: Creating a sixth bucket for boundary cases → reduces the achievable one-to-one matching accuracy.
- **Filename/metadata classification**: Grouping by filename prefix instead of pixel content → systematic misclassification on deliberately uninformative names.
- **Coverage gaps**: Leaving images in the source root or skipping hard cases → missing images count against full-coverage checks.
- **Inconsistent boundary resolution**: Routing similar boundary cases to different folders → one true class scatters across multiple predicted folders, collapsing class completeness.

## Self-Check Questions

- [ ] Are the folder names exactly the required names, with no invented labels?
- [ ] Are there exactly the required number of category folders and no extras?
- [ ] Is every image present exactly once across the folders, with original filenames preserved?
- [ ] Did I visually inspect each image rather than classifying from filename or size?
- [ ] Did I classify by primary subject matter, not secondary attributes?
- [ ] Is my boundary-case resolution rule applied uniformly across the whole batch?
- [ ] Is the output directory free of stray files, thumbnails, and archive leftovers?
