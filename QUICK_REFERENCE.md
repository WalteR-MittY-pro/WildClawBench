# 🚀 WildClawBench Baseline 快速命令参考

## 📌 核心问题解答

### 1. runtime配置来源
配置参考自agentClawBench：
- **GPT-5.4-mini**: 300s timeout (快速模型)
- **GLM-5.1**: 600s timeout (已优化，原本300s不够)

### 2. GLM-5.1 SSE支持 ✅ 已解决
```json
// models_config_glm5.1.json
"api": "openai-compatible"  // ✅ 支持SSE (原来是openai-completions)
"llm_timeout_seconds": 600   // ✅ 增加到600s
"llm_max_retries": 2         // ✅ 增加重试次数
```

---

## ⚡ 一键启动（推荐）

```bash
cd /Users/user/Desktop/project/winder/WildClawBench
./start_all_baselines.sh
```

**启动后会自动进入tmux会话，包含：**
- 窗口0: monitor (实时监控)
- 窗口1-4: GPT-5.4-mini (域01, 02, 03, 04+05+06)
- 窗口5-8: GLM-5.1 (域01, 02, 03, 04+05+06)

---

## 🎮 Tmux操作速查

| 操作 | 快捷键 | 命令 |
|------|--------|------|
| 附加会话 | - | `tmux attach -t wildclaw` |
| 切换窗口 | `Ctrl+b` → `0-8` | - |
| 列出窗口 | `Ctrl+b` → `w` | - |
| 分离会话 | `Ctrl+b` → `d` | - |
| 终止会话 | - | `tmux kill-session -t wildclaw` |
| 查看所有会话 | - | `tmux ls` |

---

## 📂 手动启动（分步执行）

### 启动GPT-5.4-mini任务

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 方式1: 后台运行
nohup ./run_gpt_script1.sh > logs/nohup_gpt1.out 2>&1 &  # 域01
nohup ./run_gpt_script2.sh > logs/nohup_gpt2.out 2>&1 &  # 域02
nohup ./run_gpt_script3.sh > logs/nohup_gpt3.out 2>&1 &  # 域03
nohup ./run_gpt_script4.sh > logs/nohup_gpt4.out 2>&1 &  # 域04+05+06

# 方式2: 前台运行（单个终端）
./run_gpt_script1.sh  # 运行完毕后再启动下一个
```

### 启动GLM-5.1任务

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

nohup ./run_glm_script1.sh > logs/nohup_glm1.out 2>&1 &  # 域01
nohup ./run_glm_script2.sh > logs/nohup_glm2.out 2>&1 &  # 域02
nohup ./run_glm_script3.sh > logs/nohup_glm3.out 2>&1 &  # 域03
nohup ./run_glm_script4.sh > logs/nohup_glm4.out 2>&1 &  # 域04+05+06
```

---

## 📊 监控命令

### 实时查看日志

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 查看特定日志
tail -f logs/gpt5.4mini_cat01.log
tail -f logs/glm5.1_cat01.log

# 同时监控多个日志（多窗格）
tmux split-window -h "tail -f logs/gpt5.4mini_cat01.log"
```

### 检查进程状态

```bash
# 查看运行中的脚本
ps aux | grep run_.*_script | grep -v grep

# 查看后台任务
jobs -l

# 查看Python进程
ps aux | grep run_batch.py | grep -v grep
```

### 查看完成进度

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 统计已完成任务数
find output/ -name "score.json" 2>/dev/null | wc -l

# 统计失败任务数
find output/ -name "error.txt" 2>/dev/null | wc -l

# 查看最新日志
ls -lt logs/ | head -10
```

---

## 🔍 验证GLM SSE配置

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 测试单个任务
python3 eval/run_batch.py \
    --agent-backend openclaw \
    --category 01_Productivity_Flow \
    --parallel 1 \
    --models-config models_config_glm5.1.json

# 检查是否使用SSE
grep -i "stream\|compatible" output/*/gateway.log | head -5

# 检查超时情况
grep -i "timeout\|timed out" output/*/agent.log
```

---

## 🛑 停止任务

### 停止特定脚本

```bash
# 查找进程ID
ps aux | grep run_gpt_script1 | grep -v grep

# 终止进程
kill -9 <PID>

# 或使用pkill
pkill -f run_gpt_script1.sh
```

### 停止所有任务

```bash
# 终止所有baseline脚本
pkill -f "run_.*_script"

# 终止所有run_batch.py进程
pkill -f "run_batch.py"

# 终止tmux会话
tmux kill-session -t wildclaw
```

---

## 📈 结果收集

### 统计汇总

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 快速统计
python3 << 'EOF'
import json
from pathlib import Path

scores = []
for p in Path('output').rglob('score.json'):
    try:
        data = json.loads(p.read_text())
        scores.append(data.get('overall_score', 0))
    except:
        pass

if scores:
    print(f'总任务数: {len(scores)}')
    print(f'平均分数: {sum(scores)/len(scores):.3f}')
    print(f'成功率: {sum(1 for s in scores if s > 0.5)/len(scores):.2%}')
else:
    print('未找到结果')
EOF
```

### 备份结果

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 打包输出和日志
tar -czf wildclawbench_$(date +%Y%m%d_%H%M%S).tar.gz output/ logs/

# 查看压缩包大小
du -h wildclawbench_*.tar.gz
```

---

## 📝 配置文件位置

```
WildClawBench/
├── .env                          # GPT KEY1 + GLM共享KEY
├── .env2                         # GPT KEY2 + GLM共享KEY
├── models_config_gpt5.4mini.json # GPT配置 (api: openai-completions)
├── models_config_glm5.1.json     # GLM配置 (api: openai-compatible) ✅
├── run_gpt_script1.sh            # GPT 域01 (使用.env)
├── run_gpt_script2.sh            # GPT 域02 (使用.env)
├── run_gpt_script3.sh            # GPT 域03 (使用.env2)
├── run_gpt_script4.sh            # GPT 域04+05+06 (使用.env2)
├── run_glm_script1.sh            # GLM 域01 (使用.env)
├── run_glm_script2.sh            # GLM 域02 (使用.env)
├── run_glm_script3.sh            # GLM 域03 (使用.env)
├── run_glm_script4.sh            # GLM 域04+05+06 (使用.env)
├── start_all_baselines.sh        # 一键启动脚本
├── logs/                         # 日志输出目录
└── output/                       # 结果输出目录
```

---

## ⚠️ 常见问题

### Q1: GLM-5.1超时怎么办？
**A:** 已经将timeout从300s增加到600s，如果仍然超时：
```bash
# 编辑配置文件
vim models_config_glm5.1.json
# 将 "llm_timeout_seconds": 600 改为 900
```

### Q2: API限流怎么办？
**A:** 脚本会自动重试。如果频繁限流：
- GPT: 已使用两个不同API key分散负载
- GLM: 考虑降低并行数 `--parallel 2`

### Q3: 如何查看某个任务的详细日志？
**A:**
```bash
# 找到任务输出目录
ls output/01-01/

# 查看agent日志
cat output/01-01/agent.log

# 查看gateway日志
cat output/01-01/gateway.log
```

### Q4: 中断后如何恢复？
**A:** 直接重新运行对应的脚本，已完成的任务会被跳过。

---

## 📞 快速帮助

```bash
# 查看所有脚本
ls -lh run_*.sh start_*.sh

# 查看配置文件
cat models_config_gpt5.4mini.json
cat models_config_glm5.1.json

# 查看详细执行指南
cat EXECUTION_GUIDE.md

# 查看配置解答
cat wildclawbench_config_guide.md
```
