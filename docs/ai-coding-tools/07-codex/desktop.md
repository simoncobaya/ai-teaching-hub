# 🖥️ Codex 桌面版（Codex App）

> OpenAI 的桌面编程指挥中心，macOS 和 Windows 都能用！

---

## 🤔 Codex 桌面版是什么？

Codex 桌面版（Codex App）是一个 **桌面应用程序**，提供图形界面来管理多个 AI Agent 并行工作。和 CLI 不同，你不需要在终端里敲命令，有完整的图形界面。

它支持多个 AI Agent 同时工作、自动化日常任务、Git 操作、内置浏览器等丰富功能。

---

## 📥 安装

Codex App 目前支持 **macOS** 和 **Windows**（Linux 尚未推出）。

| 平台 | 下载 |
|------|------|
| macOS Apple Silicon | [下载](https://openai.com/codex/) |
| macOS Intel | [下载](https://openai.com/codex/) |
| Windows | [下载](https://openai.com/codex/) |

---

## 🔑 登录认证

安装后打开，支持两种登录方式：

### 方式一：ChatGPT 账号登录（推荐 ✅）

用你的 ChatGPT 账号直接登录，功能最完整。

> 💡 需要以下任一订阅：Plus、Pro、Business、Edu、Enterprise

### 方式二：OpenAI API Key

也可以用 API Key 登录，但部分功能可能不可用。

---

## 🌟 核心功能

### 🤖 多任务并行

- 同时运行 **多个项目线程**，快速切换
- 每个 Agent 在自己的 **独立空间** 里工作，互不干扰
- 就像你可以同时打开好几本作业本写不同科目的作业 📚

```
想象一下：

Agent 1：帮你写新功能 ← 同时进行 → Agent 2：帮你修 bug
                                          ↓
Agent 3：帮你写文档                        互不干扰！
```

### 🌿 Worktrees（独立工作区）

- 每个任务有自己的独立工作区，不会互相影响
- 就像给每个作业准备一个单独的桌子 🪑

### 📱 Remote Connections（远程控制）

- 用 ChatGPT 手机 App 远程控制 Codex 的工作
- 就像用遥控器操控机器人 🤖

### 🖥️ Computer Use（电脑操控）

- 让 Codex 帮你操作电脑上的应用程序
- 就像有一个小助手帮你点鼠标和打字 🖱️

### 📸 Appshots（截图发送）

- 一键发送当前应用窗口截图给 Codex
- 就像拍照发给朋友看 👀

### 🔍 Review & Ship（审查与发布）

- 查看你改了什么代码
- 检查有没有问题
- 确认没问题就提交 🚀

### 💻 Terminal（终端）

- 每个线程都有独立的终端
- 可以启动可重复的项目操作

### 🌐 In-app Browser（内置浏览器）

- 打开渲染好的页面
- 留评论
- 让 Codex 操作本地浏览器流程

### 🧩 Chrome Extension（Chrome 插件）

- 添加 Chrome 插件后，Codex 可以使用 Chrome 执行需要登录的浏览器任务
- 你只需管理网站授权

### 🎨 Image Generation（图片生成）

- 在线程中生成或编辑图片
- 同时处理相关代码和资源

### ⚙️ Automations（自动化）

Codex 可以 **定时自动运行** 任务：

| 自动化任务 | 说明 |
|------|------|
| 📬 **定时任务** | 定期运行重复性工作 |
| 🔄 **持续检查** | 唤醒同一线程进行持续检查 |
| ✅ **批量处理** | 自动处理 Issue、PR 审查等 |

### 🛠️ Skills（技能系统）

- 在 App、CLI 和 IDE Extension 之间 **共享技能**
- 可复用的指令和工作流

### 📎 Sidebar & Artifacts（侧边栏）

- 跟踪计划、来源、任务摘要
- 预览生成的文件

### 🔌 Plugins（插件）

- 连接应用、技能和 MCP 服务器
- 扩展 Codex 的能力

### 🌍 Sites（网站部署）

- 构建和部署托管网站、Web 应用和游戏

### 🔗 IDE Extension Sync（IDE 同步）

- App 和 IDE 之间共享 Auto Context 和活动线程

---

## 🚀 怎么用？

### Step 1：下载安装

从官网下载对应平台的安装包 👉 **[openai.com/codex](https://openai.com/codex/)**

### Step 2：登录

用 **ChatGPT 账号** 或 **OpenAI API Key** 登录。

### Step 3：选择项目

选择一个项目文件夹让 Codex 工作在。

> 💡 如果之前用过 Codex App、CLI 或 IDE Extension，会自动显示过去的项目。

### Step 4：开始使用

确保选择了 **Local**（本地模式），然后发送你的第一条消息：

- 🧠 "介绍一下这个项目"
- 🎮 "帮我写一个贪吃蛇游戏"
- 🐛 "找出并修复代码中的 bug"

---

## 🆚 桌面版 vs CLI

| 对比项 | 🖥️ 桌面版（App） | 📟 CLI |
|--------|-------------------|--------|
| **界面** | 图形界面（GUI） | 终端命令行（TUI） |
| **平台** | macOS、Windows | macOS、Windows、Linux |
| **安装** | 下载安装包 | curl / npm / brew |
| **认证** | ChatGPT 账号 ✅ / API Key ✅ | ChatGPT 账号 ✅ / API Key ✅ |
| **运行位置** | 本地 + 云端 | 本地 |
| **多任务** | ✅ 多线程并行 | ✅ 多 Agent（subagents） |
| **自动化** | ✅ 定时任务 | ✅ codex exec（脚本） |
| **内置浏览器** | ✅ | ❌ |
| **Computer Use** | ✅ 操控 GUI 应用 | ❌ |
| **Git Worktree** | ✅ 内置 | ❌ |
| **费用** | ChatGPT 订阅（含额度） | ChatGPT 订阅或 API 按量计费 |
| **开源** | ❌ | ✅ |

---

## 💡 使用建议

```
什么时候用桌面版？
✅ 需要同时处理多个项目
✅ 想要图形界面操作
✅ 需要定时自动运行任务
✅ 想用浏览器和 Computer Use
✅ 需要 Git Worktree 隔离

什么时候用 CLI？
✅ 喜欢在终端工作
✅ 需要 CI/CD 自动化集成
✅ 需要 JSON 输出做管道处理
✅ 在 Linux 上工作
✅ 快速的单次任务
```

---

## 🔗 相关链接

| 名称 | 链接 |
|------|------|
| Codex App 官方文档 | https://developers.openai.com/codex/app |
| Codex App 功能介绍 | https://developers.openai.com/codex/app/features |
| Codex App 下载 | https://openai.com/codex/ |
| Codex CLI | https://github.com/openai/codex |

---

## 📌 下一步

👉 **[Codex CLI 安装](./install.md)** — 试试终端版

👉 **[Codex CLI 基础用法](./basics.md)** — 学习 CLI 的使用方式

👉 **[工具对比](../99-comparison/README.md)** — 和其他工具对比
