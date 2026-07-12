---
name: 04-search-retrieval-task-6-excel-with-search
description: Use when an entity must be isolated from tabular data via compound filters, then combined with web knowledge for a derived calculation. Focuses on multi-filter row selection, cross-source numeric reasoning, and threshold-definition lookup.
---

# Compound-Filter Table Lookup with Web-Augmented Calculation

## Core Challenge

Two sub-tasks chain together: first, a single row must be isolated from a spreadsheet using several simultaneous categorical and numeric filters; second, a derived quantity must be computed by combining that row's value with a threshold whose definition lives outside the table (on the web). The difficulty is keeping the goal coherent across a context switch from structured filtering to open-web definition lookup, and not collapsing the two steps into a guess.

## Solution Strategy

1. **Parse the filter conjunction before touching data**: Write down every column predicate (e.g., region = X, role = Y, service-level = Z) and only then filter. Common mistake: applying filters one at a time from memory and dropping one.
2. **Filter on all categorical constraints, then rank by the numeric one**: Use the equality filters to shrink the set, then sort the survivors by the comparison field to find the extremum. Common mistake: sorting the whole table first and then checking categories only on the top row.
3. **Read across worksheets when data spans files**: The isolating data and the comparison data may live in different sheets/files; load both and key them on a shared identifier. Common mistake: assuming all needed columns are in one sheet.
4. **Treat the threshold definition as a separate lookup**: When the calculation needs "what counts as category X," that definition is domain knowledge on the web, not in the sheet. Common mistake: guessing the threshold from the data distribution.
5. **Compute the derived quantity explicitly and show the arithmetic**: State the threshold value, the entity's value, and the difference as a transparent calculation. Common mistake: reporting a number without showing what was subtracted from what.
6. **Verify the isolated entity against ALL filters one more time**: Before finalizing, re-confirm the chosen row meets every original predicate. Common mistake: a row slipped through a relaxed filter.

## Decision Points

- **Tie-breaking on the extremum**: If two rows tie on the ranking field, re-apply any remaining distinguishing filter; if still tied, report both rather than arbitrarily picking.
- **When the threshold definition is ambiguous**: The official classification scheme governs; if the web gives a numeric cutoff, use that exact cutoff rather than an inferred one.
- **Year-column ambiguity**: Datasets often have multiple year-suffixed columns (e.g., CY21 vs. FY23); confirm which column each predicate references before filtering.

## Common Failure Patterns

- **Filter dropout**: Mentally dropping one of several simultaneous filters → wrong row isolated.
- **Wrong-column sorting**: Sorting by a similarly-named column → extremum of the wrong metric.
- **Threshold guessing**: Inferring the category boundary from the data instead of looking it up → derived calculation off by the definition gap.
- **Cross-file key mismatch**: Joining two sheets on the wrong identifier → pulled the wrong entity's value into the calculation.
- **Hidden arithmetic**: Reporting a final integer without showing threshold minus actual → unverifiable and often a sign of a guess.

## Self-Check Questions

- [ ] Did I enumerate every filter predicate before selecting the row?
- [ ] Did I apply all categorical filters first, then rank by the numeric field?
- [ ] Did I confirm the isolating data and the comparison data come from the correct sheets/files?
- [ ] Did I look up the category-threshold definition on the web rather than guess it?
- [ ] Did I show the explicit arithmetic (threshold minus entity value) for the derived quantity?
- [ ] Did I re-verify the chosen row against every original filter before finalizing?
- [ ] Did I disambiguate same-prefixed year columns (e.g., CY vs. FY) correctly?

## Technical Notes

- Spreadsheet cells may hold mixed types (numbers stored as text); coerce before sorting or the extremum will be string-ordered, not numeric.
- Classification thresholds in regulated datasets (e.g., aviation, census) are published in an official document; cite that document for the cutoff, not a forum summary.
