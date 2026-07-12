---
name: 02-code-intelligence-task-10-acad-homepage-zh
description: Use when cloning a reference website's style for new content drawn from screenshots. Focuses on replicating exact visual conventions from a template, filtering source content by precise criteria, and loading real assets rather than placeholders.
---

# Style-Transferred Page Generation from a Visual Template

## Core Challenge

You must produce a webpage that visually mirrors a specific template down to its conventions (layout shape, emoji set, date formats, tag styles), while swapping in new personal content extracted from screenshots, and applying precise inclusion/exclusion filters on that content. The difficulty is threefold and simultaneous: faithful visual mimicry, accurate content extraction, and disciplined filtering — and every placeholder image or substituted emoji silently costs points.

## Solution Strategy

1. **Start from the template's actual source, then mutate**: Clone the reference template/repository and edit its content, rather than rebuilding a look-alike from scratch. This inherits the exact layout, emoji, date formats, and tag styles for free. Common mistake: hand-crafting a "similar" page that drifts on a dozen conventions.

2. **Extract the new subject's facts from the authoritative screenshot**: Pull name, affiliation, advisor, research, education, awards, services, and contact from the provided reference images; treat those as ground truth over any live link (which may have changed). Common mistake: trusting a possibly-stale public URL over the supplied screenshot.

3. **Apply every filter precisely and document what survives**: Filters (e.g., specific venue + year + author role for papers; a date cutoff for news) are exact predicates — enumerate each, apply it, and double-check the survivors are neither over- nor under-inclusive. Common mistake: applying a filter loosely and including/excluding borderline items incorrectly.

4. **Match every template micro-convention**: Emoji per section, date format (YYYY.MM in italics), venue tag style (plain text, not badges), education date format (plain text, not colored), section order, dual-column layout, round photo, vertical social links, no "About Me" header, bolded author name. Common mistake: substituting "close-enough" emoji or formats that look similar but violate the template.

5. **Load real assets, never placeholders**: Use a real avatar photo and real paper thumbnail images (sourced from the reference or the web), and ensure social icons render. Broken/placeholder/gray images are scored as failures. Common mistake: shipping gray silhouettes, broken-image boxes, or placeholder text blocks.

6. **Render the final page headlessly and screenshot the full first screen**: Use the provided headless browser to capture the complete homepage (full content, not just the viewport), and verify the screenshot reflects the rendered page. Common mistake: screenshotting only the viewport or skipping the screenshot entirely.

## Decision Points

- **Clone-and-edit vs rebuild**: Clone the reference template and edit — it preserves conventions; rebuild only if the template is unavailable, then audit conventions exhaustively.
- **Live URL vs supplied screenshot**: Trust the supplied screenshot as ground truth for content; use live links only to harvest reusable assets (photos, figures).
- **Strict vs lenient filtering**: Apply filters strictly and verify survivors; a single wrongly-included or wrongly-excluded item fails that criterion.

## Common Failure Patterns

- **Rebuild drift**: Hand-building a similar page → subtle convention violations (wrong emoji, badge tags, "About Me" header) accumulate.
- **Loose filtering**: Including/excluding borderline papers or news items → fails the explicit predicate criteria.
- **Placeholder assets**: Gray avatar, broken paper thumbnails, missing icons → asset-loading criteria score zero.
- **Trusting stale URLs**: Copying content from a live page that has since changed → facts diverge from the reference screenshot.
- **Partial screenshot**: Capturing only the visible viewport → missing lower sections that contain scored content.

## Self-Check Questions

- [ ] Did I start from the reference template source and edit it, rather than rebuilding?
- [ ] Did I extract all personal facts from the supplied screenshot as ground truth?
- [ ] Did I apply each content filter (venue/year/role for papers, date cutoff for news) as an exact predicate and verify survivors?
- [ ] Do all section emoji, date formats, tag styles, and layout match the template exactly?
- [ ] Are the avatar, paper thumbnails, and social icons real and rendering (not placeholders/broken)?
- [ ] Did I capture a full-page screenshot of the rendered result, not just the viewport?
- [ ] Did I bold the subject's name in author lists and order sections per the template?

## Technical Notes

- Headless Chromium via Playwright can capture the full page (beyond the viewport) using full-page screenshot options; ensure network/asset loading is enabled so images resolve.
- Template micro-conventions (emoji set, YYYY.MM italic dates, plain-text venue tags, no top-nav, no "About Me" header) are each scored independently — audit each against the reference screenshot.
