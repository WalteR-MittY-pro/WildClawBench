#!/usr/bin/env bash
# 清理WildClawBench所有运行任务、输出文件和Docker容器

set -euo pipefail

cd "$(dirname "$0")"

echo "========================================="
echo "WildClawBench 清理脚本"
echo "========================================="
echo ""

# 1. 停止所有运行中的脚本
echo "1. 停止运行中的脚本..."
if pgrep -f "run_.*_script.sh" > /dev/null; then
    echo "   发现运行中的脚本，正在终止..."
    pkill -9 -f "run_.*_script.sh" || true
    echo "   ✅ 脚本已终止"
else
    echo "   ℹ️  没有运行中的脚本"
fi

# 2. 停止所有run_batch.py进程
echo ""
echo "2. 停止run_batch.py进程..."
if pgrep -f "run_batch.py" > /dev/null; then
    echo "   发现run_batch.py进程，正在终止..."
    pkill -9 -f "run_batch.py" || true
    echo "   ✅ run_batch.py进程已终止"
else
    echo "   ℹ️  没有run_batch.py进程"
fi

# 3. 停止tmux会话
echo ""
echo "3. 停止tmux会话..."
if tmux has-session -t wildclaw 2>/dev/null; then
    echo "   发现wildclaw会话，正在终止..."
    tmux kill-session -t wildclaw
    echo "   ✅ wildclaw会话已终止"
else
    echo "   ℹ️  没有wildclaw会话"
fi

if tmux has-session -t gpt54 2>/dev/null; then
    echo "   发现gpt54会话，正在终止..."
    tmux kill-session -t gpt54
    echo "   ✅ gpt54会话已终止"
else
    echo "   ℹ️  没有gpt54会话"
fi

# 4. 停止并删除Docker容器
echo ""
echo "4. 停止并删除Docker容器..."
containers=$(docker ps -a --filter "ancestor=wildclawbench-ubuntu:v1.3" --format "{{.ID}}" 2>/dev/null || true)
if [ -n "$containers" ]; then
    echo "   发现 $(echo "$containers" | wc -l) 个容器，正在删除..."
    echo "$containers" | xargs docker rm -f 2>/dev/null || true
    echo "   ✅ Docker容器已删除"
else
    echo "   ℹ️  没有相关Docker容器"
fi

# 5. 删除输出文件
echo ""
echo "5. 删除输出文件..."
if [ -d "output" ]; then
    file_count=$(find output -type f 2>/dev/null | wc -l || echo "0")
    echo "   发现 $file_count 个输出文件，正在删除..."
    rm -rf output/*
    echo "   ✅ output/目录已清空"
else
    echo "   ℹ️  output/目录不存在"
fi

# 6. 删除日志文件
echo ""
echo "6. 删除日志文件..."
if [ -d "logs" ]; then
    log_count=$(find logs -name "*.log" -o -name "*.out" 2>/dev/null | wc -l || echo "0")
    if [ "$log_count" -gt 0 ]; then
        echo "   发现 $log_count 个日志文件，正在删除..."
        rm -f logs/*.log logs/*.out
        echo "   ✅ 日志文件已删除"
    else
        echo "   ℹ️  没有日志文件"
    fi
else
    echo "   ℹ️  logs/目录不存在"
fi

# 7. 清理nohup文件
echo ""
echo "7. 清理nohup文件..."
if [ -f "nohup.out" ]; then
    rm -f nohup.out
    echo "   ✅ nohup.out已删除"
else
    echo "   ℹ️  没有nohup.out文件"
fi

echo ""
echo "========================================="
echo "✅ 清理完成！"
echo "========================================="
echo ""
echo "状态检查:"
echo "  - 运行中的脚本: $(pgrep -f "run_.*_script.sh" | wc -l || echo 0)"
echo "  - 运行中的Python进程: $(pgrep -f "run_batch.py" | wc -l || echo 0)"
echo "  - Docker容器数: $(docker ps -a --filter "ancestor=wildclawbench-ubuntu:v1.3" --format "{{.ID}}" 2>/dev/null | wc -l || echo 0)"
echo "  - output/文件数: $(find output -type f 2>/dev/null | wc -l || echo 0)"
echo "  - logs/文件数: $(find logs -name "*.log" -o -name "*.out" 2>/dev/null | wc -l || echo 0)"
echo ""
