# TTS功能快速开始指南

## 🚀 快速开始

### 1. 安装edge-tts

```bash
# 方法1
pip install edge-tts

# 方法2
python3 -m pip install edge-tts

# 方法3（如果网络有问题，使用国内镜像）
pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 2. 启用TTS功能

编辑 `config/config.yaml`，将 `tts.enabled` 设置为 `true`：

```yaml
tts:
  enabled: true  # 改为 true
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"  # 女声，温柔
  rate: "+0%"  # 正常语速
  output_format: "mp3"
```

### 3. 运行程序

```bash
python3 main.py
```

### 4. 查看生成的音频文件

```
output/2026年01月17日/script/
  ├── 口播稿.txt      # 文本口播稿
  └── 口播稿.mp3      # TTS音频文件 ⭐
```

## 🧪 测试TTS功能

运行测试脚本：

```bash
python3 test_tts.py
```

测试脚本会：
1. 生成短文本测试音频 (`test_short.mp3`)
2. 为完整口播稿生成音频 (`output/.../口播稿.mp3`)
3. 列出所有可用的中文语音

## 🎤 可用的中文语音

| 语音ID | 性别 | 风格 | 推荐场景 |
|--------|------|------|---------|
| `zh-CN-XiaoxiaoNeural` | 女 | 温柔 | 一般播报 ⭐ |
| `zh-CN-YunxiNeural` | 男 | 沉稳 | 一般播报 |
| `zh-CN-YunyangNeural` | 男 | 新闻风格 | 新闻播报 ⭐⭐⭐ |
| `zh-CN-XiaoyiNeural` | 女 | 活泼 | 轻松内容 |
| `zh-CN-YunjianNeural` | 男 | 成熟 | 专业内容 |

## ⚙️ 配置示例

### 新闻播报风格（推荐）

```yaml
tts:
  enabled: true
  engine: "edge-tts"
  voice: "zh-CN-YunyangNeural"  # 新闻风格男声
  rate: "+0%"
  output_format: "mp3"
```

### 温柔女声

```yaml
tts:
  enabled: true
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"  # 温柔女声
  rate: "+0%"
  output_format: "mp3"
```

### 稍快语速

```yaml
tts:
  enabled: true
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"
  rate: "+10%"  # 稍快10%
  output_format: "mp3"
```

## 📊 性能参考

- **生成时间**: 约1-2秒/100字
  - 1300字口播稿 ≈ 20-30秒
- **文件大小**: 约1-2 MB/1000字
  - 1300字口播稿 ≈ 1.5-2.5 MB

## ❓ 常见问题

### Q: 安装失败怎么办？

**A:** 尝试使用国内镜像：
```bash
pip install edge-tts -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 如何查看所有可用语音？

**A:** 运行：
```bash
edge-tts --list-voices | grep zh-CN
```

### Q: 音频质量如何？

**A:** edge-tts的音质接近真人发音，非常适合新闻播报。

### Q: 能否离线使用？

**A:** edge-tts需要网络连接，如需离线可以使用pyttsx3（但音质较差）。

## 📚 更多信息

详细文档请查看：`TTS_USAGE.md`
