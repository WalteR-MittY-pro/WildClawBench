# WildClawBench Baseline 执行指南

## 📋 配置总览

### 已创建的配置文件

1. **环境变量文件**
   - `.env` - GPT_API_KEY1 + GLM共享KEY
   - `.env2` - GPT_API_KEY2 + GLM共享KEY

2. **模型配置文件**
   - `models_config_gpt5.4mini.json` - GPT-5.4-mini配置
     - API类型: `openai-completions`
     - Timeout: 300s
     - Stream: true
   
   - `models_config_glm5.1.json` - GLM-5.1配置（已优化SSE支持）
     - API类型: `openai-compatible` ✅ **支持SSE**
     - Timeout: 600s ✅ **已增加**
     - Max retries: 2 ✅ **已增加**
     - Stream: true

### 关键配置变更

**GLM-5.1配置已针对SSE需求优化：**

```json
{
  "api": "openai-compatible",      // 支持SSE流式传输
  "llm_timeout_seconds": 600,      // 从300s增加到600s
  "llm_max_retries": 2             // 从1增加到2
}
```

## 🚀 执行方案

### 任务分配

#### GPT-5.4-mini（4个脚本）
| 脚本 | 域 | .env文件 | API Key |
|------|-----|----------|---------|
| Script 1 | 01_Productivity_Flow | .env | KEY1 |
| Script 2 | 02_Code_Intelligence | .env | KEY1 |
| Script 3 | 03_Social_Interaction | .env2 | KEY2 |
| Script 4 | 04+05+06 | .env2 | KEY2 |

#### GLM-5.1（4个脚本）
| 脚本 | 域 | .env文件 | API Key |
|------|-----|----------|---------|
| Script 1 | 01_Productivity_Flow | .env | 共享GLM_KEY |
| Script 2 | 02_Code_Intelligence | .env | 共享GLM_KEY |
| Script 3 | 03_Social_Interaction | .env | 共享GLM_KEY |
| Script 4 | 04+05+06 | .env | 共享GLM_KEY |

## 📝 执行命令

### 方式1：使用tmux（推荐，易于管理）

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 创建tmux会话
tmux new-session -d -s wildclaw

# GPT-5.4-mini 4个窗口
tmux new-window -t wildclaw:1 -n gpt-01 './run_gpt_script1.sh'
tmux new-window -t wildclaw:2 -n gpt-02 './run_gpt_script2.sh'
tmux new-window -t wildclaw:3 -n gpt-03 './run_gpt_script3.sh'
tmux new-window -t wildclaw:4 -n gpt-456 './run_gpt_script4.sh'

# GLM-5.1 4个窗口
tmux new-window -t wildclaw:5 -n glm-01 './run_glm_script1.sh'
tmux new-window -t wildclaw:6 -n glm-02 './run_glm_script2.sh'
tmux new-window -t wildclaw:7 -n glm-03 './run_glm_script3.sh'
tmux new-window -t wildclaw:8 -n glm-456 './run_glm_script4.sh'

# 附加到会话查看
tmux attach -t wildclaw
```

**tmux快捷键：**
- `Ctrl+b` → `1-8` : 切换窗口
- `Ctrl+b` → `d` : 分离会话（后台继续运行）
- `Ctrl+b` → `,` : 重命名窗口
- `tmux attach -t wildclaw` : 重新附加
- `tmux kill-session -t wildclaw` : 终止所有任务

### 方式2：使用nohup后台运行

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# GPT-5.4-mini 4个任务
nohup ./run_gpt_script1.sh > logs/nohup_gpt1.out 2>&1 &
nohup ./run_gpt_script2.sh > logs/nohup_gpt2.out 2>&1 &
nohup ./run_gpt_script3.sh > logs/nohup_gpt3.out 2>&1 &
nohup ./run_gpt_script4.sh > logs/nohup_gpt4.out 2>&1 &

# GLM-5.1 4个任务
nohup ./run_glm_script1.sh > logs/nohup_glm1.out 2>&1 &
nohup ./run_glm_script2.sh > logs/nohup_glm2.out 2>&1 &
nohup ./run_glm_script3.sh > logs/nohup_glm3.out 2>&1 &
nohup ./run_glm_script4.sh > logs/nohup_glm4.out 2>&1 &

# 查看所有后台任务
jobs -l
ps aux | grep "run_.*_script"
```

### 方式3：单独终端窗口

打开8个终端，每个执行：

```bash
# 终端1-4: GPT脚本
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_gpt_script1.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_gpt_script2.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_gpt_script3.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_gpt_script4.sh

# 终端5-8: GLM脚本
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_glm_script1.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_glm_script2.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_glm_script3.sh
cd /Users/user/Desktop/project/winder/WildClawBench && ./run_glm_script4.sh
```

## 📊 监控进度

