---
name: 05-creative-synthesis-task-7-paper-to-poster
description: Use when converting a dense research paper into a single-page academic conference poster. Focuses on distilling a narrative from technical content, sourcing real figures, and designing for legibility at conference scale.
---

# Academic Paper to Conference Poster

## Core Challenge

The agent must read a dense research paper, decide which contributions and results actually matter for a one-page treatment, obtain or generate genuine figures (not decorative filler), and lay everything out as a poster that is simultaneously content-complete, readable from a distance, and aesthetically coherent. The recurring failure is producing a wall of tiny text or a pretty layout with placeholder graphics — either content or design wins, but not both.

## Solution Strategy

1. **Read the paper for narrative, not just facts**: Identify the motivation, the core method, the key quantitative results, qualitative visualizations, and the conclusion as the five load-bearing sections before designing anything. Common mistake: pulling isolated sentences without a coherent arc.
2. **Source real figures, never decorative filler**: Use the paper's actual diagrams, result plots, and comparison tables (extracted from the PDF or repo); if none exist for a section, generate a meaningful schematic rather than a stock graphic. Common mistake: dropping in generic icons or shapes to fill space.
3. **Design for legibility at conference viewing distance**: Title and headings must dominate; body text must be large enough to read from a meter away; figure labels and axes must remain legible. When in doubt, fewer words at larger size beats more words at smaller size. Common mistake: cramming the paper's full text at 10pt to fit everything.
4. **Establish a clear visual hierarchy and reading order**: Use column structure, section headers, and whitespace to guide the eye from problem to method to results to conclusion. Common mistake: a single dense block with no navigational cues.
5. **Keep a cohesive, restrained design system**: A limited, harmonious palette; consistent typography; uniform figure treatment. Academic posters reward restraint, not visual fireworks. Common mistake: clashing colors or a different font per section.
6. **Verify the required anchors are present and readable**: Confirm the paper title, author block, and a minimum number of substantive figures are all visually present and legible at the output resolution. Common mistake: including the title as tiny header text or burying authors in a footnote.

## Decision Points

- **Depth vs. legibility**: When a section has too much content for its allotted space, cut detail and keep the headline message rather than shrinking the font. A readable summary beats an unreadable exhaustive treatment.
- **Extracted vs. generated figures**: Prefer the paper's own figures (extracted from PDF) for authenticity; generate schematics only when no suitable figure exists. Never substitute an unrelated image.
- **Information density**: Target moderate density with generous whitespace; posters that look like a printed manuscript are failures even if every fact is correct.

## Common Failure Patterns

- **Text-wall poster**: Pasting paragraph after paragraph at tiny font sizes → unreadable at viewing distance.
- **Decorative figure filler**: Generic icons or stock visuals standing in for real results → no informative content.
- **Missing anchors**: Title too small, authors omitted, or fewer than the required number of substantive figures → fails gating.
- **Hierarchy collapse**: No visual distinction between title, headings, and body → viewer can't find the reading order.
- **Design chaos**: Clashing palette, inconsistent fonts, misaligned elements → looks auto-generated.
- **Resolution shortfall**: Output below the required poster-scale resolution → fails the size gate.

## Self-Check Questions

- [ ] Does the poster convey the paper's motivation, method, results, and conclusion?
- [ ] Are the figures real and informative (from the paper or generated schematics), not decorative?
- [ ] Is the title large and clearly readable?
- [ ] Is body text large enough to read from a conference viewing distance?
- [ ] Are figure labels, axes, and legends legible?
- [ ] Is there a clear reading order via columns, headers, and whitespace?
- [ ] Is the color palette cohesive and the typography consistent?
- [ ] Is the output at the required resolution/size?

## Technical Notes

- Extract figures from the source PDF using a library like PyMuPDF (`fitz`) to render embedded images, or render full pages and crop regions of interest at high DPI.
- When rendering the final poster programmatically, set the canvas to the required pixel dimensions explicitly and verify with an image library before saving; downscaling a larger canvas is safer than upscaling a small one.
