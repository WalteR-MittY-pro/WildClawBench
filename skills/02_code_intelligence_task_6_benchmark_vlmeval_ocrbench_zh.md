---
name: 02-code-intelligence-task-6-benchmark-vlmeval-ocrbench-zh
description: Use when running an unfamiliar ML evaluation framework against a custom API endpoint and a specific benchmark version. Focuses on bridging an external framework to a proxied model API, selecting the exact benchmark variant, and reproducing results under time pressure.
---

# Driving an Unfamiliar Eval Framework with a Custom API

## Core Challenge

You must reproduce a model's benchmark score using a heavyweight evaluation framework you've never used, wired to a non-standard API endpoint, on one specific benchmark version among several similarly named ones. There are no end-to-end examples for your exact setup, so every bridge — API config, model wrapper, dataset path, version selection — must be inferred from the framework's source and docs. The traps are silent: the wrong version still "runs," a misconfigured API still returns plausible JSON, and an unverifiable number looks done.

## Solution Strategy

1. **Pin the exact benchmark variant before doing anything**: Frameworks host multiple versions with near-identical names (v1 vs v2). Identify the precise dataset/config string the framework uses for the target version and use only that. Common mistake: running with the default or similarly-named variant and assuming it's correct.

2. **Bridge the custom API via the framework's native extension point**: Most frameworks support registering a custom OpenAI-compatible client (base_url + key) rather than requiring their built-in model class. Find that mechanism (config file, env var, or `--api-base` flag) instead of patching internals. Common mistake: hand-rolling the entire inference loop and abandoning the framework's scoring.

3. **Ensure reproducibility by setting decoding determinism**: Set temperature and any sampling flags so repeated runs are stable; the framework may expose these via CLI or a config the model wrapper reads. Common mistake: leaving defaults that introduce run-to-run variance into the score.

4. **Use local/cached data when provided to save time**: If the dataset is pre-staged, point the framework at it instead of downloading; this both speeds the run and avoids network flakiness. Common mistake: re-downloading a large dataset when a local copy is available.

5. **Map the framework's native output into the required schema**: The framework writes its own result files in its own shape; parse the produced scores and re-emit only the fields the task demands, with correct types. Common mistake: assuming the framework's raw output file already satisfies the required format.

6. **Time-box: prefer partial-but-real over perfect-but-incomplete**: A real score from a subset is more valuable than a full run that times out. Prefer the framework's fast-path options (fewer samples, caching) when offered. Common mistake: running the full benchmark naively and exceeding the time budget.

## Decision Points

- **Framework-native custom API vs custom inference loop**: Always prefer the framework's native OpenAI-compatible endpoint registration; write a custom loop only if no hook exists, and reuse the framework's scoring afterward.
- **Full benchmark vs accelerated subset**: Use the framework's acceleration options (workdir caching, reduced samples) when time is tight; verify the accelerated run still uses the correct benchmark variant.
- **Framework output vs required output**: Treat them as separate — let the framework write its files, then transform to the required schema explicitly.

## Common Failure Patterns

- **Wrong benchmark version**: Running a similarly-named variant → score is real but for the wrong benchmark.
- **Silent API misconfiguration**: Wrong base_url/key handling → the framework errors or returns garbage that still looks like a score.
- **Abandoning the framework**: Re-implementing inference from scratch → loses the official scoring logic, producing an unverifiable number.
- **Default sampling**: Leaving temperature unset → run-to-run variance undermines reproducibility.
- **Format assumptions**: Submitting the framework's raw output file → required fields missing or mistyped.

## Self-Check Questions

- [ ] Did I confirm the exact benchmark variant string and that it differs from similarly-named ones?
- [ ] Am I using the framework's native custom-API mechanism rather than a hand-built loop?
- [ ] Did I set decoding parameters (temperature, etc.) for reproducibility?
- [ ] Did I use the pre-staged dataset instead of re-downloading?
- [ ] Did I transform the framework's output into the exact required schema with correct value types?
- [ ] Did I verify the run actually completed and produced a plausible score before submitting?
- [ ] Did I use acceleration options to fit within the time budget without changing the benchmark?

## Technical Notes

- OpenAI-compatible proxies usually require setting both the base URL and the API key via the framework's expected env vars or config; the model name must match what the proxy recognizes.
- Eval frameworks often name benchmark variants by a dataset key that differs across versions; the config key, not the display name, determines which data is loaded.
