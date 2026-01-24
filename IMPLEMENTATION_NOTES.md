# 数字人视频生成功能实现说明

## 📝 当前状态

已创建基础框架和模块，但**需要根据实际选择的平台API文档进行完善**。

## ✅ 已完成

1. **基础模块框架** (`digital_human_generator.py`)
   - 支持多平台架构
   - KreadoAI实现框架
   - 阿里云Wan-2.2-S2V实现框架
   - 统一的接口设计

2. **配置模板** (`config.yaml.digital_human.example`)
   - 完整的配置示例
   - 支持环境变量

3. **测试脚本** (`test_digital_human.py`)
   - 测试流程示例
   - 错误检查

4. **使用文档** (`DIGITAL_HUMAN_USAGE.md`)
   - 平台对比
   - 配置说明
   - 使用指南

## ⚠️ 需要完善的部分

### 1. API实现细节

当前实现是基于常见API模式的**框架代码**，需要根据实际平台的API文档进行调整：

- **KreadoAI**: 需要查询实际API端点、请求格式、响应格式
- **阿里云Wan-2.2-S2V**: 需要查询阿里云API文档
- **OmniHuman**: 需要查询API文档

### 2. 集成到主程序

需要修改 `main.py`，在TTS生成后调用数字人视频生成：

```python
# 在 generate_html_report 函数中，TTS生成后添加：
if audio_file and CONFIG.get("DIGITAL_HUMAN", {}).get("enabled", False):
    try:
        from digital_human_generator import generate_digital_human_video
        
        print("正在生成数字人视频...")
        video_config = CONFIG.get("DIGITAL_HUMAN", {})
        video_file = generate_digital_human_video(
            str(audio_file),
            video_config,
            output_file=str(Path(audio_file).parent / "口播稿.mp4")
        )
        if video_file:
            print(f"✅ 数字人视频已生成: {video_file}")
    except Exception as e:
        print(f"⚠️ 数字人视频生成出错: {e}")
```

### 3. 飞书视频发送

需要修改飞书发送逻辑，支持视频文件：

- 如果使用webhook：只能发送视频链接
- 如果使用API：可以上传视频文件

## 🔍 下一步行动

### 方案A：使用SaaS平台（推荐先做）

1. **选择平台**
   - 推荐：KreadoAI 或 阿里云
   - 访问平台官网，查看API文档

2. **获取API Key**
   - 注册账号
   - 申请API访问权限
   - 获取API Key和Secret（如需要）

3. **测试API**
   - 使用Postman或curl测试API
   - 验证请求/响应格式
   - 调整代码实现

4. **准备形象素材**
   - 准备数字人形象图片
   - 或使用平台提供的默认形象

5. **完善代码**
   - 根据实际API文档修改实现
   - 测试生成流程
   - 优化错误处理

6. **集成测试**
   - 集成到主程序
   - 测试完整流程
   - 验证飞书发送

### 方案B：使用开源方案（长期方案）

如果希望自主可控或降低成本，可以考虑：

1. **SadTalker**（推荐）
   - GitHub: https://github.com/OpenTalker/SadTalker
   - 单图+语音生成视频
   - 需要GPU支持

2. **Wav2Lip**
   - 口型同步
   - 需要配合其他工具

## 📋 集成检查清单

- [ ] 选择并注册平台
- [ ] 获取API Key
- [ ] 准备数字人形象图片
- [ ] 根据API文档完善代码
- [ ] 测试API调用
- [ ] 集成到主程序
- [ ] 配置config.yaml
- [ ] 测试完整流程
- [ ] 验证飞书发送
- [ ] 优化成本与性能

## 💡 建议

1. **先做Demo验证**
   - 选择一个平台（推荐KreadoAI）
   - 先用免费额度或试用套餐测试
   - 验证效果和成本

2. **逐步优化**
   - 先实现基本功能
   - 再优化视频质量
   - 最后优化成本

3. **成本控制**
   - 设置使用限额
   - 监控API调用次数
   - 优化视频质量设置

## 🔗 相关资源

- **KreadoAI**: https://www.kreadoai.com/zh/openapi
- **阿里云Wan-2.2-S2V**: https://help.aliyun.com/zh/model-studio/wan-s2v-api
- **OmniHuman**: https://evolink.ai/zh/omnihuman-1-5
- **SadTalker**: https://github.com/OpenTalker/SadTalker

---

**当前版本**: 框架代码（需要根据实际API完善）  
**建议**: 先选择一个平台测试，再根据实际API文档完善实现
