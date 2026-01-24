# TTS语音合成功能使用指南

## 📢 功能说明

TTS（Text-to-Speech）语音合成功能可以将AI生成的口播稿自动转换为语音文件，方便制作音频节目、播客等。

## 🎯 支持的TTS引擎

### 1. edge-tts（推荐）⭐

**优点：**
- ✅ 完全免费
- ✅ 音质优秀，接近真人发音
- ✅ 支持多种中文语音
- ✅ 支持语速调节

**安装：**
```bash
pip install edge-tts
```

**配置：**
```yaml
tts:
  enabled: true
  engine: "edge-tts"
  voice: "zh-CN-XiaoxiaoNeural"  # 女声
  rate: "+0%"  # 正常语速
  output_format: "mp3"
```

**可用的中文语音：**
- `zh-CN-XiaoxiaoNeural` - 女声，温柔
- `zh-CN-YunxiNeural` - 男声，沉稳
- `zh-CN-YunyangNeural` - 男声，新闻风格
- `zh-CN-XiaoyiNeural` - 女声，活泼
- `zh-CN-YunjianNeural` - 男声，成熟

**查看所有可用语音：**
```bash
edge-tts --list-voices | grep zh-CN
```

### 2. gTTS（Google Text-to-Speech）

**优点：**
- ✅ 免费
- ✅ 使用简单

**缺点：**
- ⚠️ 需要网络连接
- ⚠️ 音质一般

**安装：**
```bash
pip install gtts
```

**配置：**
```yaml
tts:
  enabled: true
  engine: "gtts"
  output_format: "mp3"
```

### 3. pyttsx3（离线TTS）

**优点：**
- ✅ 完全离线
- ✅ 无需网络

**缺点：**
- ⚠️ 中文支持有限（需要系统安装中文语音包）
- ⚠️ 音质一般

**安装：**
```bash
pip install pyttsx3
```

**配置：**
```yaml
tts:
  enabled: true
  engine: "pyttsx3"
  output_format: "wav"  # 只支持wav格式
```

## 🚀 使用方法

### 1. 启用TTS功能

在 `config/config.yaml` 中配置：

```yaml
tts:
  enabled: true  # 启用TTS
  engine: "edge-tts"  # 选择引擎
  voice: "zh-CN-XiaoxiaoNeural"
  rate: "+0%"
  output_format: "mp3"
```

### 2. 运行程序

正常运行主程序，口播稿生成后会自动生成TTS音频：

```bash
python3 main.py
```

### 3. 查看生成的文件

生成的文件位置：
```
output/YYYY年MM月DD日/script/
  ├── 口播稿.txt      # 文本口播稿
  └── 口播稿.mp3      # TTS音频文件
```

## 📊 性能说明

### 生成时间
- **edge-tts**: 约1-2秒/100字
- **gTTS**: 约1-2秒/100字（依赖网络）
- **pyttsx3**: 约0.5秒/100字（本地）

### 文件大小
- **1300字口播稿**:
  - mp3格式: 约1-2 MB
  - wav格式: 约10-20 MB

## 🔧 高级配置

### 调整语速

edge-tts支持语速调节（-50% 到 +100%）：

```yaml
tts:
  rate: "+10%"  # 稍快
  rate: "-10%"  # 稍慢
  rate: "+0%"   # 正常
```

### 切换语音风格

根据不同场景选择合适的语音：

```yaml
# 新闻播报风格
voice: "zh-CN-YunyangNeural"

# 温柔女声
voice: "zh-CN-XiaoxiaoNeural"

# 沉稳男声
voice: "zh-CN-YunxiNeural"
```

### 长文本处理

如果口播稿超过5000字，TTS模块会自动分段处理。如需合并音频，需要安装ffmpeg：

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# 下载 https://ffmpeg.org/download.html
```

## 💡 使用技巧

### 1. 独立生成TTS

如果只想为已有口播稿生成TTS：

```python
from tts_generator import generate_tts_audio

config = {
    "enabled": True,
    "engine": "edge-tts",
    "voice": "zh-CN-XiaoxiaoNeural",
    "rate": "+0%",
    "output_format": "mp3"
}

audio_file = generate_tts_audio(
    "output/2026年01月17日/script/口播稿.txt",
    config
)
```

### 2. 批量生成

为历史口播稿批量生成TTS：

```bash
# 查找所有口播稿
find output -name "口播稿.txt" -type f | while read file; do
    python3 -c "
from tts_generator import generate_tts_audio
config = {'enabled': True, 'engine': 'edge-tts', 'voice': 'zh-CN-XiaoxiaoNeural', 'rate': '+0%', 'output_format': 'mp3'}
generate_tts_audio('$file', config)
"
done
```

### 3. 音频后处理

生成音频后，可以使用ffmpeg进行后处理：

```bash
# 调整音量
ffmpeg -i 口播稿.mp3 -af "volume=1.2" 口播稿_大声.mp3

# 添加淡入淡出
ffmpeg -i 口播稿.mp3 -af "afade=t=in:st=0:d=1,afade=t=out:st=20:d=1" 口播稿_淡入淡出.mp3

# 转换为其他格式
ffmpeg -i 口播稿.mp3 口播稿.wav
```

## ❓ 常见问题

### Q1: TTS生成失败怎么办？

**检查：**
1. 确认已安装对应的TTS库
2. 检查网络连接（gTTS需要网络）
3. 查看错误日志

### Q2: 音频质量不好？

**建议：**
1. 使用edge-tts（推荐）
2. 选择合适的语音（zh-CN-YunyangNeural适合新闻）
3. 调整语速到合适范围

### Q3: 长文本处理很慢？

**优化：**
1. 安装ffmpeg支持合并功能
2. 考虑分段处理
3. 使用离线引擎（pyttsx3）

### Q4: 如何在HTML中嵌入音频？

在HTML报告中可以添加音频播放器：

```html
<audio controls>
  <source src="script/口播稿.mp3" type="audio/mpeg">
  您的浏览器不支持音频播放。
</audio>
```

## 📚 参考资源

- [edge-tts GitHub](https://github.com/rany2/edge-tts)
- [gTTS 文档](https://gtts.readthedocs.io/)
- [pyttsx3 文档](https://pyttsx3.readthedocs.io/)
- [Microsoft Edge TTS 语音列表](https://speech.platform.bing.com/consumer/speech/synthesize/readaloud/voices/list)

---

**最后更新**: 2026-01-17  
**版本**: v2.4.0 + TTS功能
