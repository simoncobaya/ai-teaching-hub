# 🤖 OpenAI Codex

> OpenAI 出品的 AI 编程助手，有终端版和桌面版两种使用方式！

---

## 🤔 Codex 是什么？

Codex 是 OpenAI 推出的 **AI 编程产品**，能帮你写代码、修 bug、做重构、跑测试，甚至自动处理日常开发任务。它有两种使用方式：

| | 📟 Codex CLI | 🖥️ Codex 桌面版 |
|---|---|---|
| **在哪用** | 终端命令行 | 桌面应用（macOS / Windows） |
| **怎么用** | 输入命令 | 图形界面操作 |
| **需要安装** | ✅ 需要安装 | ✅ 下载安装包 |
| **认证方式** | ChatGPT 账号 ✅ / API Key ✅ | ChatGPT 账号 ✅ / API Key ✅ |
| **开源** | ✅ GitHub 开源免费 | ❌ 闭源 |
| **适合谁** | 喜欢终端、本地操作 | 想要图形界面、多线程并行 |

---

## 🖥️ Codex 桌面版

Codex 桌面版是 OpenAI 的 **桌面编程指挥中心**，功能更强大：

### 核心功能

| 功能 | 说明 |
|------|------|
| 🤖 **多 Agent 并行** | 多个 AI Agent 同时处理不同任务，效率翻倍 |
| 🛠️ **Skills（技能）** | 代码理解、原型设计、文档编写，适配团队规范 |
| ⚙️ **Automations（自动化）** | 自动处理 Issue 分类、告警监控、CI/CD |
| 🔍 **代码审查** | 自动进行设计评审、测试覆盖、高质量 Review |

### 使用方式

1. 打开 [openai.com/codex](https://openai.com/codex/) 下载安装
2. 用 ChatGPT 账号或 API Key 登录
3. 开始使用！

> 💡 桌面版包含在 ChatGPT Plus、Pro、Business、Edu 和 Enterprise 订阅中。

👉 **详细教程：[Codex 桌面版](./desktop.md)**

---

## 📟 Codex CLI

Codex CLI 是开源的 **终端编程工具**，轻量简单：

### 核心功能

- 💻 读写文件
- 🏃 运行命令
- 🔧 修改代码
- 🧪 运行测试

### Codex CLI 的特点

| 特点 | 说明 |
|------|------|
| 🆓 **开源免费** | 完全开源，免费安装和使用 |
| 🔒 **安全沙箱** | 在沙箱中运行，保护你的电脑 |
| 📁 **本地操作** | 直接操作本地文件 |
| 🤖 **默认模型** | 使用 OpenAI 编程模型（如 gpt-4.1-mini） |
| 🔌 **支持自定义** | 可以配置使用其他模型 |

### 安装命令

```bash
# 一键安装（macOS / Linux）推荐！
curl -fsSL https://chatgpt.com/codex/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://chatgpt.com/codex/install.ps1 | iex"

# npm 安装
npm install -g @openai/codex

# Homebrew（macOS）
brew install --cask codex
```

### 快速体验

```bash
# 启动交互模式
codex

# 直接给任务
codex "帮我创建一个 Python 的 hello world 程序"
```

👉 **详细教程：[安装 Codex CLI](./install.md) → [基础用法](./basics.md)**

---

## 🌟 怎么选？

```
你更喜欢哪种方式？

喜欢终端命令行？     →  📟 Codex CLI（开源免费，本地操作）
想要图形界面？       →  🖥️ Codex 桌面版（功能更强大）
两个都想试试？       →  都试试看！它们用同一个 ChatGPT 账号
```

---

## 🔗 相关链接

| 名称 | 链接 |
|------|------|
| Codex 官网（桌面版） | https://openai.com/codex/ |
| Codex CLI GitHub | https://github.com/openai/codex |
| Codex CLI 文档 | https://developers.openai.com/codex/cli |

---

## 📌 下一步

👉 **[Codex 桌面版教程](./desktop.md)** — 了解桌面版的详细功能

👉 **[安装 Codex CLI](./install.md)** — 在终端里用 Codex

👉 **[OpenCode 教程](../08-opencode/README.md)** — 免费开源的替代方案

👉 **[CC Switch 教程](../04-cc-switch/README.md)** — 用 CC Switch 管理 Codex 配置
