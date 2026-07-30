#!/usr/bin/env bash
# GPT-5.4 Script 3: Category 03 (using .env2)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env2
export $(cat .env2 | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "GPT-5.4 Script 3: Category 03"
echo "Using .env2 with API_KEY: ${GPT_API_KEY:0:20}..."
echo "========================================="

python3 eval/run_batch.py \
    --agent-backend openclaw \
    --category 03_Social_Interaction \
    --parallel 1 \
    --models-config models_config_gpt5.4.json \
    2>&1 | tee logs/gpt5.4_cat03.log

echo "Script 3 completed at $(date)"
