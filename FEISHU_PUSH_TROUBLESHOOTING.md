# 飞书自动推送未收到 — 排查指南

## ⚠️ 情况：只有手动 run，没有定时（schedule）run

若 Actions 里 **「Hot News Crawler」** 只有 **手动触发** 的记录，**没有任何 8:00 / 12:00 / 21:00 的定时运行**，说明 **cron 定时任务没有触发**，所以飞书不会自动推送。

**按下面「定时任务未触发」的步骤逐项检查。**

---

## 🔧 定时任务未触发 — 处理步骤

### 1. 若仓库是 Fork

**Fork 仓库默认关闭定时任务。**

1. 打开仓库 **Settings** → **Actions** → **General**
2. 在 **Actions permissions** 里选 **Allow all actions and reusable workflows**
3. 往下找到 **Fork pull request workflows from outside collaborators**，若存在则按需开启
4. **重要**：Fork 的 **Scheduled workflows** 可能被禁用，若有 **「Allow scheduled workflows」** 或类似选项，请勾选并保存

### 2. 重新启用 Workflow

1. 打开 **Actions** → 左侧 **Hot News Crawler**
2. 若出现 **「This workflow was disabled manually」** 或 **「This workflow was disabled for scheduled triggers」**，点击 **Enable workflow** 或 **Enable scheduled workflows**

### 3. 确认 Workflow 在默认分支

- 定时任务只跑 **默认分支**（通常是 `main`）上的 workflow
- 确认 `.github/workflows/crawler.yml` 在 **main** 且已推送

### 4. 重新推送 workflow 文件（重新注册定时）

有时需要重新推送一次 workflow 才能正确注册 schedule：

```bash
cd yuqing-TrendRadar
git add .github/workflows/crawler.yml
git commit -m "chore: 重新推送 workflow 以注册 schedule"
git push origin main
```

### 5. 等待下一次整点

- 定时可能有 **5–15 分钟** 延迟
- 推送后至少等 **下一个整点**（8:00 / 12:00 / 21:00 北京时间）再查看 Actions 是否出现 **schedule** 触发的 run

### 6. 检查仓库是否长期无活动

- 公开仓库 **60 天无 commit** 时，GitHub 可能 **自动关闭** 该 workflow 的定时触发
- 若有 **「Workflow was disabled due to inactivity」**，点 **Enable workflow** 重新开启

---

## 一、先做这两步（最常见）

### 1. 确认 GitHub Actions 是否运行

1. 打开：https://github.com/TerryTang0759/yuqing_feishu/actions  
2. 点左侧 **「Hot News Crawler」**  
3. 看 **今天** 是否有运行记录（8:00、12:00、21:00 北京时间）

**若今天没有任何运行：**

- 检查 workflow 是否被关掉：列表里该 workflow 旁有没有 **「This workflow was disabled manually」** → 点 **「Enable workflow」** 重新开启  
- 定时可能延迟：GitHub 计划任务常有 5–15 分钟延迟，接近整点再等一下  
- 确认 `crawler.yml` 已在 **main 分支** 并已推送（Schedule 只认默认分支）

---

### 2. 确认 GitHub Secrets 已配置

**路径：** 仓库 → **Settings** → **Secrets and variables** → **Actions**

必须有的 Secret：

| 名称 | 说明 | 未配置时表现 |
|------|------|--------------|
| `FEISHU_WEBHOOK_URL` | 飞书 Webhook 地址 | 无飞书推送（可能用 config 兜底，见下） |
| `AI_API_KEY` | DeepSeek 等 API 密钥 | 口播稿生成失败，但推送仍可发 |

**重要：**  
- 若 **没配** `FEISHU_WEBHOOK_URL`，且 **config 里也没有** `feishu_url`，则不会发飞书，日志里会出现 **「未配置任何 webhook URL」**。  
- 若 config 里写了 `feishu_url`，Actions 会用它，但官方建议 **一律用 Secrets**，不要写在 config 里。

请对照 [GITHUB_SECRETS_SETUP.md](./GITHUB_SECRETS_SETUP.md) 把 **FEISHU_WEBHOOK_URL** 和 **AI_API_KEY** 都配好。

