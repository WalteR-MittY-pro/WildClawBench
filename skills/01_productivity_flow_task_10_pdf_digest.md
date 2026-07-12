---
name: 01-productivity-flow-task-10-pdf-digest
description: Use when batch-processing PDFs to rename by parsed title, classify into categories, and selectively extract a structural element (e.g., the nth table) from a topic-filtered subset. Focuses on reading titles from page content, referential consistency across coupled outputs, and faithful extraction.
---

# PDF Corpus Digest: Rename, Classify, and Extract by Structure

## Core Challenge

The core difficulty is maintaining referential consistency across a multi-stage pipeline where one parsed artifact (the title) drives every downstream output: the rename, the rename-mapping table, the classification, and the topic-filtered table extraction. An early parsing error — especially the common trap of trusting PDF metadata fields rather than first-page body text — cascades into misaligned outputs across all sections. A second axis is faithful structural extraction: locating a specific numbered table in a PDF and rendering its caption, columns, and cell values accurately.

## Solution Strategy

1. **Parse titles from first-page body text, never from PDF metadata fields**: Embedded metadata (Title/Author/DOI fields) in these corpora is deliberately unreliable; extract the title from the rendered first-page text (largest top-of-page text, or the title line above the author block). Common mistake: reading the PDF's Title metadata field, which produces wrong rename targets and corrupts every downstream section.
2. **Make the title the single source of truth across all outputs**: The rename target, the rename-mapping table, the classification list, and the table-extraction section must all derive from the same parsed title; never re-derive the title differently in each stage. Common mistake: parsing the title one way for renaming and another way for classification, so the mapping table and the classification list disagree.
3. **Apply rename sanitization deterministically**: Replace the specified characters (spaces, slashes) with the specified replacement, keep the suffix; execute the rule uniformly so the renamed filename is predictable from the title. Common mistake: applying different sanitization (e.g., removing punctuation the rule didn't mention) that makes filenames unmatchable.
4. **Classify from title plus abstract, routing non-fits to a catch-all**: Use the title and abstract together for the fixed category set, and place every paper that doesn't fit the named categories into the explicit catch-all bucket so the partition is exhaustive. Common mistake: classifying on title alone and dropping ambiguous papers instead of routing them to the catch-all.
5. **For the topic-filtered subset, locate the requested structural element by position, not by caption match**: When asked for "the second table," enumerate tables in document order and pick the second; do not search for a caption that looks like "Table 2." Common mistake: grabbing the table whose caption mentions "2" rather than the second table in reading order.
6. **Render extracted tables faithfully, including caption, columns, and key cells**: Preserve the table's caption text, its column headers, the data row count, and the distinctive cell values; paraphrasing or truncating loses the cell-level checks. Common mistake: rendering only the data rows and dropping the caption, or merging cells that should be separate.
7. **Keep the renamed-file tree flat and free of strays**: Renamed files live directly under the designated directory with no subfolders and no leftover archives or extracted files. Common mistake: nesting renamed files in subdirectories or leaving the extracted archive behind.

## Decision Points

- **Body-text title vs metadata title**: Always use body text; treat metadata fields as adversarial.
- **Title normalization for matching**: When the same title appears in the mapping table and the classification list, use identical string forms so they can be cross-referenced.
- **Table position vs table number in caption**: Position in document order is the source of truth; a caption's self-reported number may differ from its position.

## Common Failure Patterns

- **Metadata-title trust**: Reading the PDF Title field → wrong rename targets that propagate to every section.
- **Title re-derivation drift**: Parsing the title differently per stage → mapping table and classification list disagree about which paper is which.
- **Caption-as-position**: Selecting a table by its caption number instead of its document-order position → the wrong table extracted when numbering is non-sequential.
- **Table truncation**: Rendering data rows without the caption or column headers → caption and column checks fail.
- **Catch-all omission**: Dropping papers that don't fit named categories instead of routing them to the catch-all → the partition is no longer exhaustive.
- **Output-tree clutter**: Leaving extracted archives or nesting files in subdirectories → flat-structure and cleanliness checks fail.

## Self-Check Questions

- [ ] Did I parse every title from first-page body text rather than PDF metadata fields?
- [ ] Is the parsed title the single source of truth across the rename, mapping table, classification, and extraction sections?
- [ ] Did I apply the rename sanitization rule deterministically and uniformly?
- [ ] Did I classify using title plus abstract and route non-fitting papers to the catch-all?
- [ ] For the topic-filtered subset, did I select the requested table by document-order position rather than caption number?
- [ ] Does each extracted table preserve its caption, column headers, row count, and distinctive cell values?
- [ ] Is the renamed-file tree flat, with no subdirectories and no leftover archives?

## Technical Notes

- PDF metadata fields (Title/Author/DOI) in synthetic corpora are frequently poisoned; extract titles from rendered first-page text via a text-extraction layer instead.
- Enumerate tables in document order before selecting by position; a table's self-reported number in its caption can be non-sequential or reused.
