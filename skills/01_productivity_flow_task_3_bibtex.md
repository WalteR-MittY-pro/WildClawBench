---
name: 01-productivity-flow-task-3-bibtex
description: Use when reconciling unreliable local artifacts (messy filenames, corrupted PDFs) against authoritative external metadata to produce renamed copies and canonical records. Focuses on degraded-input handling, exact byte preservation, and strict output-set minimality.
---

# Reconciling Corrupted Local Documents with Authoritative Metadata

## Core Challenge

The core difficulty is multi-source reconciliation under uncertainty: each local artifact may be damaged (missing pages, scribbles, truncated), so identifying signals must be extracted from whatever content survives and cross-referenced against an authoritative external source. The trap is that the easy path (trusting PDF metadata fields, inferring from filenames) is exactly what fails, while the reliable path (content fingerprinting, external lookup) is more work. A second axis is output hygiene: byte-identical copies, exact manifest schemas, and zero extra files are all hard constraints that zero the entire result if violated.

## Solution Strategy

1. **Identify by surviving content, never by metadata fields or filename**: Extract identifying signals (title text from the first readable page, arXiv ID from headers, author names) from the document body, then confirm via the authoritative external source. Damaged documents still usually expose enough body text to identify them. Common mistake: trusting embedded PDF metadata fields, which are frequently wrong or missing.
2. **Fingerprint inputs to track identity across renaming**: Hash each input file so that identity survives filename changes; the manifest must map original to renamed via content, not guesswork. Common mistake: keying by filename, which breaks when names are unreliable.
3. **Copy bytes verbatim, never re-export**: Renamed copies must be byte-identical to the input; use a raw file copy, not a PDF re-save. Common mistake: opening and re-saving the PDF, which changes bytes even if visually identical.
4. **Pull canonical records from the authoritative source, not reconstructed**: Official BibTeX must come from the platform's official page, reconstructed entries drift on field order and escaping. Common mistake: hand-writing BibTeX from extracted metadata instead of fetching the official entry.
5. **Apply filename-sanitization rules exactly and in order**: When a deterministic sanitization pipeline is specified (Unicode normalization, character replacement, whitespace collapse, trailing-dot strip, suffix append), execute each step in the prescribed order; skipping or reordering steps produces filenames that won't match. Common mistake: collapsing whitespace before character replacement, or forgetting the trailing-dot removal.
6. **Treat output minimality as a hard constraint**: Produce exactly the requested files and nothing else; intermediate archives, scripts, and debug logs must not appear in the output tree. Common mistake: leaving extraction artifacts or helper scripts in the results directory.
7. **Count what is actually visible, not what should be there**: For damaged documents, count elements (figures, pages) that genuinely appear in the surviving pages, not the count the full document would have had. Common mistake: assuming the canonical figure count for a truncated PDF.

## Decision Points

- **When body text is unreadable**: Fall back to embedded metadata only as a last resort, and flag low confidence; cross-check any metadata-derived identity against an external source before committing.
- **Multiple candidate identities**: Prefer the match confirmed by the most independent signals (title + authors + arXiv header), not the single strongest signal.
- **One output per input vs filtering**: Include exactly one manifest entry and one renamed copy per qualifying input; exclude non-qualifying inputs entirely rather than erroring the whole batch.

## Common Failure Patterns

- **Trusting PDF metadata fields**: Reading embedded title/author metadata, which is frequently wrong → wrong identities and wrong canonical records.
- **Re-exported copies**: Re-saving PDFs during rename → byte-identity checks fail and the whole submission can be zeroed.
- **Hand-built BibTeX**: Constructing citation entries from extracted fields → field order, escaping, and key format diverge from the official entry.
- **Sanitization step reordering**: Applying whitespace collapse before character replacement → filenames that don't match the deterministic rule.
- **Output clutter**: Leaving helper scripts or extracted folders in results → minimality constraints penalized.
- **Assumed counts for damaged files**: Using the known-good figure count for a truncated PDF → count mismatch on exactly the inputs weighted most heavily.

## Self-Check Questions

- [ ] Did I identify each document from surviving body content, not from metadata fields or filenames?
- [ ] Are renamed copies byte-identical to the inputs (verified by hash, not by visual inspection)?
- [ ] Did I fetch canonical records (BibTeX) from the authoritative source rather than reconstructing them?
- [ ] Did I apply the filename-sanitization pipeline in the exact order specified?
- [ ] For damaged documents, did I count only what is actually visible in the surviving pages?
- [ ] Does the manifest contain exactly one entry per qualifying input with the exact required fields and no extras?
- [ ] Is the output tree free of any files beyond those explicitly requested?

## Technical Notes

- Hash inputs (e.g., SHA-256) to track identity through renames; filenames are unreliable in this class of task.
- Use raw byte copy (`shutil.copyfile` or equivalent), never a PDF library re-save, to preserve byte identity.
