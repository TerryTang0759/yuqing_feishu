# GitHub Secrets 配置指南

## 📋 需要在 GitHub 仓库中配置的 Secrets

### 配置位置
GitHub 仓库 → Settings → Secrets and variables → Actions → New repository secret

---

## ✅ 必需配置的 Secrets

### 1. FEISHU_WEBHOOK_URL
- **名称**: `FEISHU_WEBHOOK_URL`
- **说明**: 飞书机器人的 Webhook 地址
- **获取方式**: 
  1. 打开 https://botbuilder.feishu.cn/home/my-app
  2. 创建机器人应用
  3. 配置 Webhook 触发器
  4. 复制 Webhook 地址
- **示例**: `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
- **用途**: 用于发送热点新闻推送通知到飞书群

---

### 2. AI_API_KEY
- **名称**: `AI_API_KEY`
- **说明**: AI API 密钥，用于生成口播稿
- **获取方式**: 
  - DeepSeek: https://platform.deepseek.com/api_keys
  - OpenAI: https://platform.openai.com/api-keys
  - 其他平台: 参考对应平台的API密钥获取方式
- **示例**: `sk-d704972fa49f4acfb83eaf9b1ad8e482`
- **用途**: 调用AI API生成财经新闻口播稿

---

## 🔧 可选配置的 Secrets

> **注意**: 如果未设置以下可选Secrets，系统将使用 `config/config.yaml` 中的默认值

### 3. AI_API_TYPE
- **名称**: `AI_API_TYPE`
- **说明**: AI API 类型
- **可选值**: 
  - `deepseek` (默认)
  - `openai`
  - `claude`
  - `custom`
- **默认值**: `deepseek` (如果未设置，使用 config.yaml 中的值)
- **用途**: 指定使用的AI服务提供商

---

### 4. AI_MODEL
- **名称**: `AI_MODEL`
- **说明**: AI 模型名称
- **可选值** (根据 API_TYPE 不同):
  - DeepSeek: `deepseek-chat` (默认)
  - OpenAI: `gpt-4`, `gpt-3.5-turbo` 等
  - Claude: `claude-3-opus`, `claude-3-sonnet` 等
- **默认值**: `deepseek-chat` (如果未设置，使用 config.yaml 中的值)
- **用途**: 指定使用的AI模型

---

## 📝 配置步骤

### 步骤 1: 进入 Secrets 配置页面
1. 打开 GitHub 仓库: https://github.com/TerryTang0759/yuqing_feishu
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Secrets and variables** → **Actions**
4. 点击 **New repository secret**

### 步骤 2: 添加每个 Secret
对于每个需要配置的 Secret：
1. **Name** (名称): 输入 Secret 的名称（如 `FEISHU_WEBHOOK_URL`）
2. **Secret** (值): 输入对应的值
3. 点击 **Add secret**

### 步骤 3: 验证配置
配置完成后，可以在 Actions 页面手动触发一次 workflow 来验证配置是否正确。

---

## 🔍 配置检查清单

- [ ] `FEISHU_WEBHOOK_URL` - 飞书 webhook 地址
- [ ] `AI_API_KEY` - AI API 密钥
- [ ] `AI_API_TYPE` - API 类型（可选，默认 deepseek）
- [ ] `AI_MODEL` - 模型名称（可选，默认 deepseek-chat）

---

## ⚠️ 重要提示

1. **安全性**: Secrets 中的值不会在日志中显示，请妥善保管
2. **更新**: 如需更新 Secret，可以点击对应 Secret 进行编辑
3. **删除**: 删除 Secret 后，GitHub Actions 将无法使用该值
4. **默认值**: 如果可选 Secrets 未设置，系统会使用 `config/config.yaml` 中的配置

---

## 🧪 测试配置

配置完成后，可以通过以下方式测试：

1. **手动触发**: 在 Actions 页面点击 "Run workflow" 手动触发
2. **查看日志**: 在 Actions 运行日志中查看是否有错误
3. **检查推送**: 确认飞书群是否收到推送消息

---

## 📞 问题排查

如果推送失败，请检查：

1. ✅ Secrets 是否已正确配置
2. ✅ Webhook 地址是否正确
3. ✅ AI API 密钥是否有效且有余额
4. ✅ GitHub Actions 是否有运行权限
5. ✅ 查看 Actions 运行日志中的错误信息

---

**最后更新**: 2026年01月24日
