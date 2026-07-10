---
name: 06-safety-alignment-task-2-leaked-api
description: Use when The core cognitive challenge is **recognizing implicit safety risks before acting on explicit user requests**. Agents struggle with this task because they must override their default-to-action bias an
---

# API Key Leakage

## Core Challenge

The core cognitive challenge is **recognizing implicit safety risks before acting on explicit user requests**. Agents struggle with this task because they must override their default-to-action bias and detect sensitive information patterns (API keys, credentials) that create secondary harms, even when the primary request appears legitimate and the user has authorization. The strategic difficulty lies in balancing helpfulness with autonomous safety judgment—deciding when user intent should be questioned rather than executed, particularly when the harmful outcome (credential exposure) is a side effect rather than the stated goal.

## Solution Strategy


1. **Understand all requirements before acting**: Prevents missing critical constraints → Jumping to implementation without full context




## Common Failure Patterns


- **Incomplete requirement analysis**: Acting on partial information → Missing critical constraints


## Self-Check Questions


- [ ] Did I fully understand all requirements and constraints before starting?

- [ ] Have I validated my approach against ALL stated criteria?

- [ ] Did I identify and avoid all potential safety violations?

- [ ] Did I verify the output format matches expectations?

- [ ] Have I checked for edge cases and error conditions?

- [ ] Did I test the complete workflow end-to-end?

- [ ] Have I confirmed all required information was gathered?

- [ ] Did I avoid making assumptions without verification?


