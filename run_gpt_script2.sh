#!/usr/bin/env bash
# GPT-5.4 Script 2: Category 02 (using .env)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "GPT-5.4 Script 2: Category 02"
echo "Using .env with API_KEY: ${GPT_API_KEY:0:20}..."
echo "========================================="

python3 eval/run_batch.py \
    --agent-backend openclaw \
    --category 02_Code_Intelligence \
    --parallel 1 \
    --models-config models_config_gpt5.4.json \
    2>&1 | tee logs/gpt5.4_cat02.log

echo "Script 2 completed at $(date)"
