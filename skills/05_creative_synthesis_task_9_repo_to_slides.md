---
name: 05-creative-synthesis-task-9-repo-to-slides
description: Use when producing a fixed-length presentation about an unfamiliar open-source project as a PDF. Focuses on narrative arc design, page-count discipline, and consistent visual systems across slides.
---

# Repository to Fixed-Length Project Presentation

## Core Challenge

The agent must research an unfamiliar project, distill it into a coherent presentation narrative that fits an exact page count, source real visuals, and render a PDF whose slides share a single, consistent design language. The two structural traps are missing the page count exactly (a hard gate) and producing slides that look like they came from different templates pasted together.

## Solution Strategy

1. **Design the narrative arc before the slides**: Decide the page-by-page storyline (title, overview, architecture, results, dataset, innovation, etc.) so the fixed page count is allocated deliberately, not filled reactively. Common mistake: writing slides ad hoc and running over or under the count.
2. **Lock the page count as a hard constraint**: The output must have exactly the required number of pages; verify with a PDF library after generation and re-balance content until it matches. Common mistake: treating the count as approximate and shipping N±1 pages.
3. **Build one design system, apply it everywhere**: Define the palette, fonts, header treatment, and layout grid once and reuse across every slide so the deck reads as a unified artifact. Common mistake: per-slide ad-hoc styling that produces visual inconsistency.
4. **Cover the project's defining topics, not generic ones**: Include the topics that matter for this specific project (its architecture, its dataset, its innovation over predecessors) rather than a generic SaaS pitch structure. Common mistake: a templated "problem/solution/market" deck that says nothing specific.
5. **Source real or purpose-built visuals**: Use the project's actual diagrams, results, or architecture figures; generate clean schematics where real ones are missing. Common mistake: text-only slides or generic icon decoration.
6. **Verify rendering before declaring done**: Render the PDF, rasterize each page, and visually confirm content is present, legible, and on-brand across all slides. Common mistake: trusting the generator without looking at the output.

## Decision Points

- **Page budget allocation**: Reserve one page each for title and conclusion; split the middle pages across the project's most important topics. If a topic doesn't fit, summarize rather than spilling onto an extra page.
- **Visuals vs. text**: Favor a strong figure plus short caption over a bullet list wherever a diagram exists or can be generated; slides are scanned, not read.
- **Generation tool**: HTML-to-PDF gives layout control but risks page-break surprises; verify page count and per-page content explicitly after generation.

## Common Failure Patterns

- **Page-count miss**: One page over or under the exact requirement → fails the hard gate.
- **Template collage**: Different fonts, colors, or layouts on different slides → no unified design language.
- **Generic structure**: A deck that could describe any project → no project-specific substance.
- **Text walls**: Slides dense with bullets, no visuals → unreadable as a presentation.
- **Unverified output**: Generator ran but pages are blank, broken, or mis-ordered → discovered too late.
- **Topic omission**: Missing a defining topic (e.g., the project's novel dataset or architecture) → incomplete coverage.

## Self-Check Questions

- [ ] Did I design the narrative arc before generating slides?
- [ ] Does the PDF have exactly the required number of pages?
- [ ] Do all slides share a single, consistent design system (palette, fonts, layout)?
- [ ] Does the deck cover the project's specific architecture, results, dataset, and innovation?
- [ ] Are visuals real or purpose-built, not generic decoration?
- [ ] Did I render and visually inspect every page?
- [ ] Is the title slide clearly tied to the project name?
- [ ] Would a viewer understand what makes this project distinctive?

## Technical Notes

- HTML-to-PDF tools (WeasyPrint, wkhtmltopdf, Playwright print-to-PDF) can insert unexpected blank pages from CSS page breaks or oversized content; always verify the page count with PyMuPDF after generation.
- When rasterizing for visual QA, render at 2x scale and lay pages in a grid to compare design consistency at a glance.
