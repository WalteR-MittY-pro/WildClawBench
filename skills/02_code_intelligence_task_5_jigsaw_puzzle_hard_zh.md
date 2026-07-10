---
name: 02-code-intelligence-task-5-jigsaw-puzzle-hard-zh
description: Use when The core cognitive challenge is **combinatorial search under ambiguity with noisy similarity signals**. The agent must simultaneously solve three interdependent optimization problems—identifying which
---

# Hard Jigsaw Puzzle — 5×5 Pieces, Filter, Rectify, and Reassemble

## Core Challenge

The core cognitive challenge is **combinatorial search under ambiguity with noisy similarity signals**. The agent must simultaneously solve three interdependent optimization problems—identifying which 25 of 37 visually similar pieces are genuine, determining the rotation state of each genuine piece, and finding the correct spatial arrangement—while the intentionally inserted distractor pieces (offset crops from the same image) create highly plausible false matches that cannot be ruled out through simple perceptual heuristics. Success requires the agent to recognize that exact pixel-level edge alignment is the discriminative signal, then orchestrate a search strategy that explores the exponentially large solution space efficiently, balancing local pairwise constraints with global coherence rather than greedily committing to early matches.

## Solution Strategy


1. **Understand all requirements before acting**: Prevents missing critical constraints → Jumping to implementation without full context




## Common Failure Patterns


- **Incomplete requirement analysis**: Acting on partial information → Missing critical constraints


## Self-Check Questions


- [ ] Did I fully understand all requirements and constraints before starting?

- [ ] Have I validated my approach against ALL stated criteria?

- [ ] Did I analyze the code structure before making inferences?

- [ ] Did I verify the output format matches expectations?

- [ ] Have I checked for edge cases and error conditions?

- [ ] Did I test the complete workflow end-to-end?

- [ ] Have I confirmed all required information was gathered?

- [ ] Did I avoid making assumptions without verification?


