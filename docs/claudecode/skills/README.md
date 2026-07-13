# 🧩 Claude Code 官方 Skills 市场

> Claude Code 有 228 个官方插件，覆盖开发、数据库、安全、设计等 12 个领域。这里整理了全部列表和使用指南。

---

## 🤔 什么是 Plugin？

Plugin（插件）是 Claude Code 的"扩展包"。安装后，AI 获得新的能力。一个 Plugin 可以包含以下几种组件：

### 六种组件类型

| 组件 | 有 Slash？ | 谁调用？ | 本质 |
|------|:--:|------|------|
| 📋 **Skill** | ✅ `/name` | 你手动 或 AI 自动 | 一个独立目录，包含 SKILL.md 指导文档，可附带脚本和参考文件 |
| ⌨️ **Command** | ✅ `/name` | 你手动 或 AI 自动 | 类似 Skill，但放在 `commands/` 目录，单文件，不能打包额外资源 |
| 🤖 **Agent** | ❌ 无 | 仅 AI 内部 | 拥有**独立上下文**的子 AI，可**指定模型**（用便宜的 haiku 省钱），不占主对话窗口 |
| 🔌 **MCP** | ❌ 无 | AI 自动 | 外部工具服务器，给 AI 提供新"工具"（如浏览器、操作文件） |
| 🔍 **LSP** | ❌ 无 | AI 通过内置 LSP 工具 | 代码语言服务器，提供定义跳转、引用查找、诊断（需手动装服务器二进制） |
| 🪝 **Hook** | ❌ 无 | 生命周期自动触发 | 在会话开始/结束等时机执行脚本，注入指令或改变行为 |

