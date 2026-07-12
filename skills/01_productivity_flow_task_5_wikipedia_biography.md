---
name: 01-productivity-flow-task-5-wikipedia-biography
description: Use when mining a source Wikipedia section for mentioned entities, then for each entity fetching and saving a specific named section from its own page. Focuses on complete entity extraction, canonical-name resolution (titles vs personal names), section-boundary scoping, and output-set exactness.
---

# Entity Extraction & Per-Entity Section Harvesting from Wikipedia

## Core Challenge

The core difficulty is exhaustive entity extraction with canonicalization: a narrative section mentions many people, sometimes by title rather than name, and the agent must resolve every mention to a canonical personal name, decide which of those have the target section on their own page, and save exactly those sections without leaking navigation chrome or extra files. The trap is partial extraction — grabbing only the most prominent figures — and name/title confusion (an entity referenced by reign title rather than personal name).

## Solution Strategy

1. **Extract entities exhaustively from the source section**: Read the entire target section and list every person mentioned, including those appearing only in subordinate clauses or quoted decrees; prominence is not a filter. Common mistake: harvesting only the main figures and missing minor ones mentioned once.
2. **Resolve each mention to the canonical personal name**: People are often referenced by title, posthumous name, or reign name; map each to the actual personal name used as the article title and as the output filename. Common mistake: saving a file under the reign title instead of the personal name.
3. **Exclude the source subject explicitly**: The entity that owns the source section is not a target output, even though it appears throughout. Common mistake: including the source subject's own biography among the outputs.
4. **Verify the target section exists on each candidate page before saving**: Not every mentioned person has the requested section; fetch each page and confirm the section heading exists before extracting. Common mistake: creating files for people whose page lacks the section, or skipping the check and saving unrelated content.
5. **Scope extraction to the target section only**: Capture from the target heading to the next heading of the same or higher level; do not bleed into adjacent sections and do not include the entire article. Common mistake: capturing from the section heading to end-of-page.
6. **Strip chrome while preserving prose**: Keep the section's prose, headers, and structure as they appear; remove URLs and hyperlinks since their presence causes content mismatch; normalize character forms consistently (e.g., simplified characters where required). Common mistake: leaving hyperlink markup in the text.
7. **Emit exactly one file per qualifying entity and nothing else**: Output-set exactness matters; extra files are penalized and missing files lose coverage. Common mistake: emitting a file for a person who lacked the section, or forgetting a minor figure.

## Decision Points

- **Ambiguous mention resolution**: When a name could refer to multiple historical figures, pick the one consistent with the source page's context and internal links; if uncertain, check the candidate page's lead.
- **Section-name variants**: The target section may appear under several headings (e.g., a biography section named differently across pages); match any of the accepted variants.
- **Title vs personal name for filename**: Always use the personal name that serves as the article title, not the reign title or courtesy name.

## Common Failure Patterns

- **Prominence bias**: Extracting only major figures → low coverage of minor but valid entities.
- **Title-as-name**: Saving files under reign or posthumous titles → filenames don't match canonical names.
- **Section over-capture**: Extracting from the heading to end-of-page → content mismatch with the true section boundary.
- **Chrome leakage**: Leaving URLs, hyperlinks, or reference markers in output → content comparison fails.
- **Source-subject inclusion**: Saving the source subject's own section → an extra, incorrect file.
- **Unverified section existence**: Creating files for entities whose page lacks the target section → extra files that shouldn't exist.

## Self-Check Questions

- [ ] Did I read the entire source section and list every person mentioned, including minor ones?
- [ ] Is each entity resolved to its canonical personal name (not reign/courtesy title)?
- [ ] Did I exclude the source section's own subject from the outputs?
- [ ] For each candidate, did I verify the target section exists on their page before saving?
- [ ] Is each extraction scoped to the target section (heading to next same-or-higher heading)?
- [ ] Is the output free of URLs, hyperlinks, and stray navigation chrome?
- [ ] Did I emit exactly one file per qualifying entity with no extra files?
- [ ] Are character forms (e.g., simplified Chinese) used consistently?
