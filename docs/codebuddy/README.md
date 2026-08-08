# CodeBuddy（腾讯云代码助手）

> CodeBuddy 全称 Tencent Cloud CodeBuddy（腾讯云代码助手），是腾讯云推出的 AI 编程工具，定位为"AI 时代的智能编程伙伴"。2024 年 5 月 22 日正式对外开放。

---

## 三种产品形态

CodeBuddy 提供三种产品形态，是国内首家实现"插件 + IDE + CLI"全形态覆盖的 AI 编程工具：

| 形态 | 说明 | 面向用户 | 关键节点 |
|------|------|----------|----------|
| **插件** | 安装到 VS Code / JetBrains / 微信开发者工具中使用 | 日常编码开发者 | 2024-05-22 正式开放 |
| **IDE（独立编辑器）** | 基于 Eclipse Theia 深度定制的独立 AI 代码编辑器 | 产品、设计师、全栈开发 | 2025-07-22 内测，2025-08-21 公测 |
| **CLI（CodeBuddy Code）** | 在终端中使用的 AI 命令行工具 | DevOps、运维、资深开发者 | 2025-09-09 发布 |

> ⚠️ **CodeBuddy IDE 是独立的桌面应用程序**，不是 VS Code 插件。插件安装在已有 IDE 中，而 IDE 是完全独立的编辑器，支持从 VS Code / Cursor 导入设置。

---

## 各形态功能对比

| 功能 | CodeBuddy IDE | 插件（VS Code / JetBrains / 微信开发者工具） | CLI |
|------|:---:|:---:|:---:|
| Ask 对话模式 | ✅ | ✅ | — |
| Craft 模式 | ✅ | ✅ | ✅ |
| Plan 计划模式 | ✅ | ❌ | ✅（2.0 起） |
| Figma 设计稿转代码 | ✅ | ❌ | — |
| 组件库（TDesign / MUI / Shadcn） | ✅ | ❌ | — |
| 后端集成（Supabase / CloudBase） | ✅ | ❌ | — |
| 云端部署（CloudStudio / EdgeOne Pages） | ✅ | ❌ | — |
| MCP 协议 | ✅ | ✅ | ✅ |

---

## IDE 交互模式

CodeBuddy IDE 提供三种对话模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **Ask（问答模式）** | 类似聊天机器人，专注技术问答，不直接修改代码 | 快速获取思路、查阅 API |
| **Craft（自主执行模式）** | AI 深度理解需求，**独立完成多文件代码编写与修改** | 从自然语言需求到生成完整应用 |
| **Plan（计划模式）** | Craft 先拆解任务、制定计划并澄清需求，确认后自主执行 | 跨文件修改、复杂功能开发 |

> 💡 **Plan 模式仅 CodeBuddy IDE 和 CLI 支持**，VS Code / JetBrains 插件仅支持 Ask 和 Craft。

---

## 核心功能

| 功能 | 说明 |
|------|------|
| **代码补全** | 多行智能补全，按 `Tab` 接受建议 |
| **NES（补全 Pro）** | Next Edit Suggestions，不仅补全当前行，还预测下一步编辑意图；按 `Tab` 接受，`Esc` 取消 |
| **Figma 转代码** | 内置 Figma，将设计稿转换为可维护的前端代码（TDesign / MUI / Shadcn 组件库） |
| **后端集成** | 内置 Supabase、Tencent CloudBase，自动处理数据库和认证 |
| **一键部署** | 部署至 CloudStudio / EdgeOne Pages，生成可分享链接 |
| **MCP 协议** | 中国首个支持 MCP（Model Context Protocol）的编程助手（2025-05） |
| **Skills** | CLI 2.0 引入，中国首款支持 Skills 的 AI 编程工具 |
| **Boost Prompt** | 将模糊 Prompt 自动优化，在 Chat / Craft 模式中可用 |
| **`@` 上下文** | 添加文件、知识库等作为对话上下文 |
| **`/` 快捷指令** | 调用预置或自定义指令 |

---

## 国内版与国际版

CodeBuddy 有两个独立的官网和账号体系：

| 版本 | 官网 | 文档站 | CLI 登录地址 |
|------|------|--------|-------------|
| **国内版** | https://www.codebuddy.cn/ | https://www.codebuddy.cn/docs | copilot.tencent.com（微信扫码） |
| **国际版** | https://www.codebuddy.ai/ | https://www.codebuddy.ai/docs | codebuddy.ai（Google / GitHub） |

> CLI 是**同一工具**，安装后在登录时选择站点（Chinese Site / International Site / Enterprise Domain）。IDE 则从对应官网下载。

详见 **[国内版 vs 国际版](./versions.md)**。

---

## 安装

| 形态 | 安装方式 |
|------|---------|
| **IDE** | 从官网下载独立安装包：<https://www.codebuddy.cn/ide> 或 <https://www.codebuddy.ai/ide> |
| **插件** | IDE 插件市场搜索 **"CodeBuddy"**（VS Code / JetBrains / 微信开发者工具） |
| **CLI** | `npm install -g @tencent-ai/codebuddy-code`（Node.js 18.0+） |

> 详细安装指南见 **[安装文档](./install.md)**

---

## IDE 快捷键

| 操作 | macOS | Windows |
|------|-------|---------|
| 内联对话 | `⌘ + I` | `Ctrl + I` |
| 侧边栏对话 | `Ctrl + ⌘ + I` | `Ctrl + Win + I` |
| 接受补全 / NES 建议 | `Tab` | `Tab` |
| 取消 NES 建议 | `Esc` | `Esc` |
| 命令面板 | `⌘ + Shift + P` | `Ctrl + Shift + P` |

---

## 下一步

- **[安装 CodeBuddy](./install.md)** — IDE / 插件 / CLI 详细安装指南
- **[国内版 vs 国际版](./versions.md)** — 两个版本的详细对比