> 💡 **Command 已合并进 Skill**（[官方说明](https://code.claude.com/docs/en/skills)）。放在 `commands/deploy.md` 和放在 `skills/deploy/SKILL.md` 效果完全一样，都能通过 `/deploy` 触发。Command 是旧格式，Skill 是新格式，支持打包额外资源。

### 目录结构

一个插件可以同时包含多种组件，目录结构如下：

```
plugin-dev/                         # 插件根目录
├── .claude-plugin/
│   └── plugin.json                # 插件元数据（名称、描述、作者）
├── README.md
├── skills/                        # 📋 Skill
│   ├── skill-development/
│   │   ├── SKILL.md               #   技能定义（name: + description:）
│   │   └── scripts/               #   可附带脚本等资源
│   └── agent-development/
│       └── SKILL.md
├── commands/                      # ⌨️ Command（旧格式，单文件）
│   ├── create-plugin.md
│   └── plugin-structure.md
├── agents/                        # 🤖 Agent
│   ├── agent-creator.md           #   子智能体定义（可指定 model:）
│   └── code-simplifier.md
├── .mcp.json                      # 🔌 MCP 服务器配置
│                                  #   定义外部工具连接方式（stdio/HTTP）
├── .lsp.json                      # 🔍 LSP 语言服务器配置（社区插件风格）
│                                  #   { "command": "pyright", "extensionToLanguage": ... }
├── hooks/                         # 🪝 Hook（生命周期钩子）
│   └── hooks.json                 #   定义触发时机和命令
└── hooks-handlers/
    └── session-start.sh           #   钩子执行的脚本
```

> ⚠️ **LSP 配置也可以直接写在 `plugin.json` 的 `lspServers` 字段里**，不需要单独的 `.lsp.json` 文件。Claude Code 官方 LSP 插件均采用此方式。

### 通俗理解

```
Plugin = 一个文件夹，里面装着不同类型的"零件"

Skill:   📋 说明书——独立目录，能打包脚本和参考文件
Command: ⚡ 快捷指令——单文件版说明书，轻量简单
Agent:   🤖 小助手——AI 自己派"小弟"去干专门的活
MCP:     🔧 新工具——给 AI 装上"新武器"（浏览器、数据库连接等）
LSP:     🔍 代码雷达——让 AI 能跳转定义、查引用、看报错（需要装语言服务器）
Hook:    🪝 自动化——在特定时机执行脚本（如会话开始时注入指令）
```

### 举个例子

安装了 `plugin-dev` 这个插件后，你得到了：

- `/skill-development` → 📋 Skill：你说"帮我创建一个新 Skill"，它教你一步步做
- `/command-development` → ⌨️ Command：你输入 `/command-development`，它帮你生成命令模板
- `agent-creator` → 🤖 Agent：AI 自动派它去创建新的 Agent 文件
- `/plugin-structure` → ⌨️ Command：查看插件目录结构

安装了 `github` 这个插件后：

- 🔌 MCP：AI 自动获得了 `create_issue`、`search_repos` 等工具，不需要你手动调

安装了 `typescript-lsp` 这个插件后：

- 🔍 LSP：Claude 通过内置 `LSP` 工具查询代码定义、引用、诊断信息（编辑后自动推送错误提示）

---

## 📥 如何安装

### Step 1：添加官方市场

在 Claude Code 中输入：

```
/plugin marketplace add anthropics/claude-plugins-official
```

第二个市场（Anthropic 示例技能）：

```
/plugin marketplace add anthropics/skills
```

### Step 2：安装插件

```
/plugin install <插件名>@claude-plugins-official
```

例如：
```
/plugin install code-review@claude-plugins-official
/plugin install frontend-design@claude-plugins-official
```

### Step 3：查看已安装

```
/plugin list
```

### Step 4：选择安装作用域 🎯

安装插件时，Claude Code 会提示你选择作用域：

```
   Install for you (user scope)
  > Install for all collaborators on this repository (project scope)
    Install for you, in this repo only (local scope)
```

三种作用域的区别：

| 作用域 | 配置文件 | 生效范围 | 提交 Git？ | 别人能看到？ |
|--------|---------|---------|:---:|:---:|
| 👤 **User** | `~/.claude/settings.json` | 你所有项目 | ❌ | ❌ |
| 👥 **Project** | `.claude/settings.json` | 仓库所有协作者 | ✅ | ✅ |
| 🏠 **Local** | `.claude/settings.local.json` | 仅你，仅此项目 | ❌ 自动忽略 | ❌ |

**优先级**：`Local > Project > User`，Local 设置会覆盖 Project 和 User，Project 覆盖 User。

#### 👤 User Scope — 给你自己，跨所有项目

- 插件写到用户主目录的 `~/.claude/settings.json`
- 你打开**任何项目**都能用
- 适合：个人偏好的通用工具（如主题、代码审查风格）

#### 👥 Project Scope — 给团队所有人

- 插件写到项目的 `.claude/settings.json`，**提交到 Git**
- 别人 clone 代码后**自动生效**
- 适合：团队约定的统一工具（如 ESLint 检查、特定框架的 Skill）
- ⚠️ 只有仓库的**所有协作者**都能用，不是任何人

#### 🏠 Local Scope — 仅自己，仅此项目

- 插件写到 `.claude/settings.local.json`
- Claude Code 会自动在 `.gitignore` 中添加忽略，**不会提交**
- 适合：你个人在一个项目里试用插件，不想影响全局，也不想影响队友

> 💡 **简单记**：User = 我所有的项目，Project = 我们团队的约定，Local = 我自己在这个项目的私藏。

> 📖 **官方文档**：[Claude Code Settings](https://code.claude.com/docs/en/settings)

---


---

## 📊 概览

共 **228 个插件**，包含 **1461 个 Skill** + **63 个 Agent** + **151 个 Command**（截止 2026/06/17，marketplace 数据）。另有约 **46 个插件** 通过 MCP 工具或输出风格提供服务（无 Skill/Agent/Command）。

| 类型 | 用户手动调用 | AI 自动调用 | 示例 |
|------|:--:|:--:|------|
| 📋 Skill | ✅ `/name` | ✅ 匹配描述自动触发 | `/frontend-design` |
| ⌨️ Command | ✅ `/name` | ❌（通常） | `/code-review` |
| 🤖 Agent | ❌ 无 slash | ✅ AI 内部调用 | `code-simplifier` |
| 🔌 MCP | ❌ 无 slash | ✅ 自动提供工具 | `github`、`playwright` |
| 🔍 LSP | ❌ 无 slash | ✅ 通过内置 LSP 工具（定义/引用/诊断） | `clangd`、`pyright` |

> ⚠️ **LSP 插件需要手动安装语言服务器二进制**，插件只提供文件类型→服务器的映射配置。例如 `typescript-lsp` 需要 `npm install -g typescript-language-server typescript`，否则安装插件后不会有任何效果。

### 分类总览

| 分类 | 插件数 |
|------|:--:|
| [🛠️ 开发](#cat-dev) | 97 |
| [📋 效率](#cat-prod) | 42 |
| [🗄️ 数据库](#cat-db) | 31 |
| [🔒 安全](#cat-sec) | 13 |
| [📈 监控](#cat-mon) | 11 |
| [🚀 部署](#cat-dep) | 6 |
| [🎨 设计](#cat-des) | 5 |
| [📦 其他](#cat-other) | 20 |

---

## ⭐ 重点推荐（对学生最有用）

> 基于官方市场安装量 Top 50 筛选，适合 4-6 年级编程初学者。

| 插件 | 类型 | 调用方式 | 用途 | 安装量 |
|------|:--:|------|------|:---:|
| [`frontend-design`](frontend-design.md) | 📋 Skill | `/frontend-design` | 描述→生成界面，即时可见 👀 | 907K |
| [`superpowers`](superpowers.md) | 📋 插件（14 Skill） | 自动触发 | 教会 Claude 先思考再动手：头脑风暴→制定计划→分步实现 🧠 | 822K |
| [`playground`](playground.md) | 📋 Skill | `/playground` | 交互式 HTML 演示，好玩 🎮 | 57K |
| `skill-creator` | 📋 Skill | `/skill-creator` | 创建自己的 Skill，像搭积木 🧱 | 311K |
| `github` | 🔌 MCP | 自动 | GitHub 仓库操作（Issue、PR 等）🐙 | 278K |
| `commit-commands` | ⌨️ Command | `/commit`、`/commit-push-pr` | Git commit 工作流，一键提交 📦 | 153K |
| `playwright` | 🔌 MCP | 自动 | 浏览器自动化测试，看效果 🌐 | 268K |

> 💡 **所有 Skill 和 Command 都有 Slash Command**（`/name`）。只有 Agent 没有，仅 AI 内部调用。
> 
> 统计：Skill 1461（全有 slash）| Agent 63（无 slash）| Command 151（全有 slash）

