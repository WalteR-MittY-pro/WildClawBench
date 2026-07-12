---
name: 05-creative-synthesis-task-2-goal-highlights
description: Use when compiling a bounded-duration highlight reel of specific events from a long video. Focuses on temporal boundary detection, completeness under a duration budget, and content exclusion.
---

# Bounded Highlight Compilation from Long Video

## Core Challenge

The agent must locate every instance of a target event type for a specific subject, define tight temporal boundaries around each instance, and concatenate them into a single reel whose total duration does not exceed a fixed budget. The difficulty is tri-fold: completeness (no missed instances), boundary discipline (start at the beginning of the relevant action, end before irrelevant footage), and budget management (the sum of all clips must fit).

## Solution Strategy

1. **Enumerate before extracting**: First produce a complete candidate list of every target event with approximate timestamps, then verify each. Only after the list is complete should you cut clips. Common mistake: cutting clips one at a time and running out of budget before finding later events.
2. **Define the semantic start and end of each event explicitly**: For each event type, decide what marks the legitimate start (e.g., initiation of the attacking move) and the legitimate end (e.g., ball crossing the line), and cut to those markers. Common mistake: using arbitrary time offsets around a peak moment.
3. **Budget the reel before final concatenation**: Sum the planned durations; if over budget, tighten boundaries or trim lead-in rather than dropping events. Common mistake: concatenating everything and only then discovering the total is too long.
4. **Exclude the explicitly-excluded content**: Identify what must NOT appear (e.g., post-event celebrations, replays, commentary cutaways) and trim aggressively at the boundary. Common mistake: including visually exciting but explicitly forbidden footage.
5. **Preserve source fidelity**: Concatenate without re-encoding effects, overlays, watermarks, or text. The reel should be a clean subsequence of the source. Common mistake: adding transitions or titles that contaminate the original.
6. **Document each cut in a machine-readable sheet**: Record the source start/end and a description for every segment so the compilation is auditable and reproducible. Common mistake: producing only the video with no cut record.

## Decision Points

- **Completeness vs. budget**: When budget is tight, prefer shortening each clip's lead-in/out over dropping an event — a missing event is usually a harder failure than a tighter clip.
- **Boundary ambiguity**: When the semantic start is fuzzy (e.g., "start of attacking play"), pick the most recent clear restart (throw-in, kickoff, turnover) as the anchor rather than guessing mid-play.
- **Lossless concat vs. re-encode**: Use stream copy (`-c copy`) with the concat demuxer when all clips share codec/params; re-encode only if parameters differ, and accept the quality/time cost deliberately.

## Common Failure Patterns

- **Missing late events**: Stopping the scan early or sampling sparsely in the back half of the video → incomplete reel.
- **Celebration inclusion**: Cutting the end boundary at the moment of excitement rather than the moment of completion → forbidden footage leaks in.
- **Budget blowout**: Not summing durations before concat → reel exceeds the limit and gets penalized or rejected.
- **Arbitrary boundaries**: Using fixed ±N second offsets around a timestamp → clips miss the build-up or include irrelevant footage.
- **Re-encode contamination**: Re-encoding with filters or overlays → artifacts, watermarks, or quality loss vs. source.

## Self-Check Questions

- [ ] Have I confirmed I found every instance of the target event for the target subject?
- [ ] Does each clip start at the genuine beginning of the relevant action?
- [ ] Does each clip end at the completion moment, excluding any forbidden post-event footage?
- [ ] Is the sum of all clip durations within the required budget?
- [ ] Did I avoid adding any effects, text, or watermarks not present in the source?
- [ ] Is there a cut sheet documenting each segment's source range and description?
- [ ] Do the cut-sheet timestamps actually correspond to the concatenated footage?
- [ ] Is the output in the required container/codec?

## Technical Notes

- `ffmpeg` concat demuxer (`-f concat -i list.txt -c copy`) is the cleanest lossless join when all segments share codec/parameters; otherwise re-encode with `-filter_complex concat`.
- `ffprobe` gives precise per-segment duration; sum these before concatenating to verify the budget.
- Always verify final output duration with `ffprobe` after concatenation — concat quirks can shift duration slightly.
