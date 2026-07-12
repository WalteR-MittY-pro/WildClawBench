---
name: 02-code-intelligence-task-11-resume-homepage-zh
description: Use when building a styled personal page whose facts come from a structured document and whose look comes from a template screenshot. Focuses on extracting facts from a PDF source, applying precise academic filtering, and replicating exact template conventions without drift.
---

# Document-Grounded Page Generation with Template Fidelity

## Core Challenge

The page's facts must come from a PDF document (the authoritative source), its visual style from a separate template screenshot, and its content must survive a set of precise academic-status filters (author role, acceptance status, venue category, date window). Three independent sources of truth must be reconciled, each filter is an exact predicate, and every template micro-convention must be matched — while real assets load and nothing is left as a placeholder.

## Solution Strategy

1. **Treat the PDF as the single source of facts**: Extract name, affiliation, advisor, research, education, internship, awards, services, and contact from the resume PDF; treat any live link as only a source of reusable assets, never as authoritative content. Common mistake: copying content from a possibly-stale public homepage over the PDF.

2. **Clone the template and edit, do not rebuild**: Inherit the reference template's exact layout, emoji, formats, and section structure by forking it; rebuild only forces you to re-derive every convention. Common mistake: hand-authoring a "similar" page that drifts on layout, emoji, or tag styles.

3. **Apply each academic filter as a strict predicate**: Paper inclusion typically requires a specific author role (first/co-first), formal acceptance (not under review), and sometimes venue-category exclusion (e.g., no Findings); news requires a specific date window. Enumerate and apply each precisely. Common mistake: loose interpretation that includes borderline or excludes valid items.

4. **Match every template micro-convention**: Section emoji, date format (YYYY.MM italics), venue tag style (plain text), education date format (plain text), section order, dual-column layout, round avatar, vertical social links, no top-nav, no "About Me" header, vertical section stacking, standalone Educations section, bolded author name. Common mistake: substituting near-equivalents that still violate the template.

5. **Load real assets and verify rendering**: Use a real avatar photo and real paper figures (from the PDF, the reference, or the web); ensure social icons resolve. Placeholder/gray/broken images each fail independently. Common mistake: shipping broken thumbnails or a gray avatar.

6. **Screenshot the full page headlessly**: Capture the complete first page (full content, beyond the viewport) with the provided headless browser and confirm it reflects the rendered page. Common mistake: capturing only the visible viewport, missing scored lower sections.

## Decision Points

- **PDF vs live URL vs template screenshot**: PDF = facts, template screenshot = style, live URL = assets only. Never let a live URL override PDF facts.
- **Clone-and-edit vs rebuild**: Clone the template and edit to preserve conventions; rebuild only as a last resort with an exhaustive convention audit.
- **Strict vs lenient filtering**: Apply filters strictly and verify each survivor/exclusion against the exact predicate; one wrong inclusion or exclusion fails that criterion.

## Common Failure Patterns

- **Source confusion**: Letting a live homepage override the PDF → facts diverge from the authoritative source.
- **Rebuild drift**: Hand-building → convention violations (wrong emoji, badge tags, top-nav, "About Me" header, side-by-side sections) accumulate.
- **Filter looseness**: Including under-review or wrong-category papers, or news outside the date window → predicate criteria fail.
- **Placeholder assets**: Gray avatar, broken paper images, missing icons → asset criteria score zero.
- **Viewport-only screenshot**: Missing lower-page sections that contain awards/services/talks content.

## Self-Check Questions

- [ ] Did I extract all facts from the PDF as the authoritative source?
- [ ] Did I clone the template and edit it, rather than rebuilding from scratch?
- [ ] Did I apply each academic filter (author role, acceptance status, venue category, date window) as an exact predicate?
- [ ] Do all section emoji, date formats, tag styles, layout, and section ordering match the template exactly?
- [ ] Are the avatar, paper thumbnails, and social icons real and rendering?
- [ ] Did I capture a full-page screenshot (not just the viewport) of the rendered result?
- [ ] Did I bold the subject's name in author lists and include standalone Educations, Services, and Talks sections?

## Technical Notes

- Headless Chromium (Playwright) full-page screenshots capture content beyond the viewport; ensure assets load before capture.
- Each template micro-convention (emoji set, YYYY.MM italic dates, plain-text venue tags, no top-nav, vertical section stacking) is scored independently — audit each against the template screenshot, not memory.
