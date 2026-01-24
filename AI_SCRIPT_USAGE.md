# AI口播稿功能使用指南

## 🎯 功能简介

AI口播稿生成功能可以自动将热点新闻数据转化为专业、简洁的口播稿，适合：
- 📻 播客节目准备
- 📺 视频内容创作
- 🎙️ 语音播报系统
- 📝 新闻简报制作

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 配置API密钥

#### 方法一：环境变量（推荐）

```bash
# Linux/Mac
export AI_API_KEY="your_api_key_here"
export AI_API_TYPE="deepseek"
export AI_MODEL="deepseek-chat"

# Windows
set AI_API_KEY=your_api_key_here
set AI_API_TYPE=deepseek
set AI_MODEL=deepseek-chat
```

#### 方法二：配置文件

编辑 `config/config.yaml`：

```yaml
ai_script:
  enabled: true
  api_type: "deepseek"
  api_key: "your_api_key_here"  # ⚠️ 注意：不要提交到公开仓库
  model: "deepseek-chat"
  max_tokens: 1000
  temperature: 0.7
```

### 3. 启用功能

在 `config/config.yaml` 中设置：

```yaml
ai_script:
  enabled: true  # 改为 true
```

### 4. 运行程序

```bash
python3 main.py
```

口播稿将自动生成并保存到：
- `output/YYYY年MM月DD日/script/口播稿.txt`

## 🔑 API配置说明

### DeepSeek（推荐，性价比高）

```yaml
ai_script:
  enabled: true
  api_type: "deepseek"
  api_key: "sk-xxxxx"  # 从 https://platform.deepseek.com 获取
  model: "deepseek-chat"
  api_base: ""  # 使用默认值
```

**优势：**
- ✅ 价格便宜（比OpenAI便宜很多）
- ✅ 中文理解能力强
- ✅ 响应速度快

### OpenAI

```yaml
ai_script:
  enabled: true
  api_type: "openai"
  api_key: "sk-xxxxx"  # 从 https://platform.openai.com 获取
  model: "gpt-3.5-turbo"  # 或 "gpt-4"
  api_base: ""  # 使用默认值
```

### Claude

```yaml
ai_script:
  enabled: true
  api_type: "claude"
  api_key: "sk-ant-xxxxx"  # 从 https://console.anthropic.com 获取
  model: "claude-3-sonnet-20240229"
  api_base: ""  # 使用默认值
```

### 自定义API

```yaml
ai_script:
  enabled: true
  api_type: "custom"
  api_key: "your_api_key"
  api_base: "https://your-api-endpoint.com/v1/chat"
  model: "your-model-name"
```

## 📝 口播稿示例

```
【2026年1月17日 财经新闻口播稿】

各位听众，大家好。今天是2026年1月17日，为您带来今日财经热点。

首先，芯片行业传来重大消息。中国芯片迎来最大IPO，同时我国芯片制造核心装备取得重要突破，这标志着中国半导体产业进入新的发展阶段。

其次，贸易政策方面，特朗普威胁对不支持美国控制格陵兰岛计划的国家加征关税，引发市场关注。同时，加拿大总理宣布中国将加油菜籽关税降至15%，为双边贸易带来积极信号。

此外，人工智能领域持续活跃。ChatGPT加入广告功能引发讨论，AI算力需求推动PCB业务爆发，相关企业业绩大幅预增。

在能源市场，伊拉克石油出口数据公布，原油价格波动值得关注。黄金市场方面，有分析师认为黄金已失去吸引力，建议关注中国股市的可持续上涨机会。

最后，A股市场方面，半导体封测概念股两日累计涨超30%，但整体市场仍面临四连跌压力，退守4100点。

以上就是今日财经热点，感谢收听。
```

## ⚙️ 参数调优

### temperature（创造性）

- `0.3-0.5`：更保守、准确，适合严肃新闻
- `0.7`：平衡，推荐值
- `0.8-1.0`：更有创造性，但可能不够准确

### max_tokens（长度）

- `500-800`：简短版（30-60秒）
- `1000-1500`：标准版（60-90秒）⭐ 推荐
- `2000+`：详细版（90-120秒）

## 🔧 集成到主程序

### 方法一：直接修改 main.py

1. 在文件顶部添加导入：
```python
try:
    from ai_news_script_generator import generate_news_script
    AI_SCRIPT_AVAILABLE = True
except ImportError:
    AI_SCRIPT_AVAILABLE = False
```

2. 在 `load_config()` 中添加AI配置加载（参考 `integrate_ai_script_example.py`）

