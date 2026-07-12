---
name: 05-creative-synthesis-task-11-video-en-to-zh-dub
description: Use when replacing an English video's speech with a Chinese dub while preserving the original visuals. Focuses on multi-stage pipeline orchestration, translation fidelity, and audio-video remux integrity.
---

# Cross-Language Video Dubbing Pipeline

## Core Challenge

The agent must orchestrate a chain of heterogeneous stages — audio extraction, speech recognition, translation, text-to-speech synthesis, and audio-video remuxing — where each stage's output is the next stage's input and any weak link (a transcription error, a translation drift, a voice mismatch, a desynced mux) cascades into the final product. The difficulty is that the stages belong to different tool ecosystems with different format and timing constraints, and the final deliverable is judged on every link simultaneously.

## Solution Strategy

1. **Lock the exact duration target before generating**: Determine the precise output length (e.g., first N seconds) and trim at the video level first, so every downstream stage operates on the correct span. Common mistake: transcribing the whole video then struggling to bound the output.
2. **Transcribe cleanly before translating**: Get an accurate transcript of the target span first, since translation quality is capped by transcription quality. Verify the transcript against the audio. Common mistake: translating a noisy or partial transcript.
3. **Translate for fidelity and naturalness together**: Preserve all information without omission or addition, use correct and consistent terminology, and keep the original's tone and register. Match source emphasis rather than paraphrasing loosely. Common mistake: a fluent-but-loose translation that drops or adds meaning.
4. **Match the dubbed voice to the original speaker**: The synthesized voice should match the original speaker's gender, energy, and pace — gender match is usually a hard requirement, not a nice-to-have. Common mistake: defaulting to whatever TTS voice is easiest, ignoring speaker characteristics.
5. **Time the dub to the original speech window**: Aim the synthesized speech at the same span where the original speech occurred, so the dub is intelligible and content-verifiable in that window. Common mistake: uncontrolled TTS timing that doesn't correspond to the original speech segment.
6. **Remux without touching the video track**: Replace only the audio; the video frames must be byte-for-byte (or frame-for-frame) identical to the source's corresponding span. Verify visually by frame comparison. Common mistake: re-encoding the video and introducing subtle visual differences.
7. **Produce all required artifacts**: The transcript files and the dubbed video are all graded; do not skip any. Common mistake: delivering only the video and forgetting the text artifacts.

## Decision Points

- **Transcription source**: Prefer dedicated ASR (Whisper-class) on the extracted audio over multimodal frame-based guessing for accuracy; cross-check with the audio.
- **TTS voice selection**: When multiple voices are available, explicitly pick the one matching the speaker's perceived gender and tone; never accept a silent default.
- **Trim-then-process vs. process-then-trim**: Trim the video to the target span first, then run the pipeline on that span — this keeps duration control simple and avoids trimming artifacts at the mux stage.
- **Mux approach**: Use stream copy for the video track (`-c:v copy`) and encode only the audio to guarantee visual identity preservation.

## Common Failure Patterns

- **Transcription errors**: Misheard words cap translation and dub accuracy → content match fails.
- **Loose translation**: Fluent but unfaithful, omitting or adding meaning → fidelity scores collapse.
- **Voice/gender mismatch**: Default TTS voice that doesn't match the speaker → speaker-match scores near zero.
- **Video re-encoding**: Re-encoding the video track during mux → subtle visual drift vs. the original frames.
- **Duration overrun**: Output exceeds the target length → fails the gating duration check.
- **Missing artifacts**: Delivering the video but not the transcript files (or vice versa) → partial-zero grading.
- **Untimed dub**: TTS audio placed without regard to the original speech window → content can't be verified in the expected segment.

## Self-Check Questions

- [ ] Did I trim the video to the exact required span before running the pipeline?
- [ ] Is the transcript verified against the audio for accuracy?
- [ ] Does the translation preserve all meaning with correct, consistent terminology?
- [ ] Does the dubbed voice match the original speaker's gender and energy?
- [ ] Is the dubbed audio intelligible in the original speech window?
- [ ] Did I remux with the video track copied, not re-encoded?
- [ ] Are the output visuals frame-identical to the source's corresponding span?
- [ ] Are all required artifacts (transcript files + video) present and non-empty?

## Technical Notes

- `ffmpeg -i input -ss <start> -t <dur> -c:v copy -c:a aac output` copies the video stream losslessly while encoding only audio — the safe pattern for dubbing.
- For frame-identity verification, extract matching timestamps from source and output and compare via MSE/SSIM; even re-encodes that look identical can fail a strict frame comparison.
- TTS systems (e.g., edge-tts) often accept voice selectors for gender/locale — set these explicitly rather than relying on defaults.
