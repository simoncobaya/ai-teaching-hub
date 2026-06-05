# 🌟 方式一：用 CC Switch 配置（推荐！）

> CC Switch 是一个图形界面工具，帮你一键配置 Claude Code + DeepSeek。**最简单的方式！**

---

## 🎯 目标

用 CC Switch 图形界面，完成 Claude Code + DeepSeek 的配置。

---

## 📋 你需要准备

- [ ] ✅ DeepSeek API Key（[如何获取](../01-deepseek/register.md)）
- [ ] ✅ Claude Code 已安装（[如何安装](../02-claude-code/install.md)）

---

## 🚀 配置步骤

### Step 1：安装 CC Switch

如果你还没有安装 CC Switch，请先看 [CC Switch 安装教程](../04-cc-switch/install.md)。

安装完成后打开 CC Switch。

---

### Step 2：添加 DeepSeek 供应商

👉 **[详细图文教程：添加 API 供应商](../04-cc-switch/add-provider.md)**

跟着上面的教程操作，完成以下事项：

- ✅ 在 CC Switch 中添加 DeepSeek 供应商
- ✅ 填入你的 API Key
- ✅ 配置高级选项（1M 上下文、最大强度思考）
- ✅ 测试连接成功
- ✅ 配置用量查询
- ✅ 启用 DeepSeek

---

### Step 3：验证配置

1. 打开终端
2. 启动 Claude Code：
   ```bash
   claude
   ```
3. 在 Claude Code 中输入：
   ```
   你好！请用一句话介绍你自己。
   ```
4. 如果 AI 正常回复，说明配置成功！🎉

---

## 🎉 完成！

恭喜你！你已经用 CC Switch 完成了配置！

现在你可以：
- 直接用 Claude Code 对话，背后用的是 DeepSeek
- 在 CC Switch 中一键切换供应商（DeepSeek ↔ Claude 等）
- 在 Claude Code 中用 `/model sonnet`、`/model opus`、`/model haiku` 切换模型层级

---

## 📌 下一步

👉 **[验证配置是否成功](./verify.md)** — 确认一切正常

👉 **[实践：让 AI 帮你写个猜数字游戏 🎮](./first-project.md)** — 马上试试！

---

<details>
<summary>🔧 不想用 CC Switch？试试其他方式</summary>

如果你不想用 CC Switch，或者 CC Switch 不适合你，还有手动配置方式：

- **[方式二：手动配置](./method-env.md)** — 编辑 settings.json 或设置环境变量

</details>
