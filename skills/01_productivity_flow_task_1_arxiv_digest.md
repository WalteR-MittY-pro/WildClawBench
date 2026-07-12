---
name: 01-productivity-flow-task-1-arxiv-digest
description: Use when compiling a periodic digest from a paper source that must classify items into fixed categories, extract per-item metadata, and produce personalized recommendations. Focuses on classification, deep document parsing with internal-consistency constraints, and context-aware prioritization.
---

# Academic Paper Digest & Metadata Auditing

## Core Challenge

The fundamental difficulty is orchestrating a multi-stage pipeline where each stage transforms data differently (raw feed → category labels → precise tabular metadata → personalized picks), and where later stages demand deep document inspection whose accuracy is judged against strict internal-consistency rules. The hardest sub-problem is not classification but *granular metadata auditing* — distinguishing main-paper content from appendix content and verifying that split counts add up — because it requires actually reading the document structure rather than trusting summary fields.

## Solution Strategy

1. **Enumerate every output obligation up front**: A digest task bundles several independent deliverables (classification, metadata table, recommendations, benchmark extraction) that are graded separately and can silently drop if not tracked. Common mistake: treating it as "summarize papers" and producing only the most salient section while omitting the tedious table.
2. **Fetch the full set before classifying**: Classification accuracy requires the complete day's listing, not a sample, because papers are partitioned into exhaustive buckets including a catch-all. Common mistake: classifying only the first page of results and leaving the catch-all nearly empty.
3. **Classify from titles plus abstracts, not titles alone**: A title often omits the modality (e.g., a medical paper whose title is a method name). Reading the abstract is cheap insurance against systematic miscategorization. Common mistake: keyword-matching on titles and producing cross-category errors.
4. **Audit metadata by reading document structure, not metadata fields**: Figure/table counts and appendix boundaries live in the rendered document (HTML/PDF body), and totals must equal `main + appendix`. Treat that arithmetic as a hard self-check you re-derive after counting. Common mistake: pulling counts from a summary field or counting subfigure markers like "(a)/(b)" as separate figures.
5. **Establish the appendix boundary explicitly before counting**: Decide where the main paper ends (first appendix/supplementary heading) and count everything after it as appendix; record the heading text as evidence. Common mistake: counting all figures together and guessing a split, which breaks the total-consistency invariant.
6. **Make recommendations defensible against the stated research profile**: The "papers of interest" pick must map to concrete signals in the user's profile (their own method, their topic), and benchmark comparisons must be lifted verbatim from the source table — rows, columns, and the user's method included. Common mistake: generic "this looks relevant" justifications or omitting the user's own method from the comparison.

## Decision Points

- **HTML vs PDF for metadata**: Prefer the arXiv HTML rendering when available — figure/table environments are reliably delimited there. Fall back to PDF only when HTML is missing or structurally degraded.
- **Exhaustive vs sampled fetch**: If the API supports date-scoped listing, fetch exhaustively; pagination must continue until the date boundary is passed. Never sample.
- **Single best recommendation vs multiple**: Follow the literal cardinality the request specifies (e.g., "exactly 1"); over-delivering recommendations is as wrong as under-delivering.

## Common Failure Patterns

- **Section omission via under-scoping**: The agent produces the easy sections and skips the tedious metadata table because it "looks done" → loses the largest-graded component.
- **Metadata from the wrong layer**: Trusting abstract-page metadata or abstract text for figure counts → counts that don't match the document body and fail the main+appendix=total invariant.
- **Partial author lists**: Copying only the first few authors shown in a collapsed UI → author-completeness checks fail silently.
- **Reconstructed benchmark tables**: Recreating a comparison table from memory or paraphrase instead of copying the actual cells → numeric values drift and the user's own method row is missing.
- **Category leakage**: A paper that fits two buckets gets placed in both, or a paper with no clear fit is dropped instead of routed to the catch-all → exhaustiveness violated.

## Self-Check Questions

- [ ] Have I listed every required section before starting, and confirmed each will exist in the final file?
- [ ] Did I fetch the complete paper set for the requested date, not just the first page?
- [ ] For each metadata row, did I read the actual document body to count figures and tables?
- [ ] Did I split counts into main vs appendix using an explicit boundary heading, and does main+appendix equal total for both figures and tables?
- [ ] Is the author list complete for every audited paper, not truncated?
- [ ] Does my recommendation map to a concrete signal in the user's stated research profile?
- [ ] If a benchmark comparison is requested, did I copy the user's own method row verbatim from the source?
- [ ] Did I use the exact section headings and nesting levels the request specifies?

## Technical Notes

- arXiv listing APIs return Atom/XML; parse with an XML parser, not string matching, to handle author entities and escaped characters correctly.
- When counting figures from HTML, count top-level `<figure>` environments, not nested subfigure markers.
