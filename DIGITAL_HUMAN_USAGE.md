# 数字人视频生成功能使用指南

## 📹 功能说明

可以将TTS语音转换成带说话动作、口型同步的数字人视频，提升内容的视觉吸引力和专业度。

## 🎯 支持的平台

### 1. KreadoAI ⭐（推荐，功能丰富）

**特点：**
- ✅ 支持多种数字人形象
- ✅ 高质量口型同步
- ✅ 支持中文
- ✅ API完善

**配置：**
```yaml
digital_human:
  enabled: true
  platform: "kreadoai"
  api_key: "your_api_key"  # 或使用环境变量 DIGITAL_HUMAN_API_KEY
  api_secret: "your_api_secret"  # 或使用环境变量 DIGITAL_HUMAN_API_SECRET
  avatar_image: "avatars/default.jpg"  # 数字人形象图片（可选）
  avatar_id: ""  # 或使用平台提供的默认形象ID
  video_quality: "720p"  # 720p 或 1080p
  output_format: "mp4"
```

**注册：**
- 访问 https://www.kreadoai.com/
- 注册账号并获取API Key

### 2. 阿里云Wan-2.2-S2V（国内友好）

**特点：**
- ✅ 国内平台，访问稳定
- ✅ 支持说话/唱歌/表演模式
- ✅ 按秒计费

**配置：**
```yaml
digital_human:
  enabled: true
  platform: "aliyun"
  api_key: "your_api_key"  # 阿里云API Key
  avatar_image: "avatars/default.jpg"  # 必需：数字人形象图片
  video_resolution: "720p"  # 480p, 720p
  output_format: "mp4"
```

**注册：**
- 访问 https://dashscope.aliyun.com/
- 开通Wan-2.2-S2V服务
- 获取API Key

### 3. OmniHuman 1.5（高质量）

**特点：**
- ✅ 高质量视频输出
- ✅ 相机运动、表情优化
- ⚠️ 成本较高

**配置：**
```yaml
digital_human:
  enabled: true
  platform: "omnihuman"
  api_key: "your_api_key"
  avatar_image: "avatars/default.jpg"
  output_format: "mp4"
```

## 🚀 使用方法

### 1. 准备数字人形象图片

准备一张数字人形象图片（推荐尺寸：512x512 或 1024x1024）：
- 可以是真人照片
- 可以是AI生成的虚拟形象
- 可以是卡通角色

将图片放在 `avatars/` 目录下，或指定完整路径。

### 2. 配置

在 `config/config.yaml` 中添加：

```yaml
# 数字人视频生成配置（可选功能）
# 支持 KreadoAI、阿里云Wan-2.2-S2V等平台
digital_human:
  enabled: true  # 是否启用数字人视频生成
  platform: "kreadoai"  # 平台选择
  api_key: ""  # API密钥（建议使用环境变量）
  api_secret: ""  # API密钥（如需要）
  avatar_image: "avatars/news_host.jpg"  # 数字人形象图片路径
  video_quality: "720p"  # 视频质量
  output_format: "mp4"  # 输出格式
```

### 3. 运行程序

```bash
python3 main.py
```

程序会自动：
1. 生成口播稿文本
2. 生成TTS音频
3. 生成数字人视频 ⭐
4. 发送到飞书群

### 4. 查看生成的文件

```
output/YYYY年MM月DD日/script/
  ├── 口播稿.txt      # 文本口播稿
  ├── 口播稿.mp3      # TTS音频
  └── 口播稿.mp4      # 数字人视频 ⭐
```

## 💰 成本参考

| 平台 | 计费方式 | 预估成本（1分钟视频） |
|------|---------|---------------------|
| KreadoAI | 按秒/按质量 | $0.5-2/分钟 |
| 阿里云Wan-2.2-S2V | 按秒计费 | ¥0.1-0.5/秒 ≈ ¥6-30/分钟 |
| OmniHuman | 按秒/高质量 | $1-5/分钟 |

**注意：**
- 以上价格为参考，具体以平台实际价格为准
- 建议先用免费额度或试用套餐测试

## ⏱️ 生成时间

- **音频上传**: 约5-10秒
- **视频生成**: 约30-120秒（取决于视频长度和平台）
- **视频下载**: 约10-30秒（取决于文件大小）
- **总计**: 约1-3分钟/分钟视频

## 📊 视频规格

- **分辨率**: 720p 或 1080p（取决于平台和配置）
- **格式**: MP4
- **文件大小**: 约5-30 MB/分钟（取决于质量）
- **帧率**: 25/30 fps

## 🔍 故障排查

### 问题1: API调用失败

**检查：**
1. ✅ API Key是否正确
2. ✅ 网络连接是否正常
3. ✅ API余额是否充足

### 问题2: 形象图片问题

**检查：**
1. ✅ 图片路径是否正确
2. ✅ 图片格式是否支持（JPG/PNG）
3. ✅ 图片大小是否在限制内

### 问题3: 视频生成超时

**解决方案：**
- 增加超时时间配置
- 检查视频长度（建议不超过5分钟）
- 降低视频质量（720p → 480p）

### 问题4: 视频文件过大

**解决方案：**
- 降低视频质量
- 压缩视频文件
- 使用外链而非直接发送文件

## ⚙️ 环境变量配置（推荐）

```bash
# 使用环境变量存储API密钥（更安全）
export DIGITAL_HUMAN_API_KEY="your_api_key"
export DIGITAL_HUMAN_API_SECRET="your_api_secret"
```

**GitHub Actions配置：**
- 在仓库 Settings → Secrets 中添加：
  - `DIGITAL_HUMAN_API_KEY`
  - `DIGITAL_HUMAN_API_SECRET`

## 📝 注意事项

1. **版权与隐私**
   - ⚠️ 确保形象图片的使用权
   - ⚠️ 不要使用未经授权的真人照片

2. **成本控制**
   - 视频生成会产生费用
   - 建议先测试，确认效果后再批量使用
   - 设置使用限额或预算

3. **文件存储**
   - 视频文件较大（5-30MB/分钟）
   - GitHub Actions有存储限制
   - 建议压缩或使用云存储

4. **生成时间**
   - 视频生成比音频生成慢
   - 可能增加整体运行时间
   - 建议异步处理或使用队列

## 🎯 推荐配置（首次使用）

```yaml
digital_human:
  enabled: false  # 先禁用，测试好后再启用
  platform: "kreadoai"  # 推荐KreadoAI（功能完善）
  api_key: ""  # 从环境变量读取
  avatar_image: "avatars/default.jpg"
  video_quality: "720p"  # 先使用720p测试
  output_format: "mp4"
```

## 📚 平台文档链接

- **KreadoAI**: https://www.kreadoai.com/zh/openapi
- **阿里云Wan-2.2-S2V**: https://help.aliyun.com/zh/model-studio/wan-s2v-api
- **OmniHuman**: https://evolink.ai/zh/omnihuman-1-5

---

**最后更新**: 2026-01-17  
**版本**: v2.6.0 + 数字人视频生成
