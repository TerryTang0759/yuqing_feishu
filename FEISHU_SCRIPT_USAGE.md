# 飞书口播稿发送功能使用指南

## 📢 功能说明

可以将AI生成的口播稿文本和TTS音频文件发送到飞书群，方便团队成员查看和收听。

## 🎯 支持的方式

### 方式1: Webhook方式（简单，推荐）⭐

**特点：**
- ✅ 配置简单，只需webhook URL
- ✅ 可以发送口播稿文本
- ⚠️ 音频文件只能通过链接发送（需要配置base_url）

**配置：**
```yaml
# config/config.yaml
app:
  base_url: "https://your-username.github.io/TrendRadar"  # GitHub Pages地址

notification:
  webhooks:
    feishu_url: "https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx"
```

**效果：**
- 口播稿文本会添加到飞书消息中
- 音频文件会以链接形式发送（如果配置了base_url）

### 方式2: 飞书开放平台API（完整功能）⭐⭐⭐

**特点：**
- ✅ 可以发送口播稿文本
- ✅ 可以直接发送音频文件（无需外部链接）
- ⚠️ 需要创建飞书应用并配置权限

**配置步骤：**

1. **创建飞书应用**
   - 访问 https://open.feishu.cn/
   - 创建企业自建应用
   - 获取 `App ID` 和 `App Secret`

2. **配置应用权限**
   - 需要以下权限：
     - `im:message` - 发送消息
     - `drive:drive` - 上传文件

3. **获取群聊ID**
   - 在飞书群聊中，点击群设置 → 群信息 → 查看群ID

4. **配置环境变量或GitHub Secrets**
   ```bash
   # 环境变量
   export FEISHU_APP_ID="your_app_id"
   export FEISHU_APP_SECRET="your_app_secret"
   export FEISHU_CHAT_ID="your_chat_id"
   ```

   **GitHub Actions配置：**
   - 在仓库 Settings → Secrets 中添加：
     - `FEISHU_APP_ID`
     - `FEISHU_APP_SECRET`
     - `FEISHU_CHAT_ID`

5. **修改代码启用API方式**
   
   在 `main.py` 的 `send_to_webhooks` 函数中，取消注释API配置部分：
   ```python
   feishu_config = {
       "feishu_webhook_url": feishu_url,
       "base_url": CONFIG.get("BASE_URL", ""),
       "proxy_url": proxy_url,
       "feishu_app_id": os.environ.get("FEISHU_APP_ID", ""),
       "feishu_app_secret": os.environ.get("FEISHU_APP_SECRET", ""),
       "feishu_chat_id": os.environ.get("FEISHU_CHAT_ID", ""),
   }
   ```

## 🚀 使用方法

### 自动发送（推荐）

配置完成后，运行主程序，口播稿会自动发送：

```bash
python3 main.py
```

**发送流程：**
1. 生成口播稿文本 → 添加到飞书消息中
2. 生成TTS音频 → 通过链接或API发送

### 手动发送

```python
from feishu_script_sender import send_script_to_feishu

config = {
    "feishu_webhook_url": "your_webhook_url",
    "base_url": "https://your-username.github.io/TrendRadar",
}

send_script_to_feishu(
    "output/2026年01月17日/script/口播稿.txt",
    "output/2026年01月17日/script/口播稿.mp3",
    config
)
```

## 📊 消息格式

### Webhook方式

```
📊 热点词汇统计
...

━━━━━━━━━━━━━━━━━━━

📢 AI生成口播稿

晚上好，今天是2026年01月17日...

🎵 音频文件: [点击收听](https://your-url/口播稿.mp3)
```

### API方式

```
📢 AI生成口播稿

晚上好，今天是2026年01月17日...

[音频文件附件]
```

## ⚙️ 配置说明

### config.yaml

```yaml
app:
  base_url: "https://your-username.github.io/TrendRadar"  # 用于生成音频链接

notification:
  webhooks:
    feishu_url: "your_webhook_url"  # 飞书webhook URL
```

### 环境变量（API方式）

```bash
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_CHAT_ID=your_chat_id
```

## 🔍 故障排查

### 问题1: 口播稿文本未发送

**检查：**
1. ✅ 是否生成了口播稿文件
2. ✅ 飞书webhook URL是否正确
3. ✅ 查看程序日志

### 问题2: 音频文件链接无法访问

**检查：**
1. ✅ `base_url` 是否配置正确
2. ✅ 音频文件是否已提交到仓库（GitHub Actions）
3. ✅ GitHub Pages是否已启用

### 问题3: API方式发送失败

**检查：**
1. ✅ App ID和Secret是否正确
2. ✅ 应用权限是否配置完整
3. ✅ 群聊ID是否正确
4. ✅ 查看API返回的错误信息

## 📝 注意事项

1. **消息长度限制**
   - 飞书消息有长度限制，口播稿文本如果超过2000字会被截断
   - 建议保持口播稿在合理长度

2. **音频文件大小**
   - 飞书API上传文件有大小限制（通常20MB）
   - 1300字口播稿约1.6MB，在限制内

3. **GitHub Actions部署**
   - 如果使用GitHub Actions，需要确保：
     - 音频文件已提交到仓库
     - GitHub Pages已启用
     - base_url配置正确

4. **隐私和安全**
   - ⚠️ 不要将webhook URL或API凭证提交到公开仓库
   - 使用GitHub Secrets存储敏感信息

## 🎯 推荐配置

### 简单场景（Webhook + 链接）

```yaml
app:
  base_url: "https://your-username.github.io/TrendRadar"

notification:
  webhooks:
    feishu_url: "your_webhook_url"
```

### 完整功能（API方式）

```bash
# 环境变量
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
FEISHU_CHAT_ID=your_chat_id
```

---

**最后更新**: 2026-01-17  
**版本**: v2.5.0 + 飞书口播稿发送
