# 📚 AI 编程工具全家桶教程

> 把 AI 工具变成你的编程好帮手！

---

## 🌟 这套教程教什么？

你有没有想过，让 AI 帮你写代码？

想象一下：
- 你说"帮我写一个猜数字游戏"，AI 就真的帮你写出来了 🎮
- 你说"这个程序有个 bug，帮我找找"，AI 就帮你找到问题并修好 🐛
- 你说"帮我把这个网页做得更好看"，AI 就帮你优化代码 🎨

这套教程就是教你 **怎么用 AI 工具来帮你编程**！

---

## 📖 教程目录

### 🌟 [开篇：走进 AI 编程世界](./00-introduction/README.md)
- [什么是 AI 编程工具？](./00-introduction/README.md)
- [为什么要学 AI 编程？](./00-introduction/why-learn.md)
- [AI 编程工具全景图](./00-introduction/tool-map.md)

### 🐋 [DeepSeek 入门](./01-deepseek/README.md)
- [DeepSeek 是什么？](./01-deepseek/README.md)
- [注册账号 + 获取 API Key](./01-deepseek/register.md)
- [在线体验 DeepSeek](./01-deepseek/playground.md)

### 🤖 [Claude Code 入门](./02-claude-code/README.md)
- [Claude Code 是什么？](./02-claude-code/README.md)
- [安装 Claude Code](./02-claude-code/install.md)
- [基础用法](./02-claude-code/basics.md)
- [实用小技巧](./02-claude-code/tips.md)

### ⭐ [核心：Claude Code + DeepSeek 配置](./03-deepseek-claudecode/README.md)
- [为什么用 DeepSeek + Claude Code？](./03-deepseek-claudecode/README.md)
- [方式一：用 CC Switch（最简单！推荐）](./03-deepseek-claudecode/method-ccswitch.md)
- [方式二：修改 settings.json](./03-deepseek-claudecode/method-settings.md)
- [方式三：设置环境变量](./03-deepseek-claudecode/method-env.md)
- [验证配置是否成功](./03-deepseek-claudecode/verify.md)
- [实践：让 AI 帮你写个猜数字游戏 🎮](./03-deepseek-claudecode/first-project.md)
- [常见问题解决](./03-deepseek-claudecode/troubleshooting.md)

### 🔧 [CC Switch 配置管理](./04-cc-switch/README.md)
- [CC Switch 是什么？](./04-cc-switch/README.md)
- [安装 CC Switch](./04-cc-switch/install.md)
- [添加 API 供应商](./04-cc-switch/add-provider.md)
- [一键切换模型](./04-cc-switch/switch-model.md)
- [管理多个工具](./04-cc-switch/manage-tools.md)
- [MCP 服务器管理](./04-cc-switch/mcp-management.md)

### 🧠 [智谱 GLM + ZCode](./05-glm-zcode/README.md)
- [智谱 Coding Plan 介绍](./05-glm-zcode/README.md)
- [订阅套餐](./05-glm-zcode/subscribe.md)
- [配置 Claude Code 使用 GLM](./05-glm-zcode/configure-claudecode.md)
- [配置 Cursor 使用 GLM](./05-glm-zcode/configure-cursor.md)
- [专属 MCP 服务器](./05-glm-zcode/mcp-servers.md)
- [ZCode 编程工具简介](./05-glm-zcode/zcode-intro.md)

### 🖥️ [Cursor IDE](./06-cursor/README.md)
- [Cursor 是什么？](./06-cursor/README.md)
- [下载安装](./06-cursor/install.md)
- [基础用法](./06-cursor/basics.md)
- [配置 DeepSeek 模型](./06-cursor/configure-deepseek.md)

### 🤖 [OpenAI Codex](./07-codex/README.md)
- [Codex 是什么？](./07-codex/README.md)
- [Codex 桌面版](./07-codex/desktop.md)
- [Codex CLI 安装](./07-codex/install.md)
- [Codex CLI 基础用法](./07-codex/basics.md)

### 🆓 [OpenCode](./08-opencode/README.md)
- [OpenCode 是什么？](./08-opencode/README.md)
- [安装](./08-opencode/install.md)
- [基础用法](./08-opencode/basics.md)
- [配置各种模型](./08-opencode/configure-models.md)

### 🎨 [TRAE IDE](./09-trae/README.md)
- [TRAE 是什么？](./09-trae/README.md)
- [下载安装](./09-trae/install.md)
- [基础用法](./09-trae/basics.md)

### 👯 [CodeBuddy](./10-codebuddy/README.md)
- [CodeBuddy 是什么？](./10-codebuddy/README.md)
- [安装](./10-codebuddy/install.md)
- [国内版 vs 国际版](./10-codebuddy/versions.md)

### 🟣 [Qoder](./11-qoder/README.md)
- [Qoder 是什么？](./11-qoder/README.md)
- [下载安装](./11-qoder/install.md)
- [国内版 vs 国际版](./11-qoder/versions.md)

### 📊 [工具对比与选择指南](./99-comparison/README.md)
- [全工具对比表](./99-comparison/README.md)
- [如何选择适合你的工具？](./99-comparison/choose-your-tool.md)
- [费用对比](./99-comparison/cost-comparison.md)
- [推荐工作流](./99-comparison/recommended-workflow.md)

---

## 🗺️ 学习路线

### 路线 A：零基础入门（推荐大多数同学！）

跟着这个路线，一步一个脚印 👇

