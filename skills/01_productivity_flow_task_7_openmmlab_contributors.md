---
name: 01-productivity-flow-task-7-openmmlab-contributors
description: Use when aggregating per-contributor commit statistics across a dynamically-filtered repository set from a code-hosting platform. Focuses on metadata filtering, surviving API rate limits via bulk pagination, threshold-based inclusion, and exact-count integrity between coupled outputs.
---

# Filtering a Repo Set & Aggregating Per-Contributor Stats Under Rate Limits

## Core Challenge

The core difficulty has three layers. First, the working set is not given — it must be derived by applying metadata filters (fork status, repo type, an activity cutoff) to an organization's full repository list, and any error in that derivation cascades into every downstream count. Second, gathering commit data across the resulting set under a hostile anonymous-API rate limit forces a bulk-pagination strategy rather than naive iteration. Third, two outputs must stay referentially consistent: every project named in a contributor record must appear in the repo list, and threshold inclusion must be applied uniformly.

## Solution Strategy

1. **Derive the working set first and validate it before aggregating**: Apply the metadata filters (non-fork, project-type, activity cutoff by the platform's pushed-at timestamp) to enumerate exactly the qualifying repositories; write that set down and treat it as the source of truth for every subsequent join. Common mistake: aggregating against an ad-hoc or partially-filtered repo list, so counts reference repos that shouldn't qualify.
2. **Plan around the rate limit before the first call**: Anonymous platform APIs often allow only ~60 requests/hour; design for bulk endpoints with maximum page size, cache aggressively, and budget calls against the known working-set size. Common mistake: naive per-repo, per-contributor iteration that exhausts the quota after a few repos.
3. **Use the platform's aggregated contributor endpoint, not hand-counted commit lists**: Prefer the endpoint that returns per-user commit totals for a repo in one call over walking the full commit history. Common mistake: paginating through every commit to count per author, which multiplies the request count by orders of magnitude.
4. **Apply the threshold rule identically everywhere**: A contributor appears in the output if and only if they meet the commit threshold in at least one qualifying repo, and their project map includes exactly the repos where they meet it — no more, no less. Common mistake: including a repo where the contributor is below threshold, or omitting one where they clear it.
5. **Keep the two outputs referentially consistent**: Every project key in a contributor's record must be a name present in the repo-list output; never emit a project that wasn't in the filtered set. Common mistake: a contributor record references a repo that was filtered out or never listed.
6. **Emit each contributor exactly once with exact integer counts**: One record per user, project map mapping repo name to integer commit count; duplicates or non-integer counts break schema validation. Common mistake: splitting a contributor across multiple lines or emitting counts as strings.
7. **Normalize repo names consistently across outputs**: Use the same canonical form (e.g., the platform's exact repo name) in both the list and the project keys; comparison is often name-canonicalizing but mixing forms invites mismatches. Common mistake: using full names in one place and short names in another.

## Decision Points

- **Bulk endpoint vs commit walk**: Always prefer the platform's per-repo contributor-summary endpoint; only walk commits when the summary endpoint is unavailable for a repo.
- **Token vs anonymous access**: If an authenticated token is available, the rate budget is far larger; if not, design strictly for the anonymous budget with bulk pages and caching.
- **Threshold as include vs exclude**: The threshold defines inclusion (include contributors and repos that clear it); do not invert it into an exclusion rule that drops borderline-but-qualifying entries.

## Common Failure Patterns

- **Working-set drift**: Aggregating against a partially-filtered repo list → counts that reference non-qualifying repos and fail referential integrity.
- **Rate-limit exhaustion**: Naive iteration without bulk pagination → quota consumed before the working set is covered, leaving repos uncounted.
- **Threshold inversion**: Including repos where a contributor is below the threshold, or omitting ones where they clear it → project lists don't match the reference.
- **Cross-output inconsistency**: A project name in a contributor record that doesn't appear in the repo list → schema/referential checks fail.
- **Count source mismatch**: Hand-counting commits differently from the platform's own contributor totals → integer counts drift from the reference.
- **Duplicate or malformed records**: A contributor split across lines, or counts emitted as strings/floats → schema validation fails.

## Self-Check Questions

- [ ] Did I derive the working repository set by applying every metadata filter before aggregating?
- [ ] Did I plan my API call budget against the rate limit using bulk pagination and caching?
- [ ] Did I use the platform's aggregated contributor endpoint rather than walking commits?
- [ ] Is the threshold rule applied identically for contributor inclusion and for per-repo project entries?
- [ ] Does every project key in each contributor record appear in the repo-list output?
- [ ] Is each contributor emitted exactly once, with integer commit counts?
- [ ] Are repo names canonicalized consistently across both outputs?

## Technical Notes

- Anonymous code-hosting APIs typically enforce ~60 requests/hour; prefer `per_page=100` bulk endpoints and cache responses to survive the budget.
- The platform's per-repo contributor endpoint returns pre-aggregated commit counts per user — use it instead of reconstructing counts from commit history.
