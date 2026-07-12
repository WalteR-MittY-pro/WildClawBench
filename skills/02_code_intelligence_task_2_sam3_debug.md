---
name: 02-code-intelligence-task-2-sam3-debug
description: Use when a model inference script produces systematically wrong outputs due to injected logic bugs. Focuses on reading error patterns in outputs to localize and fix bugs in unfamiliar model code without a test harness.
---

# Debugging Injected Bugs in Model Code from Output Symptoms

## Core Challenge

The code runs without crashing, but produces visibly wrong results — negative coordinates, swapped dimensions, saturated outputs. There is no failing test pointing at a line; the only signal is the *shape of the wrongness*. The challenge is working backward from an output pathology to the exact faulty line across a large, unfamiliar codebase, while leaving correct code untouched.

## Solution Strategy

1. **Characterize the error before hunting**: Quantify *how* the output is wrong — are all boxes shifted, scaled, sign-flipped, axis-swapped, or clamped? Each pathology maps to a small family of root causes. Common mistake: opening files at random hoping to "spot" the bug.

2. **Let the symptom point to the subsystem**: Negative coordinates implicate box-conversion functions; value-range overflow implicates normalization; axis-swapped geometry implicates width/height handling; flat/saturated logits implicate the activation function. Common mistake: searching the whole repo generically instead of the subsystem the symptom implicates.

3. **Read the function, not the call graph**: For each candidate function, verify the math against first principles — is the numerator/denominator order correct, is the sigmoid actually a sigmoid, are width/height indexed correctly? Common mistake: assuming a function works because it's named correctly.

4. **Fix the minimal change and re-run**: Change only the proven-faulty logic, rerun, and check whether the output pathology disappears. One bug at a time keeps the search tractable. Common mistake: rewriting whole functions on suspicion and introducing new errors.

5. **Do not modify the harness**: When the test driver is off-limits, every fix must live in library/model code; treat the driver as ground truth and the library as suspect. Common mistake: "fixing" the driver to compensate, which masks the real bug.

## Decision Points

- **Symptom-driven localization vs line-by-line scan**: Always start from the symptom; scan line-by-line only as a last resort when the symptom is ambiguous.
- **Fix at the source vs compensate downstream**: Always fix at the function where the math is wrong; compensating downstream hides the bug and breaks other code paths.
- **Trust the original vs the "buggy" version**: When unsure whether a line is a bug or intentional, compare against the well-known correct form of that operation (e.g., standard IoU, standard sigmoid) — injected bugs deviate from the canonical implementation.

## Common Failure Patterns

- **Shotgun debugging**: Changing multiple things at once to "see what works" → can't tell which fix mattered, and new bugs creep in.
- **Symptom-blind searching**: Grepping for keywords without relating them to the observed pathology → wastes time on irrelevant code.
- **Trusting names over math**: Assuming `box_cxcywh_to_xyxy` is correct because of its name → the swapped operand inside goes unnoticed.
- **Patching the driver**: Editing the test script to force correct-looking output → the underlying library bug remains and is re-introduced next run.
- **Stopping at the first plausible fix**: Fixing one pathology and declaring done → a second injected bug in another subsystem remains.

## Self-Check Questions

- [ ] Did I describe the output error in precise terms (shifted, swapped, saturated, sign-flipped) before searching?
- [ ] Does each candidate root cause I'm considering actually explain the specific observed pathology?
- [ ] For every function I suspect, did I verify its math line-by-line against the canonical correct form?
- [ ] Did I change only one thing at a time and re-run between changes?
- [ ] Did I leave the prohibited files (e.g. the test driver) untouched?
- [ ] After fixing, did I confirm the output pathology is gone across all test cases, not just one?
- [ ] Did I check whether multiple independent bugs exist rather than assuming a single cause?

## Technical Notes

- Coordinate errors in detection code almost always stem from xyxy/xywh/cxcywh confusion or width/height index swaps (e.g. `x2 = x1 + h` instead of `w`); these produce boxes with swapped aspect ratios or negative extent.
- Activation-substitution bugs (e.g. sigmoid replaced by tanh or a linear) produce logits that saturate or overshoot [0,1]; check every `sigmoid`/`softmax` call against the expected output range.
