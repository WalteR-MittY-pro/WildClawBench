#!/usr/bin/env bash
# GLM-5.1 Script 4: Categories 04, 05, 06 (using GLM from .env)
set -euo pipefail

cd "$(dirname "$0")"

# Load .env
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

echo "========================================="
echo "GLM-5.1 Script 4: Categories 04, 05, 06"
echo "Using GLM with API_KEY: ${GLM_API_KEY:0:20}..."
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
        --models-config models_config_glm5.1.json \
        2>&1 | tee "logs/glm5.1_${category}.log"

    echo "$category completed at $(date)"
done

echo ""
echo "========================================="
echo "Script 4 completed all categories at $(date)"
echo "========================================="
