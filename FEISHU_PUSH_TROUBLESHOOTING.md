# 飞书推送故障排查

## 定时任务未触发

若 Actions 里只有手动 run，没有定时运行记录：

1. **Fork 仓库默认关闭定时任务**
   - Settings → Actions → General → 确认 Actions 已启用
   - 若有「Allow scheduled workflows」选项，勾选并保存

2. **重新启用 Workflow**
   - Actions → Hot News Crawler → 若显示「disabled」→ 点 Enable workflow

3. **确认在默认分支**
   - 定时任务只跑 `main` 分支上的 workflow
   - 确认 `.github/workflows/crawler.yml` 在 `main` 且已推送

4. **重新推送 workflow**
   ```bash
   git add .github/workflows/crawler.yml
   git commit -m "chore: re-register schedule"
   git push origin main
   ```

5. **60 天无活动**
   - 公开仓库 60 天无 commit 时 GitHub 会自动关闭定时触发
   - 出现「disabled due to inactivity」→ 点 Enable workflow

---

## 飞书收不到消息

1. **检查 Secrets 配置**
   - Settings → Secrets and variables → Actions
   - 确认有 `FEISHU_WEBHOOK_URL`（值为飞书 Webhook 地址）

2. **查看 Actions 日志**
   - Actions → 点进某次 run → Run crawler 步骤
   - 正常：`飞书通知发送成功 [当日汇总]`
   - 异常：`未配置任何webhook URL` 或 `飞书通知发送失败`

3. **口播稿未包含在消息中**
   - 日志有 `⚠️ AI API密钥未配置` → 在 Secrets 中添加 `AI_API_KEY`
   - 日志有 `⚠️ 当天口播稿文件不存在` → AI 调用失败，无口播稿可发
   - 日志有 `📢 口播稿将包含在飞书消息中` → 口播稿正常

---

## 口播稿生成失败

1. 确认 `AI_API_KEY` 已在 GitHub Secrets 中配置（不是 `DEEPSEEK_API_KEY`）
2. 确认 API 余额充足
3. 查看日志中的具体错误信息
