---
name: 01-productivity-flow-task-4-2022-conference-papers
description: Use when compiling a structured bibliography for an author and publication window, pulling each field from a designated source and emitting a dataset plus underlying sources. Focuses on source-tier discipline, multi-platform entity resolution, and strict output-set control.
---

# Author-Bounded Bibliography Compilation with Provenance Tiers

## Core Challenge

The core difficulty is enforcing a strict provenance hierarchy across many heterogeneous sources: each field has a designated source-of-truth (official proceedings for title/authors/abstract, personal homepages for links, repository history for commit ids), and the agent must resist the temptation to fill any field from whatever source is closest. A second axis is scope discipline — including only main-conference papers in the exact year window, excluding workshops/arXiv/journals — where over- or under-inclusion cascades into many field errors. Output hygiene (exact TSV schema, no extra files, recovered source files matching byte-for-byte) rounds out the challenge.

## Solution Strategy

1. **Lock the scope with explicit inclusion/exclusion rules first**: Define precisely what counts (main conference proceedings, target year) and what does not (workshops, tutorials, arXiv-only, journal versions), then enumerate candidates against that filter before extracting any fields. Common mistake: grabbing anything that mentions the author and the year, which inflates the candidate set with workshop and arXiv papers.
2. **Assign each field to its designated source and never substitute**: Conference/title/authors/abstract come from official proceedings; author links from personal homepages; commit ids from repository history. Crossing these tiers silently introduces errors. Common mistake: copying the abstract from arXiv when the proceedings abstract differs slightly.
3. **Resolve entities across platforms by title, not by heuristic**: Match a proceedings entry to its arXiv source and its repository by exact title, then carry identity forward; never assume the "first hit" repository belongs to the paper. Common mistake: matching on partial title strings and associating the wrong repository.
4. **Recover source files from the canonical source package**: The requested `.tex` files must come from the platform's source archive for each version, identified as the primary top-level document file; do not reconstruct from the PDF. Common mistake: emitting PDF-extracted text and calling it source.
5. **Validate structural invariants before finishing**: The tabular output must have the exact header, one row per paper, no embedded newlines, correct sort order, and author-links aligned one-to-one with the author list. Common mistake: an author appearing in the author list but missing from the links field, or vice versa.
6. **Treat the output directory as a closed set**: Emit exactly the requested tabular file plus the requested source files; any leftover archive, extracted folder, or scratch file is penalized. Common mistake: leaving the downloaded source tarball in the results directory.
7. **Resolve dynamic values to the specified point in time**: When a commit id is requested as-of a specific date, query the repository history at that date rather than the current tip. Common mistake: recording the latest commit at run time, which drifts from the as-of requirement.

## Decision Points

- **Proceedings vs arXiv for a field**: Default to proceedings for all bibliographic fields; use arXiv only to locate the source package, not to populate the table.
- **Personal homepage vs secondary profile**: Prefer a personal academic site over Scholar/DBLP/ORCID/LinkedIn when both exist; use `not found` rather than a low-confidence link.
- **Multiple arXiv versions**: Save each version that actually exists as a separately versioned file; do not fabricate versions or collapse to one.

## Common Failure Patterns

- **Scope creep**: Including workshops, arXiv preprints, or journal versions → precision drops and downstream field errors multiply.
- **Source-tier violation**: Pulling the abstract from arXiv instead of proceedings → subtle wording differences fail normalized comparison.
- **Repository misattribution**: Linking a same-named but unrelated repository → wrong commit ids that may be structurally valid but factually wrong.
- **Author-link misalignment**: Link field out of order or missing an author → format-validity checks fail even when individual links are correct.
- **Output clutter**: Leaving archives or scratch files in results → directory-cleanliness penalty applied to the whole score.
- **Time-drifted commit ids**: Recording HEAD at runtime instead of the as-of date → commit ids that won't match the reference.

## Self-Check Questions

- [ ] Did I enumerate candidates against the inclusion/exclusion scope before extracting any fields?
- [ ] Does each field come from its designated authoritative source, with no tier substitutions?
- [ ] Did I resolve each paper to its arXiv source and repository by exact title match?
- [ ] Are the recovered source files the primary document files from the actual source archive?
- [ ] Does the tabular output have the exact header, correct sort order, and no embedded newlines?
- [ ] Is every author in the author list represented exactly once in the links field, in the same order?
- [ ] Are commit ids resolved to the specified as-of date, not the current repository tip?
- [ ] Is the output directory free of any files beyond the table and the requested source files?