```
Step 1 → 00-introduction/README         了解 AI 编程是什么
         └─ why-learn                   为什么要学 AI 编程？
         └─ tool-map                    看看有哪些工具

Step 2 → 00-introduction/install-nodejs  ✅ 安装 Node.js（很多工具都需要）

Step 3 → 01-deepseek/README             认识 DeepSeek
         └─ register                    注册 DeepSeek，拿到你的 API Key 🔑
         └─ playground                  在线体验 DeepSeek 的编程能力

Step 4 → 02-claude-code/README          认识 Claude Code
         └─ install                     安装 Claude Code 📥

Step 5 → 03-deepseek-claudecode/README  ⭐ 最重要的一步！
         └─ method-ccswitch             用 CC Switch 配置 DeepSeek（最简单）
         └─ verify                      检查配置是否成功
         └─ first-project               让 AI 帮你写第一个程序！🎮

Step 6 → 99-comparison/README           看看其他工具，按兴趣探索
         └─ choose-your-tool            根据你的情况选择更多工具
```

**预计时间**：2-3 小时（可以分几天完成）

**适合**：第一次接触 AI 编程工具的所有同学

---

### 路线 B：想免费体验

```
Step 1 → 08-opencode/README             认识 OpenCode（完全免费开源！）
         └─ install                     安装 OpenCode

Step 2 → 01-deepseek/register           注册 DeepSeek，充值 ¥10

Step 3 → 08-opencode/configure-models   把 OpenCode 配置用 DeepSeek 模型

Step 4 → 开始写代码！🎉
```

**预计时间**：1-2 小时

**适合**：想完全用免费/低成本方案的同学

---

### 路线 C：想要图形界面（IDE）

不喜欢黑黑的终端？试试有图形界面的编辑器 👇

```
Step 1 → 06-cursor/README               认识 Cursor（最流行的 AI 编辑器）
         └─ install                     下载安装 Cursor

Step 2 → 01-deepseek/register           注册 DeepSeek，拿到 API Key

Step 3 → 06-cursor/configure-deepseek   让 Cursor 使用便宜的 DeepSeek

Step 4 → 06-cursor/basics               学会 Cursor 基本操作
```

**预计时间**：1-2 小时

**适合**：喜欢图形界面、不想用命令行的同学

---

### 路线 D：我想全部搞清楚！

如果你想让 AI 帮你管理所有工具配置 👇

```
Step 1 → 完成路线 A 的 Step 1-4        打好基础

Step 2 → 04-cc-switch/README            认识 CC Switch 配置管理工具
         └─ install                     安装 CC Switch
         └─ add-provider                添加多个 AI 供应商
         └─ switch-model                一键切换模型
         └─ manage-tools                同时管理 Claude Code、Cursor 等

Step 3 → 05-glm-zcode/README            了解智谱 GLM（国内最强）
         └─ subscribe                   订阅适合的套餐

Step 4 → 按兴趣探索其他工具！
```

**预计时间**：3-5 小时

**适合**：想深入了解 AI 编程工具、参加竞赛的同学

---

> 💡 **不知道怎么选？** 大多数同学从 **路线 A** 开始就对了！学完路线 A，你就已经能用 AI 写程序了。其他路线可以以后按兴趣慢慢探索。

> 🌱 **千里之行，始于足下。** 跟着路线一步步走，你就能让 AI 帮你编程！

---

## 🎯 适合谁？

- **4-6 年级学生** — 想学编程，想让 AI 帮你写代码
- **编程初学者** — 刚开始学编程，想用 AI 工具帮助学习
- **竞赛选手** — 参加 AI 竞赛，需要掌握多种 AI 编程工具

---

## 💡 小贴士

> 🌟 **建议从哪里开始？**
>
> 如果你是第一次接触 AI 编程工具，建议从 **00-introduction** 开始，按顺序学习到 **03-deepseek-claudecode**。这是最核心的内容！
>
> 其他工具（Cursor、TRAE、Codex 等）可以按兴趣选择阅读。

---

## 🔗 有用的链接

### 🧠 AI 模型

| 名称 | 链接 |
|------|------|
| DeepSeek 官网 | https://www.deepseek.com/ |
| 智谱 🇨🇳 国内版 | https://bigmodel.cn/ |
| 智谱 🌍 国际版 | https://z.ai |

### 📟 终端工具（CLI）

| 名称 | 链接 |
|------|------|
| Claude Code 官网 | https://claude.com/product/claude-code |
| OpenAI Codex CLI | https://github.com/openai/codex |
| OpenCode 官网 | https://opencode.ai/ |
| TRAE CLI（企业版） | https://docs.trae.cn/cli |
| CodeBuddy CLI 🇨🇳 入口 | https://www.codebuddy.cn/cli/ |
| CodeBuddy CLI 🌍 入口 | https://www.codebuddy.ai/cli |
| Qoder CLI 🇨🇳 国内版 | https://qoder.com.cn/cli |
| Qoder CLI 🌍 国际版 | https://docs.qoder.com/en/cli/quick-start |

### 🖥️ IDE（编辑器）

| 名称 | 链接 |
|------|------|
| Cursor 下载 | https://cursor.com/download |
| OpenAI Codex 桌面版 | https://openai.com/codex/ |
| TRAE 下载 🇨🇳 国内版 | https://www.trae.cn/ide/download |
| TRAE 下载 🌍 国际版 | https://www.trae.ai/download |
| Qoder 🇨🇳 国内版 | https://qoder.com.cn/desktop |
| Qoder 🌍 国际版 | https://qoder.com/desktop |
| CodeBuddy 🇨🇳 国内版 | https://www.codebuddy.cn/ide |
| CodeBuddy 🌍 国际版 | https://www.codebuddy.ai/ide |

### 🔧 配置工具

| 名称 | 链接 |
|------|------|
| CC Switch 下载 | https://github.com/farion1231/cc-switch |
