---
name: 03-social-interaction-task-4-chat-thread-consolidation
description: Use when The core cognitive challenge is **multi-step information reconciliation across conflicting revisions**, where the agent must track correction chains through multiple messages to distinguish between ou
---

# Chat Message Thread Consolidation with Contradiction Detection

## Core Challenge

The core cognitive challenge is **multi-step information reconciliation across conflicting revisions**, where the agent must track correction chains through multiple messages to distinguish between outdated corrections (Alice's "fixed" 70% is still wrong) and authoritative updates (Bob's 60% is correct), while integrating new dependencies that cascade through the critical path. Agents typically struggle to maintain a temporal model of which correction supersedes which, especially when intermediate corrections appear authoritative but are explicitly contradicted later, requiring the agent to weight source reliability and cross-reference assertions rather than simply taking the most recent value per metric. The strategic difficulty lies in recognizing that surface-level "corrections" may themselves be errors requiring further correction, demanding careful dependency tracking to understand how a late-breaking issue (QA security finding) invalidates previous timeline calculations by introducing new blocking work.

## Solution Strategy


1. **Understand all requirements before acting**: Prevents missing critical constraints → Jumping to implementation without full context




## Common Failure Patterns


- **Incomplete requirement analysis**: Acting on partial information → Missing critical constraints


## Self-Check Questions


- [ ] Did I fully understand all requirements and constraints before starting?

- [ ] Have I validated my approach against ALL stated criteria?

- [ ] Did I consider all stakeholders' perspectives and constraints?

- [ ] Did I verify the output format matches expectations?

- [ ] Have I checked for edge cases and error conditions?

- [ ] Did I test the complete workflow end-to-end?

- [ ] Have I confirmed all required information was gathered?

- [ ] Did I avoid making assumptions without verification?



## Technical Notes


- format

