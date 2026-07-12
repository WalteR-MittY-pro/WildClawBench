---
name: 02-code-intelligence-task-1-sam3-inference
description: Use when you must use an undocumented code library by reading source alone. Focuses on inferring the intended API surface, parameter formats, and data conventions from implementation details without any README or examples.
---

# Reverse-Engineering an Undocumented Code Library

## Core Challenge

You must build working code against a library that ships no documentation, examples, or notebooks. Correct usage has to be inferred entirely from reading source: which entry points are public, what parameter shapes they expect, and what implicit conventions (coordinate systems, normalization, ordering) the implementation silently assumes. The difficulty is distinguishing the intended interface from internal plumbing, and recovering the invisible contracts that only tests or examples would normally reveal.

## Solution Strategy

1. **Map the package layout before reading any file**: Directory structure, `__init__.py` exports, and module names reveal the intended public surface and call hierarchy. Common mistake: diving straight into a deep module and treating a private helper as the entry point.

2. **Treat exported names as the contract**: Names re-exported in `__init__.py` or named `build_*` / `load_*` are the documented interface in absence of docs. Trace their signatures and return types first. Common mistake: constructing a class directly when a builder function exists to handle configuration.

3. **Infer conventions from the math, not the names**: Coordinate formats (xyxy vs xywh), normalization ranges, and channel orders are encoded in how arrays are sliced, indexed, and compared. A line like `x2 = x + w` tells you the input is center/wh, not corners. Common mistake: assuming a parameter name ("box") implies its format, then producing silently-wrong geometry.

4. **Write a minimal probe before the full script**: Run the smallest possible call that returns *anything*, then inspect `.shape`, `dtype`, and value ranges of every object in the chain. This exposes the real data flow far faster than reading. Common mistake: writing the complete pipeline blind and debugging six stacked assumptions at once.

5. **Mirror the preprocessing the model itself applies**: Models wrap inputs in a processor/transform that resizes, normalizes, and pads. Use that processor rather than hand-rolling tensors, or output coordinates will be in the wrong frame. Common mistake: feeding raw tensors and getting predictions in a normalized/resized coordinate space that never maps back to pixels.

## Decision Points

- **Builder function vs direct class construction**: Prefer the factory/builder whenever the package exposes one — it wires defaults and device handling; reach for the class directly only when you need non-standard config.
- **Hand-crafted tensor vs official processor**: Use the official processor/transform; hand-craft only if you have proven the processor's exact output format and it cannot do what you need.
- **Coordinate output format**: Decide by inspecting where outputs are consumed — convert to the consumer's expected convention (e.g. pixel xyxy) as the final step, after discovering the model's native frame.

## Common Failure Patterns

- **Trusting parameter names over behavior**: "boxes" must be xyxy because the arg is named boxes → wrong-format coordinates that still "run" but detect nothing.
- **Skipping the processor**: Feeding raw images so the model receives un-normalized/wrong-sized input → plausible-but-garbage predictions.
- **Confusing public and private API**: Importing from an underscored module or instantiating internals → brittle code that breaks on the next checkout.
- **Outputting in native instead of requested space**: Returning normalized or resized-frame coordinates → boxes that look correct relatively but are offset/scaled against the real image.
- **Stacking assumptions, then debugging all at once**: Writing the full script then running once → a single error hides five latent mistakes.

## Self-Check Questions

- [ ] Did I enumerate the public entry points from `__init__.py` before writing code?
- [ ] For every parameter, can I point to the source line that defines its expected format?
- [ ] Did I run a minimal probe and inspect shapes/dtypes/ranges of each intermediate object?
- [ ] Did I confirm whether coordinates are expected normalized or in pixels, and in which frame?
- [ ] Am I using the library's processor/transform rather than manual tensor construction?
- [ ] Did I verify my output coordinates map back to the original image dimensions?
- [ ] Did I confirm the model loads and runs on the target device without errors before finalizing?
- [ ] Did I test each prompt type (text, box, combined) independently rather than assuming one works for all?

## Technical Notes

- Detection/segmentation libraries commonly store boxes as `xyxy` (corner) but accept prompts as `xywh` (or center + size); the conversion is where most silent bugs live — find the exact line that consumes your input.
- When a processor resizes the image for the model, predicted coordinates are in the *processed* frame; most libraries provide a rescale/postprocess step you must call to return to original pixels.
