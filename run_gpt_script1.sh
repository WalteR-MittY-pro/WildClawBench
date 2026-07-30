#!/usr/bin/env bash
# GPT-5.4 Script 1: Category 01 (using .env)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "GPT-5.4 Script 1: Category 01"
echo "Using .env with API_KEY: ${GPT_API_KEY:0:20}..."
echo "========================================="

python3 eval/run_batch.py \
    --agent-backend openclaw \
    --category 01_Productivity_Flow \
    --parallel 1 \
    --models-config models_config_gpt5.4.json \
    2>&1 | tee logs/gpt5.4_cat01.log

echo "Script 1 completed at $(date)"
