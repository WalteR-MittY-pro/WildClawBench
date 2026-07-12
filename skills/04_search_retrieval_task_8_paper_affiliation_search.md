---
name: 04-search-retrieval-task-8-paper-affiliation-search
description: Use when counting accepted papers by first-author affiliation across a conference program. Focuses on exhaustive list collection, affiliation parsing, and "first affiliation" disambiguation.
---

# Conference Paper Affiliation Aggregation

## Core Challenge

The agent must (a) obtain a complete list of a specific acceptance tier from a conference, then (b) for each paper determine the institution listed as the first affiliation — a field that is inconsistently formatted, often abbreviated or multilingual, and conflated with co-author affiliations. The difficulty is being exhaustive over the list and precise about what "first affiliation" means, without false positives from name similarity.

## Solution Strategy

1. **Obtain the official acceptance-tier list first**: Get the authoritative program page for the specific track (e.g., Oral/Spotlight/Poster), not a partial blog summary. Common mistake: working from an incomplete secondary list and missing papers.
2. **Confirm the list is complete and current**: Conferences publish tier lists in waves; verify you have the final version, not a partial early release. Common mistake: counting against an interim list.
3. **Define "first affiliation" precisely**: It is the affiliation of the first author as listed on the paper, or the first institution in the paper's affiliation block — decide the convention and apply it uniformly. Common mistake: counting any author's affiliation as a match.
4. **Normalize institution aliases**: The same university appears under many strings (full name, abbreviation, transliteration); build an alias set for each target institution before matching. Common mistake: matching only one spelling and undercounting.
5. **Verify per-paper, not per-guess**: For each paper in the list, open the actual paper or its metadata to read the affiliation — do not infer from the title or a co-author's known affiliation. Common mistake: inferring affiliation from author reputation.
6. **Count and list with evidence**: Report the count AND the matching paper titles, and be explicit about zero counts (an empty result is a valid finding). Common mistake: omitting the list, or omitting the zero case.

## Decision Points

- **Author-order vs. affiliation-block order for "first affiliation"**: When the first author's affiliation block lists multiple institutions, the convention is usually the first-listed institution; apply that rule consistently and note it.
- **Ambiguous or merged institutions**: If two institutions share a name root but are distinct entities, confirm the specific department/campus before counting.
- **Zero matches**: A count of zero is a legitimate answer; verify it by re-checking a sample of papers rather than padding the count to seem productive.

## Common Failure Patterns

- **Incomplete list**: Working from a partial program → undercount regardless of affiliation accuracy.
- **Any-author matching**: Counting a paper because some co-author is from the target institution → inflates the count.
- **Alias blindness**: Matching only one spelling of the institution → misses papers with the same institution under a different string.
- **Inference from reputation**: Assigning an affiliation based on the author's known home → wrong for visiting/collaborative papers.
- **Hidden zero**: Not reporting a zero count because "no matches found" feels like failure → the answer is incomplete.

## Self-Check Questions

- [ ] Did I obtain the official, complete, final list for the specific acceptance tier?
- [ ] Did I define "first affiliation" precisely and apply it uniformly?
- [ ] Did I build an alias set covering full names, abbreviations, and transliterations?
- [ ] For each paper, did I read the actual affiliation rather than infer it?
- [ ] Did I match on the first author's affiliation only, not any co-author's?
- [ ] Did I report both the count and the list of matching titles?
- [ ] If a target had zero matches, did I state that explicitly?

## Technical Notes

- Conference program pages sometimes paginate or load papers via JavaScript; ensure the full tier list is loaded before enumerating.
- OpenReview/CVF pages expose per-paper metadata including author affiliations; prefer those structured fields over parsing the PDF.
