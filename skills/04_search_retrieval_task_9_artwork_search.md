---
name: 04-search-retrieval-task-9-artwork-search
description: Use when an artwork must be identified from an image and its current physical location resolved at a specific date. Focuses on visual identification plus temporal-location verification, distinguishing permanent home from temporary exhibition.
---

# Artwork Identification and Time-Anchored Location

## Core Challenge

The task has two sequential identification steps: first identify the specific artwork from its image, then determine where it physically was at a particular point in time. Artworks travel on loan and exhibition tours, so the permanent-collection home and the date-specific location often differ — and the grade keys on the date-specific location, not the home. The difficulty is treating location as time-sensitive and verifying it against the target date rather than defaulting to the museum that owns the piece.

## Solution Strategy

1. **Identify the artwork before searching for its location**: Use visual features (style, subject, signature, medium) to name the specific work and artist first; the location query depends on the identity. Common mistake: skipping identification and searching the image generically.
2. **Extract the most identifying visual features**: Signature, title text, distinctive subject matter, and artist's known style are higher-yield than color palette. Common mistake: describing the image vaguely.
3. **Treat the target date as a hard constraint, not context**: The question is "where was it ON this date," which may differ from "where is it usually." Search specifically for exhibition/loan history around that date. Common mistake: returning the permanent home.
4. **Distinguish permanent collection from temporary exhibition**: Look for current exhibition, tour, or loan announcements spanning the target date. Common mistake: assuming the owning museum is the answer.
5. **Verify the date-specific location against an authoritative source**: The exhibiting institution's own "on view" page or exhibition calendar for that period is decisive; a travel blog is not. Common mistake: trusting a secondary source for a date-sensitive fact.
6. **Confirm, do not assume, when home and date-location coincide**: Even if the work is normally at its home, verify it was not on loan during the target window. Common mistake: skipping verification because the answer seems obvious.

## Decision Points

- **When the work is genuinely on loan during the target window**: Report the borrowing institution and the exhibition, with dates that span the target date.
- **When no exhibition is found for the window**: The permanent home is the likely answer, but state explicitly that no loan was active and cite the absence.
- **Conflicting exhibition claims**: Prefer the exhibiting institution's own calendar over third-party listings when they disagree.

## Common Failure Patterns

- **Permanent-home default**: Returning the owning museum without checking for a loan → wrong whenever the piece is traveling.
- **Date-agnostic location**: Treating "where is it" as timeless → ignores the time-sensitivity the task demands.
- **Weak identification**: Misidentifying the artwork → the entire downstream location search is off-target.
- **Secondary-source trust for a time-sensitive fact**: Trusting a blog that may be stale → location no longer accurate for the target date.
- **Skipping verification on the "obvious" case**: Not checking the loan calendar when the home seems right → silent error if a loan was active.

## Self-Check Questions

- [ ] Did I positively identify the specific artwork (title and artist) before locating it?
- [ ] Did I treat the target date as a hard constraint on location?
- [ ] Did I search for exhibition/loan/tour history spanning that specific date?
- [ ] Did I distinguish the permanent-collection home from a temporary exhibition venue?
- [ ] Did I verify the date-specific location against the exhibiting institution's own calendar?
- [ ] If the work appears to be at its home, did I confirm no loan was active in the window?
- [ ] Did I cite a source whose information is valid for the target date (not just currently)?

## Technical Notes

- Exhibition pages are often dated; check that the page's "on view" range actually covers the target date, not just the current month.
- Major artworks on tour generate press coverage and institution calendar entries at the borrowing venue — search both the owner's and the borrower's sites.
