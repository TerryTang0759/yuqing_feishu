# GitHub Actions 部署 TTS 功能指南

## ✅ TTS在GitHub Actions中的可行性分析

### 1. 技术可行性

| 项目 | 状态 | 说明 |
|------|------|------|
| **网络访问** | ✅ 支持 | GitHub Actions默认有网络访问，edge-tts可以调用Microsoft Edge TTS API |
| **依赖安装** | ✅ 支持 | pip install edge-tts 在Ubuntu环境中可以正常安装 |
| **运行环境** | ✅ 支持 | Ubuntu-latest环境完全支持Python和edge-tts |
| **文件大小** | ✅ 支持 | 音频文件约1.6MB，远低于GitHub的100MB限制 |
| **存储空间** | ✅ 支持 | GitHub仓库可以存储音频文件，会提交到output目录 |

### 2. 潜在问题

| 问题 | 影响 | 解决方案 |
|------|------|---------|
| **执行时间** | ⚠️ 轻微 | TTS生成需要20-30秒，可能增加总运行时间（GitHub Actions免费版有45分钟限制） |
| **依赖安装** | ⚠️ 需要配置 | 需要在requirements.txt中添加edge-tts |
| **配置启用** | ⚠️ 需要配置 | 需要在config.yaml中启用TTS，或通过环境变量控制 |
| **文件提交** | ✅ 自动 | GitHub Actions会自动提交生成的音频文件 |

## 🚀 部署步骤

### 步骤1: 更新 requirements.txt

确保 `requirements.txt` 包含 `edge-tts`：

```txt
# ... 其他依赖 ...
edge-tts>=6.1.0
```

### 步骤2: 更新 GitHub Actions 配置

更新 `.github/workflows/crawler.yml`，添加环境变量（如果需要）：

```yaml
- name: Run crawler
  env:
    FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
    TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
    TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
    DINGTALK_WEBHOOK_URL: ${{ secrets.DINGTALK_WEBHOOK_URL }}
    WEWORK_WEBHOOK_URL: ${{ secrets.WEWORK_WEBHOOK_URL }}
    AI_API_KEY: ${{ secrets.AI_API_KEY }}  # AI口播稿API密钥
    GITHUB_ACTIONS: true
  run: python main.py
```

### 步骤3: 配置 TTS 功能

有两种方式：

#### 方式1: 在 config.yaml 中启用（推荐）

编辑 `config/config.yaml`：

```yaml
tts:
  enabled: true  # 启用TTS
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"
  rate: "+0%"
  output_format: "mp3"
```

**注意**: 如果提交config.yaml到仓库，所有运行都会启用TTS。

#### 方式2: 通过环境变量控制（灵活）

在 `.github/workflows/crawler.yml` 中添加：

```yaml
env:
  # ... 其他环境变量 ...
  TTS_ENABLED: "true"  # 控制TTS是否启用
```

然后在代码中检查环境变量（需要修改main.py）。

### 步骤4: 处理音频文件

GitHub Actions会自动提交生成的音频文件：

```
output/YYYY年MM月DD日/script/
  ├── 口播稿.txt
  └── 口播稿.mp3  # 会自动提交到仓库
```

**注意事项**:
- 音频文件会占用仓库空间（每次运行约1.6MB）
- 如果每天运行多次，会累积文件
- 建议定期清理或使用Git LFS（如果文件很多）

## 📊 性能影响

### 运行时间分析

| 步骤 | 时间（本地） | 时间（GitHub Actions） |
|------|-------------|----------------------|
| 爬取新闻 | 10-15秒 | 10-15秒 |
| 处理数据 | 1-2秒 | 1-2秒 |
| 生成口播稿 | 5-10秒 | 5-10秒 |
| **生成TTS** | **20-30秒** | **20-30秒** ⚠️ |
| 生成报告 | 1-2秒 | 1-2秒 |
| **总计** | **40-60秒** | **40-60秒** |

**结论**: TTS会增加约30秒的运行时间，但仍在GitHub Actions的45分钟限制内。

## ⚙️ 推荐配置

### 1. 生产环境推荐（GitHub Actions）

