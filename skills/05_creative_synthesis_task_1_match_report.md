---
name: 05-creative-synthesis-task-1-match-report
description: Use when producing a narrative report interleaved with extracted media clips from a long video. Focuses on temporal event detection, precise timestamp mapping, and selective media extraction.
---

# Video Event Report with Interleaved Clips

## Core Challenge

The agent must continuously watch a long video, decide which moments are semantically significant versus routine background, map those moments to precise timestamps in the source file, and then synthesize a coherent narrative that interlinks prose with the extracted evidence. The hard part is closing the loop between perception (seeing the event), temporal precision (finding the exact frame range), and narrative coherence (describing it accurately so text and clip agree).

## Solution Strategy

1. **Sample the whole timeline before committing**: A long video cannot be understood from a few frames. Extract frames on a dense, regular grid (plus audio/subtitle cues if available) to build a complete mental timeline. Common mistake: sampling only a handful of frames and missing events that occur between them.
2. **Define event-significance criteria up front**: Decide what counts as a "key event" (score changes, dismissals, decisive moments) versus secondary highlights before scanning, so the boundary is principled rather than vibes-based. Common mistake: conflating exciting but inconsequential play with documentable events.
3. **Lock timestamps to source-file position, not match clock**: Broadcast clocks, added time, and replay offsets all diverge from the raw video position. Always record the position in the source file. Common mistake: copying the on-screen match clock and extracting the wrong segment.
4. **Verify each extracted clip against its description**: After cutting, sample frames from the clip and check they actually depict what the text claims. Common mistake: trusting the timestamp math without visually confirming the clip content.
5. **Keep structured and narrative artifacts in sync**: The human-readable report and the machine-readable event list must reference the same timestamps and clip filenames. Regenerate one if the other changes. Common mistake: editing prose timestamps but leaving the JSON stale.
6. **Bound clip duration to the event, not the spectacle**: Extract only the window that shows the event itself; trim lead-in and trailing footage to stay within length limits. Common mistake: padding clips with pre/post context until they exceed limits.

## Decision Points

- **Frame density vs. cost**: Use denser sampling around likely event clusters (e.g., after restarts) and sparser sampling during dead time. If multimodal API calls are metered, sample strategically rather than uniformly.
- **Subtitle/audio vs. vision-only**: If the video has an audio track or subtitles, use them as a fast index to locate candidate events, then confirm visually. Pure frame-walking is far slower and noisier.
- **Structured-only vs. full narrative**: When a structured event list is also required, derive the narrative from the verified structured list rather than maintaining two independent reasoning passes.

## Common Failure Patterns

- **Timestamp drift**: Recording match clock or commentary time instead of file position → clips land on the wrong footage and text/clip disagree.
- **Event omission**: Sampling too sparsely and silently skipping an event that happened between sampled frames → incomplete event list, lost clips.
- **Hallucinated description**: Writing plausible-sounding detail (player names, move sequence) without visual confirmation → text contradicts the extracted clip.
- **Clip/text mismatch**: Extracting a clip at roughly the right time but describing a different phase of play → grader sees frames that don't match the prose.
- **Format sprawl**: Inconsistent timestamp formatting, relative-path errors, or mismatched filenames between report and structured file → references break.

## Self-Check Questions

- [ ] Did I sample enough of the video to be confident I found every significant event?
- [ ] Are all timestamps expressed as position in the source file, not broadcast clock?
- [ ] Did I visually verify each extracted clip actually shows the described event?
- [ ] Does every key event have both a narrative description and a media clip?
- [ ] Are the structured event list and the prose report consistent with each other?
- [ ] Are clip durations within the required bounds?
- [ ] Do relative media references resolve correctly from the report's location?
- [ ] Did I distinguish key events (with clips) from secondary highlights (text only)?

## Technical Notes

- `ffmpeg -ss <start> -t <dur> -i input -c copy out.mp4` is the standard fast extraction; placing `-ss` before `-i` does a fast keyframe seek but may start slightly off — re-verify visually.
- For dense frame sampling, use `-vf fps=1` to get one frame per second, then batch-send to a VLM. Higher fps for fast-action segments.
- If verifying clips programmatically, extract ~5-10 frames spread across the clip rather than just the first frame.
