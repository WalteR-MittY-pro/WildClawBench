---
name: 02-code-intelligence-task-4-jigsaw-puzzle-medium-zh
description: Use when The core cognitive challenge is **combinatorial reasoning under ambiguity with noisy similarity signals**. Agents must distinguish genuine jigsaw pieces from visually similar distractors that share th
---

# Medium Jigsaw Puzzle — 4×4 Pieces, Filter, Rectify, and Reassemble

## Core Challenge

The core cognitive challenge is **combinatorial reasoning under ambiguity with noisy similarity signals**. Agents must distinguish genuine jigsaw pieces from visually similar distractors that share the same content and style but are spatially misaligned, requiring precise edge-matching algorithms rather than heuristic similarity measures. The task demands jointly optimizing piece selection, rotation detection, and spatial placement across a large search space (24 choose 16 × 4^16 rotations × 16! arrangements), where local greedy decisions easily lead to dead ends and global constraint satisfaction is necessary to filter out the carefully designed interference.

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


