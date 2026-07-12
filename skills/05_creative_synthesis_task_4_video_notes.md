---
name: 05-creative-synthesis-task-4-video-notes
description: Use when converting a lecture/instructional video into comprehensive study notes. Focuses on dense factual extraction from temporal media and distinguishing source-specific content from generic prior knowledge.
---

# Lecture Video to Comprehensive Study Notes

## Core Challenge

The agent must watch an instructional video and reconstruct its content as structured notes that faithfully reflect what was actually said and shown — including specific definitions, examples, numbers, and the video's own framing — rather than collapsing the content into generic textbook knowledge it already holds. The trap is that the topic is familiar, so the agent is tempted to write what it already knows instead of what the video actually communicates.

## Solution Strategy

1. **Extract before synthesizing**: Do a dedicated extraction pass that pulls concrete claims, definitions, examples, analogies, numbers, and named entities directly from the video's audio and frames. Common mistake: writing notes from prior knowledge and only sprinkling in a few video details.
2. **Preserve the source's structure and framing**: Mirror the video's own sectioning, ordering, and emphasis; if the speaker spends five minutes on a subtopic, the notes should reflect that weight. Common mistake: reorganizing into a generic textbook outline that loses the source's pedagogical arc.
3. **Capture specific claims, not paraphrased gist**: Each concept should include the precise mechanism, number, or qualifier the speaker used, not a rounded approximation. Common mistake: writing "models are trained on lots of data" when the speaker specified scale and method.
4. **Distinguish source-anchored facts from your own elaboration**: If you add explanatory context, make sure the core claim is still the one from the video. Common mistake: substituting a correct-but-different framing that doesn't match the source's wording or emphasis.
5. **Use multiple modalities as evidence**: Audio transcript, on-screen text, diagrams, and code samples are all source material; cross-check them to catch details a single modality misses. Common mistake: relying on audio only and missing visual definitions.
6. **Verify completeness against the full timeline**: After drafting, walk the notes back against the full video timeline to confirm every major section and key claim is represented. Common mistake: stopping early and omitting the final third.

## Decision Points

- **Fidelity vs. readability**: Lean toward fidelity — notes that omit a specific claim to "read better" lose the facts that matter for review. Add structure for readability, but never at the cost of source content.
- **Transcript-first vs. frame-first**: For talking-head lectures, transcript is primary and frames fill gaps (diagrams, on-screen definitions). For highly visual content, sample frames more densely.
- **Depth vs. length limits**: When length is bounded, prioritize covering all source sections at moderate depth over deep-diving one section and skipping others.

## Common Failure Patterns

- **Generic-knowledge collapse**: Writing familiar-sounding notes that could apply to any source on the topic → missing the specific claims that make this source reviewable.
- **Section omission**: Stopping the extraction before the video ends → entire topics absent from notes.
- **Gist paraphrase**: Summarizing "the idea is roughly X" → losing the precise mechanism, number, or qualifier.
- **Single-modality dependence**: Ignoring slides/diagrams → missing visual definitions or examples.
- **Length blowout or shortfall**: Over-quoting verbatim or under-writing → outside required length bounds.

## Self-Check Questions

- [ ] Did I do a dedicated extraction pass before writing prose?
- [ ] Are specific definitions, mechanisms, numbers, and examples captured, not just gist?
- [ ] Do the notes mirror the video's own structure and emphasis?
- [ ] Did I use both audio and visual evidence?
- [ ] Is every major section of the video represented?
- [ ] Could a reader who never saw the video reconstruct its specific claims from my notes?
- [ ] Are the notes within the required length bounds?
- [ ] Is the markdown well-structured with clear headings?

## Technical Notes

- For dense sampling, extract audio and run ASR (or use a multimodal model on sampled frames at ~1fps) to get a working transcript; then sample frames at higher density around sections heavy in diagrams or on-screen text.
- If the video has embedded captions/subtitles, extract them directly with `ffmpeg`'s subtitle stream — they're usually the most accurate source.