3. 在生成报告后调用：
```python
if AI_SCRIPT_AVAILABLE and CONFIG["AI_SCRIPT"]["ENABLED"]:
    report_data = {"stats": stats, "total_titles": total}
    script = generate_news_script(report_data, CONFIG["AI_SCRIPT"])
    if script:
        # 保存口播稿
        script_file = Path(output_dir) / "script" / "口播稿.txt"
        script_file.parent.mkdir(parents=True, exist_ok=True)
        script_file.write_text(script, encoding="utf-8")
```

### 方法二：使用独立脚本

创建 `generate_script.py`：

```python
import json
from ai_news_script_generator import generate_news_script
from pathlib import Path

# 读取API数据
with open("api/trends.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 转换为报告数据格式
report_data = {
    "stats": [
        {
            "word": trend["keyword_group"],
            "count": trend["match_count"],
            "titles": trend["titles"]
        }
        for trend in data["trends"]
    ],
    "total_titles": data["total_titles_processed"]
}

# 配置
ai_config = {
    "enabled": True,
    "api_type": "deepseek",
    "api_key": "your_api_key",
    "model": "deepseek-chat",
    "max_tokens": 1000,
    "temperature": 0.7
}

# 生成口播稿
script = generate_news_script(report_data, ai_config)

if script:
    # 保存
    output_file = Path("output") / "script" / "口播稿.txt"
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(script, encoding="utf-8")
    print(f"✅ 口播稿已生成: {output_file}")
```

运行：
```bash
python3 generate_script.py
```

## 💡 使用技巧

### 1. 优化提示词

修改 `ai_news_script_generator.py` 中的 `_build_prompt()` 方法，自定义提示词：

```python
prompt = f"""你是一位专业的财经新闻主播。请根据以下热点新闻，生成一段专业、简洁的新闻口播稿。

要求：
1. 时长控制在60-90秒（约200-300字）
2. 语言专业、流畅，适合口播
3. 突出重点，按重要性排序
4. 使用"首先"、"其次"、"此外"等连接词
5. 开头要有时间提示，结尾要有总结
6. 风格：{style}  # 可以添加风格参数

热点新闻摘要：
{news_text}

请生成口播稿："""
```

### 2. 批量生成

可以针对不同主题生成多个口播稿：

```python
# 按关键词组分组生成
for stat in stats:
    if stat["count"] >= 3:  # 只处理有足够新闻的主题
        report_data = {"stats": [stat], "total_titles": stat["count"]}
        script = generate_news_script(report_data, ai_config)
        # 保存到不同文件
```

### 3. 多语言支持

修改提示词支持英文、日文等：

```python
prompt = f"""You are a professional financial news anchor. Please generate a professional, concise news script based on the following hot news.

Language: English
Duration: 60-90 seconds (about 200-300 words)
...
"""
```

## 🐛 故障排除

### 问题1：API调用失败

**错误信息：** `⚠️ AI口播稿生成失败: ...`

**解决方案：**
1. 检查API密钥是否正确
2. 检查网络连接
3. 检查API余额
4. 查看详细错误信息

### 问题2：生成内容为空

**可能原因：**
- API返回格式不正确
- Token限制太小
- 新闻数据为空

**解决方案：**
1. 增加 `max_tokens` 值
2. 检查新闻数据是否正常
3. 查看API响应日志

### 问题3：生成速度慢

**解决方案：**
1. 使用更快的模型（如 `gpt-3.5-turbo` 而非 `gpt-4`）
2. 减少 `max_tokens`
3. 异步调用API

## 📊 成本估算

### DeepSeek（推荐）

- 价格：约 $0.14 / 1M tokens（输入+输出）
- 单次生成：约 2000 tokens
- 成本：约 $0.0003 / 次（约 0.002 元人民币）
- 每天10次：约 0.02 元/天

### OpenAI GPT-3.5-turbo

- 价格：约 $1.5 / 1M tokens
- 单次生成：约 2000 tokens
- 成本：约 $0.003 / 次（约 0.02 元人民币）
- 每天10次：约 0.2 元/天

### OpenAI GPT-4

- 价格：约 $30 / 1M tokens
- 单次生成：约 2000 tokens
- 成本：约 $0.06 / 次（约 0.4 元人民币）
- 每天10次：约 4 元/天

## 🎉 下一步

1. ✅ 配置API密钥
2. ✅ 启用功能
3. ✅ 测试生成效果
4. ⏳ 集成到主程序
5. ⏳ 优化提示词
6. ⏳ 添加语音合成（TTS）
