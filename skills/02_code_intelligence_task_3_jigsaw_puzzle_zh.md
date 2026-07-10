---
name: 02-code-intelligence-task-3-jigsaw-puzzle-zh
description: Use when The core challenge is **multi-constraint combinatorial search with ambiguous similarity**: the agent must simultaneously solve three interdependent problems—identifying which 9 of 15 highly similar pi
---

# Jigsaw Puzzle Restoration — Filter, Rectify, and Reassemble Pieces

## Core Challenge

The core challenge is **multi-constraint combinatorial search with ambiguous similarity**: the agent must simultaneously solve three interdependent problems—identifying which 9 of 15 highly similar pieces belong to the original grid, determining each piece's rotation state, and finding their correct spatial arrangement—where naive greedy matching fails because distractor pieces (offset crops from the same image) create false positive edge alignments that only global consistency checking can disambiguate. 

Agents typically struggle with the exponential search space and the need to reason about relational constraints (edge compatibility) across multiple transformation states rather than treating piece selection and placement as independent classification tasks.

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


