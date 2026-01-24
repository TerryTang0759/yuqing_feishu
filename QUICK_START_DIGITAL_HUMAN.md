# 数字人视频生成 - 快速开始指南

## 🚀 5分钟快速测试

### 步骤1: 选择一个平台并注册（3分钟）

**推荐：Deep Video（最简单）**

1. 访问：https://deepvideo.pro/
2. 注册账号（使用邮箱或手机号）
3. 进入API设置页面
4. 获取API Key

**或 KreadoAI：**

1. 访问：https://www.kreadoai.com/
2. 注册账号
3. 申请API访问
4. 获取API Key和Secret

### 步骤2: 准备数字人形象（1分钟）

```bash
# 创建目录
mkdir -p avatars

# 准备一张图片（512x512 或 1024x1024）
# 可以是：
# - 真人照片
# - AI生成的虚拟形象
# - 卡通角色
# 保存为 avatars/default.jpg
```

**图片要求：**
- 尺寸：512x512 或 1024x1024
- 格式：JPG或PNG
- 清晰度：高清

### 步骤3: 配置并测试（1分钟）

```bash
# 1. 设置API Key（推荐使用环境变量）
export DIGITAL_HUMAN_API_KEY="your_api_key_here"

# 2. 如果有API Secret
export DIGITAL_HUMAN_API_SECRET="your_api_secret_here"

# 3. 配置config.yaml（添加digital_human部分）
# 参考 config.yaml.digital_human.example

# 4. 运行测试
python3 test_digital_human.py
```

### 步骤4: 集成到主程序（可选）

如果测试成功，在主程序中使用：

```bash
# 运行时会自动生成数字人视频
python3 main.py
```

## 📋 配置示例

在 `config/config.yaml` 中添加：

```yaml
# 数字人视频生成配置
digital_human:
  enabled: true  # 启用数字人视频生成
  platform: "deepvideo"  # 或 "kreadoai"
  api_key: ""  # 从环境变量读取（推荐）
  api_secret: ""  # 如需要
  avatar_image: "avatars/default.jpg"  # 形象图片路径
  video_quality: "720p"  # 视频质量
  output_format: "mp4"  # 输出格式
```

## ✅ 测试清单

- [ ] 已注册平台账号
- [ ] 已获取API Key
- [ ] 已准备形象图片（avatars/default.jpg）
- [ ] 已配置config.yaml
- [ ] 已有音频文件（output/.../口播稿.mp3）
- [ ] 已运行测试脚本

## 🎯 预期结果

测试成功后，会在以下位置生成视频：

```
output/2026年01月17日/script/
  ├── 口播稿.txt      # 文本口播稿
  ├── 口播稿.mp3      # TTS音频
  └── 口播稿.mp4      # 数字人视频 ⭐
```

## ⚠️ 可能遇到的问题

### 问题1: API Key错误
**解决：** 检查API Key是否正确，是否从环境变量读取

### 问题2: 形象图片未找到
**解决：** 确认图片路径正确，图片存在

### 问题3: API格式不匹配
**解决：** 不同平台API格式可能不同，需要根据实际文档调整代码

### 问题4: 免费额度用完
**解决：** 尝试其他平台，或考虑开源方案

## 💡 提示

1. **先测试一个小视频**：确认效果和流程
2. **保存API Key**：使用环境变量，不要提交到仓库
3. **查看免费额度**：确认还剩余多少免费额度
4. **准备备用方案**：如果平台不可用，考虑其他选项

## 🔗 相关文档

- `DIGITAL_HUMAN_USAGE.md` - 详细使用文档
- `COST_ANALYSIS.md` - 成本分析
- `IMPLEMENTATION_NOTES.md` - 实现说明
- `test_free_platforms.md` - 免费平台测试指南

---

准备好后开始测试吧！ 🚀
