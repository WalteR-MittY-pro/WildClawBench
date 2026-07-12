---
name: 04-search-retrieval-task-11-fuzzy-repo-search
description: Use when a repository must be pinpointed from several indirect circumstantial clues. Focuses on candidate-set generation, clue-by-clue elimination, and resisting fixation on the most famous candidate.
---

# Multi-Clue Repository Disambiguation

## Core Challenge

Several indirect clues (implementation language, naming reference, creator's other projects, a technical innovation, a popularity threshold) collectively identify one repository, but no single clue is decisive and several famous candidates satisfy some clues. The agent must generate a candidate set, then eliminate rigorously clue-by-clue, rather than jumping to the most famous project that superficially fits the topic.

## Solution Strategy

1. **Generate a broad candidate set from the topic clue first**: Query the problem domain (e.g., "run LLMs on consumer hardware") to enumerate several plausible projects before applying fine clues. Common mistake: searching for the single "right" project and missing alternatives.
2. **List every clue as an elimination predicate**: Treat each clue (language, name reference, creator history, technical artifact, star count) as a must-pass filter, not a hint. Common mistake: using clues as soft signals and averaging.
3. **Apply the most discriminating clues first**: The clue that eliminates the most candidates (e.g., "creator also built X") should be checked before the clue many candidates share (e.g., "written in C/C++"). Common mistake: confirming the easy shared clue and declaring victory.
4. **Verify each clue from a primary source**: Check the repo's own README, the creator's profile, and the repo's file format docs — not a secondary roundup. Common mistake: trusting a blog's summary of what a project does.
5. **Beware the famous-candidate trap**: The most popular project in a domain often satisfies the topic clue but fails a circumstantial clue; do not let fame substitute for verification. Common mistake: picking the household-name project that misses the naming or creator clue.
6. **Confirm the survivor against ALL clues before answering**: The final pick must pass every clue, with evidence for each. Common mistake: confirming four of five clues and hand-waving the fifth.

## Decision Points

- **When two candidates survive most clues**: Use the single most discriminating clue (often the creator-history or naming clue) as the tiebreaker, verified from a primary source.
- **Famous candidate vs. lesser-known correct one**: Always prefer the candidate that satisfies the circumstantial clues over the one that is merely well-known for the topic; fame is not a clue.
- **Clue that is hard to verify**: If one clue resists verification, do not discard the candidate — but do not assert the clue either; keep the candidate only if all other clues pass decisively.

## Common Failure Patterns

- **Fame bias**: Picking the most famous project in the domain → wrong when it fails a circumstantial clue.
- **Easy-clue fixation**: Confirming the shared clue (language) and stopping → multiple candidates still alive.
- **Soft averaging**: Treating clues as weighted hints → picks the candidate with the most "kinda" matches instead of the one that passes all.
- **Secondary-source trust**: Accepting a blog's characterization of a project → may misstate the distinguishing clue.
- **Premature singleton**: Locking onto one candidate before enumerating alternatives → never considers the correct one.

## Self-Check Questions

- [ ] Did I generate a broad candidate set before applying fine clues?
- [ ] Did I treat every clue as a must-pass filter rather than a soft hint?
- [ ] Did I apply the most discriminating clue first?
- [ ] Did I verify each clue from a primary source (repo, creator profile, format docs)?
- [ ] Did I resist picking the most famous candidate when it fails a circumstantial clue?
- [ ] Does my final pick pass EVERY clue, with evidence for each?
- [ ] If two candidates were close, did I break the tie with the single most selective clue?

## Technical Notes

- GitHub repository metadata (primary language, star count, owner's other repos) is directly available from the repo page or API; use it for verification rather than third-party rankings.
- A custom file format introduced by a project is usually documented in the repo's README or a dedicated format spec; confirm the "pioneered by" claim there, not from community adoption summaries.