### 实时查看日志

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 查看特定分类日志
tail -f logs/gpt5.4mini_cat01.log
tail -f logs/glm5.1_cat01.log

# 查看所有日志文件
ls -lht logs/

# 多窗口同时监控（使用tmux）
tmux split-window -h "tail -f logs/gpt5.4mini_cat01.log"
tmux split-window -v "tail -f logs/glm5.1_cat01.log"
```

### 检查进程状态

```bash
# 查看运行中的脚本
ps aux | grep run_.*_script

# 查看Python进程
ps aux | grep "run_batch.py"

# 查看资源使用
top -p $(pgrep -d',' -f run_batch.py)
```

### 检查输出结果

```bash
# 查看输出目录结构
tree -L 2 output/

# 查看已完成任务
find output/ -name "score.json" | wc -l

# 查看错误任务
find output/ -name "error.txt" | head -10
```

## 🔍 验证SSE配置

### 验证GLM-5.1使用SSE

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 运行单个测试任务
python3 eval/run_batch.py \
    --agent-backend openclaw \
    --category 01_Productivity_Flow \
    --parallel 1 \
    --models-config models_config_glm5.1.json

# 检查gateway日志中的API调用
grep -i "stream\|sse\|compatible" output/*/gateway.log | head -20

# 检查是否有超时错误
grep -i "timeout\|timed out" output/*/agent.log | head -10
```

## 📈 预期时间估算

### 单个任务平均时间
- **简单任务**: 2-5分钟
- **中等复杂度**: 5-15分钟
- **复杂任务**: 15-30分钟

### 域任务数量（参考）
- 01_Productivity_Flow: ~10-15个任务
- 02_Code_Intelligence: ~10-15个任务
- 03_Social_Interaction: ~8-12个任务
- 04_Search_Retrieval: ~8-12个任务
- 05_Creative_Synthesis: ~8-12个任务
- 06_Safety_Alignment: ~6-10个任务

### 预估总时间
- **单个脚本**: 2-6小时
- **所有8个脚本并行**: 2-6小时
- **GPT-5.4-mini总时间**: ~8-12小时（4个脚本并行）
- **GLM-5.1总时间**: ~10-15小时（4个脚本并行，可能更慢）

## ⚠️ 注意事项

1. **API限流**
   - GPT使用两个不同的API key（KEY1, KEY2）
   - GLM所有脚本共享一个API key，注意限流
   - 如果遇到限流，脚本会自动重试

2. **超时处理**
   - GLM已设置600s timeout
   - 如果仍然超时，考虑进一步增加到900s

3. **磁盘空间**
   - 每个任务会生成日志和输出文件
   - 确保有足够空间（建议>50GB）

4. **Docker资源**
   - 8个脚本会启动多个Docker容器
   - 确保Docker有足够资源（CPU/内存）

5. **中断恢复**
   - 如果脚本中断，可以重新运行
   - 已完成的任务会被跳过

## 📝 日志文件说明

```
logs/
├── gpt5.4mini_cat01.log              # GPT Script 1 完整日志
├── gpt5.4mini_cat02.log              # GPT Script 2 完整日志
├── gpt5.4mini_cat03.log              # GPT Script 3 完整日志
├── gpt5.4mini_04_Search_Retrieval.log     # GPT Script 4 - 域04
├── gpt5.4mini_05_Creative_Synthesis.log   # GPT Script 4 - 域05
├── gpt5.4mini_06_Safety_Alignment.log     # GPT Script 4 - 域06
├── glm5.1_cat01.log                  # GLM Script 1 完整日志
├── glm5.1_cat02.log                  # GLM Script 2 完整日志
├── glm5.1_cat03.log                  # GLM Script 3 完整日志
├── glm5.1_04_Search_Retrieval.log         # GLM Script 4 - 域04
├── glm5.1_05_Creative_Synthesis.log       # GLM Script 4 - 域05
└── glm5.1_06_Safety_Alignment.log         # GLM Script 4 - 域06
```

## ✅ 完成后

### 收集结果

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# 统计成功/失败任务
find output/ -name "score.json" | wc -l
find output/ -name "error.txt" | wc -l

# 汇总分数
python3 -c "
import json
from pathlib import Path

scores = []
for p in Path('output').rglob('score.json'):
    data = json.loads(p.read_text())
    scores.append(data.get('overall_score', 0))

print(f'Total tasks: {len(scores)}')
print(f'Average score: {sum(scores)/len(scores):.3f}')
print(f'Success rate: {sum(1 for s in scores if s > 0.5)/len(scores):.2%}')
"
```

### 备份结果

```bash
# 打包输出目录
cd /Users/user/Desktop/project/winder/WildClawBench
tar -czf wildclawbench_results_$(date +%Y%m%d).tar.gz output/ logs/

# 或使用rsync备份
rsync -av output/ logs/ /path/to/backup/
```
