---
name: 01-productivity-flow-task-9-scp-crawl
description: Use when crawling similarly-structured wiki entries and producing per entry a text dump, image counts, and structured metadata. Focuses on sustained consistency across pages, content-vs-chrome separation, fallback metadata rules, and summary-record alignment with per-item artifacts.
---

# Bulk Wiki Crawling with Per-Item Text, Images, and Metadata

## Core Challenge

The core difficulty is sustaining a consistent extraction pattern across dozens of pages that each have idiosyncratic structure (multi-proposal entries, varying collapsible-block implementations, inconsistent class labeling). The traps are content-vs-chrome confusion (counting navigation icons as article images), over-eager or under-eager text capture, and drift between the per-item artifacts and the aggregate summary — the summary's per-item counts must agree with the files actually saved in each item directory.

## Solution Strategy

1. **Build one general extraction pattern, then audit page-specific anomalies**: Parse a representative page to establish the content container, image selectors, and collapsible-block markers; then sweep the range and flag any page whose structure deviates for individual handling. Common mistake: assuming every page shares one structure and silently mis-parsing the outliers.
2. **Separate article content from site chrome ruthlessly**: Article images are those embedded in the entry's content body; exclude avatars, navigation icons, social buttons, and rating widgets. Restrict extraction to the main content container's DOM subtree. Common mistake: grabbing every `<img>` on the page, which floods the image set with chrome.
3. **Apply metadata fallback rules in their specified order**: When a primary field (e.g., Object Class) is absent, fall back to the next-ranked source (e.g., Containment Class), and only then to an explicit Unknown sentinel — never invent a value. Common mistake: defaulting to Unknown without checking the fallback field, or free-texting a value when both fields are absent.
4. **Count structural features by their logical unit, not their DOM occurrences**: Collapsible/collapsible blocks are counted once per logical block, even if the page renders multiple toggle controls for one block; include content-area blocks even when labeled as licensing or citation. Common mistake: counting toggle buttons instead of blocks, or excluding licensing blocks that are themselves collapsible.
5. **Capture the main article text substantially, not just a summary**: The text artifact must preserve the page's main body content (prose, formatting, structure), not a one-line excerpt; truncating to a teaser causes content-anchor recall to fail. Common mistake: saving only the abstract or the first paragraph.
6. **Keep the summary record and the per-item artifacts in lockstep**: The image count and item id in the summary must equal the number of image files saved in that item's directory, and the item directory must exist for every id in the summary. Common mistake: the summary reports three images but only two files were saved (or vice versa).
7. **Use sequential, deterministic image filenames inside each item directory**: Number images in document order; even a page with zero images still gets a directory and a text file. Common mistake: preserving source image filenames, which breaks the expected sequential naming.

## Decision Points

- **Browser rendering vs raw HTML**: Prefer raw HTML parsing when the content is server-rendered; reserve headless rendering for pages whose collapsible blocks or images are injected by JavaScript.
- **Multi-proposal entries**: For an entry that bundles several proposals, capture the page as a single item (the canonical id) rather than splitting into sub-items; the summary expects one record per canonical id.
- **Empty-image pages**: Always create the item directory and text file even when no article images exist; omit only the image files.

## Common Failure Patterns

- **Chrome inclusion**: Counting site navigation icons and avatars as article images → inflated image counts that disagree with the reference.
- **Fallback-rule skipping**: Defaulting to Unknown without checking the secondary field → metadata accuracy drops on entries that legitimately use the fallback.
- **Block-vs-button confusion**: Counting toggle buttons instead of logical collapsible blocks → block counts diverge from the reference.
- **Text truncation**: Saving only a teaser or abstract → content-anchor recall fails because distinctive phrases are missing.
- **Summary/artifact drift**: Summary image counts disagreeing with saved files → at least one of the two checks fails for that item.
- **Source-filename preservation**: Keeping original image filenames instead of sequential numbering → expected filename set doesn't match.

## Self-Check Questions

- [ ] Did I establish one extraction pattern and then audit pages that deviate from it?
- [ ] Are counted images restricted to the main content container, excluding all site chrome?
- [ ] Did I apply the metadata fallback rule in the specified order, defaulting to Unknown only as a last resort?
- [ ] Are collapsible blocks counted once per logical block, including content-area blocks labeled as licensing/citation?
- [ ] Does each text artifact preserve the page's main body content rather than just a summary?
- [ ] For every item, does the summary's image count equal the number of image files saved in its directory?
- [ ] Are images named sequentially inside each item directory, and does every item have a directory and text file?
- [ ] Is the summary valid one-object-per-line JSONL covering exactly the requested id range?

## Technical Notes

- Wiki pages of this kind are usually server-rendered; raw HTML parsing is faster and more deterministic than headless rendering, but collapsible-block structure may live in a content container distinct from the page's rating/widget chrome.
- Validate that saved image files are well-formed (correct magic bytes / trailing markers) before finishing, since broken downloads are graded as missing.
