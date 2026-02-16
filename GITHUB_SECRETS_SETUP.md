# GitHub Secrets 配置指南

## 配置位置

**GitHub 仓库** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

---

## 必需配置（2 个）

### 1. FEISHU_WEBHOOK_URL

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `FEISHU_WEBHOOK_URL` |
| **说明** | 飞书机器人 Webhook 地址 |
| **格式** | `https://open.feishu.cn/open-apis/bot/v2/hook/xxxxx` |

---

### 2. AI_API_KEY

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_API_KEY` |
| **说明** | DeepSeek API 密钥（用于生成 AI 口播稿） |
| **格式** | `sk-xxxxxxxxxxxxxxxx` |

**名称必须为 `AI_API_KEY`，不能是 `DEEPSEEK_API_KEY`。** workflow 和脚本只读取 `AI_API_KEY`，填错名称会导致「AI API密钥未配置」。

---

## 可选配置（2 个）

> 未设置时使用 `config/config.yaml` 中的默认值。

### 3. AI_API_TYPE

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_API_TYPE` |
| **默认值** | `deepseek` |
| **可选值** | `deepseek` / `openai` / `claude` / `custom` |

### 4. AI_MODEL

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_MODEL` |
| **默认值** | `deepseek-chat` |
| **可选值** | `deepseek-chat` / `gpt-4` / `gpt-3.5-turbo` 等 |

---

## 配置步骤

1. 打开仓库 **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 依次添加上述 Secret（名称 + 值）

---

## 检查清单

- [ ] `FEISHU_WEBHOOK_URL` — 飞书 Webhook 地址
- [ ] `AI_API_KEY` — DeepSeek API 密钥（**不是** `DEEPSEEK_API_KEY`）
- [ ] `AI_API_TYPE` — `deepseek`（可选）
- [ ] `AI_MODEL` — `deepseek-chat`（可选）

---

## 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| 日志「AI API密钥未配置」 | Secret 名称写成 `DEEPSEEK_API_KEY` | 新建 `AI_API_KEY`，值为你的密钥 |
| 飞书未收到推送 | `FEISHU_WEBHOOK_URL` 未配置 | 在 Secrets 中添加飞书 Webhook 地址 |
| 口播稿未包含在飞书消息中 | AI API 调用失败 | 检查 `AI_API_KEY` 是否正确 |

---

## 安全提示

1. **勿将密钥写入代码或 config.yaml 并提交**，应使用 GitHub Secrets 或 `.env` 文件
2. `.env` 文件已在 `.gitignore` 中，不会被提交
3. 定时推送：每天 8:00、12:00、21:00（北京时间）
