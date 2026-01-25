# GitHub Secrets 配置指南

## 📋 配置位置

**GitHub 仓库** → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

---

## ✅ 必需配置（2 个）

### 1. FEISHU_WEBHOOK_URL

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `FEISHU_WEBHOOK_URL` |
| **说明** | 飞书机器人 Webhook 地址 |
| **你当前使用的值** | `https://open.feishu.cn/open-apis/bot/v2/hook/90f6c3f0-7db8-4444-a32a-224147f77728` |
| **用途** | 推送热点新闻到飞书群 |

---

### 2. AI_API_KEY

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_API_KEY` |
| **说明** | DeepSeek API 密钥（用于生成口播稿） |
| **你当前使用的值** | `sk-d704972fa49f4acfb83eaf9b1ad8e482` |
| **用途** | 调用 AI 生成财经新闻口播稿 |

**⚠️ 名称必须为 `AI_API_KEY`，不能是 `DEEPSEEK_API_KEY`**。workflow 和脚本只读取 `AI_API_KEY`，填错会导致「AI API密钥未配置」。

---

## 🔧 可选配置（2 个）

> 未设置时使用 `config/config.yaml` 默认值

### 3. AI_API_TYPE

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_API_TYPE` |
| **说明** | API 类型 |
| **你当前使用的值** | `deepseek` |
| **可选值** | `deepseek` \| `openai` \| `claude` \| `custom` |

---

### 4. AI_MODEL

| 项目 | 值 |
|------|-----|
| **Secret 名称** | `AI_MODEL` |
| **说明** | 模型名称 |
| **你当前使用的值** | `deepseek-chat` |
| **可选值** | `deepseek-chat` \| `gpt-4` \| `gpt-3.5-turbo` 等 |

---

## 📝 配置步骤

1. 打开 https://github.com/TerryTang0759/yuqing_feishu
2. **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 按上表依次添加 4 个 Secret（名称 + 值）

---

## 🔍 检查清单

- [ ] `FEISHU_WEBHOOK_URL` = `https://open.feishu.cn/open-apis/bot/v2/hook/90f6c3f0-7db8-4444-a32a-224147f77728`
- [ ] `AI_API_KEY` = 你的 DeepSeek API 密钥（**不是** `DEEPSEEK_API_KEY`）
- [ ] `AI_API_TYPE` = `deepseek`（可选）
- [ ] `AI_MODEL` = `deepseek-chat`（可选）

### 常见错误

| 现象 | 原因 | 处理 |
|------|------|------|
| 日志里出现「AI API密钥未配置」 | 添加了 `DEEPSEEK_API_KEY` 而非 `AI_API_KEY` | 新建 Secret **`AI_API_KEY`**，值为你的 DeepSeek 密钥；可删除 `DEEPSEEK_API_KEY` |

---

## ⚠️ 安全提示

1. **勿将密钥写入代码或 config.yaml 并提交**，应使用 GitHub Secrets。
2. 若已在 config 中填写，建议删除后改为仅在 Secrets 中配置。
3. 本配置与当前本地/`.env` 使用一致，用于 Actions 定时推送（每天 8:00、12:00、21:00 北京时间）。

---

**最后更新**: 2026年01月24日
