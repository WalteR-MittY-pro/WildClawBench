# ✅ WildClawBench 配置更新完成

## 📋 更新内容

### 模型变更
- **原配置**: GPT-5.4-mini
- **新配置**: GPT-5.4 ✅

### 已更新文件

1. **配置文件**
   - ✅ `models_config_gpt5.4mini.json` → `models_config_gpt5.4.json`
   - 模型ID: `gpt-5.4`
   - 模型名称: `openai/gpt-5.4`

2. **执行脚本（4个）**
   - ✅ `run_gpt_script1.sh` - 引用更新为 `models_config_gpt5.4.json`
   - ✅ `run_gpt_script2.sh` - 引用更新为 `models_config_gpt5.4.json`
   - ✅ `run_gpt_script3.sh` - 引用更新为 `models_config_gpt5.4.json`
   - ✅ `run_gpt_script4.sh` - 引用更新为 `models_config_gpt5.4.json`

3. **启动脚本**
   - ✅ `start_all_baselines.sh` - 描述更新为 GPT-5.4

4. **日志文件名**
   - ✅ `logs/gpt5.4mini_*.log` → `logs/gpt5.4_*.log`

## 🎯 最终配置总览

### GPT-5.4 配置
```json
{
  "moduleModels": {
    "openclaw_agent": "gpt-5.4",
    "oracle": "gpt-5.4"
  },
  "runtime": {
    "oracle_rate_limit_retries": 2,
    "oracle_rate_limit_wait_seconds": 120,
    "llm_timeout_seconds": 300,
    "llm_max_retries": 1
  },
  "stream": true,
  "providers": {
    "openai": {
      "baseUrl": "${GPT_BASE_URL}",
      "apiKey": "${GPT_API_KEY}",
      "api": "openai-completions"
    }
  }
}
```

### GLM-5.1 配置（SSE支持）
```json
{
  "moduleModels": {
    "openclaw_agent": "GLM-5.1",
    "oracle": "GLM-5.1"
  },
  "runtime": {
    "oracle_rate_limit_retries": 2,
    "oracle_rate_limit_wait_seconds": 120,
    "llm_timeout_seconds": 600,
    "llm_max_retries": 2
  },
  "stream": true,
  "providers": {
    "glm": {
      "baseUrl": "${GLM_BASE_URL}",
      "apiKey": "${GLM_API_KEY}",
      "api": "openai-compatible"
    }
  }
}
```

## 🚀 立即执行

### 一键启动所有任务

```bash
cd /Users/user/Desktop/project/winder/WildClawBench
./start_all_baselines.sh
```

### 手动启动（后台运行）

```bash
cd /Users/user/Desktop/project/winder/WildClawBench

# GPT-5.4任务
nohup ./run_gpt_script1.sh > logs/nohup_gpt1.out 2>&1 &
nohup ./run_gpt_script2.sh > logs/nohup_gpt2.out 2>&1 &
nohup ./run_gpt_script3.sh > logs/nohup_gpt3.out 2>&1 &
nohup ./run_gpt_script4.sh > logs/nohup_gpt4.out 2>&1 &

# GLM-5.1任务
nohup ./run_glm_script1.sh > logs/nohup_glm1.out 2>&1 &
nohup ./run_glm_script2.sh > logs/nohup_glm2.out 2>&1 &
nohup ./run_glm_script3.sh > logs/nohup_glm3.out 2>&1 &
nohup ./run_glm_script4.sh > logs/nohup_glm4.out 2>&1 &
```

## 📊 任务分配

### GPT-5.4（4个脚本）
| 脚本 | 域 | .env文件 | API Key | 日志文件 |
|------|-----|----------|---------|----------|
| Script 1 | 01_Productivity_Flow | .env | KEY1 | logs/gpt5.4_cat01.log |
| Script 2 | 02_Code_Intelligence | .env | KEY1 | logs/gpt5.4_cat02.log |
| Script 3 | 03_Social_Interaction | .env2 | KEY2 | logs/gpt5.4_cat03.log |
| Script 4 | 04+05+06 | .env2 | KEY2 | logs/gpt5.4_04_*.log, logs/gpt5.4_05_*.log, logs/gpt5.4_06_*.log |

### GLM-5.1（4个脚本）
| 脚本 | 域 | .env文件 | API Key | 日志文件 |
|------|-----|----------|---------|----------|
| Script 1 | 01_Productivity_Flow | .env | 共享 | logs/glm5.1_cat01.log |
| Script 2 | 02_Code_Intelligence | .env | 共享 | logs/glm5.1_cat02.log |
| Script 3 | 03_Social_Interaction | .env | 共享 | logs/glm5.1_cat03.log |
| Script 4 | 04+05+06 | .env | 共享 | logs/glm5.1_04_*.log, logs/glm5.1_05_*.log, logs/glm5.1_06_*.log |

## 📈 监控命令

```bash
# 查看日志
tail -f logs/gpt5.4_cat01.log
tail -f logs/glm5.1_cat01.log

# 查看进程
ps aux | grep run_.*_script | grep -v grep

# 查看完成进度
find output/ -name "score.json" 2>/dev/null | wc -l
```

## ⚙️ 关键配置对比

| 项目 | GPT-5.4 | GLM-5.1 |
|------|---------|---------|
| **模型** | gpt-5.4 | GLM-5.1 |
| **API类型** | openai-completions | openai-compatible (SSE) ✅ |
| **Timeout** | 300s | 600s ✅ |
| **重试次数** | 1 | 2 ✅ |
| **API Key** | KEY1 + KEY2 (分散) | 共享KEY |
| **Stream** | true | true |

## ✅ 所有配置已就绪

现在你可以直接执行命令启动8个baseline任务！

```bash
cd /Users/user/Desktop/project/winder/WildClawBench
./start_all_baselines.sh
```
