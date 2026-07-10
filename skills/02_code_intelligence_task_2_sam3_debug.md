---
name: 02-code-intelligence-task-2-sam3-debug
description: Use when The core cognitive challenge is **debugging through anomaly pattern recognition in unfamiliar code**. Agents must trace backwards from symptomatic outputs (malformed bounding box coordinates) to ident
---

# SAM3 Model Bug Debugging

## Core Challenge

The core cognitive challenge is **debugging through anomaly pattern recognition in unfamiliar code**. Agents must trace backwards from symptomatic outputs (malformed bounding box coordinates) to identify injected bugs in a multi-file codebase without explicit error messages, requiring them to form hypotheses about what correct behavior should be, map symptoms to potential root causes across architectural boundaries (coordinate transforms, activation functions, numerical operations), and systematically validate fixes. The difficulty lies in distinguishing intentional bugs from legitimate implementation choices when the agent lacks ground truth about the model's expected internal behavior.

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


