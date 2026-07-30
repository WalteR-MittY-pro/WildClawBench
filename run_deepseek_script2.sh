#!/usr/bin/env bash
# DeepSeek Script 4: Categories 04, 05, 06 (using .env)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "DeepSeek Script 4: Categories 01, 02, 03"
echo "Using .env with API_KEY: ${DEEPSEEK_API_KEY:0:20}..."
echo "========================================="

CATEGORIES=(
    "01_Productivity_Flow"
    "02_Code_Intelligence"
    "03_Social_Interaction"
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
        --models-config models_config_deepseek.json \
        2>&1 | tee "logs/deepseek_${category}.log"

    echo "$category completed at $(date)"
done

echo ""
echo "========================================="
echo "Script 4 completed all categories at $(date)"
echo "========================================="