```yaml
# config/config.yaml
tts:
  enabled: true  # 启用TTS
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"  # 或 zh-CN-YunyangNeural（新闻风格）
  rate: "+0%"
  output_format: "mp3"
```

### 2. 节省空间的方案（可选）

如果担心仓库空间，可以：

#### 选项A: 不启用TTS（默认）
```yaml
tts:
  enabled: false  # 不生成TTS，只保留文本口播稿
```

#### 选项B: 使用.gitignore过滤音频文件
在 `.gitignore` 中添加：
```
output/**/*.mp3
```

#### 选项C: 定期清理旧音频
创建清理脚本，保留最近N天的音频。

## 🔍 故障排查

### 问题1: TTS生成失败

**检查项**:
1. ✅ `requirements.txt` 是否包含 `edge-tts`
2. ✅ `config.yaml` 中 `tts.enabled` 是否为 `true`
3. ✅ GitHub Actions日志中是否有错误信息

**解决方案**:
```bash
# 检查依赖安装
pip list | grep edge-tts

# 检查配置文件
cat config/config.yaml | grep -A 5 "^tts:"
```

### 问题2: 网络连接问题

**症状**: TTS生成超时或失败

**解决方案**:
- edge-tts需要访问 `speech.platform.bing.com`
- GitHub Actions默认可以访问，如果失败可能是临时网络问题
- 可以重试或使用gTTS作为备选

### 问题3: 文件提交失败

**症状**: 音频文件未提交到仓库

**检查项**:
1. ✅ `.gitignore` 是否排除了 `.mp3` 文件
2. ✅ GitHub Actions权限是否正确（`contents: write`）

## 📝 完整示例配置

### requirements.txt
```txt
requests>=2.28.0
pyyaml>=6.0
flask>=2.0.0
playwright>=1.20.0
edge-tts>=6.1.0  # TTS功能依赖
```

### .github/workflows/crawler.yml（更新后）
```yaml
name: Hot News Crawler

on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  crawl:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.9"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          playwright install --with-deps

      - name: Verify required files
        run: |
          echo "🔍 检查必需的配置文件..."
          if [ ! -f config/config.yaml ]; then
            echo "❌ 错误: config/config.yaml 文件不存在"
            exit 1
          fi
          if [ ! -f config/frequency_words.txt ]; then
            echo "❌ 错误: config/frequency_words.txt 文件不存在"
            exit 1
          fi
          echo "✅ 配置文件检查通过"

      - name: Run crawler
        env:
          FEISHU_WEBHOOK_URL: ${{ secrets.FEISHU_WEBHOOK_URL }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          DINGTALK_WEBHOOK_URL: ${{ secrets.DINGTALK_WEBHOOK_URL }}
          WEWORK_WEBHOOK_URL: ${{ secrets.WEWORK_WEBHOOK_URL }}
          AI_API_KEY: ${{ secrets.AI_API_KEY }}
          GITHUB_ACTIONS: true
        run: python main.py

      - name: Commit and push if changes
        run: |
          git config --global user.name 'GitHub Actions'
          git config --global user.email 'actions@github.com'
          git add -A
          git diff --quiet && git diff --staged --quiet || (git commit -m "Auto update by GitHub Actions at $(TZ=Asia/Shanghai date)" && git push)
```

## ✅ 总结

### TTS在GitHub Actions中的可行性：✅ **完全可行**

**优点**:
- ✅ 网络访问支持
- ✅ 依赖安装简单
- ✅ 文件大小合适
- ✅ 自动提交到仓库

**注意事项**:
- ⚠️ 会增加20-30秒运行时间
- ⚠️ 需要更新requirements.txt
- ⚠️ 音频文件会占用仓库空间

**推荐做法**:
1. ✅ 更新 `requirements.txt` 添加 `edge-tts`
2. ✅ 在 `config.yaml` 中启用TTS
3. ✅ 监控运行时间和仓库空间
4. ✅ 根据需要调整TTS启用策略

---

**最后更新**: 2026-01-17  
**测试环境**: GitHub Actions (Ubuntu-latest)
