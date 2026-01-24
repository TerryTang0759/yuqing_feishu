# 免费平台测试指南

## 🎯 推荐测试平台（有免费额度）

### 平台1: Deep Video（推荐首先尝试）⭐

**免费额度：** 注册送1200积分 ≈ 2分钟HD视频

**测试步骤：**

1. **注册账号**
   - 访问：https://deepvideo.pro/
   - 注册并登录

2. **获取API Key**
   - 进入API设置页面
   - 获取API Key

3. **配置测试**
   ```yaml
   # config.yaml
   digital_human:
     enabled: true
     platform: "deepvideo"
     api_key: "your_api_key_from_deepvideo"
     avatar_image: "avatars/default.jpg"
     video_quality: "720p"
   ```

4. **运行测试**
   ```bash
   python3 test_digital_human.py
   ```

**优点：**
- ✅ 免费额度较充足（2分钟）
- ✅ 支持API调用
- ✅ 中文支持

### 平台2: KreadoAI

**免费额度：** 新用户3分钟免费视频

**测试步骤：**

1. **注册账号**
   - 访问：https://www.kreadoai.com/
   - 注册账号

2. **获取API Key**
   - 进入API页面
   - 申请API访问权限
   - 获取API Key和Secret

3. **配置测试**
   ```yaml
   digital_human:
     enabled: true
     platform: "kreadoai"
     api_key: "your_api_key"
     api_secret: "your_api_secret"
     video_quality: "720p"
   ```

**优点：**
- ✅ 3分钟免费额度
- ✅ API功能完善
- ✅ 支持中文

### 平台3: Cutout.pro

**免费额度：** 注册送免费积分

**测试步骤：**

1. **注册账号**
   - 访问：https://www.cutout.pro/
   - 注册账号

2. **获取API Key**
   - 进入开发者页面
   - 获取API Key

3. **配置测试**
   ```yaml
   digital_human:
     enabled: true
     platform: "cutout"
     api_key: "your_api_key"
     avatar_image: "avatars/default.jpg"
   ```

## 🧪 快速测试步骤

### 1. 准备素材

创建 `avatars/` 目录并准备一张数字人形象图片：

```bash
mkdir -p avatars
# 准备一张图片（512x512 或 1024x1024），命名为 default.jpg
```

### 2. 获取API Key

选择一个平台，注册并获取API Key

### 3. 配置测试

编辑 `config.yaml` 添加配置：

```yaml
digital_human:
  enabled: true
  platform: "deepvideo"  # 或 "kreadoai", "cutout"
  api_key: "your_api_key_here"
  avatar_image: "avatars/default.jpg"
  video_quality: "720p"
  output_format: "mp4"
```

### 4. 运行测试

```bash
# 使用现有音频测试
python3 test_digital_human.py

# 或完整流程测试
export DIGITAL_HUMAN_API_KEY="your_api_key"
python3 main.py
```

## 📝 测试检查清单

- [ ] 注册了平台账号
- [ ] 获取了API Key
- [ ] 准备了数字人形象图片（avatars/default.jpg）
- [ ] 配置了config.yaml
- [ ] 有可用的音频文件（output/.../口播稿.mp3）
- [ ] 运行了测试脚本

## ⚠️ 注意事项

1. **免费额度限制**
   - 各平台免费额度有限
   - 建议先测试1个短视频
   - 确认效果后再批量使用

2. **API调用格式**
   - 不同平台的API格式可能不同
   - 需要根据实际API文档调整代码

3. **形象图片要求**
   - 推荐尺寸：512x512 或 1024x1024
   - 格式：JPG或PNG
   - 清晰度要高

4. **生成时间**
   - 视频生成需要1-3分钟
   - 请耐心等待

## 🔗 平台注册链接

- **Deep Video**: https://deepvideo.pro/
- **KreadoAI**: https://www.kreadoai.com/zh/openapi
- **Cutout.pro**: https://www.cutout.pro/digital-human

## 💡 如果遇到问题

1. **API调用失败**
   - 检查API Key是否正确
   - 查看API文档确认格式
   - 检查网络连接

2. **免费额度用完**
   - 尝试其他平台
   - 或考虑SadTalker开源方案

3. **视频生成失败**
   - 检查形象图片是否符合要求
   - 检查音频文件格式
   - 查看错误日志

---

准备好后，告诉我你想测试哪个平台，我可以帮你完善对应的实现！
