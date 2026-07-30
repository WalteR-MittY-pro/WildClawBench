#!/usr/bin/env bash
# WildClawBench 一键启动所有8个baseline脚本

set -euo pipefail

cd "$(dirname "$0")"

echo "========================================"
echo "WildClawBench Baseline 批量启动脚本"
echo "========================================"
echo ""
echo "启动方案: tmux多窗口管理"
echo ""
echo "将启动8个并行任务:"
echo "  - GPT-5.4 x 4 (域01, 02, 03, 04+05+06)"
echo "  - GLM-5.1 x 4 (域01, 02, 03, 04+05+06)"
echo ""
echo "配置说明:"
echo "  - GPT Script 1-2: 使用.env (KEY1)"
echo "  - GPT Script 3-4: 使用.env2 (KEY2)"
echo "  - GLM Script 1-4: 使用.env (共享GLM_KEY)"
echo ""
echo "GPT-5.4配置: api=openai-completions, timeout=300s"
echo "GLM-5.1配置: api=openai-compatible (SSE支持), timeout=600s"
echo ""

read -p "确认启动所有8个脚本? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

# 检查tmux是否安装
if ! command -v tmux &> /dev/null; then
    echo "错误: 未安装tmux"
    echo "请先安装: sudo apt-get install tmux 或 brew install tmux"
    exit 1
fi

# 检查必要文件
for script in run_gpt_script{1..4}.sh run_glm_script{1..4}.sh; do
    if [[ ! -f "$script" ]]; then
        echo "错误: 找不到 $script"
        exit 1
    fi
done

# 创建日志目录
mkdir -p logs

echo ""
echo "启动tmux会话: wildclaw"
echo ""

# 创建tmux会话
tmux new-session -d -s wildclaw -n "monitor"

# GPT-5.4 4个窗口
echo "启动 GPT-5.4 任务..."
tmux new-window -t wildclaw:1 -n gpt-01 "cd '$PWD' && ./run_gpt_script1.sh"
tmux new-window -t wildclaw:2 -n gpt-02 "cd '$PWD' && ./run_gpt_script2.sh"
tmux new-window -t wildclaw:3 -n gpt-03 "cd '$PWD' && ./run_gpt_script3.sh"
tmux new-window -t wildclaw:4 -n gpt-456 "cd '$PWD' && ./run_gpt_script4.sh"

# GLM-5.1 4个窗口
echo "启动 GLM-5.1 任务..."
tmux new-window -t wildclaw:5 -n glm-01 "cd '$PWD' && ./run_glm_script1.sh"
tmux new-window -t wildclaw:6 -n glm-02 "cd '$PWD' && ./run_glm_script2.sh"
tmux new-window -t wildclaw:7 -n glm-03 "cd '$PWD' && ./run_glm_script3.sh"
tmux new-window -t wildclaw:8 -n glm-456 "cd '$PWD' && ./run_glm_script4.sh"

# 在monitor窗口显示状态
tmux send-keys -t wildclaw:0 "cd '$PWD'" C-m
tmux send-keys -t wildclaw:0 "watch -n 5 'echo \"=== Running Processes ===\"  && ps aux | grep run_.*_script | grep -v grep && echo && echo \"=== Completed Tasks ===\" && find output/ -name score.json 2>/dev/null | wc -l && echo && echo \"=== Log Files ===\" && ls -lht logs/ | head -10'" C-m

echo ""
echo "✅ 所有任务已启动!"
echo ""
echo "tmux操作指南:"
echo "  - 附加到会话: tmux attach -t wildclaw"
echo "  - 切换窗口: Ctrl+b 然后按 0-8"
echo "  - 分离会话: Ctrl+b 然后按 d"
echo "  - 列出窗口: Ctrl+b 然后按 w"
echo "  - 终止会话: tmux kill-session -t wildclaw"
echo ""
echo "窗口列表:"
echo "  0: monitor  - 任务监控"
echo "  1: gpt-01   - GPT域01"
echo "  2: gpt-02   - GPT域02"
echo "  3: gpt-03   - GPT域03"
echo "  4: gpt-456  - GPT域04+05+06"
echo "  5: glm-01   - GLM域01"
echo "  6: glm-02   - GLM域02"
echo "  7: glm-03   - GLM域03"
echo "  8: glm-456  - GLM域04+05+06"
echo ""
echo "日志文件位置: $(pwd)/logs/"
echo ""

# 自动附加到会话
sleep 2
tmux attach -t wildclaw
