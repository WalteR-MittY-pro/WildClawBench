---
name: 04-search-retrieval-task-7-location-search
description: Use when a geographic location must be derived from a photo of a place. Focuses on diagnostic visual-feature extraction, query formulation from landmarks, and coordinate verification.
---

# Image-to-Location Geolocation

## Core Challenge

A photo gives no explicit location text, so the agent must extract diagnostic visual features (signage, architecture, skyline, vegetation, transit livery), convert them into searchable queries, and converge from candidate regions to a specific city and coordinate. The difficulty is distinguishing features that uniquely pin a place from features that are generic, and knowing when a hypothesis is confirmed versus merely plausible.

## Solution Strategy

1. **Inventory every visible text-bearing surface first**: Signs, shop names, transit labels, license plates, and storefronts are the highest-yield clues; transcribe them exactly before searching. Common mistake: skipping text and guessing from skyline alone.
2. **Separate diagnostic from generic features**: A unique building or local-language sign is diagnostic; trees, sky, and weather are not. Rank clues by selectivity. Common mistake: overweighting aesthetic features that could be anywhere.
3. **Query the most selective clue, not the whole scene**: A distinctive business name or transit line returns the city in one search; a generic "modern building with river" returns nothing useful. Common mistake: describing the image in prose instead of searching a specific identifier.
4. **Cross-check the candidate against the image**: Once a candidate location is hypothesized, verify that the visible landmarks actually exist there (street view, photos) before committing. Common mistake: accepting the first plausible region without visual confirmation.
5. **Resolve to city, then to precise coordinate**: Narrow country → city → specific landmark, and only then look up the coordinate of that landmark. Common mistake: guessing coordinates before the landmark is confirmed.
6. **Use the right precision for the answer**: Report coordinates to the precision the task demands; over-precise invented decimals are a red flag for guessing. Common mistake: inventing decimal places not supported by the source.

## Decision Points

- **Text vs. architecture as lead clue**: Prefer readable text when present (it is unambiguous); fall back to architectural style only when no text is visible.
- **Multiple candidate cities with similar features**: Use a second, independent diagnostic clue to disambiguate rather than picking the more famous candidate.
- **When the landmark is confirmed but the coordinate is uncertain**: Use the landmark's officially published coordinate (museum, square, station) rather than estimating from the photo framing.

## Common Failure Patterns

- **Skyline-only guessing**: Naming a famous city because the skyline "looks like" it → wrong when the photo is of a lesser-known district.
- **Ignoring local-language text**: Treating non-Latin signage as decoration → discards the single most selective clue.
- **Plausibility-as-truth**: Settling on a region that "could be right" without visual cross-check → confident but unverified.
- **Coordinate fabrication**: Reporting a coordinate to many decimals without a source → guess dressed as precision.
- **Premature commitment**: Locking onto the first hypothesis and ignoring disconfirming features in the image.

## Self-Check Questions

- [ ] Did I transcribe every visible text element before searching?
- [ ] Did I rank clues by selectivity and query the most diagnostic one?
- [ ] Did I distinguish generic features from ones that uniquely identify a place?
- [ ] Did I cross-check my candidate location against the image via independent photos?
- [ ] Did I narrow country → city → specific landmark in that order?
- [ ] Is my coordinate sourced from the confirmed landmark, not invented?
- [ ] Did I disambiguate between similar-looking candidate cities with a second clue?

## Technical Notes

- Reverse-image search and multimodal vision APIs can surface near-duplicate photos that already name the location; use them as a hypothesis source, then verify the claim against the original image.
- Coordinates should match the precision the task specifies; rounding to the requested decimals is safer than over-reporting fabricated precision.