---

## 二、看 Actions 运行日志

在 **Actions** → 点进 **某次今天的 run** → 看 **Run crawler** 这一步的日志。

### 正常情况会看到类似：

```
Webhook 配置来源: 飞书(环境变量) 或 飞书(配置文件)
通知功能已启用，将发送webhook通知
...
飞书通知发送成功 [当日汇总]
```

### 若未收到推送，重点查这几类输出：

| 日志内容 | 含义 | 处理办法 |
|----------|------|----------|
| `未配置任何 webhook URL` | 没用飞书 | 配好 `FEISHU_WEBHOOK_URL`（或 config 里 `feishu_url`） |
| `通知功能已禁用` | 关掉了通知 | 在 `config/config.yaml` 里设 `enable_notification: true` |
| `跳过...通知：未匹配到有效的新闻内容` | 当天没匹配到关键词 | 查 `config/frequency_words.txt`，或放宽词条 |
| `静默模式：当前时间不在推送时间范围内` | 开了静默推送且不在时间窗内 | 你当前 `silent_push.enabled: false`，可忽略 |
| `静默模式：今天已推送过，跳过本次推送` | 静默模式且当天已推过 | 同上，你未开静默模式，可忽略 |
| `AI API密钥未配置` | 没配 `AI_API_KEY` | 口播稿会失败，但**推送仍可发**；建议补配 |
| 红色报错、`ModuleNotFoundError`、`exit 1` 等 | 依赖或运行出错 | 根据报错修代码或 `requirements.txt` |

若 **Run crawler** 整步失败（红叉），则不会执行推送，需要先修运行错误。

---

## 三、当前定时与推送逻辑（简要）

- **定时：** 每天 **8:00、12:00、21:00** 北京时间（对应 UTC 0:00、4:00、13:00）  
- **模式：** `report.mode: daily` → 跑 **当日汇总**，汇总完成后 **发一次飞书**  
- **静默推送：** `silent_push.enabled: false` → 不限制时间窗、不限制「每天只推一次」，每次跑完汇总就会推  
- **Webhook 来源：** 优先用 **Secrets** 里的 `FEISHU_WEBHOOK_URL`，没有再用 **config** 里的 `feishu_url`

---

## 四、建议自检清单

- [ ] Actions 里 **「Hot News Crawler」** 今天有 run，且 **未被 disable**  
- [ ] `FEISHU_WEBHOOK_URL` 已在 **Secrets** 中配置（或 config 里 `feishu_url` 正确）  
- [ ] `config/config.yaml` 里 `enable_notification: true`  
- [ ] `config/frequency_words.txt` 非空，且能匹配到当天新闻  
- [ ] 飞书机器人 Webhook 未过期、未被禁用  
- [ ] 若用 **API 发送**：飞书应用权限、群组等配置正确（你当前是 Webhook，一般不用管）

---

## 五、快速验证：手动触发一次

1. 打开：https://github.com/TerryTang0759/yuqing_feishu/actions  
2. 选 **「Hot News Crawler」**  
3. 点 **「Run workflow」** → **「Run workflow」**  
4. 等跑完，看 **Run crawler** 日志里是否有 **「飞书通知发送成功」**  
5. 同时看飞书群是否收到推送  

若 **手动 run 能收到**，而 **定时 run 收不到**，多半是 **定时没跑**（见第一节）或 **跑错分支**。

---

## 六、仍然收不到时

把以下信息整理出来，便于进一步排查：

1. **今天是否有 run：** 有 / 没有；若有，大致时间（北京时间）  
2. **Run crawler 是否成功：** 绿色勾 / 红色叉  
3. **该步完整日志**（尤其含 `Webhook`、`通知`、`飞书`、`跳过`、`Error` 的行）  
4. **Secrets 配置情况：** 已配置 `FEISHU_WEBHOOK_URL` 和 `AI_API_KEY` 是 / 否  

有了上述信息，可以更精确判断是 **未运行**、**未配置**、**过滤掉** 还是 **飞书侧** 的问题。

---

**最后更新：** 2026-01-24
