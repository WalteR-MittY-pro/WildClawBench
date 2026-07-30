#!/usr/bin/env bash
# GPT-5.4 Script 4: Categories 04, 05, 06 (using .env2)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env2
export $(cat .env2 | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "GPT-5.4 Script 4: Categories 04, 05, 06"
echo "Using .env2 with API_KEY: ${GPT_API_KEY:0:20}..."
echo "========================================="

CATEGORIES=(
    "04_Search_Retrieval"
    "05_Creative_Synthesis"
    "06_Safety_Alignment"
)

for category in "${CATEGORIES[@]}"; do
    echo ""
    echo "-----------------------------------------"
    echo "Running category: $category"
    echo "-----------------------------------------"

    python3 eval/run_batch.py \
        --agent-backend openclaw \
        --category "$category" \
        --parallel 1 \
        --models-config models_config_gpt5.4.json \
        2>&1 | tee "logs/gpt5.4_${category}.log"

    echo "$category completed at $(date)"
done

echo ""
echo "========================================="
echo "Script 4 completed all categories at $(date)"
echo "========================================="
