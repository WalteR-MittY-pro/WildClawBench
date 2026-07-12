---
name: 01-productivity-flow-task-2-table-tex-download
description: Use when recovering source artifacts (LaTeX environments, code blocks) from an academic archive and emitting each as a numbered file. Focuses on discovering access conventions, locating embedded environments across multi-file sources, and preserving exact ordering for positional matching.
---

# Recovering Source Environments from Academic Archives

## Core Challenge

The core difficulty is that the task assumes implicit domain knowledge (how to reach an arXiv source package rather than the PDF, how LaTeX structures documents) and grades on positional exactness: each extracted environment must be the n-th one in document order and byte-faithful to the original. Agents fail not because extraction is conceptually hard but because they guess the archive URL, merge or skip tables, wrap output in prose, or lose ordering when environments are split across included files.

## Solution Strategy

1. **Discover the source-archive convention before downloading**: Academic platforms expose source via a stable, inferable URL pattern distinct from the abstract/PDF URLs; confirm you have the archive (tarball/zip), not the rendered PDF. Common mistake: downloading the PDF and trying to reconstruct LaTeX from it, which can never match the original source.
2. **Enumerate all target environments in true document order**: Walk the primary document file (resolving includes) and record every environment occurrence by its position in the rendered document, not by its source-line position. Common mistake: extracting in file order when includes reorder content.
3. **Extract each environment as an intact, unwrapped unit**: Copy the complete environment from opening to closing delimiter with no surrounding prose, no markdown fences, no commentary; the grader normalizes whitespace but not added text. Common mistake: wrapping each table in a markdown code fence or prefixing it with a description.
4. **Use dense sequential numbering with no gaps**: Files named 1, 2, 3... must be contiguous and start at 1; the n-th file must correspond to the n-th environment. Common mistake: zero-indexing, skipping a table that looks trivial, or reusing the paper's own table numbers.
5. **Clean up the downloaded archive after extraction**: Source packages are bulky and not part of the requested output; leaving them creates clutter that may be penalized. Common mistake: leaving the tarball and extracted tree in the workspace.
6. **Preserve original formatting within each environment**: Keep comments, alignment characters, and multi-line structure intact; normalization is the grader's job, not yours. Common mistake: tidying the LaTeX, which changes normalized equality.

## Decision Points

- **Single main file vs multi-file project**: Identify the top-level document file and follow includes to find environments; environments may live in separate chapter or table files.
- **Table vs non-table environments**: Match only the requested environment type (e.g., the full table container, not the inner tabular alone); use the outer container delimiter.
- **When two candidate sources exist**: Prefer the version-of-record source package on the platform over any author-hosted mirror.

## Common Failure Patterns

- **PDF reconstruction**: Rebuilding LaTeX from the rendered PDF → output never matches the original source byte-for-byte.
- **Ordering collapse**: Sorting tables by caption or by source-line rather than rendered order → positional match fails even when content is correct.
- **Prose contamination**: Adding explanatory headers or markdown fences around each environment → added bytes break normalized equality.
- **Gap-in-sequence numbering**: Skipping unimportant tables or starting at 0 → the n-th file no longer maps to the n-th ground-truth environment.
- **Environment boundary errors**: Capturing only the inner tabular instead of the full enclosing table environment → missing caption or label that belong to the environment.

## Self-Check Questions

- [ ] Did I download the actual source archive, not the PDF?
- [ ] Did I follow include directives to find environments across all source files?
- [ ] Are my extracted environments in rendered document order, not file order?
- [ ] Is each file a bare environment with no markdown fences, comments, or prose wrapper?
- [ ] Are files contiguously numbered starting at 1 with no gaps?
- [ ] Did I capture the full outer environment (including caption and label), not just the inner tabular?
- [ ] Did I remove the downloaded archive and extracted tree from the output directory?
