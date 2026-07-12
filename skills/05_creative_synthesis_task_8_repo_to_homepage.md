---
name: 05-creative-synthesis-task-8-repo-to-homepage
description: Use when turning an unfamiliar open-source repository into a polished, self-contained single-page project homepage. Focuses on autonomous project research, asset sourcing, responsive design, and verifiable rendering.
---

# Repository to Single-Page Project Homepage

## Core Challenge

The agent must independently research an unfamiliar code repository to understand what the project is and why it matters, source or generate the visual assets needed to make the page feel real (not stock-photo filler), design a responsive, professional single-file page, and then prove it renders correctly by capturing a real browser screenshot. The failure surface is broad: thin research, placeholder imagery, broken layout, or a page that only the author's machine renders correctly.

## Solution Strategy

1. **Research the project before touching markup**: Read the README, docs, and repo structure to extract the genuine value proposition, core features, supported models/benchmarks, and quick-start instructions. Common mistake: writing generic "a powerful tool for X" copy that could describe any project.
2. **Source real assets, not placeholders**: Use the project's actual logo, architecture diagrams, benchmark screenshots, or result visualizations; generate designed graphics only when real ones are unavailable. Common mistake: dropping in unrelated stock images or empty divs.
3. **Plan the content sections around what a visitor needs**: Cover at minimum introduction, key features, supported scope, quick start, and links — structured so a first-time visitor can orient in seconds. Common mistake: omitting a quick-start or citation/community section.
4. **Build responsive and self-contained**: Include a correct viewport meta tag and real media queries for mobile; inline or embed all CSS and assets so the single file renders anywhere without external dependencies. Common mistake: relying on external CDNs that may be unreachable, or skipping responsive rules.
5. **Render and capture to verify, not assume**: Use a headless browser to screenshot the full page at a defined viewport width, and inspect the screenshot for broken images, layout collapse, or empty regions. Common mistake: shipping unverified markup that looks fine in source but renders broken.
6. **Hit all structural anchors**: Confirm the project name, a link to the repo, a navigation element, a minimum image count, and a minimum section count are all actually present in the rendered DOM. Common mistake: counting decorative svgs or background images that don't meaningfully count.

## Decision Points

- **Research depth vs. breadth**: Prioritize the project's defining differentiators (what makes it unlike alternatives) over exhaustive feature lists; a homepage that conveys "why this, not that" beats a feature dump.
- **Asset realism**: Real project assets (logo, diagrams, result figures) always beat generated or stock substitutes; invest in extracting them from the repo before generating alternatives.
- **Verification path**: A headless-browser screenshot is the ground truth for what the page actually looks like; source-code inspection alone is insufficient because runtime rendering can differ.

## Common Failure Patterns

- **Generic copy**: "A powerful, modern framework" with no project-specific substance → reads as filler.
- **Placeholder imagery**: Empty divs, broken image links, or unrelated stock → page feels hollow.
- **Non-responsive**: Missing viewport tag or no media queries → fails mobile adaptation.
- **External dependencies**: CDN links that break when offline → single-file guarantee violated.
- **Unverified rendering**: Shipping source without a screenshot → broken layout goes unnoticed.
- **Thin section count**: Too few distinct content blocks → fails structural anchors.

## Self-Check Questions

- [ ] Did I research the repo deeply enough to write project-specific copy?
- [ ] Are the visual assets real (from the repo) or purpose-generated, not stock filler?
- [ ] Does the page cover introduction, features, scope, quick start, and links?
- [ ] Is there a viewport meta tag and at least one functional media query?
- [ ] Are all styles and assets inlined so the single file is self-contained?
- [ ] Did I capture a real browser screenshot at the required width?
- [ ] Does the screenshot show a complete, non-broken, professional layout?
- [ ] Are the project name, repo link, navigation, and minimum image/section counts present in the DOM?

## Technical Notes

- Playwright headless Chromium with `page.set_viewport_size` and `page.screenshot(full_page=True)` is the reliable path for full-page capture; set the viewport width explicitly before navigation.
- Inlined SVGs and data-URI images keep the file self-contained; external CDNs risk both the single-file guarantee and offline rendering.
