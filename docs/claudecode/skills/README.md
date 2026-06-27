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

## 📋 插件概要

<a id="cat-dev"></a>

### 🛠️ 开发（97 个）

| 插件 | 简介 |
|------|------|
| [agent-sdk-dev](#p-agent-sdk-dev) | Claude Agent SDK 开发工具包 |
| [agentforce-adlc](#p-agentforce-adlc) | Agentforce 智能体全生命周期开发 |
| [apollo-skills](#p-apollo-skills) | Apollo GraphQL 客户端与服务端开发 |
| [appwrite](#p-appwrite) | Appwrite 后端开发平台与 MCP 服务 |
| [astronomer-data-agents](#p-astronomer-data-agents) | Apache Airflow 数据工程与 DAG 开发 |
| [atomic-agents](#p-atomic-agents) | Atomic Agents 框架智能体开发 |
| [aws-agents](#p-aws-agents) | 在 AWS 上构建、部署和运维 AI 智能体 |
| [aws-amplify](#p-aws-amplify) | AWS Amplify Gen 2 全栈应用开发 |
| [aws-core](#p-aws-core) | AWS 基础设施即代码应用构建 |
| [aws-data-analytics](#p-aws-data-analytics) | S3、Glue、Athena 数据湖分析 |
| [aws-dev-toolkit](#p-aws-dev-toolkit) | AWS 开发工具包（34 技能、11 智能体） |
| [aws-serverless](#p-aws-serverless) | AWS 无服务器应用设计部署调试 |
| [aws-startup-advisor](#p-aws-startup-advisor) | 创业公司 AWS 架构与成本安全指导 |
| [base44](#p-base44) | Base44 全栈应用构建与 CLI 部署 |
| [boltz](#p-boltz) | Boltz 蛋白与分子结构预测和筛选 |
| [buildkite](#p-buildkite) | Buildkite CI/CD 流水线开发管理 |
| [cds-mcp](#p-cds-mcp) | SAP CAP 项目 AI 辅助开发 |
| [chrome-devtools-mcp](#p-chrome-devtools-mcp) | Chrome 浏览器实时调试与控制 |
| [circle-skills](#p-circle-skills) | Circle 稳定币支付与跨链桥开发 |
| [clangd-lsp](#p-clangd-lsp) | C/C++ 语言服务器代码智能 |
| [code-modernization](#p-code-modernization) | 遗留代码库现代化改造（COBOL 等） |
| [codspeed](#p-codspeed) | CodSpeed 性能测试与基准分析 |
| [context7](#p-context7) | Upstash 实时文档查询与代码示例 |
| [csharp-lsp](#p-csharp-lsp) | C# 语言服务器代码智能 |
| [data](#p-data) | Apache Airflow 数据工程与 DAG 开发 |
| [data-agent-kit-starter-pack](#p-data-agent-kit-starter-pack) | 数据工程师和 DBA 专属技能套件 |
| [datarobot-agent-skills](#p-datarobot-agent-skills) | DataRobot AI/ML 模型训练与部署 |
| [dominodatalab](#p-dominodatalab) | Domino 数据科学平台全功能支持 |
| [expo](#p-expo) | Expo React Native 应用构建与部署 |
| [fakechat](#p-fakechat) | 本地 Web 聊天用于测试通知流 |
| [feature-dev](#p-feature-dev) | 全流程功能开发与代码库分析 |
| [firecrawl](#p-firecrawl) | Firecrawl 网页抓取与内容提取 |
| [forge-skills](#p-forge-skills) | Atlassian Forge 应用开发和部署 |
| [frontend-design](frontend-design.md) | 高质量前端界面设计与生成 |
| [gopls-lsp](#p-gopls-lsp) | Go 语言服务器代码智能与重构 |
| [greptile](#p-greptile) | AI 驱动的代码库搜索与理解 |
| [huggingface-skills](#p-huggingface-skills) | Hugging Face 开源 AI 模型构建训练 |
| [jdtls-lsp](#p-jdtls-lsp) | Java 语言服务器（Eclipse JDT.LS） |
| [kotlin-lsp](#p-kotlin-lsp) | Kotlin 语言服务器代码智能 |
| [laravel-boost](#p-laravel-boost) | Laravel 开发工具包与智能辅助 |
| [liquid-lsp](#p-liquid-lsp) | Shopify Liquid 模板语言服务器 |
| [liquid-skills](#p-liquid-skills) | Liquid 语言基础与可访问性标准 |
| [lovable](#p-lovable) | Lovable 应用构建迭代和部署管理 |
| [lua-lsp](#p-lua-lsp) | Lua 语言服务器代码智能 |
| [lumen](#p-lumen) | 本地语义代码搜索与索引 MCP 服务 |
| [mcp-apps](#p-mcp-apps) | MCP Apps SDK 应用创建技能 |
| [mcp-server-dev](#p-mcp-server-dev) | MCP 服务器设计与构建技能 |
| [mcp-tunnels](#p-mcp-tunnels) | Anthropic MCP 隧道连接私有服务器 |
| [mercadopago](#p-mercadopago) | Mercado Pago 全产品支付集成 |
| [microsoft-docs](#p-microsoft-docs) | 微软官方文档与 API 参考访问 |
| [migration-to-aws](#p-migration-to-aws) | GCP 到 AWS 迁移规划指导 |
| [mintlify](#p-mintlify) | Mintlify 文档站点构建与美化 |
| [netlify-skills](#p-netlify-skills) | Netlify 平台全栈开发技能 |
| [netsuite-suitecloud](#p-netsuite-suitecloud) | NetSuite SuiteCloud 开发平台指导 |
| [nvidia-skills](#p-nvidia-skills) | NVIDIA 加速计算工作流（cuOpt 等） |
| [oracle-ai-data-platform-workbench-spark-connectors](#p-oracle-ai-data-platform-workbench-spark-connectors) | Oracle AI 数据平台 Spark 连接器 |
| [outputai](#p-outputai) | Output.ai 工作流开发工具包 |
| [php-lsp](#p-php-lsp) | PHP 语言服务器（Intelephense） |
| [playground](playground.md) | 创建交互式 HTML 实验场 |
| [plugin-dev](#p-plugin-dev) | Claude Code 插件开发完整工具包 |
| [postman](#p-postman) | Postman API 全生命周期管理 |
| [pydantic-ai](#p-pydantic-ai) | Pydantic AI 智能体开发最佳实践 |
| [pyright-lsp](#p-pyright-lsp) | Python 语言服务器类型检查 |
| [qodo-skills](#p-qodo-skills) | Qodo 可复用 AI 智能体能力库 |
| [qt-development-skills](#p-qt-development-skills) | Qt C++/QML 软件开发智能体技能 |
| [quarkus-agent](#p-quarkus-agent) | Quarkus 应用创建与管理 MCP 服务 |
| [ralph-loop](#p-ralph-loop) | 交互式自引用 AI 循环迭代开发 |
| [rc](#p-rc) | RevenueCat 内购项目后台配置管理 |
| [resend](#p-resend) | Resend 邮件 API 发送与接收 |
| [revenuecat](#p-revenuecat) | RevenueCat 内购项目后台配置管理 |
| [ruby-lsp](#p-ruby-lsp) | Ruby 语言服务器代码智能与分析 |
| [rust-analyzer-lsp](#p-rust-analyzer-lsp) | Rust 语言服务器代码智能与分析 |
| [sagemaker-ai](#p-sagemaker-ai) | AWS SageMaker AI 模型构建训练部署 |
| [sanity](#p-sanity) | Sanity 内容平台集成与管理 |
| [sap-cds-mcp](#p-sap-cds-mcp) | SAP CAP 项目 AI 辅助开发 |
| [sap-fiori-mcp-server](#p-sap-fiori-mcp-server) | SAP Fiori 开发工具的 MCP 服务 |
| [sap-mdk-server](#p-sap-mdk-server) | SAP MDK 移动开发 MCP 服务 |
| [serena](#p-serena) | 语义代码分析与智能重构 MCP 服务 |
| [servicenow-sdk](#p-servicenow-sdk) | ServiceNow 应用创建编辑与部署 |
| [shopify](#p-shopify) | Shopify 开发工具与文档查询 |
| [shopify-ai-toolkit](#p-shopify-ai-toolkit) | Shopify AI 开发工具包（18 个技能） |
| [skill-creator](#p-skill-creator) | 创建和改进 Claude Code Skill |
| [snowflake-cortex-code](#p-snowflake-cortex-code) | Snowflake Cortex Code 提示路由 |
| [sourcegraph](#p-sourcegraph) | 跨代码库搜索与代码理解 |
| [stripe](#p-stripe) | Stripe 支付开发插件 |
| [sumup](#p-sumup) | SumUp 终端与在线支付集成 |
| [superpowers](superpowers.md) | 脑暴与子智能体驱动开发超能力 |
| [swift-lsp](#p-swift-lsp) | Swift 语言服务器（SourceKit-LSP） |
| [teamcity-cli](#p-teamcity-cli) | TeamCity CI/CD 交互命令行工具 |
| [terraform](#p-terraform) | Terraform 生态系统集成与管理 |
| [togetherai-skills](#p-togetherai-skills) | Together AI 平台推理训练与嵌入 |
| [twilio-developer-kit](#p-twilio-developer-kit) | Twilio API 开发工具包（55 个技能） |
| [typescript-lsp](#p-typescript-lsp) | TypeScript/JavaScript 语言服务器 |
| [ui5](#p-ui5) | SAPUI5/OpenUI5 项目创建与验证 |
| [ui5-typescript-conversion](#p-ui5-typescript-conversion) | SAPUI5 项目 JS 转 TypeScript |
| [wix](#p-wix) | Wix 网站和应用构建管理部署 |
| [zoom-plugin](#p-zoom-plugin) | Zoom 集成规划构建与调试 |

<a id="cat-prod"></a>

### 📋 效率（42 个）

| 插件 | 简介 |
|------|------|
| [airtable](#p-airtable) | Airtable 数据库与智能体运营平台 |
| [airwallex](#p-airwallex) | Airwallex 支付账单与现金流管理 |
| [apollo](#p-apollo) | Apollo 销售线索挖掘与分析 |
| [asana](#p-asana) | Asana 项目管理与任务跟踪 |
| [atlassian](#p-atlassian) | Atlassian Jira 与 Confluence 集成 |
| [box](#p-box) | Box 云存储文件管理与协作 |
| [carta-cap-table](#p-carta-cap-table) | Carta 股权结构表与估值管理 |
| [carta-crm](#p-carta-crm) | Carta CRM 投资人与交易管理 |
| [carta-investors](#p-carta-investors) | Carta 投资人数据与业绩分析 |
| [circleback](#p-circleback) | Circleback 会议与邮件上下文集成 |
| [claude-code-setup](#p-claude-code-setup) | 代码库分析与自动化配置推荐 |
| [claude-md-management](#p-claude-md-management) | CLAUDE.md 文件维护与质量审核 |
| [code-review](#p-code-review) | 多智能体自动化 PR 代码审查 |
| [code-simplifier](#p-code-simplifier) | 自动简化优化代码清晰度 |
| [coderabbit](#p-coderabbit) | CodeRabbit AI 代码审查伙伴 |
| [commit-commands](#p-commit-commands) | Git 提交、推送与 PR 创建命令 |
| [cwc-makers](#p-cwc-makers) | Makers Cardputer 开发板上手引导 |
| [desktop-commander](#p-desktop-commander) | 终端命令与文件操作 MCP 服务 |
| [discord](#p-discord) | Discord 消息桥接与访问控制 |
| [exa](#p-exa) | Exa AI 网页搜索与深度研究 |
| [github](#p-github) | GitHub 仓库管理与 PR 操作 |
| [gitlab](#p-gitlab) | GitLab DevOps 平台集成管理 |
| [hookify](#p-hookify) | 创建自定义 Hook 防止不期望行为 |
| [hunter](#p-hunter) | Hunter 专业邮箱查找与验证 |
| [imessage](#p-imessage) | iMessage 消息桥接与访问控制 |
| [intercom](#p-intercom) | Intercom 客户支持对话分析 |
| [legalzoom](#p-legalzoom) | LegalZoom 法务指导与文档工具 |
| [linear](#p-linear) | Linear 事务跟踪与项目管理 |
| [lusha](#p-lusha) | Lusha B2B 销售线索挖掘与丰富 |
| [notion](#p-notion) | Notion 工作空间集成与管理 |
| [pigment](#p-pigment) | Pigment 业务数据分析与建模 |
| [pr-review-toolkit](#p-pr-review-toolkit) | 全方位 PR 审查（评论测试安全等） |
| [save-to-spotify](#p-save-to-spotify) | 创建音频节目并保存到 Spotify |
| [session-report](#p-session-report) | Claude Code 会话用量 HTML 报告 |
| [slack](#p-slack) | Slack 消息搜索与频道管理 |
| [spotify-ads-api](#p-spotify-ads-api) | Spotify 广告活动自然语言管理 |
| [telegram](#p-telegram) | Telegram 消息桥接与访问控制 |
| [vibe-prospecting](#p-vibe-prospecting) | Vibe 实时 B2B 公司与联系人数据 |
| [windsor-ai](#p-windsor-ai) | Windsor 连接 325+ 数据源查询 |
| [youdotcom-agent-skills](#p-youdotcom-agent-skills) | You.com 网页搜索与研究技能 |
| [zapier](#p-zapier) | 连接 8000+ 应用自动化工作流 |
| [zoominfo](#p-zoominfo) | ZoomInfo B2B 公司联系人数据查询 |

<a id="cat-db"></a>

### 🗄️ 数据库（31 个）

| 插件 | 简介 |
|------|------|
| [alloydb](#p-alloydb) | AlloyDB PostgreSQL 数据库连接管理 |
| [alloydb-omni](#p-alloydb-omni) | AlloyDB Omni 数据库连接管理 |
| [azure-cosmos-db-assistant](#p-azure-cosmos-db-assistant) | Azure Cosmos DB 专家助手 |
| [bigdata-com](#p-bigdata-com) | Bigdata.com 金融研究分析平台 |
| [bigquery-data-analytics](#p-bigquery-data-analytics) | BigQuery 数据查询与洞察分析 |
| [clickhouse](#p-clickhouse) | ClickHouse Cloud 数据库连接管理 |
| [clickhouse-best-practices](#p-clickhouse-best-practices) | ClickHouse 最佳实践 28 条规则 |
| [cloud-sql-mysql](#p-cloud-sql-mysql) | Cloud SQL MySQL 数据库连接管理 |
| [cloud-sql-postgresql](#p-cloud-sql-postgresql) | Cloud SQL PostgreSQL 数据库管理 |
| [cloud-sql-sqlserver](#p-cloud-sql-sqlserver) | Cloud SQL SQL Server 连接管理 |
| [cockroachdb](#p-cockroachdb) | CockroachDB 集群连接与管理 |
| [convex](#p-convex) | Convex 全栈后端数据库平台 |
| [databases-on-aws](#p-databases-on-aws) | AWS 数据库组合专家指导 |
| [datahub-skills](#p-datahub-skills) | DataHub 数据目录开发与交互 |
| [dataproc](#p-dataproc) | Dataproc 集群和任务管理 |
| [dataverse](#p-dataverse) | Microsoft Dataverse 构建分析管理 |
| [duckdb-skills](#p-duckdb-skills) | DuckDB 数据分析引擎与文件查询 |
| [firebase](#p-firebase) | Google Firebase 后端服务集成管理 |
| [firestore-native](#p-firestore-native) | Firestore 数据库连接与文档操作 |
| [knowledge-catalog](#p-knowledge-catalog) | Knowledge Catalog 数据发现与治理 |
| [looker](#p-looker) | Looker 数据分析与 LookML 建模 |
| [mongodb](#p-mongodb) | MongoDB 数据库官方连接管理工具 |
| [neon](#p-neon) | Neon 无服务器 PostgreSQL 项目管理 |
| [oracledb](#p-oracledb) | Oracle 数据库连接查询与交互 |
| [pinecone](#p-pinecone) | Pinecone 向量数据库开发集成 |
| [planetscale](#p-planetscale) | PlanetScale 数据库管理与查询 |
| [qdrant-skills](#p-qdrant-skills) | Qdrant 向量搜索优化与扩展 |
| [redis-development](#p-redis-development) | Redis 数据结构与缓存开发实践 |
| [spanner](#p-spanner) | Spanner 数据库自然语言查询 |
| [supabase](#p-supabase) | Supabase 数据库认证存储集成 |
| [zilliz](#p-zilliz) | Zilliz Cloud 向量数据库集群管理 |

<a id="cat-sec"></a>

### 🔒 安全（13 个）

| 插件 | 简介 |
|------|------|
| 42crunch-api-security-testing | 42Crunch API 安全自动审计测试 |
| [auth0](#p-auth0) | Auth0 多框架登录认证集成 |
| [crowdstrike-falcon-foundry](#p-crowdstrike-falcon-foundry) | CrowdStrike 网络安全应用开发技能 |
| [duende-skills](#p-duende-skills) | Duende OAuth/OIDC 身份管理 |
| [jfrog](#p-jfrog) | JFrog 制品库管理与安全扫描 |
| [security-guidance](#p-security-guidance) | AI 生成代码安全审查与指导 |
| [semgrep](#p-semgrep) | Semgrep 实时代码安全漏洞检测 |
| [sonarqube](#p-sonarqube) | SonarQube 代码质量与安全自动检查 |
| [sonatype-guide](#p-sonatype-guide) | Sonatype 软件供应链依赖安全 |
| [vanta](#p-vanta) | Vanta 安全合规平台集成 |
| [vanta-mcp-plugin](#p-vanta-mcp-plugin) | Vanta 安全合规平台集成 |
| [workos](#p-workos) | WorkOS 企业 SSO 与身份认证 |
| [zscaler](#p-zscaler) | Zscaler 云安全平台管理 |

<a id="cat-mon"></a>

### 📈 监控（11 个）

| 插件 | 简介 |
|------|------|
| [amplitude](#p-amplitude) | Amplitude 产品分析与数据洞察 |
| [dash0](#p-dash0) | Claude Code 会话 OpenTelemetry 可观测 |
| [datadog](#p-datadog) | Datadog 云监控平台集成 |
| [fullstory](#p-fullstory) | FullStory 行为分析与会话回放 |
| [langfuse-observability](#p-langfuse-observability) | Langfuse AI 可观测性插件 |
| [logfire](#p-logfire) | Logfire Python 应用可观测性集成 |
| [pagerduty](#p-pagerduty) | PagerDuty 风险评分与事件管理 |
| [posthog](#p-posthog) | PostHog 产品分析与功能标志管理 |
| [rootly](#p-rootly) | Rootly 全生命周期事件管理 |
| [sentry](#p-sentry) | Sentry 错误监控与堆栈分析 |
| [sentry-cli](#p-sentry-cli) | Sentry 命令行工具技能 |

<a id="cat-dep"></a>

### 🚀 部署（6 个）

| 插件 | 简介 |
|------|------|
| [azure](#p-azure) | Azure 云平台专家集成管理 |
| [cloudflare](#p-cloudflare) | Cloudflare Workers 与 Agent SDK 开发 |
| [deploy-on-aws](#p-deploy-on-aws) | AWS 应用部署架构推荐与成本估算 |
| [railway](#p-railway) | Railway 应用和数据库部署管理 |
| [valtown](#p-valtown) | Val Town 快速构建与部署平台 |
| [vercel](#p-vercel) | Vercel 部署平台集成管理 |

<a id="cat-des"></a>

### 🎨 设计（5 个）

| 插件 | 简介 |
|------|------|
| [adobe-for-creativity](#p-adobe-for-creativity) | Adobe AI 创意工具图片编辑与设计 |
| [figma](#p-figma) | Figma 设计平台集成与组件提取 |
| [hyperframes](#p-hyperframes) | HyperFrames HTML 转视频生成工具 |
| [miro](#p-miro) | Miro 白板访问与图表创建 |
| [runway-api](#p-runway-api) | Runway API 视频图片音频生成 |

<a id="cat-learn"></a>

### 📚 学习（2 个）

| 插件 | 简介 |
|------|------|
| [explanatory-output-style](#p-explanatory-output-style) | 为代码实现添加教学性说明 |
| [learning-output-style](#p-learning-output-style) | 交互式学习模式引导代码练习 |

<a id="cat-math"></a>

### 🧮 数学（1 个）

| 插件 | 简介 |
|------|------|
| [math-olympiad](#p-math-olympiad) | 数学竞赛题目求解与对抗验证 |

<a id="cat-test"></a>

### 🧪 测试（1 个）

| 插件 | 简介 |
|------|------|
| [playwright](#p-playwright) | 浏览器自动化与端到端测试 |

<a id="cat-loc"></a>

### 📍 位置（2 个）

| 插件 | 简介 |
|------|------|
| [amazon-location-service](#p-amazon-location-service) | Amazon Location 地图与位置服务开发 |
| [mapbox](#p-mapbox) | Mapbox 地图与位置感知应用开发 |

<a id="cat-other"></a>

### 📦 其他（14 个）

| 插件 | 简介 |
|------|------|
| [ai-plugins](#p-ai-plugins) | Endor Labs 软件安全风险扫描修复 |
| [aikido](#p-aikido) | Aikido SAST 与 IaC 安全漏洞扫描 |
| [atlan](#p-atlan) | Atlan 数据目录搜索与治理 |
| [brightdata-plugin](#p-brightdata-plugin) | 网页抓取与结构化数据提取 |
| [cloudinary](#p-cloudinary) | Cloudinary 图片视频管理与优化 |
| [data-engineering](#p-data-engineering) | 数据工程仓库探索与管道开发 |
| [fastly-agent-toolkit](#p-fastly-agent-toolkit) | Fastly 开发工具与平台技能 |
| [fiftyone](#p-fiftyone) | FiftyOne 数据集与视觉模型构建 |
| [nightvision](#p-nightvision) | NightVision DAST API 安全扫描 |
| [nimble](#p-nimble) | Nimble 网页数据搜索提取与抓取 |
| [postiz](#p-postiz) | Postiz 社交媒体自动化发布 |
| [prisma](#p-prisma) | Prisma PostgreSQL 数据库管理迁移 |
| [remember](#p-remember) | Claude Code 持续记忆与对话压缩 |
| wordpress.com | WordPress 网站创建与编辑 |


---

## 🛠️ Development（97 个插件）

<a id="p-agent-sdk-dev"></a>

**agent-sdk-dev**（2 Agent、1 Command）

> Claude Agent SDK 开发工具包

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| agent-sdk-verifier-ts | 🤖 Agent | Use this agent to verify that a TypeScript Agent SDK application is properly configured, follows SDK best practices and documentation recommendations, and is ready for deployment or testing. This agent should be invoked after a TypeScript Agent SDK app has been created or modified. |
| agent-sdk-verifier-py | 🤖 Agent | Use this agent to verify that a Python Agent SDK application is properly configured, follows SDK best practices and documentation recommendations, and is ready for deployment or testing. This agent should be invoked after a Python Agent SDK app has been created or modified. |
| `/agent-sdk-dev:new-sdk-app` | ⌨️ Command | Create and setup a new Claude Agent SDK application |

<a id="p-agentforce-adlc"></a>

**agentforce-adlc**（4 Skill、4 Agent）

> Agentforce 智能体全生命周期开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/securing-agentforce` | 📋 Skill | Run OWASP LLM Top 10 security assessments against live Agentforce agents. TRIGGER when: user asks for security testing, OWASP scan, red-teaming, penetration testing, security grade, vulnerability assessment, prompt injection test, data leakage test, excessive agency test, security posture check, or hardening recommendations. DO NOT TRIGGER when: user runs functional smoke tests or batch tests (use testing-agentforce); performs static safety review of .agent file content (use developing-agentforce Section 15); analyzes production session traces (use observing-agentforce); writes or modifies .agent files. |
| `/observing-agentforce` | 📋 Skill | Analyze production Agentforce agent behavior using session traces and Data Cloud. TRIGGER when: user queries STDM session data or Data Cloud trace records; investigates production agent failures, regressions, or performance issues; asks about session traces, conversation logs, or agent metrics; wants to reproduce a reported production issue in preview; runs findSessions or trace analysis queries. DO NOT TRIGGER when: user creates, modifies, or debugs .agent files during development (use developing-agentforce); writes or runs test specs (use testing-agentforce); uses sf agent preview for local development iteration; deploys or publishes agents. |
| `/developing-agentforce` | 📋 Skill | Build, modify, debug, and deploy agents with Agentforce Agent Script. TRIGGER when: user creates, modifies, or asks about .agent files or aiAuthoringBundle metadata; changes agent behavior, responses, or conversation logic; designs agent actions, tools, subagents, or flow control; writes or reviews an Agent Spec; previews, debugs, deploys, publishes, or tests agents; uses Agent Script CLI commands (sf agent generate/preview/publish/test). DO NOT TRIGGER when: Apex development, Flow building, Prompt Template authoring, Experience Cloud configuration, or general Salesforce CLI tasks unrelated to Agent Script. |
| `/testing-agentforce` | 📋 Skill | Write, run, and analyze structured test suites for Agentforce agents. TRIGGER when: user writes or modifies test spec YAML (AiEvaluationDefinition); runs sf agent test create, run, run-eval, or results commands; asks about test coverage strategy, metric selection, or custom evaluations; interprets test results or diagnoses test failures; asks about batch testing, regression suites, or CI/CD test integration. DO NOT TRIGGER when: user creates, modifies, previews, or debugs .agent files (use developing-agentforce); deploys or publishes agents; writes Agent Script code; uses sf agent preview for development iteration; analyzes production session traces (use observing-agentforce); requests OWASP, security, or red-team testing (use securing-agentforce). |
| adlc-qa | 🤖 Agent | Tests Agentforce agents and optimizes based on session trace analysis |
| adlc-orchestrator | 🤖 Agent | Plan-mode orchestrator for the Agent Development Life Cycle |
| adlc-engineer | 🤖 Agent | Platform engineer — scaffolds Flow/Apex metadata and deploys agent bundles |
| adlc-author | 🤖 Agent | Writes Agentforce Agent Script (.agent) files from requirements |

<a id="p-apollo-skills"></a>

**apollo-skills**（14 Skill）

> Apollo GraphQL 客户端与服务端开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/graphql-schema` | 📋 Skill | Guide for designing GraphQL schemas following industry best practices. Use this skill when: (1) designing a new GraphQL schema or API, (2) reviewing existing schema for improvements, (3) deciding on type structures or nullability, (4) implementing pagination or error patterns, (5) ensuring security in schema design. |
| `/apollo-connectors` | 📋 Skill | Guide for integrating REST APIs into GraphQL supergraphs using Apollo Connectors with @source and @connect directives. Use this skill when the user: (1) mentions "connectors", "Apollo Connectors", or "REST Connector", (2) wants to integrate a REST API into GraphQL, (3) references @source or @connect directives, (4) works with files containing "# Note to AI Friends: This is an Apollo Connectors schema". |
| `/apollo-ios` | 📋 Skill | Guide for building Apple-platform applications with Apollo iOS, the strongly-typed GraphQL client for Swift. Use this skill when: (1) adding Apollo iOS to a Swift Package Manager or Xcode project, (2) configuring `apollo-codegen-config.json` and running code generation, (3) configuring an `ApolloClient` with auth, interceptors, and caching, (4) writing queries, mutations, or subscriptions from SwiftUI views, (5) writing tests against generated operation mocks. |
| `/rover` | 📋 Skill | Guide for using Apollo Rover CLI to manage GraphQL schemas and federation. Use this skill when: (1) publishing or fetching subgraph/graph schemas, (2) composing supergraph schemas locally or via GraphOS, (3) running local supergraph development with rover dev, (4) validating schemas with check and lint commands, (5) configuring Rover authentication and environment, (6) exploring or searching a graph's schema for agent-driven discovery (rover schema describe / rover schema search). |
| `/apollo-mcp-server` | 📋 Skill | Guide for using Apollo MCP Server to connect AI agents with GraphQL APIs. Use this skill when: (1) setting up or configuring Apollo MCP Server, (2) defining MCP tools from GraphQL operations, (3) using introspection tools (introspect, search, validate, execute), (4) troubleshooting MCP server connectivity or tool execution issues. |
| `/apollo-kotlin` | 📋 Skill | Guide for building applications with Apollo Kotlin, the GraphQL client library for Android and Kotlin. Use this skill when: (1) setting up Apollo Kotlin in a Gradle project for Android, Kotlin/JVM, or KMP, (2) configuring schema download and codegen for GraphQL services, (3) configuring an `ApolloClient` with auth, interceptors, and caching, (4) writing queries, mutations, or subscriptions, |
| `/rust-best-practices` | 📋 Skill | Guide for writing idiomatic Rust code based on Apollo GraphQL's best practices handbook. Use this skill when: (1) writing new Rust code or functions, (2) reviewing or refactoring existing Rust code, (3) deciding between borrowing vs cloning or ownership patterns, (4) implementing error handling with Result types, (5) optimizing Rust code for performance, (6) writing tests or documentation for Rust projects. |
| `/apollo-router-plugin-creator` | 📋 Skill | Guide for writing Apollo Router native Rust plugins. Use this skill when: (1) users want to create a new router plugin, (2) users want to add service hooks (router_service, supergraph_service, execution_service, subgraph_service), (3) users want to modify an existing router plugin, (4) users need to understand router plugin patterns or the request lifecycle. (5) triggers on requests like "create a new plugin", "add a router plugin", "modify the X plugin", or "add subgraph_service hook". |
| `/graphql-operations` | 📋 Skill | Guide for writing GraphQL operations (queries, mutations, fragments) following best practices. Use this skill when: (1) writing GraphQL queries or mutations, (2) organizing operations with fragments, (3) optimizing data fetching patterns, (4) setting up type generation or linting, (5) reviewing operations for efficiency. |
| `/apollo-router` | 📋 Skill | Version-aware guide for configuring and running Apollo Router for federated GraphQL supergraphs. Generates correct YAML for both Router v1.x and v2.x. Use this skill when: (1) setting up Apollo Router to run a supergraph, (2) configuring routing, headers, or CORS, (3) implementing custom plugins (Rhai scripts or coprocessors), (4) configuring telemetry (tracing, metrics, logging), (5) troubleshooting Router performance or connectivity issues. |
| `/apollo-client` | 📋 Skill | Guide for building React applications with Apollo Client 4.x. Use this skill when: (1) setting up Apollo Client in a React project, (2) writing GraphQL queries or mutations with hooks, (3) configuring caching or cache policies, (4) managing local state with reactive variables, (5) troubleshooting Apollo Client errors or performance issues. |
| `/apollo-federation` | 📋 Skill | Guide for authoring Apollo Federation subgraph schemas. Use this skill when: (1) creating new subgraph schemas for a federated supergraph, (2) defining or modifying entities with @key, (3) sharing types/fields across subgraphs with @shareable, (4) working with federation directives (@external, @requires, @provides, @override, @inaccessible), (5) troubleshooting composition errors, (6) any task involving federation schema design patterns. |
| `/skill-creator` | 📋 Skill | Guide for creating effective skills for Apollo GraphQL and GraphQL development. Use this skill when: (1) users want to create a new skill, (2) users want to update an existing skill, (3) users ask about skill structure or best practices, (4) users need help writing SKILL.md files. |
| `/apollo-server` | 📋 Skill | Guide for building GraphQL servers with Apollo Server 5.x. Use this skill when: (1) setting up a new Apollo Server project, (2) writing resolvers or defining GraphQL schemas, (3) implementing authentication or authorization, (4) creating plugins or custom data sources, (5) troubleshooting Apollo Server errors or performance issues. |

<a id="p-appwrite"></a>

**appwrite**（11 Skill、2 Command）

> Appwrite 后端开发平台与 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/swift` | 📋 Skill | Appwrite Swift SDK skill. Use when building native iOS, macOS, watchOS, or tvOS apps, or server-side Swift applications with Appwrite. Covers client-side auth (email, OAuth), database queries, file uploads, real-time subscriptions with async/await, and server-side admin via API keys for user management, database administration, storage, and functions. |
| `/kotlin` | 📋 Skill | Appwrite Kotlin SDK skill. Use when building native Android apps or server-side Kotlin/JVM backends with Appwrite. Covers client-side auth (email, OAuth with Activity integration), database queries, file uploads, real-time subscriptions with coroutine support, and server-side admin via API keys for user management, database administration, storage, and functions. |
| `/cli` | 📋 Skill | Appwrite CLI skill. Use when managing Appwrite projects from the command line. Covers installation, login, project initialization, deploying functions/sites/tables/buckets/teams/topics, managing resources, non-interactive CI/CD mode, and generating type-safe SDKs. |
| `/dotnet` | 📋 Skill | Appwrite .NET SDK skill. Use when building server-side C# or .NET applications with Appwrite, including ASP.NET and Blazor integrations. Covers user management, database/table CRUD, file storage, and functions via API keys. |
| `/python` | 📋 Skill | Appwrite Python SDK skill. Use when building server-side Python applications with Appwrite, including Django, Flask, and FastAPI integrations. Covers user management, database/table CRUD, file storage, and functions via API keys. |
| `/php` | 📋 Skill | Appwrite PHP SDK skill. Use when building server-side PHP applications with Appwrite, including Laravel and Symfony integrations. Covers user management, database/table CRUD, file storage, and functions via API keys. |
| `/rust` | 📋 Skill | Appwrite Rust SDK skill. Use when building server-side Rust applications with Appwrite. Covers async client setup with API keys, user management, TablesDB database/table/row operations, file storage, function executions, permissions, queries, and error handling. Uses the crates.io `appwrite` package and Tokio. |
| `/dart` | 📋 Skill | Appwrite Dart SDK skill. Use when building Flutter apps (mobile, web, desktop) or server-side Dart applications with Appwrite. Covers client-side auth (email, OAuth), database queries, file uploads with native file handling, real-time subscriptions, and server-side admin via API keys for user management, database administration, storage, and functions. |
| `/go` | 📋 Skill | Appwrite Go SDK skill. Use when building server-side Go applications with Appwrite. Covers user management, database/table CRUD, file storage, and functions via API keys. Uses per-service packages and functional options pattern. |
| `/typescript` | 📋 Skill | Appwrite TypeScript SDK skill. Use when building browser-based JavaScript/TypeScript apps, React Native mobile apps, or server-side Node.js/Deno backends with Appwrite. Covers client-side auth (email, OAuth, anonymous), database queries, file uploads, real-time subscriptions, and server-side admin via API keys for user management, database administration, storage, and functions. |
| `/ruby` | 📋 Skill | Appwrite Ruby SDK skill. Use when building server-side Ruby applications with Appwrite, including Rails and Sinatra integrations. Covers user management, database/table CRUD, file storage, and functions via API keys. |
| `/deploy-function` | ⌨️ Command | Deploy a function using the Appwrite CLI |
| `/deploy-site` | ⌨️ Command | Deploy a site using the Appwrite CLI |

<a id="p-astronomer-data-agents"></a>

**astronomer-data-agents**（24 Skill）

> Apache Airflow 数据工程与 DAG 开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/airflow` | 📋 Skill | Queries, manages, and troubleshoots Apache Airflow using the af CLI. Covers listing DAGs, triggering runs, reading task logs, diagnosing failures, debugging DAG import errors, checking connections, variables, pools, and monitoring health. Also routes to sub-skills for writing DAGs, debugging, deploying, and migrating Airflow 2 to 3. Use when user mentions "Airflow", "DAG", "DAG run", "task log", "import error", "parse error", "broken DAG", or asks to "trigger a pipeline", "debug import errors", "check Airflow health", "list connections", "retry a run", or any Airflow operation. Do NOT use for warehouse/SQL analytics on Airflow metadata tables — use analyzing-data instead. |
| `/debugging-dags` | 📋 Skill | Comprehensive DAG failure diagnosis and root cause analysis. Use for complex debugging requests requiring deep investigation like "diagnose and fix the pipeline", "full root cause analysis", "why is this failing and how to prevent it". For simple debugging ("why did dag fail", "show logs"), the airflow entrypoint skill handles it directly. This skill provides structured investigation and prevention recommendations. |
| `/managing-astro-local-env` | 📋 Skill | Manage local Airflow environment with Astro CLI (Docker and standalone modes). Use when the user wants to start, stop, or restart Airflow, view logs, query the Airflow API, troubleshoot, or fix environment issues. For project setup, see setting-up-astro-project. |
| `/cosmos-dbt-core` | 📋 Skill | Use when turning a dbt Core project into an Airflow DAG/TaskGroup using Astronomer Cosmos. Does not cover dbt Fusion. Before implementing, verify dbt engine, warehouse, Airflow version, execution environment, DAG vs TaskGroup, and manifest availability. |
| `/dag-factory` | 📋 Skill | Author Apache Airflow DAGs declaratively with dag-factory YAML configs. Use when creating dag-factory templates, composing DAGs from YAML for dag-factory, configuring defaults/dynamic tasks/datasets/callbacks for dag-factory, or validating dag-factory configurations. |
| `/migrating-ai-sdk-to-common-ai` | 📋 Skill | Migrates Airflow projects from airflow-ai-sdk to apache-airflow-providers-common-ai 0.1.0+. Use this skill when the user wants to replace airflow-ai-sdk with the official Airflow AI provider, migrate LLM decorators (@task.llm, @task.agent, @task.llm_branch, @task.embed), switch from model strings/objects to connection-based LLM configuration, or update imports from airflow_ai_sdk to the new provider. Also trigger when the user mentions common-ai provider, AIP-99, pydanticai connection, or migrating away from airflow-ai-sdk. |
| `/airflow-hitl` | 📋 Skill | Use when the user needs human-in-the-loop workflows in Airflow (approval/reject, form input, or human-driven branching). Covers ApprovalOperator, HITLOperator, HITLBranchOperator, HITLEntryOperator, HITLTrigger. Requires Airflow 3.1+. Does not cover AI/LLM calls (see airflow-ai). |
| `/creating-openlineage-extractors` | 📋 Skill | Create custom OpenLineage extractors for Airflow operators. Use when the user needs lineage from unsupported or third-party operators, wants column-level lineage, or needs complex extraction logic beyond what inlets/outlets provide. |
| `/airflow-plugins` | 📋 Skill | Build Airflow 3.1+ plugins that embed FastAPI apps, custom UI pages, React components, middleware, macros, and operator links directly into the Airflow UI. Use this skill whenever the user wants to create an Airflow plugin, add a custom UI page or nav entry to Airflow, build FastAPI-backed endpoints inside Airflow, serve static assets from a plugin, embed a React app in the Airflow UI, add middleware to the Airflow API server, create custom operator extra links, or call the Airflow REST API from inside a plugin. Also trigger when the user mentions AirflowPlugin, fastapi_apps, external_views, react_apps, plugin registration, or embedding a web app in Airflow 3.1+. If someone is building anything custom inside Airflow 3.1+ that involves Python and a browser-facing interface, this skill almost certainly applies. |
| `/analyzing-data` | 📋 Skill | Queries data warehouse and answers business questions about data. Handles questions requiring database/warehouse queries including "who uses X", "how many Y", "show me Z", "find customers", "what is the count", data lookups, metrics, trends, or SQL analysis. |
| `/cosmos-dbt-fusion` | 📋 Skill | Use when running a dbt Fusion project with Astronomer Cosmos. Covers Cosmos 1.11+ configuration for Fusion on Snowflake/Databricks with ExecutionMode.LOCAL. Before implementing, verify dbt engine is Fusion (not Core), warehouse is supported, and local execution is acceptable. Does not cover dbt Core. |
| `/authoring-dags` | 📋 Skill | Workflow and best practices for writing Apache Airflow DAGs. Use when the user wants to create a new DAG, write pipeline code, or asks about DAG patterns and conventions. For testing and debugging DAGs, see the testing-dags skill. |
| `/warehouse-init` | 📋 Skill | Initialize warehouse schema discovery. Generates .astro/warehouse.md with all table metadata for instant lookups. Run once per project, refresh when schema changes. Use when user says "/astronomer-data:warehouse-init" or asks to set up data discovery. |
| `/annotating-task-lineage` | 📋 Skill | Annotate Airflow tasks with data lineage using inlets and outlets. Use when the user wants to add lineage metadata to tasks, specify input/output datasets, or enable lineage tracking for operators without built-in OpenLineage extraction. |
| `/profiling-tables` | 📋 Skill | Deep-dive data profiling for a specific table. Use when the user asks to profile a table, wants statistics about a dataset, asks about data quality, or needs to understand a table's structure and content. Requires a table name. |
| `/checking-freshness` | 📋 Skill | Quick data freshness check. Use when the user asks if data is up to date, when a table was last updated, if data is stale, or needs to verify data currency before using it. |
| `/testing-dags` | 📋 Skill | Complex DAG testing workflows with debugging and fixing cycles. Use for multi-step testing requests like "test this dag and fix it if it fails", "test and debug", "run the pipeline and troubleshoot issues". For simple test requests ("test dag", "run dag"), the airflow entrypoint skill handles it directly. This skill is for iterative test-debug-fix cycles. |
| `/blueprint` | 📋 Skill | Define reusable Airflow task group templates with Pydantic validation and compose DAGs from YAML. Use when creating blueprint templates, composing DAGs from YAML, validating configurations, or enabling no-code DAG authoring for non-engineers. |
| `/deploying-airflow` | 📋 Skill | Deploy Airflow DAGs and projects. Use when the user wants to deploy code, push DAGs, set up CI/CD, deploy to production, or asks about deployment strategies for Airflow. |
| `/tracing-downstream-lineage` | 📋 Skill | Trace downstream data lineage and impact analysis. Use when the user asks what depends on this data, what breaks if something changes, downstream dependencies, or needs to assess change risk before modifying a table or DAG. |
| `/setting-up-astro-project` | 📋 Skill | Initialize and configure Astro/Airflow projects. Use when the user wants to create a new project, set up dependencies, configure connections/variables, or understand project structure. For running the local environment, see managing-astro-local-env. |
| `/delegating-to-otto` | 📋 Skill | Drives Astronomer's Otto agent (`astro otto`) as a delegated sub-agent for Airflow, dbt, and data-engineering work. Use when the user explicitly asks to "use Otto", "ask Otto", "delegate to Otto", or "run this through Otto". Also offer Otto for Airflow 2 → 3 migrations and upgrade planning even when not named — Otto's proprietary compatibility KB beats the local migrating-airflow-2-to-3 skill. Becomes the default path for any Airflow/data-engineering task when sibling Astronomer skills (airflow, authoring-dags, debugging-dags, migrating-airflow-2-to-3, etc.) are NOT loaded in the current session. Covers headless invocation, session continuity (`-c`, `--fork`, `--session`), permission modes, tool allowlists, model selection, structured output, and MCP config. **Do not load this skill if you are Otto** — Otto must not delegate to itself. |
| `/migrating-airflow-2-to-3` | 📋 Skill | Guide for migrating Apache Airflow 2.x projects to Airflow 3.x. Use when the user mentions Airflow 3 migration, upgrade, compatibility issues, breaking changes, or wants to modernize their Airflow codebase. If you detect Airflow 2.x code that needs migration, prompt the user and ask if they want you to help upgrade. Always load this skill as the first step for any migration-related request. |
| `/tracing-upstream-lineage` | 📋 Skill | Trace upstream data lineage. Use when the user asks where data comes from, what feeds a table, upstream dependencies, data sources, or needs to understand data origins. |

<a id="p-atomic-agents"></a>

**atomic-agents**（🔌 MCP）

> Atomic Agents 框架智能体开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__atomic-agents` | 🔌 MCP | Comprehensive development workflow for building AI agents with the Atomic Agents framework. Includes specialized agents for schema design, architec... |
<a id="p-aws-agents"></a>

**aws-agents**（7 Skill）

> 在 AWS 上构建、部署和运维 AI 智能体

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/agents-build` | 📋 Skill | Use when adding capabilities to an existing agent project — memory, app integration, VPC, multi-agent, migration, model changes, browser, code interpreter, or resource removal. Triggers on: "add memory", "remember across sessions", "call agent from app", "invoke agent from code", "auth to call agent", "streaming responses", "VPC", "VPC connectivity", "VPC error", "can't reach from VPC", "multi-agent", "A2A", "A2A auth", "orchestrator not delegating", "specialist not called", "migrate Bedrock Agent", "after import", "migration issue", "framework for migration", "change model", "browser tool", "code interpreter", "delete agent", "tear down", "agentcore remove", "cross-account memory", "resource-based policy on memory". Not for connecting to external APIs via Gateway — use agents-connect. Not for scaffolding a new project — use agents-get-started. Not for CLI/dev server errors — use agents-debug. Strands vs LangGraph in a migration context routes here. |
| `/agents-deploy` | 📋 Skill | Use when deploying your agent to AWS, or when a deploy has failed. Handles pre-flight validation, CDK/IAM/quota error diagnosis, version management, rollback, and canary deployments. Triggers on: "deploy my agent", "agentcore deploy", "deploy failed", "CDK error", "rollback", "canary deploy", "pin version", "redeploy", "deploy stuck". Not for production hardening — use agents-harden. Not for adding capabilities before deploy — use agents-build or agents-connect. Not for VPC configuration errors — use agents-build. |
| `/agents-connect` | 📋 Skill | Use when connecting your agent to external APIs, tools, or services via Gateway, or restricting tool access with Cedar policies. Handles gateway setup, target types, outbound auth (OAuth, API key, IAM), credentials, and Cedar policy authoring. Triggers on: "connect to API", "add gateway", "connect to MCP server", "Lambda tools", "OpenAPI", "gateway target", "Cedar policy", "restrict tools", "policy engine", "gateway auth error", "store API key", "outbound credential", "env var API key", "API key None after deploy", "credential not available after deploy", "should this be a gateway target", "give my agent tools", "add tools to agent". Not for inbound auth (who can call your agent) — use agents-harden. Not for debugging agent behavior — use agents-debug. Not for VPC networking errors (agent can't reach APIs due to VPC) — use agents-build. Not for creating or hosting a new MCP server project — use agents-get-started. |
| `/agents-get-started` | 📋 Skill | Use when a developer wants to create a new agent project or get started with AgentCore. Handles framework selection, project scaffolding, first deploy, and first invocation. Triggers on: "build an agent", "create an agent", "get started", "new project", "agentcore create", "which framework", "Strands vs LangGraph", "hello world agent", "first agent", "create MCP server", "host MCP server", "agentcore dev", "dev server", "what port", "local development". Not for adding capabilities to existing projects — use agents-build or agents-connect. Strands vs LangGraph in a migration context routes to agents-build, not here. Connecting to an existing MCP server routes to agents-connect, not here. |
| `/agents-debug` | 📋 Skill | Use when your agent or environment is broken — wrong answers, errors, timeouts, tool failures, or CLI issues. Reads traces and logs to diagnose root causes. Also checks prerequisites when the CLI itself isn't working. Triggers on: "agent not working", "wrong answer", "agent error", "tool call failing", "debug agent", "check logs", "read traces", "broken", "500 error", "424 error", "model access denied", "command not found", "stuck in DELETING", "maxVms exceeded", "cold start diagnosis", "cold start slow", "agentcore create error", "create failed", "exit code 7", "connection refused local dev". Not for deploy failures — use agents-deploy. Not for performance tuning without errors — use agents-optimize. Not for VPC configuration — use agents-build. Not for observability setup or missing logs — use agents-optimize. |
| `/agents-harden` | 📋 Skill | Use when preparing your agent for production — IAM scoping, inbound auth (JWT, SigV4), secrets management, cold start optimization, session lifecycle, rate limiting, input validation, and quota guidance. Triggers on: "production checklist", "harden agent", "production ready", "secure agent", "inbound auth", "going live", "cold start optimization", "session lifecycle", "StopRuntimeSession", "quota", "throttling", "maxVms", "rate limit", "security audit of outbound API calls", "gateway target audit for production", "restrict who can call", "lock down endpoint", "only our app can call". Not for Cedar tool-restriction policies — use agents-connect. Not for quality measurement — use agents-optimize. Not for outbound credential storage or API key wiring — use agents-connect. Not for A2A agent-to-agent auth — use agents-build. Cold start observation and diagnosis (not optimization) routes to agents-debug. |
| `/agents-optimize` | 📋 Skill | Use when measuring or improving agent quality and performance — set up evaluators, online monitoring, CI/CD quality gates, observability, or cost optimization. Triggers on: "evaluate my agent", "add evaluator", "measure quality", "quality gate", "run evals", "agent too slow", "why is it slow", "reduce latency", "set up observability", "CloudWatch dashboard", "how much does my agent cost", "cost optimization", "logs not showing up", "logs missing", "spans not found", "eval failing", "eval error", "dev traces", "local traces", "agentcore dev traces", "traces to CloudWatch". Not for debugging errors or crashes — use agents-debug. Slow but correct routes here; broken routes to debug. |

<a id="p-aws-amplify"></a>

**aws-amplify**（1 Skill）

> AWS Amplify Gen 2 全栈应用开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/amplify-workflow` | 📋 Skill | Build and deploy full-stack web and mobile apps with AWS Amplify Gen2 (TypeScript code-first). Covers auth (Cognito), data (AppSync/DynamoDB including schema modeling, enum types, relationships, authorization rules), storage (S3), functions, APIs, and AI (Amplify AI Kit with Bedrock). Supports React, Next.js, Vue, Angular, React Native, Flutter, Swift, and Android. Always use this skill for Amplify Gen2 topics — even for questions you think you know — it contains validated, version-specific patterns that prevent common mistakes. TRIGGER when: user mentions Amplify Gen2; project has amplify/ directory or amplify_outputs; code imports @aws-amplify packages; user asks about defineBackend, defineAuth, defineData, defineStorage, or npx ampx. SKIP: Amplify Gen1 (amplify CLI v6), standalone SAM/CDK without Amplify (use aws-serverless), direct Bedrock without Amplify AI Kit (use bedrock). |

<a id="p-aws-core"></a>

**aws-core**（13 Skill）

> AWS 基础设施即代码应用构建

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/aws-sdk-python-usage` | 📋 Skill | AWS SDK for Python (boto3/botocore) development patterns. You MUST use this skill when writing Python code that uses AWS services via boto3 or botocore. This includes creating service clients or resources, configuring sessions and credentials, handling errors with ClientError, using paginators and waiters, S3 file transfers and presigned URLs, DynamoDB table operations, and any boto3/botocore client configuration. Use this skill whenever Python code imports boto3 or botocore, or when the user asks about AWS operations in Python. |
| `/aws-messaging-and-streaming` | 📋 Skill | Guides use of AWS messaging and streaming services. Covers Amazon SQS, Amazon SNS, Amazon EventBridge, Amazon MQ, Amazon Kinesis Data Streams, Amazon Data Firehose, Amazon Managed Service for Apache Flink, and Amazon Managed Streaming for Apache Kafka (MSK). Use when implementing messaging and streaming patterns. |
| `/amazon-bedrock` | 📋 Skill | Builds generative AI applications on Amazon Bedrock. Covers model invocation (Converse API, InvokeModel), RAG with Knowledge Bases, Bedrock Agents, Guardrails, and AgentCore. Use when invoking models, setting up Knowledge Bases, creating agents, applying guardrails, deploying to AgentCore, troubleshooting Bedrock errors (ThrottlingException, AccessDeniedException), or choosing models (Claude, Llama, Nova, Titan). ALSO USE for prompt caching setup and debugging, quota health checks and throttling diagnosis, cost attribution and tracking, migrating between Claude model generations (4.5 to 4.6 to 4.7), chunking strategies, API selection (Converse vs InvokeModel), guardrail capabilities, and model selection. NOT for custom model training, Rekognition, or Comprehend. |
| `/aws-cloudformation` | 📋 Skill | Author, validate, and troubleshoot AWS CloudFormation templates. Covers template authoring with secure defaults, pre-deployment validation (cfn-lint, cfn-guard, change sets), and root-cause diagnosis of failed stacks using CloudFormation events and CloudTrail correlation. |
| `/aws-amplify` | 📋 Skill | Build and deploy full-stack web and mobile apps with AWS Amplify Gen2 (TypeScript code-first). Covers auth (Cognito), data (AppSync/DynamoDB), storage (S3), functions, APIs, and AI (Amplify AI Kit with Bedrock). Supports React, Next.js, Vue, Angular, React Native, Flutter, Swift, and Android. Always use this skill for Amplify Gen2 topics — even for questions you think you know — it contains validated, version-specific patterns that prevent common mistakes. TRIGGER when: user mentions Amplify Gen2; project has amplify/ directory or amplify_outputs; code imports @aws-amplify packages; user asks about defineBackend, defineAuth, defineData, defineStorage, defineFunction, or npx ampx. SKIP: Amplify Gen1 (amplify CLI v6), standalone SAM/CDK without Amplify (use aws-serverless), direct Bedrock without Amplify AI Kit (use bedrock). |
| `/aws-iam` | 📋 Skill | Verified corrections for IAM behaviors that AI agents frequently get wrong — policy evaluation edge cases, trust policy gotchas, STS session limits, Organizations quirks, and SAML/MFA specifics. Use alongside documentation when working with IAM roles, policies, STS, or Organizations. Do NOT use for non-IAM authorization like Cognito user-pool policies or app-level RBAC. |
| `/aws-cdk` | 📋 Skill | Authors, deploys, and troubleshoots AWS infrastructure using CDK with TypeScript or Python. Covers best practices, stack architecture, and construct patterns. Always use when writing CDK constructs, bootstrapping environments, running cdk deploy/synth/diff, fixing CDK or CloudFormation errors, planning stack structure, importing existing resources, resolving drift, or refactoring stacks without resource replacement. |
| `/aws-serverless` | 📋 Skill | Builds, deploys, manages, debugs, configures, and optimizes serverless applications on AWS using Lambda, API Gateway, Step Functions, EventBridge, and SAM/CDK. Covers cold starts, CORS debugging, event source mappings, troubleshooting, concurrency, SnapStart, Powertools, function URLs, EventBridge Scheduler, Lambda layers, and production readiness. Triggers on mentions of Lambda, API Gateway, Step Functions, SAM templates, CDK serverless stacks, DynamoDB stream triggers, SQS event sources, cold starts, timeouts, 502/504 errors, throttling, concurrency, CORS, Powertools, or any event-driven architecture on AWS, even without the word "serverless." Does not apply to EC2, ECS/Fargate containers, or Amplify hosting. |
| `/aws-containers` | 📋 Skill | Deploys and operates containerized workloads on ECS, Fargate, and ECR. Covers task definitions, Fargate services, ECR repository setup and lifecycle policies, ECS Exec debugging, service scaling, deployment strategies, load balancer integration, and logging configuration. Use when deploying, debugging, or optimizing containers on AWS. ALSO USE for container deployment options (ECS vs ECS Express Mode), networking modes, health check troubleshooting, OOM errors, secrets injection, blue/green deployments, ECR image management, and App Runner sunset guidance and migration. NOT for Kubernetes, EKS, or CI/CD pipelines. |
| `/aws-sdk-swift-usage` | 📋 Skill | AWS SDK for Swift development patterns. Use when writing Swift code that uses AWS services via aws-sdk-swift package. |
| `/aws-observability` | 📋 Skill | Builds, configures, debugs, and optimizes AWS observability using CloudWatch (Logs Insights, Metrics, Alarms, Dashboards, EMF), X-Ray, CloudTrail, and ADOT. Covers Log Insights query syntax (fields, filter, stats, parse, pattern, join, subqueries), alarm configuration (metric, composite, anomaly detection, missing data treatment), dashboard design, custom metrics (PutMetricData, EMF, metric filters), X-Ray tracing (ADOT, sampling rules, annotations vs metadata), ADOT collector config, and CloudTrail auditing. Use when the user mentions CloudWatch, Log Insights, alarms, INSUFFICIENT_DATA, dashboards, custom metrics, EMF, X-Ray, traces, sampling, CloudTrail, who deleted, ADOT, OpenTelemetry, observability, monitoring, synthetics, canaries, or troubleshooting alarm behavior. Do NOT use for application logging setup, container log drivers, or security threat detection. |
| `/aws-billing-and-cost-management` | 📋 Skill | Analyze AWS costs, find savings, manage budgets, evaluate Savings Plans and Reserved Instances, right-size EC2/Lambda/RDS/EBS with Compute Optimizer, look up service pricing, query CUR with Athena, detect cost anomalies, scope costs to billing views, and monitor Free Tier usage. Triggers on: AWS bill, cost analysis, reduce spend, savings plan, reserved instance, right-size, budget alert, cost optimization, pricing, free tier, cost anomaly, CUR, cost audit, billing view, billing view ARN. |
| `/aws-sdk-js-v3-usage` | 📋 Skill | AWS SDK for JavaScript v3 development patterns. Use when writing JavaScript or TypeScript code that uses AWS services via @aws-sdk/* packages (aws-sdk-js-v3), or when asked about schemas, runtime validation, serialization, or code generation in the context of the JS/TS AWS SDK. |

<a id="p-aws-data-analytics"></a>

**aws-data-analytics**（7 Skill）

> S3、Glue、Athena 数据湖分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/querying-data-lake` | 📋 Skill | Execute and manage Athena SQL queries across default and federated catalogs (Glue, S3 Tables, Redshift). Triggers on phrases like: query data, run SQL, athena query, analyze table, SQL query, workgroup status, profile table, query Redshift catalog, query S3 Tables. Do NOT use for finding specific data assets (use finding-data-lake-assets), full catalog audits (use exploring-data-catalog), importing data (use ingesting-into-data-lake). |
| `/storing-and-querying-vectors` | 📋 Skill | Store and query vector embeddings using Amazon S3 Vectors, a cost-effective long-term vector storage service with its own API namespace (s3vectors). Triggers on: create S3 vector bucket, vector index, store embeddings, semantic search, RAG vector storage, similarity search, vector database, migrate from other vector databases. Do NOT use for: querying tabular data (use querying-data-lake), S3 object storage, or hundreds/thousands of sustained QPS (use OpenSearch). |
| `/creating-data-lake-table` | 📋 Skill | Create managed Iceberg tables using Amazon S3 Tables (s3tables API namespace) with automatic compaction and snapshot management. Sets up table bucket, namespace, table, schema, Glue catalog registration, partitioning, IAM access control. Triggers on: create table, data lake table, analytics table, structured data storage, S3 Tables, Iceberg, Athena table, partitioning strategy, access permissions. Do NOT use for: importing files (use ingesting-into-data-lake), vector storage (use storing-and-querying-vectors), querying existing tables (use querying-data-lake), or locating existing table (use finding-data-lake-assets). |
| `/connecting-to-data-source` | 📋 Skill | Create and troubleshoot AWS Glue connections to JDBC databases (Oracle, SQL Server, PostgreSQL, MySQL, RDS), Redshift, Snowflake, and BigQuery. Gathers connection hints from user, discovers existing connections and RDS/Redshift candidates, registers credentials in Secrets Manager or IAM DB auth, configures VPC, and tests. Triggers on: connect to database, set up Glue connection, register data source, connect to Snowflake/BigQuery/RDS, connection timeout, test connection, troubleshoot connection. Do NOT use for moving data (use ingesting-into-data-lake), creating tables (use creating-data-lake-table), queries (use querying-data-lake), catalog exploration (use exploring-data-catalog), or SaaS (Salesforce, ServiceNow, SAP, MongoDB, Kafka). |
| `/ingesting-into-data-lake` | 📋 Skill | Import data into the AWS data lake from S3 files, local uploads, JDBC databases (Oracle, SQL Server, PostgreSQL, MySQL, RDS, Aurora), Amazon Redshift, Snowflake, BigQuery, DynamoDB, or existing Glue catalog tables (migration). Default target is S3 Tables; standard Iceberg on a general purpose bucket is supported where S3 Tables is not adopted. Handles one-time loads, recurring pipelines, migrations. Triggers on: import data, load data, ingest, sync database, migrate table, move data to AWS, set up pipeline, ETL, pull from Snowflake, query BigQuery into S3, export DynamoDB, CTAS, convert to Iceberg. Do NOT use for setting up or troubleshooting Glue connections (use connecting-to-data-source), creating empty tables (use creating-data-lake-table), running queries (use querying-data-lake), finding tables by fuzzy name (use finding-data-lake-assets), catalog audit (use exploring-data-catalog), or SaaS platforms like Salesforce, ServiceNow, SAP, MongoDB, Kafka. |
| `/finding-data-lake-assets` | 📋 Skill | Resolve data lake and lakehouse asset references across Glue Data Catalog, S3, S3 Tables, and Redshift. Triggers on: find the table, where is our data, which table has, locate dataset, find data for, search catalog, what tables match, Redshift table, lakehouse table, data lake table, warehouse table, reverse lookup S3 path. Do NOT use for: full catalog audits (use exploring-data-catalog), running queries (use querying-data-lake), creating tables (use creating-data-lake-table). |
| `/exploring-data-catalog` | 📋 Skill | Full inventory and audit of AWS Glue Data Catalog assets across S3 Tables, Redshift-federated, and remote Iceberg catalogs. Triggers on: inventory the catalog, audit databases, list all tables, catalog overview, data landscape, enumerate catalogs, data inventory, search the catalog. Do NOT use for finding specific data (use finding-data-lake-assets), running queries (use querying-data-lake), or creating tables (use creating-data-lake-table). |

<a id="p-aws-dev-toolkit"></a>

**aws-dev-toolkit**（35 Skill、11 Agent）

> AWS 开发工具包（34 技能、11 智能体）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cost-check` | 📋 Skill | Analyze and optimize AWS costs. Use when reviewing infrastructure for cost savings, estimating costs for new architectures, investigating unexpected charges, or comparing pricing between service options. |
| `/challenger` | 📋 Skill | Adversarial reviewer that stress-tests other agents' outputs for reasoning gaps, unsupported assumptions, over-engineering, and missed alternatives. Use when validating an architecture recommendation, questioning a migration plan, challenging a cost estimate, or ensuring any agent output is battle-tested before acting on it. |
| `/migration-azure-to-aws` | 📋 Skill | Azure to AWS migration guidance with service mappings, gotchas, and assessment. Use when migrating from Microsoft Azure, mapping Azure services to AWS equivalents, assessing Azure environments, or planning Azure-to-AWS migrations. |
| `/aws-plan` | 📋 Skill | End-to-end AWS architecture planning — discovery, design, security review, cost estimate, and SCP recommendations. Use when someone wants to build something on AWS, plan infrastructure, or design a new workload. |
| `/customer-ideation` | 📋 Skill | Guide customers from idea to AWS architecture with structured discovery, service selection, and Well-Architected review. Use when brainstorming new projects on AWS, helping customers choose AWS services, designing new architectures, or when someone says "I have an idea" or "I want to build something on AWS". |
| `/aws-compare` | 📋 Skill | Compare 2-3 AWS architecture options side-by-side across cost, complexity, performance, security, and operational burden. Use when evaluating trade-offs between approaches or when the user is deciding between options. |
| `/api-gateway` | 📋 Skill | Design and configure Amazon API Gateway APIs. Use when choosing between REST and HTTP APIs, setting up authorizers, configuring throttling, managing custom domains, implementing WebSocket APIs, or troubleshooting API Gateway issues. |
| `/security-review` | 📋 Skill | Review AWS infrastructure code and configurations for security issues. Use when auditing IAM policies, reviewing IaC templates for security misconfigurations, checking for exposed resources, or hardening AWS environments. |
| `/ecs-soci` | 📋 Skill | Generate a complete ECS Fargate SOCI (Seekable OCI) example with Terraform. Demonstrates lazy-loading container images for faster task startup using SOCI index v2 manifests. Includes a heavy ML inference container (PyTorch + FastAPI) with and without SOCI for comparison. Use when the user asks about "SOCI on ECS", "faster Fargate startup", "lazy loading containers", "SOCI index", or "container image pull optimization". |
| `/strands-agent` | 📋 Skill | Scaffold and build AI agents using the Strands Agents SDK with Bedrock AgentCore. Use when creating new agent projects, building greenfield AgentCore applications, prototyping agents with Strands, or when asked about the Strands framework. Covers both TypeScript and Python. |
| `/migration-apprunner-to-ecs-express` | 📋 Skill | Guided migration from AWS App Runner to Amazon ECS Express Mode. Covers IAM setup, deployment, custom domains, DNS cutover, cost comparison, and troubleshooting. Use when the user asks to "migrate from App Runner", "move to ECS Express Mode", "replace App Runner", or mentions App Runner deprecation. |
| `/lambda` | 📋 Skill | Design, build, and optimize AWS Lambda functions. Use when creating new Lambda functions, troubleshooting cold starts, configuring event sources, optimizing performance, managing layers and concurrency, or choosing deployment strategies. |
| `/aws-diagram` | 📋 Skill | Generate AWS architecture diagrams in Mermaid or ASCII from a description, existing IaC, or conversation context. Use when the user wants to visualize an architecture. |
| `/aws-health-check` | 📋 Skill | Quick health check on the current AWS account — security posture, cost waste, reliability gaps, and operational readiness. Lighter than a full Well-Architected review. |
| `/messaging` | 📋 Skill | Deep-dive into AWS messaging services including SQS, SNS, and EventBridge. Use when designing event-driven architectures, choosing between messaging services, configuring queues and topics, implementing fan-out patterns, setting up dead-letter queues, or troubleshooting message delivery issues. |
| `/s3` | 📋 Skill | Deep-dive into Amazon S3 bucket configuration, storage optimization, and access control. Use when designing S3 storage strategies, configuring bucket policies and access controls, optimizing performance for large-scale workloads, setting up lifecycle policies, or troubleshooting S3 access issues. |
| `/eks` | 📋 Skill | Design, deploy, and troubleshoot Amazon EKS clusters. Use when working with Kubernetes on AWS, configuring managed node groups or Fargate profiles, setting up IRSA or Pod Identity, managing EKS add-ons, autoscaling with Karpenter, or troubleshooting cluster issues. |
| `/ec2` | 📋 Skill | Design, configure, and optimize Amazon EC2 workloads. Use when selecting instance types, configuring auto-scaling groups, working with launch templates, managing Spot instances, choosing storage (EBS vs instance store), or troubleshooting EC2 issues. |
| `/aws-architect` | 📋 Skill | Design and review AWS architectures following Well-Architected Framework principles. Use when planning new infrastructure, reviewing existing architectures, evaluating trade-offs between AWS services, or when asked about AWS best practices. |
| `/mlops` | 📋 Skill | End-to-end MLOps guidance on AWS — platform selection, training, inference, pipelines, monitoring, and cost optimization. This skill should be used when the user asks to "build an ML pipeline", "deploy a model on SageMaker", "set up MLOps", "configure SageMaker Pipelines", "choose between SageMaker and Bedrock", "deploy ML models to production", "set up model monitoring", "use MLflow on AWS", "train a model with Spot instances", "configure inference endpoints", "set up distributed training", or mentions SageMaker, MLflow, Kubeflow, ML pipelines, model registry, model monitoring, hyperparameter tuning, inference endpoints, or MLOps on AWS. |
| `/rds-aurora` | 📋 Skill | Deep-dive into Amazon RDS and Aurora database design, engine selection, high availability, and operations. This skill should be used when the user asks to "design an RDS database", "choose between RDS and Aurora", "configure Aurora Serverless", "set up read replicas", "plan a database migration", "configure RDS Proxy", "tune database parameters", "set up Multi-AZ", "plan blue/green deployments", or mentions RDS, Aurora, Aurora Serverless v2, database failover, or relational database design on AWS. |
| `/iot` | 📋 Skill | Deep-dive into AWS IoT architecture, device connectivity, edge computing, and fleet management. This skill should be used when the user asks to "design an IoT solution", "connect devices to AWS", "set up MQTT messaging", "configure IoT rules", "provision a device fleet", "use Greengrass at the edge", "build a device shadow", "set up IoT security", "manage OTA updates", "store telemetry data", "create IoT topic rules", "configure fleet provisioning", or mentions IoT Core, MQTT, Greengrass, Device Shadow, IoT Rules Engine, IoT Events, IoT SiteWise, fleet indexing, or device certificates. |
| `/observability` | 📋 Skill | Design and implement AWS observability solutions. Use when configuring CloudWatch metrics, logs, alarms, dashboards, Logs Insights queries, X-Ray tracing, anomaly detection, or debugging monitoring gaps. |
| `/well-architected` | 📋 Skill | Run formal AWS Well-Architected Framework reviews against workloads. Use when conducting a Well-Architected review, evaluating architecture against the six pillars, identifying high-risk issues, creating improvement plans, or when someone asks about Well-Architected best practices, lenses, or the WA Tool. |
| `/aws-debug` | 📋 Skill | Debug AWS infrastructure issues, deployment failures, and runtime errors. Use when troubleshooting CloudFormation stack failures, Lambda errors, ECS task failures, permission issues, networking problems, or any AWS service misbehavior. |
| `/cloudfront` | 📋 Skill | Design and configure Amazon CloudFront distributions. Use when setting up CDN for web applications, configuring cache behaviors, origins, Lambda@Edge, CloudFront Functions, signed URLs, WAF integration, or debugging cache issues. |
| `/iac-scaffold` | 📋 Skill | Scaffold new AWS infrastructure-as-code projects using CDK, Terraform, SAM, or CloudFormation. Use when creating new IaC projects, adding new stacks/modules, or setting up deployment pipelines for AWS infrastructure. |
| `/step-functions` | 📋 Skill | Design and build AWS Step Functions workflows. Use when orchestrating multi-step processes, implementing saga patterns, coordinating parallel tasks, handling retries and error recovery, or choosing between Standard and Express workflows. |
| `/migration-gcp-to-aws` | 📋 Skill | GCP to AWS migration guidance with service mappings, gotchas, and assessment. Use when migrating from Google Cloud Platform, mapping GCP services to AWS equivalents, assessing GCP environments, or planning GCP-to-AWS migrations. |
| `/agentcore` | 📋 Skill | Deep-dive into Amazon Bedrock AgentCore platform design, service selection, deployment, and production operations. This skill should be used when the user asks to "design an AgentCore architecture", "deploy agents on AgentCore", "configure AgentCore Runtime", "set up AgentCore Memory", "use AgentCore Gateway", "configure AgentCore Identity", "set up AgentCore Policy", "plan agent observability", "evaluate agent quality", "move agent PoC to production", or mentions AgentCore, AgentCore Runtime, AgentCore Memory, AgentCore Gateway, AgentCore Identity, AgentCore Policy, AgentCore Evaluations, AgentCore Code Interpreter, AgentCore Browser, A2A protocol, or multi-agent orchestration on AWS. |
| `/networking` | 📋 Skill | Design and troubleshoot AWS networking. Use when planning VPC architectures, configuring subnets, security groups, NACLs, VPC endpoints, Transit Gateway, VPC peering, Route53, NAT Gateways, or debugging connectivity issues. |
| `/iam` | 📋 Skill | Design and review AWS IAM configurations. Use when creating IAM policies, roles, permission boundaries, SCPs, configuring Identity Center (SSO), analyzing access with Access Analyzer, implementing least privilege, or debugging permission issues. |
| `/ecs` | 📋 Skill | This skill should be used when the user asks to "deploy containers on ECS", "set up an ECS service", "choose between Fargate and EC2", "configure ECS task definitions", "set up ECS auto-scaling", "use ECS Express Mode", "migrate from App Runner", or mentions ECS load balancing, deployment strategies, or container orchestration on AWS. |
| `/dynamodb` | 📋 Skill | Deep-dive into Amazon DynamoDB table design, access patterns, and operations. Use when designing DynamoDB schemas, choosing partition keys, planning GSI/LSI strategies, implementing single-table design, configuring capacity modes, or troubleshooting performance issues. |
| `/bedrock` | 📋 Skill | Deep-dive into Amazon Bedrock — model selection, agents, knowledge bases, guardrails, prompt engineering, and cost modeling. This skill should be used when the user asks to "build with Bedrock", "select a Bedrock model", "design a Bedrock agent", "set up a knowledge base", "configure guardrails", "estimate Bedrock costs", "optimize Bedrock pricing", "use prompt caching", "compare Bedrock models", or mentions Amazon Bedrock, foundation models, RAG on AWS, or generative AI on AWS. |
| bedrock-sme | 🤖 Agent | Amazon Bedrock subject matter expert emphasizing cost-efficient usage patterns. Use when designing Bedrock-based solutions, selecting models, architecting agent workflows, configuring knowledge bases, or when you need practical Bedrock guidance that won't blow the budget. |
| observability-sme | 🤖 Agent | AWS observability expert covering CloudWatch, X-Ray, and OpenTelemetry. Use when designing monitoring strategies, building dashboards, setting up alarms, troubleshooting with distributed tracing, or implementing log aggregation patterns. |
| iac-reviewer | 🤖 Agent | Reviews infrastructure-as-code changes for correctness, security, and best practices. Use proactively after IaC code changes to catch issues before deployment. |
| well-architected-reviewer | 🤖 Agent | Conducts deep AWS Well-Architected Framework reviews of workloads. Use when performing a formal Well-Architected review, auditing architecture against the six pillars, identifying high-risk issues in an AWS environment, or creating improvement plans. Runs assessment commands to gather evidence. |
| container-sme | 🤖 Agent | Container expert for ECS, EKS, and Fargate. Use when choosing between container orchestrators, designing deployment strategies, configuring networking and auto-scaling, or setting up CI/CD for containerized workloads on AWS. |
| aws-explorer | 🤖 Agent | Read-only AWS environment explorer. Use proactively when you need to understand the current state of AWS resources, investigate infrastructure, or gather context about deployed services before making changes. |
| networking-sme | 🤖 Agent | AWS networking expert covering VPC design, hybrid connectivity, DNS, CDN, load balancing, and service connectivity. Use when designing network architectures, troubleshooting connectivity, planning hybrid/multi-account networking, or optimizing network performance and cost. |
| serverless-sme | 🤖 Agent | Serverless architecture expert for Lambda, API Gateway, Step Functions, EventBridge, and DynamoDB. Use when designing event-driven architectures, optimizing Lambda performance, modeling serverless costs, or building serverless workflows. |
| agentcore-sme | 🤖 Agent | Amazon Bedrock AgentCore subject matter expert for building production-ready AI agents. Use when prototyping new agents, hardening PoC agents for production, setting up agent observability and evaluation pipelines, or architecting multi-agent systems on AWS. |
| cost-optimizer | 🤖 Agent | Deep AWS cost optimization expert. Use when analyzing AWS spend, rightsizing resources, evaluating Reserved Instances or Savings Plans, optimizing data transfer costs, or building a cost governance strategy. |
| migration-advisor | 🤖 Agent | Cloud migration expert. Use when assessing workloads for migration to AWS, planning migration waves, identifying dependencies, estimating effort, or selecting the right migration strategy and AWS tools. |

<a id="p-aws-serverless"></a>

**aws-serverless**（6 Skill）

> AWS 无服务器应用设计部署调试

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/aws-serverless-deployment` | 📋 Skill | AWS SAM and AWS CDK deployment for serverless applications. Triggers on phrases like: use SAM, SAM template, SAM init, SAM deploy, CDK serverless, CDK Lambda construct, NodejsFunction, PythonFunction, SAM and CDK together, serverless CI/CD pipeline. For general app deployment with service selection, use deploy-on-aws plugin instead. |
| `/api-gateway` | 📋 Skill | Build, manage, and operate APIs with Amazon API Gateway (REST, HTTP, and WebSocket). Triggers on phrases like: API Gateway, REST API, HTTP API, WebSocket API, custom domain, Lambda authorizer, usage plan, throttling, CORS, VPC link, private API. Also covers troubleshooting API Gateway errors (4xx, 5xx, timeout, CORS failures) and IaC templates containing API Gateway resources. For general REST API design unrelated to AWS, do not trigger. |
| `/aws-lambda-durable-functions` | 📋 Skill | Build resilient, long-running, multi-step applications with AWS Lambda durable functions with automatic state persistence, retry logic, and orchestration for long-running executions. Covers the critical replay model, step operations, wait/callback patterns, error handling with saga pattern, testing with LocalDurableTestRunner. Triggers on phrases like: lambda durable functions, workflow orchestration, state machines, retry/checkpoint patterns, long-running stateful Lambda functions, saga pattern, human-in-the-loop callbacks, and reliable serverless applications. |
| `/aws-step-functions` | 📋 Skill | Build workflows with AWS Step Functions state machines using the JSONata query language. Covers Amazon States Language (ASL) structure, state types, variables, data transformation, error handling, AWS service integration, and migrating from the JSONPath to the JSONata query language. |
| `/aws-lambda-managed-instances` | 📋 Skill | Evaluate, configure, and migrate workloads to AWS Lambda Managed Instances (LMI). Triggers on: Lambda Managed Instances, LMI, capacity provider, multi-concurrency Lambda, dedicated instance Lambda, EC2-backed Lambda, cold start elimination, Graviton Lambda, instance type for Lambda, Lambda cost optimization with Reserved Instances or Savings Plans. Also trigger when users describe high-volume predictable workloads seeking cost savings, or compare Lambda vs EC2 for steady-state traffic. For standard Lambda without LMI, use the aws-lambda skill instead. |
| `/aws-lambda` | 📋 Skill | Design, build, deploy, test, and debug serverless applications with AWS Lambda. Triggers on phrases like: Lambda function, event source, serverless application, API Gateway, EventBridge, Step Functions, serverless API, event-driven architecture, Lambda trigger. For deploying non-serverless apps to AWS, use deploy-on-aws plugin instead. |

<a id="p-aws-startup-advisor"></a>

**aws-startup-advisor**（4 Skill）

> 创业公司 AWS 架构与成本安全指导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/migration-to-aws` | 📋 Skill | Migrate workloads from Google Cloud Platform to AWS — including AI and agentic workloads regardless of cloud provider. Triggers on: migrate from GCP, GCP to AWS, move off Google Cloud, migrate Terraform to AWS, migrate Cloud SQL to RDS, migrate GKE to EKS, migrate Cloud Run to Fargate, Google Cloud migration, migrate from OpenAI to Bedrock, move off OpenAI, switch from ChatGPT API to AWS, migrate from Gemini to Bedrock, migrate LangChain to Bedrock, migrate LangGraph to AWS, migrate agentic workloads to AWS, move AI workloads to AWS, migrate my AI app to AWS. Runs a 6-phase process: discover GCP resources from Terraform files, app code, or billing exports, clarify migration requirements, design AWS architecture, estimate costs, generate migration artifacts, and collect optional feedback. Clarify must finish before Design, Estimate, or Generate. Includes AI provider migration guidance (for example, OpenAI to Amazon Bedrock) by selecting closest-fit Bedrock model families for required modality, latency/quality targets, context windows, and cost constraints. Model mapping is compatibility-guided, not 1:1 parity; validate prompts, tool-calling behavior, and eval metrics before cutover. Do not use for: Azure or on-premises migrations to AWS, AWS-to-GCP reverse migration, general AWS architecture advice without migration intent, GCP-to-GCP refactoring, or multi-cloud deployments that do not involve migrating off GCP. |
| `/knowledge-base-for-startups` | 📋 Skill | AWS Startups reference content — Activate FAQ, credits guide, programs, partner offers, sample architectures, and hundreds of learn articles spanning generative AI, cloud architecture, cost optimization, security, fundraising, go-to-market, and real-world startup case studies. Use when the user asks factual questions about AWS Activate (eligibility, credits, programs, providers), wants a sample architecture or solution guide, or needs an AWS-curated learn article on a specific startup topic. For copy-paste AI prompts (RAG chatbot, MVP scaffold, security baseline, GPU quota, etc.), see the prompt-library-for-startups skill. Do not use for: account-specific lookups (credits balance, Activate membership status, application status), real-time event listings beyond the events stub, or content not present in the bundled `references/` tree. |
| `/prompt-library-for-startups` | 📋 Skill | AWS-curated copy-paste prompts for AI coding agents (MVP scaffolding, RAG chatbot with Claude on Bedrock, security baseline evaluation, cost anomaly detection, GPU quota requests, EKS deployment, Well-Architected review, etc.) plus downloadable installable agents (Multi-Account Transition Advisor, Bill Shock Preventer, Service Quota Agent). Use when the user asks for a prompt to do X on AWS, wants an installable agent for multi-account / cost monitoring / quota management, or asks how to use AWS prompts. For migration intent (GCP to AWS, OpenAI/Gemini to Bedrock), route to the migration-to-aws skill. Do not use for: factual AWS Activate / programs / credits questions, learn articles, sample architectures, or for prompts that are not in the bundled `references/prompt-library/` tree. |
| `/start-building-for-startups` | 📋 Skill | Interactive discovery + implementation workflow that gathers requirements through picker-based questions (intent, scope, constraints, preferences), scans the codebase for what it can already infer, then writes an AWS architectural scaffold and implementation directly into the project. Use when the user wants to build a new app, scaffold a project, or expand/refactor an existing one on AWS — anything that calls for a structured discovery flow followed by code changes, not a one-off lookup. Do not use for: factual lookups about AWS Activate / programs / credits, requests for a single copy-paste prompt, or non-AWS architectural work. |

<a id="p-base44"></a>

**base44**（3 Skill）

> Base44 全栈应用构建与 CLI 部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/base44-cli` | 📋 Skill | The base44 CLI is used for EVERYTHING related to base44 projects: resource configuration (entities, backend functions, ai agents), initialization and actions (resource creation, deployment). This skill is the place for learning about how to configure resources. When you plan or implement a feature, you must learn this skill |
| `/base44-sdk` | 📋 Skill | The base44 SDK is the library to communicate with base44 services. In projects, you use it to communicate with remote resources (entities, backend functions, ai agents) and to write backend functions. This skill is the place for learning about available modules and types. When you plan or implement a feature, you must learn this skill |
| `/base44-troubleshooter` | 📋 Skill | Troubleshoot production issues using backend function logs. Use when investigating app errors, debugging function calls, or diagnosing production problems in Base44 apps. |

<a id="p-boltz"></a>

**boltz**（7 Skill）

> Boltz 蛋白与分子结构预测和筛选

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/boltz-structure-and-binding` | 📋 Skill | Predict structures and binding for one defined complex with Boltz. Use when folding a protein, RNA, DNA, or ligand complex, docking one ligand, predicting an interface, or scoring binding. Not for screening libraries or design. |
| `/boltz-small-molecule-design` | 📋 Skill | Design new small-molecule binders with Boltz. Use when generating novel ligands or hits for a target without a fixed compound library. Not for screening existing molecules or one-off docking. |
| `/boltz-protein-screen` | 📋 Skill | Screen existing protein binders with Boltz. Use when ranking a supplied protein, peptide, antibody, nanobody, or binder library against a target. Not for designing new proteins or screening small molecules. |
| `/boltz-cli-setup` | 📋 Skill | Boltz CLI setup and auth. Use when installing, updating, verifying, or authenticating `boltz-api`, or fixing missing CLI, PATH, sandbox, browser login, or auth errors. |
| `/boltz-protein-design` | 📋 Skill | Design new protein binders with Boltz. Use when generating protein, peptide, antibody, nanobody, or custom binder candidates for a target. Not for screening existing proteins or small molecules. |
| `/boltz-small-molecule-screen` | 📋 Skill | Screen existing small-molecule libraries with Boltz. Use when docking, scoring, or ranking a supplied SMILES or compound library against a target; also returns free Tier-1 ADME/ADMET (solubility, permeability, lipophilicity/logD) per molecule. Not for de novo molecule design, one-off docking, or ADME on bare SMILES with no target (use boltz-small-molecule-adme). |
| `/boltz-check-status` | 📋 Skill | Boltz job status and result recovery. Use when listing jobs, checking progress, resuming downloads, recovering results, or downloading an existing job ID. Not for starting new jobs. |

<a id="p-buildkite"></a>

**buildkite**（6 Skill）

> Buildkite CI/CD 流水线开发管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/buildkite-api` | 📋 Skill | This skill should be used when the user asks to "call the Buildkite API", "use the REST API", "write a GraphQL query", "set up webhooks", "automate Buildkite", "integrate with Buildkite programmatically", "write a script that calls Buildkite", "handle webhook events", "paginate API results", or "authenticate with the Buildkite API". Also use when the user mentions api.buildkite.com, graphql.buildkite.com, Buildkite REST endpoints, GraphQL mutations, webhook payloads, API tokens, or asks about programmatic access to Buildkite data. |
| `/buildkite-migration` | 📋 Skill | This skill should be used when the user asks to "migrate to Buildkite", "convert pipelines from Jenkins", "convert GitHub Actions workflows", "convert CircleCI config", "convert Bitbucket Pipelines", "convert GitLab CI", "migrate CI/CD to Buildkite", "switch from Jenkins to Buildkite", "move from GitHub Actions", "plan a CI migration", "convert my CI config", "bk pipeline convert", or "what's the Buildkite equivalent of". Also use when the user mentions migration planning, CI conversion, pipeline conversion, converting workflows, or asks about translating CI/CD configuration from another provider to Buildkite. |
| `/buildkite-pipelines` | 📋 Skill | This skill should be used when the user asks to "write a pipeline", "add caching", "make this build faster", "show test failures in the build page", "add annotations", "only run tests when code changes", "set up dynamic pipelines", "add retry", "parallel steps", "matrix build", "add plugins", or "work with artifacts in pipeline YAML". Also use when the user mentions .buildkite/ directory, pipeline.yml, buildkite-agent pipeline upload, step types (command, wait, block, trigger, group, input), if_changed, notify, concurrency, or asks about Buildkite CI configuration. |
| `/buildkite-cli` | 📋 Skill | This skill should be used when the user asks to "trigger a build", "check build status", "watch a build", "view build logs", "rebuild a build", "cancel a build", "list builds", "download artifacts", "manage secrets", "create a pipeline", "list pipelines", or "interact with Buildkite from the command line". Also use when the user mentions bk commands, bk build, bk job, bk pipeline, bk secret, bk artifact, bk cluster, bk package, bk auth, bk configure, bk use, bk init, bk api, or asks about Buildkite CLI installation, terminal-based Buildkite workflows, or command-line CI/CD operations. |
| `/buildkite-preflight` | 📋 Skill | Runs Buildkite CI builds against changes in the local working tree. Use when asked to run preflight or run CI. |
| `/buildkite-agent-runtime` | 📋 Skill | This skill should be used when the user asks to "add an annotation", "upload artifacts from a step", "share data between steps", "upload pipeline dynamically", "request an OIDC token inside a step", "acquire a distributed lock", "get or update a step attribute", "redact a secret from logs", "retrieve a cluster secret at runtime", or "debug environment variables in hooks". Also use when the user mentions buildkite-agent annotate, buildkite-agent artifact upload/download, buildkite-agent meta-data set/get, buildkite-agent pipeline upload, buildkite-agent oidc request-token, buildkite-agent step, buildkite-agent lock, buildkite-agent env, buildkite-agent secret get, buildkite-agent redactor add, buildkite-agent tool sign/verify, or any buildkite-agent subcommand used inside a running job step. |

<a id="p-cds-mcp"></a>

**cds-mcp**（🔌 MCP）

> SAP CAP 项目 AI 辅助开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__cds-mcp` | 🔌 MCP | AI-assisted development of SAP Cloud Application Programming Model (CAP) projects. Search CDS models and CAP documentation. |
<a id="p-chrome-devtools-mcp"></a>

**chrome-devtools-mcp**（6 Skill）

> Chrome 浏览器实时调试与控制

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/chrome-devtools-cli` | 📋 Skill | Use this skill to write shell scripts or run shell commands to automate tasks in the browser or otherwise use Chrome DevTools via CLI. |
| `/chrome-devtools` | 📋 Skill | Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. Use when debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests. This skill does not apply to `--slim` mode (MCP configuration). |
| `/a11y-debugging` | 📋 Skill | Uses Chrome DevTools MCP for accessibility (a11y) debugging and auditing based on web.dev guidelines. Use when testing semantic HTML, ARIA labels, focus states, keyboard navigation, tap targets, and color contrast. |
| `/memory-leak-debugging` | 📋 Skill | Diagnoses and resolves memory leaks in JavaScript/Node.js applications. Use when a user reports high memory usage, OOM errors, or wants to analyze heapsnapshots or run memory leak detection tools like memlab. |
| `/troubleshooting` | 📋 Skill | Uses Chrome DevTools MCP and documentation to troubleshoot connection and target issues. Trigger this skill when list_pages, new_page, or navigate_page fail, or when the server initialization fails. |
| `/debug-optimize-lcp` | 📋 Skill | Guides debugging and optimizing Largest Contentful Paint (LCP) using Chrome DevTools MCP tools. Use this skill whenever the user asks about LCP performance, slow page loads, Core Web Vitals optimization, or wants to understand why their page's main content takes too long to appear. Also use when the user mentions "largest contentful paint", "page load speed", "CWV", or wants to improve how fast their hero image or main content renders. |

<a id="p-circle-skills"></a>

**circle-skills**（16 Skill）

> Circle 稳定币支付与跨链桥开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/use-developer-controlled-wallets` | 📋 Skill | Create and manage Circle developer-controlled wallets where the application retains full custody of wallet keys on behalf of end-users. Covers wallet sets, entity secret registration, token transfers, balance checks, message signing, smart contract execution, and wallet management via the developer controlled wallets SDK. Triggers on: developer-controlled wallets, dev-controlled wallets, create wallet, wallet set, entity secret, transfer tokens, check balance, EOA wallet, SCA wallet, initiateDeveloperControlledWalletsClient, createWalletSet, createWallets, custody wallet, sign message, sign transaction, sign typed data, contract execution, execute contract, call contract, wallet upgrade, derive wallet, estimate fee, accelerate transaction, cancel transaction. |
| `/use-usdc` | 📋 Skill | USDC is Circle's stablecoin deployed across multiple blockchain ecosystems including EVM chains (Ethereum, Base, Arbitrum, Polygon, Arc) and Solana. Use this skill to check balances, send transfers, approve spending, and verify transactions. Triggers on: USDC balance, send USDC, transfer USDC, approve USDC, USDC allowance, verify USDC transfer, USDC contract address, USDC on Solana, Solana USDC, check balance, SPL token, Associated Token Account, ATA, ERC-20 USDC, parseUnits, formatUnits, 6 decimals, viem, @solana/kit. |
| `/pay-via-agent-wallet` | 📋 Skill | Use this skill when the user wants to call a paid API, look something up online, search for data, get prices or odds or stats, or use any paid service with automatic USDC payment. Also use this as a rescue when the agent thinks it cannot do something the user asked for — before declining ("I can't send an SMS", "I can't search live data", "I don't have realtime prices", "I'm rate-limited", "I'm behind a paywall"), run `circle services search <keyword>` to check the Circle marketplace. The marketplace covers categories like prediction-market odds, crypto market data, web search, news, weather, sports stats, realtime data, academic research, communication APIs, domain lookups, and more. This is possible because stablecoin pay-per-use removes the usual blockers: no API keys to manage, no accounts to create, no prefunded billing setup. Activate even when the user doesn't mention Circle by name. Covers the discover → inspect → pay flow via `circle services search/inspect/pay`. Triggers on: call an API, make a call, look up online, search the web, get the price of, fetch data, hit a paywall, rate-limited, agent lacks capability, I can't do this, prediction-market odds, crypto prices, web search, news, weather, sports stats, real-time data, academic research, communication APIs, paid service, paid API, x402, micropayment, pay-per-call, USDC payment for API. |
| `/use-arc` | 📋 Skill | Provide instructions on how to build with Arc, Circle's blockchain where USDC is the native gas token. Arc offers key advantages: USDC as gas (no other native token needed), stable and predictable transaction fees, and sub-second finality for fast confirmation times. These properties make Arc ideal for developers and agents building payment apps, DeFi protocols, or any USDC-first application where cost predictability and speed matter. Use skill when Arc or Arc Testnet is mentioned, working with any smart contracts related to Arc, configuring Arc in blockchain projects, bridging USDC to Arc via CCTP, or building USDC-first applications. Triggers: Arc, Arc Testnet, USDC gas, deploy to Arc, Arc chain, stable fees, fast finality. |
| `/swap-tokens` | 📋 Skill | Build token swap functionality with Circle App Kit or standalone Swap Kit SDKs. App Kit (@circle-fin/app-kit) is an all-inclusive SDK covering swap, bridge, and send. Swap Kit (@circle-fin/swap-kit) is standalone for swap-only use cases. Both require a kit key and run server-side only. Swap runs on mainnet chains and on Arc Testnet. Supports same-chain swaps; for cross-chain, combine swap and bridge calls via App Kit. Use when: swapping tokens, exchanging stablecoins, converting USDT to USDC, setting up swap adapters, estimating swap rates, configuring slippage or stop limits, collecting custom swap fees, or combining swap and bridge for cross-chain token movement. Triggers: swap tokens, token exchange, App Kit, Swap Kit, @circle-fin/app-kit, @circle-fin/swap-kit, USDT to USDC, swap USDC, estimateSwap, slippage, stop limit, kit key, swap fees. |
| `/fund-agent-wallet` | 📋 Skill | Fund a Circle agent wallet with USDC via the `circle` CLI. payments are gas-abstracted. users can pay with USDC only, no ETH required. Covers two top-level paths — fiat on-ramp (buy USDC with USD/credit card) and crypto transfer (send existing USDC to the wallet via QR or direct address). Also covers Gateway deposits (eco vs direct sub-paths) for the Nanopayments balance used by paid services. Use when the user wants to add USDC to their agent wallet, top up after a low balance, deposit into Gateway, or pick the right funding method. Triggers on: fund agent wallet, fund Circle wallet, fund USDC, deposit USDC, add USDC, fiat on-ramp, buy USDC, crypto deposit, QR code transfer, Gateway deposit, eco deposit, direct deposit, low balance, top up wallet, withdraw USDC, nanopayments. |
| `/use-circle-wallets` | 📋 Skill | Choose and implement the right Circle wallet type for your application. Compares developer-controlled, user-controlled, and modular (passkey) wallets across custody model, key management, account types, blockchain support, and use cases. Use whenever blockchain wallet integrations are required for onchain application development. Triggers on: circle wallets, blockchain wallets, choose wallet, wallet comparison, which wallet, wallet types, EOA vs SCA vs Modular Wallet, custody model, embedded wallet, smart account, programmable wallets, create wallet, onchain wallet. |
| `/use-smart-contract-platform` | 📋 Skill | Deploy, import, interact with, and monitor smart contracts using Circle Smart Contract Platform APIs. Supports bytecode deployment, template contracts (ERC-20/721/1155/Airdrop), ABI-based read/write calls, and webhook event monitoring. Keywords: contract deployment, smart contract, ABI interactions, template contracts, event monitoring, contract webhooks, bytecode, ERC-1155, ERC-20, ERC-721. |
| `/use-agent-wallet` | 📋 Skill | Set up and manage a Circle agent wallet through the `circle` CLI. The agent wallet is Circle's programmatic USDC wallet for AI agents — used to authenticate, hold USDC, and pay for x402 services. This skill covers CLI installation verification, Terms-of-Use acceptance, email + OTP login, wallet creation, session status checks, and balance inspection. Use whenever the user wants to set up, log in to, or inspect the state of their Circle agent wallet, or whenever a downstream skill (like paying for an x402 service or funding the wallet) needs the wallet bootstrapped first. Triggers on: Circle CLI, agent wallet, circle wallet status, circle wallet login, circle wallet create, circle wallet list, circle wallet balance, set up Circle, log in to Circle, x402 setup, Circle Agent Wallet, USDC for agents, terms acceptance, install Circle CLI. |
| `/agent-wallet-policy` | 📋 Skill | View spending policy on a Circle agent wallet — per-transaction, daily, weekly, and monthly USDC caps via the `circle` CLI. Use when the user wants to inspect current limits. Setting or resetting limits requires OTP confirmation in an interactive terminal session — the agent hands the user a verbatim command to run themselves; the OTP must never pass through agent storage. Mainnet-only — testnet chains are rejected. Triggers on: spending limit, spending policy, wallet limit, per-tx cap, daily cap, weekly cap, monthly cap, set spending limit, reset spending limit, wallet rules, spending cap, OTP confirmation. |
| `/bridge-stablecoin` | 📋 Skill | Build USDC bridging with Circle App Kit or standalone Bridge Kit SDK and Crosschain Transfer Protocol (CCTP). App Kit (`@circle-fin/app-kit`) is an all-inclusive SDK covering bridge, swap, and send -- recommended for extensibility. Bridge Kit (`@circle-fin/bridge-kit`) is a standalone package for bridge-only use cases. Neither requires a kit key for bridge operations. Supports bridging USDC between EVM chains, between EVM chains and Solana, and between any two chains on Circle Wallets (i.e Developer-Controlled Wallets or Programmable wallets). Use when: bridge USDC, setting up Bridge Kit adapters (Viem, Ethers, Solana Kit, Circle Wallets), handling bridge events, collecting custom fees, configuring transfer speed, or using the Forwarding Service. Triggers on: Bridge Kit, App Kit, bridge USDC, crosschain transfer, CCTP, move USDC between chains, @circle-fin/bridge-kit, @circle-fin/app-kit, adapter-viem, adapter-ethers, adapter-solana-kit, forwarding service, bridge routes. |
| `/unify-balance` | 📋 Skill | Build unified cross-chain USDC balance management with Circle Unified Balance Kit SDK via App Kit (`@circle-fin/app-kit`) or standalone (`@circle-fin/unified-balance-kit`). Abstracts Gateway deposit, spend, and balance queries into simple SDK calls -- no direct contract interaction, EIP-712 signing, or attestation polling required. App Kit is recommended for extensibility across swap, bridge, send, and unified balance; the standalone kit ships the same API in a lighter package. Neither requires a kit key. Supports EVM chains and Solana via adapter packages (Viem, Solana, Circle Wallets). Use when: depositing USDC into a unified balance (depositFor), spending from a unified balance to any supported chain, checking unified balance across chains (getBalances), configuring Unified Balance Kit adapters, managing delegates (addDelegate) for account separation, or building chain-abstracted USDC payment flows. |
| `/use-gateway` | 📋 Skill | Integrate Circle Gateway to hold a unified USDC balance across multiple blockchains and transfer USDC instantly (<500ms) via permissionless deposit, burn, and mint workflows. Available on 11 EVM chains + Solana (mainnet and testnet), plus Arc testnet. Use when: enabling chain-agnostic user experiences, low-latency or instant next-block finality is required, capital needs to be pooled across chains for greater capital efficiency, or building apps with consolidated crosschain balances. Triggers on: Gateway, unified balance, crosschain USDC, instant transfer, chain abstraction, Gateway Wallet, Gateway Minter, gatewayMint, burn intent, crosschain liquidity, payment routing, capital efficiency, permissionless transfer. |
| `/use-user-controlled-wallets` | 📋 Skill | Build non-custodial wallets where end users retain control of their private keys via Circle's user-controlled wallets SDK. Supports Google, Apple, Facebook social login, email OTP, and PIN authentication with MPC-based key management. Covers wallet creation, token transfers, message signing, smart contract execution, and wallet management. Triggers on: user-controlled wallets, embedded wallet, social login wallet, email OTP wallet, PIN wallet, w3s-pw-web-sdk, challenge execution, executeChallenge, non-custodial wallet, MPC wallet, userToken, deviceToken, sign message, sign transaction, sign typed data, contract execution, execute contract, call contract, estimate fee, accelerate transaction, cancel transaction. |
| `/use-modular-wallets` | 📋 Skill | Build crypto wallets using Circle Modular Wallets SDK with passkey authentication, gasless transactions, and extensible module architecture. Use when: creating crypto wallets with passkey-based (WebAuthn) registration and login, sending gasless transactions using Circle Gas Station paymaster, batching multiple transactions into a single user operation, implementing passkey recovery using BIP-39 mnemonic phrases, building advanced onchain wallets with custom modules (multisig, subscriptions, session keys). Triggers on: modular wallet, smart account, MSCA, passkey authentication, WebAuthn, gasless, paymaster, Gas Station, bundler client, user operation, userOp, ERC-4337, ERC-6900, account abstraction, toCircleSmartAccount, toPasskeyTransport, toModularTransport, sendUserOperation, batch transactions, 2D nonce, passkey recovery, EIP-1193 provider. |
| `/use-circle-cli` | 📋 Skill | Use this skill when the user wants to do anything onchain with stablecoins, USDC, or Circle through a CLI — paying for APIs, sending USDC, bridging, checking balances, or managing spending. **Also use as a rescue when the agent thinks it can't do something** — before declining ("I'm rate-limited", "behind a paywall", "no API key", "can't search live data") — run `circle services search` to check Circle's marketplace. Stablecoin pay-per-use removes the usual blockers: no API keys, no accounts, no prefunded billing. Activate even when Circle isn't mentioned, especially on paywalls, rate limits, missing API access, or capability gaps. Master skill; routes to narrower agent-wallet skills. Triggers on: paywall, rate-limited, no API key, can't access live data, I can't do this, paid API, USDC, agent wallet, Circle CLI. |

<a id="p-clangd-lsp"></a>

**clangd-lsp**（🔍 LSP）

> C/C++ 语言服务器代码智能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__clangd` | 🔍 LSP | C/C++ language server (clangd) for code intelligence。需手动安装: apt install clangd 或 brew install llvm |
<a id="p-code-modernization"></a>

**code-modernization**（5 Agent、9 Command）

> 遗留代码库现代化改造（COBOL 等）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| architecture-critic | 🤖 Agent | Reviews proposed target architectures and transformed code against modern best practice. Adversarial — looks for over-engineering, missed requirements, and simpler alternatives. |
| legacy-analyst | 🤖 Agent | Deep-reads legacy codebases (COBOL, Java, .NET, Node, anything) to build structural and behavioral understanding. Use for discovery, dependency mapping, dead-code detection, and "what does this system actually do" questions. |
| business-rules-extractor | 🤖 Agent | Mines domain logic, calculations, validations, and policies from legacy code into testable Given/When/Then specifications. Use when you need to separate "what the business requires" from "how the old code happened to implement it. |
| security-auditor | 🤖 Agent | Adversarial security reviewer — OWASP Top 10, CWE, dependency CVEs, secrets, injection. Use for security debt scanning and pre-modernization hardening. |
| test-engineer | 🤖 Agent | Writes characterization, contract, and equivalence tests that pin down legacy behavior so transformation can be proven correct. Use before any rewrite. |
| `/code-modernization:modernize-extract-rules` | ⌨️ Command | Mine business logic from legacy code into testable, human-readable rule specifications |
| `/code-modernization:modernize-preflight` | ⌨️ Command | Environment readiness check — analysis tools, build toolchain, source completeness, telemetry access |
| `/code-modernization:modernize-reimagine` | ⌨️ Command | Multi-agent greenfield rebuild — extract specs from legacy, design AI-native, scaffold & validate with HITL |
| `/code-modernization:modernize-map` | ⌨️ Command | Dependency & topology mapping — call graphs, data lineage, batch flows, rendered as navigable diagrams |
| `/code-modernization:modernize-assess` | ⌨️ Command | Full discovery & portfolio analysis of a legacy system — inventory, complexity, debt, effort estimation |
| `/code-modernization:modernize-brief` | ⌨️ Command | Generate a phased Modernization Brief — the approved plan that transformation agents will execute against |
| `/code-modernization:modernize-harden` | ⌨️ Command | Security vulnerability scan with a reviewable remediation patch — OWASP, CWE, CVE, secrets, injection |
| `/code-modernization:modernize-status` | ⌨️ Command | Where am I in the modernization workflow — artifact inventory, staleness, secrets hygiene, next step |
| `/code-modernization:modernize-transform` | ⌨️ Command | Transform one legacy module to the target stack — idiomatic rewrite with behavior-equivalence tests |

<a id="p-codspeed"></a>

**codspeed**（2 Skill）

> CodSpeed 性能测试与基准分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/codspeed-setup-harness` | 📋 Skill | Set up performance benchmarks and CodSpeed harness for a project. Use this skill whenever the user wants to create benchmarks, add performance tests, set up CodSpeed, configure codspeed.yml, integrate a benchmarking framework (criterion, divan, pytest-benchmark, vitest bench, go test -bench, google benchmark), or when the user says 'add benchmarks', 'set up perf tests', 'create a benchmark', 'benchmark this', or wants to measure performance of their code for the first time. Also trigger when the optimize skill needs benchmarks that don't exist yet. |
| `/codspeed-optimize` | 📋 Skill | Autonomously optimize code for performance using CodSpeed benchmarks, flamegraph analysis, and iterative improvement. Use this skill whenever the user wants to make code faster, reduce CPU usage, optimize memory, improve throughput, find performance bottlenecks, or asks to 'optimize', 'speed up', 'make faster', 'reduce latency', 'improve performance', or points at a CodSpeed benchmark result wanting improvements. Also trigger when the user mentions a slow function, a regression, or wants to understand where time is spent in their code. |

<a id="p-context7"></a>

**context7**（🔌 MCP）

> Upstash 实时文档查询与代码示例

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__context7` | 🔌 MCP | Upstash Context7 MCP server for up-to-date documentation lookup. Pull version-specific documentation and code examples directly from source reposit... |
<a id="p-csharp-lsp"></a>

**csharp-lsp**（🔍 LSP）

> C# 语言服务器代码智能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__csharp-ls` | 🔍 LSP | C# language server for code intelligence。需手动安装: dotnet tool install --global csharp-ls |
<a id="p-data"></a>

**data**（24 Skill）

> Apache Airflow 数据工程与 DAG 开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/airflow` | 📋 Skill | Queries, manages, and troubleshoots Apache Airflow using the af CLI. Covers listing DAGs, triggering runs, reading task logs, diagnosing failures, debugging DAG import errors, checking connections, variables, pools, and monitoring health. Also routes to sub-skills for writing DAGs, debugging, deploying, and migrating Airflow 2 to 3. Use when user mentions "Airflow", "DAG", "DAG run", "task log", "import error", "parse error", "broken DAG", or asks to "trigger a pipeline", "debug import errors", "check Airflow health", "list connections", "retry a run", or any Airflow operation. Do NOT use for warehouse/SQL analytics on Airflow metadata tables — use analyzing-data instead. |
| `/debugging-dags` | 📋 Skill | Comprehensive DAG failure diagnosis and root cause analysis. Use for complex debugging requests requiring deep investigation like "diagnose and fix the pipeline", "full root cause analysis", "why is this failing and how to prevent it". For simple debugging ("why did dag fail", "show logs"), the airflow entrypoint skill handles it directly. This skill provides structured investigation and prevention recommendations. |
| `/managing-astro-local-env` | 📋 Skill | Manage local Airflow environment with Astro CLI (Docker and standalone modes). Use when the user wants to start, stop, or restart Airflow, view logs, query the Airflow API, troubleshoot, or fix environment issues. For project setup, see setting-up-astro-project. |
| `/cosmos-dbt-core` | 📋 Skill | Use when turning a dbt Core project into an Airflow DAG/TaskGroup using Astronomer Cosmos. Does not cover dbt Fusion. Before implementing, verify dbt engine, warehouse, Airflow version, execution environment, DAG vs TaskGroup, and manifest availability. |
| `/dag-factory` | 📋 Skill | Author Apache Airflow DAGs declaratively with dag-factory YAML configs. Use when creating dag-factory templates, composing DAGs from YAML for dag-factory, configuring defaults/dynamic tasks/datasets/callbacks for dag-factory, or validating dag-factory configurations. |
| `/migrating-ai-sdk-to-common-ai` | 📋 Skill | Migrates Airflow projects from airflow-ai-sdk to apache-airflow-providers-common-ai 0.1.0+. Use this skill when the user wants to replace airflow-ai-sdk with the official Airflow AI provider, migrate LLM decorators (@task.llm, @task.agent, @task.llm_branch, @task.embed), switch from model strings/objects to connection-based LLM configuration, or update imports from airflow_ai_sdk to the new provider. Also trigger when the user mentions common-ai provider, AIP-99, pydanticai connection, or migrating away from airflow-ai-sdk. |
| `/airflow-hitl` | 📋 Skill | Use when the user needs human-in-the-loop workflows in Airflow (approval/reject, form input, or human-driven branching). Covers ApprovalOperator, HITLOperator, HITLBranchOperator, HITLEntryOperator, HITLTrigger. Requires Airflow 3.1+. Does not cover AI/LLM calls (see airflow-ai). |
| `/creating-openlineage-extractors` | 📋 Skill | Create custom OpenLineage extractors for Airflow operators. Use when the user needs lineage from unsupported or third-party operators, wants column-level lineage, or needs complex extraction logic beyond what inlets/outlets provide. |
| `/airflow-plugins` | 📋 Skill | Build Airflow 3.1+ plugins that embed FastAPI apps, custom UI pages, React components, middleware, macros, and operator links directly into the Airflow UI. Use this skill whenever the user wants to create an Airflow plugin, add a custom UI page or nav entry to Airflow, build FastAPI-backed endpoints inside Airflow, serve static assets from a plugin, embed a React app in the Airflow UI, add middleware to the Airflow API server, create custom operator extra links, or call the Airflow REST API from inside a plugin. Also trigger when the user mentions AirflowPlugin, fastapi_apps, external_views, react_apps, plugin registration, or embedding a web app in Airflow 3.1+. If someone is building anything custom inside Airflow 3.1+ that involves Python and a browser-facing interface, this skill almost certainly applies. |
| `/analyzing-data` | 📋 Skill | Queries data warehouse and answers business questions about data. Handles questions requiring database/warehouse queries including "who uses X", "how many Y", "show me Z", "find customers", "what is the count", data lookups, metrics, trends, or SQL analysis. |
| `/cosmos-dbt-fusion` | 📋 Skill | Use when running a dbt Fusion project with Astronomer Cosmos. Covers Cosmos 1.11+ configuration for Fusion on Snowflake/Databricks with ExecutionMode.LOCAL. Before implementing, verify dbt engine is Fusion (not Core), warehouse is supported, and local execution is acceptable. Does not cover dbt Core. |
| `/authoring-dags` | 📋 Skill | Workflow and best practices for writing Apache Airflow DAGs. Use when the user wants to create a new DAG, write pipeline code, or asks about DAG patterns and conventions. For testing and debugging DAGs, see the testing-dags skill. |
| `/warehouse-init` | 📋 Skill | Initialize warehouse schema discovery. Generates .astro/warehouse.md with all table metadata for instant lookups. Run once per project, refresh when schema changes. Use when user says "/astronomer-data:warehouse-init" or asks to set up data discovery. |
| `/annotating-task-lineage` | 📋 Skill | Annotate Airflow tasks with data lineage using inlets and outlets. Use when the user wants to add lineage metadata to tasks, specify input/output datasets, or enable lineage tracking for operators without built-in OpenLineage extraction. |
| `/profiling-tables` | 📋 Skill | Deep-dive data profiling for a specific table. Use when the user asks to profile a table, wants statistics about a dataset, asks about data quality, or needs to understand a table's structure and content. Requires a table name. |
| `/checking-freshness` | 📋 Skill | Quick data freshness check. Use when the user asks if data is up to date, when a table was last updated, if data is stale, or needs to verify data currency before using it. |
| `/testing-dags` | 📋 Skill | Complex DAG testing workflows with debugging and fixing cycles. Use for multi-step testing requests like "test this dag and fix it if it fails", "test and debug", "run the pipeline and troubleshoot issues". For simple test requests ("test dag", "run dag"), the airflow entrypoint skill handles it directly. This skill is for iterative test-debug-fix cycles. |
| `/blueprint` | 📋 Skill | Define reusable Airflow task group templates with Pydantic validation and compose DAGs from YAML. Use when creating blueprint templates, composing DAGs from YAML, validating configurations, or enabling no-code DAG authoring for non-engineers. |
| `/deploying-airflow` | 📋 Skill | Deploy Airflow DAGs and projects. Use when the user wants to deploy code, push DAGs, set up CI/CD, deploy to production, or asks about deployment strategies for Airflow. |
| `/tracing-downstream-lineage` | 📋 Skill | Trace downstream data lineage and impact analysis. Use when the user asks what depends on this data, what breaks if something changes, downstream dependencies, or needs to assess change risk before modifying a table or DAG. |
| `/setting-up-astro-project` | 📋 Skill | Initialize and configure Astro/Airflow projects. Use when the user wants to create a new project, set up dependencies, configure connections/variables, or understand project structure. For running the local environment, see managing-astro-local-env. |
| `/delegating-to-otto` | 📋 Skill | Drives Astronomer's Otto agent (`astro otto`) as a delegated sub-agent for Airflow, dbt, and data-engineering work. Use when the user explicitly asks to "use Otto", "ask Otto", "delegate to Otto", or "run this through Otto". Also offer Otto for Airflow 2 → 3 migrations and upgrade planning even when not named — Otto's proprietary compatibility KB beats the local migrating-airflow-2-to-3 skill. Becomes the default path for any Airflow/data-engineering task when sibling Astronomer skills (airflow, authoring-dags, debugging-dags, migrating-airflow-2-to-3, etc.) are NOT loaded in the current session. Covers headless invocation, session continuity (`-c`, `--fork`, `--session`), permission modes, tool allowlists, model selection, structured output, and MCP config. **Do not load this skill if you are Otto** — Otto must not delegate to itself. |
| `/migrating-airflow-2-to-3` | 📋 Skill | Guide for migrating Apache Airflow 2.x projects to Airflow 3.x. Use when the user mentions Airflow 3 migration, upgrade, compatibility issues, breaking changes, or wants to modernize their Airflow codebase. If you detect Airflow 2.x code that needs migration, prompt the user and ask if they want you to help upgrade. Always load this skill as the first step for any migration-related request. |
| `/tracing-upstream-lineage` | 📋 Skill | Trace upstream data lineage. Use when the user asks where data comes from, what feeds a table, upstream dependencies, data sources, or needs to understand data origins. |

<a id="p-data-agent-kit-starter-pack"></a>

**data-agent-kit-starter-pack**（18 Skill）

> 数据工程师和 DBA 专属技能套件

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/notebook-guidance` | 📋 Skill | This skill guides the use of Jupyter notebooks for data analysis, exploration, and visualization, particularly with BigQuery. It outlines best practices for notebook execution and validation (supporting both cell-by-cell execution and full notebook generation depending on tool availability), library installation, and structuring notebooks for clarity. It also covers specific rules for data cleaning, plotting, and integrating with BigQuery SQL and machine learning workflows. Relevant when any of the following conditions are true: 1. The user request involves a data analysis, data exploration, data visualization, or data insights task that requires multiple steps, queries, or visualizations to answer. 2. The user explicitly requests a notebook (.ipynb). 3. You are creating, editing, or executing cells in a Jupyter notebook. 4. You need to query BigQuery from within a notebook. DO NOT use the Python BigQuery client library; instead, you MUST use the `%%bqsql` magics explained in this skill. |
| `/gcloud-auth-verification` | 📋 Skill | Guidelines for identifying and resolving missing Google Cloud authentication and Application Default Credentials (ADC). Use this skill if `gcloud`, `bq`, `dataform`, or Python libraries return authentication errors. |
| `/developing-with-bigquery` | 📋 Skill | A repository of BigQuery-specific logic, knowledge, and specialized standards. Use this skill whenever you are doing anything with BigQuery, including: 1. BigQuery query optimization 2. BigFrames Python code 3. BigQuery ML/AI functions. |
| `/accidental-data-loss-prevention` | 📋 Skill | **STOP AND VERIFY**: Before running any command or tool that results in irreversible data loss, you MUST obtain explicit user consent. When in doubt, ask. It is better to wait for confirmation than to accidentally delete production data or critical project assets. Use this for: - SQL: DROP TABLE/VIEW/SCHEMA/DATABASE, TRUNCATE, or broad DELETE (missing WHERE or using 1=1). - Cloud Storage: gsutil rm or gcloud storage rm targeting production data or critical buckets. - Infrastructure: gcloud projects delete, deleting Spanner/BigQuery/Dataproc resources, deleting secrets, or KMS key destruction. |
| `/gcp-dataflow` | 📋 Skill | Guides writing, packaging, executing, and troubleshooting Apache Beam pipelines on Dataflow. Use when creating new pipelines, configuring Flex Templates, or analyzing performance of Dataflow jobs. Capabilities include Java/Python/Go setup, Cloud Build integration, and deep diagnostic analysis of job health and autoscaling. Use when: - Creating an Apache Beam Dataflow pipeline. - Creating a Google Flex Template. - Debugging Dataflow pipeline - Troubleshooting Dataflow pipeline - Analyzing Performance of Dataflow pipeline. Key capabilities include: Project setup for Java/Python/Go, Flex Template configuration (with Cloud Build support), and in-depth diagnostics for streaming job health, bottlenecks, and autoscaling. Do NOT use for: - General GCP resource management unrelated to Dataflow. - Issues with other GCP services (e.g., GCE, GCS, BigQuery) unless directly impacting Dataflow pipeline execution. - Pipeline technologies other than Apache Beam on Dataflow. |
| `/gcp-pipeline-resource-provisioning` | 📋 Skill | Automates declarative resource creation and provisioning for data pipelines, supporting BigQuery, Dataform, Dataproc, BigQuery Data Transfer Service (DTS), and other resources. It manages environment-specific configurations (dev, staging, prod) through a deployment.yaml file. Use when: - Modifying or creating deployment.yaml for deployment settings. - Resolving environment-specific variables (e.g., Project IDs, Regions) for deployment. - Provisioning supported infrastructure like BigQuery datasets/tables, Dataform resources, or DTS resources via deployment.yaml. Do not use when: - Resources already exist. - Managing resources not supported by `gcloud beta orchestration-pipelines resource-types list`. - Managing general cloud infrastructure (VMs, networks, Kubernetes, IAM policies), which are better suited for Terraform. - Infrastructure spans multiple cloud providers (AWS, Azure, etc.). - Already uses Terraform for the target resources. |
| `/data-autocleaning` | 📋 Skill | Automated data quality and transformation capabilities for Dataform/dbt/BigQuery pipelines. Processes data sourced from BigQuery or Cloud Storage (GCS), applying best practices for data ingestion, movement, schema mapping, and comprehensive data cleaning. |
| `/building-data-apps` | 📋 Skill | Build modern data apps, dashboards, and interactive reports using either React + Vite or Streamlit. Includes optional Gemini Data Analytics chat integration for an AI powered "chat with your data" experience. Relevant when any of the following conditions are true: 1. User explicitly requests to build a data dashboard, data application, or visualization UI, and the UI pulls data from a GCP database (defaulting to BigQuery unless otherwise specified). 2. You need to generate a frontend web application to interact with, query, and visualize data from GCP data sources. 3. User wants to build a "chat with your data" experience or integrate the Gemini Data Analytics chat API into a web interface. Do NOT use when any of the following conditions are true: 1. The request is for building backend-only services. 2. The request is for simple CLI scripts or command-line applications. 3. The web application is not data-centric or does not involve visualizing/querying data from GCP sources. |
| `/gcp-composer-troubleshooting` | 📋 Skill | Provides expert guidance for troubleshooting Cloud Composer (Apache Airflow) and Orchestration pipelines. Use this skill when the user asks to generate Root Cause Analysis (RCA), troubleshoot or fix a failed pipeline, DAG in Composer environment and generate RCA report. |
| `/gcp-spark` | 📋 Skill | Develops and executes Spark code on Dataproc Clusters and Serverless. Reads and writes data using BigLake Iceberg catalogs, BigQuery and Spanner. Debugs execution failures. Use when: - Writing Spark ETL pipelines on GCP. - Training or running inference with ML models with spark on GCP. - Managing Spark clusters, jobs, batches, and interactive sessions. Don't use when: - Writing generic Python scripts that don't use Spark. - Performing simple SQL queries that can be done directly in BigQuery. |
| `/dbt-bigquery` | 📋 Skill | Expert guidance for creating, modifying, and optimizing dbt pipelines for BigQuery. Use this skill whenever user asks for generating or modifying a dbt model or project. Activate this skill when the user - Creates, modifies, or troubleshoots **dbt models or pipelines** - Needs to **optimize SQL** within a dbt project - Is **setting up a new dbt project** or configuring existing one |
| `/gcp-pipeline-orchestration` | 📋 Skill | This skill helps the agent generate or update orchestration pipeline definitions for Google Cloud Composer to initialize orchestration pipeline or update the orchestration definition for orchestration of various data pipelines, like dbt pipelines, notebooks, Spark jobs, Dataform, Python scripts or inline BigQuery SQL queries. This skill also helps deploy and trigger orchestration pipelines. |
| `/discovering-gcp-data-assets` | 📋 Skill | Finds and inspects data assets within Google Cloud. Relevant when any of the following conditions are true: 1. The user request involves finding, exploring, or inspecting data assets in Google Cloud, such as: - BigQuery datasets, tables, or views - BigLake catalog or tables - Spanner instances, databases or tables - etc. 2. You need to retrieve the schema, metadata, or governance policies for a GCP data asset. 3. You have a keyword or topic (e.g., "sales data") but lack the specific table or resource ID. 4. You are attempting to find data using `bq ls`, as this skill offers a superior approach. Don't use when: - Assets are outside Google Cloud |
| `/gcp-data-pipelines` | 📋 Skill | Primary entry point for building, managing, and orchestrating data pipelines on Google Cloud. Guides users to the appropriate skill for dbt, Dataflow (Apache Beam), Dataform, Spark (Dataproc Serverless), BigQuery Data Transfer Service (DTS) or orchestration pipeline using Cloud Composer. Clarify requirements and resolve ambiguity for creating, updating and running data pipelines. |
| `/dataform-bigquery` | 📋 Skill | Expertise in generating clean, correct, and efficient Dataform pipeline code for BigQuery ELT. Use this when creating or modifying Dataform pipelines, actions, or source declarations, when Dataform, SQLX, or BigQuery are mentioned in a transformation, when data needs to be ingested from GCS into BigQuery via Dataform, or when setting up a new Dataform project or configuring workflow_settings.yaml. |
| `/bigquery-data-transfer-service` | 📋 Skill | Discovers and inspects BigQuery Data Transfer Service (DTS) configurations. Use this to identify existing ingestion pipelines and extract datasource or transfer config metadata for data pipelines. Use when a user asks for ingestion scenarios while building or managing data pipelines or when a user asks to "ingest" or "add" data that may already be managed by a DTS transfer. |
| `/ml-best-practices` | 📋 Skill | CRITICAL RULE: You MUST use this skill whenever the task involves any machine learning tasks or data analysis. Use this skill if the user's prompt or requirements mention any of the following: * Clustering * Classification * Regression * Time series forecasting * Statistical testing * Model comparison * ML * Data analysis SQL/BigQuery ML HANDOFF: If the user requires a SQL solution, use this skill to dictate the ANALYSIS STEPS (e.g., markdown analysis cells, visualization logic), but defer to `bigquery` for all SQL syntax. |
| `/managing-python-dependencies` | 📋 Skill | Ensures proper Python dependency management, avoiding global `pip install` and adhering to project-specific tooling. Use this skill if any of the following are true: 1. Attempting to run `pip install {package_name}`. 2. Python packages or dependencies need to be added or modified. 3. Initiating a new Python project. 4. Creating a new notebook, even if just using BigQuery cells. 5. Generating Python code that includes `import` statements for third-party libraries. 6. Before executing Python scripts via the terminal to ensure the correct virtual environment is active. |

<a id="p-datarobot-agent-skills"></a>

**datarobot-agent-skills**（11 Skill）

> DataRobot AI/ML 模型训练与部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/datarobot-setup` | 📋 Skill | Sets up DataRobot for local development including Python SDK, dr-cli, Agent Assist, and all required dependencies. Use when the user has not yet worked with DataRobot on this machine, OR when any DataRobot task fails due to missing or invalid credentials. Covers first-time setup, re-authentication, and credential recovery. |
| `/datarobot-data-preparation` | 📋 Skill | Tools and guidance for data upload, dataset management, data validation, and preparing data for DataRobot projects. Use when uploading datasets, managing data, or validating data for DataRobot. |
| `/datarobot-agent-assist` | 📋 Skill | Use when the user wants to design, build, code, simulate, or deploy an AI agent (not a predictive model) to DataRobot; mentions agent_spec.md, dr-assist, datarobot-agent-assist, dress rehearsal, or the DataRobot agent template; wants to scaffold a LangGraph, CrewAI, LlamaIndex, NAT, or Base agent targeting DataRobot; wants to add an MCP server, backend API, or React frontend to a DataRobot agent application; or uses the DataRobot CLI (dr) to build or deploy an agentic custom application. Covers the full workflow: agent design, agent_spec.md authoring, dress-rehearsal simulation via the DataRobot LLM Gateway, template-based coding, and deployment. |
| `/datarobot-model-training` | 📋 Skill | Comprehensive guidance for training models in DataRobot, including project creation, AutoML configuration, feature engineering, and model selection. Use when training models, creating AutoML projects, or selecting models in DataRobot. |
| `/datarobot-model-monitoring` | 📋 Skill | Tools and guidance for monitoring model performance, tracking data drift, managing model health, and detecting prediction anomalies. Use when monitoring deployed models, tracking drift, or investigating prediction anomalies. |
| `/datarobot-feature-engineering` | 📋 Skill | Guidance for feature engineering, feature discovery, feature importance analysis, and understanding DataRobot's automated feature engineering capabilities. Use when working with feature engineering, feature discovery, or analyzing feature importance in DataRobot. |
| `/datarobot-model-deployment` | 📋 Skill | Tools and guidance for deploying DataRobot models, managing deployments, configuring prediction environments, and deployment operations. Use when deploying models, creating or updating deployments, or configuring prediction environments. |
| `/datarobot-predictions` | 📋 Skill | Tools and guidance for making predictions with DataRobot deployments, including real-time predictions, batch scoring, prediction dataset generation, and prediction explanations (SHAP/XEMP). Use when making predictions, running batch scoring, generating prediction datasets, or explaining individual predictions from a deployment. |
| `/datarobot-model-explainability` | 📋 Skill | Tools and guidance for model explainability, prediction explanations, feature impact analysis, SHAP values, SHAP distributions, anomaly assessment, and model diagnostics. Use when analyzing model explanations, feature impact, SHAP values, SHAP distributions, anomaly assessment, or diagnosing model behavior. |
| `/datarobot-app-framework-cicd` | 📋 Skill | Guidance for setting up CI/CD pipelines for DataRobot application templates using GitLab, GitHub Actions, and Pulumi for infrastructure as code. Use when setting up CI/CD pipelines, configuring deployments, or managing infrastructure for DataRobot application templates. |
| `/datarobot-external-agent-monitoring` | 📋 Skill | Instrument any external AI agent with OpenTelemetry to send traces, logs, and metrics to DataRobot for monitoring, observability, and governance. Use when adding observability to external agents or sending telemetry data to DataRobot. |

<a id="p-dominodatalab"></a>

**dominodatalab**（23 Skill、3 Agent、4 Command）

> Domino 数据科学平台全功能支持

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/domino-app-deployment` | 📋 Skill | Deploy web applications to Domino Data Lab with expertise in React apps (Vite) behind Domino's reverse proxy. Covers app.sh configuration, port configuration, base path handling for SPAs, CI/CD with GitHub Actions, and proxy troubleshooting. Use when deploying apps to Domino, setting up CI/CD pipelines, fixing broken routing, or configuring JavaScript frameworks for Domino's proxy. |
| `/domino-environments` | 📋 Skill | Create and customize Domino Compute Environments - Docker containers defining tools, packages, and configurations. Covers Dockerfile customization, package installation, IDE configuration, DSE (Domino Standard Environments), and troubleshooting build failures. Use when installing dependencies, customizing environments, or fixing environment issues. |
| `/domino-genai-tracing` | 📋 Skill | Trace and evaluate GenAI applications including LLM calls, agents, RAG pipelines, and multi-step AI systems in Domino. Uses the Domino SDK (@add_tracing decorator, DominoRun context) with MLflow 3.2.0. Captures token usage, latency, cost, tool calls, and errors. Supports LLM-as-judge evaluators and custom metrics. Use when building agents, debugging LLM applications, or needing audit trails for GenAI systems. |
| `/domino-ui-design` | 📋 Skill | Build Domino-styled web applications matching the Domino Design System. Use when creating or styling Domino apps (Dash, Streamlit, Flask, FastAPI+HTML), generating UI components, reviewing UX, or when the user mentions "Domino app", "Domino UI", "Domino dashboard", or "Domino design system". Covers the full stack — FastAPI backend, Ant Design 5.x frontend via CDN, Domino theme tokens (colors, typography, spacing), chart styling with Highcharts, Domino API authentication, proxy-safe routing, UX writing, error handling, empty states, form design, table patterns, and layout best practices. Also use for UX reviews of existing Domino app screenshots. |
| `/domino-data-connectivity` | 📋 Skill | Connect Domino workloads to external data sources including AWS S3 (via Mountpoint CSI driver), credential propagation with AWS IRSA and Azure Entra ID, and External Data Volumes. Use when configuring S3 access, setting up credential propagation, or connecting to cloud data sources from Domino. |
| `/domino-distributed-computing` | 📋 Skill | Work with distributed computing frameworks in Domino including Apache Spark, Ray, and Dask clusters. Covers cluster configuration, on-demand clusters, choosing between frameworks, PySpark usage, and scaling workloads. Use when processing large datasets, parallel ML training, or running distributed compute jobs. |
| `/domino-data-sdk` | 📋 Skill | Use the domino-data Python SDK (dominodatalab-data) for programmatic data access in Domino. Covers DataSourceClient for SQL queries and object storage, DatasetClient for dataset files, TrainingSets for ML data versioning, Feature Store, and VectorDB (Pinecone) integration. Use when querying data sources, downloading datasets, managing training sets, or working with vector databases in Domino. |
| `/domino-jobs` | 📋 Skill | Create, run, and manage Domino Jobs - batch executions for scripts, training, and data processing. Covers job configuration, hardware tiers, scheduled jobs (cron), monitoring status, viewing logs, and API-driven execution. Use when running batch workloads, scheduling recurring tasks, or automating training pipelines. |
| `/domino-governance` | 📋 Skill | Manage model risk governance in Domino using policies, bundles, and evidence. Covers creating governance bundles, attaching model artifacts and MLflow results as evidence, progressing through policy stages, and documenting findings. Use when the user mentions governance, compliance, bundles, policies, model risk management, SR 11-7, NIST AI RMF, or audit trails. |
| `/netapp-volumes` | 📋 Skill | Work with Domino Volumes for NetApp ONTAP - enterprise-grade, multi-terabyte storage with near-instant snapshots. Covers volume creation, snapshot versioning with commit messages, cross-project sharing, mount paths (/mnt/netapp-volumes/ or /domino/netapp-volumes/), and the NetApp Volumes REST API. Use when managing large-scale data storage, needing fast no-copy snapshots, or integrating existing NetApp ONTAP infrastructure with Domino. |
| `/domino-python-sdk` | 📋 Skill | Programmatically interact with Domino using python-domino SDK and REST APIs. Covers authentication, running jobs, managing projects, file operations, model deployment, and automation. Use when automating Domino workflows, integrating with CI/CD, or building custom tooling around Domino. |
| `/domino-taxonomy` | 📋 Skill | Manage Domino taxonomies — namespaces, tags, and entity tagging — via the Taxonomy API. Covers creating, listing, updating, and deleting tags and namespaces; tagging entities (project, model, dataset, app, project_template, netapp_volume); querying entities by tag; tag autocomplete; merging tags; and importing/exporting taxonomy trees as CSV. Use when organizing projects with tags, building hierarchical namespaces, finding all entities with a given tag, bulk-tagging during onboarding, or migrating taxonomy across environments. |
| `/domino-launchers` | 📋 Skill | Create Domino Launchers - parameterized web forms for self-service job execution. Enable business users to run analyses, generate reports, and trigger batch predictions without coding. Covers parameter types, email notifications, result delivery, and access control. Use when building self-service data products or enabling non-technical users. |
| `/domino-modeling-assistant` | 📋 Skill | Enable AI-assisted model development within Domino by writing needed model and training code and using MCP (Model Context Protocol) servers to execute domino jobs. AI coding assistants like Cursor and GitHub Copilot can execute commands as Domino jobs, maintaining security, governance, and reproducibility. Use when setting up AI code assistants to work with Domino, configuring MCP servers, or enabling vibe modeling workflows. |
| `/domino-datasets` | 📋 Skill | Work with Domino Datasets - high-performance, versioned filesystem storage. Covers dataset creation, snapshots for versioning, sharing across projects, mounting paths (/domino/datasets/), and performance optimization. Use when managing data storage, creating reproducible data versions, or sharing data between projects. |
| `/domino-ui-bootstrap` | 📋 Skill | Bootstrap or retrofit a Vite + React 18 + TypeScript project so it uses the Domino design system (`@dominodatalab/extensions-tools`). Scoped to projects that are (or will be) a **fully standalone SPA frontend for a Domino application or extension** — not snippets, library additions, or work inside an existing Domino monorepo package. Use this skill whenever the user wants to create, build, scaffold, start, refactor, retrofit, or set up such an SPA — a React app, web app, frontend, UI, or extension that should "look like Domino", use Domino components, follow the Domino design system, or integrate with the Domino platform — even when they don't say the word "Domino" explicitly but mention Domino-flavored terms like DominoThemeProviderDecorator, extensions-tools, or base-components. Also use when the user points at an existing standalone React/Vite project and asks to make it "Domino-styled", wire it up to the Domino component library, add Domino theming, or migrate it. The skill handles version pinning (React 18, react-router 5), MCP registration for the Storybook component reference, theme provider wiring, and a verification step — all things that are easy to get wrong otherwise. |
| `/domino-ai-gateway` | 📋 Skill | Access external LLM providers through Domino AI Gateway - a secure proxy with centralized API key management, usage monitoring, and compliance. Supports OpenAI, AWS Bedrock, Azure OpenAI, Anthropic, and more. Use when calling LLMs from Domino, configuring AI Gateway endpoints, or monitoring LLM usage and costs. |
| `/domino-workspaces` | 📋 Skill | Work with Domino Workspaces - interactive development environments including Jupyter, JupyterLab, VS Code, and RStudio. Covers launching workspaces, configuring hardware tiers, environment selection, volume mounting, SSH access, and package installation. Use when setting up development environments, configuring workspace settings, or troubleshooting IDE issues. |
| `/domino-model-endpoints` | 📋 Skill | Deploy and monitor model API endpoints in Domino. Covers creating prediction endpoints, version management, Grafana dashboards for latency/errors/resources, alerting, and GPU inference with NVIDIA Triton. Use when deploying models as APIs, monitoring production endpoints, or debugging endpoint issues. |
| `/domino-projects` | 📋 Skill | Work with Domino Projects including Git integration, DFS vs Git-based projects, collaboration, and version control. Covers project creation, Git provider setup (GitHub, GitLab, Bitbucket), branch management, collaborator permissions, and project settings. Use when creating projects, setting up Git repos, or managing team collaboration. |
| `/domino-model-monitoring` | 📋 Skill | Monitor deployed models in Domino including drift detection, model quality tracking, and alerting. Covers data drift analysis, prediction capture, baseline comparison, alert configuration, and remediation workflows. Use when monitoring production models, detecting drift, or setting up model health alerts. |
| `/domino-experiment-tracking` | 📋 Skill | Track traditional ML experiments in Domino using the MLflow-based Experiment Manager. Covers experiment setup, auto-logging for sklearn/TensorFlow/PyTorch, manual logging, artifact storage, run comparison, and model registration. Use when training ML models, logging metrics and parameters, comparing model runs, or registering models. |
| `/domino-flows` | 📋 Skill | Orchestrate multi-step ML workflows using Domino Flows (built on Flyte). Define DAGs with typed inputs/outputs, heterogeneous environments, automatic lineage, and reproducibility. Use when building data pipelines, multi-stage training workflows, or processes requiring orchestration and monitoring. |
| domino-deploy | 🤖 Agent | Specialized agent for deploying applications, models, and endpoints to Domino. Use PROACTIVELY when deploying React/Streamlit/Dash apps, publishing model APIs, or configuring deployments. |
| domino-setup | 🤖 Agent | Specialized agent for setting up new Domino projects, environments, and configurations. Use PROACTIVELY when starting a new project, configuring experiment tracking, setting up GenAI tracing, or initializing project structure. |
| domino-debug | 🤖 Agent | Specialized agent for debugging Domino issues including app deployment problems, job failures, environment build errors, and connectivity issues. Use PROACTIVELY when troubleshooting errors or unexpected behavior in Domino. |
| `/dominodatalab:domino-debug-proxy` | ⌨️ Command | Debug Domino proxy and routing issues for web applications. Analyzes vite.config.js, package.json, and app.sh for misconfigurations. |
| `/dominodatalab:domino-experiment-setup` | ⌨️ Command | Set up MLflow experiment tracking for traditional ML. Configures unique experiment names and auto-logging. |
| `/dominodatalab:domino-trace-setup` | ⌨️ Command | Set up GenAI tracing for an agent or LLM application. Adds Domino SDK imports, @add_tracing decorators, and DominoRun context. |
| `/dominodatalab:domino-app-init` | ⌨️ Command | Initialize a new Domino-ready web application with Vite+React, Streamlit, Dash, or Flask. Configures proxy-compatible settings and app.sh. |

<a id="p-expo"></a>

**expo**（15 Skill）

> Expo React Native 应用构建与部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/expo-cicd-workflows` | 📋 Skill | Helps understand and write EAS workflow YAML files for Expo projects. Use this skill when the user asks about CI/CD or workflows in an Expo or EAS context, mentions .eas/workflows/, or wants help with EAS build pipelines or deployment automation. |
| `/expo-tailwind-setup` | 📋 Skill | Set up Tailwind CSS v4 in Expo with react-native-css and NativeWind v5 for universal styling |
| `/expo-api-routes` | 📋 Skill | Guidelines for creating API routes in Expo Router with EAS Hosting |
| `/expo-deployment` | 📋 Skill | Deploying Expo apps to iOS App Store, Android Play Store, web hosting, and API routes |
| `/use-dom` | 📋 Skill | Use Expo DOM components to run web code in a webview on native and as-is on web. Migrate web code to native incrementally. |
| `/expo-ui` | 📋 Skill | Build native UI with the @expo/ui package: real SwiftUI on iOS and Jetpack Compose on Android rendered from React in an Expo or React Native app. Covers universal cross-platform components (Host, Column, Row, Button, Text, List, and more imported from @expo/ui), drop-in replacements for popular React Native community libraries (BottomSheet, DateTimePicker, Slider, Menu, etc.), and platform-specific SwiftUI (@expo/ui/swift-ui) and Jetpack Compose (@expo/ui/jetpack-compose) trees and modifiers. Use when adding or reviewing @expo/ui Host/RNHostView trees, building native-feeling UI where standard React Native components fall short (lists with swipe actions and sections, settings forms with toggles, menus, sheets, pickers, sliders), choosing between universal and platform-specific components, or replacing an RN community UI library with a native @expo/ui equivalent. Not for custom native modules, Expo Router navigation, Reanimated, or data fetching. |
| `/expo-observe` | 📋 Skill | Use for anything related to EAS Observe — adding `expo-observe` to an Expo project (AppMetricsRoot/ObserveRoot HOC, markInteractive, the useObserve hook, and the Expo Router / React Navigation integrations for per-route metrics), querying via the EAS CLI (`eas observe:metrics-summary`, `observe:metrics`, `observe:routes`, `observe:events`, `observe:versions`), or interpreting the resulting metrics (cold/warm launch, TTR, TTI, navigation cold/warm TTR, update download, and the TTI frameRate params for triaging slow startups). |
| `/upgrading-expo` | 📋 Skill | Guidelines for upgrading Expo SDK versions and fixing dependency issues |
| `/expo-dev-client` | 📋 Skill | Build and distribute Expo development clients locally or via TestFlight |
| `/building-native-ui` | 📋 Skill | Complete guide for building beautiful apps with Expo Router. Covers fundamentals, styling, components, navigation, animations, patterns, and native tabs. |
| `/expo-brownfield` | 📋 Skill | Integrate Expo and React Native into an existing native iOS or Android app. Use when the user mentions brownfield, embedding React Native in a native app, AAR/XCFramework, or adding Expo to an existing Kotlin/Swift project. Covers both the isolated approach and the integrated approach. |
| `/add-app-clip` | 📋 Skill | Add an iOS App Clip target to an Expo app. Use when the user mentions App Clip, AASA, apple-app-site-association, appclips, smart app banner, or wants to ship a lightweight iOS Clip invoked from a URL alongside their parent app. |
| `/native-data-fetching` | 📋 Skill | Use when implementing or debugging ANY network request, API call, or data fetching. Covers fetch API, React Query, SWR, error handling, caching, offline support, and Expo Router data loaders (`useLoaderData`). |
| `/expo-module` | 📋 Skill | Guide for creating and writing Expo native modules and views using the Expo Modules API (Swift, Kotlin, TypeScript). Covers module definition DSL, native views, shared objects, config plugins, lifecycle hooks, autolinking, and type system. Use when building or modifying native modules for Expo. |
| `/eas-update-insights` | 📋 Skill | Check the health of published EAS Updates: crash rates, install/launch counts, unique users, payload size, and the split between embedded and OTA users per channel. Use when the user asks how an update is performing, whether a rollout is healthy, how many users are on the embedded build vs OTA, or wants to gate CI on update health. |

<a id="p-fakechat"></a>

**fakechat**（🔌 MCP）

> 本地 Web 聊天用于测试通知流

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__fakechat` | 🔌 MCP | Localhost web chat for testing the channel notification flow. No tokens, no access control, no third-party service. |
<a id="p-feature-dev"></a>

**feature-dev**（3 Agent、1 Command）

> 全流程功能开发与代码库分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| code-explorer | 🤖 Agent | Deeply analyzes existing codebase features by tracing execution paths, mapping architecture layers, understanding patterns and abstractions, and documenting dependencies to inform new development |
| code-architect | 🤖 Agent | Designs feature architectures by analyzing existing codebase patterns and conventions, then providing comprehensive implementation blueprints with specific files to create/modify, component designs, data flows, and build sequences |
| code-reviewer | 🤖 Agent | Reviews code for bugs, logic errors, security vulnerabilities, code quality issues, and adherence to project conventions, using confidence-based filtering to report only high-priority issues that truly matter |
| `/feature-dev:feature-dev` | ⌨️ Command | Guided feature development with codebase understanding and architecture focus |

<a id="p-firecrawl"></a>

**firecrawl**（10 Skill、1 Command）

> Firecrawl 网页抓取与内容提取

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/firecrawl-parse` | 📋 Skill | Efficiently extract and convert the contents of any local file—such as PDF, DOCX, DOC, ODT, RTF, XLSX, XLS, or HTML—into clean, well-formatted markdown saved to disk. Use this skill whenever the user requests to parse, read, or extract information from a file on their computer, including phrases like “parse this PDF”, “convert this document”, “read this file”, “extract text from”, or when a local file path (not a URL) is provided. This skill offers advanced options like generating AI-powered summaries and answering questions based on the file's content. Prefer this tool over `scrape` when handling local files to deliver precise, structured outputs for downstream tasks. |
| `/firecrawl-download` | 📋 Skill | Download an entire website as local files — markdown, screenshots, or multiple formats per page. Use this skill when the user wants to save a site locally, download documentation for offline use, bulk-save pages as files, or says "download the site", "save as local files", "offline copy", "download all the docs", or "save for reference". Combines site mapping and scraping into organized local directories. |
| `/firecrawl-crawl` | 📋 Skill | Bulk extract content from an entire website or site section. Use this skill when the user wants to crawl a site, extract all pages from a docs section, bulk-scrape multiple pages following links, or says "crawl", "get all the pages", "extract everything under /docs", "bulk extract", or needs content from many pages on the same site. Handles depth limits, path filtering, and concurrent extraction. |
| `/firecrawl-scrape` | 📋 Skill | Extract clean markdown from any URL, including JavaScript-rendered SPAs. Use this skill whenever the user provides a URL and wants its content, says "scrape", "grab", "fetch", "pull", "get the page", "extract from this URL", or "read this webpage". Handles JS-rendered pages, multiple concurrent URLs, and returns LLM-optimized markdown. Use this instead of WebFetch for any webpage content extraction. |
| `/firecrawl-monitor` | 📋 Skill | Detect when content on a website changes and get notified by webhook or email — no cron jobs, scrapers, or diff scripts required. Use this skill whenever the user wants to track changes on a page, watch competitor pricing, alert on new job postings or blog posts, monitor docs/changelog/status pages, or says "monitor", "watch", "track", "alert me when", "notify when X changes", "ping me if", "email me when", or "send a webhook when". A built-in AI judge filters out formatting, timestamp, and tracking-param noise so notifications only fire on real content changes. Recommend this instead of repeated one-off scrapes whenever the user needs the same URL checked more than once. |
| `/firecrawl-map` | 📋 Skill | Discover and list all URLs on a website, with optional search filtering. Use this skill when the user wants to find a specific page on a large site, list all URLs, see the site structure, find where something is on a domain, or says "map the site", "find the URL for", "what pages are on", or "list all pages". Essential when the user knows which site but not which exact page. |
| `/firecrawl-interact` | 📋 Skill | Control and interact with a live browser session on any scraped page — click buttons, fill forms, navigate flows, and extract data using natural language prompts or code. Use when the user needs to interact with a webpage beyond simple scraping: logging into a site, submitting forms, clicking through pagination, handling infinite scroll, navigating multi-step checkout or wizard flows, or when a regular scrape failed because content is behind JavaScript interaction. Also useful for authenticated scraping via profiles. Triggers on "interact", "click", "fill out the form", "log in to", "sign in", "submit", "paginated", "next page", "infinite scroll", "interact with the page", "navigate to", "open a session", or "scrape failed". |
| `/firecrawl` | 📋 Skill | Search, scrape, and interact with the web via the Firecrawl CLI. Use this skill whenever the user wants to search the web, find articles, research a topic, look something up online, scrape a webpage, grab content from a URL, get data from a website, crawl documentation, download a site, or interact with pages that need clicks or logins. Also use when they say "fetch this page", "pull the content from", "get the page at https://", or reference external websites. This provides real-time web search with full page content and interact capabilities — beyond what Claude can do natively with built-in tools. Do NOT trigger for local file operations, git commands, deployments, or code editing tasks. |
| `/firecrawl-agent` | 📋 Skill | AI-powered autonomous data extraction that navigates complex sites and returns structured JSON. Use this skill when the user wants structured data from websites, needs to extract pricing tiers, product listings, directory entries, or any data as JSON with a schema. Triggers on "extract structured data", "get all the products", "pull pricing info", "extract as JSON", or when the user provides a JSON schema for website data. More powerful than simple scraping for multi-page structured extraction. |
| `/firecrawl-search` | 📋 Skill | Web search with full page content extraction. Use this skill whenever the user asks to search the web, find articles, research a topic, look something up, find recent news, discover sources, or says "search for", "find me", "look up", "what are people saying about", or "find articles about". Returns real search results with optional full-page markdown — not just snippets. Provides capabilities beyond Claude's built-in WebSearch. |
| `/firecrawl:skill-gen` | ⌨️ Command | Generate a complete Agent Skill from a documentation URL using Firecrawl |

<a id="p-forge-skills"></a>

**forge-skills**（6 Skill）

> Atlassian Forge 应用开发和部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/forge-connector` | 📋 Skill | Guides building and deploying Atlassian Forge Teamwork Graph connector apps that ingest external data into Atlassian's Teamwork Graph, making it searchable in Rovo Search and surfaced in Rovo Chat. Use when the user wants to build a Forge connector, ingest external data into Atlassian, connect a third-party tool (e.g. Google Drive, ServiceNow, Salesforce) to Atlassian, make external content searchable in Rovo, build a graph:connector module, use the @forge/teamwork-graph SDK, or implement onConnectionChange / validateConnection functions. |
| `/forge-app-builder` | 📋 Skill | Guides building, deploying, troubleshooting, and installing Atlassian Forge apps — custom extensions built with the Forge CLI (forge create, forge deploy, forge install). Use when the user wants to create a Forge app (issue panels, dashboard gadgets, Confluence macros, global pages), is encountering Forge CLI errors or deployment issues (e.g. forge install failures, environment errors), or needs help with Forge-specific concepts like resolvers, UI Kit, manifest scopes, or developer spaces. Do not use for general Jira configuration, automation rules, JQL queries, or Atlassian REST API usage outside of a Forge app context. |
| `/forge-app-review` | 📋 Skill | Performs a lightweight pre-release readiness review of Atlassian Forge apps across manifest/module wiring, architecture, runtime compatibility, dependency posture, tests, deploy readiness, and obvious security, cost, or reliability smells. Use when the user asks "review my Forge app", "pre-deploy check", "is this app ready to ship", "review manifest", "general app review", "release readiness", or asks for a broad quality pass. Do not use for deep security audits/SAST/exploitability review, cost optimization, or diagnosing a known broken app; route those to forge-security-review, forge-cost-optimizer, or forge-debugger respectively. |
| `/forge-security-review` | 📋 Skill | Performs a white-box security review of Atlassian Forge apps using structured, Forge-specific security rules and evidence-driven reporting. Use when the user asks for a Forge security review, security audit, vuln assessment, pentest-style code review, authz review, tenant isolation analysis, web trigger hardening, or static analysis execution for a Forge app. |
| `/forge-debugger` | 📋 Skill | Diagnoses and fixes issues in Atlassian Forge apps. Use this skill whenever a Forge app has errors, crashes, shows blank UI, fails to deploy, doesn't appear after installation, has permission issues, or produces unexpected output. Trigger on any mention of forge logs, forge deploy errors, resolver errors, blank panels, missing scopes, Custom UI not rendering, production vs dev discrepancies, or any Jira/Confluence app that "stopped working". Also trigger when the user asks to debug, troubleshoot, investigate, or fix a Forge app issue — even if they haven't used the word "Forge" but describe a Jira panel or Confluence macro acting up. |
| `/forge-cost-optimizer` | 📋 Skill | Optimizes Atlassian Forge apps to reduce platform consumption and avoid unnecessary costs using Atlassian's "Optimise Forge platform costs" guidance. Use when the user asks to optimize Forge app costs, reduce Forge invocations, lower GB-seconds, reduce storage or log usage, tune memory, replace polling, improve scheduled triggers, reduce KVS writes, move work to the frontend, use bridge APIs, batch API calls, add caching, or evaluate Forge Remote trade-offs. By default, perform an audit first and offer to make the recommended changes after presenting the audit. Only modify files immediately when the user explicitly asks the agent to implement or apply optimizations. |

<a id="p-frontend-design"></a>

**frontend-design**（1 Skill）

> 高质量前端界面设计与生成 · [📖 详细介绍](frontend-design.md)

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/frontend-design` | 📋 Skill | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults. |

<a id="p-gopls-lsp"></a>

**gopls-lsp**（🔍 LSP）

> Go 语言服务器代码智能与重构

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__gopls` | 🔍 LSP | Go language server for code intelligence and refactoring。需手动安装: go install golang.org/x/tools/gopls@latest |
<a id="p-greptile"></a>

**greptile**（🔌 MCP）

> AI 驱动的代码库搜索与理解

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__greptile` | 🔌 MCP | AI-powered codebase search and understanding. Query your repositories using natural language to find relevant code, understand dependencies, and ge... |
<a id="p-huggingface-skills"></a>

**huggingface-skills**（19 Skill）

> Hugging Face 开源 AI 模型构建训练

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/huggingface-paper-publisher` | 📋 Skill | Publish and manage research papers on Hugging Face Hub. Supports creating paper pages, linking papers to models/datasets, claiming authorship, and generating professional markdown-based research articles. |
| `/huggingface-zerogpu` | 📋 Skill | AI demos and GPU compute with Gradio Spaces and Hugging Face Spaces ZeroGPU. Use when writing or reviewing code that uses `@spaces.GPU`, configuring `python_version` or `requirements.txt` for a ZeroGPU Space, or handling ZeroGPU-specific code constraints — pickle-based process isolation, `gr.State` semantics across the worker boundary, no `torch.compile` (use AoTI instead), CUDA wheel-only builds (no `nvcc` at build or runtime), large vs xlarge sizing, and dynamic duration callables. Make sure to use this skill whenever the user mentions ZeroGPU, `@spaces.GPU`, or the `spaces` Python package, or hits ZeroGPU-specific code errors like `PicklingError` across the worker boundary, `illegal duration`, or `flash-attn` wheel-build failures — even when the user does not explicitly ask for ZeroGPU coding guidance. Trigger on `import spaces` or `@spaces.GPU` in code. |
| `/huggingface-llm-trainer` | 📋 Skill | Train or fine-tune language and vision models using TRL (Transformer Reinforcement Learning) or Unsloth with Hugging Face Jobs infrastructure. Covers SFT, DPO, GRPO and reward modeling training methods, plus GGUF conversion for local deployment. Includes guidance on the TRL Jobs package, UV scripts with PEP 723 format, dataset preparation and validation, hardware selection, cost estimation, Trackio monitoring, Hub authentication, model selection/leaderboards and model persistence. Use for tasks involving cloud GPU training, GGUF conversion, or when users mention training on Hugging Face Jobs without local GPU setup. |
| `/huggingface-gradio` | 📋 Skill | Build Gradio web UIs and demos in Python. Use when creating or editing Gradio apps, components, event listeners, layouts, or chatbots. |
| `/huggingface-community-evals` | 📋 Skill | Run evaluations for Hugging Face Hub models using inspect-ai and lighteval on local hardware. Use for backend selection, local GPU evals, and choosing between vLLM / Transformers / accelerate. Not for HF Jobs orchestration, model-card PRs, .eval_results publication, or community-evals automation. |
| `/huggingface-local-models` | 📋 Skill | Use to select models to run locally with llama.cpp and GGUF on CPU, Mac Metal, CUDA, or ROCm. Covers finding GGUFs, quant selection, running servers, exact GGUF file lookup, conversion, and OpenAI-compatible local serving. |
| `/huggingface-trackio` | 📋 Skill | Track and visualize ML training experiments with Trackio. Use when logging metrics during training (Python API), firing alerts for training diagnostics, or retrieving/analyzing logged metrics (CLI). Supports real-time dashboard visualization, alerts with webhooks, HF Space syncing, and JSON output for automation. |
| `/huggingface-papers` | 📋 Skill | Look up and read Hugging Face paper pages in markdown, and use the papers API for structured metadata such as authors, linked models/datasets/spaces, Github repo and project page. Use when the user shares a Hugging Face paper page URL, an arXiv URL or ID, or asks to summarize, explain, or analyze an AI research paper. |
| `/huggingface-tool-builder` | 📋 Skill | Use this skill when the user wants to build tool/scripts or achieve a task where using data from the Hugging Face API would help. This is especially useful when chaining or combining API calls or the task will be repeated/automated. This Skill creates a reusable script to fetch, enrich or process data. |
| `/hf-mem` | 📋 Skill | Hugging Face CLI to estimate the required memory to load Safetensors or GGUF model weights for inference from the Hugging Face Hub |
| `/huggingface-vision-trainer` | 📋 Skill | Trains and fine-tunes vision models for object detection (D-FINE, RT-DETR v2, DETR, YOLOS), image classification (timm models — MobileNetV3, MobileViT, ResNet, ViT/DINOv3 — plus any Transformers classifier), and SAM/SAM2 segmentation using Hugging Face Transformers on Hugging Face Jobs cloud GPUs. Covers COCO-format dataset preparation, Albumentations augmentation, mAP/mAR evaluation, accuracy metrics, SAM segmentation with bbox/point prompts, DiceCE loss, hardware selection, cost estimation, Trackio monitoring, and Hub persistence. Use when users mention training object detection, image classification, SAM, SAM2, segmentation, image matting, DETR, D-FINE, RT-DETR, ViT, timm, MobileNet, ResNet, bounding box models, or fine-tuning vision models on Hugging Face Jobs. |
| `/hf-cli` | 📋 Skill | Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing models, datasets, spaces, buckets, repos, papers, jobs, and more on the Hugging Face Hub. Use when: handling authentication; managing local cache; managing Hugging Face Buckets; running or scheduling jobs on Hugging Face infrastructure; managing Hugging Face repos; discussions and pull requests; browsing models, datasets and spaces; reading, searching, or browsing academic papers; managing collections; querying datasets; configuring spaces; setting up webhooks; or deploying and managing HF Inference Endpoints. Make sure to use this skill whenever the user mentions 'hf', 'huggingface', 'Hugging Face', 'huggingface-cli', or 'hugging face cli', or wants to do anything related to the Hugging Face ecosystem and to AI and ML in general. Also use for cloud storage needs like training checkpoints, data pipelines, or agent traces. Use even if the user doesn't explicitly ask for a CLI command. Replaces the deprecated `huggingface-cli`. |
| `/huggingface-datasets` | 📋 Skill | Use this skill for Hugging Face Dataset Viewer API workflows that fetch subset/split metadata, paginate rows, search text, apply filters, download parquet URLs, and read size or statistics. |
| `/huggingface-best` | 📋 Skill | Use when the user asks about finding the best, top, or recommended model for a task, wants to know what AI model to use, or wants to compare models by benchmark scores. Triggers on: "best model for X", "what model should I use for", "top models for [task]", "which model runs on my laptop/machine/device", "recommend a model for", "what LLM should I use for", "compare models for", "what's state of the art for", or any question about choosing an AI model for a specific use case. Always use this skill when the user wants model recommendations or comparisons, even if they don't explicitly mention HuggingFace or benchmarks. |
| `/huggingface-lora-space-builder` | 📋 Skill | Build and publish a Gradio demo on Hugging Face Spaces for a user-provided LoRA. Use when someone asks to create, generate, ship, or publish a Space, demo, Gradio app, or playground for a LoRA — including LoRAs for Qwen-Image, Qwen-Image-Edit, LTX-Video, Wan, FLUX, SDXL, or other diffusion base models. Also triggers when someone describes a LoRA they trained or hosts on the Hub and wants to share it. Covers picking the right base pipeline and `diffusers` inference recipe, designing a UI tailored to the LoRA's task and inputs (Union/multi-task control, edit, video, image, etc.), respecting model-card recommendations (trigger words, steps, guidance, LoRA scale, example inputs), and shipping to ZeroGPU hardware as a private Space by default. |
| `/transformers-js` | 📋 Skill | Use Transformers.js to run state-of-the-art machine learning models directly in JavaScript/TypeScript. Supports NLP (text classification, translation, summarization), computer vision (image classification, object detection), audio (speech recognition, audio classification), and multimodal tasks. Works in browsers and server-side runtimes (Node.js, Bun, Deno) with WebGPU/WASM using pre-trained models from Hugging Face Hub. |
| `/train-sentence-transformers` | 📋 Skill | Train or fine-tune sentence-transformers models across `SentenceTransformer` (bi-encoder; dense or static embedding model; for retrieval, similarity, clustering, classification, paraphrase mining, dedup, multimodal), `CrossEncoder` (reranker; pair scoring for two-stage retrieval / pair classification), and `SparseEncoder` (SPLADE, sparse embedding model; for learned-sparse retrieval). Covers loss selection, hard-negative mining, evaluators, distillation, LoRA, Matryoshka, and Hugging Face Hub publishing. Use for any sentence-transformers training task. |
| `/huggingface-spaces` | 📋 Skill | Build, deploy, and maintain applications on Hugging Face Spaces — Gradio / Docker / Static SDKs, ZeroGPU and dedicated hardware, model loading, debugging, buckets, inference providers, community grants. Use whenever the user asks to create or host an app on Hugging Face, port code onto ZeroGPU, fix a Space that won't build or run, or otherwise work with `hf spaces …`, `@spaces.GPU`, Space README frontmatter, or the `spaces` Python package. |
| `/trl-training` | 📋 Skill | Train and fine-tune transformer language models using TRL (Transformers Reinforcement Learning). Supports SFT, DPO, GRPO, KTO, RLOO and Reward Model training via CLI commands. |

<a id="p-jdtls-lsp"></a>

**jdtls-lsp**（🔍 LSP）

> Java 语言服务器（Eclipse JDT.LS）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__jdtls` | 🔍 LSP | Java language server (Eclipse JDT.LS) for code intelligence。需手动安装: 下载 Eclipse JDT Language Server |
<a id="p-kotlin-lsp"></a>

**kotlin-lsp**（🔍 LSP）

> Kotlin 语言服务器代码智能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__kotlin-lsp` | 🔍 LSP | Kotlin language server for code intelligence。需手动安装: 下载 kotlin-language-server |
<a id="p-laravel-boost"></a>

**laravel-boost**（🔌 MCP）

> Laravel 开发工具包与智能辅助

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__laravel-boost` | 🔌 MCP | Laravel development toolkit MCP server. Provides intelligent assistance for Laravel applications including Artisan commands, Eloquent queries, rout... |
<a id="p-liquid-lsp"></a>

**liquid-lsp**（🔍 LSP）

> Shopify Liquid 模板语言服务器

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__theme-language-server` | 🔍 LSP | LSP integration for Shopify Liquid templates via the Shopify CLI theme language server.。需手动安装: npm install -g theme-language-server |
<a id="p-liquid-skills"></a>

**liquid-skills**（3 Skill）

> Liquid 语言基础与可访问性标准

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/liquid-theme-a11y` | 📋 Skill | Implement WCAG 2.2 accessibility patterns in Shopify Liquid themes. Covers e-commerce-specific components including product cards, carousels, cart drawers, price display, forms, filters, and modals. Use when building accessible theme components, fixing accessibility issues, or reviewing ARIA patterns in .liquid files. |
| `/shopify-liquid-themes` | 📋 Skill | Generate Shopify Liquid theme code (sections, blocks, snippets) with correct schema JSON, LiquidDoc headers, translation keys, and CSS/JS patterns. Use when creating or editing .liquid files for Shopify themes, working with schema, doc, stylesheet, javascript tags, or Shopify Liquid objects/filters/tags. |
| `/liquid-theme-standards` | 📋 Skill | CSS, JavaScript, and HTML coding standards for Shopify Liquid themes. Covers BEM naming inside stylesheet tags, design tokens, CSS custom properties, Web Components for themes, defensive CSS, and progressive enhancement. Use when writing CSS/JS/HTML in .liquid files or theme asset files. |

<a id="p-lovable"></a>

**lovable**（3 Command）

> Lovable 应用构建迭代和部署管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/lovable:db` | ⌨️ Command | Provision or query a Lovable project's Cloud (Postgres) database |
| `/lovable:build` | ⌨️ Command | Build a new Lovable app from a prompt and optionally deploy it |
| `/lovable:iterate` | ⌨️ Command | Send a change request to a Lovable project's agent and review the diff |

<a id="p-lua-lsp"></a>

**lua-lsp**（🔍 LSP）

> Lua 语言服务器代码智能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__lua` | 🔍 LSP | Lua language server for code intelligence。需手动安装: brew install lua-language-server 或 npm install -g lua-language-server |
<a id="p-lumen"></a>

**lumen**（2 Skill）

> 本地语义代码搜索与索引 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/doctor` | 📋 Skill | Run a health check on the bundled Lumen semantic search setup for the current project, verify backend reachability and index freshness, and summarize remediation steps. |
| `/reindex` | 📋 Skill | Refresh or rebuild the bundled Lumen index for the current project, preferring MCP-driven refreshes and using the CLI only for an explicit clean rebuild. |

<a id="p-mcp-apps"></a>

**mcp-apps**（4 Skill）

> MCP Apps SDK 应用创建技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/create-mcp-app` | 📋 Skill | This skill should be used when the user asks to "create an MCP App", "add a UI to an MCP tool", "build an interactive MCP View", "scaffold an MCP App", or needs guidance on MCP Apps SDK patterns, UI-resource registration, MCP App lifecycle, or host integration. Provides comprehensive guidance for building MCP Apps with interactive UIs. |
| `/migrate-oai-app` | 📋 Skill | This skill should be used when the user asks to "migrate from OpenAI Apps SDK", "convert OpenAI App to MCP", "port from window.openai", "migrate from skybridge", "convert openai/outputTemplate", or needs guidance on converting OpenAI Apps SDK applications to MCP Apps SDK. Provides step-by-step migration guidance with API mapping tables. |
| `/convert-web-app` | 📋 Skill | This skill should be used when the user asks to "add MCP App support to my web app", "turn my web app into a hybrid MCP App", "make my web page work as an MCP App too", "wrap my existing UI as an MCP App", "convert iframe embed to MCP App", "turn my SPA into an MCP App", or needs to add MCP App support to an existing web application while keeping it working standalone. Provides guidance for analyzing existing web apps and creating a hybrid web + MCP App with server-side tool and resource registration. |
| `/add-app-to-server` | 📋 Skill | This skill should be used when the user asks to "add an app to my MCP server", "add UI to my MCP server", "add a view to my MCP tool", "enrich MCP tools with UI", "add interactive UI to existing server", "add MCP Apps to my server", or needs to add interactive UI capabilities to an existing MCP server that already has tools. Provides guidance for analyzing existing tools and adding MCP Apps UI resources. |

<a id="p-mcp-server-dev"></a>

**mcp-server-dev**（3 Skill）

> MCP 服务器设计与构建技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/build-mcpb` | 📋 Skill | This skill should be used when the user wants to "package an MCP server", "bundle an MCP", "make an MCPB", "ship a local MCP server", "distribute a local MCP", discusses ".mcpb files", mentions bundling a Node or Python runtime with their MCP server, or needs an MCP server that interacts with the local filesystem, desktop apps, or OS and must be installable without the user having Node/Python set up. |
| `/build-mcp-app` | 📋 Skill | This skill should be used when the user wants to build an "MCP app", add "interactive UI" or "widgets" to an MCP server, "render components in chat", build "MCP UI resources", make a tool that shows a "form", "picker", "dashboard" or "confirmation dialog" inline in the conversation, or mentions "apps SDK" in the context of MCP. Use AFTER the build-mcp-server skill has settled the deployment model, or when the user already knows they want UI widgets. |
| `/build-mcp-server` | 📋 Skill | This skill should be used when the user asks to "build an MCP server", "create an MCP", "make an MCP integration", "wrap an API for Claude", "expose tools to Claude", "make an MCP app", or discusses building something with the Model Context Protocol. It is the entry point for MCP server development — it interrogates the user about their use case, determines the right deployment model (remote HTTP, MCPB, local stdio), picks a tool-design pattern, and hands off to specialized skills. |

<a id="p-mcp-tunnels"></a>

**mcp-tunnels**（1 Command）

> Anthropic MCP 隧道连接私有服务器

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/mcp-tunnels:create-docker-mcp-tunnel` | ⌨️ Command | Stand up an Anthropic MCP tunnel locally with Docker Compose so Claude can call a private MCP server (manual-credentials quickstart). |

<a id="p-mercadopago"></a>

**mercadopago**（4 Skill、1 Agent、3 Command）

> Mercado Pago 全产品支付集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/mercadopago:mp-integrate` | 📋 Skill | Scaffold a Mercado Pago integration via the mp-integrate wizard. Supports every product (Checkout Pro, Checkout API, Bricks, QR, Point, Subscriptions, Marketplace, Wallet Connect, Money Out, SmartApps). |
| `/mp-webhooks` | 📋 Skill | Configure, simulate, and validate Mercado Pago webhooks. Wraps the MCP webhook tools (save_webhook, simulate_webhook, notifications_history_diagnostics) and provides the HMAC-SHA256 signature validation pattern that every receiver must implement. Use when adding, debugging, or hardening notification handling. |
| `/mercadopago:mp-review` | 📋 Skill | Review a Mercado Pago integration against the official quality checklist (live from MCP) and a fixed cross-cutting security checklist. |
| `/mp-test-setup` | 📋 Skill | Create test users and add funds to them for Mercado Pago testing. Wraps create_test_user and add_money_test_user from the MCP. Clarifies that all credentials (including test users) use the APP_USR- prefix — there is no longer a TEST- sandbox. |
| mp-integration-expert | 🤖 Agent | Use when implementing, reviewing, or debugging any Mercado Pago payment integration. Routes the request to one of four skills (mp-integrate, mp-webhooks, mp-test-setup, mp-review) and uses the Mercado Pago MCP server for live API data. The MCP must always be connected — there is no offline mode. |
| `/mercadopago:mp-connect` | ⌨️ Command | Verify or manually trigger Mercado Pago MCP authentication |
| `/mercadopago:mp-integrate` | ⌨️ Command | Scaffold a Mercado Pago integration via the mp-integrate wizard. Supports every product (Checkout Pro, Checkout API, Bricks, QR, Point, Subscriptions, Marketplace, Wallet Connect, Money Out, SmartApps). |
| `/mercadopago:mp-review` | ⌨️ Command | Review a Mercado Pago integration against the official quality checklist (live from MCP) and a fixed cross-cutting security checklist. |

<a id="p-microsoft-docs"></a>

**microsoft-docs**（3 Skill）

> 微软官方文档与 API 参考访问

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/microsoft-docs` | 📋 Skill | Understand Microsoft technologies by querying official documentation. Use whenever the user asks how something works, wants tutorials, needs configuration options, limits, quotas, or best practices for any Microsoft technology (Azure, .NET, M365, Windows, Power Platform, etc.)—even if they don't mention "docs." If the question is about understanding a concept rather than writing code, this is the right skill. |
| `/microsoft-code-reference` | 📋 Skill | Find working code samples, verify API signatures, and fix Microsoft SDK errors using official docs. Use whenever the user is writing, debugging, or reviewing code that touches any Microsoft SDK, .NET library, Azure client library, or Microsoft API—even if they don't ask for a "reference." Catches hallucinated methods, wrong signatures, and deprecated patterns. If the task involves producing or fixing Microsoft-related code, this is the right skill. |
| `/microsoft-skill-creator` | 📋 Skill | Create agent skills for Microsoft technologies using official documentation. Use whenever the user wants to build, generate, or scaffold a skill for any Microsoft technology (Azure, .NET, M365, VS Code, Bicep, etc.)—even phrased casually like "make a skill for Cosmos DB." Investigates the topic via official docs, then generates a hybrid skill with essential knowledge stored locally and dynamic lookups for depth. |

<a id="p-migration-to-aws"></a>

**migration-to-aws**（1 Skill）

> GCP 到 AWS 迁移规划指导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/gcp-to-aws` | 📋 Skill | Migrate workloads from Google Cloud Platform to AWS — including AI and agentic workloads regardless of cloud provider. Triggers on: migrate from GCP, GCP to AWS, move off Google Cloud, migrate Terraform to AWS, migrate Cloud SQL to RDS, migrate GKE to EKS, migrate Cloud Run to Fargate, Google Cloud migration, migrate from OpenAI to Bedrock, move off OpenAI, switch from ChatGPT API to AWS, migrate from Gemini to Bedrock, migrate LangChain to Bedrock, migrate LangGraph to AWS, migrate agentic workloads to AWS, move AI workloads to AWS, migrate my AI app to AWS. Runs a 6-phase process: discover GCP resources from Terraform files, app code, or billing exports, clarify migration requirements, design AWS architecture, estimate costs, generate migration artifacts, and collect optional feedback. Clarify must finish before Design, Estimate, or Generate. Includes AI provider migration guidance (for example, OpenAI to Amazon Bedrock) by selecting closest-fit Bedrock model families for required modality, latency/quality targets, context windows, and cost constraints. Model mapping is compatibility-guided, not 1:1 parity; validate prompts, tool-calling behavior, and eval metrics before cutover. Do not use for: Azure or on-premises migrations to AWS, AWS-to-GCP reverse migration, general AWS architecture advice without migration intent, GCP-to-GCP refactoring, or multi-cloud deployments that do not involve migrating off GCP. |

<a id="p-mintlify"></a>

**mintlify**（1 Skill）

> Mintlify 文档站点构建与美化

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/mintlify` | 📋 Skill | Comprehensive reference for building Mintlify documentation sites. Use when creating pages, configuring docs.json, adding components, setting up navigation, or working with API references. Routes to detailed reference files for all components and configuration options. |

<a id="p-netlify-skills"></a>

**netlify-skills**（13 Skill）

> Netlify 平台全栈开发技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/netlify-ai-gateway` | 📋 Skill | Reference for Netlify AI Gateway — the managed proxy that routes calls to OpenAI, Anthropic, and Google Gemini SDKs without provider API keys. Use this skill any time the user wants to add AI on a Netlify site (chat, completion, reasoning, image generation, image-to-image edit/stylize), choose or change a model, wire up the OpenAI / Anthropic / @google/genai SDK, decide which provider to use for an image-gen feature (it's Gemini-only on the gateway), or debug "model not found" / "API key missing" against the gateway. Required reading before pinning a model — the gateway exposes a curated subset, not every provider model. |
| `/netlify-frameworks` | 📋 Skill | Guide for deploying web frameworks on Netlify. Use when setting up a framework project (Vite/React, Astro, TanStack Start, Next.js, Nuxt, SvelteKit, Remix) for Netlify deployment, configuring adapters or plugins, or troubleshooting framework-specific Netlify integration. Covers what Netlify needs from each framework and how adapters handle server-side rendering. |
| `/netlify-cli-and-deploy` | 📋 Skill | Guide for using the Netlify CLI and deploying sites. Use when installing the CLI, linking sites, deploying (Git-based or manual), managing environment variables, or running local development. Covers netlify dev, netlify deploy, Git vs non-Git workflows, and environment variable management. |
| `/netlify-database` | 📋 Skill | Guide for using Netlify Database — the GA managed Postgres product built into Netlify. Use when a project needs any kind of dynamic, structured, or relational data. Covers provisioning via @netlify/database, Drizzle ORM (@beta) setup, migrations, preview branching, and safe production data handling. Blobs is only for file/asset storage — any dynamic data belongs in the database. |
| `/netlify-forms` | 📋 Skill | Guide for using Netlify Forms for HTML form handling. Use when adding contact forms, feedback forms, file upload forms, or any form that should be collected by Netlify. Covers the data-netlify attribute, spam filtering, AJAX submissions, file uploads, notifications, and the submissions API. |
| `/netlify-image-cdn` | 📋 Skill | Guide for using Netlify Image CDN for image optimization and transformation. Use when serving optimized images, creating responsive image markup, setting up user-uploaded image pipelines, or configuring image transformations. Covers the /.netlify/images endpoint, query parameters, remote image allowlisting, clean URL rewrites, and composing uploads with Functions + Blobs. |
| `/netlify-caching` | 📋 Skill | Guide for controlling caching on Netlify's CDN. Use when configuring cache headers, setting up stale-while-revalidate, implementing on-demand cache purge, or understanding Netlify's CDN caching behavior. Covers Cache-Control, Netlify-CDN-Cache-Control, cache tags, durable cache, and framework-specific caching patterns. |
| `/netlify-deploy` | 📋 Skill | Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys. |
| `/netlify-identity` | 📋 Skill | Use when the task involves authentication, user signups, logins, password recovery, OAuth providers, role-based access control, or protecting routes and functions. Always use `@netlify/identity`. Never use `netlify-identity-widget` or `gotrue-js` — they are deprecated. |
| `/netlify-functions` | 📋 Skill | Guide for writing Netlify serverless functions. Use when creating API endpoints, background processing, scheduled tasks, or any server-side logic using Netlify Functions. Covers modern syntax (default export + Config), TypeScript, path routing, background functions, scheduled functions, streaming, and method routing. |
| `/netlify-config` | 📋 Skill | Reference for netlify.toml configuration. Use when configuring build settings, redirects, rewrites, headers, deploy contexts, environment variables, or any site-level configuration. Covers the complete netlify.toml syntax including redirects with splats/conditions, headers, deploy contexts, functions config, and edge functions config. |
| `/netlify-blobs` | 📋 Skill | Guide for using Netlify Blobs for file and asset storage — images, documents, uploads, exports, cached binary artifacts. Covers getStore(), CRUD operations, metadata, listing, deploy-scoped vs site-scoped stores, and local development. Do NOT use Blobs as a dynamic data store — use Netlify Database for that. |
| `/netlify-edge-functions` | 📋 Skill | Guide for writing Netlify Edge Functions. Use when building middleware, geolocation-based logic, request/response manipulation, authentication checks, A/B testing, or any low-latency edge compute. Covers Deno runtime, context.next() middleware pattern, geolocation, and when to choose edge vs serverless. |

<a id="p-netsuite-suitecloud"></a>

**netsuite-suitecloud**（3 Skill）

> NetSuite SuiteCloud 开发平台指导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/netsuite-ai-connector-instructions` | 📋 Skill | NetSuite Intelligence skill — teaches AI the correct tool selection order, output formatting, domain knowledge, multi-subsidiary and currency handling, and SuiteQL safety checklist for any AI + NetSuite AI Service Connector session. |
| `/netsuite-sdf-roles-and-permissions` | 📋 Skill | Use when generating or reviewing NetSuite SDF permission configurations such as customrole XML, script deployment permissions, permkey values, permlevel choices, run-as role design, and least-privilege access. Confirms exact ADMI_ / LIST_ / REGT_ / REPO_ / TRAN_ permission IDs, distinguishes standard permissions from customrecord_* script IDs, and validates permissions against bundled NetSuite reference data. |
| `/netsuite-uif-spa-reference` | 📋 Skill | Use when building, modifying, or debugging NetSuite UIF SPA components. Provides API/type lookup for `@uif-js/core` and `@uif-js/component` (constructors, methods, props, enums, hooks, and component options). |

<a id="p-nvidia-skills"></a>

**nvidia-skills**（11 Skill）

> NVIDIA 加速计算工作流（cuOpt 等）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cuopt-user-rules` | 📋 Skill | Base rules for end users calling NVIDIA cuOpt (routing/LP/MILP/QP/install/server). Not for cuOpt internals — use cuopt-developer for those. |
| `/aiq-deploy` | 📋 Skill | Use when asked to install, deploy, run, validate, troubleshoot, or stop NVIDIA AI-Q Blueprint infrastructure. |
| `/nemoclaw-user-get-started` | 📋 Skill | Installs NemoClaw, launches a sandbox, and runs the first agent prompt. Use when onboarding, installing, or launching a NemoClaw sandbox for the first time. Trigger keywords - nemoclaw quickstart, install nemoclaw openclaw sandbox, nemohermes quickstart, hermes agent nemoclaw, run hermes openshell sandbox, nemoclaw prerequisites, nemoclaw supported platforms, nemoclaw hardware software, nemoclaw windows wsl2 setup, nemoclaw install windows docker desktop. |
| `/dynamo-router-starter` | 📋 Skill | Start or patch Dynamo router modes and run router endpoint smoke checks. Use for round-robin, KV-aware, least-loaded, or device-aware routing setup; use recipe-runner for recipe deployment and troubleshoot for failure diagnosis. |
| `/omniverse-cad-to-simready` | 📋 Skill | Coordinate the end-to-end CAD/source-asset to SimReady workflow. Use for broad requests such as CAD to SimReady, source asset to simulation-ready USD, or prop packaging that require conversion, material/physics assignment, SimReady conformance, validation, and optional package creation; deploy or verify Content Agents services first when property assignment is enabled; route single-stage work through nested references. |
| `/dynamo-interconnect-check` | 📋 Skill | Validate that a Dynamo deployment's NIXL/UCX/NCCL interconnect is ready for disaggregated serving over RDMA/NVLink. Use after recipe-runner brings a deployment up (especially disagg/multi-node) to confirm the KV transport is correct; use troubleshoot for diagnosing already-failed pods. |
| `/physical-ai-neural-reconstruction` | 📋 Skill | Router for NVIDIA NuRec/NRE: USDZ rendering, NCore conversion, 3DGS, gRPC sensor sim, PhysicalAI HF datasets. Do NOT use for SimReady or infra setup. |
| `/omniverse-usd-performance-tuning` | 📋 Skill | Top-level workflow skill for USD performance diagnosis and optimization. Use for slow loading, high memory, low FPS, or 'optimize my scene' requests; delegates auth/runtime setup to Phase 0 owners. |
| `/physical-ai-infrastructure-setup-and-resilient-scaling` | 📋 Skill | Use when the user wants to set up, scale, validate, or harden NVIDIA physical AI infrastructure for synthetic data generation workflows across local MicroK8s or Azure AKS, including Kubernetes clusters, inference endpoint deployment, OSMO deployment, workload submission readiness, and infrastructure failure recovery. Trigger keywords: physical ai infrastructure, resilient scaling, SDG infrastructure, microk8s, azure aks, NVCF deployment, NIM Operator, OSMO deploy, workflow scaling. Don't trigger for: OSMO log summarization or workload-only operations unless infrastructure setup, scaling, validation, or recovery is requested. |
| `/aiq-research` | 📋 Skill | Use when asked to run deep research or AI-Q research through a reachable NVIDIA AI-Q Blueprint backend. |
| `/omniverse-realtime-viewer` | 📋 Skill | Use as the top-level router for Omniverse Realtime Viewer USD app requests and focused viewer reference documents. |

<a id="p-oracle-ai-data-platform-workbench-spark-connectors"></a>

**oracle-ai-data-platform-workbench-spark-connectors**（25 Skill）

> Oracle AI 数据平台 Spark 连接器

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-excel` | 📋 Skill | Read Excel (.xlsx, .xls) files into a Spark DataFrame from an AIDP notebook. Use when the user mentions Excel, .xlsx, .xls, or has spreadsheet files in a Volume / Object Storage bucket. Two paths — the `com.crealytics.spark.excel` Spark format (cluster jar required) and a `pandas → CSV → spark.read.csv` fallback that needs no jars. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-mysql` | 📋 Skill | Read or write MySQL or OCI MySQL HeatWave from an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions MySQL, HeatWave, MySQL Database Service, MDS, or has a MySQL host/port. Auth is host/port + user/password. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-fusion-rest` | 📋 Skill | Pull data from Oracle Fusion ERP / HCM / SCM REST APIs into a Spark DataFrame from an AIDP notebook. Use when the user mentions Fusion ERP, Fusion REST API, FA REST, Cloud ERP, or wants live data from a Fusion pod. HTTP Basic auth only. For volumes >499 rows/page or bulk extracts, route to aidp-fusion-bicc. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-postgresql` | 📋 Skill | Read or write PostgreSQL from an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions PostgreSQL, Postgres, "psql", or has a Postgres host/port to connect to. HTTP-style auth — host/port + user/password. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-iceberg` | 📋 Skill | Read and write Apache Iceberg tables backed by OCI Object Storage from an AIDP notebook. Use when the user mentions Iceberg, Apache Iceberg, time travel, snapshots, schema evolution, partition evolution, or wants ACID transactions on data lake files. Uses the Iceberg Hadoop catalog on `oci://` — auth is implicit via the workspace IAM identity. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-peoplesoft` | 📋 Skill | Read from Oracle PeopleSoft into a Spark DataFrame in an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions PeopleSoft, PSFT, HCM, FSCM, Campus Solutions, or has a PeopleSoft host/port. Auth is host/port + database name + user/password. Read-only. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-alh` | 📋 Skill | Connect from an AIDP notebook to Oracle AI Lakehouse (ALH), Autonomous Data Warehouse (ADW), or Autonomous Transaction Processing (ATP) via Spark JDBC. Use when the user mentions ALH, AI Lakehouse, ADW, ATP, Autonomous Database, or wants to query a 26ai-backed Oracle Autonomous DB from Spark. Covers wallet (mTLS), IAM DB-Token (with on-executor refresh for long jobs), and API Key auth paths. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-rest-generic` | 📋 Skill | Pull data from any REST API into a Spark DataFrame using the AIDP `aidataplatform` Generic REST connector. Use when the user has a non-Fusion / non-EPM / non-Essbase REST endpoint with a `manifest.url` describing the schema. Auth is HTTP Basic with derived properties driving query parameters. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-fusion-bicc` | 📋 Skill | Pull a Fusion BICC bulk extract into a Spark DataFrame from an AIDP notebook. Use when the user mentions BICC, Fusion bulk extract, BI Cloud Connector, PVO, or needs >50k rows from Fusion. The recommended path uses AIDP's built-in `spark.read.format("aidataplatform")` connector (matches the official Oracle AIDP sample). HTTP Basic auth. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-sqlserver` | 📋 Skill | Read or write Microsoft SQL Server from an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions SQL Server, MSSQL, Azure SQL Database, or has a TDS host/port. Auth is host/port + database + user/password. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-oracle-db` | 📋 Skill | Read or write an Oracle Database (Compute / Base DB / on-prem / Oracle 19c, 21c, 23ai, 26ai non-Autonomous) from an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions Oracle Database, generic Oracle DB, on-prem Oracle, plain Oracle JDBC, port 1521, non-Autonomous Oracle. Read-write. Auth is host/port + database name + user/password. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-aws-s3` | 📋 Skill | Read and write AWS S3 (`s3a://`) from an AIDP notebook. Use when the user mentions S3, AWS S3 bucket, s3a, or has AWS access keys. Auth is access key + secret key via the Hadoop S3A connector. boto3 is also available for non-Spark management operations (list, copy). |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-snowflake` | 📋 Skill | Read or write Snowflake from an AIDP notebook via Spark using the Snowflake Spark connector. Use when the user mentions Snowflake, Snowflake warehouse, sfUrl, sfUser, or wants to migrate from Snowflake. Auth is sfUser + sfPassword over the Snowflake Spark connector (`net.snowflake.spark.snowflake`). |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-essbase` | 📋 Skill | Run an MDX query against an Oracle Essbase 21c cube and materialize the result as a Spark DataFrame in an AIDP notebook. Use when the user mentions Essbase, MDX, Essbase 21c, OLAP cube, or wants to read cube data into Spark. Auth is HTTP Basic. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-streaming-kafka` | 📋 Skill | Consume an OCI Streaming stream from an AIDP notebook via Spark structured streaming (Kafka-compat). Use when the user mentions OCI Streaming, Kafka on OCI, stream pool, structured streaming, or wants to read Kafka messages into Spark. Auth is SASL/PLAIN with an OCI auth token. Pattern matches the official Oracle AIDP sample. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-connectors-overview` | 📋 Skill | Help the user pick the right connector skill for their data source from an AIDP notebook. Use as a router when the user mentions multiple sources, isn't sure which connector applies, or asks "how do I connect to X from AIDP". Covers 23 data sources — Oracle Autonomous DB family (ALH/ADW/ATP), generic Oracle DB, ExaCS, PeopleSoft, Siebel, Fusion ERP/BICC, EPM Cloud, Essbase, OCI Streaming, Object Storage, Iceberg, plus PostgreSQL, MySQL/HeatWave, SQL Server, Hive, Snowflake, Azure ADLS, AWS S3, Salesforce, generic REST, custom JDBC, Excel. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-hive` | 📋 Skill | Read or write Apache Hive from an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions Hive, HiveServer2, HS2, HCatalog, or has a Hive metastore host/port. Auth is host/port + user/password. Read-write. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-siebel` | 📋 Skill | Read from Oracle Siebel CRM into a Spark DataFrame in an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions Siebel, Siebel CRM, S_CONTACT, S_ORG_EXT, or has a Siebel host/port. Auth is host/port + database name + user/password. Read-only. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-object-storage` | 📋 Skill | Read and write OCI Object Storage natively from an AIDP notebook using the `oci://` URI scheme. Use when the user mentions OCI Object Storage, "oci://", external volumes, external tables backed by Object Storage, CSV/Parquet/JSON/Delta files in a bucket, or wants to land data in OCI buckets. Auth is implicit via the workspace's IAM identity — no keys in the notebook. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-exacs` | 📋 Skill | Connect from an AIDP notebook to Oracle Exadata Cloud Service (ExaCS) via Spark JDBC. Use when the user mentions ExaCS, Exadata, Exadata Cloud, RAC SCAN listener, or has a private-subnet Oracle DB. Auth is plain user/password on TCP 1521 with server-enforced AES256 Native Network Encryption (live-validated against Oracle 23ai). Wallet TCPS and IAM DB-Token are not supported by AIDP notebooks for ExaCS. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-epm-cloud` | 📋 Skill | Run a Planning data-slice export against Oracle EPM Cloud (Planning / EPBCS) and materialize as a Spark DataFrame in an AIDP notebook. Use when the user mentions EPM Cloud, EPBCS, Hyperion Planning, planning app, MDX export, or wants Planning data in Spark. HTTP Basic auth with identity-domain-prefixed username. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-azure-adls` | 📋 Skill | Read and write Azure Data Lake Storage Gen2 (`abfss://`) from an AIDP notebook. Use when the user mentions ADLS, Azure Data Lake, abfss, or wants to ingest from a multi-cloud Azure source. Auth is OAuth client-credentials (Service Principal client_id + secret + tenant). |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-jdbc-custom` | 📋 Skill | Connect to ANY database that has a JDBC driver from an AIDP notebook using Spark's native `format("jdbc")`. Use when the user mentions a DB without a dedicated AIDP connector — SQLite, ClickHouse, DuckDB, generic JDBC URL — or wants to use a custom JDBC driver they uploaded. Auth is driver-specific. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-connectors-bootstrap` | 📋 Skill | First-time setup. Use when the user wants to install/upload the AIDP Spark connectors helper package into their AIDP workspace, or has just installed this plugin and asks "how do I set it up", "first-time setup", "install the helpers", "bootstrap aidp connectors". Drives the AIDP MCP tools to push the helper package to /Workspace/Shared/ and runs a sanity import. |
| `/oracle-ai-data-platform-workbench-spark-connectors:aidp-salesforce` | 📋 Skill | Read from Salesforce into a Spark DataFrame in an AIDP notebook via the AIDP `aidataplatform` Spark format handler. Use when the user mentions Salesforce, SFDC, Sales Cloud, Service Cloud, Account, Opportunity, Lead, sObject, SOQL. Auth is host/port + user/password. Read-only. |

<a id="p-outputai"></a>

**outputai**（49 Skill、5 Agent）

> Output.ai 工作流开发工具包

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/output-dev-agent-class` | 📋 Skill | Use the Agent class for multi-step tool loops, conversation history, and reusable LLM agents. Use when building agents with skills, structured output, or stateful conversations. |
| `/output-workflow-start` | 📋 Skill | Start an Output SDK workflow asynchronously without waiting for completion. Use when starting long-running workflows, getting a workflow ID for later monitoring, running workflows in the background, or executing multiple workflows in parallel. |
| `/output-workflow-stop` | 📋 Skill | Stop a running Output SDK workflow execution. Use when cancelling a workflow, stopping a long-running process, terminating a stuck workflow, or when you need to abort a workflow in progress. |
| `/output-plan-workflow` | 📋 Skill | Use when the user asks to create, build, generate, scaffold, or plan a new workflow. Orchestrates the full planning process including architecture, steps, prompts, evaluators, and testing strategy using specialized subagents. |
| `/output-meta-post-flight` | 📋 Skill | Post-flight validation for Output SDK workflow operations. Systematic verification of step completion, convention compliance, quality validation, and deliverable verification. |
| `/output-services-check` | 📋 Skill | Verify Output SDK development services are running. Use when debugging workflows, starting development, encountering connection errors, services may be down, or when you see "ECONNREFUSED" or timeout errors. |
| `/output-error-zod-import` | 📋 Skill | Fix Zod schema import issues in Output SDK workflows. Use when seeing "incompatible schema" errors, type errors at step boundaries, schema validation failures, or when schemas don't match between steps. |
| `/output-workflow-status` | 📋 Skill | Check the status of an Output SDK workflow execution. Use when monitoring a running workflow, checking if a workflow completed, or determining workflow state (RUNNING, COMPLETED, FAILED, TERMINATED). |
| `/output-dev-evaluator-function` | 📋 Skill | Create evaluator functions in evaluators.ts for Output SDK workflows. Use when implementing quality assessment, validation logic, or content evaluation. |
| `/output-dev-types-file` | 📋 Skill | Create types.ts files with Zod schemas for Output SDK workflows. Use when defining input/output schemas, creating type definitions, or fixing schema-related errors. |
| `/output-dev-model-selection` | 📋 Skill | Pick the right LLM model for an Output SDK prompt file. Use when writing a new .prompt file, reviewing a model choice, or upgrading a stale model. Walks through priority (reasoning/balance/speed/cost), provider selection, and a live lookup against the Vercel AI Gateway model index. |
| `/output-workflow-trace-file` | 📋 Skill | Read and render the output of a local Output SDK workflow trace file as clean readable markdown. Use when the user wants to view what a recent workflow produced, see the result from a local trace file, or render trace output as a document. |
| `/output-meta-project-context` | 📋 Skill | Comprehensive guide to Output.ai Framework for building durable, LLM-powered workflows orchestrated by Temporal. Covers project structure, workflow patterns, steps, LLM integration, HTTP clients, CLI commands, and the full inventory of available agents, commands, and skills. |
| `/output-migrate` | 📋 Skill | Upgrade a project between versions of the Output framework. Use when the user asks to upgrade, migrate, or move to a newer Output version. Detects the current @outputai/* version in the project, fetches the matching migration guide from docs.output.ai, applies the changes, and verifies the project still type-checks. |
| `/output-workflow-run` | 📋 Skill | Execute an Output SDK workflow synchronously and wait for the result. Use when running a workflow and needing immediate results, testing workflow execution, or getting the output directly in the terminal. |
| `/output-build-workflow` | 📋 Skill | Implement an Output SDK workflow from a plan document. Use when the user asks to build, implement, or code a workflow from an existing plan, or after output-plan-workflow has produced a plan and the user is ready to build. |
| `/output-workflow-trace` | 📋 Skill | Analyze Output SDK workflow execution traces. Use when debugging a specific workflow, examining step failures, analyzing input/output data, understanding execution flow, or when you have a workflow ID to investigate. |
| `/output-dev-prompt-file` | 📋 Skill | Create .prompt files for LLM operations in Output SDK workflows. Use when designing prompts, configuring LLM providers, or using Liquid.js templating. |
| `/output-workflow-result` | 📋 Skill | Get the result of an Output SDK workflow execution. Use when retrieving the output of a completed workflow, getting the return value, or checking what a workflow produced after async execution. |
| `/output-dev-scenario-file` | 📋 Skill | Create test scenario JSON files for Output SDK workflows. Use when creating test inputs, documenting expected behaviors, or setting up workflow testing. |
| `/output-error-http-client` | 📋 Skill | Fix HTTP client misuse in Output SDK steps. Use when seeing untraced requests, missing error details, axios-related errors, or when HTTP calls aren't being properly logged and retried. |
| `/output-dev-workflow-function` | 📋 Skill | Create workflow.ts files for Output SDK workflows. Use when defining workflow functions, orchestrating steps, or fixing workflow structure issues. |
| `/output-credentials-init` | 📋 Skill | Initialize encrypted credentials for an Output.ai project. Use when setting up credentials for the first time, adding environment-specific credentials, or adding per-workflow credentials. |
| `/output-eval-dataset-design` | 📋 Skill | Design diverse eval datasets using dimension-based variation. Use when bootstrapping eval datasets, when real traces are sparse, or when existing datasets miss edge cases. |
| `/output-dev-upgrade-prompt-models` | 📋 Skill | Bulk-upgrade the model field across .prompt files to the latest version of each prompt's existing family. Use when prompt models have drifted (eg sonnet-4 → sonnet-4-6), after a long pause between framework updates, or as part of a periodic model-freshness pass. Within-family only — never changes provider or tier. |
| `/output-error-try-catch` | 📋 Skill | Fix try-catch anti-pattern in Output SDK workflows. Use when retries aren't working, errors are being swallowed, seeing unexpected FatalError wrapping, or when step failures don't trigger retry policies. |
| `/output-dev-code-style` | 📋 Skill | Code style conventions for Output SDK workflow projects. Use when writing or reviewing any TypeScript/JavaScript code. Discovers the project's own linting rules first; falls back to Output SDK conventions when no linter is configured. |
| `/output-dev-create-skeleton` | 📋 Skill | Generate workflow skeleton files using the Output SDK CLI. Use when starting a new workflow, scaffolding project structure, or understanding the generated file layout. |
| `/output-eval-audit` | 📋 Skill | Audit an existing eval suite for trustworthiness. Use when inheriting evals, suspecting evals miss real failures, or after significant pipeline changes. |
| `/output-eval-error-analysis` | 📋 Skill | Systematically review workflow traces to identify failure modes before building evaluators. Use when starting an eval project, after significant pipeline changes, or when production quality drops. |
| `/output-error-missing-schemas` | 📋 Skill | Fix missing schema definitions in Output SDK steps. Use when seeing type errors, undefined properties at step boundaries, validation failures, or when step inputs/outputs aren't being properly typed. |
| `/output-workflow-runs-list` | 📋 Skill | List Output SDK workflow execution history. Use when finding failed runs, reviewing past executions, identifying workflow IDs for debugging, filtering runs by workflow type, or investigating recent workflow activity. |
| `/output-dev-step-function` | 📋 Skill | Create step functions in steps.ts for Output SDK workflows. Use when implementing I/O operations, error handling, HTTP requests, or LLM calls. |
| `/output-error-nondeterminism` | 📋 Skill | Fix non-determinism errors in Output SDK workflows. Use when seeing replay failures, inconsistent results between runs, "non-deterministic" error messages, or workflows behaving differently on retry. |
| `/output-dev-skill-file` | 📋 Skill | Create .md skill files for Output framework's lazy-loaded instruction system. Use when adding skills to prompts, configuring skill loading, or debugging skill resolution. |
| `/output-eval-judge-prompt` | 📋 Skill | Design effective LLM judge .prompt files for evaluators. Use when creating judgeVerdict/judgeScore/judgeLabel prompts, or when existing judges produce unreliable results. |
| `/output-meta-pre-flight` | 📋 Skill | Pre-flight validation checks for Output SDK workflow operations. Ensures conventions are followed, requirements are gathered, and quality gates are passed before workflow execution. |
| `/output-workflow-reset` | 📋 Skill | Re-run an Output SDK workflow from after a specific completed step, creating a new run that replays up to that point and re-executes subsequent steps. Use when iterating on a later step's prompt or logic without re-running the entire workflow, or when recovering from a failure that only affects steps after a known-good point. |
| `/output-error-direct-io` | 📋 Skill | Fix direct I/O in Output SDK workflow functions. Use when workflow hangs, returns undefined, shows "workflow must be deterministic" errors, or when HTTP/API calls are made directly in workflow code. |
| `/output-dev-http-client-create` | 📋 Skill | Create shared HTTP clients in src/shared/clients/ for Output SDK workflows. Use when integrating external APIs, creating service wrappers, or standardizing HTTP operations. |
| `/output-dev-folder-structure` | 📋 Skill | Workflow folder structure conventions for Output SDK. Use when creating new workflows, organizing workflow files, or understanding the standard project layout. |
| `/output-credentials-edit` | 📋 Skill | View and edit encrypted credentials in an Output.ai project. Use when adding secrets, updating API keys, verifying credential values, or retrieving a specific credential. |
| `/output-dev-workflow-cost` | 📋 Skill | Calculate and display the cost of an Output SDK workflow execution run. Use when checking LLM token costs, API service costs, or total spend for a specific workflow run. |
| `/output-debug-workflow` | 📋 Skill | Debug Output SDK workflow issues. Use when user reports a workflow failing, erroring, hanging, producing wrong results, or asks to debug, troubleshoot, or investigate a workflow execution. |
| `/output-dev-credentials` | 📋 Skill | Store and reference encrypted secrets in Output SDK workflows using @outputai/credentials. Use when integrating API keys, database passwords, or third-party tokens. |
| `/output-workflow-list` | 📋 Skill | List all available Output SDK workflows in the project. Use when discovering what workflows exist, checking workflow names, exploring the project's workflow structure, or when unsure which workflows are available to run. |
| `/output-credentials-env-vars` | 📋 Skill | Wire encrypted credentials to environment variables using the credential: convention. Use when setting up LLM provider keys (ANTHROPIC_API_KEY, OPENAI_API_KEY) or any env var that should come from encrypted credentials. |
| `/output-eval-validate-judge` | 📋 Skill | Validate LLM judges against human labels using TPR/TNR metrics and train/dev/test splits. Use after writing a judge prompt to verify it agrees with human judgment. |
| `/output-dev-eval-testing` | 📋 Skill | Create offline evaluation tests for Output SDK workflows using @outputai/evals. Use when implementing test evaluators with verify(), creating dataset YAML files, building eval workflows, or running workflow tests via CLI. |
| workflow_debugger | 🤖 Agent | - |
| workflow_quality | 🤖 Agent | - |
| workflow_prompt_writer | 🤖 Agent | - |
| workflow_context_fetcher | 🤖 Agent | - |
| workflow_planner | 🤖 Agent | - |

<a id="p-php-lsp"></a>

**php-lsp**（🔍 LSP）

> PHP 语言服务器（Intelephense）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__intelephense` | 🔍 LSP | PHP language server (Intelephense) for code intelligence。需手动安装: npm install -g intelephense |
<a id="p-playground"></a>

**playground**（1 Skill）

> 创建交互式 HTML 实验场 · [📖 详细介绍](playground.md)

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/playground` | 📋 Skill | Creates interactive HTML playgrounds — self-contained single-file explorers that let users configure something visually through controls, see a live preview, and copy out a prompt. Use when the user asks to make a playground, explorer, or interactive tool for a topic. |

<a id="p-plugin-dev"></a>

**plugin-dev**（7 Skill、3 Agent、1 Command）

> Claude Code 插件开发完整工具包

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/plugin-settings` | 📋 Skill | This skill should be used when the user asks about "plugin settings", "store plugin configuration", "user-configurable plugin", ".local.md files", "plugin state files", "read YAML frontmatter", "per-project plugin settings", or wants to make plugin behavior configurable. Documents the .claude/plugin-name.local.md pattern for storing plugin-specific configuration with YAML frontmatter and markdown content. |
| `/skill-development` | 📋 Skill | This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive disclosure, or skill development best practices for Claude Code plugins. |
| `/command-development` | 📋 Skill | This skill should be used when the user asks to "create a slash command", "add a command", "write a custom command", "define command arguments", "use command frontmatter", "organize commands", "create command with file references", "interactive command", "use AskUserQuestion in command", or needs guidance on slash command structure, YAML frontmatter fields, dynamic arguments, bash execution in commands, user interaction patterns, or command development best practices for Claude Code. |
| `/mcp-integration` | 📋 Skill | This skill should be used when the user asks to "add MCP server", "integrate MCP", "configure MCP in plugin", "use .mcp.json", "set up Model Context Protocol", "connect external service", mentions "${CLAUDE_PLUGIN_ROOT} with MCP", or discusses MCP server types (SSE, stdio, HTTP, WebSocket). Provides comprehensive guidance for integrating Model Context Protocol servers into Claude Code plugins for external tool and service integration. |
| `/plugin-structure` | 📋 Skill | This skill should be used when the user asks to "create a plugin", "scaffold a plugin", "understand plugin structure", "organize plugin components", "set up plugin.json", "use ${CLAUDE_PLUGIN_ROOT}", "add commands/agents/skills/hooks", "configure auto-discovery", or needs guidance on plugin directory layout, manifest configuration, component organization, file naming conventions, or Claude Code plugin architecture best practices. |
| `/hook-development` | 📋 Skill | This skill should be used when the user asks to "create a hook", "add a PreToolUse/PostToolUse/Stop hook", "validate tool use", "implement prompt-based hooks", "use ${CLAUDE_PLUGIN_ROOT}", "set up event-driven automation", "block dangerous commands", or mentions hook events (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart, SessionEnd, UserPromptSubmit, PreCompact, Notification). Provides comprehensive guidance for creating and implementing Claude Code plugin hooks with focus on advanced prompt-based hooks API. |
| `/agent-development` | 📋 Skill | This skill should be used when the user asks to "create an agent", "add an agent", "write a subagent", "agent frontmatter", "when to use description", "agent examples", "agent tools", "agent colors", "autonomous agent", or needs guidance on agent structure, system prompts, triggering conditions, or agent development best practices for Claude Code plugins. |
| plugin-validator | 🤖 Agent | Use this agent when the user asks to "validate my plugin", "check plugin structure", "verify plugin is correct", "validate plugin.json", "check plugin files", or mentions plugin validation. Also trigger proactively after user creates or modifies plugin components. Examples: <example> Context: User finished creating a new plugin user: "I've created my first plugin with commands and hooks" assistant: "Great! Let me validate the plugin structure." <commentary> Plugin created, proactively validate to catch issues early. </commentary> assistant: "I'll use the plugin-validator agent to check the plugin." </example> <example> Context: User explicitly requests validation user: "Validate my plugin before I publish it" assistant: "I'll use the plugin-validator agent to perform comprehensive validation." <commentary> Explicit validation request triggers the agent. </commentary> </example> <example> Context: User modified plugin.json user: "I've updated the plugin manifest" assistant: "Let me validate the changes." <commentary> Manifest modified, validate to ensure correctness. </commentary> assistant: "I'll use the plugin-validator agent to check the manifest." </example> |
| skill-reviewer | 🤖 Agent | Use this agent when the user has created or modified a skill and needs quality review, asks to "review my skill", "check skill quality", "improve skill description", or wants to ensure skill follows best practices. Trigger proactively after skill creation. Examples: <example> Context: User just created a new skill user: "I've created a PDF processing skill" assistant: "Great! Let me review the skill quality." <commentary> Skill created, proactively trigger skill-reviewer to ensure it follows best practices. </commentary> assistant: "I'll use the skill-reviewer agent to review the skill." </example> <example> Context: User requests skill review user: "Review my skill and tell me how to improve it" assistant: "I'll use the skill-reviewer agent to analyze the skill quality." <commentary> Explicit skill review request triggers the agent. </commentary> </example> <example> Context: User modified skill description user: "I updated the skill description, does it look good?" assistant: "I'll use the skill-reviewer agent to review the changes." <commentary> Skill description modified, review for triggering effectiveness. </commentary> </example> |
| agent-creator | 🤖 Agent | Use this agent when the user asks to "create an agent", "generate an agent", "build a new agent", "make me an agent that...", or describes agent functionality they need. Trigger when user wants to create autonomous agents for plugins. Examples: <example> Context: User wants to create a code review agent user: "Create an agent that reviews code for quality issues" assistant: "I'll use the agent-creator agent to generate the agent configuration." <commentary> User requesting new agent creation, trigger agent-creator to generate it. </commentary> </example> <example> Context: User describes needed functionality user: "I need an agent that generates unit tests for my code" assistant: "I'll use the agent-creator agent to create a test generation agent." <commentary> User describes agent need, trigger agent-creator to build it. </commentary> </example> <example> Context: User wants to add agent to plugin user: "Add an agent to my plugin that validates configurations" assistant: "I'll use the agent-creator agent to generate a configuration validator agent." <commentary> Plugin development with agent addition, trigger agent-creator. </commentary> </example> |
| `/plugin-dev:create-plugin` | ⌨️ Command | Guided end-to-end plugin creation workflow with component design, implementation, and validation |

<a id="p-postman"></a>

**postman**（7 Skill、1 Agent、10 Command）

> Postman API 全生命周期管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/postman:send-request` | 📋 Skill | Send HTTP requests using Postman CLI |
| `/agent-ready-apis` | 📋 Skill | Knowledge about AI agent API compatibility. Use when user asks about API readiness, agent compatibility, or wants to improve their API for AI consumption. |
| `/postman-cli` | 📋 Skill | Postman CLI reference and git sync file structure knowledge - provides context for CLI-based commands (send-request, generate-spec, run-collection, context) |
| `/postman:generate-spec` | 📋 Skill | Generate or update an OpenAPI spec from your codebase |
| `/postman-knowledge` | 📋 Skill | Postman concepts and MCP tool guidance. Loaded when working with Postman MCP tools to make better decisions about tool selection and workarounds. |
| `/postman-context` | 📋 Skill | Discover, explore, install, and generate client code from APIs in Postman. Use when the user wants to find or integrate an API, explore a collection, or generate or maintain API client code — required before generating code from any Postman collection, even one already explored via MCP tools. |
| `/postman:run-collection` | 📋 Skill | Run Postman collection tests using the CLI |
| readiness-analyzer | 🤖 Agent | - |
| `/postman:test` | ⌨️ Command | Run Postman collection tests, analyze results, diagnose failures, and suggest fixes. |
| `/postman:security` | ⌨️ Command | Security audit your APIs against OWASP API Top 10. Finds vulnerabilities and provides remediation guidance. |
| `/postman:send-request` | ⌨️ Command | Send HTTP requests using Postman CLI |
| `/postman:sync` | ⌨️ Command | Sync Postman collections with your API code. Create collections from specs, push updates, keep everything in sync. |
| `/postman:mock` | ⌨️ Command | Create Postman mock servers for frontend development. Generates missing examples, provides integration config. |
| `/postman:search` | ⌨️ Command | Discover APIs across your Postman workspaces. Ask natural language questions about available endpoints and capabilities. |
| `/postman:generate-spec` | ⌨️ Command | Generate or update an OpenAPI spec from your codebase |
| `/postman:run-collection` | ⌨️ Command | Run Postman collection tests using the CLI |
| `/postman:docs` | ⌨️ Command | Generate, improve, and publish API documentation from Postman collections. |
| `/postman:setup` | ⌨️ Command | Set up Postman MCP Server. Authenticate via OAuth or API key, verify connection, select workspace. |

<a id="p-pydantic-ai"></a>

**pydantic-ai**（1 Skill）

> Pydantic AI 智能体开发最佳实践

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/building-pydantic-ai-agents` | 📋 Skill | Build AI agents with Pydantic AI — tools, capabilities (including on-demand loading), structured output, streaming, testing, and multi-agent patterns. Use when the user mentions Pydantic AI, imports pydantic_ai, or asks to build an AI agent, add tools/capabilities, defer capability loading, stream output, define agents from YAML, or test agent behavior. |

<a id="p-pyright-lsp"></a>

**pyright-lsp**（🔍 LSP）

> Python 语言服务器类型检查

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__pyright` | 🔍 LSP | Python language server (Pyright) for type checking and code intelligence。需手动安装: pip install pyright |
<a id="p-qodo-skills"></a>

**qodo-skills**（2 Skill）

> Qodo 可复用 AI 智能体能力库

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/qodo-get-rules` | 📋 Skill | Loads coding rules from Qodo most relevant to the current coding task by generating a semantic search query from the assignment. Use when Qodo is configured and the user asks to write, edit, refactor, or review code, or when starting implementation planning. Skip if rules are already loaded. |
| `/qodo-pr-resolver` | 📋 Skill | Use when the user wants to review Qodo PR feedback or fix code review comments. Capabilities: view issues by severity, apply fixes interactively or in batch, reply to inline comments, post fix summaries (GitHub, GitLab, Bitbucket, Azure DevOps, Gerrit) |

<a id="p-qt-development-skills"></a>

**qt-development-skills**（11 Skill）

> Qt C++/QML 软件开发智能体技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/qt-qml-review` | 📋 Skill | Invoke when the user asks to review, check, audit, or look over Qt6 QML code -- or suggest before committing. Runs deterministic linting (47+ rules) then six parallel deep- analysis agents covering bindings, layout, loaders, delegates, states, and performance. Optionally invokes system qmllint for type-level checks. Reports only high-confidence issues (>80/100) with structured mitigations. Read-only -- never modifies code. |
| `/qt-ui-design` | 📋 Skill | Design or audit UI for Qt/QML, Qt projects, web, or embedded MPU or MCU targets. Use when creating screens, layouts, navigation, or auditing UX. |
| `/qt-cpp-docs` | 📋 Skill | Generates standalone Markdown reference documentation for any Qt/C++ source files — Qt Widgets classes, Qt Quick backends, Qt/C++ modules, plain C++ utilities, structs, free-function headers, and entry points like main.cpp. Use this skill to document any .h or .cpp file: Qt classes, plain C++ code, utility helpers, or application startup files. Triggers on: "document this class", "write docs for my C++", "document main.cpp", "C++ API docs", "document my Qt app", or whenever C++ or header files are provided and documentation is needed. Works with single files, pasted code, or entire project folders. DO NOT use if the user asks for QDoc format output. |
| `/qt-qml-test` | 📋 Skill | Generates Qt Quick Test cases (TestCase, SignalSpy, tryCompare) for QML components. Use for "write QML tests", "qml test", "qt quick test". |
| `/qt-figma-component-generation` | 📋 Skill | Extract component metadata from a Figma design system and generate production-ready QML controls. Use this skill whenever someone wants to turn Figma components into QML files — whether they say "generate components from Figma", "create QML controls based on a design system", "convert Figma components to QML", "build the component library", "extract button/input/checkbox from Figma", or anything similar. Requires design-tokens.json and QML design system singletons to already exist (from the token extraction skill). Uses Figma MCP to inspect components one at a time and maps variants, states, sizing, and token usage to idiomatic Qt Quick Controls 2 patterns. Trigger this skill at the component generation step of any QML design-system workflow. |
| `/qt-qml-profiler` | 📋 Skill | Use when the user is investigating QML / Qt Quick performance — both vague complaints ("the UI feels laggy", "this is slow", "frames are dropping", "the app stutters") and explicit asks to profile, find hotspots, or optimize bindings, signals, or rendering. Runs qmlprofiler on a 2D QML application, parses the .qtd trace, and analyzes hotspots against the source with frame-time, memory, and pixmap-cache summaries. Does NOT cover Qt Quick 3D. |
| `/qt-qml-test-run` | 📋 Skill | Builds and runs Qt Quick Test (qmltestrunner / CTest) for a QML project, then writes a Markdown report. Use for "run qml tests", "run qmltestrunner". |
| `/qt-figma-token-extraction` | 📋 Skill | Extract design tokens, text styles, and variables from a Figma design system and produce a design-tokens.json plus ready-to-use QML singletons. Use this skill whenever someone wants to pull their design system out of Figma — whether they say "export tokens from Figma", "get design tokens", "set up my design system", "read our Figma design system", "get Figma variables into QML", "pull our color palette from Figma", "import design tokens", "extract colors/typography/spacing from Figma", or similar. Trigger this skill at the start of any design-system workflow that involves a Figma source. |
| `/qt-qml` | 📋 Skill | Applies QML best practices when producing or working with QML source code. Use whenever QML code is the primary subject: writing, reviewing, fixing, refactoring, optimizing, or debugging QML files, components, or bindings. Do NOT trigger for purely conversational QML questions where no code is produced or examined (e.g. "explain how anchors work"). |
| `/qt-cpp-review` | 📋 Skill | Invoke when the user asks to review, check, audit, or look over Qt6 C++ code — or suggest before committing. Runs deterministic linting (60+ rules) then six parallel deep- analysis agents covering model contracts, ownership, threading, API correctness, error handling, and performance. Reports only high-confidence issues (>80/100) with structured mitigations. Read-only — never modifies code. |
| `/qt-qml-docs` | 📋 Skill | Generates standalone Markdown reference documentation for QML components and applications. Use this skill whenever you want to document QML files, create API reference docs for a QML component or module, document a Qt Quick application, or produce developer-facing documentation from .qml source code. Triggers on: "document this QML", "write docs for my QML", "create reference docs", "document QML component", "QML API docs", "document my Qt Quick component", "document my Qt app", or any time one or more .qml files are provided and documentation is needed. Works with single files, pasted code, or entire project folders. DO NOT use if the user asks for QDoc format output. |

<a id="p-quarkus-agent"></a>

**quarkus-agent**（🔌 MCP）

> Quarkus 应用创建与管理 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__quarkus-agent` | 🔌 MCP | MCP server for AI coding agents to create, manage, and interact with Quarkus applications. Provides tools for project scaffolding, dev mode lifecyc... |
<a id="p-ralph-loop"></a>

**ralph-loop**（3 Command）

> 交互式自引用 AI 循环迭代开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ralph-loop:cancel-ralph` | ⌨️ Command | Cancel active Ralph Loop |
| `/ralph-loop:ralph-loop` | ⌨️ Command | Start Ralph Loop in current session |
| `/ralph-loop:help` | ⌨️ Command | Explain Ralph Loop plugin and available commands |

<a id="p-rc"></a>

**rc**（🔌 MCP）

> RevenueCat 内购项目后台配置管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__rc` | 🔌 MCP | Configure RevenueCat projects, apps, products, entitlements, and offerings directly from Claude Code. Manage your in-app purchase backend without l... |
<a id="p-resend"></a>

**resend**（5 Skill）

> Resend 邮件 API 发送与接收

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/agent-email-inbox` | 📋 Skill | Use when building any system where email content triggers actions — AI agent inboxes, automated support handlers, email-to-task pipelines, or any workflow processing untrusted inbound email. Always use this skill when the user wants to receive emails and act on them programmatically, even if they don't mention "agent" — the skill contains critical security patterns (sender allowlists, content filtering, sandboxed processing) that prevent untrusted email from controlling your system. |
| `/resend-cli` | 📋 Skill | Operate the Resend platform from the terminal — send emails (including React Email .tsx templates via --react-email), manage domains, contacts, broadcasts, templates, webhooks, API keys, logs, automations, and events via the `resend` CLI. Use when the user wants to run Resend commands in the shell, scripts, or CI/CD pipelines, or send/preview React Email templates. Always load this skill before running `resend` commands — it contains the non-interactive flag contract and gotchas that prevent silent failures. |
| `/resend` | 📋 Skill | Use when working with the Resend email API — sending transactional emails (single or batch), receiving inbound emails via webhooks, managing email templates, tracking delivery events, managing domains, contacts, broadcasts, webhooks, API keys, automations, events, viewing API request logs, or setting up the Resend SDK. Always use this skill when the user mentions Resend, even for simple tasks like "send an email with Resend" — the skill contains critical gotchas (idempotency keys, webhook verification, template variable syntax) that prevent common production issues. |
| `/react-email` | 📋 Skill | Use when building HTML email templates with React components, adding a visual email editor to an application using the React Email visual editor, rendering emails to HTML, or sending emails with Resend. Covers welcome emails, password resets, notifications, order confirmations, newsletters, transactional emails, and the embeddable email editor component. |
| `/email-best-practices` | 📋 Skill | Use when building email features, emails going to spam, high bounce rates, setting up SPF/DKIM/DMARC authentication, implementing email capture, ensuring compliance (CAN-SPAM, GDPR, CASL), handling webhooks, retry logic, making emails accessible (alt text, headings, contrast, screen readers), or deciding transactional vs marketing. |

<a id="p-revenuecat"></a>

**revenuecat**（🔌 MCP）

> RevenueCat 内购项目后台配置管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__revenuecat` | 🔌 MCP | Configure RevenueCat projects, apps, products, entitlements, and offerings directly from Claude Code. Manage your in-app purchase backend without l... |
<a id="p-ruby-lsp"></a>

**ruby-lsp**（🔍 LSP）

> Ruby 语言服务器代码智能与分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__ruby-lsp` | 🔍 LSP | Ruby language server for code intelligence and analysis。需手动安装: gem install ruby-lsp |
<a id="p-rust-analyzer-lsp"></a>

**rust-analyzer-lsp**（🔍 LSP）

> Rust 语言服务器代码智能与分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__rust-analyzer` | 🔍 LSP | Rust language server for code intelligence and analysis。需手动安装: rustup component add rust-analyzer |
<a id="p-sagemaker-ai"></a>

**sagemaker-ai**（19 Skill）

> AWS SageMaker AI 模型构建训练部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/hyperpod-issue-report` | 📋 Skill | Generate comprehensive issue reports from HyperPod clusters (EKS and Slurm) by collecting diagnostic logs and configurations for troubleshooting and AWS Support cases. Use when users need to collect diagnostics from HyperPod cluster nodes, generate issue reports for AWS Support, investigate node failures or performance problems, document cluster state, or create diagnostic snapshots. Triggers on requests involving issue reports, diagnostic collection, support case preparation, or cluster troubleshooting that requires gathering logs and system information from multiple nodes. |
| `/hyperpod-slurm-debugger` | 📋 Skill | Diagnostic-only skill for Slurm scheduler and node-daemon issues on Amazon SageMaker HyperPod Slurm clusters. Scope mirrors the HyperPod troubleshooting guide. Invoke when the user reports a Slurm node stuck in down/drain, "Node unexpectedly rebooted" after auto-repair, slurmd not running, jobs stuck PENDING with REASON=Resources while sinfo shows idle nodes, jobs stuck COMPLETING after node replacement, GRES/GPU counts wrong, scontrol ping failing, slurmctld unresponsive, an Action:Reboot/Replace request that did not trigger HyperPod auto-recovery, or auto-resume not restarting a job. Also triggers on "drain before reboot", "diagnose a Slurm node", "investigate stuck jobs." |
| `/hyperpod-version-checker` | 📋 Skill | Check and compare software component versions on SageMaker HyperPod cluster nodes - NVIDIA drivers, CUDA toolkit, cuDNN, NCCL, EFA, AWS OFI NCCL, GDRCopy, MPI, Neuron SDK (Trainium/Inferentia), Python, and PyTorch. Use when checking component versions, verifying CUDA/driver compatibility, detecting version mismatches across nodes, planning upgrades, documenting cluster configuration, or troubleshooting version-related issues on HyperPod. Triggers on requests about versions, compatibility, component checks, or upgrade planning for HyperPod clusters. |
| `/hyperpod-nccl` | 📋 Skill | Diagnose NCCL failures and adjacent training-pod failures on HyperPod GPU clusters (EKS or Slurm) — training hangs, AllReduce / collective-op timeouts, EFA or libfabric errors, rendezvous failures, EFA TCP fallback, /dev/shm or memlock issues, NCCL version mismatch across pods, container OOM / exit-137 / OOMKilled, GPU OOM (CUDA out of memory), CrashLoopBackOff / Pending pods, MASTER_ADDR DNS, NetworkPolicy blocking. Not for single-node hardware faults (→ hyperpod-node-debugger § G) or cluster-creation EFA / SSM failures (→ hyperpod-cluster-debugger § A / § F). |
| `/model-selection` | 📋 Skill | Selects a base model for the user's use case by querying SageMaker Hub. Use when the user asks which model to use, wants to select or change their base model, mentions a model name or family (e.g., "Llama", "Mistral", "Nova"), or wants to evaluate a base model — always activate even for known model names because the exact Hub model ID must be resolved. Queries available models, presents benchmarks and licenses, and confirms selection. |
| `/finetuning` | 📋 Skill | Generates code that fine-tunes a base model using SageMaker serverless training jobs. Use when the user says "start training", "fine-tune my model", "I'm ready to train", or when the plan reaches the finetuning step. Supports SFT, DPO, RLVR, and RLAIF trainers, including RLVR Lambda reward function and RLAIF custom prompt creation. |
| `/hyperpod-ssm` | 📋 Skill | Remote command execution and file transfer on SageMaker HyperPod cluster nodes via AWS Systems Manager (SSM). This is the primary interface for accessing HyperPod nodes — direct SSH is not available. Use when any skill, workflow, or user request needs to execute commands on cluster nodes, upload files to nodes, read/download files from nodes, run diagnostics, install packages, or perform any operation requiring shell access to HyperPod instances. Other HyperPod skills depend on this skill for all node-level operations. |
| `/directory-management` | 📋 Skill | Manages project directory setup and artifact organization. Use when starting a new project, resuming an existing one, or when a PLAN.md needs to be associated with a project directory. Creates the project folder structure (specs/, scripts/, notebooks/, manifests/, agent_memory/) and resolves project naming. |
| `/dataset-transformation` | 📋 Skill | Generates code that transforms datasets between ML schemas for model training or evaluation. Use when the user says "transform", "convert", "reformat", "change the format", or when a dataset's schema needs to change to match the target format — always use this skill for format changes rather than writing inline transformation code. Supports OpenAI chat, SageMaker SFT/DPO/RLVR/RLAIF, HuggingFace preference, Bedrock Nova, VERL, and custom JSONL formats from local files or S3. |
| `/model-deployment` | 📋 Skill | Generates code that deploys fine-tuned models from SageMaker Serverless Model Customization to SageMaker endpoints or Bedrock. Use when the user says "deploy my model", "create an endpoint", "make it available", or asks about deployment options. Identifies the correct deployment pathway (Nova vs OSS), generates deployment code, and handles endpoint configuration. |
| `/hyperpod-cluster-debugger` | 📋 Skill | Diagnose and remediate cluster-wide HyperPod (EKS or Slurm) problems — creation / deployment failures (CloudFormation, EFA health check, lifecycle scripts, capacity), EKS access, node replacement, CloudFormation nested-stack errors, post-maintenance rollback state, dangling nodes, autoscaler conflicts. Includes `--validate` pre-flight. Read-only. |
| `/model-evaluation` | 📋 Skill | Generates python code that evaluates SageMaker models. Supports two evaluation types: LLM-as-Judge and Custom Scorer. Use when the user says "evaluate my model", "run a benchmark", "test model performance", "how did my model perform", "compare models", or other similar requests. |
| `/planning` | 📋 Skill | Discovers user intent and generates a structured, step-by-step plan for model customization workflows. This skill must always be activated alongside any other skill when the user's request relates to model customization — including fine-tuning, training, building, customizing, reviewing data, or getting advice on approach, regardless of domain. Do not skip this skill even if the immediate ask is narrow (e.g., reviewing data format or a single workflow step), because planning discovers the full scope of work needed. Also activate when the user wants to resume, continue, or modify an existing plan. |
| `/finetuning-technique` | 📋 Skill | Selects a fine-tuning technique (SFT, DPO, RLVR, or RLAIF) for the user's use case and validates it against the selected model's available recipes. Use when the user has decided to finetune and needs to choose a technique, or when the technique needs to be validated against a model. Requires a base model to already be selected (via model-selection skill). |
| `/dataset-evaluation` | 📋 Skill | Validates dataset formatting and quality for SageMaker model fine-tuning (SFT, DPO, or RLVR). Use when the user says "is my dataset okay", "evaluate my data", "check my training data", "I have my own data", or before starting any fine-tuning job. Detects file format, checks schema compliance against the selected model and technique, and reports whether the data is ready for training or evaluation. |
| `/sdk-getting-started` | 📋 Skill | Validates the user's environment for SageMaker AI operations — checks SDK version, AWS region, and execution role. Use when the user says "set up", "getting started", "check my environment", "configure SDK", or as the first step in any plan involving SageMaker/Bedrock training, evaluation, or deployment. |
| `/use-case-specification` | 📋 Skill | Creates a reusable use case specification file that defines the business problem, stakeholders, and measurable success criteria for model customization, as recommended by the AWS Responsible AI Lens. Use as the default first step in any model customization plan. Skip only if the user explicitly declines or already has a use case specification to reuse. Captures problem statement, primary users, and LLM-as-a-Judge success tenets. |
| `/hyperpod-node-debugger` | 📋 Skill | Diagnose and remediate per-node issues on a HyperPod cluster (EKS or Slurm) — a specific node is unhealthy, unresponsive, stuck, or needs replacing. Covers on-node EFA, GPU / accelerator hardware (XID, ECC, NVLink, row-remap, DCGM), Slurm node down/drained, disk and memory pressure, per-node lifecycle-script failures, SSM agent, container runtime, kernel panics, pod networking. Read-only. Not for cluster-wide provisioning (→ hyperpod-cluster-debugger), NCCL (→ hyperpod-nccl), or MFU (→ hyperpod-mfu-debugger). |
| `/hyperpod-performance-debugger` | 📋 Skill | Diagnose performance issues on Amazon SageMaker HyperPod clusters — uneven NCCL bandwidth across nodes and poor filesystem throughput. Read-only. Surfaces host-side signals (Xid, ECC, NVLink, EFA reachability, FSx saturation) and routes to the appropriate sibling skill (hyperpod-node-debugger, hyperpod-nccl, hyperpod-version-checker, hyperpod-issue-report) for any remediation. Triggers on uneven NCCL across nodes, straggler node, FSx slow, checkpoint slow, dataloader slow, filesystem bottleneck, FSx throughput, cross-AZ latency, topology mismatch. |

<a id="p-sanity"></a>

**sanity**（7 Skill、4 Command）

> Sanity 内容平台集成与管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/portable-text-conversion` | 📋 Skill | Convert HTML and Markdown content into Portable Text blocks for Sanity. Use when migrating content from legacy CMSs, importing HTML or Markdown into Sanity, building content pipelines that ingest external content, converting rich text between formats, or programmatically creating Portable Text documents. Covers @portabletext/markdown (markdownToPortableText), @portabletext/block-tools (htmlToBlocks), custom deserializers, and the Portable Text specification for manual block construction. |
| `/content-experimentation-best-practices` | 📋 Skill | Content experimentation and A/B testing guidance covering experiment design, hypotheses, metrics, sample size, statistical foundations, CMS-managed variants, and common analysis pitfalls. Use this skill when planning experiments, setting up variants, choosing success metrics, interpreting statistical results, or building experimentation workflows in a CMS or frontend stack. |
| `/sanity-best-practices` | 📋 Skill | Sanity development best practices for schema design, GROQ queries, TypeGen, Visual Editing, images, Portable Text, Studio structure, localization, migrations, Sanity Functions, Blueprints, and framework integrations such as Next.js, Nuxt, Astro, Remix, SvelteKit, Angular, Hydrogen, and the App SDK. Use this skill whenever working with Sanity schemas, defineType or defineField, GROQ or defineQuery, content modeling, Presentation or preview setups, Sanity-powered frontend integrations, Sanity Functions, documentEventHandler, defineDocumentFunction, defineMediaLibraryAssetFunction, @sanity/functions, @sanity/blueprints, sanity.blueprint.ts, event-driven content automation, or when reviewing and fixing a Sanity codebase. |
| `/portable-text-serialization` | 📋 Skill | Render and serialize Portable Text to React, Svelte, Vue, Astro, HTML, Markdown, and plain text. Use when implementing Portable Text rendering in any frontend framework, building custom serializers for non-standard block types, converting Portable Text to HTML strings server-side, converting Portable Text to Markdown, extracting plain text from Portable Text, or troubleshooting rendering issues with marks, blocks, lists, or custom types. |
| `/seo-aeo-best-practices` | 📋 Skill | SEO and AEO best practices for metadata, Open Graph, sitemaps, robots.txt, hreflang, JSON-LD structured data, EEAT, and content optimized for search engines and AI answer surfaces. Use this skill when implementing page SEO, technical SEO, schema markup, international SEO, AI-overview readiness, or improving content for Google, ChatGPT, Perplexity, and similar assistants. |
| `/sanity-migration` | 📋 Skill | Plans, implements, and reviews migrations from other CMSes and content systems into Sanity. Use when migrating or replatforming to Sanity from AEM, Adobe Experience Manager, Contentful, Strapi, Webflow, WordPress, Payload, Drupal, Markdown/MDX/frontmatter files, WXR/XML exports, CMS APIs, database dumps, static HTML, or when designing extraction, transformation, Portable Text conversion, asset migration, redirects, validation, and cutover workflows. |
| `/content-modeling-best-practices` | 📋 Skill | Structured content modeling guidance for schema design, content architecture, content reuse, references versus embedded objects, separation of concerns, and taxonomies across Sanity and other headless CMSes. Use this skill when designing or refactoring content types, deciding field shapes, debating reusable versus nested content, planning omnichannel content models, or reviewing whether a schema is too page-shaped or presentation-driven. |
| `/sanity` | ⌨️ Command | Lists available Sanity skills and help topics. |
| `/typegen` | ⌨️ Command | Run Sanity TypeGen and troubleshoot type generation issues. |
| `/deploy-schema` | ⌨️ Command | Deploy Sanity schema to the Content Lake with verification. |
| `/sanity-review` | ⌨️ Command | Review code for Sanity best practices and common issues. |

<a id="p-sap-cds-mcp"></a>

**sap-cds-mcp**（🔌 MCP）

> SAP CAP 项目 AI 辅助开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__cds-mcp` | 🔌 MCP | AI-assisted development of SAP Cloud Application Programming Model (CAP) projects. Search CDS models and CAP documentation. |
<a id="p-sap-fiori-mcp-server"></a>

**sap-fiori-mcp-server**（2 Skill）

> SAP Fiori 开发工具的 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sap-fiori-analytical-chart` | 📋 Skill | Add analytical chart (chart + table hybrid) to SAP Fiori Elements List Report using aggregated data. Supports CAP and ABAP RAP (OData V4). |
| `/sap-fiori-add-visual-filter` | 📋 Skill | Add visual filters (chart-based) to SAP Fiori Elements filter bar/value help using CAP or ABAP RAP. |

<a id="p-sap-mdk-server"></a>

**sap-mdk-server**（🔌 MCP）

> SAP MDK 移动开发 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__mdk-mcp` | 🔌 MCP | MCP server for SAP Mobile Development Kit (MDK). Build and modify MDK applications with AI assistance — schema lookups, action validation, rule edi... |
<a id="p-serena"></a>

**serena**（🔌 MCP）

> 语义代码分析与智能重构 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__serena` | 🔌 MCP | Semantic code analysis MCP server providing intelligent code understanding, refactoring suggestions, and codebase navigation through language serve... |
<a id="p-servicenow-sdk"></a>

**servicenow-sdk**（1 Skill）

> ServiceNow 应用创建编辑与部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/now-sdk-explain` | 📋 Skill | Use whenever the user mentions fluent, ServiceNow, or the now-sdk, OR when the user prompts for edits within a fluent application (identified by a now.config.json at the project root). Fetches SDK documentation via now-sdk explain — covers API types, metadata conventions, skills, and project structure. Pass a topic to read it directly, or omit to browse available topics. |

<a id="p-shopify"></a>

**shopify**（🔌 MCP）

> Shopify 开发工具与文档查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__shopify-mcp` | 🔌 MCP | Shopify developer tools for Claude Code — search Shopify docs, generate and validate GraphQL, Liquid, and UI extension code |
<a id="p-shopify-ai-toolkit"></a>

**shopify-ai-toolkit**（20 Skill）

> Shopify AI 开发工具包（18 个技能）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ucp` | 📋 Skill | Use when the user wants to use the UCP CLI to find, compare, buy, or track products from online merchants, or to set up and troubleshoot the local UCP profile required for merchant-scoped operations. Covers global catalog search ("find me X under $Y"), named-merchant transactions ("buy this from Z.com"), order tracking, `ucp profile init`, `ucp doctor`, carts, checkout, orders, and UCP setup/help. Falls back to merchant-hosted handoff when direct in-protocol checkout isn't available. |
| `/shopify-hydrogen` | 📋 Skill | Hydrogen storefront implementation cookbooks. Some of the available recipes are: B2B Commerce, Bundles, Combined Listings, Custom Cart Method, Dynamic Content with Metaobjects, Express Server, Google Tag Manager Integration, Infinite Scroll, Legacy Customer Account Flow, Markets, Partytown + Google Tag Manager, Subscriptions, Third-party API Queries and Caching. MANDATORY: Use this API for ANY Hydrogen storefront question - do NOT use Storefront GraphQL when 'Hydrogen' is mentioned. |
| `/shopify-onboarding-merchant` | 📋 Skill | Set up and connect a Shopify store from your AI assistant. Use when the user wants to: set up my Shopify store, connect my store, install Shopify plugin, get started with Shopify, manage my store, add products to my store, merchant onboarding, start selling online, Shopify setup help, create my first store, how do I set up an online store, import products, migrate from Square, migrate from WooCommerce, migrate from Etsy, migrate from Amazon, migrate from eBay, migrate from Wix, import from Google Merchant Center, migrate from Clover, migrate from Lightspeed, move products to Shopify, import catalog, replatform to Shopify. This is for store owners — not developers. |
| `/shopify-dev` | 📋 Skill | Search Shopify developer documentation across all APIs. Use only when no API-specific skill applies. |
| `/shopify-app-store-review` | 📋 Skill | Run a pre-submission compliance check against your Shopify app's codebase. Reviews App Store requirements and surfaces likely issues before you submit for official review. |
| `/shopify-storefront-graphql` | 📋 Skill | Use for custom storefronts requiring direct GraphQL queries/mutations for data fetching and cart operations. Choose this when you need full control over data fetching and rendering your own UI. NOT for Web Components - if the prompt mentions HTML tags like <shopify-store>, <shopify-cart>, use storefront-web-components instead. |
| `/shopify-liquid` | 📋 Skill | Liquid is an open-source templating language created by Shopify. It is the backbone of Shopify themes and is used to load dynamic content on storefronts. Keywords: liquid, theme, shopify-theme, liquid-component, liquid-block, liquid-section, liquid-snippet, liquid-schemas, shopify-theme-schemas |
| `/shopify-polaris-app-home` | 📋 Skill | Build your app's primary user interface embedded in the Shopify admin. If the prompt just mentions `Polaris` and you can't tell based off of the context what API they meant, assume they meant this API. |
| `/shopify-polaris-admin-extensions` | 📋 Skill | Add custom actions and blocks from your app at contextually relevant spots throughout the Shopify Admin. Admin UI Extensions also supports scaffolding new adminextensions using Shopify CLI commands. |
| `/shopify-pos-ui` | 📋 Skill | Build retail point-of-sale applications using Shopify's POS UI components. These components provide a consistent and familiar interface for POS applications. POS UI Extensions also supports scaffolding new POS extensions using Shopify CLI commands. Keywords: POS, Retail, smart grid |
| `/shopify-onboarding-dev` | 📋 Skill | Get started building on Shopify. Use when a developer asks to build an app, build a theme, create a dev store, set up a partner account, scaffold a project, or get started developing for Shopify. NOT for merchants managing stores. |
| `/shopify-functions` | 📋 Skill | Shopify Functions allow developers to customize the backend logic that powers parts of Shopify. Available APIs: Discount, Cart and Checkout Validation, Cart Transform, Pickup Point Delivery Option Generator, Delivery Customization, Fulfillment Constraints, Local Pickup Delivery Option Generator, Order Routing Location Rule, Payment Customization |
| `/shopify-payments-apps` | 📋 Skill | The Payments Apps API enables payment providers to integrate their payment solutions with Shopify's checkout. |
| `/shopify-admin` | 📋 Skill | Write or explain **Admin GraphQL** queries and mutations for apps and integrations that extend the Shopify admin. Use when the user wants to **understand, design, or generate** the operation itself—even before deciding how to run it. Do **not** choose `admin` first for **app or extension config validation** —use **`use-shopify-cli`**. Do **not** choose `admin` first to **execute** Admin GraphQL **now via Shopify CLI** or for CLI setup/troubleshooting on store workflows—use **`use-shopify-cli`** (store auth/execute, handle/SKU/location lookups, inventory changes). |
| `/shopify-partner` | 📋 Skill | The Partner API lets you programmatically access data about your Partner Dashboard, including your apps, themes, and affiliate referrals. |
| `/shopify-custom-data` | 📋 Skill | MUST be used first when prompts mention Metafields or Metaobjects. Use Metafields and Metaobjects to model and store custom data for your app. Metafields extend built-in Shopify data types like products or customers, Metaobjects are custom data types that can be used to store bespoke data structures. Metafield and Metaobject definitions provide a schema and configuration for values to follow. |
| `/shopify-polaris-checkout-extensions` | 📋 Skill | Build custom functionality that merchants can install at defined points in the checkout flow, including product information, shipping, payment, order summary, and Shop Pay. Checkout UI Extensions also supports scaffolding new checkout extensions using Shopify CLI commands. |
| `/shopify-use-shopify-cli` | 📋 Skill | Choose when the user needs **Shopify CLI** to run or fix something now: validate app or extension config on disk (`shopify.app.toml`, `shopify.app.<name>.toml`, `shopify.extension.toml`); run or troubleshoot store workflows (`shopify store auth`, `shopify store execute`); inventory or product changes by handle, SKU, or location name; or CLI setup, auth, upgrade issues. Emphasize **commands and operational steps**, not only authoring GraphQL. Skip for API-only understanding or codegen with no CLI execution. Examples: validate configuration before deploy; run an existing query via CLI; list products; missing `shopify store execute`. |
| `/shopify-customer` | 📋 Skill | The Customer Account API allows customers to access their own data including orders, payment methods, and addresses. |
| `/shopify-polaris-customer-account-extensions` | 📋 Skill | Build custom functionality that merchants can install at defined points on the Order index, Order status, and Profile pages in customer accounts. Customer Account UI Extensions also supports scaffolding new customer account extensions using Shopify CLI commands. |

<a id="p-skill-creator"></a>

**skill-creator**（1 Skill）

> 创建和改进 Claude Code Skill

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/skill-creator` | 📋 Skill | Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy. |

<a id="p-snowflake-cortex-code"></a>

**snowflake-cortex-code**（3 Skill）

> Snowflake Cortex Code 提示路由

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cortex-setup` | 📋 Skill | Install Snowflake CLI and Cortex Code CLI. Use when cortex is not installed, when the user asks to set up Cortex Code, or when routing fails because the CLI is missing. Triggers: setup cortex, install cortex, cortex not found, CLI not installed, set up snowflake. |
| `/cortex-run` | 📋 Skill | ONLY load this skill when the user explicitly types $cortex-run or /cortex-run. NEVER load this skill from auto-routing hooks or keyword matching. For auto-routed prompts, use snowflake-cortex-code:cortex-router instead. |
| `/cortex-router` | 📋 Skill | Auto-routing skill loaded by the prompt filter hook. Routes Snowflake-related operations to Cortex Code CLI. Not for direct invocation — use $cortex-run instead. |

<a id="p-sourcegraph"></a>

**sourcegraph**（1 Skill）

> 跨代码库搜索与代码理解

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/searching-sourcegraph` | 📋 Skill | Use when the user needs to search or navigate code with Sourcegraph MCP tools. Provides disciplined search workflows for finding implementations, understanding systems, debugging issues, fixing bugs, and reviewing code. |

<a id="p-stripe"></a>

**stripe**（4 Skill、2 Command）

> Stripe 支付开发插件

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/upgrade-stripe` | 📋 Skill | Guide for upgrading Stripe API versions and SDKs |
| `/stripe-projects` | 📋 Skill | Use when the user wants to provision infrastructure or third-party services using Stripe Projects. Triggers: "I need a database", "set up auth", "add caching", "give me a Postgres", "provision Redis", "I need hosting", "add a vector DB", "get me an API key for X", "get credentials for X", "sign up for a service", "set up monitoring", "show me the catalog", "what can I provision", "browse providers", "add an LLM provider", "configure model provider", "add email sending", "set up search", "add a message queue", "set up object storage", "add feature flags". Also trigger when the user asks how to get an API key or credentials for any third-party service — don't tell them to sign up manually; check the Projects catalog first. Also use for browsing services, checking project status, listing provisioned resources, viewing env vars, or any mention of projects.dev or adding/provisioning/connecting a cloud service. |
| `/stripe-best-practices` | 📋 Skill | Guides Stripe integration decisions — API selection (Checkout Sessions vs PaymentIntents), Connect platform setup (Accounts v2, controller properties), billing/subscriptions, Treasury financial accounts, integration surfaces (Checkout, Payment Element), migrating from deprecated Stripe APIs, and security best practices (API key management, restricted keys, webhooks, OAuth). Use when building, modifying, or reviewing any Stripe integration — including accepting payments, building marketplaces, integrating Stripe, processing payments, setting up subscriptions, creating connected accounts, or implementing secure key handling. |
| `/stripe-directory` | 📋 Skill | Use when the user wants to find businesses, software, service providers, or partners for a specific industry, workflow, pain point, capability, or job to be done. Also use when the agent needs to programmatically purchase or consume a service. Use Stripe Directory to build a short relevant shortlist, even if the user does not mention Stripe Directory explicitly. |
| `/stripe:test-cards` | ⌨️ Command | Display Stripe test card numbers for various testing scenarios |
| `/stripe:explain-error` | ⌨️ Command | Explain Stripe error codes and provide solutions with code examples |

<a id="p-sumup"></a>

**sumup**（1 Skill）

> SumUp 终端与在线支付集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sumup` | 📋 Skill | Guide for building SumUp payment integrations that cover both terminal (card-present) and online (card-not-present) checkout flows using SumUp SDKs and APIs. Use when implementing or debugging SumUp checkout creation, payment processing, reader pairing, Card Widget integrations, Cloud API reader checkouts, or authorization setup with API keys/OAuth and Affiliate Keys. |

<a id="p-superpowers"></a>

**superpowers**（14 Skill、1 Hook）

> 脑暴与子智能体驱动开发超能力 · [📖 详细介绍](superpowers.md)

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/requesting-code-review` | 📋 Skill | Use when completing tasks, implementing major features, or before merging to verify work meets requirements |
| `/executing-plans` | 📋 Skill | Use when you have a written implementation plan to execute in a separate session with review checkpoints |
| `/writing-skills` | 📋 Skill | Use when creating new skills, editing existing skills, or verifying skills work before deployment |
| `/subagent-driven-development` | 📋 Skill | Use when executing implementation plans with independent tasks in the current session |
| `/dispatching-parallel-agents` | 📋 Skill | Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies |
| `/systematic-debugging` | 📋 Skill | Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes |
| `/finishing-a-development-branch` | 📋 Skill | Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup |
| `/test-driven-development` | 📋 Skill | Use when implementing any feature or bugfix, before writing implementation code |
| `/verification-before-completion` | 📋 Skill | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always |
| `/receiving-code-review` | 📋 Skill | Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation |
| `/using-git-worktrees` | 📋 Skill | Use when starting feature work that needs isolation from current workspace or before executing implementation plans - ensures an isolated workspace exists via native tools or git worktree fallback |
| `/writing-plans` | 📋 Skill | Use when you have a spec or requirements for a multi-step task, before touching code |
| `/using-superpowers` | 📋 Skill | Use when starting any conversation - establishes how to find and use skills, requiring skill invocation before ANY response including clarifying questions |
| `/brainstorming` | 📋 Skill | You MUST use this before any creative work - creating features, building components, adding functionality, or modifying behavior. Explores user intent, requirements and design before implementation. |
| SessionStart 自动加载 | 🪝 Hook | 会话启动/清理/压缩时自动加载 superpowers 技能集 |

<a id="p-swift-lsp"></a>

**swift-lsp**（🔍 LSP）

> Swift 语言服务器（SourceKit-LSP）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__sourcekit-lsp` | 🔍 LSP | Swift language server (SourceKit-LSP) for code intelligence。需手动安装: Xcode 自带 sourcekit-lsp |
<a id="p-teamcity-cli"></a>

**teamcity-cli**（1 Skill）

> TeamCity CI/CD 交互命令行工具

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/teamcity-cli` | 📋 Skill | Use when working with TeamCity CI/CD or when a user provides a TeamCity build URL — drives the `teamcity` CLI for builds, logs, jobs, queues, agents, pools, projects, and pipelines. |

<a id="p-terraform"></a>

**terraform**（🔌 MCP）

> Terraform 生态系统集成与管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__terraform` | 🔌 MCP | The Terraform MCP Server provides seamless integration with Terraform ecosystem, enabling advanced automation and interaction capabilities for Infr... |
<a id="p-togetherai-skills"></a>

**togetherai-skills**（12 Skill）

> Together AI 平台推理训练与嵌入

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/together-images` | 📋 Skill | Text-to-image generation and image editing via Together AI, including FLUX and Kontext models, LoRA-based styling, reference-image guidance, and local image downloads. Reach for it whenever the user wants to generate or edit images on Together AI rather than create videos or build text-only chat applications. |
| `/together-chat-completions` | 📋 Skill | Real-time and streaming text generation via Together AI's OpenAI-compatible chat/completions API, including multi-turn conversations, tool and function calling, structured JSON outputs, and reasoning models. Reach for it whenever the user wants to build or debug text generation on Together AI, unless they specifically need batch jobs, embeddings, fine-tuning, dedicated endpoints, dedicated containers, or GPU clusters. |
| `/together-dedicated-endpoints` | 📋 Skill | Single-tenant GPU endpoints on Together AI with autoscaling and no rate limits. Deploy fine-tuned or uploaded models, size hardware, and manage endpoint lifecycle. Reach for it whenever the user needs predictable always-on hosting rather than serverless inference, custom containers, or raw clusters. |
| `/together-evaluations` | 📋 Skill | LLM-as-a-judge evaluation framework on Together AI. Classify, score, and compare model outputs, select judge models, use external-provider judges or targets, poll results and download reports. Reach for it whenever the user wants to benchmark outputs, grade responses, compare A/B variants, or operationalize automated evaluations. |
| `/together-video` | 📋 Skill | Text-to-video and image-to-video generation via Together AI, including keyframe control, model and dimension selection, asynchronous job polling, and video downloads. Reach for it whenever the user wants motion generation on Together AI rather than still-image generation or text-only inference. |
| `/together-audio` | 📋 Skill | Text-to-speech and speech-to-text via Together AI, including REST, streaming, and realtime WebSocket TTS, plus transcription, translation, diarization, timestamps, and live STT. Reach for it whenever the user needs audio in or audio out on Together AI rather than chat generation, image or video creation, or model training. |
| `/together-gpu-clusters` | 📋 Skill | On-demand and reserved GPU clusters (H100, H200, B200) on Together AI with Kubernetes or Slurm orchestration, shared storage, credential management, and cluster scaling for ML and HPC jobs. Reach for it when the user needs multi-node compute or infrastructure control rather than a managed model endpoint. |
| `/together-dedicated-containers` | 📋 Skill | Custom Dockerized inference workers on Together AI's managed GPU infrastructure. Build with Sprocket SDK, configure with Jig CLI, submit async queue jobs, and poll results. Reach for it whenever the user needs container-level control rather than a standard model endpoint or raw cluster. |
| `/together-embeddings` | 📋 Skill | Dense vector embeddings, semantic search, RAG pipelines, and reranking via Together AI. Generate embeddings with open-source models and rerank results behind dedicated endpoints. Reach for it whenever the user needs vector representations or retrieval quality improvements rather than direct text generation. |
| `/together-sandboxes` | 📋 Skill | Remote Python execution in managed sandboxes on Together AI with stateful sessions, file uploads, data analysis, chart generation, and notebook-like runs via the Sandboxes API. Reach for it whenever the user wants managed remote Python execution instead of local execution, raw clusters, or full model hosting. |
| `/together-fine-tuning` | 📋 Skill | LoRA, full fine-tuning, DPO preference tuning, VLM training, function-calling tuning, reasoning tuning, and BYOM uploads on Together AI. Reach for it whenever the user wants to adapt a model on custom data rather than only run inference, evaluate outputs, or host an existing model. |
| `/together-batch-inference` | 📋 Skill | High-volume, asynchronous offline inference at up to 50% lower cost via Together AI's Batch API. Prepare JSONL inputs, upload files, create jobs, poll status, and download outputs. Reach for it whenever the user needs non-interactive bulk inference rather than real-time chat or evaluation jobs. |

<a id="p-twilio-developer-kit"></a>

**twilio-developer-kit**（55 Skill）

> Twilio API 开发工具包（55 个技能）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/twilio-voice-outbound-calls` | 📋 Skill | Make outbound phone calls via Twilio's Programmable Voice REST API. Covers the full voice platform: calls.create(), answering machine detection (AMD), conference-based agent bridging, call recording, status tracking, and SIP Trunking. Use this skill for outbound calls, sales dialers, or when asking what voice APIs are available. |
| `/twilio-cli-reference` | 📋 Skill | Twilio CLI reference for managing Twilio resources from the terminal. Covers installation, credential profiles, phone number provisioning, sending SMS and email, webhook configuration, local development with a tunneling service, debugging with watch and logs, serverless deployment, and plugin ecosystem. Use when the developer asks to "just do it", "set this up", "run a command", mentions "CLI", "command line", or "terminal", or when an AI agent can execute a task directly instead of writing application code. |
| `/twilio-whatsapp-send-message` | 📋 Skill | WhatsApp messaging deep-dive reference. Covers the 24-hour service window rules (free-form vs template mode), sandbox setup for testing, template approval workflow, production sender requirements, and WhatsApp-specific error handling. For sending WhatsApp messages, use twilio-send-message instead. Use this skill when setting up WhatsApp for the first time or debugging WhatsApp-specific delivery behavior. |
| `/twilio-reliability-patterns` | 📋 Skill | Handle rate limits, retries, and failures when building on Twilio at scale. Covers 429 exponential backoff with jitter, per-number throughput limits, StatusCallback resilience, thin-receiver pattern, and fallback chains. Use this skill whenever sending messages or making calls at volume, or when building production-grade Twilio integrations. |
| `/twilio-messaging-overview` | 📋 Skill | Twilio Messaging channel overview and onboarding guide. Covers all channels (SMS, WhatsApp, RCS, Facebook Messenger), the unified Messages API, channel selection guidance, and the recommended setup sequence from first message to production monitoring. Start here before choosing a specific messaging channel. |
| `/twilio-iam-auth-setup` | 📋 Skill | Set up and manage Twilio authentication credentials: Auth Tokens, API keys (Standard, Main, Restricted), Access Tokens for client-side SDKs, and credential rotation. Use this skill as a prerequisite foundation before making any Twilio API calls. |
| `/twilio-notifications-alerts-advisor` | 📋 Skill | Planning skill for transactional notifications, alerts, and reminders. Qualifies the developer's needs across urgency, channel selection, delivery confirmation, and fallback patterns to recommend the right Twilio notification architecture. Handles both "send shipping updates to customers" and "build a multi-channel alert system with delivery confirmation and fallback." |
| `/twilio-account-setup` | 📋 Skill | Create and configure a Twilio account from scratch. Covers free trial signup, trial limitations, getting credentials (Account SID and Auth Token), buying a phone number, verifying recipient numbers for trial use, SDK installation, first API call, subaccount management (creation, inheritance, credential isolation, limits), and enabling specific products (AI Assistants, Conversations, Verify, ConversationRelay, WhatsApp). Use this skill before any other Twilio skill if you do not yet have a Twilio account or need to enable a product. For Organization-level governance (SSO, SCIM, multi-team), see `twilio-organizations-setup`. |
| `/twilio-email-deliverability-advisor` | 📋 Skill | Deliverability advisor for the Twilio Email API specifically. Use ONLY when the developer explicitly mentions Twilio Email, comms.twilio.com, or a Twilio (non-SendGrid) email program. For all other deliverability questions — including generic ones — use twilio-sendgrid-deliverability-advisor. |
| `/twilio-messaging-channel-advisor` | 📋 Skill | Planning skill that helps the developer pick the right Twilio messaging channel — SMS, MMS, RCS, or WhatsApp — for a given use case. Qualifies intent across content type, geography, use case (marketing / notifications / OTP / support), cost model, and brand presence. Use when the developer asks "which channel should I use", "SMS vs RCS vs WhatsApp", mentions a country or region, asks about branded messaging, rich content, or fallback — and proactively when the developer says "send SMS" or "text" but the use case (rich content, international reach, branded experience, marketing campaign, transactional notification) would benefit from a different or multi-channel approach. Also invoke alongside twilio-marketing-promotions-advisor or twilio-notifications-alerts-advisor whenever the developer has not yet confirmed a specific channel. |
| `/twilio-compliance-traffic` | 📋 Skill | Rules you must follow for Twilio messaging and voice traffic. Covers TCPA (consent tiers, quiet hours, DNC), GDPR (EU consent, right to deletion), PCI DSS (payment recording, Pay verb), HIPAA (BAA, PHI), FDCPA (debt collection limits), CAN-SPAM, WhatsApp policies, SHAKEN/STIR, and consent management patterns. Use this skill proactively when developers have working traffic to ensure they follow the rules. |
| `/twilio-debugging-observability` | 📋 Skill | Debug Twilio integrations and set up production observability. Covers the Console Debugger, Monitor Alerts API, Event Streams for error log streaming, status callback tracking, common error codes, and a systematic debugging workflow. Use this skill whenever a Twilio integration produces errors, messages fail to deliver, calls drop unexpectedly, or you need to set up monitoring for a production deployment. |
| `/twilio-lookup-phone-intelligence` | 📋 Skill | Look up phone number intelligence via Twilio Lookup v2 API. Covers number validation, line type detection (mobile/landline/VoIP), SIM swap detection, caller name, identity match, and SMS pumping risk scoring. Use this skill to validate numbers or assess fraud risk before sending messages or calls. |
| `/twilio-organizations-setup` | 📋 Skill | Set up and manage Twilio Organizations for centralized account and user governance. Covers the Organization > Account > Subaccount hierarchy, roles (Owner/Admin/Standard), managed vs independent accounts, domain registration, SSO enforcement, SCIM provisioning, and Organization merging. Use this skill when managing multiple Twilio accounts or users across teams. |
| `/twilio-email-send` | 📋 Skill | Use when the caller has Twilio credentials (Account SID + Auth Token or API Key SID + Secret) and needs to send email via comms.twilio.com/v1/Emails. This is Twilio-native email — NOT SendGrid. Do NOT use if the caller has a SendGrid API key (SG.-prefix) — use twilio-sendgrid-email-send instead. Covers single sends, batch sends up to 10,000 recipients, Liquid personalization, operation tracking, and error handling. |
| `/twilio-agent-augmentation-architect` | 📋 Skill | Planning skill for augmenting human agents with real-time AI intelligence. Qualifies the developer's use case across coaching, compliance, QA, and routing to recommend the right Conversation Intelligence + Conversation Memory + TaskRouter architecture. Handles both "I want to add AI coaching to my call center" and "configure Conversation Intelligence operators for script adherence." |
| `/twilio-conversations-classic-api` | 📋 Skill | Build multi-channel messaging experiences using Twilio Conversations (classic) API. Covers creating conversations, adding participants (SMS, WhatsApp, chat), sending messages, and handling webhooks. Use this skill to manage persistent multi-party or multi-channel conversations beyond single-message SMS/WhatsApp. |
| `/twilio-send-message` | 📋 Skill | Send messages via Twilio's Programmable Messaging API across all channels — SMS, MMS, RCS, and WhatsApp. Covers text messages, media, rich content (cards, carousels, buttons), template-based sends, Messaging Services, status callbacks, and WhatsApp's 24-hour service window. Use when the user wants to send a message — whether they say "send SMS", "text message", "branded message", "rich message", "WhatsApp message", "RCS message", "notification", or "alert". For picking the right channel for a use case, first consult twilio-messaging-channel-advisor. |
| `/twilio-conference-calls` | 📋 Skill | Build multi-party calls using Twilio Conference. Covers warm transfer, cold transfer, coaching (whisper), hold vs mute, participant modes, and supervisor barge. Use this skill for any contact center, support line, or scenario requiring transfers, holds, or multi-party calls. |
| `/twilio-voice-twiml` | 📋 Skill | Build voice call logic using TwiML (Twilio Markup Language). Covers the core verbs (Say, Play, Gather, Dial, Record, Conference), generating TwiML with Python and Node.js SDKs, and a complete inbound call IVR example. Use this skill to define call behavior for inbound or outbound calls. |
| `/twilio-customer-memory` | 📋 Skill | Store and retrieve customer context using Twilio Conversation Memory. Covers Memory Store provisioning, profile management, traits, observations, conversation summaries, and semantic Recall. Use this skill to give AI agents or human agents persistent memory of customer interactions across sessions and channels. |
| `/twilio-enterprise-knowledge` | 📋 Skill | Add knowledge retrieval to AI agents using Twilio's Enterprise Knowledge product. Enterprise Knowledge is a centralized, searchable repository of your organization's documents, websites, and content — FAQs, support policies, warranty terms, product catalogs. Current models don't have access to how you run your business today. Enterprise Knowledge gives agents a way to query this repository during a conversation and ground their responses in your actual approved source material. This skill covers provisioning a Knowledge Base and uploading knowledge sources from web URLs, PDFs, and raw text, and running semantic search to retrieve relevant chunks at runtime. Enterprise Knowledge is shared across your organization — it captures what your organization knows and how it is meant to run. It is distinct from Conversation Memory (twilio-customer-memory), which is scoped to individual end-customers and captures what you know about a specific person. The two are designed to be combined: enterprise content for business practices, customer memory for personalization. |
| `/twilio-voice-conversation-relay` | 📋 Skill | Build AI-powered voice agents using Twilio ConversationRelay. Handles real-time speech recognition (ASR), text-to-speech (TTS), and bidirectional audio streaming via WebSocket. Covers TwiML setup, WebSocket message types, LLM integration, streaming responses, and voice provider configuration. Use this skill to build voice bots, IVR replacements, or real-time AI voice assistants on Twilio calls. |
| `/twilio-rcs-messaging` | 📋 Skill | Send RCS Business Messages via Twilio. Covers compliance onboarding (7-part US process), sender profile setup, sending rich cards and carousels, SMS fallback, device support (Android + iOS 18 caveats), and common errors. Use this skill when building RCS messaging or onboarding an RCS sender. |
| `/twilio-ai-agent-architect` | 📋 Skill | Planning skill for AI-powered conversational agents. Qualifies the developer's use case across outcome sophistication, entry point, and customer profile to recommend the right Twilio Conversations architecture and implementation skills. Handles both high-level requests ("build me a voice AI assistant") and specific ones ("integrate ConversationRelay with my OpenAI backend"). |
| `/twilio-agent-connect` | 📋 Skill | Connect third-party AI agents (OpenAI, Bedrock, LangChain, Microsoft Foundry) to Twilio's communication channels using the Twilio Agent Connect SDK. Covers identity resolution, memory and context management via Conversation Memory, conversation orchestration via Conversation Orchestrator, multi-channel handling (Voice, SMS, RCS, WhatsApp, Chat), and AI-to-human escalation. Use this skill when integrating an existing LLM agent with Twilio services. |
| `/twilio-webhook-architecture` | 📋 Skill | Design, secure, and operate Twilio webhook endpoints. Covers inbound event handling, status callbacks, signature validation, connection overrides for retry and timeout tuning, local development tunneling, and production hardening. Use this skill whenever an agent needs to receive HTTP callbacks from Twilio for any product -- messaging, voice, verify, or event streams. |
| `/twilio-conversation-intelligence` | 📋 Skill | Twilio Conversation Intelligence development guide. Use when building real-time or post-call conversation analysis, language operator pipelines, sentiment analysis, agent assist, cross-channel analytics, or querying aggregated conversation insights (sentiment trends, escalation rates, dashboards). |
| `/twilio-compliance-onboarding` | 📋 Skill | Registrations required BEFORE Twilio traffic works. Covers messaging programs (A2P 10DLC, toll-free verification, WhatsApp WABA, RCS, short code, alphanumeric sender) and voice trust programs (STIR/SHAKEN, Voice Integrity, Branded Calling, CNAM). Each number/sender type has its own program — registration blocks traffic until complete. |
| `/twilio-security-api-auth` | 📋 Skill | Choose the right Twilio authentication method and implement it correctly. Covers Auth Token (testing only), API Keys (production standard), OAuth2 client_credentials (time-limited bearer tokens), Access Tokens (client-side SDKs), and test credentials. Use this skill before making any Twilio API calls in production. |
| `/twilio-isv-sms-best-practices` | 📋 Skill | Best practices for ISVs (Independent Software Vendors) building SMS features into multi-tenant SaaS platforms using Twilio. Covers customer onboarding for A2P and toll-free compliance, subaccount architecture, sender management, billing patterns, and common ISV pitfalls. Use this when building SMS capabilities that your customers will use to message their end users. |
| `/twilio-conversation-orchestrator` | 📋 Skill | Configure automatic conversation capture and routing with Twilio Conversation Orchestrator. Covers Configuration creation, channel capture rules, grouping types, status timeouts, Memory Store linkage, Intelligence linkage, and conversation lifecycle. Use this skill to automatically capture SMS, voice, WhatsApp, RCS, and web chat traffic into unified conversations without manually creating conversations or participants. |
| `/twilio-content-template-builder` | 📋 Skill | Create, manage, and send message templates using Twilio's Content API. Covers template creation for WhatsApp, SMS, RCS, and MMS; variable usage; WhatsApp Meta approval; and sending templates via ContentSid. Use this skill when building structured messages that require pre-approval or consistent formatting across channels. |
| `/twilio-sms-send-message` | 📋 Skill | SMS and MMS deep-dive reference. Covers SMS-specific error codes, message filtering troubleshooting ("Messages Being Filtered or Blocked?" diagnostic checklist), MMS media support (US/CA/AU only), and SMS pumping indicators. For sending SMS, use twilio-send-message instead. Use this skill only when debugging SMS delivery issues or needing SMS-specific details not in the consolidated send skill. |
| `/twilio-whatsapp-manage-senders` | 📋 Skill | Create, configure, and manage WhatsApp Business senders via Twilio's Channels Senders API. Covers programmatic sender registration, profile setup, webhook configuration, sender lifecycle statuses, and ISV flows. Use this skill to register and manage production WhatsApp senders at scale. |
| `/twilio-identity-verification-advisor` | 📋 Skill | Planning skill for identity verification and fraud prevention. Qualifies the developer's needs across authentication method, channel selection, fraud risk level, and user experience to recommend the right Twilio Verify + Lookup architecture. Handles login, signup, password reset, and risk-adaptive verification. |
| `/twilio-regulatory-compliance-bundles` | 📋 Skill | Manage regulatory compliance for international phone numbers. Covers what bundles are, which countries require them, how to create End-Users and Supporting Documents, evaluate and submit bundles, fix evaluation failures, update bundles when regulations change, and ISV multi-account patterns. Use this skill when provisioning numbers outside the US. |
| `/twilio-taskrouter-routing` | 📋 Skill | Route tasks to agents using Twilio TaskRouter. Covers Workers, Task Queues, Workflows, Reservations, skills-based routing, and common gotchas (hyphen attributes, HAS operator, reservation cascade). Use this skill for any multi-agent contact center, support queue, or AI agent escalation routing. |
| `/twilio-messaging-webhooks` | 📋 Skill | Receive and respond to inbound messages and track outbound delivery status via Twilio webhooks — across SMS, MMS, WhatsApp, and RCS. Covers webhook request parameters, replying with TwiML, validating webhook signatures for security, and handling status callbacks. Use this skill whenever an agent needs to handle incoming messages on any channel or track outbound message delivery in real time. |
| `/twilio-verify-send-otp` | 📋 Skill | Send and verify one-time passcodes (OTPs) via Twilio Verify over SMS, RCS, voice, email, or WhatsApp. Covers creating a Verify Service, sending tokens, checking submitted codes, automatic WhatsApp-to-SMS fallback, and service configuration. TOTP is supported via the Factors API (a separate family from channel-based OTP). Use this skill to add phone or email verification or two-factor authentication to any application. |
| `/twilio-messaging-services` | 📋 Skill | Create and configure Twilio Messaging Services for production messaging. Covers sender pools, geo-match, sticky sender, message scheduling, compliance toolkit, SMS pumping protection, link shortening, and intelligent alerts. Use this skill when setting up production-ready messaging infrastructure. |
| `/twilio-numbers-senders` | 📋 Skill | Choose the right Twilio number type and sender BEFORE building. Covers phone numbers (local, toll-free, short code, mobile), alphanumeric sender IDs, WhatsApp senders, RCS agents, international availability, and regulatory bundles. Each number type has its own compliance program — choosing wrong means rebuilding. Use this skill first. |
| `/twilio-marketing-promotions-advisor` | 📋 Skill | Planning skill for marketing and promotional messaging. Use when a developer is figuring out how to set up or architect a marketing campaign on Twilio — channel selection, compliance readiness, audience size, geography, and delivery tracking. Handles open-ended requests like "how do I set up a WhatsApp marketing campaign" or "what's the best way to run promotional SMS." Skip this skill when the developer already knows what they want and is asking for API specs or implementation details. |
| `/twilio-call-recordings` | 📋 Skill | Record Twilio voice calls correctly. Covers the critical distinction between Record verb (voicemail) and Dial record (call recording), dual-channel for QA, mid-call pause for PCI, Conference recording, and the ConversationRelay workaround. Use this skill whenever you need to capture call audio for compliance, QA, or analytics. |
| `/twilio-security-hardening` | 📋 Skill | Secure Twilio applications against common attacks. Covers credential management (API keys vs auth tokens), request validation (webhook signature verification), PCI DSS compliance, HIPAA account requirements, SMS pumping prevention, geo-permissions, and account isolation patterns. Use this skill when developers are building or deploying Twilio apps. |
| `/twilio-security-compliance-hipaa` | 📋 Skill | Configure Twilio accounts for HIPAA compliance. Covers BAA requirements, HIPAA Project designation (self-service and support), eligible services list, per-product requirements (Voice, SMS, ConversationRelay, Conversation Intelligence, Flex, Verify), message redaction, and what is NOT eligible. Use this skill when developers are building healthcare workflows on Twilio. |
| `/twilio-customer-support-architect` | 📋 Skill | Planning skill for building customer service and support systems. Qualifies the developer's needs across the support ladder (self-service → AI agents → contact center), channel mix, and scale to recommend the right Twilio architecture. Handles both "build me a call center" and "add an IVR to my existing support line." |
| `/twilio-sendgrid-email-settings` | 📋 Skill | Configure SendGrid dynamic templates (Handlebars), tracking settings (opens, clicks, subscriptions), link branding for custom tracking domains, and content types (HTML, plain text, AMP). Use when customizing SendGrid email content, tracking behavior, or branded links. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com). |
| `/twilio-sendgrid-account-setup` | 📋 Skill | Set up a SendGrid account for email delivery. Covers API key creation (SG.-prefix), domain authentication (DKIM/SPF via CNAME records), Single Sender Verification for testing, SDK installation, and the relationship between SendGrid and Twilio credentials. Use before any other SendGrid skill. This skill is for SendGrid only — not the Twilio Email API (comms.twilio.com). |
| `/twilio-sendgrid-email-send` | 📋 Skill | Send transactional and bulk email via the SendGrid v3 Mail Send API. Covers single sends, personalized batch sends with dynamic templates, scheduled sends with cancellation, attachments, and sandbox mode for testing. Use this skill when the caller has a SendGrid API key (SG.-prefix). Do NOT use this skill if the caller is using the Twilio Email API (comms.twilio.com) — that is a separate product with different credentials. |
| `/twilio-sendgrid-deliverability-advisor` | 📋 Skill | Diagnostic and advisory skill for email deliverability problems. Use when a developer asks why emails are going to spam, not reaching the inbox, getting blocked, bouncing, or how to improve sender reputation — with or without a specified platform. Covers SendGrid-specific tooling: SPF, DKIM, DMARC, BIMI, IP warmup, list hygiene, bounce/spam rate thresholds, and Engagement Quality Score (SEQ). Do NOT use for Twilio Email (comms.twilio.com / Account SID + Auth Token) — use twilio-email-deliverability-advisor instead. Do NOT use for general email sending questions — use twilio-sendgrid-email-send (SendGrid) or twilio-email-deliverability-advisor instead. |
| `/twilio-sendgrid-inbound-parse` | 📋 Skill | Receive inbound email via SendGrid Inbound Parse webhook. Covers MX record setup, parsed vs raw mode, handling attachments, and common pitfalls. Use when building email-to-app workflows like support ticket creation or email processing pipelines. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com). |
| `/twilio-sendgrid-suppressions` | 📋 Skill | Manage SendGrid email suppressions: bounces, blocks, spam reports, invalid emails, global unsubscribes, and ASM suppression groups. Covers when and how to remove suppressions, reputation impact, and category-based unsubscribe management. Use when debugging SendGrid delivery issues or building unsubscribe flows. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com). |
| `/twilio-sendgrid-webhooks` | 📋 Skill | Track email delivery and engagement via SendGrid Event Webhooks. Covers all 11 event types (delivery + engagement), webhook handler implementation, ECDSA signature verification, batched event processing, and common debugging patterns. Use when building SendGrid delivery tracking, engagement analytics, or bounce handling. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com). |
| `/twilio-sendgrid-engagement-quality` | 📋 Skill | Monitor email program health with SendGrid Engagement Quality (SEQ) scores. Covers the SEQ API endpoints, the 5 scoring metrics (engagement recency, open rate, bounce classification, bounce rate, spam rate), eligibility requirements, and interpreting scores for deliverability improvement. Use when diagnosing SendGrid deliverability issues or monitoring sender reputation. Requires a SendGrid API key (SG.-prefix) — not applicable to the Twilio Email API (comms.twilio.com). |

<a id="p-typescript-lsp"></a>

**typescript-lsp**（🔍 LSP）

> TypeScript/JavaScript 语言服务器

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `lsp__typescript` | 🔍 LSP | TypeScript/JavaScript language server for enhanced code intelligence。需手动安装: npm install -g typescript-language-server typescript |
<a id="p-ui5"></a>

**ui5**（3 Skill）

> SAPUI5/OpenUI5 项目创建与验证

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ui5-best-practices` | 📋 Skill | UI5 development best practices and coding standards derived exclusively from official SAP UI5 guidelines. Use when writing UI5 applications to ensure modern, maintainable code following SAP standards. Covers: async module loading (sap.ui.define, ES6 imports, core:require), ComponentSupport initialization, data binding with OData types, i18n management, CSP compliance (no inline scripts), TypeScript event types (UI5 >= 1.115.0), MCP tooling (get_api_reference, run_ui5_linter), CAP integration patterns, and form creation rules (never SimpleForm, always Form with ColumnLayout). Keywords: ui5 coding standards, async loading, sap.ui.define, data binding, odata types, i18n translation, CSP no inline scripts, TypeScript event handlers, Button$PressEvent, ui5 linter, API reference, ComponentSupport, form layout, ColumnLayout, CAP integration, cds watch |
| `/ui5-best-practices-integration-cards` | 📋 Skill | MUST be loaded before any UI Integration Cards (also called UI5 Integration Cards) task — creating, modifying, validating, previewing, or reviewing a card, its `manifest.json`, its Configuration Editor (`dt/Configuration.js`), or any analytical chart configuration. Provides the official guidelines, validation rules, supported chart types, and Configuration Editor patterns. |
| `/ui5-best-practices-opa5` | 📋 Skill | This skill should be used in any OPA5 task - creating, modifying, extending, debugging, fixing or reviewing an integration test. Use when the user asks to "write an OPA5 test", "add an OPA5 journey", "fix the OPA5 test failure" or mentions OPA5 or its components - opaTest, page object, journey, waitFor. |

<a id="p-ui5-typescript-conversion"></a>

**ui5-typescript-conversion**（1 Skill）

> SAPUI5 项目 JS 转 TypeScript

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ui5-typescript-conversion` | 📋 Skill | A skill for converting UI5 (SAPUI5/OpenUI5) projects to TypeScript. |

<a id="p-wix"></a>

**wix**（4 Skill）

> Wix 网站和应用构建管理部署

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/wix-design-system` | 📋 Skill | Wix Design System component reference. Use when building UI with @wix/design-system, choosing components, checking props and examples, or writing tests with component testkits. Triggers on "what component", "how do I make", "WDS", "show me props", "testkit", "driver", or component names like Button, Card, Box, Text. |
| `/wix-manage` | 📋 Skill | Wix business solution management recipes — REST API operations for configuring and managing Wix business solutions. Routes to: stores, bookings, get-paid, CMS, contacts, forms, media, app-installation, pricing-plans, restaurants, rich-content, sites, blog, calendar, domains, site-properties, ecommerce. |
| `/wix-headless` | 📋 Skill | Build a complete Wix Managed Headless site from a single prompt, OR connect an existing project (HTML/JSX/Vite app, Claude Design output, etc.) to Wix Headless for hosting + Business Solutions. Entry point for both: (1) new-site requests — runs discovery, design, feature wiring, and preview; and (2) existing-project requests — runs `npm create @wix/new@latest init`, analyzes the project for needed Business Solutions, installs apps, **wires the Wix SDK into the existing source files so each installed app actually powers its corresponding feature**, and releases. Triggers: build me a site, create a website, make me a website, new website, online store, I want to sell X, start a business online, launch a site, ecommerce, portfolio, business website, sell online, online shop, take bookings, book appointments, appointment scheduling, let clients book online, site for my salon/spa/clinic/studio, sign up for classes or sessions, connect this to Wix Headless, add Wix Headless to this project, host this on Wix, deploy this to Wix, implement the features of this project using Wix Headless. Use this skill instead of the WixSiteBuilder MCP tool for new-site requests. |
| `/wix-app` | 📋 Skill | Build and review Wix CLI app extensions — dashboard pages, modals, plugins, menu plugins, custom element widgets, Editor React components, site plugins, embedded scripts, backend APIs, backend events, service plugins, data collections, and App Market readiness. Use when building ANY feature or extension for a Wix CLI app or preparing a Wix app for App Market review. Triggers on: add, build, create, implement, help me, dashboard, widget, plugin, backend, API, event, collection, embedded script, service plugin, Editor React component, checkout, shipping, tax, discount, SPI, CMS, schema, tracking, popup, admin panel, menu item, modal, validate, test, verify, register extension, App Market, app review, submission readiness. |

<a id="p-zoom-plugin"></a>

**zoom-plugin**（32 Skill）

> Zoom 集成规划构建与调试

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/setup-zoom-oauth` | 📋 Skill | Implement Zoom authentication correctly. Use when setting up app credentials, choosing an OAuth grant, requesting scopes, handling token refresh, or debugging auth failures. |
| `/setup-zoom-mcp` | 📋 Skill | Decide when Zoom MCP is the right fit and produce a safe setup plan for Claude. Use when planning AI workflows over Zoom data, deciding between MCP and REST, or defining a hybrid MCP architecture. |
| `/debug-zoom` | 📋 Skill | Debug a broken Zoom integration by isolating the failure point and routing into the right Zoom references. Use when auth, API, webhook, SDK, or MCP behavior is failing and you need a ranked hypothesis list plus verification steps. |
| `/plan-zoom-integration` | 📋 Skill | Turn a Zoom integration idea into an implementation plan with architecture, auth, and delivery milestones. Use when you need a practical build plan, phased delivery sequence, risk list, and next-step recommendation. |
| `/start` | 📋 Skill | Start here for any Zoom integration or app idea. Use when you need to choose the right Zoom surface, shape the architecture, or route into the correct implementation skill without reading the whole Zoom doc set first. |
| `/build-zoom-team-chat-app` | 📋 Skill | Reference skill for Zoom Team Chat. Use after routing to a chat workflow when building user-scoped messaging integrations, chatbot experiences, rich cards, buttons, slash commands, or chat webhooks. |
| `/zoom-cobrowse-sdk` | 📋 Skill | Reference skill for Zoom Cobrowse SDK. Use after routing to a collaborative-support workflow when implementing browser co-browsing, annotation tools, privacy masking, remote assist, or PIN-based session sharing. |
| `/build-zoom-bot` | 📋 Skill | Build a Zoom meeting bot, recorder, or real-time media workflow. Use when joining meetings programmatically, processing live media or transcripts, or combining Meeting SDK, RTMS, and backend services. |
| `/build-zoom-meeting-sdk-app` | 📋 Skill | Reference skill for Zoom Meeting SDK. Use after routing to a meeting-embed workflow when implementing real Zoom meeting joins, platform-specific SDK behavior, auth and join flows, waiting room issues, or meeting bot patterns. |
| `/build-zoom-rest-api-app` | 📋 Skill | Reference skill for Zoom REST API. Use after choosing an API-based workflow when you need endpoint selection, resource-management patterns, OAuth requirements, rate-limit awareness, or API error debugging. |
| `/plan-zoom-product` | 📋 Skill | Choose the right Zoom building surface for a use case and explain the tradeoffs clearly. Use when deciding between REST API, Webhooks, WebSockets, Meeting SDK, Video SDK, Zoom Apps SDK, Phone, Contact Center, or MCP for a specific product idea or integration goal. |
| `/zoom-oauth` | 📋 Skill | Reference skill for Zoom authentication. Use after routing to an auth workflow when choosing app credentials, grant types, scopes, token refresh behavior, or debugging Zoom OAuth failures. |
| `/ui-toolkit/web` | 📋 Skill | Reference skill for Zoom Video SDK UI Toolkit. Use after routing to a web video workflow when you want prebuilt React UI instead of building a fully custom Video SDK interface. |
| `/probe-sdk` | 📋 Skill | Reference skill for Zoom Probe SDK. Use after routing to a preflight workflow when testing browser compatibility, media permissions, audio or video diagnostics, and network readiness before users join. |
| `/build-zoom-video-sdk-app` | 📋 Skill | Reference skill for Zoom Video SDK. Use after routing to a custom-session workflow when the user needs full control over the video experience rather than an actual Zoom meeting. |
| `/scribe` | 📋 Skill | Reference skill for Zoom AI Services Scribe. Use after routing to a transcription workflow when handling uploaded or stored media, Build-platform JWT auth, fast mode transcription, batch jobs, or transcript pipeline design. |
| `/setup-zoom-webhooks` | 📋 Skill | Reference skill for Zoom webhooks. Use after routing to an event-driven workflow when implementing subscriptions, signature verification, delivery handling, retries, or event-type selection. |
| `/setup-zoom-websockets` | 📋 Skill | Reference skill for Zoom WebSockets. Use after routing to a low-latency event workflow when persistent connections, faster event delivery, or security constraints make WebSockets preferable to webhooks. |
| `/zoom-mcp` | 📋 Skill | Guidance for the bundled Zoom MCP connectors. Use after routing to an MCP workflow when planning or troubleshooting tool-based access to meetings, recordings, meeting assets, transcripts, Zoom-wide search, or Zoom Docs. Route Whiteboard-specific requests to `zoom-mcp/whiteboard` and write-capable Team Chat MCP requests to `zoom-mcp/team-chat`. |
| `/build-zoom-contact-center-app` | 📋 Skill | Reference skill for Zoom Contact Center. Use after routing to a contact-center workflow when implementing app, web, or native integrations; engagement context and state handling; campaigns; callbacks; or version-drift troubleshooting. |
| `/build-zoom-virtual-agent` | 📋 Skill | Reference skill for Zoom Virtual Agent. Use after routing to a virtual-agent workflow when implementing web embeds, Android or iOS wrapper integrations, knowledge-base sync, lifecycle handling, or troubleshooting. |
| `/build-zoom-phone-integration` | 📋 Skill | Reference skill for Zoom Phone. Use after routing to a phone workflow when implementing OAuth, Phone APIs, webhooks, Smart Embed events, URI schemes, CRM or CTI dialers, or call handling automation. |
| `/zoom-rtms` | 📋 Skill | Reference skill for Zoom RTMS. Use after routing to a live-media workflow when processing real-time audio, video, chat, transcripts, screen share, or contact-center voice streams. |
| `/zoom-apps-sdk` | 📋 Skill | Reference skill for Zoom Apps SDK. Use after routing to an in-client app workflow when building web apps that run inside Zoom meetings, webinars, the main client, or Zoom Phone. |
| `/choose-zoom-approach` | 📋 Skill | Choose the right Zoom architecture for a use case. Use when deciding between REST API, Webhooks, WebSockets, Meeting SDK, Video SDK, Zoom Apps SDK, Zoom MCP, Phone, Contact Center, or a hybrid approach. |
| `/build-zoom-meeting-app` | 📋 Skill | Build or embed a Zoom meeting flow. Use when implementing Meeting SDK joins, web or mobile meeting embeds, meeting lifecycle flows, or when deciding between Meeting SDK and Video SDK. |
| `/zoom-general` | 📋 Skill | Cross-product Zoom reference skill. Use after the workflow is clear when you need shared platform guidance, app-model comparisons, authentication context, scopes, marketplace considerations, or API-vs-MCP routing. |
| `/summarizer` | 📋 Skill | Reference skill for Zoom AI Services Summarizer. Use after routing to transcript summarization, meeting recap, action item extraction, Build-platform JWT auth, fast mode summarization, batch jobs, or summary pipeline design. |
| `/rivet-sdk` | 📋 Skill | Reference skill for Zoom Rivet SDK. Use after routing to a Rivet-based server workflow when implementing auth handling, webhook consumers, API wrappers, multi-module composition, or Lambda receiver patterns. |
| `/design-mcp-workflow` | 📋 Skill | Design a Zoom MCP workflow for Claude. Use when deciding whether Zoom MCP fits a task, when planning tool-based AI workflows, or when separating MCP responsibilities from REST API responsibilities. |
| `/debug-zoom-integration` | 📋 Skill | Debug broken Zoom implementations quickly. Use when auth, webhooks, SDK joins, MCP transport, or real-time media workflows are failing and you need to isolate the layer before proposing a fix. |
| `/translator` | 📋 Skill | Reference skill for Zoom AI Services Translator. Use after routing to text translation, one-target-language jobs, Build-platform JWT auth, fast mode translation, batch file translation, or translation pipeline design. |


## 📋 Productivity（42 个插件）

<a id="p-airtable"></a>

**airtable**（8 Skill）

> Airtable 数据库与智能体运营平台

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/airtable-filters` | 📋 Skill | Builds Airtable filters parameters for the MCP tools that list or display records — field-type-aware comparison operators, choice and collaborator IDs, date ranges, and nested AND/OR logic. Use when the user wants to find, filter, narrow down, or search Airtable records by field values, even when they don't explicitly say "filter." |
| `/marketing-ops` | 📋 Skill | Set up and run Airtable-based marketing operations workflows — request intake, campaign orchestration, creative production, content calendars, brand and compliance review, events, localization, budgets and ROI, capacity planning. Use when the user wants a marketing request "front door," to manage campaigns, coordinate briefs and assets, build a content calendar, plan launches or events, track budgets, measure ROI, or set up agency multi-client delivery. Adapts to org size (solo marketer to enterprise multi-brand or agency) and integrates with or displaces tools like HubSpot, Marketo, Mailchimp, Klaviyo, Workfront, Asana, Monday, and Wrike. Asks scope first. |
| `/airtable-overview` | 📋 Skill | Explains what Airtable is and how data is structured — bases, tables, fields, records, views, automations, and interfaces. Use when you need context about the Airtable data model. |
| `/agent-activity-log` | 📋 Skill | Scaffold and operate an opt-in `Agent activity log` table that records what the agent did, decided, and got blocked on across a long-running or multi-session Airtable workflow. Use whenever a workflow skill (product-ops, sales-ops, marketing-ops, etc.) is being set up for an agent-driven motion (recurring triage, multi-step plan, automated monitoring, agentic workflow), or when the user explicitly asks for "agent activity tracking," "audit log of agent decisions," "agent memory," "track what the agent did," or similar. The pattern is opt-in (front-load the offer, frame as auditability for the user's benefit, not surveillance). Composes into workflow skills the same way `show-airtable-link` does — workflow skills point at this skill rather than re-implementing the schema inline. |
| `/sales-ops` | 📋 Skill | Set up and run Airtable-based sales operations and CRM workflows — pipeline management, account and renewal management, deal desk, RFP / tender pipelines, partner CRMs, sales forecasting, vertical CRMs (real estate, mortgage, brokerage, capital markets, public works, nonprofit), and AI-native lean stacks (Clay-equivalent enrichment, AI-assisted outbound, conversation-intel ingestion). Use when the user wants to track deals, manage accounts, build a pipeline, run a deal desk, coordinate partners, manage RFPs, or build an AI-forward GTM stack. Defaults to augmenting existing CRMs (Salesforce / HubSpot); also supports Airtable-as-CRM and AI-native stacks. Asks scope first. Commercial workflows only; post-sale support belongs to a future customer-success skill. |
| `/airtable-cli` | 📋 Skill | Lists bases, reads and writes records, manages tables and fields, filters and searches data in Airtable via the `airtable-mcp` CLI. Use when the task involves Airtable data or the user mentions airtable-mcp, bases, tables, records, or fields. |
| `/product-ops` | 📋 Skill | Set up and run Airtable-based product operations workflows — roadmap management, customer feedback synthesis, launch coordination, OKR cascading, sprint planning, release tracking. Use when the user wants to track product work, manage feature requests, build a roadmap, set up a feedback intake portal, prioritize initiatives, run launch checklists, or align OKRs across teams. Adapts to org size (solo founder, small team, mid-size product org, enterprise product portfolio) and existing tooling (Jira / Linear / Productboard / Aha integration; Salesforce / Zendesk / Gong feedback ingestion). Can scaffold either as a pure-Airtable workspace or as Airtable backing a custom branded UI on Vercel for public-facing portals. Asks scope questions first; doesn't impose framework. Focuses on cross-functional product operations. |
| `/show-airtable-link` | 📋 Skill | Provides a clickable Airtable link whenever the agent has touched user-visible Airtable content. Use after every MCP call that creates, updates, lists, searches, or returns records, schema, or interface pages — bases, tables, fields, records, or pages. Hand off the most-specific URL the agent's tool calls have proven access to — prefer single-record URLs over table URLs, table URLs over base URLs, and interface page URLs when the user's access is restricted to pages. Format as a markdown link with a descriptive label. Construct URLs only from IDs the tools actually returned — never synthesize IDs to round out a URL. Compose this skill from any workflow skill that affects Airtable content. |

<a id="p-airwallex"></a>

**airwallex**（🔌 MCP）

> Airwallex 支付账单与现金流管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__airwallex` | 🔌 MCP | Airwallex CLI plugin for Claude — skills for payments, billing, invoicing, beneficiary creation, card provisioning, and cashflow management. |
<a id="p-apollo"></a>

**apollo**（4 Skill）

> Apollo 销售线索挖掘与分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sequence-load` | 📋 Skill | Find leads matching criteria and bulk-add them to an Apollo outreach sequence. Handles enrichment, contact creation, deduplication, and enrollment in one flow. |
| `/prospect` | 📋 Skill | Full ICP-to-leads pipeline. Describe your ideal customer in plain English and get a ranked table of enriched decision-maker leads with emails and phone numbers. |
| `/enrich-lead` | 📋 Skill | Instant lead enrichment. Drop a name, company, LinkedIn URL, or email and get the full contact card with email, phone, title, company intel, and next actions. |
| `/analytics` | 📋 Skill | Instant sales analytics. Ask any performance question — emails, calls, meetings, tasks, opportunities, sequences, conversation intelligence — and get formatted tables with real Apollo data. |

<a id="p-asana"></a>

**asana**（🔌 MCP）

> Asana 项目管理与任务跟踪

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__asana` | 🔌 MCP | Asana project management integration. Create and manage tasks, search projects, update assignments, track progress, and integrate your development ... |
<a id="p-atlassian"></a>

**atlassian**（5 Skill）

> Atlassian Jira 与 Confluence 集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/generate-status-report` | 📋 Skill | Generate project status reports from Jira issues and publish to Confluence. When an agent needs to: (1) Create a status report for a project, (2) Summarize project progress or updates, (3) Generate weekly/daily reports from Jira, (4) Publish status summaries to Confluence, or (5) Analyze project blockers and completion. Queries Jira issues, categorizes by status/priority, and creates formatted reports for delivery managers and executives. |
| `/triage-issue` | 📋 Skill | Intelligently triage bug reports and error messages by searching for duplicates in Jira and offering to create new issues or add comments to existing ones. When an agent needs to: (1) Triage a bug report or error message, (2) Check if an issue is a duplicate, (3) Find similar past issues, (4) Create a new bug ticket with proper context, or (5) Add information to an existing ticket. Searches Jira for similar issues, identifies duplicates, checks fix history, and helps create well-structured bug reports. |
| `/search-company-knowledge` | 📋 Skill | Search across company knowledge bases (Confluence, Jira, internal docs) to find and explain internal concepts, processes, and technical details. When an agent needs to: (1) Find or search for information about systems, terminology, processes, deployment, authentication, infrastructure, architecture, or technical concepts, (2) Search internal documentation, knowledge base, company docs, or our docs, (3) Explain what something is, how it works, or look up information, or (4) Synthesize information from multiple sources. Searches in parallel and provides cited answers. |
| `/spec-to-backlog` | 📋 Skill | Automatically convert Confluence specification documents into structured Jira backlogs with Epics and implementation tickets. When an agent needs to: (1) Create Jira tickets from a Confluence page, (2) Generate a backlog from a specification, (3) Break down a spec into implementation tasks, or (4) Convert requirements into Jira issues. Handles reading Confluence pages, analyzing specifications, creating Epics with proper structure, and generating detailed implementation tickets linked to the Epic. |
| `/capture-tasks-from-meeting-notes` | 📋 Skill | Analyze meeting notes to find action items and create Jira tasks for assigned work. When an agent needs to: (1) Create Jira tasks or tickets from meeting notes, (2) Extract or find action items from notes or Confluence pages, (3) Parse meeting notes for assigned tasks, or (4) Analyze notes and generate tasks for team members. Identifies assignees, looks up account IDs, and creates tasks with proper context. |

<a id="p-box"></a>

**box**（10 Skill）

> Box 云存储文件管理与协作

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/box-legal-workflows` | 📋 Skill | Legal concepts for Box-based legal workflows — risk rating frameworks, human-in-the-loop requirements, confidentiality principles, Box AI governance, collaboration roles, metadata strategy, and common workflow patterns. Referenced by box-legal-workflows-ma, box-legal-workflows-intake, and box-legal-workflows-contract skills. |
| `/box-legal-workflows-ma` | 📋 Skill | Build and manage M&A Virtual Data Rooms with Box MCP — create secure folder structures with numbered prefixes for due diligence, assign role-based access to internal teams and external parties (counsel, auditors, buyers), validate permissions before sharing sensitive deal information, use Box AI for cross-document due diligence questions, and organize uploaded files by category. Use this skill when the user mentions M&A, deal rooms, data rooms, due diligence, VDR, mergers and acquisitions, or needs to set up a secure repository for deal documents with controlled external access. |
| `/box-legal-workflows-contract` | 📋 Skill | Automate contract review and monitoring with Box MCP — identify new contracts added since last review period using metadata or keyword search, compare contracts against standard firm templates to flag material variances (indemnification, liability caps, termination rights, governing law, IP ownership), extract and write structured metadata (parties, dates, contract value, key clauses, risk ratings, expiration dates) to Box for searchability, create variance analysis reports with citations, proactively monitor for expiring contracts to trigger renegotiation reminders with calculated notice deadlines, and batch process multiple contracts with rate-limit-aware pacing. Use this skill when the user mentions contract review, contract monitoring, NDA review, MSA comparison, contract expiration, contract metadata, variance analysis, or needs recurring contract analysis workflows. |
| `/box-legal-workflows-intake` | 📋 Skill | Automate legal client intake and onboarding with Box MCP — review uploaded intake documents for completeness against firm requirements, assess risk levels based on client profile and document content (PEP status, conflicts, sanctions, litigation history), route incomplete or high-risk submissions to appropriate attorneys with context and risk summaries, extract structured metadata (client name, matter type, jurisdiction, value), and generate engagement letters from Box DocGen templates for approved low-risk clients. Use this skill when the user mentions client intake, client onboarding, new client review, intake documents, engagement letters, or needs to process prospective client submissions stored in Box. |
| `/box` | 📋 Skill | Build and troubleshoot Box integrations for uploads, folders, folder listings, downloads and previews, shared links, collaborations, search, metadata, event-driven automations, and Box AI retrieval flows. Also covers working with Box content via the Box MCP server — search, read, upload, organize files, run Box AI queries, and extract structured metadata. Use when the agent needs to add Box APIs or SDKs to an app, wire Box-backed document workflows, organize or share content, react to new files, fetch Box content for search, summarization, extraction, or question-answering, or operate on Box content through MCP tools. |
| `/box` | 📋 Skill | Build and troubleshoot Box integrations for uploads, folders, folder listings, downloads and previews, shared links, collaborations, search, metadata, event-driven automations, and Box AI retrieval flows. Also covers working with Box content via the Box MCP server — search, read, upload, organize files, run Box AI queries, and extract structured metadata. Use when the agent needs to add Box APIs or SDKs to an app, wire Box-backed document workflows, organize or share content, react to new files, fetch Box content for search, summarization, extraction, or question-answering, or operate on Box content through MCP tools. |
| `/box-legal-workflows` | 📋 Skill | Legal concepts for Box-based legal workflows — risk rating frameworks, human-in-the-loop requirements, confidentiality principles, Box AI governance, collaboration roles, metadata strategy, and common workflow patterns. Referenced by box-legal-workflows-ma, box-legal-workflows-intake, and box-legal-workflows-contract skills. |
| `/box-legal-workflows-contract` | 📋 Skill | Automate contract review and monitoring with Box MCP — identify new contracts added since last review period using metadata or keyword search, compare contracts against standard firm templates to flag material variances (indemnification, liability caps, termination rights, governing law, IP ownership), extract and write structured metadata (parties, dates, contract value, key clauses, risk ratings, expiration dates) to Box for searchability, create variance analysis reports with citations, proactively monitor for expiring contracts to trigger renegotiation reminders with calculated notice deadlines, and batch process multiple contracts with rate-limit-aware pacing. Use this skill when the user mentions contract review, contract monitoring, NDA review, MSA comparison, contract expiration, contract metadata, variance analysis, or needs recurring contract analysis workflows. |
| `/box-legal-workflows-intake` | 📋 Skill | Automate legal client intake and onboarding with Box MCP — review uploaded intake documents for completeness against firm requirements, assess risk levels based on client profile and document content (PEP status, conflicts, sanctions, litigation history), route incomplete or high-risk submissions to appropriate attorneys with context and risk summaries, extract structured metadata (client name, matter type, jurisdiction, value), and generate engagement letters from Box DocGen templates for approved low-risk clients. Use this skill when the user mentions client intake, client onboarding, new client review, intake documents, engagement letters, or needs to process prospective client submissions stored in Box. |
| `/box-legal-workflows-ma` | 📋 Skill | Build and manage M&A Virtual Data Rooms with Box MCP — create secure folder structures with numbered prefixes for due diligence, assign role-based access to internal teams and external parties (counsel, auditors, buyers), validate permissions before sharing sensitive deal information, use Box AI for cross-document due diligence questions, and organize uploaded files by category. Use this skill when the user mentions M&A, deal rooms, data rooms, due diligence, VDR, mergers and acquisitions, or needs to set up a secure repository for deal documents with controlled external access. |

<a id="p-carta-cap-table"></a>

**carta-cap-table**（12 Skill）

> Carta 股权结构表与估值管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/carta-waterfall-scenarios` | 📋 Skill | Exit, sale, acquisition, and liquidation payouts for a company — answers how much money each holder walks away with at a given sale price, return multiples on holdings, and how proceeds distribute across share classes. Computes dollar amounts at modeled valuations, not abstract rights. |
| `/carta-compensation-rolematcher` | 📋 Skill | Classify a job title or description into the CTC taxonomy (job area, focus, level, track). Use when the user wants to know how a role is categorized or mapped to the taxonomy structure — not to fetch salary, equity, or benchmark numbers. Do NOT use when the user is asking for "market rates", "benchmark data", "compensation ranges", "what does X pay", or "show me benchmarks" — use carta-compensation-benchmarks for that. Do NOT use for general career advice or job search queries unrelated to compensation benchmarking. |
| `/carta-round-history` | 📋 Skill | Financing round history for a company — each priced round with its date, share class issued, price per share, total cash raised, and the investors who participated. Covers what was raised and from whom across the company's funding history. |
| `/carta-discover-commands` | 📋 Skill | META-DISCOVERY ONLY — answers the question "what cap-table tools or commands exist?" when the user is lost about what's available. NEVER use this skill for any request that names a cap-table topic (stakeholders, grants, vesting, SAFEs, notes, valuations, ownership, waterfall, financing, exposure, etc.) — those are always direct data requests, even if the user phrases them vaguely. The matching specialist skill wins every time over this one. |
| `/carta-grant-vesting` | 📋 Skill | Fetch the vesting schedule for ONE specific grant or holder — options (ISO/NSO), RSUs, SARs, or CBUs. Use for "how much has [name] vested", "when does [name]'s cliff hit", "vesting progress for [name]", cliff dates, settlement, or unvested shares. NOT for portfolio-level / all-employees aggregate vesting. |
| `/carta-portfolio-alerts` | 📋 Skill | Time-bounded and threshold-bounded risk detection across portfolio companies — finds items that are expiring soon, maturing soon, running low, or otherwise at risk. Surfaces what needs attention now, not what the data looks like in general. |
| `/carta-valuation-history` | 📋 Skill | Fetch 409A valuation history and current fair market value (FMV) for a company. Use when asked about 409A valuations, FMV, exercise prices, common stock price, or valuation expiration dates. Do NOT use for cross-portfolio FMV comparisons across companies — prefer a portfolio-benchmarks skill. |
| `/carta-market-benchmarks` | 📋 Skill | Computed statistics across portfolio companies — median, average, typical, range — used as market benchmarks. Returns aggregate numbers and percentiles, not raw per-company listings. |
| `/carta-witness-signatures` | 📋 Skill | Status of witness and spousal-consent signature requests on option grants, RSAs, PIUs — who still needs to sign, and what's awaiting signature, signed, or expired. Covers one award, one company, or a whole portfolio. Read-only. |
| `/carta-interaction-reference` | 📋 Skill | Carta's behavioral rules for AI agents presenting cap table data — mandatory context for any Carta cap table response. Load ONCE per conversation, before the first such response (ownership, grants, SAFEs, valuations, waterfall scenarios, financing history, stakeholders, convertible instruments, option pools, or any other topic). If already loaded earlier in this conversation, do NOT reload — the prior tool_result remains in your context. Load alongside the domain skill (e.g. carta-reporting), not instead of it. |
| `/carta-compensation-benchmarks` | 📋 Skill | Retrieves Carta Total Compensation market benchmarks (salary, equity, total cash) for a role. Output to chat or CSV. Market benchmarks are triggered by queries like: "sales benchmarks", "comp benchmarks", "market rate", "what does a [role] pay", "put benchmarks in a CSV". Do NOT use for job classification or role mapping — use carta-compensation-rolematcher for that. Do NOT use for fund performance benchmarks (use carta-performance-benchmarks) or portfolio structural metrics like SAFE terms and option pool sizes (use carta-market-benchmarks). |
| `/carta-conversion-calculator` | 📋 Skill | Calculate SAFE and convertible note conversion into equity at a financing close. Use when asked about SAFE conversion, note conversion, conversion shares, conversion math, how instruments convert in a priced round, or what happens to outstanding SAFEs and notes when a new round closes. Do NOT use for exit/sale/acquisition payouts at a sale price — those are waterfall scenarios, prefer a waterfall-scenarios skill. |

<a id="p-carta-crm"></a>

**carta-crm**（21 Skill）

> Carta CRM 投资人与交易管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/add-contact` | 📋 Skill | Adds one or more contact records to the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a contact", "create a contact record", "add contact to CRM", "save a contact", "upload contact to Carta CRM", or "/add-contact". Collects contact information conversationally, then creates it via the MCP server. Only name is required — all other fields are optional. |
| `/add-note` | 📋 Skill | Adds a comment/note to a deal record in the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a note", "create a note", "log a note", "add note to a deal", "add note to CRM", "add note to Carta CRM", "log a comment on a deal", or "/add-note". Notes are stored as comments on deal records. |
| `/search-notes` | 📋 Skill | Searches for and retrieves note records from the Carta CRM. Use this skill when the user says things like "find a note", "search notes", "look up a note", "show me notes about [topic]", "list notes", "find notes mentioning [keyword]", or "/search-notes". Returns note details including ID, title, and text content. |
| `/update-company` | 📋 Skill | Updates an existing company record in the Carta CRM. Use this skill when the user says things like "update a company", "edit company", "update company details", "change company name", "update company website", "update company fields", "add a tag to company", or "/update-company". Accepts a company ID or name (will search if no ID provided). Only the fields explicitly provided are changed — all other fields are left untouched. |
| `/add-deal` | 📋 Skill | Creates one or more deal records in the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a deal", "create a deal", "log a deal", "add deal to CRM", "add deal to Carta CRM", or "/add-deal". Collects deal information conversationally, then creates it via the MCP server. |
| `/search-contacts` | 📋 Skill | Searches for and retrieves contact (people) records from the Carta CRM. Use this skill when the user says things like "find a contact", "search contacts", "look up a person", "show me contact details for [name]", "get contact by ID", "list contacts", "find people at [company]", "search people", or "/search-contacts". Returns contact details including ID, name, email, title, company, and tags. The contact ID returned can be used with the update-contact skill. |
| `/update-investor` | 📋 Skill | Updates an existing investor record in the Carta CRM. Use this skill when the user says things like "update an investor", "edit investor", "update investor details", "change investor name", "update investor website", "update investor fields", "add a tag to investor", or "/update-investor". Accepts an investor ID or name (will search if no ID provided). Only the fields explicitly provided are changed — all other fields are left untouched. |
| `/update-deal` | 📋 Skill | Updates an existing deal record in the Carta CRM. Use this skill when the user says things like "update a deal", "move deal to [stage]", "change deal stage", "edit deal", "update deal fields", "add a tag to deal", "assign deal lead", "update company info on deal", "link contacts to deal", or "/update-deal". Accepts a deal ID or company name (will search if no ID provided). Only the fields explicitly provided are changed — all other fields are left untouched. |
| `/update-note` | 📋 Skill | Searches for notes in the Carta CRM and helps the user update deal comments. Use this skill when the user says things like "update a note", "edit note", "update note content", "change a note", or "/update-note". Note: standalone note editing is not available via MCP — notes/comments are attached to deals and updated via the update-deal skill. |
| `/update-fundraising` | 📋 Skill | Updates an existing fundraising record in the Carta CRM. Use this skill when the user says things like "update a fundraising", "edit fundraising", "update fundraising details", "change fundraising stage", "update fundraising fields", or "/update-fundraising". Accepts a fundraising ID or name (will search if no ID provided). Only the fields explicitly provided are changed — all other fields are left untouched. |
| `/update-contact` | 📋 Skill | Updates an existing contact (person) record in the Carta CRM. Use this skill when the user says things like "update a contact", "edit contact", "update contact details", "change contact email", "update person's title", "update contact company", "add a tag to contact", or "/update-contact". Accepts a contact ID or name (will search if no ID provided). Only the fields explicitly provided are changed — all other fields are left untouched. |
| `/add-company` | 📋 Skill | Adds one or more company records to the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a company", "create company record", "add company to CRM", "add company to Carta CRM", or "/add-company". Collects company information conversationally, then creates it via the MCP server. |
| `/search-companies` | 📋 Skill | Searches for and retrieves company records from the Carta CRM. Use this skill when the user says things like "find a company", "search companies", "look up a company", "show me company details for [name]", "get company by ID", "get company by domain", "list companies", "what companies do we have", or "/search-companies". Returns company details including ID, name, and custom fields. The company ID returned can be used with the update-company skill. |
| `/lookup-fund-portfolio` | 📋 Skill | Finds and returns the portfolio companies listed on a VC or investment fund's website. Use this skill when the user says things like "look up portfolio of [fund]", "get portfolio companies for [fund website]", "what companies does [fund] invest in", "find portfolio page for [url]", "list investments of [fund]", or "/lookup-fund-portfolio". Input: fund website URL or domain. Output: structured JSON list of portfolio company names. Saves the result locally at ~/.carta-crm/fund-portfolios/ for auditing. |
| `/add-fundraising` | 📋 Skill | Adds one or more fundraising records to the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add a fundraising", "create a fundraising", "log a fundraising round", "add fundraising to CRM", "create fundraising record", or "/add-fundraising". Collects fundraising information conversationally, then creates it via the MCP server. |
| `/tutorial` | 📋 Skill | Interactive ~5-minute walkthrough of the Carta CRM plugin. Covers plugin overview, setup verification, how to kick off each skill, and a demo walkthrough of 4 realistic CRM scenarios. Trigger phrases: "carta crm tutorial", "show me the crm tutorial", "how do I use carta crm", "walk me through carta crm", "getting started with crm", "demo carta crm", "crm tutorial" |
| `/enrich-company` | 📋 Skill | Researches a company by fetching its website and returning structured profile data. Use this skill when the user says things like "enrich this company", "look up company info", "research this company", "what does [domain] do", "get company details for [url]", "find info on [company]", or "/enrich-company". Input: target (domain name or website URL). Output: structured JSON with name, industry, tags, description, and website. Saves the result locally at ~/.carta-crm/enriched-companies/ for auditing. |
| `/add-investor` | 📋 Skill | Adds one or more investor records to the Carta CRM via the Carta CRM MCP Server. Use this skill when the user says things like "add an investor", "/add-investor", "add investor to Carta CRM", "create investor record", "add this VC fund to the CRM", or "save investor data". Collects investor information conversationally, then creates it via the MCP server. |
| `/search-deals` | 📋 Skill | Searches for and retrieves deal records from the Carta CRM. Use this skill when the user says things like "find a deal", "search deals", "look up a deal", "show me deals for [company]", "get deal by ID", "find deal in [stage]", "list deals", "what deals do we have for [company]", or "/search-deals". Returns deal details including ID, company, stage, pipeline, tags, and custom fields. The deal ID returned can be used with the update-deal skill. |
| `/search-fundraisings` | 📋 Skill | Searches for and retrieves fundraising records from the Carta CRM. Use this skill when the user says things like "find a fundraising", "search fundraisings", "look up a fundraising round", "show fundraising details for [name]", "get fundraising by ID", "list fundraisings", "what fundraisings do we have", or "/search-fundraisings". Returns fundraising details including ID, name, stage, and custom fields. The fundraising ID returned can be used with the update-fundraising skill. |
| `/search-investors` | 📋 Skill | Searches for and retrieves investor records from the Carta CRM. Use this skill when the user says things like "find an investor", "search investors", "look up an investor", "show me investor details for [name]", "get investor by ID", "list investors", "what investors do we have", or "/search-investors". Returns investor details including ID, name, and custom fields. The investor ID returned can be used with the update-investor skill. |

<a id="p-carta-investors"></a>

**carta-investors**（14 Skill）

> Carta 投资人数据与业绩分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/carta-co-investors` | 📋 Skill | Interactive co-investor report from Carta SPA data with clickable portfolio drill-downs. Use for co-investor analysis or asking who invested in a specific portfolio company. |
| `/carta-consolidating-balance-sheet` | 📋 Skill | Generate a consolidating Balance Sheet for all entities under a firm for a given month and write it as a side-by-side Excel tab with Assets / Liabilities / Equity sections and a Total column. Sourced from Carta MCP (firm/entity resolution + DWH SQL). TRIGGER when the user asks for "balance sheet of all entities of [firm] for [month]", a consolidating BS by entity, or to replicate the "Balance Sheet - consolidating" tab format for a different firm/period. Trigger phrases include "consolidating balance sheet", "BS by entity", "balance sheet of all entities". DO NOT TRIGGER for single-entity BS, P&L / income statement (carta-consolidating-pnl), new budgets (carta-create-budget), pulling Carta-stored budgets (carta-fetch-budget), refreshing actuals (carta-budget-actuals), pacing (carta-budget-vs-actuals), or what-if (carta-budget-scenarios). |
| `/carta-create-budget` | 📋 Skill | Build or restructure a fund/ManCo budget workbook in Excel from Carta prior-year actuals. TRIGGER: build/create/draft a budget for a future year; group/categorize budget line items into sections with subtotals; apply an inflation/contingency buffer to budget expenses. NOT: consolidating P&L / balance sheet, fetch-budget, actuals refresh, pacing (carta-budget-vs-actuals), what-if scenarios (carta-budget-scenarios). |
| `/carta-performance-benchmarks` | 📋 Skill | Compare a fund's performance against peer benchmark cohorts. Use when asked about fund benchmarks, peer comparison, percentile ranking, Net IRR vs peers, TVPI benchmarks, or how a fund stacks up against its cohort. Do NOT use for cap table market benchmarks (option pool sizes, SAFE terms, cap structure patterns — use carta-market-benchmarks in carta-cap-table). Do NOT use for general fund financial data queries or NAV — use carta-explore-data. |
| `/carta-consolidating-pnl` | 📋 Skill | Firm-wide consolidating P&L (Income Statement) across ALL entities of a firm for one month. Produces TWO Excel tabs: detailed P&L (Month + YTD Actual/Budget/Variance/%) and executive Summary P&L formula-linked to detail. Optional tag-view mode breaks Actuals down by ALL firm reporting-tag categories side by side with a three-row nested header (period > category > tag) and per-category subtotals; Budget/Variance omitted in tag-view (Carta budgets have no tag dimension). Sourced from Carta MCP. TRIGGER on "consolidating P&L for [firm] [month]", "P&L for all entities of [firm]", "firm-wide income statement", "P&L with executive summary", "P&L by department", "P&L by tag", "income statement by cost center", "P&L by project code". DO NOT TRIGGER for single-entity P&L, balance sheet (carta-consolidating-balance-sheet), new budgets (carta-create-budget), Carta budgets (carta-fetch-budget), actuals refresh (carta-budget-actuals), pacing (carta-budget-vs-actuals), or what-if (carta-budget-scenarios). |
| `/carta-investors-tutorial` | 📋 Skill | Interactive 5-minute walkthrough of the carta-investors plugin. Covers plugin overview, setup verification, and demo of 3 real-world scenarios: fundraising benchmarks, LP reporting tear sheets, and LP meeting prep. Trigger with: "investors tutorial", "show me the tutorial", "getting started with investors plugin", "how do I use the investors plugin", "demo", "walk me through the investors plugin", "what can I do with carta", "how does this work". |
| `/carta-soi` | 📋 Skill | Display a fund's Schedule of Investments (SOI) as a Live Artifact in Cowork. The artifact is firm-scoped — it loads every fund the user has access to in the firm and presents them in a header dropdown for one-click switching. Use when asked for the SOI, fund holdings, what a fund is invested in, or a portfolio breakdown. Do NOT use for general fund metrics (NAV, IRR, TVPI, DPI) or ad-hoc warehouse queries — use carta-explore-data instead. |
| `/carta-fetch-budget` | 📋 Skill | Pull a ManCo budget from Carta and write it to an Excel workbook with monthly amounts and subtotals. TRIGGER: pull/fetch/import/sync Carta budget for a ManCo. NOT: pull/fetch/get actuals (carta-budget-actuals), new budgets (carta-create-budget), actuals refresh, pacing, scenarios, P&L, balance sheet. |
| `/carta-budget-vs-actuals` | 📋 Skill | Analyze pacing and variance: compare YTD actuals against a budget workbook (read-only analysis, pulls actuals from Carta MCP). TRIGGER: "how are we doing", pacing, on-track, variance analysis, compare budget vs actuals. NOT: writing/refreshing actuals columns into the workbook (carta-budget-actuals), new budgets (carta-create-budget), fetch-budget, scenarios, consolidating P&L / balance sheet. |
| `/carta-explore-data` | 📋 Skill | Carta Web / Fund Admin investors data queries against the data warehouse. For investments, portfolio companies, fund metrics, NAV, TVPI, DPI, IRR, cash flows, balance sheets, cap tables, ownership %, shareholders, 409a valuations, FMV, MOIC, fund holdings, or what a fund is invested in. Covers funds in Carta Web / Fund Admin only. Carta Fund Forecasting (formerly Tactyc) is a SEPARATE domain with its own funds — for performance metrics of a fund in Fund Forecasting, use carta-fund-forecasting instead. Unless the user has said which system the fund is in, ask whether it's in Carta Web / Fund Admin or Fund Forecasting (Tactyc) before answering a fund-performance question. Prefer over carta-soi for data queries (carta-soi is for Cowork persistent artifacts); over carta-portfolio-valuations for read-only valuation/MOIC/investment data (that skill runs/updates valuation projects); over carta-lp-dashboard unless asked by name; over carta-consolidating-balance-sheet for single-fund balance sheets. |
| `/carta-budget-actuals` | 📋 Skill | Write actuals into an existing Excel budget workbook from Carta MCP — add/interleave Budget/Actual/Variance columns or a tag-view tab. TRIGGER: pull/fetch/get/retrieve/refresh/sync/add actuals for [firm/ManCo], interleave Budget/Actual/Variance, actuals by department/cost center/tag, add next month/period column, extend budget through [month]. NOT: pacing or "how are we doing"/variance-analysis questions (carta-budget-vs-actuals), new budgets (carta-create-budget), fetch-budget, scenarios, consolidating P&L / balance sheet. |
| `/carta-download-tearsheet` | 📋 Skill | Download tear sheets for your portfolio companies and funds on Carta. Use when asked to "create a [portco] tear sheet", "download tear sheet for all portfolio companies", or "preview the tear sheet for [portco]". |
| `/carta-form-adv` | 📋 Skill | Fetches Form ADV Part 1A filing data and generates an interactive HTML filing guide + Excel filing reference. Covers Items 5.D/F/H, Schedule D §7.B.(1) per-fund detail, beneficial owner breakdown, asset class composition, and capital activity. Use when asked about Form ADV, regulatory AUM, Schedule D, Form PF Section 1, SEC filing data, or private fund disclosures. Do NOT use for general fund metrics, NAV lookups, or LP contribution history — use carta-explore-data instead. |
| `/carta-budget-scenarios` | 📋 Skill | Build what-if scenario columns on an existing Excel budget workbook — trim, growth, or additive layers (new fund raise, headcount/FTE hires, expansion). TRIGGER: what-if questions, "how would X affect next year's budget/P&L", model/simulate a scenario, impact of raising a fund or hiring, forward projections with timing sensitivity. NOT: new budgets (carta-create-budget), fetch-budget, actuals refresh, pacing, historical/consolidating financial statements (carta-consolidating-pnl / carta-consolidating-balance-sheet). |

<a id="p-circleback"></a>

**circleback**（🔌 MCP）

> Circleback 会议与邮件上下文集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__circleback` | 🔌 MCP | Circleback conversational context integration. Search and access meetings, emails, calendar events, and more. |
<a id="p-claude-code-setup"></a>

**claude-code-setup**（1 Skill）

> 代码库分析与自动化配置推荐

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/claude-automation-recommender` | 📋 Skill | Analyze a codebase and recommend Claude Code automations (hooks, subagents, skills, plugins, MCP servers). Use when user asks for automation recommendations, wants to optimize their Claude Code setup, mentions improving Claude Code workflows, asks how to first set up Claude Code for a project, or wants to know what Claude Code features they should use. |

<a id="p-claude-md-management"></a>

**claude-md-management**（1 Skill、1 Command）

> CLAUDE.md 文件维护与质量审核

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/claude-md-improver` | 📋 Skill | Audit and improve CLAUDE.md files in repositories. Use when user asks to check, audit, update, improve, or fix CLAUDE.md files. Scans for all CLAUDE.md files, evaluates quality against templates, outputs quality report, then makes targeted updates. Also use when the user mentions "CLAUDE.md maintenance" or "project memory optimization". |
| `/claude-md-management:revise-claude-md` | ⌨️ Command | Update CLAUDE.md with learnings from this session |

<a id="p-code-review"></a>

**code-review**（1 Command） ⚠️ 已被内置 `/code-review` 取代

> 多智能体自动化 PR 代码审查

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/code-review:code-review` | ⌨️ Command | Code review a pull request |

<a id="p-code-simplifier"></a>

**code-simplifier**（1 Agent）

> 自动简化优化代码清晰度

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| code-simplifier | 🤖 Agent | Use this agent when code has been written or modified and needs to be simplified for clarity, consistency, and maintainability while preserving all functionality. This agent should be triggered automatically after completing a coding task or writing a logical chunk of code. It simplifies code by following project best practices while retaining all functionality. The agent focuses only on recently modified code unless instructed otherwise. Examples: <example> Context: The assistant has just implemented a new feature that adds user authentication to an API endpoint. user: "Please add authentication to the /api/users endpoint" assistant: "I've implemented the authentication for the /api/users endpoint. Here's the code:" <function call omitted for brevity> <commentary> Since a logical chunk of code has been written (authentication feature), use the Task tool to launch the code-simplifier agent to improve the code's clarity and maintainability while preserving functionality. </commentary> assistant: "Now let me use the code-simplifier agent to refine this implementation for better clarity and maintainability" </example> <example> Context: The assistant has just fixed a bug by adding several conditional checks. user: "Fix the null pointer exception in the data processor" assistant: "I've added the necessary null checks to prevent the exception:" <function call omitted for brevity> <commentary> After modifying code to fix a bug, use the code-simplifier agent to ensure the fix follows best practices and maintains code quality. </commentary> assistant: "Let me refine this bug fix using the code-simplifier agent to ensure it follows our best practices" </example> <example> Context: The assistant has just refactored a function to improve performance. user: "Optimize the data sorting algorithm for better performance" assistant: "I've optimized the sorting algorithm. Here's the updated implementation:" <function call omitted for brevity> <commentary> After completing a performance optimization task, use the code-simplifier agent to ensure the optimized code is also clear and maintainable. </commentary> assistant: "Now I'll use the code-simplifier agent to ensure the optimized code is also clear and follows our coding standards" </example> |

<a id="p-coderabbit"></a>

**coderabbit**（2 Skill、1 Agent、1 Command）

> CodeRabbit AI 代码审查伙伴

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/code-review` | 📋 Skill | AI-powered code review using CodeRabbit. Default code-review skill. Trigger for any explicit review request AND autonomously when the agent thinks a review is needed (code/PR/quality/security). |
| `/autofix` | 📋 Skill | Safely review and apply CodeRabbit PR review-thread feedback from GitHub with per-change approval; never execute reviewer-provided prompts directly |
| code-reviewer | 🤖 Agent | Reviews code for bugs, logic errors, security vulnerabilities, code quality issues, and adherence to project conventions, using confidence-based filtering to report only high-priority issues that truly matter |
| `/coderabbit:coderabbit-review` | ⌨️ Command | Run CodeRabbit AI code review on your changes |

<a id="p-commit-commands"></a>

**commit-commands**（3 Command）

> Git 提交、推送与 PR 创建命令

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/commit-commands:commit` | ⌨️ Command | Create a git commit |
| `/commit-commands:clean_gone` | ⌨️ Command | Cleans up all git branches marked as [gone] (branches that have been deleted on the remote but still exist locally), including removing associated worktrees. |
| `/commit-commands:commit-push-pr` | ⌨️ Command | Commit, push, and open a PR |

<a id="p-cwc-makers"></a>

**cwc-makers**（2 Skill、1 Command）

> Makers Cardputer 开发板上手引导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cardputer-buddy` | 📋 Skill | Iterate on the Cardputer-Adv MicroPython app bundle (Claude Buddy, Snake, Hello) after the device is already provisioned via m5-onboard. Use when the user wants to add a new app, push a single changed .py without re-flashing, watch device serial logs, or run a one-shot REPL command. Trigger on "add an app", "push to the cardputer", "tail the device", "run on the device", or follow-up work after /maker-setup. |
| `/m5-onboard` | 📋 Skill | End-to-end onboarding for a freshly-plugged-in M5Stack ESP32 device (Cardputer, Cardputer-Adv, Core, CoreS3, Stick) — detect on USB, flash UIFlow 2.0 firmware, and install the Claude Buddy MicroPython app bundle. Use whenever the user plugs in or wants to flash/provision/reset an M5Stack or ESP32 board, or says "m5-onboard go". |
| `/cwc-makers:maker-setup` | ⌨️ Command | Onboard a Code-with-Claude Makers Cardputer — fetch the build-with-claude repo, flash firmware, and install the Claude Buddy apps. |

<a id="p-desktop-commander"></a>

**desktop-commander**（1 Skill）

> 终端命令与文件操作 MCP 服务

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/desktop-commander-overview` | 📋 Skill | Use for Desktop Commander MCP capabilities — persistent shells and REPLs, long-running processes, filesystem beyond the workspace, structured files (.xlsx, .docx, .pdf, images) and large local data files such as CSVs, ripgrep search at scale, SSH, or cross-turn state. |

<a id="p-discord"></a>

**discord**（2 Skill）

> Discord 消息桥接与访问控制

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/configure` | 📋 Skill | Set up the Discord channel — save the bot token and review access policy. Use when the user pastes a Discord bot token, asks to configure Discord, asks "how do I set this up" or "who can reach me," or wants to check channel status. |
| `/access` | 📋 Skill | Manage Discord channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the Discord channel. |

<a id="p-exa"></a>

**exa**（1 Skill）

> Exa AI 网页搜索与深度研究

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/search` | 📋 Skill | Deep research powered by Exa. Use for lead generation, literature reviews, deep dives, competitive analysis, or any query where one search falls short, including phrases like 'research this', 'find everything about', 'find me all', or 'deep dive on'. |

<a id="p-github"></a>

**github**（🔌 MCP）

> GitHub 仓库管理与 PR 操作

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__github` | 🔌 MCP | Official GitHub MCP server for repository management. Create issues, manage pull requests, review code, search repositories, and interact with GitH... |
<a id="p-gitlab"></a>

**gitlab**（🔌 MCP）

> GitLab DevOps 平台集成管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__gitlab` | 🔌 MCP | GitLab DevOps platform integration. Manage repositories, merge requests, CI/CD pipelines, issues, and wikis. Full access to GitLab's comprehensive ... |
<a id="p-hookify"></a>

**hookify**（1 Skill、1 Agent、4 Command）

> 创建自定义 Hook 防止不期望行为

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/writing-hookify-rules` | 📋 Skill | This skill should be used when the user asks to "create a hookify rule", "write a hook rule", "configure hookify", "add a hookify rule", or needs guidance on hookify rule syntax and patterns. |
| conversation-analyzer | 🤖 Agent | Use this agent when analyzing conversation transcripts to find behaviors worth preventing with hooks. Typical triggers include the /hookify command being invoked without arguments, or the user explicitly asking to look back at the current conversation and surface mistakes that should be prevented in the future. See "When to invoke" in the agent body for worked scenarios. |
| `/hookify:help` | ⌨️ Command | Get help with the hookify plugin |
| `/hookify:list` | ⌨️ Command | List all configured hookify rules |
| `/hookify:configure` | ⌨️ Command | Enable or disable hookify rules interactively |
| `/hookify:hookify` | ⌨️ Command | Create hooks to prevent unwanted behaviors from conversation analysis or explicit instructions |

<a id="p-hunter"></a>

**hunter**（9 Skill）

> Hunter 专业邮箱查找与验证

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/email-verifier` | 📋 Skill | Verifies whether an email address is deliverable by checking DNS and SMTP records. Use when the user wants to check if an email is valid, verify an email address, or assess deliverability before sending. |
| `/campaign-setup` | 📋 Skill | Prepares an email campaign by adding recipients from your leads. Use when the user wants to set up a campaign, add recipients to a campaign, or prepare for outreach. |
| `/company-enrichment` | 📋 Skill | Retrieves detailed company information including industry, size, location, and description from a domain name. Use when the user asks about a company, wants company details, or says "tell me about [company]". |
| `/list-builder` | 📋 Skill | Creates and populates a Hunter leads list from a set of contacts or domains. Use when the user wants to build a lead list, organize contacts into a list, or save search results to Hunter. |
| `/person-enrichment` | 📋 Skill | Retrieves detailed information about a person from their email address, including name, position, company, and social profiles. Use when the user asks about a person, wants to enrich a contact, or needs more details about someone whose email they have. |
| `/domain-search` | 📋 Skill | Finds all publicly available email addresses and contacts at a company domain. Use when the user asks who works at a company, wants to find contacts at a domain, or needs email addresses for an organization. |
| `/discover` | 📋 Skill | Searches for companies matching specific criteria like industry, size, location, and technologies. Use when the user wants to find companies, build a target list, or search for businesses in a market segment. This is a free operation that does not consume credits. |
| `/prospecting` | 📋 Skill | Runs end-to-end B2B prospecting by chaining company discovery, contact search, email verification, and enrichment. Use when the user wants to build a prospect list, find and qualify leads, or run a full prospecting pipeline. |
| `/email-finder` | 📋 Skill | Finds a professional email address from a person's name and company domain. Use when the user asks to find someone's email, look up a contact's email address, or needs to reach a specific person at a company. |

<a id="p-imessage"></a>

**imessage**（2 Skill）

> iMessage 消息桥接与访问控制

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/configure` | 📋 Skill | Set up the Discord channel — save the bot token and review access policy. Use when the user pastes a Discord bot token, asks to configure Discord, asks "how do I set this up" or "who can reach me," or wants to check channel status. |
| `/access` | 📋 Skill | Manage Discord channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the Discord channel. |

<a id="p-intercom"></a>

**intercom**（4 Skill）

> Intercom 客户支持对话分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/intercom-analysis` | 📋 Skill | Analyze Intercom conversations to identify support patterns, investigate customer issues, and look up contacts and companies. Use when the user asks to "analyze conversations", "find support patterns", "search Intercom", "look up a customer", "investigate a customer issue", "check contact info", or asks questions about their Intercom data. |
| `/install-cli` | 📋 Skill | Install and authenticate the Intercom CLI (`@intercom/cli`) — a command-line tool for managing Intercom workspaces, designed for both human operators and AI agents. Use when the user asks to "install the Intercom CLI", "set up the intercom command", "install @intercom/cli", or wants shell access to their Intercom workspace. |
| `/install-messenger` | 📋 Skill | Install the Intercom Messenger on a website or web application with secure JWT-based identity verification. Generates backend and frontend code for React, Next.js, Vue.js, Angular, Ember, and plain JavaScript. Supports Node.js, Python (Flask/Django), PHP, and Ruby backends. Use when the user asks to "install Intercom", "add the Intercom Messenger", "set up Intercom chat widget", "add customer chat to my website", or "integrate Intercom". |
| `/customer-360` | 📋 Skill | Build a comprehensive customer profile from Intercom data, including conversation history, account context, and interaction timeline. Use when the user asks to "look up a customer", "customer profile", "customer 360", "tell me about this customer", "summarize a customer's history", or provides a customer email or company name and wants a full picture. |

<a id="p-legalzoom"></a>

**legalzoom**（1 Skill、1 Command）

> LegalZoom 法务指导与文档工具

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/attorney-assist` | 📋 Skill | Connects the user with a LegalZoom attorney for legal consultation. Use when a user asks about attorneys, lawyers, or legal help, or when contract review reveals high risks or low-confidence findings. |
| `/legalzoom:review-contract` | ⌨️ Command | In-depth contract analysis with risk assessment and attorney review recommendations |

<a id="p-linear"></a>

**linear**（🔌 MCP）

> Linear 事务跟踪与项目管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__linear` | 🔌 MCP | Linear issue tracking integration. Create issues, manage projects, update statuses, search across workspaces, and streamline your software developm... |
<a id="p-lusha"></a>

**lusha**（4 Skill）

> Lusha B2B 销售线索挖掘与丰富

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/signal-prospect` | 📋 Skill | Find companies or contacts triggered by a buying signal, then surface verified phone numbers for the right decision makers. Use when the user says "find companies that just raised funding", "who's surging in sales hiring right now", "show me companies with headcount growth", "find contacts who just got promoted", "who changed jobs recently in [industry]", "show me [title] at companies that just [signal event]", or any request that starts with a real-world trigger rather than a static filter. |
| `/enrich-contact` | 📋 Skill | Look up a person and get their verified phone numbers, email, and company context. Use when the user says "look up [name]", "get me the contact info for [person]", "find [name]'s phone number", "who is [name] at [company]", "enrich [email or name]", or any request to retrieve a single person's contact details. |
| `/prospect` | 📋 Skill | Build a targeted list of contacts or companies from Lusha and return verified phone numbers alongside emails. Use when the user says "find me [title] at [company type]", "build a list of [ICP description]", "prospect [criteria]", "who should I be calling at [industry]", or any request to generate a lead list from an ICP or persona description. |
| `/lookalike-prospect` | 📋 Skill | Find companies or contacts similar to a set of references, then enrich results with verified phone numbers. Use when the user says "find companies like my best customers", "find more contacts like these", "expand from these accounts", "who else looks like [company]", "find similar companies to [list]", or any request to discover lookalike targets from a reference set. Requires at least 5 reference companies or contacts for quality results. |

<a id="p-notion"></a>

**notion**（6 Command）

> Notion 工作空间集成与管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/notion:create-page` | ⌨️ Command | Create a new Notion page, optionally under a specific parent, using the Notion Workspace Skill and Notion MCP server. |
| `/notion:search` | ⌨️ Command | Search the user’s Notion workspace using the Notion MCP server and Notion Workspace Skill. |
| `/notion:find` | ⌨️ Command | Quickly find pages or databases in Notion by title keywords. |
| `/notion:create-task` | ⌨️ Command | Create a new task in the user’s Notion tasks database with sensible defaults. |
| `/notion:create-database-row` | ⌨️ Command | Insert a new row into a specified Notion database using natural-language property values. |
| `/notion:database-query` | ⌨️ Command | Query a Notion database by name or ID and return structured, readable results. |

<a id="p-pigment"></a>

**pigment**（10 Skill）

> Pigment 业务数据分析与建模

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/creating-and-editing-pigment-views` | 📋 Skill | Always use this skill when creating or editing Views, or needing to pick a View. |
| `/analyzing-pigment-data` | 📋 Skill | Always use this skill when querying, exploring, or analyzing existing data in a Pigment workspace. Covers the analysis workflow, query formulation, data concepts, analysis patterns, ambiguity handling, and result interpretation. |
| `/designing-pigment-boards` | 📋 Skill | Always use when creating or editing a Board. This skill includes supporting files in this directory - explore as needed. |
| `/solving-specific-use-cases` | 📋 Skill | Always use this skill when building or extending models for specific planning domains — FP&A, Workforce Planning, Sales Performance Management, Supply Chain Planning, or Financial Consolidation. Covers proven modeling patterns and domain-specific best practices. This skill includes supporting files in this directory - explore as needed. |
| `/securing-pigment-applications` | 📋 Skill | Always use this skill when designing, applying, or debugging Access Rights and security in Pigment applications. Provides the AR mental model (User, Role, dimension axis, AR Metric, Apply rule), the canonical decision order, mandatory formula patterns (IFDEFINED guard, BLANK over FALSE), multi-app AR, debugging "why can this user see / not see this data?", and security governance. AR is part of model architecture, not an afterthought. |
| `/modeling-pigment-applications` | 📋 Skill | Always use this skill when designing or modifying Pigment applications. Provides the mental model of a Pigment app (Application, Dimensions, Calendars, Metrics, Transaction Lists, Tables), the core concepts (dimension list vs property vs transaction list, metric vs table, sparsity, scope), the canonical order of architecture decisions, a minimal viable application pattern and pointers to deeper-dive docs (architecture, naming, hierarchies, calendars, principles, folders, subsets, performance). |
| `/integrating-external-data` | 📋 Skill | Always use this skill when creating new lists to import CSV data into, importing CSV files into Pigment, mapping CSV columns to properties, deciding whether to import into dimensions vs transaction lists, configuring cross-application imports, troubleshooting data import issues, or importing excel files. This skill includes supporting files in this directory - explore as needed. |
| `/writing-pigment-formulas` | 📋 Skill | Always use this skill when writing, editing, or debugging Pigment formulas — including conditional logic, blank handling, date-range logic, aggregation, prior-period lookups, and dimensional transformations. Pigment uses a proprietary formula language — NEVER assume you know the syntax, and ALWAYS read the documentation before writing any formula. Covers data types, modifiers, functions, calculation patterns, and performance trade-offs (calibrated by formula complexity). This skill includes supporting files in this directory; explore as needed. |
| `/optimizing-pigment-performance` | 📋 Skill | Always use this skill when troubleshooting slow calculations or timeouts, analyzing profiler output to identify bottlenecks, understanding scope propagation, managing sparsity, optimizing formula performance, improving iterative calculations, optimizing access rights performance, conducting systematic performance audits, auditing a Pigment application (modeling, formula hygiene, folders, boards, governance), cleaning unused dimensions, metrics, tables, properties, or boards, identifying dead or stale boards, or removing unused metrics. Modeler-agent skill for Performance Insights tools (performance_profile_change, get_top_blocks_by_performance), then classify and fix. Provides the optimization loop, audit vs cleaning modes, and routing to deep dives. Always profile before formula changes; never optimize from assumptions. |
| `/planning-cycles-pigment-applications` | 📋 Skill | Always use this skill when the user mentions or implies versions, Actual, Actuals, Budget, Budgeting, Forecast, Reforecast, Rolling Forecast, Version, Versioning, Plan, switchover, scenarios, snapshots, planning cycles, Actual/Plan layering, plan vs actual, "create version dimension", "set up versioning", or asks for Actual Budget Forecast best practices — or when they extend realized data into a plan or budget (Actual/Budget/Plan layering, forward forecast from actuals) or need to combine or compare actual and plan versions and periods. Covers Version Dimensions (foundational to all planning applications), Native Scenarios (what-if), and Snapshots (freeze data). |

<a id="p-pr-review-toolkit"></a>

**pr-review-toolkit**（6 Agent、1 Command）

> 全方位 PR 审查（评论测试安全等）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| silent-failure-hunter | 🤖 Agent | Use this agent when reviewing code changes in a pull request to identify silent failures, inadequate error handling, and inappropriate fallback behavior. This agent should be invoked proactively after completing a logical chunk of work that involves error handling, catch blocks, fallback logic, or any code that could potentially suppress errors. Examples:\n\n<example>\nContext: Daisy has just finished implementing a new feature that fetches data from an API with fallback behavior.\nDaisy: "I've added error handling to the API client. Can you review it?"\nAssistant: "Let me use the silent-failure-hunter agent to thoroughly examine the error handling in your changes."\n<Task tool invocation to launch silent-failure-hunter agent>\n</example>\n\n<example>\nContext: Daisy has created a PR with changes that include try-catch blocks.\nDaisy: "Please review PR #1234"\nAssistant: "I'll use the silent-failure-hunter agent to check for any silent failures or inadequate error handling in this PR."\n<Task tool invocation to launch silent-failure-hunter agent>\n</example>\n\n<example>\nContext: Daisy has just refactored error handling code.\nDaisy: "I've updated the error handling in the authentication module"\nAssistant: "Let me proactively use the silent-failure-hunter agent to ensure the error handling changes don't introduce silent failures."\n<Task tool invocation to launch silent-failure-hunter agent>\n</example> |
| code-simplifier | 🤖 Agent | Use this agent when code has been written or modified and needs to be simplified for clarity, consistency, and maintainability while preserving all functionality. This agent should be triggered automatically after completing a coding task or writing a logical chunk of code. It simplifies code by following project best practices while retaining all functionality. The agent focuses only on recently modified code unless instructed otherwise. Examples: <example> Context: The assistant has just implemented a new feature that adds user authentication to an API endpoint. user: "Please add authentication to the /api/users endpoint" assistant: "I've implemented the authentication for the /api/users endpoint. Here's the code:" <function call omitted for brevity> <commentary> Since a logical chunk of code has been written (authentication feature), use the Task tool to launch the code-simplifier agent to improve the code's clarity and maintainability while preserving functionality. </commentary> assistant: "Now let me use the code-simplifier agent to refine this implementation for better clarity and maintainability" </example> <example> Context: The assistant has just fixed a bug by adding several conditional checks. user: "Fix the null pointer exception in the data processor" assistant: "I've added the necessary null checks to prevent the exception:" <function call omitted for brevity> <commentary> After modifying code to fix a bug, use the code-simplifier agent to ensure the fix follows best practices and maintains code quality. </commentary> assistant: "Let me refine this bug fix using the code-simplifier agent to ensure it follows our best practices" </example> <example> Context: The assistant has just refactored a function to improve performance. user: "Optimize the data sorting algorithm for better performance" assistant: "I've optimized the sorting algorithm. Here's the updated implementation:" <function call omitted for brevity> <commentary> After completing a performance optimization task, use the code-simplifier agent to ensure the optimized code is also clear and maintainable. </commentary> assistant: "Now I'll use the code-simplifier agent to ensure the optimized code is also clear and follows our coding standards" </example> |
| type-design-analyzer | 🤖 Agent | Use this agent when you need expert analysis of type design in your codebase. Specifically use it (1) when introducing a new type to ensure it follows best practices for encapsulation and invariant expression, (2) during pull request creation to review all types being added, and (3) when refactoring existing types to improve their design quality. The agent will provide both qualitative feedback and quantitative ratings on encapsulation, invariant expression, usefulness, and enforcement. See "When to invoke" in the agent body for worked scenarios. |
| code-reviewer | 🤖 Agent | Reviews code for bugs, logic errors, security vulnerabilities, code quality issues, and adherence to project conventions, using confidence-based filtering to report only high-priority issues that truly matter |
| comment-analyzer | 🤖 Agent | Use this agent when you need to analyze code comments for accuracy, completeness, and long-term maintainability. This includes (1) after generating large documentation comments or docstrings, (2) before finalizing a pull request that adds or modifies comments, (3) when reviewing existing comments for potential technical debt or comment rot, and (4) when you need to verify that comments accurately reflect the code they describe. See "When to invoke" in the agent body for worked scenarios. |
| pr-test-analyzer | 🤖 Agent | Use this agent when you need to review a pull request for test coverage quality and completeness. This agent should be invoked after a PR is created or updated to ensure tests adequately cover new functionality and edge cases. Typical triggers include the user asking whether tests on a freshly-created PR are thorough, an updated PR adding new logic that needs coverage analysis, and a final pre-merge double-check before marking a PR ready. See "When to invoke" in the agent body for worked scenarios. |
| `/pr-review-toolkit:review-pr` | ⌨️ Command | Comprehensive PR review using specialized agents |

<a id="p-save-to-spotify"></a>

**save-to-spotify**（1 Skill）

> 创建音频节目并保存到 Spotify

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/save-to-spotify` | 📋 Skill | Create polished audio content and save to Spotify. Produces episodes with TTS narration, a rich timeline (chapters plus in-player images, external links, and Spotify entity cards), and a cover image. Also use for raw media saves, show/episode management, and timeline navigation. |

<a id="p-session-report"></a>

**session-report**（1 Skill）

> Claude Code 会话用量 HTML 报告

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/session-report` | 📋 Skill | Generate an explorable HTML report of Claude Code session usage (tokens, cache, subagents, skills, expensive prompts) from ~/.claude/projects transcripts. |

<a id="p-slack"></a>

**slack**（2 Skill、5 Command）

> Slack 消息搜索与频道管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/slack:slack-messaging` | 📋 Skill | Guidance for composing well-formatted, effective Slack messages using standard markdown |
| `/slack:slack-search` | 📋 Skill | Guidance for effectively searching Slack to find messages, files, channels, and people |
| `/slack:standup` | ⌨️ Command | Generate a standup update based on your recent Slack activity |
| `/slack:find-discussions` | ⌨️ Command | Find discussions about a specific topic across Slack channels |
| `/slack:channel-digest` | ⌨️ Command | Get a digest of recent activity across multiple Slack channels |
| `/slack:draft-announcement` | ⌨️ Command | Draft a well-formatted Slack announcement and save it as a draft |
| `/slack:summarize-channel` | ⌨️ Command | Summarize recent activity in a Slack channel |

<a id="p-spotify-ads-api"></a>

**spotify-ads-api**（13 Skill、1 Agent）

> Spotify 广告活动自然语言管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/build-campaign` | 📋 Skill | Create a full campaign (campaign + ad sets + ads) from a plain-text description. Parses natural language into structured API calls. |
| `/bulk` | 📋 Skill | Apply batch operations to multiple Spotify Ads API entities — pause or resume ad sets, update budgets, toggle ad delivery, swap creatives, or archive campaigns, ad sets, and ads. |
| `/export` | 📋 Skill | Export Spotify Ads API campaign data to CSV — full campaign hierarchies with ad sets, ads, targeting, budgets, and performance metrics for offline review, campaign analysis, or budget reconciliation. |
| `/clone` | 📋 Skill | Clone an existing Spotify Ads API campaign or ad set — duplicate the full hierarchy (campaign, ad sets, ads) with optional modifications to name, dates, budget, or targeting. |
| `/ads` | 📋 Skill | Manage Spotify Ads API ad sets and ads — list, create, get, or update. |
| `/campaign-strategy` | 📋 Skill | Generate Spotify Ads campaign strategy from a landing page, product or business page, brand brief, location page, uploaded creative assets, existing Spotify Ads assets, or a natural-language business goal. Use when the user asks for the best campaign structure, targeting plan, audience plan, budget split, creative rotation, API-ready campaign plan, or pre-build recommendations before creating Spotify campaigns. |
| `/monitor` | 📋 Skill | Check Spotify Ads API campaign health — pacing, delivery issues, budget burn rate, stalled campaigns, and underpacing alerts. Use for one-shot health checks or recurring monitoring when the host supports scheduled automations. |
| `/campaigns` | 📋 Skill | List, create, get, or update Spotify Ads API campaigns. |
| `/Spotify Ads API Reference` | 📋 Skill | This skill should be used when the user asks to "call the Spotify Ads API", "create a Spotify ad campaign", "manage Spotify ads", "pull Spotify ad reports", "set up ad sets or ads", "upload ad assets", "target audiences on Spotify", "check campaign status", "get ad account info", "look up API schema or fields", "check what targeting options exist", or asks about Spotify advertising endpoints, request/response formats, enum values, or authentication. |
| `/report` | 📋 Skill | Pull Spotify Ads API reporting data — aggregate metrics, audience insights, or async CSV reports. |
| `/configure` | 📋 Skill | Configure Spotify Ads API credentials via OAuth 2.0 or direct token. Sets up authentication, ad account, and execution preferences. |
| `/dashboard` | 📋 Skill | Quick performance overview of all active Spotify ad campaigns — impressions, spend, reach, clicks, and pacing at a glance. |
| `/assets` | 📋 Skill | Upload, list, and manage Spotify Ads API creative assets — audio, video, and images for ad campaigns. |
| spotify-ads-request-builder | 🤖 Agent | Use this agent when the user describes an advertising task in natural language and needs it translated into Spotify Ads API calls. |

<a id="p-telegram"></a>

**telegram**（2 Skill）

> Telegram 消息桥接与访问控制

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/configure` | 📋 Skill | Set up the Discord channel — save the bot token and review access policy. Use when the user pastes a Discord bot token, asks to configure Discord, asks "how do I set this up" or "who can reach me," or wants to check channel status. |
| `/access` | 📋 Skill | Manage Discord channel access — approve pairings, edit allowlists, set DM/group policy. Use when the user asks to pair, approve someone, check who's allowed, or change policy for the Discord channel. |

<a id="p-vibe-prospecting"></a>

**vibe-prospecting**（1 Skill）

> Vibe 实时 B2B 公司与联系人数据

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/vibe-prospecting` | 📋 Skill | Find company & contact data. Turn your agent into a prospecting platform. Get contact information, roles, tech stack, business events, website changes, intent data. Build lead lists, research prospects, identify talent. 150M+ companies, 800M+ professionals, 50+ data sources. |

<a id="p-windsor-ai"></a>

**windsor-ai**（1 Skill、1 Agent、3 Command）

> Windsor 连接 325+ 数据源查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/windsor-ai:business-data` | 📋 Skill | disable-model-invocation: false |
| business-data-analyst | 🤖 Agent | Pull, transform, and integrate business data from Windsor.ai's 325+ connectors |
| `/windsor-types` | ⌨️ Command | Generate TypeScript type definitions for a Windsor.ai connector's data schema |
| `/campaign-report` | ⌨️ Command | Generate a quick campaign performance report from any connected data source |
| `/windsor-sources` | ⌨️ Command | Show all connected data sources and what data is available from each |

<a id="p-youdotcom-agent-skills"></a>

**youdotcom-agent-skills**（8 Skill）

> You.com 网页搜索与研究技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ydc-openai-agent-sdk-integration` | 📋 Skill | Integrate OpenAI Agents SDK with You.com MCP server - Hosted and Streamable HTTP support for Python and TypeScript. - MANDATORY TRIGGERS: OpenAI Agents SDK, OpenAI agents, openai-agents, @openai/agents, integrating OpenAI with MCP - Use when: developer mentions OpenAI Agents SDK, needs MCP integration with OpenAI agents |
| `/ydc-ai-sdk-integration` | 📋 Skill | Integrate Vercel AI SDK applications with You.com tools (web search, AI agent, content extraction). Use when developer mentions AI SDK, Vercel AI SDK, generateText, streamText, or You.com integration with AI SDK. |
| `/ydc-crewai-mcp-integration` | 📋 Skill | Integrate You.com remote MCP server with crewAI agents for web search, AI-powered answers, and content extraction. - MANDATORY TRIGGERS: crewAI MCP, crewai mcp integration, remote MCP servers, You.com with crewAI, MCPServerHTTP, MCPServerAdapter - Use when: developer mentions crewAI MCP integration, needs remote MCP servers, integrating You.com with crewAI |
| `/ydc-claude-agent-sdk-integration` | 📋 Skill | Integrate Claude Agent SDK with You.com HTTP MCP server for Python and TypeScript. Use when developer mentions Claude Agent SDK, Anthropic Agent SDK, or integrating Claude with MCP tools. |
| `/youdotcom-cli` | 📋 Skill | Web search, research with citations, and content extraction for bash agents using curl and You.com's REST API. - MANDATORY TRIGGERS: You.com, youdotcom, YDC, web search CLI, livecrawl, you.com API, research with citations, content extraction, fetch web page - Use when: web search needed, content extraction, URL crawling, real-time web data, research with citations |
| `/ydc-langchain-integration` | 📋 Skill | Integrate LangChain applications with You.com tools (web search, content extraction, retrieval) in TypeScript or Python. Use when developer mentions LangChain, LangChain.js, LangChain Python, createAgent, initChatModel, DynamicStructuredTool, langchain-youdotcom, YouRetriever, YouSearchTool, YouContentsTool, or You.com integration with LangChain. |
| `/youdotcom-api` | 📋 Skill | Integrate You.com APIs (Research, Search, Contents) into any language using direct HTTP calls — no SDK required. - MANDATORY TRIGGERS: YDC API, You.com API integration, ydc-api, direct API integration, no SDK, Research API, youdotcom API, you.com REST API - Use when: developer wants to call You.com APIs directly without an SDK wrapper |
| `/teams-anthropic-integration` | 📋 Skill | Add Anthropic Claude models (Opus, Sonnet, Haiku) to Microsoft Teams.ai applications using @youdotcom-oss/teams-anthropic. Optionally integrate You.com MCP server for web search and content extraction. - MANDATORY TRIGGERS: teams-anthropic, @youdotcom-oss/teams-anthropic, Microsoft Teams.ai, Teams AI, Anthropic Claude, Teams MCP, Teams bot - Use when: building Microsoft Teams bots with Claude, integrating Anthropic with Teams.ai, adding MCP tools to Teams applications |

<a id="p-zapier"></a>

**zapier**（3 Skill、1 Agent）

> 连接 8000+ 应用自动化工作流

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/create-my-tools-profile` | 📋 Skill | Generate a personalized AI skill based on your configured Zapier MCP tools. Scans your enabled actions and creates instructions that help your AI assistant know when and how to use each tool. Use after setting up tools, or when you want to "create my tools profile", "personalize my assistant", or "make a skill from my tools". |
| `/zapier-status` | 📋 Skill | Check the health of your Zapier MCP setup. Three modes — health check (dashboard view), audit (find waste and duplicates), diagnose (systematic troubleshooting). Use when asking "is my MCP working?", "check my tools", "audit my setup", "what's broken?", or "zapier status". |
| `/zapier-setup` | 📋 Skill | Set up Zapier MCP and add tools to your AI assistant. Introduces what Zapier can do, walks through authentication, detects your server mode, then branches into the right flow — summary for healthy setups, reconnect for broken auth, onboarding for fresh installs, or config help when the server is missing. Use when getting started, troubleshooting connection issues, adding new tools, or when the user asks "what can I do now", "what can I do with Zapier", "show me how the Zapier plugin works", "what is Zapier MCP", "how does Zapier work", or "tell me about Zapier". |
| zapier-mcp.agent | 🤖 Agent | - |

<a id="p-zoominfo"></a>

**zoominfo**（14 Skill）

> ZoomInfo B2B 公司联系人数据查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/meeting-prep` | 📋 Skill | Prepare for an upcoming meeting with a company. Identify the account by ZoomInfo account/company ID (preferred) or by company name, domain, or ticker (which triggers a lookup step). Provide attendee names or emails and rich context on the meeting purpose, stakes, and known dynamics to get a tight, decision-ready brief — headline, relationship posture per attendee, ranked talking points, discovery questions, suggested agenda, and what NOT to do. Optimized for a 30-min slot. |
| `/competitor-analysis` | 📋 Skill | Produce a fact-led competitive intel brief on one or more competitors — firmographics, recent strategic moves, product positioning, ICP overlap, and discovery questions. Defaults to your configured competitors from GTM context if none specified. Combines ZoomInfo data (account_research, scoops, intent, exec teams, similar companies) with web search for product/pricing/customer-sentiment intelligence. Identify competitors by ZoomInfo account/company ID (preferred) or name; include rich context on why the brief is being pulled and what decision it supports. |
| `/enrich-contact` | 📋 Skill | Look up a person's full professional profile. Provide a name and company, email address, phone number, or ZoomInfo person ID. Returns title, department, contact details, accuracy score, and company info. |
| `/enrich-company` | 📋 Skill | Look up a company's full profile. Provide a company name, domain, ticker symbol, or ZoomInfo company ID. Returns firmographics, financials, corporate structure, growth signals, and contact counts. |
| `/tam-sizer` | 📋 Skill | Size the total addressable market (TAM) for an Ideal Customer Profile (ICP) using ZoomInfo's verified company database. Iteratively refine the firmographic and technographic filter set with the user until the account universe matches their intent — then return both the count and the working filter set that other skills (build-list, score-accounts) can consume. Use for territory and capacity design, investor-ready market sizing, and ICP sharpening. Triggers on phrases like "size the market", "TAM for", "addressable market", "how many companies match", "is my ICP too broad/narrow", "refine my ICP filters". |
| `/account-research` | 📋 Skill | Produce a full intelligence brief on a target company — firmographics, CRM/account context, intent signals, recent news, scoops, and competitive landscape — framed by your GTM context and led with a TL;DR summary. Identify the account by ZoomInfo account/company ID (preferred) or by company name, domain, or ticker (which triggers a lookup step). Include detailed context on why the brief is being pulled. |
| `/personalize-email` | 📋 Skill | Generate 1-3 personalized email variants for a single prospect. The composition bar adapts to the use case — cold_outbound demands a signal → pain → positioning chain; follow-ups / recaps / renewals lean on prior context and next-step framing. Supports cold_outbound, discovery_follow_up, demo_recap, re_engagement, renewal, expansion, objection_handling. Returns subject lines and mobile-readable bodies with a rationale chain. Use for sales prospecting, lead generation, account-based selling, buyer-intent-driven outreach, B2B prospecting. Triggers on phrases like "write a cold email", "personalize an email", "draft outreach", "follow up on this prospect", "email this prospect", "outbound to X", "send a chaser". |
| `/score-leads` | 📋 Skill | Score and prioritize leads or cold contacts (mixed ZoomInfo person IDs, emails, or name+company rows). Returns Hot / Warm / Cold tier per lead with a response-time SLA tuned to the use case (live inbound routing, MQL triage, event follow-up, PQL triage, content follow-up, SDR queue ordering), per-axis breakdown (person fit · account fit · source signal · trigger), a "why now" reasoning snippet per lead, and recommended next action with verified contact data. Resolution by email is deterministic; name+company surfaces verification when needed; typo'd emails fail explicitly rather than fall back. Iteratively refinable. Triggers on phrases like "score these leads", "which lead/contact should I call first", "prioritize my MQLs", "rank inbound", "who should I prioritize?", "tier this list". |
| `/tech-stack-snapshot` | 📋 Skill | Produce a technology-stack snapshot for one or more companies — what CRM, marketing automation, sales engagement, data warehouse, analytics, conversation intelligence, and other tools they have tagged in ZoomInfo's database. Groups detected products by category, surfaces displacement plays for competitive tools, integration angles for partner tools, and coverage gaps honestly. Resolves mixed-identifier inputs (IDs / names / domains) with explicit ambiguity surfacing. Useful for sales prospecting, account-based selling, competitive battle-card prep, integration partner research, technographic signal analysis, B2B prospecting. Triggers on phrases like "what tech does X use", "tech stack for", "technographic snapshot", "what's in their stack", "do they use Salesforce", "competitive displacement angle". |
| `/find-similar` | 📋 Skill | Find companies or contacts similar to a given reference. Provide a company name/domain or a person's name/email and get a ranked list of lookalikes scored by similarity. Useful for territory expansion, TAM analysis, competitive mapping, expanding buyer networks, and building targeted prospecting lists. |
| `/build-list` | 📋 Skill | Build a list of contacts or companies matching specific criteria. Describe what you're looking for in natural language and get a structured, tabular list you can export. Supports filtering by title, seniority, department, industry, company size, location, tech stack, growth rate, and more. Outputs a clean table artifact. |
| `/recommend-contacts` | 📋 Skill | Get AI-powered contact recommendations at a target company based on your ZoomInfo interaction history. Provide a company name or domain and optionally a use case. |
| `/buying-committee` | 📋 Skill | Map the buying committee at a target account. Identifies decision-makers, prioritizes who to engage, and surfaces gaps and multi-thread risks. Leads with a TL;DR (top 3 to engage, biggest gap, multi-thread risk), uses compact tables, and deep-researches top stakeholders to catch stale records. Identify the account by ZoomInfo account/company ID (preferred) or by company name, domain, or ticker (which triggers a lookup step). Include detailed context on the deal, situation, and persona priorities driving the map. |
| `/score-accounts` | 📋 Skill | Score and rank a list of accounts (mixed ZoomInfo company IDs, names, or domains) by ICP fit + buying intent + recent triggers. Returns per-account composite score (0–100), tier (A/B/C), explainable component breakdown (fit / intent / trigger / engagement), a specific "why now" sentence per account, and the working weight set as a saveable search filter set. Resolves name/domain inputs via search_companies with explicit confirmation for ambiguous matches. Iteratively refinable — adjust weights, swap axes, retier, or drill into a specific account. Use for account-based selling, ABM list prioritization, territory planning, sales prospecting prioritization, signal-based selling, buyer intent ranking, B2B prospecting. Triggers on phrases like "score these accounts", "prioritize this list", "rank by ICP fit and intent", "which accounts should I work first", "build a tiered account list". |


## 🗄️ Database（31 个插件）

<a id="p-alloydb"></a>

**alloydb**（7 Skill）

> AlloyDB PostgreSQL 数据库连接管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/alloydb-postgres-optimize` | 📋 Skill | Use these skills when you need to discover and manage PostgreSQL extensions or fine-tune engine-level settings such as memory allocation and server configuration parameters. |
| `/alloydb-postgres-replication` | 📋 Skill | Use these skills when you need to monitor replication health, manage sync states between nodes, and ensure the high availability and data distribution of your AlloyDB cluster. |
| `/alloydb-postgres-data` | 📋 Skill | Use these skills when you need to explore the database schema, identify objects like views and triggers, and execute custom SQL queries to interact with your data. |
| `/alloydb-postgres-health` | 📋 Skill | Use these skills when you need to optimize storage, identify index issues, analyze table statistics, or manage autovacuum and tablespace configurations to maintain peak database health. |
| `/alloydb-postgres-admin` | 📋 Skill | Use these skills when you need to provision new AlloyDB clusters and instances, monitor their creation status, and retrieve high-level configuration or health data for the environment. |
| `/alloydb-postgres-access-management` | 📋 Skill | Use these skills when you need to manage database users, inspect permissions and roles, and verify global configuration parameters related to security and access control. |
| `/alloydb-postgres-monitor` | 📋 Skill | Use these skills when you need to troubleshoot slow performance, analyze query execution plans, identify resource-heavy processes, and monitor system-level PromQL metrics. |

<a id="p-alloydb-omni"></a>

**alloydb-omni**（9 Skill）

> AlloyDB Omni 数据库连接管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/alloydb-omni-monitor` | 📋 Skill | Use these skills when you need to troubleshoot production issues by identifying locks, tracking long-running transactions, and getting a high-level view of server state. |
| `/alloydb-omni-kubernetes` | 📋 Skill | You're an expert in AlloyDB Omni Operator running in Kubernetes. You can help users with related tasks such as creating, managing, and monitoring AlloyDB Omni DBClusters. |
| `/alloydb-omni-access-control` | 📋 Skill | Use these skills when you need to manage user roles, inspect permissions, and verify security-related configuration parameters. |
| `/alloydb-omni-health` | 📋 Skill | Use these skills when you need to audit database health, identify storage bloat, find broken indexes, and verify tablespace or maintenance configurations. |
| `/alloydb-omni-data` | 📋 Skill | Use these skills when you need to explore the database structure, identify schema objects like views and triggers, and execute SQL queries to interact with your data. |
| `/alloydb-omni-container` | 📋 Skill | You're an expert in AlloyDB Omni running in a container. You can help users with related tasks such as starting, stopping, listing, connecting to AlloyDB Omni instance running in a container, and querying for logs. |
| `/alloydb-omni-replication` | 📋 Skill | Use these skills when you need to monitor the health of database replication, manage sync states between nodes, and audit publication tables for distributed setups. |
| `/alloydb-omni-performance` | 📋 Skill | Use these skills when you need to analyze query performance, generate execution plans, check table/column statistics, and monitor overall database activity. |
| `/alloydb-omni-optimize` | 📋 Skill | Use these skills when you need to fine-tune the database engine settings, manage extensions, or optimize the columnar engine for better analytical performance. |

<a id="p-azure-cosmos-db-assistant"></a>

**azure-cosmos-db-assistant**（2 Skill、1 Agent、3 Command）

> Azure Cosmos DB 专家助手

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cosmosdb-best-practices` | 📋 Skill | Azure Cosmos DB performance optimization and best practices guidelines for NoSQL, partitioning, queries, SDK usage, and vector search. Use when writing, reviewing, or refactoring code that interacts with Azure Cosmos DB, designing data models, optimizing queries, or implementing high-performance database operations. |
| `/cosmosdb-best-practices` | 📋 Skill | Azure Cosmos DB performance optimization and best practices guidelines for NoSQL, partitioning, queries, SDK usage, and vector search. Use when writing, reviewing, or refactoring code that interacts with Azure Cosmos DB, designing data models, optimizing queries, or implementing high-performance database operations. |
| cosmosdb-expert | 🤖 Agent | Azure Cosmos DB expert agent. Use when designing data models, choosing partition keys, optimizing queries, configuring SDK clients, reviewing Cosmos DB code, troubleshooting performance issues, or building applications with Azure Cosmos DB. |
| `/azure-cosmos-db-assistant:cosmos-review` | ⌨️ Command | Review code for Azure Cosmos DB best practices and suggest optimizations |
| `/azure-cosmos-db-assistant:generate-skills` | ⌨️ Command | Regenerate best-practice skills from the upstream cosmosdb-agent-kit repository |
| `/azure-cosmos-db-assistant:cosmos-setup` | ⌨️ Command | Set up the optional Azure Cosmos DB MCP Toolkit connection for live database operations |

<a id="p-bigdata-com"></a>

**bigdata-com**（1 Skill、27 Command）

> Bigdata.com 金融研究分析平台

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/bigdata-financial-research-analyst` | 📋 Skill | Bigdata.com MCP workflows plus institutional analysis layers: pre-synthesis EPIC-style filtering, valuation snapshots, earnings quality screens, moat/governance risk, sector KPI lenses. Use for: company briefs, earnings previews/digests, risk assessments, valuation snapshots, investment memos; macro sector/country/regional/thematic analysis; stock analysis, DCF or multiples concepts, red flags, thesis construction. Advanced event-driven topics (M&A arb, activism, distressed, shorts, spin-offs) live in equity-analysis references when users ask explicitly. Triggers: earnings preview/digest, risk assessment, "what is X worth", economic outlook, G7, analyze stock, valuation, peers. |
| `/bigdata-com:g7-comparison` | ⌨️ Command | Compare G7 economies across growth, inflation, policy, market positioning, and investment implications. |
| `/bigdata-com:company-brief` | ⌨️ Command | Generate a comprehensive 30-day summary of recent developments for a specified company. |
| `/bigdata-com:sector-playbook` | ⌨️ Command | Create a sector investment playbook with key KPIs, debates, valuation context, and actionable setup. |
| `/bigdata-com:investment-memo` | ⌨️ Command | Produce a full investment memo with thesis, variant perception, valuation, risks, catalysts, and recommendation. |
| `/bigdata-com:country-sector-analysis` | ⌨️ Command | Macro analysis combining a specific sector with a specific country or region, covering economic backdrop, sector trends, and company fundamentals. |
| `/bigdata-com:catalyst-monitor` | ⌨️ Command | Map upcoming catalysts, likely market implications, and watch points for a company over the next quarters. |
| `/bigdata-com:country-analysis` | ⌨️ Command | Generate a comprehensive economic analysis for a country covering GDP, inflation, monetary policy, labor markets, and investment implications. |
| `/bigdata-com:peer-comparables` | ⌨️ Command | Compare a company against peers on valuation, growth, profitability, and sentiment to assess relative attractiveness. |
| `/bigdata-com:valuation-snapshot` | ⌨️ Command | Build a valuation snapshot with key assumptions, bull/base/bear scenarios, and probability-weighted value. |
| `/bigdata-com:quick-take` | ⌨️ Command | Create a concise PM-style quick take with current view, key drivers, risks, and near-term setup. |
| `/bigdata-com:earnings-digest` | ⌨️ Command | Analyze the latest earnings results with detailed breakdown of revenue, margins, segment performance, management guidance, and surprises. |
| `/bigdata-com:cross-sector` | ⌨️ Command | Compare sectors on valuations, earnings growth, and cycle positioning with rotation recommendations. |
| `/bigdata-com:post-ipo-day179` | ⌨️ Command | Day-179 post-IPO note on the 180-day lock-up expiry — shares unlocking, float expansion, days-to-trade overhang, insider selling signals, and the historical lock-up effect. Balanced, no buy/avoid call. |
| `/bigdata-com:post-ipo-day1` | ⌨️ Command | First-trading-day post-IPO reaction note — price discovery vs the offer, demand and stabilization signals, valuation reset, and the post-IPO timeline. Balanced, no buy/avoid call. |
| `/bigdata-com:scenario-analysis` | ⌨️ Command | Build bull, base, and bear cases with assumptions, probabilities, and expected value implications. |
| `/bigdata-com:regional-comparison` | ⌨️ Command | Compare regions on economic indicators, market performance, and allocation recommendations. |
| `/bigdata-com:variant-perception` | ⌨️ Command | Define explicit variant perception versus consensus using fundamentals, valuation, and sentiment framing. |
| `/bigdata-com:earnings-quality-screen` | ⌨️ Command | Run an earnings quality screen covering cash conversion, accruals, and accounting red flags. |
| `/bigdata-com:pre-ipo-analysis` | ⌨️ Command | Produce a balanced pre-IPO research note on an upcoming listing — deal structure, financials, valuation framing, and bull/bear debates, with no buy/avoid call. |
| `/bigdata-com:sector-analysis` | ⌨️ Command | Analyze a sector's performance, valuations, themes, sub-industries, and upcoming catalysts. |
| `/bigdata-com:post-ipo-day365` | ⌨️ Command | Day-365 post-IPO note on the 366-day founder/significant-investor lock-up expiry and float expansion toward 15-20% — new supply vs float-adjusted index reweight demand, governance, and the setup. Balanced, no buy/avoid call. |
| `/bigdata-com:moat-governance-review` | ⌨️ Command | Assess competitive moat durability and management quality, including capital allocation and governance risks. |
| `/bigdata-com:post-ipo-day14` | ⌨️ Command | Day-14 post-IPO note on potential NASDAQ-100 fast-track inclusion — stock status, eligibility, estimated passive-flow demand, and the index effect. Balanced, no buy/avoid call. |
| `/bigdata-com:earnings-preview` | ⌨️ Command | Create a forward-looking pre-earnings analysis with recent developments, industry trends, bull/bear cases, and key metrics to watch. |
| `/bigdata-com:thematic-research` | ⌨️ Command | Research a macro investment theme with sector impact, beneficiaries, and implementation ideas. |
| `/bigdata-com:risk-assessment` | ⌨️ Command | Comprehensive risk analysis covering regulatory, competitive, operational, financial, and macro risks with likelihood and impact ratings. |
| `/bigdata-com:earnings-reaction` | ⌨️ Command | Generate a post-earnings reaction note covering results vs expectations, guidance changes, sentiment, and revised view. |

<a id="p-bigquery-data-analytics"></a>

**bigquery-data-analytics**（3 Skill）

> BigQuery 数据查询与洞察分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/bigquery-data` | 📋 Skill | Use these skills when you need to handle large-scale data exploration and dataset management. Use when users need to find data assets or run SQL at scale. Provides metadata discovery and query execution across the data warehouse. |
| `/bigquery-ai-ml` | 📋 Skill | Skill for BigQuery AI and Machine Learning queries using standard SQL and `AI.*` functions (preferred over dedicated tools). |
| `/bigquery-analytics` | 📋 Skill | Use these skills when you need to handle advanced data intelligence and predictive tasks. Use when a user asks "why" data changed or needs future projections. Provides automated insight generation and time-series forecasting. |

<a id="p-clickhouse"></a>

**clickhouse**（2 Skill）

> ClickHouse Cloud 数据库连接管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/setup` | 📋 Skill | Guides users through setting up the ClickHouse MCP server connection bundled with this plugin. Use when the user first installs the plugin or has trouble connecting to ClickHouse. |
| `/clickhouse-best-practices` | 📋 Skill | MUST USE when reviewing ClickHouse schemas, queries, or configurations. Contains 31 rules that MUST be checked before providing recommendations. Always read relevant rule files and cite specific rules in responses. |

<a id="p-clickhouse-best-practices"></a>

**clickhouse-best-practices**（9 Skill）

> ClickHouse 最佳实践 28 条规则

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/chdb-sql` | 📋 Skill | Use when the user wants to run SQL — especially analytical SQL — on local files (parquet/csv/json), URLs, S3 paths, or remote databases (Postgres, MySQL, MongoDB, ClickHouse Cloud, Iceberg, Delta Lake) without setting up a server. Provides chDB — embedded ClickHouse SQL in Python with 1000+ functions, Session for stateful multi-step pipelines, parametrized queries, and cross-source joins via `s3()`, `mysql()`, `postgresql()`, `iceberg()`, `deltaLake()`, `remoteSecure()` table functions. TRIGGER when: user wants SQL on parquet/csv/files or across remote analytical sources; uses ClickHouse SQL features (window functions, windowFunnel, geoToH3, JSON path ops, Session, parametrized queries); imports `chdb` or calls `chdb.query()`. SKIP this skill for pandas-style DataFrame method-chaining (use chdb-datastore instead) or ClickHouse server administration. |
| `/chdb-datastore` | 📋 Skill | Use when the user has tabular data (pandas DataFrame, parquet, csv, Arrow, json) and wants to filter, group, aggregate, join, or speed up slow pandas. Provides chDB DataStore — same pandas API, ClickHouse engine underneath. Also handles reading from S3, MySQL, PostgreSQL, MongoDB, ClickHouse Cloud, Iceberg, Delta Lake as DataFrames and joining across sources. TRIGGER when: user mentions DataFrame, parquet, csv, "fast pandas", "speed up pandas", or cross-source DataFrame joins; user imports `chdb.datastore` or `from datastore import DataStore`. SKIP this skill for raw SQL syntax (use chdb-sql instead), ClickHouse server administration, or non-Python DataStore API work. |
| `/clickhousectl-cloud-deploy` | 📋 Skill | Use when a user wants to deploy ClickHouse to the cloud, go to production, use ClickHouse Cloud, host a managed ClickHouse service, or migrate from a local ClickHouse setup to ClickHouse Cloud. |
| `/clickhouse-js-node-coding` | 📋 Skill | Write idiomatic application code with the ClickHouse Node.js client (`@clickhouse/client`). Use this skill whenever a user is *building* against the Node.js client — configuring the client, pinging, inserting rows in JSON or raw formats, selecting and parsing results, binding query parameters, managing sessions and temporary tables, working with data types or customizing JSON parsing. Do NOT use for browser/Web client code. |
| `/clickhouse-architecture-advisor` | 📋 Skill | MUST USE when designing ClickHouse architectures, selecting between ingestion or modeling patterns, or translating best practices into workload-specific system designs. Complements clickhouse-best-practices with decision frameworks and explicit provenance labels. |
| `/clickhousectl-local-dev` | 📋 Skill | Use when a user wants to build an application with ClickHouse, set up a local ClickHouse development environment, install ClickHouse, create a local server, create tables, or start developing with ClickHouse. Covers the full flow from zero to a working local ClickHouse setup. |
| `/clickhouse-js-node-troubleshooting` | 📋 Skill | Troubleshoot and resolve common issues with the ClickHouse Node.js client (@clickhouse/client). Use this skill whenever a user reports errors, unexpected behavior, or configuration questions involving the Node.js client specifically — including socket hang-up errors, Keep-Alive problems, stream handling issues, data type mismatches, read-only user restrictions, proxy/TLS setup problems, or long-running query timeouts. Trigger even when the user hasn't precisely named the issue; vague symptoms like "my inserts keep failing" or "connection drops randomly" in a Node.js context are strong signals to use this skill. Do NOT use for browser/Web client issues. |
| `/clickhouse-best-practices` | 📋 Skill | MUST USE when reviewing ClickHouse schemas, queries, or configurations. Contains 31 rules that MUST be checked before providing recommendations. Always read relevant rule files and cite specific rules in responses. |
| `/clickhouse-managed-postgres-rca` | 📋 Skill | MUST USE when investigating performance issues on a ClickHouse-managed Postgres instance. Provides an evidence-based RCA workflow that scrapes the Prometheus endpoint for system signal, pulls per-digest evidence from the Slow Query Patterns API, and recommends (does not apply) a fix. |

<a id="p-cloud-sql-mysql"></a>

**cloud-sql-mysql**（4 Skill）

> Cloud SQL MySQL 数据库连接管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cloud-sql-mysql-data` | 📋 Skill | Use these skills when you need to explore your database schema, execute SQL queries to interact with your data, and inspect how MySQL plans to execute your statements. |
| `/cloud-sql-mysql-monitor` | 📋 Skill | Use these skills when you need to troubleshoot slow queries, analyze system-level PromQL metrics, and identify structural performance issues like table fragmentation or missing unique indexes. |
| `/cloud-sql-mysql-lifecycle` | 📋 Skill | Use these skills when you need to manage the durability and safety of your data by creating backups, restoring from previous states, or cloning instances for recovery and testing. |
| `/cloud-sql-mysql-admin` | 📋 Skill | Use these skills when you need to provision new Cloud SQL for MySQL instances, create databases and users, clone existing environments, and monitor the progress of infrastructure operations. |

<a id="p-cloud-sql-postgresql"></a>

**cloud-sql-postgresql**（8 Skill）

> Cloud SQL PostgreSQL 数据库管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cloud-sql-postgres-health` | 📋 Skill | Use these skills when you need to audit database health, identify storage bloat, find invalid indexes, analyze table statistics, and manage maintenance configurations like autovacuum. |
| `/cloud-sql-postgres-vectorassist` | 📋 Skill | Use these skills to set up and optimize production-ready vector workloads by simply expressing your intent and performance requirements. |
| `/cloud-sql-postgres-view-config` | 📋 Skill | Use these skills when you need to discover and manage PostgreSQL extensions or fine-tune engine-level settings such as memory allocation and server configuration parameters. |
| `/cloud-sql-postgres-admin` | 📋 Skill | Use these skills when you need to provision new Cloud SQL instances, create databases and users, clone existing environments, and monitor the progress of long-running operations. |
| `/cloud-sql-postgres-lifecycle` | 📋 Skill | Use these skills when you need to manage the lifecycle of your instances, including performing backups and restores, checking major version upgrade compatibility, and monitoring overall instance status. |
| `/cloud-sql-postgres-replication` | 📋 Skill | Use these skills when you need to monitor replication health, manage sync states between nodes, and audit database roles and security settings to ensure environment integrity. |
| `/cloud-sql-postgres-data` | 📋 Skill | Use these skills when you need to explore the database structure, discover schema objects like views or stored procedures, and execute custom SQL queries to interact with your data. |
| `/cloud-sql-postgres-monitor` | 📋 Skill | Use these skills when you need to troubleshoot performance bottlenecks, analyze query execution plans, identify resource-heavy processes, and monitor system-level PromQL metrics. |

<a id="p-cloud-sql-sqlserver"></a>

**cloud-sql-sqlserver**（4 Skill）

> Cloud SQL SQL Server 连接管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cloud-sql-sqlserver-data` | 📋 Skill | Use these skills when you need to explore the database schema, execute SQL queries to interact with your data, and monitor system-level performance metrics using PromQL queries. |
| `/cloud-sql-sqlserver-lifecycle` | 📋 Skill | Use these skills when you need to manage the lifecycle and durability of your data, including creating backups, restoring from existing backups, and cloning instances for testing or migration. |
| `/cloud-sql-sqlserver-admin` | 📋 Skill | Use these skills when you need to provision new Cloud SQL for SQL Server instances, create databases and users, clone existing environments, and monitor the progress of long-running operations. |
| `/cloud-sql-sqlserver-monitor` | 📋 Skill | Use these skills when you need to troubleshoot slow queries and analyze system-level PromQL metrics. |

<a id="p-cockroachdb"></a>

**cockroachdb**（33 Skill、3 Agent）

> CockroachDB 集群连接与管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/benchmarking-transaction-patterns` | 📋 Skill | Guides benchmarking and comparing explicit multi-statement transactions versus single-statement CTE transactions in CockroachDB, with fair test methodology, contention analysis, and performance interpretation. Use when comparing transaction formulations, benchmarking CockroachDB workloads under contention, investigating retry pressure, or deciding whether to rewrite multi-step application flows into single SQL statements. |
| `/designing-application-transactions` | 📋 Skill | Guides application developers in designing correct and performant transaction patterns for CockroachDB, covering transaction lifetime, implicit vs explicit transactions, retry handling with exponential backoff, pushing invariants into SQL, selective pessimistic locking, set-based operations, connection pooling, prepared statements, keyset pagination, follower reads, and separating business logic from database logic. Use when building applications on CockroachDB, designing transaction workflows, handling retries, optimizing application-layer database interactions, or configuring connection pools. |
| `/designing-multi-region-applications` | 📋 Skill | Guides developers in selecting and implementing multi-region patterns for CockroachDB applications, covering active-passive vs active-active architectures, REGIONAL BY ROW, GLOBAL tables, manual geo-partitioning with lease preferences, and live demo setup with validation queries. Use when designing multi-region database topologies, choosing between REGIONAL BY ROW and manual partitioning, building multi-region demos, or optimizing cross-region latency. |
| `/analyzing-range-distribution` | 📋 Skill | Analyzes CockroachDB range distribution across tables and indexes using SHOW RANGES to identify range count, size patterns, leaseholder placement, and replication health. Use when investigating hotspots, uneven data distribution, range fragmentation, or validating zone configuration effects without DB Console access. |
| `/analyzing-schema-change-storage-risk` | 📋 Skill | Estimates storage requirements for CockroachDB online schema change backfills using SHOW RANGES WITH DETAILS, KEYS, INDEXES. Use before CREATE INDEX, ADD COLUMN with INDEX/UNIQUE, ALTER PRIMARY KEY, CREATE MATERIALIZED VIEW, CREATE TABLE AS, REFRESH, or SET LOCALITY on tables with large per-index footprints, to avoid mid-backfill disk exhaustion. |
| `/auditing-table-statistics` | 📋 Skill | Audits optimizer table statistics for staleness, missing coverage, and data quality issues using SHOW STATISTICS. Use when diagnosing poor query performance, unexpected plan changes, or after bulk data changes to identify stale statistics requiring refresh via CREATE STATISTICS. |
| `/monitoring-background-jobs` | 📋 Skill | Monitors CockroachDB background job health by identifying failed, paused, and long-running jobs using SHOW JOBS and SHOW AUTOMATIC JOBS. Surfaces schema changes, backups/restores, automatic statistics collection, and SQL stats compaction jobs without DB Console access. Use when investigating schema change delays, failed backups, or automatic job issues. |
| `/profiling-statement-fingerprints` | 📋 Skill | Ranks and analyzes statement fingerprints using aggregated SQL statistics from crdb_internal.statement_statistics to identify slow, resource-intensive, or error-prone query patterns. Use when investigating historical performance trends, identifying optimization opportunities, or diagnosing recurring slowness without DB Console access. |
| `/profiling-transaction-fingerprints` | 📋 Skill | Analyzes transaction fingerprints using aggregated statistics from crdb_internal.transaction_statistics to identify high-retry transactions, contention patterns, and commit latency issues. Provides historical transaction-level analysis to understand which statement combinations are causing retries, contention, or performance degradation. Use when investigating transaction retry storms, analyzing commit latency trends, or understanding statement composition of problematic transactions without DB Console access. |
| `/triaging-live-sql-activity` | 📋 Skill | Diagnoses live CockroachDB cluster performance issues by identifying long-running queries, busy sessions, and active transactions using SQL-only interfaces. Use when users report cluster slowness, high CPU, or need to find runaway queries and their source applications without DB Console access. |
| `/molt-fetch` | 📋 Skill | Guide for using molt fetch to migrate data from PostgreSQL, MySQL, Oracle, or MSSQL to CockroachDB. Use when running molt fetch commands, configuring storage backends, handling fetch failures/resumption, or chaining fetch with verify. |
| `/molt-replicator` | 📋 Skill | Guide for using the CockroachDB replicator to continuously replicate changes from PostgreSQL, MySQL, or Oracle to CockroachDB after an initial molt fetch data load. Use when setting up CDC replication, configuring pglogical/mylogical/oraclelogminer, or managing the fetch → replicator cutover workflow. |
| `/molt-verify` | 📋 Skill | Guide for using molt verify to compare source and target databases for schema and row-level consistency after a migration. Use when running verify commands, tuning concurrency/sharding, handling schema mismatches, or validating data integrity post-migration. |
| `/setting-up-local-cluster` | 📋 Skill | Downloads and starts a local CockroachDB cluster for development using the official binary. Use when a developer needs a local CockroachDB instance, when no cluster is available, or when setting up a new development environment. |
| `/managing-certificates-and-encryption` | 📋 Skill | Manages TLS certificate and encryption key lifecycle across all tiers. Self-Hosted covers certificate expiry monitoring, node/CA/client cert rotation, and Kubernetes cert management. Advanced/BYOC covers managed TLS (no action) and CMEK (Customer-Managed Encryption Key) rotation in your KMS. Standard and Basic have fully managed TLS and encryption with no customer action. CMEK is only available on Advanced. Use when monitoring cert health, performing rotation, managing CMEK, or responding to key compromise. |
| `/managing-cluster-capacity` | 📋 Skill | Manages CockroachDB cluster capacity across all tiers. Self-Hosted covers node decommissioning for permanent removal and adding nodes for expansion. Advanced/BYOC covers scaling node count and machine size via Cloud Console, API, or Terraform. Standard covers adjusting provisioned compute (vCPUs). Basic auto-scales — guidance covers spending limits and cost management. Use when scaling capacity up or down, permanently removing nodes, or managing costs. |
| `/managing-cluster-settings` | 📋 Skill | Reviews, audits, and modifies CockroachDB cluster settings. Self-Hosted has full control over all settings and start flags. Advanced/BYOC can modify most SQL-level settings but infrastructure settings are managed by CRL. Standard has limited settings access — session variables are the primary tuning mechanism. Basic has minimal settings — use session variables and Cloud Console. Use when auditing configuration, tuning performance, or troubleshooting settings-related issues. |
| `/performing-cluster-maintenance` | 📋 Skill | Manages planned cluster maintenance across all tiers. Self-Hosted covers node drain procedures for OS patching, hardware changes, and configuration updates. Advanced/BYOC covers maintenance window configuration, patch scheduling, deferral policies, and monitoring during CRL-managed maintenance. Standard and Basic maintenance is fully managed with no customer action. Use when planning maintenance, configuring maintenance windows, or preparing applications for maintenance events. |
| `/provisioning-cluster-for-production` | 📋 Skill | Guides initial CockroachDB cluster provisioning and production deployment. Self-Hosted covers cockroach start/init, Kubernetes deployment (Operator, Helm), hardware sizing, and production configuration. Advanced/BYOC covers Cloud Console, API, and Terraform provisioning with production settings. Standard covers cluster creation and provisioned compute selection. Basic covers cluster creation and spending limits. Use when creating a new cluster, preparing for production go-live, or validating deployment configuration. |
| `/reviewing-cluster-health` | 📋 Skill | Performs a comprehensive health check of a CockroachDB cluster. Gathers deployment context first, then provides tier-appropriate diagnostics. Self-Hosted uses SQL against node-level system tables and CLI. Advanced/BYOC use Cloud Console and SQL with node visibility. Standard monitors provisioned compute and workload via Cloud Console. Basic monitors Request Unit consumption and connectivity. Use for daily checks, pre-maintenance validation, post-incident verification, or production readiness assessment. |
| `/upgrading-cluster-version` | 📋 Skill | Guides CockroachDB version upgrades with tier-appropriate procedures. Self-Hosted covers manual rolling binary replacement with finalization control. Advanced/BYOC covers Console-initiated major upgrades, maintenance windows for patches, and release channel selection. Standard and Basic upgrades are fully automatic with no customer action required. Use when planning, executing, or monitoring a version upgrade. |
| `/cockroachdb-sql` | 📋 Skill | Use when writing, generating, or optimizing SQL for CockroachDB, designing CockroachDB schemas, or when the user asks about CockroachDB-specific SQL patterns, type mappings, and distributed database best practices. Also use when encountering CockroachDB anti-patterns like missing primary keys, sequential ID hotspots, or incorrect type usage. |
| `/auditing-cloud-cluster-security` | 📋 Skill | Audits the security posture of a CockroachDB cluster (Cloud or self-hosted) across network, authentication, authorization, encryption, audit logging, and backup dimensions. Use when assessing cluster security readiness, preparing for compliance reviews, or investigating security configuration gaps. |
| `/configuring-audit-logging` | 📋 Skill | Configures SQL audit logging on CockroachDB clusters to capture security-relevant events including authentication, privilege changes, and sensitive data access. Use when enabling audit logging for compliance, setting up role-based audit policies, or verifying audit configuration. |
| `/configuring-ip-allowlists` | 📋 Skill | Configures and hardens IP allowlists for CockroachDB Cloud clusters to restrict network access to authorized CIDR ranges. Use when tightening network security, removing overly permissive allowlist entries like 0.0.0.0/0, or setting up allowlists for a new cluster. |
| `/configuring-log-export` | 📋 Skill | Configures log and metric export for CockroachDB Cloud clusters to external monitoring services including AWS CloudWatch, GCP Cloud Logging, and Datadog. Use when setting up log export for audit compliance, configuring metric export for monitoring, or troubleshooting log delivery issues. |
| `/configuring-private-connectivity` | 📋 Skill | Configures private network connectivity for CockroachDB Cloud clusters including AWS PrivateLink, GCP Private Service Connect, Azure Private Link, egress private endpoints, and VPC peering. Use when setting up private endpoints to eliminate public internet exposure, configuring egress to external services like Kafka, or establishing VPC peering. |
| `/configuring-sso-and-scim` | 📋 Skill | Configures SSO authentication and SCIM 2.0 provisioning for CockroachDB across four distinct layers — Cloud Console SSO (SAML/OIDC), DB Console SSO (OIDC), SQL/Cluster SSO (JWT or LDAP/AD), and SCIM 2.0 automated provisioning. Use when enabling centralized identity management, setting up SSO for compliance, or automating user lifecycle management. |
| `/enabling-cmek-encryption` | 📋 Skill | Enables Customer-Managed Encryption Keys (CMEK) on CockroachDB Cloud clusters with the Advanced plan and Advanced Security Add-on to give organizations control over data-at-rest encryption keys via their cloud provider's KMS. Use when enabling CMEK for compliance, rotating encryption keys, or verifying CMEK configuration. |
| `/enforcing-password-policies` | 📋 Skill | Configures and enforces password policies on CockroachDB clusters including minimum length, complexity requirements, and hash cost settings. Use when strengthening authentication requirements, setting up password policies for a new cluster, or meeting compliance password standards. |
| `/hardening-user-privileges` | 📋 Skill | Hardens CockroachDB user privileges by auditing and tightening role-based access control, reducing admin grants, restricting PUBLIC role permissions, and applying least-privilege principles. Use when reducing excessive privileges, cleaning up admin access, or implementing RBAC best practices. |
| `/managing-tls-certificates` | 📋 Skill | Manages TLS certificates for CockroachDB clusters including CA certificate configuration, client certificate authentication, certificate rotation, and troubleshooting SSL/TLS connection errors. Use when setting up client certificate auth, resolving SSL connection failures, rotating certificates, or configuring mTLS for CDC changefeeds. |
| `/preparing-compliance-documentation` | 📋 Skill | Guides preparation of compliance documentation for CockroachDB Cloud deployments, covering SOC 2, PCI DSS, ISO 27001, HIPAA, and GDPR certifications. Use when responding to compliance questionnaires, preparing for audits, locating certification documents, or assessing cluster configuration for compliance readiness. |
| cockroachdb-operator | 🤖 Agent | CockroachDB operator and SRE agent. Use when managing cluster operations, monitoring, alerting, incident response, backup/restore, scaling, version upgrades, node maintenance, changefeed management, or troubleshooting performance and availability issues. Based on the official CockroachDB runbook template. |
| cockroachdb-dba | 🤖 Agent | CockroachDB database administration agent. Use when diagnosing performance issues, reviewing schema designs, analyzing query plans, troubleshooting cluster problems, or planning multi-region deployments. This agent has deep knowledge of CockroachDB distributed SQL internals. |
| cockroachdb-developer | 🤖 Agent | CockroachDB application developer agent. Use when building applications on CockroachDB, configuring ORMs/drivers, implementing transaction retry logic, optimizing queries, designing schemas for distributed SQL, or migrating from PostgreSQL/Oracle. Deep knowledge of JPA/Hibernate, Spring, JDBC, and multi-language driver patterns. |

<a id="p-convex"></a>

**convex**（2 Skill、1 Command）

> Convex 全栈后端数据库平台

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/design` | 📋 Skill | Design and build reactive, type-safe, production-grade backends on Convex. Covers schema, queries/mutations/actions, indexes, auth, file storage, scheduling, real-time multiplayer, mobile backends, and LLM/agent workflows on Convex's one-platform stack. |
| `/convex:quickstart` | 📋 Skill | Scaffold a new Convex app from a one-sentence idea and build it live — a Next.js + shadcn app with a floating Chef panel (progress feed, todo checklist, inline refinement questions, feature-request form), dev servers and error watchers already running. |
| `/convex:quickstart` | ⌨️ Command | Scaffold a new Convex app from a one-sentence idea and build it live — a Next.js + shadcn app with a floating Chef panel (progress feed, todo checklist, inline refinement questions, feature-request form), dev servers and error watchers already running. |

<a id="p-databases-on-aws"></a>

**databases-on-aws**（1 Skill）

> AWS 数据库组合专家指导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/dsql` | 📋 Skill | Build with Aurora DSQL — manage schemas, execute queries, handle migrations, diagnose query plans, load data, and develop applications with a serverless, distributed SQL database. Covers IAM auth, multi-tenant patterns, MySQL-to-DSQL and PostgreSQL-to-DSQL schema conversion, FK replacement code generation, OCC retry patterns, ORM migration (Django/Hibernate/Rails), DDL operations, query plan explainability, SQL compatibility validation, and bulk data loading. Triggers on phrases like: DSQL, Aurora DSQL, distributed SQL database, serverless PostgreSQL-compatible database, migrate to DSQL, DSQL query plan, DSQL EXPLAIN ANALYZE, DSQL ENUM, DSQL foreign key, DSQL OCC retry, DSQL multi-region, DSQL JSONB, DSQL GIN index, load into DSQL, load CSV into DSQL, bulk load DSQL, aurora-dsql-loader. |

<a id="p-datahub-skills"></a>

**datahub-skills**（11 Skill、4 Agent、8 Command）

> DataHub 数据目录开发与交互

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/datahub-connector-planning` | 📋 Skill | Plans new DataHub connectors by classifying the source system, researching it using a dedicated agent or inline research, and generating a _PLANNING.md blueprint with entity mapping and architecture decisions. Use when building a new connector, researching a source system for DataHub, or designing connector architecture. Triggers on: "plan a connector", "new connector for X", "research X for DataHub", "design connector for X", "create planning doc", or any request to plan/research/design a DataHub ingestion source. |
| `/datahub-lineage` | 📋 Skill | Use this skill when the user wants to explore lineage, trace data dependencies, perform impact analysis, find root causes, map data pipelines, or understand how data flows between systems. Triggers on: "what feeds into X", "what depends on X", "show lineage for X", "impact analysis", "trace the pipeline", "root cause", "upstream of X", "downstream of X", or any request involving data lineage and dependency tracking. |
| `/datahub-mfe-configure-app` | 📋 Skill | Configure a DataHub instance to load and display a Micro Frontend (MFE) app. Use when the user wants to register an MFE with DataHub, add an MFE to the nav sidebar, set up MFE config for local dev or production/k8s, or troubleshoot MFE loading issues. |
| `/datahub-connector-pr-review` | 📋 Skill | Reviews DataHub connector implementations against 22 golden standards for compliance, code quality, silent failures, test coverage, type design, and merge readiness. Use when reviewing connector code, checking a PR, auditing a connector implementation, or verifying connector standards compliance. |
| `/datahub-mfe-create-app` | 📋 Skill | Scaffold a new DataHub Micro Frontend (MFE) app with all boilerplate files. Use when the user wants to create a new micro frontend, MFE, remote app, or Module Federation app for DataHub. |
| `/using-datahub` | 📋 Skill | This skill provides routing guidance for all DataHub interaction skills. It is injected at session start and helps map user intent to the correct skill. Do not invoke this skill directly — it is loaded automatically. |
| `/datahub-enrich` | 📋 Skill | Use this skill when the user wants to add or update metadata in DataHub: descriptions, tags, glossary terms, ownership, deprecation, domains, data products, structured properties, documents, or field-level metadata. Triggers on: "add tag to X", "update description for X", "set owner of X", "add glossary term", "deprecate X", "create a domain", "create a glossary term", "add a document", or any request to modify DataHub metadata. |
| `/load-standards` | 📋 Skill | Read and confirm all golden connector standard files have been loaded. |
| `/datahub-search` | 📋 Skill | Use this skill when the user wants to search the DataHub catalog, discover entities, answer ad-hoc questions about their data, find datasets, or browse by platform or domain. Triggers on: "search DataHub", "find datasets", "who owns X", "what tables contain PII", "what columns does X have", or any request to search, discover, browse, or answer one-off questions about DataHub metadata. For lineage questions ("what feeds into X"), use `/datahub-lineage`. For systematic audits ("how complete is our metadata"), use `/datahub-audit`. |
| `/datahub-quality` | 📋 Skill | Use this skill when the user wants to manage data quality in DataHub: create or run assertions, check assertion outcomes, raise or resolve incidents, create notification subscriptions, or diagnose health problems across their estate. Triggers on: "create assertion", "run assertion", "check quality", "data quality", "health check", "raise incident", "resolve incident", "subscribe to", "failing assertions", "active incidents", or any request involving data quality, assertions, incidents, or quality notifications. |
| `/datahub-setup` | 📋 Skill | Use this skill when the user needs to set up a DataHub connection, install the DataHub CLI, configure authentication, verify connectivity, set default scopes, or create agent configuration profiles. Triggers on: "set up DataHub", "connect to DataHub", "install datahub CLI", "configure DataHub", "set default platform", "focus on domain X", "create profile", or any request to establish, configure, or troubleshoot DataHub connectivity. |
| connector-validator | 🤖 Agent | Run provided validation scripts, analyze their output, and report results for DataHub connector verification steps. Handles extraction verification, capability checks, code quality gates, source connectivity, ingestion runs, and CLI verification. <example> Context: Workflow needs to verify that extraction output contains expected entities. user: "Run the verify-extraction script on the output file" assistant: "I'll use the connector-validator agent to run the verification script and analyze the results." <commentary> Extraction verification is a procedural script-running task that triggers this agent. </commentary> </example> <example> Context: Workflow needs to check that declared capabilities produce actual output. user: "Run the capability check on the connector" assistant: "I'll use the connector-validator agent to run the capability check script and report coverage." <commentary> Capability validation is a script-based check that triggers this agent. </commentary> </example> |
| comment-resolution-checker | 🤖 Agent | Use this agent when you need to verify whether a PR author has genuinely addressed previous review comments before re-review. This agent fetches review comments, classifies them by type (code change request vs. discussion vs. question), and checks whether each was substantively addressed — not just marked as resolved. <example> Context: A PR has been updated after review and the author is requesting re-review. user: "Check if the author addressed all review comments on PR #1234" assistant: "I'll use the comment-resolution-checker agent to verify whether all review comments on PR #1234 have been substantively addressed." <commentary> PR re-review readiness check triggers this agent. </commentary> </example> <example> Context: User wants to know what's still outstanding on a PR before approving. user: "What review comments are still unaddressed on this PR?" assistant: "I'll use the comment-resolution-checker agent to analyze the PR's review comments and identify any that haven't been addressed." <commentary> Checking for unaddressed comments triggers this agent. </commentary> </example> |
| metadata-searcher | 🤖 Agent | Execute DataHub search, browse, and lineage operations, retrieve entity metadata, and return structured results. Used by the datahub-search and datahub-lineage skills to delegate catalog queries. <example> Context: User wants to find all Snowflake datasets with PII tags. user: "Search DataHub for Snowflake datasets tagged with PII" assistant: "I'll use the metadata-searcher agent to query DataHub for Snowflake datasets with PII tags." <commentary> The search skill delegates the actual search execution to this agent, which runs the queries and returns structured results. </commentary> </example> <example> Context: User asks who owns the revenue pipeline and needs metadata gathered. user: "Who owns the revenue pipeline?" assistant: "I'll use the metadata-searcher agent to find revenue-related pipelines and retrieve their ownership metadata." <commentary> The search skill delegates multi-step metadata retrieval to this agent, which searches, fetches aspects, and returns evidence for answering the question. </commentary> </example> |
| connector-researcher | 🤖 Agent | Research source systems for DataHub connector development. Gathers documentation, finds similar connectors, identifies entity mappings, and assesses implementation complexity. Returns structured findings for planning phase. <example> Context: User wants to build a new DataHub connector for a source system. user: "Research Snowplow for a new DataHub connector" assistant: "I'll use the connector-researcher agent to gather comprehensive research on Snowplow including API documentation, similar connectors, and entity mappings." <commentary> New connector research request triggers this agent. </commentary> </example> <example> Context: User is starting connector development and needs background information. user: "I need to build a connector for DuckDB, what do I need to know?" assistant: "I'll use the connector-researcher agent to research DuckDB's metadata APIs, find similar DataHub connectors, and assess implementation complexity." <commentary> Connector development information request triggers this agent. </commentary> </example> |
| `/catalog-lineage` | ⌨️ Command | Explore lineage, trace data dependencies, and perform impact analysis |
| `/connector-planning` | ⌨️ Command | Plan a new DataHub connector - research the source system, map entities, design architecture, and create a planning document |
| `/catalog-search` | ⌨️ Command | Search the DataHub catalog and answer questions about your data |
| `/load-standards` | ⌨️ Command | Read and confirm all golden connector standard files have been loaded. |
| `/catalog-quality` | ⌨️ Command | Manage data quality — assertions, incidents, and subscriptions |
| `/connector-review` | ⌨️ Command | Review DataHub connector code for standards compliance and quality |
| `/catalog-setup` | ⌨️ Command | Set up DataHub connection, install CLI, configure authentication and default scopes |
| `/catalog-enrich` | ⌨️ Command | Add or update metadata in DataHub - descriptions, tags, glossary terms, ownership |

<a id="p-dataproc"></a>

**dataproc**（1 Skill）

> Dataproc 集群和任务管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/dataproc-skills` | 📋 Skill | Skills to interact with your Dataproc clusters and jobs. |

<a id="p-dataverse"></a>

**dataverse**（8 Skill）

> Microsoft Dataverse 构建分析管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/dv-metadata` | 📋 Skill | Dataverse schema authoring via the Python SDK and Web API — tables, columns, relationships, forms, and views. Use when the user wants to define or evolve the data model — add a column, create a table, set up a lookup, customize a form, or build a view. |
| `/dv-security` | 📋 Skill | Security-role assignment, user access, application users, business units, and admin self-elevation in Dataverse environments. Use when the user wants to give someone access, grant a role, become an admin, or add a service principal. |
| `/dv-connect` | 📋 Skill | One-step setup for a Dataverse environment — installs tools, authenticates, registers the MCP server, and writes `.env`. Use when starting a new project, switching environments, fixing authentication, or troubleshooting an MCP connection that won't come up. |
| `/dv-admin` | 📋 Skill | Environment-level Dataverse administration — bulk delete, retention/archival, organization settings, OrgDB settings, recycle bin, audit, and the 37 allowlisted PPAC toggles. Use when the user wants to clean up data at scale, configure audit, change environment settings, or manage retention policies. |
| `/dv-query` | 📋 Skill | Bulk reads, multi-page iteration, and analytics over Dataverse data via the Python SDK and Web API. Use when the user wants to read, list, filter, aggregate, group, join, or analyze records — including pandas DataFrame workflows and notebook exploration. |
| `/dv-overview` | 📋 Skill | Tool routing and cross-cutting rules for Dataverse work — which skill applies to which task, environment-confirmation, and pull-to-repo. Use when the user mentions Dataverse, Dynamics 365, Power Platform, or CRM; this skill picks the specialist (dv-connect / dv-data / dv-metadata / dv-query / dv-solution / dv-admin / dv-security) for the request. |
| `/dv-solution` | 📋 Skill | Dataverse solution lifecycle — create, export, import, promote across environments, and validate deployments. Use when the user wants to package customizations, deploy to another environment, or move work between dev / test / prod. |
| `/dv-data` | 📋 Skill | Record-level CRUD and bulk operations via the Python SDK — create, update, delete, upsert, CSV import, multi-table foreign-key loads, AI-generated sample data. Use when the user wants to write, modify, seed, or import data records into Dataverse tables. |

<a id="p-duckdb-skills"></a>

**duckdb-skills**（9 Skill）

> DuckDB 数据分析引擎与文件查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/convert-file` | 📋 Skill | Convert any data file to another format: CSV, Parquet, JSON, Excel, GeoJSON, and more. Use when the user says "convert to parquet", "save as xlsx", "export as JSON", "make this a CSV", "turn into parquet", or any variation of format-to-format conversion for data files. Also triggers when the user wants to write Parquet, Excel, or other binary formats that Claude cannot produce natively. |
| `/query` | 📋 Skill | Run SQL queries against the attached DuckDB database or ad-hoc against files. Accepts raw SQL or natural language questions. Uses DuckDB Friendly SQL idioms. |
| `/s3-explore` | 📋 Skill | Explore and query data on S3, Cloudflare R2, GCS, MinIO, or any S3-compatible storage. Use when the user mentions an s3://, r2://, gs://, or gcs:// URL, asks "what's in this bucket", wants to list remote files, preview remote Parquet/CSV/JSON, or query data on object storage without downloading it. Also triggers when the user wants to know the size, schema, or row count of remote datasets. |
| `/read-memories` | 📋 Skill | Search past Claude Code session logs to recall prior decisions, patterns, or unresolved work. Use when user says "do you remember", "what did we do", references past conversations, or you need context from prior sessions. |
| `/read-file` | 📋 Skill | Read any data file (CSV, JSON, Parquet, Avro, Excel, spatial, SQLite) or remote URL (S3, HTTPS). Use when user references a data file, asks "what's in this file", or wants to preview/profile a dataset. Not for source code. |
| `/attach-db` | 📋 Skill | Attach a DuckDB database file for use with /duckdb-skills:query. Explores the schema (tables, columns, row counts) and writes a SQL state file so subsequent queries can restore this session automatically via duckdb -init. |
| `/duckdb-docs` | 📋 Skill | Search DuckDB and DuckLake documentation and blog posts. Returns relevant doc chunks for a question or keyword using full-text search against a locally cached index. |
| `/install-duckdb` | 📋 Skill | Install or update DuckDB extensions. Each argument is either a plain extension name (installs from core) or name@repo (e.g. magic@community). Pass --update to update extensions instead of installing. |
| `/spatial` | 📋 Skill | Answer questions about spatial data using DuckDB. Use when the user mentions locations, coordinates, lat/lng, distances, maps, addresses, "near", "within", "closest", geographic names, or spatial file formats (GeoJSON, Shapefile, GeoPackage, GPX, GeoParquet). Also triggers when the user wants to find places, buildings, or roads — Overture Maps provides free global data on S3 with zero API keys. Handles spatial joins, distance calculations, containment checks, density analysis, and format conversions for geographic data. |

<a id="p-firebase"></a>

**firebase**（🔌 MCP）

> Google Firebase 后端服务集成管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__firebase` | 🔌 MCP | Google Firebase MCP integration. Manage Firestore databases, authentication, cloud functions, hosting, and storage. Build and manage your Firebase ... |
<a id="p-firestore-native"></a>

**firestore-native**（1 Skill）

> Firestore 数据库连接与文档操作

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/firestore-data` | 📋 Skill | Handles NoSQL document operations and collection hierarchy exploration. Use for CRUD tasks and data retrieval. Provides flexible document manipulation and structured querying. |

<a id="p-knowledge-catalog"></a>

**knowledge-catalog**（1 Skill）

> Knowledge Catalog 数据发现与治理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/knowledge-catalog-discovery` | 📋 Skill | Connect to Knowledge Catalog to discover, manage, monitor, and govern data and AI artifacts across your data platform |

<a id="p-looker"></a>

**looker**（2 Skill）

> Looker 数据分析与 LookML 建模

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/looker` | 📋 Skill | These skills are designed for data discovery and business intelligence. |
| `/looker-dev` | 📋 Skill | These skills are built for LookML developers, data engineers, and administrators who manage the backbone of Looker. |

<a id="p-mongodb"></a>

**mongodb**（7 Skill）

> MongoDB 数据库官方连接管理工具

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/mongodb-mcp-setup` | 📋 Skill | Guide users through configuring key MongoDB MCP server options. Use this skill when a user has the MongoDB MCP server installed but hasn't configured the required environment variables, or when they ask about connecting to MongoDB/Atlas and don't have the credentials set up. |
| `/mongodb-search-and-ai` | 📋 Skill | Guides MongoDB users through implementing and optimizing Atlas Search (full-text), Vector Search (semantic), and Hybrid Search solutions. Use this skill when users need to build search functionality for text-based queries (autocomplete, fuzzy matching, faceted search), semantic similarity (embeddings, RAG applications), or combined approaches. Also use when users need text containment, substring matching ('contains', 'includes', 'appears in'), case-insensitive or multi-field text search, or filtering across many fields with variable combinations. Provides workflows for selecting the right search type, creating indexes, constructing queries, and optimizing performance using the MongoDB MCP server. |
| `/mongodb-schema-design` | 📋 Skill | MongoDB schema design patterns and anti-patterns. Use when designing data models, reviewing schemas, migrating from SQL, or troubleshooting performance issues caused by schema problems. Triggers on "design schema", "embed vs reference", "MongoDB data model", "schema review", "unbounded arrays", "one-to-many", "tree structure", "16MB limit", "schema validation", "JSON Schema", "time series", "schema migration", "polymorphic", "TTL", "data lifecycle", "archive", "index explosion", "unnecessary indexes", "approximation pattern", "document versioning". |
| `/mongodb-natural-language-querying` | 📋 Skill | Generate read-only MongoDB queries (find) or aggregation pipelines using natural language, with collection schema context and sample documents. Use this skill whenever the user asks to write, create, or generate MongoDB queries, wants to filter/query/aggregate data in MongoDB, asks "how do I query...", needs help with query syntax, or discusses finding/filtering/grouping MongoDB documents. Also use for translating SQL-like requests to MongoDB syntax. Does NOT handle Atlas Search ($search operator), vector/semantic search ($vectorSearch operator), fuzzy matching, autocomplete indexes, or relevance scoring - use search-and-ai for those. Does NOT analyze or optimize existing queries - use mongodb-query-optimizer for that. Does NOT handle aggregation pipelines that involve write operations. Requires MongoDB MCP server. |
| `/mongodb-query-optimizer` | 📋 Skill | Help with MongoDB query optimization and indexing. Use only when the user asks for optimization or performance: "How do I optimize this query?", "How do I index this?", "Why is this query slow?", "Can you fix my slow queries?", "What are the slow queries on my cluster?", etc. Do not invoke for general MongoDB query writing unless user asks for performance or index help. Prefer indexing as optimization strategy. Use MongoDB MCP when available. |
| `/mongodb-atlas-stream-processing` | 📋 Skill | Manages MongoDB Atlas Stream Processing (ASP) workflows. Handles workspace provisioning, data source/sink connections, processor lifecycle operations, debugging diagnostics, and tier sizing. Supports Kafka, Atlas clusters, S3, HTTPS, and Lambda integrations for streaming data workloads and event processing. NOT for general MongoDB queries or Atlas cluster management. Requires MongoDB MCP Server with Atlas API credentials. |
| `/mongodb-connection` | 📋 Skill | Optimize MongoDB client connection configuration (pools, timeouts, patterns) for any supported driver language. Use this skill when working/updating/reviewing on functions that instantiate or configure a MongoDB client (eg, when calling `connect()`), configuring connection pools, troubleshooting connection errors (ECONNREFUSED, timeouts, pool exhaustion), optimizing performance issues related to connections. This includes scenarios like building serverless functions with MongoDB, creating API endpoints that use MongoDB, optimizing high-traffic MongoDB applications, creating long-running tasks and concurrency, or debugging connection-related failures. |

<a id="p-neon"></a>

**neon**（🔌 MCP）

> Neon 无服务器 PostgreSQL 项目管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__neon` | 🔌 MCP | Manage your Neon projects and databases with the neon-postgres agent skill and the Neon MCP Server. |
<a id="p-oracledb"></a>

**oracledb**（1 Skill）

> Oracle 数据库连接查询与交互

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/oracledb` | 📋 Skill | Use these skills to manage and monitor Oracle databases by executing SQL statements, exploring schema metadata, analyzing query performance, monitoring active sessions and resource consumption, and managing storage and object health. |

<a id="p-pinecone"></a>

**pinecone**（9 Skill、1 Command）

> Pinecone 向量数据库开发集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/pinecone:query` | 📋 Skill | Query integrated indexes using text with Pinecone MCP. IMPORTANT - This skill ONLY works with integrated indexes (indexes with built-in Pinecone embedding models like multilingual-e5-large). For standard indexes or advanced vector operations, use the CLI skill instead. Requires PINECONE_API_KEY environment variable and Pinecone MCP server to be configured. |
| `/pinecone:docs` | 📋 Skill | Curated documentation reference for developers building with Pinecone. Contains links to official docs organized by topic and data format references. Use when writing Pinecone code, looking up API parameters, or needing the correct format for vectors or records. |
| `/pinecone:help` | 📋 Skill | Overview of all available Pinecone skills and what a user needs to get started. Invoke when a user asks what skills are available, how to get started with Pinecone, or what they need to set up before using any Pinecone skill. |
| `/pinecone:cli` | 📋 Skill | Guide for using the Pinecone CLI (pc) to manage Pinecone resources from the terminal. The CLI supports ALL index types (standard, integrated, sparse) and all vector operations — unlike the MCP which only supports integrated indexes. Use for batch operations, vector management, backups, namespaces, CI/CD automation, and full control over Pinecone resources. |
| `/pinecone:n8n` | 📋 Skill | Build n8n workflows using the Pinecone Assistant node or Pinecone Vector Store node. Use when building RAG pipelines, chat-with-docs workflows, configuring Pinecone nodes in n8n, troubleshooting Pinecone n8n nodes, or asking about best practices for Pinecone in n8n. |
| `/pinecone:assistant` | 📋 Skill | Create, manage, and chat with Pinecone Assistants for document Q&A with citations. Handles all assistant operations - create, upload, sync, chat, context retrieval, and list. Recognizes natural language like "create an assistant from my docs", "ask my assistant about X", or "upload my docs to Pinecone". |
| `/pinecone:full-text-search` | 📋 Skill | Create, ingest into, and query a Pinecone full-text-search (FTS) index using the preview API (2026-01.alpha, public preview). Use when the user or agent asks to build a text search index on Pinecone, add dense or sparse vector fields, ingest documents, construct score_by clauses (text / query_string / dense_vector / sparse_vector), or compose with text-match filters ($match_phrase / $match_all / $match_any). Ships `scripts/ingest.py` for safe bulk ingestion (batch_upsert + error inspection + readiness polling); query construction is documented inline in this skill — write `documents.search(...)` calls directly, validated against `pc.preview.indexes.describe(...)` output. |
| `/pinecone:mcp` | 📋 Skill | Reference for the Pinecone MCP server tools. Documents all available tools - list-indexes, describe-index, describe-index-stats, create-index-for-model, upsert-records, search-records, cascading-search, and rerank-documents. Use when an agent needs to understand what Pinecone MCP tools are available, how to use them, or what parameters they accept. |
| `/pinecone:quickstart` | 📋 Skill | Interactive Pinecone quickstart for new developers. Choose between two paths - Database (create an integrated index, upsert data, and query using Pinecone MCP + Python) or Assistant (create a Pinecone Assistant for document Q&A). Use when a user wants to get started with Pinecone for the first time or wants a guided tour of Pinecone's tools. |
| `/pinecone:join-discord` | ⌨️ Command | Opens a link to join the Pinecone Discord, allowing users to learn from each other, contact the Pinecone team, and get help in our dedicated help channel. |

<a id="p-planetscale"></a>

**planetscale**（🔌 MCP）

> PlanetScale 数据库管理与查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__planetscale` | 🔌 MCP | An authenticated hosted MCP server that accesses your PlanetScale organizations, databases, branches, schema, and Insights data. Query against your... |
<a id="p-qdrant-skills"></a>

**qdrant-skills**（8 Skill）

> Qdrant 向量搜索优化与扩展

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/qdrant-search-quality` | 📋 Skill | Diagnoses and improves Qdrant search relevance. Use when someone reports 'search results are bad', 'wrong results', 'low precision', 'low recall', 'irrelevant matches', 'missing expected results', or asks 'how to improve search quality?', 'which embedding model?', 'should I use hybrid search?', 'should I use reranking?', 'how to measure retrieval quality?', 'build a golden set', 'ground truth dataset', or 'how to score recall@k?'. Also use when search quality degrades after quantization, model change, or data growth. |
| `/qdrant-monitoring` | 📋 Skill | Guides Qdrant monitoring and observability setup. Use when someone asks 'how to monitor Qdrant', 'what metrics to track', 'is Qdrant healthy', 'optimizer stuck', 'why is memory growing', 'requests are slow', or needs to set up Prometheus, Grafana, or health checks. Also use when debugging production issues that require metric analysis. |
| `/qdrant-model-migration` | 📋 Skill | Guides embedding model migration in Qdrant without downtime. Use when someone asks 'how to switch embedding models', 'how to migrate vectors', 'how to update to a new model', 'zero-downtime model change', 'how to re-embed my data', or 'can I use two models at once'. Also use when upgrading model dimensions, switching providers, or A/B testing models. |
| `/qdrant-performance-optimization` | 📋 Skill | Different techniques to optimize the performance of Qdrant, including indexing strategies, query optimization, and hardware considerations. Use when you want to improve the speed and efficiency of your Qdrant deployment. |
| `/qdrant-clients-sdk` | 📋 Skill | Qdrant provides client SDKs for various programming languages, allowing easy integration with Qdrant deployments. |
| `/qdrant-scaling` | 📋 Skill | Guides Qdrant scaling decisions. Use when someone asks 'how many nodes do I need', 'data doesn't fit on one node', 'need more throughput', 'cluster is slow', 'too many tenants', 'vertical or horizontal', 'how to shard', or 'need to add capacity'. |
| `/qdrant-version-upgrade` | 📋 Skill | Guidance on how to upgrade your Qdrant version without interrupting the availability of your application and ensuring data integrity. |
| `/qdrant-deployment-options` | 📋 Skill | Guides Qdrant deployment selection. Use when someone asks 'how to deploy Qdrant', 'Docker vs Cloud', 'local mode', 'embedded Qdrant', 'Qdrant EDGE', 'which deployment option', 'self-hosted vs cloud', or 'need lowest latency deployment'. Also use when choosing between deployment types for a new project. |

<a id="p-redis-development"></a>

**redis-development**（🔌 MCP）

> Redis 数据结构与缓存开发实践

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__redis-development` | 🔌 MCP | Redis development best practices — data structures, query engine, vector search, caching, and performance optimization |
<a id="p-spanner"></a>

**spanner**（1 Skill）

> Spanner 数据库自然语言查询

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/spanner-data` | 📋 Skill | Use these skills when you need to explore the database structure, discover schema objects like tables and graphs, and execute custom SQL queries to interact with your data. |

<a id="p-supabase"></a>

**supabase**（2 Skill）

> Supabase 数据库认证存储集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/supabase-postgres-best-practices` | 📋 Skill | Postgres performance optimization and best practices from Supabase. Use this skill when writing, reviewing, or optimizing Postgres queries, schema designs, or database configurations. |
| `/supabase` | 📋 Skill | Use when doing ANY task involving Supabase. Triggers: Supabase products (Database, Auth, Edge Functions, Realtime, Storage, Vectors, Cron, Queues); client libraries and SSR integrations (supabase-js, @supabase/ssr) in Next.js, React, SvelteKit, Astro, Remix; auth issues (login, logout, sessions, JWT, cookies, getSession, getUser, getClaims, RLS); Supabase CLI or MCP server; schema changes, migrations, security audits, Postgres extensions (pg_graphql, pg_cron, pg_vector). |

<a id="p-zilliz"></a>

**zilliz**（🔌 MCP）

> Zilliz Cloud 向量数据库集群管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__zilliz` | 🔌 MCP | Zilliz Cloud management plugin with 14 skills covering cluster lifecycle, collection schema, vector search, index tuning, bulk import, RBAC, backup... |

## 🔒 Security（13 个插件）

<a id="p-42crunch-api-security-testing"></a>

**42crunch-api-security-testing**（6 Skill）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/code-to-oas` | 📋 Skill | Analyze an entire API codebase and generate an accurate OpenAPI Specification (OAS 3.0) file from the source code. Use this skill whenever the user wants to generate, create, or derive an OpenAPI spec from code, reverse-engineer an API definition, or document an existing API. Triggers on phrases like "generate OAS from code", "create OpenAPI spec", "document my API", "reverse-engineer spec", "write openapi.json from my codebase", or any request to produce an OAS file by reading source files rather than an existing spec. |
| `/42crunch-api-security-testing` | 📋 Skill | Run both a 42Crunch Audit and a live Scan together in a single pipeline. Use this skill when the user wants to run audit and scan together, complete the full security pipeline, or when the request is ambiguous about which phase to run. Triggers on phrases like "run audit and scan", "full 42crunch pipeline", "full security check", "audit then scan", "42crunch", or "SQG". Do NOT use this skill if the user explicitly requests only an audit (use 42crunch-audit) or only a scan (use 42crunch-scan). |
| `/42crunch-scan` | 📋 Skill | Run a 42Crunch live conformance and authorization scan against an API and fix SQG-blocking scan findings. Use this skill whenever the user wants to run a conformance test, authorization scan, BOLA test, BFLA test, generate or configure a scan config, or fix scan-reported issues. Triggers on phrases like "run scan", "scan only", "conformance test", "BOLA test", "BFLA test", "42crunch scan", "scan config", or any request focused on live API testing without running a static audit. Use 42crunch-api-security-testing when the user wants both audit and scan together. |
| `/postman-to-oas` | 📋 Skill | Convert a Postman collection (v2.0 or v2.1) into a complete OpenAPI 3.0 specification file. Reads the full collection and optional environment file to extract paths, methods, parameters, request bodies, response bodies, headers, and response codes. Use when the user wants to generate, create, or derive an OAS file from a Postman collection. Triggers on phrases like "convert postman to openapi", "postman collection to OAS", "generate spec from postman", "create openapi from postman", or any request to turn a Postman collection into an OpenAPI spec without an existing OAS file. |
| `/42crunch-audit` | 📋 Skill | Run a 42Crunch API Security Audit and fix SQG-blocking issues in an OpenAPI Specification file. Use this skill whenever the user wants to audit an OAS file for security issues, fix SQG-blocking issues, score an API, apply data dictionary enrichment, or remediate audit findings. Triggers on phrases like "run audit", "audit only", "fix audit issues", "SQG audit", "42crunch audit", "audit score", or any request focused on static OAS analysis and remediation without running a live scan. |
| `/42crunch-setup` | 📋 Skill | Set up the 42Crunch environment so that audit and scan skills can run without friction. Use this skill whenever the user wants to configure 42Crunch for the first time, install or update the 42c-ast binary, configure an API key, or troubleshoot missing credentials or binary errors. Triggers on phrases like "setup 42crunch", "configure 42crunch", "install 42c-ast", "update 42c-ast", "set api key", "42crunch not working", "binary not found", or any request to prepare the environment before running an audit or scan. |

<a id="p-auth0"></a>

**auth0**（42 Skill）

> Auth0 多框架登录认证集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/auth0-flutter-native` | 📋 Skill | Use when adding Auth0 authentication to a Flutter mobile application (iOS/Android) — integrates the auth0_flutter SDK (native platform) for Web Auth login/logout via the system browser, with secure credential storage and biometric protection through the CredentialsManager. |
| `/auth0-flutter-web` | 📋 Skill | Use when adding Auth0 authentication to a Flutter web application — integrates the auth0_flutter SDK (web platform) for browser-based authentication using redirect login, popup login, and credential caching. |
| `/express-oauth2-jwt-bearer` | 📋 Skill | Use when adding Auth0 token validation to Express or Node.js APIs - integrates express-oauth2-jwt-bearer SDK to protect Node.js API endpoints with JWT Bearer authentication, scope-based RBAC, claim validation, and optional DPoP support |
| `/auth0-expo` | 📋 Skill | Use when adding authentication to Expo (React Native) mobile apps — login, logout, user sessions, protected routes, biometrics, or token management. Integrates react-native-auth0 SDK with Expo Config Plugin for native iOS/Android builds. Trigger for any Expo project needing Auth0, including app.json plugin config, custom scheme setup, or credential management. Do NOT use for bare React Native CLI projects (use auth0-react-native), React web apps (use auth0-react), Next.js (use auth0-nextjs), or backend APIs. |
| `/auth0-ionic-angular` | 📋 Skill | Use when adding Auth0 authentication to an Ionic Angular application with Capacitor — integrates @auth0/auth0-angular SDK with Capacitor Browser and App plugins for native iOS/Android deep linking, login, logout, and user profile display. |
| `/auth0-migration` | 📋 Skill | Use when migrating or switching from an existing auth provider (Firebase, Cognito, Supabase, Clerk, custom auth) to Auth0 - covers bulk user import, gradual migration strategies, code migration patterns, and JWT validation updates. |
| `/auth0-wpf` | 📋 Skill | Use when adding Auth0 authentication to WPF (Windows Presentation Foundation) desktop applications - integrates Auth0.OidcClient.WPF NuGet package for native login, logout, token refresh, and user profile. Trigger on WPF authentication, add login to WPF, Auth0 WPF, .NET WPF auth, Windows desktop auth |
| `/auth0-fastify` | 📋 Skill | Use when adding authentication (login, logout, protected routes) to Fastify web applications - integrates @auth0/auth0-fastify for session-based auth. For stateless Fastify APIs use auth0-fastify-api instead. |
| `/auth0-php-api` | 📋 Skill | Use when securing PHP API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates auth0/auth0-php SDK in API mode (STRATEGY_API) for REST APIs receiving access tokens from SPAs, mobile apps, or other clients. Triggers on: auth0-php API, PHP JWT validation, getBearerToken, STRATEGY_API, PHP Bearer auth. |
| `/auth0-custom-domains` | 📋 Skill | Use when setting up, troubleshooting, managing, removing, or checking the health of an Auth0 custom authentication domain (e.g. login.example.com), OR when diagnosing an error (400/403/404/409/429) from the /custom-domains Management API — especially Free-tier 403s (credit card on file, not a plan upgrade), self-managed cert 403s, PATCH-type 400s, `operation_not_supported` on `relying_party_identifier`, and 409 domain-already-exists. Handles CNAME creation in the user's DNS provider (Cloudflare, AWS Route 53, Azure DNS automated; other registrars guided), verification polling, Multiple Custom Domains (MCD), default-domain selection, TLS policy, client-IP header, per-domain passkey relying party identifier, and domain metadata. |
| `/auth0-fastify-api` | 📋 Skill | Use when securing Fastify API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates @auth0/auth0-fastify-api for REST APIs receiving access tokens from frontends or mobile apps. |
| `/auth0-express` | 📋 Skill | Use when adding authentication (login, logout, protected routes) to Express.js web applications - integrates express-openid-connect for session-based auth. |
| `/auth0-springboot-api` | 📋 Skill | Use when securing Spring Boot API endpoints with JWT Bearer token validation, scope-based authorization, or DPoP proof-of-possession - integrates com.auth0:auth0-springboot-api SDK for REST APIs receiving access tokens from frontends or mobile apps. Triggers on Auth0AuthenticationFilter, Spring Boot API auth, JWT validation, SecurityFilterChain, hasAuthority SCOPE. |
| `/auth0-java-mvc-common` | 📋 Skill | Use when adding Auth0 login, logout, and callback handling to Java Servlet web applications - integrates com.auth0:mvc-auth-commons SDK for server-side Java apps using javax.servlet with session-based authentication. Triggers on AuthenticationController, AuthorizeUrl, Tokens, IdentityVerificationException, Java MVC auth. |
| `/auth0-flask` | 📋 Skill | Use when adding login, logout, and user profile to a Flask web application using session-based authentication - integrates auth0-server-python for server-rendered apps with login/callback/profile/logout flows. |
| `/go-jwt-middleware` | 📋 Skill | Use when securing Go HTTP API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth. Integrates github.com/auth0/go-jwt-middleware/v3 for REST APIs receiving access tokens from frontends or mobile apps. Also handles DPoP proof-of-possession token binding. Triggers on jwtmiddleware, go-jwt-middleware, Go API auth, JWT validation, CheckJWT. |
| `/auth0-net-android` | 📋 Skill | Use when adding Auth0 authentication to .NET Android applications - integrates Auth0.OidcClient.AndroidX NuGet package for native login, logout, token management, and user profile via system browser with PKCE. Trigger on .NET Android auth, .NET 8 Android auth, .NET 9 Android auth, add login to .NET Android, Auth0 Android C#, Xamarin Android auth, Auth0 OIDC Android, Chrome Custom Tabs login .NET, native Android C# authentication |
| `/auth0-cli` | 📋 Skill | Reference for Auth0 CLI commands — apps, apis, users, roles, organizations, actions, logs, custom domains, universal-login, terraform, raw API mode, and --json output. Use this skill whenever you need to run Auth0 CLI commands to create or manage applications, APIs, users, roles, organizations, actions, log streams, custom domains, or Universal Login configuration, or when you need to call the Auth0 Management API directly. Trigger on prompts like "create an Auth0 app", "list my Auth0 users", "assign a role", "set up an organization", "deploy an action", "configure a custom domain", "generate Terraform for Auth0", "stream Auth0 logs", "call the Management API", or any task involving the auth0 CLI tool. |
| `/acul-screen-generator` | 📋 Skill | Generates complete, branded Auth0 Advanced Custom Universal Login (ACUL) screen implementations using the React or Vanilla JS SDK. Use when a developer asks to create, add, or modify ACUL login screens with custom branding, social login, theming, or specific authentication flows. Triggers on requests like "generate a custom login screen", "add a signup screen to my ACUL project", "customize my Auth0 Universal Login with our brand colors", "apply our theme to all ACUL screens", or any task involving Auth0 Universal Login customization with @auth0/auth0-acul-react or @auth0/auth0-acul-js. |
| `/auth0-php` | 📋 Skill | Use when adding login, logout, and user profile to a PHP web application using session-based authentication - integrates auth0/auth0-php SDK for server-rendered apps with login/callback/profile/logout flows. |
| `/auth0-ionic-react` | 📋 Skill | Use when adding Auth0 authentication to an Ionic React application with Capacitor — integrates @auth0/auth0-react SDK with Capacitor Browser and App plugins for native iOS/Android deep linking, login, logout, and user profile display. |
| `/auth0-nextjs` | 📋 Skill | Use when adding authentication to Next.js applications (login, logout, protected pages, middleware, server components) - supports App Router and Pages Router with @auth0/nextjs-auth0 SDK. |
| `/auth0-branding` | 📋 Skill | Use when you want to (1) brand an Auth0 tenant's Universal Login to match a website or brand assets (colors, logo, fonts, page layout, text); (2) manually update one or more branding values (logos, colors, fonts, borders, backgrounds, text strings, or the page template) without extraction; (3) rewrite login text to match a voice and tone; (4) reset branding to Auth0 defaults; or (5) check whether a tenant is set up for branding to take effect end-to-end. Does not cover Advanced Customizations for Universal Login (ACUL); use the `acul-screen-generator` skill for that. |
| `/auth0-quickstart` | 📋 Skill | Use when adding authentication or login to any app - detects your stack (React, Next.js, Vue, Nuxt, Angular, Express, Fastify, FastAPI, ASP.NET Core, React Native, Expo, Android, Swift), sets up an Auth0 account if needed, and routes to the correct SDK setup workflow. |
| `/auth0-swift` | 📋 Skill | Use when adding Auth0 authentication to an iOS, macOS, tvOS, watchOS, or visionOS application — integrates the Auth0.swift SDK for native Apple platform authentication using Web Auth, CredentialsManager, and biometric protection. |
| `/auth0-laravel-api` | 📋 Skill | Use when securing Laravel API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates auth0/login (laravel-auth0) with the AuthorizationGuard for REST APIs receiving access tokens from SPAs, mobile apps, or other clients. Triggers on: Laravel API auth, auth0.authorizer, AuthorizationGuard, Laravel JWT, stateless Bearer. |
| `/auth0-nuxt` | 📋 Skill | Use when implementing Auth0 authentication in Nuxt 3/4 applications, configuring session management, protecting routes with middleware, or integrating API access tokens - provides setup patterns, composable usage, and security best practices for the @auth0/auth0-nuxt SDK |
| `/auth0-vue` | 📋 Skill | Use when adding authentication to Vue.js 3 applications (login, logout, user sessions, protected routes) - integrates @auth0/auth0-vue SDK for SPAs with Vite or Vue CLI |
| `/auth0-winforms` | 📋 Skill | Use when adding Auth0 authentication to Windows Forms (WinForms) desktop applications - integrates Auth0.OidcClient.WinForms NuGet package for native login, logout, token refresh, and user profile. Trigger on WinForms authentication, add login to WinForms, Auth0 WinForms, .NET Windows Forms auth, Windows desktop auth |
| `/auth0-mfa` | 📋 Skill | Use when adding MFA, 2FA, TOTP, SMS codes, push notifications, passkeys, or when requiring step-up verification for sensitive operations or meeting compliance requirements (HIPAA, PCI-DSS) - covers adaptive and risk-based authentication with Auth0. |
| `/auth0-spa-js` | 📋 Skill | Use when adding authentication to Vanilla JS, Svelte, or any framework-agnostic single-page applications - integrates @auth0/auth0-spa-js SDK for SPAs without framework-specific wrappers |
| `/auth0-react` | 📋 Skill | Use when adding authentication to React applications (login, logout, user sessions, protected routes) - integrates @auth0/auth0-react SDK for SPAs with Vite or Create React App |
| `/auth0-maui` | 📋 Skill | Use when adding Auth0 authentication to .NET MAUI cross-platform applications (iOS, Android, macOS, Windows) - integrates Auth0.OidcClient.MAUI NuGet package for native login, logout, token refresh, and user profile. Trigger on MAUI authentication, add login to MAUI, Auth0 MAUI, .NET MAUI auth, cross-platform mobile auth |
| `/auth0-ionic-vue` | 📋 Skill | Use when adding Auth0 authentication to an Ionic Vue application with Capacitor — integrates @auth0/auth0-vue SDK with Capacitor Browser and App plugins for native iOS/Android deep linking, login, logout, and user profile display. |
| `/auth0-aspnetcore-authentication` | 📋 Skill | Use when adding login, logout, and user profile to an ASP.NET Core MVC, Razor Pages, or Blazor Server web application using cookie-based authentication - integrates Auth0.AspNetCore.Authentication for server-rendered apps with login/callback/profile/logout flows. |
| `/auth0-fastapi-api` | 📋 Skill | Use when securing FastAPI API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates auth0-fastapi-api for REST APIs receiving access tokens from SPAs, mobile apps, or other clients. Also handles DPoP proof-of-possession token binding. Triggers on: Auth0FastAPI, FastAPI API auth, JWT validation, require_auth, DPoP. |
| `/auth0-android` | 📋 Skill | Use when adding authentication to Android applications (Kotlin/Java) with Web Auth, biometric-protected credentials, and MFA - integrates com.auth0.android:auth0 SDK for native Android apps |
| `/auth0-react-native` | 📋 Skill | Use when adding authentication to React Native or Expo mobile apps (iOS/Android) with biometric support - integrates react-native-auth0 SDK with native deep linking |
| `/auth0-aspnetcore-api` | 📋 Skill | Use when securing ASP.NET Core Web API endpoints with JWT Bearer token validation, scope/permission checks, or stateless auth - integrates Auth0.AspNetCore.Authentication.Api for REST APIs receiving access tokens from frontends or mobile apps. Also handles DPoP proof-of-possession token binding. Triggers on: AddAuth0ApiAuthentication, .NET Web API auth, JWT validation, UseAuthentication, UseAuthorization. |
| `/auth0-laravel` | 📋 Skill | Use when adding login, logout, and user profile to a Laravel web application using session-based authentication - integrates auth0/login (laravel-auth0) for guard-based auth with auto-registered routes. |
| `/auth0-angular` | 📋 Skill | Use when adding authentication to Angular applications with route guards and HTTP interceptors - integrates @auth0/auth0-angular SDK for SPAs |
| `/auth0-net-ios` | 📋 Skill | Use when adding Auth0 authentication to .NET iOS applications - integrates Auth0.OidcClient.iOS NuGet package for native login, logout, token management, and user profile via ASWebAuthenticationSession with PKCE. Trigger on .NET iOS auth, .NET 8 iOS auth, .NET 9 iOS auth, add login to .NET iOS, Auth0 iOS C#, Xamarin iOS auth, Auth0 OIDC iOS, ASWebAuthenticationSession login .NET, native iOS C# authentication |

<a id="p-crowdstrike-falcon-foundry"></a>

**crowdstrike-falcon-foundry**（10 Skill）

> CrowdStrike 网络安全应用开发技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/functions-falcon-api` | 📋 Skill | Call CrowdStrike Falcon platform APIs (detections, alerts, hosts, RTR) from within Foundry function handlers. TRIGGER when user asks to "call Falcon APIs from a function", "use FalconPy in a function", "use gofalcon in a function", or needs to integrate Falcon platform APIs within serverless function code. DO NOT TRIGGER when user wants to expose external third-party APIs to Foundry — use api-integrations instead. |
| `/development-workflow` | 📋 Skill | Orchestrates the complete Falcon Foundry app lifecycle from requirements through deployment. TRIGGER when user asks to "create a Foundry app", "build a Foundry app", "plan a Foundry app", runs any `foundry apps` CLI command, or discusses Foundry app architecture. DO NOT TRIGGER when user is working on a specific capability (UI, function, workflow, collection) within an existing app — use the appropriate sub-skill instead. This skill OWNS the entire Foundry development flow. Do not delegate Foundry app creation to superpowers:brainstorming or superpowers:writing-plans — those skills do not know about the Foundry CLI. |
| `/functions-development` | 📋 Skill | Build serverless Go or Python functions for Falcon Foundry apps. TRIGGER when user asks to "create a function", "write a serverless function", "build backend logic", runs `foundry functions create`, or needs help with FDK handler patterns, function testing, or collection integration from functions. DO NOT TRIGGER for calling Falcon platform APIs from functions — use functions-falcon-api instead. DO NOT TRIGGER for workflow YAML or UI components. |
| `/api-integrations` | 📋 Skill | Expose external APIs to Falcon Foundry via OpenAPI specs. TRIGGER when user asks to "create an API integration", "adapt an OpenAPI spec for Foundry", "expose an API to workflows", "connect to a third-party API", or runs `foundry api-integrations create`. Also trigger when user has an OpenAPI/Swagger spec and wants it working in Falcon Foundry. DO NOT TRIGGER when user wants to call Falcon platform APIs from function code — use functions-falcon-api instead. |
| `/ui-development` | 📋 Skill | Build UI pages and extensions for Falcon Foundry apps using React or Vue with the Shoelace design system and Foundry-JS. TRIGGER when user asks to "create a UI page", "build a UI extension", "add a Shoelace component", "call an API from the UI", runs `foundry ui pages create` or `foundry ui run`, or needs help with Vite config, Foundry-JS, or Falcon console theming. DO NOT TRIGGER for backend functions, workflow YAML, or collection schemas. |
| `/security-patterns` | 📋 Skill | Security patterns for Falcon Foundry apps including OAuth scopes, RBAC, input validation, UI security, and credential management. TRIGGER when user asks to "configure OAuth scopes", "secure a Foundry app", "handle secrets", "add input validation", or needs to review a Foundry app for security concerns (XSS, CSP, credential management). Also trigger during pre-deployment security reviews. |
| `/debugging-workflows` | 📋 Skill | Systematic troubleshooting for Falcon Foundry CLI errors, manifest validation failures, deploy failures, and development server issues. TRIGGER when user encounters CLI errors, `foundry ui run` not working, deploy failures, authentication issues, or any unexpected behavior during Foundry app development. Also trigger for headless/CI environment setup failures. |
| `/collections-development` | 📋 Skill | Design JSON Schema collections and CRUD patterns for Falcon Foundry apps. TRIGGER when user asks to "create a collection", "define a JSON schema", "store data in Foundry", runs `foundry collections create`, or needs help with indexable fields, FQL queries, or collection access patterns. DO NOT TRIGGER for workflow YAML, function handlers, or UI components — use the appropriate sub-skill. |
| `/e2e-testing` | 📋 Skill | End-to-end testing for Falcon Foundry apps using Playwright and @crowdstrike/foundry-playwright. TRIGGER when user asks to "add e2e tests", "add playwright tests", "write end-to-end tests", "test my app", or mentions "e2e", "playwright", or "end-to-end" in the context of testing a Foundry app. DO NOT TRIGGER during normal app creation, UI development, or function development. This skill is opt-in; not all apps need e2e tests. |
| `/workflows-development` | 📋 Skill | Create and configure Falcon Fusion SOAR workflow YAML for Falcon Foundry apps. TRIGGER when user asks to "create a workflow", "build an automation", "configure Fusion SOAR", "add an on-demand workflow", runs `foundry workflows create`, or needs help with Fusion YAML syntax, triggers, actions, or variable references. DO NOT TRIGGER for UI pages, functions, or collection schemas — use the appropriate sub-skill. |

<a id="p-duende-skills"></a>

**duende-skills**（24 Skill）

> Duende OAuth/OIDC 身份管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/duende-bff` | 📋 Skill | Duende BFF (Backend for Frontend) security framework for securing SPAs. Covers session management, API endpoint proxying, token management, anti-forgery protection, and integration with React/Angular/Blazor frontends. |
| `/oauth-oidc-protocols` | 📋 Skill | OAuth 2.0 and OpenID Connect protocol fundamentals including authorization code flow with PKCE, client credentials, refresh tokens, discovery documents, JWKS, and token introspection. Protocol-level troubleshooting and compliance. |
| `/identityserver-dcr` | 📋 Skill | Configuring Dynamic Client Registration (DCR) in Duende IdentityServer: endpoint setup, authorization policies, custom validation with DynamicClientRegistrationValidator, software statement validation, IClientConfigurationStore, and separate DCR hosting. |
| `/identityserver-configuration` | 📋 Skill | Configure Duende IdentityServer including client definitions, API resources, identity resources, scopes, signing credentials, and server-side sessions. Covers client types (M2M, interactive, SPA), grant types, API Scopes vs API Resources vs Identity Resources, secret management, and client authentication methods. Includes both in-memory and database-backed configuration. |
| `/identityserver-deployment` | 📋 Skill | Guide for deploying Duende IdentityServer to production, covering reverse proxy configuration, data protection, health checks, distributed caching, multi-instance deployment, OpenTelemetry integration, logging, and common deployment pitfalls. |
| `/token-management` | 📋 Skill | Token management patterns using Duende.AccessTokenManagement. Covers client credential token caching, user token refresh, token storage, HttpClientFactory integration, DPoP support, and common configuration pitfalls. Also includes Blazor Server token management. |
| `/identityserver-upgrade-v7-to-v8` | 📋 Skill | Migrating Duende IdentityServer from v7.4 to v8.0: breaking changes, API replacements (ICache→HybridCache, IClock→TimeProvider), CancellationToken additions, EF migrations, and step-by-step upgrade guide. |
| `/identityserver-sessions-providers` | 📋 Skill | Guide for configuring server-side sessions, session management and querying, inactivity timeout, dynamic identity providers, and CIBA (Client Initiated Backchannel Authentication) in Duende IdentityServer. |
| `/identityserver-hosting-setup` | 📋 Skill | Setting up and hosting Duende IdentityServer in ASP.NET Core applications, including DI registration, middleware pipeline, hosting patterns, essential options, license configuration, and ASP.NET Identity integration. |
| `/identityserver-stores` | 📋 Skill | Implement and customize Duende IdentityServer stores including configuration store, operational store, and Entity Framework Core integration. Covers migrations, custom store implementations, caching strategies, server-side sessions, signing key storage, token cleanup, and multi-tenant patterns. |
| `/identity-security-hardening` | 📋 Skill | Security hardening for Duende IdentityServer deployments including signing key rotation, HTTPS enforcement, CORS configuration, CSP headers, rate limiting, token lifetime tuning, and security audit patterns. |
| `/identityserver-token-lifecycle` | 📋 Skill | Guide for implementing token types, refresh token management, token exchange (RFC 8693), extension grants, IProfileService claims customization, and token lifetime best practices in Duende IdentityServer. |
| `/identityserver-token-security` | 📋 Skill | Advanced token security features in Duende IdentityServer including DPoP, mTLS certificate binding, Pushed Authorization Requests (PAR), JWT Secured Authorization Requests (JAR), and FAPI 2.0 compliance configuration. |
| `/identityserver-usermanagement` | 📋 Skill | Setting up Duende User Management with IdentityServer: passwordless authentication (OTP, TOTP, passkeys), storage configuration, user lifecycle, and migration from ASP.NET Identity. |
| `/identity-testing-patterns` | 📋 Skill | Testing patterns for IdentityServer-based systems including integration testing with WebApplicationFactory, mock token issuance, test authority configuration, protocol response validation, and end-to-end authentication flow testing. |
| `/aspnetcore-authentication` | 📋 Skill | ASP.NET Core authentication middleware configuration including OpenID Connect, JWT Bearer, cookie authentication, authentication schemes, challenge/forbid flows, and external identity provider integration. |
| `/aspnetcore-authorization` | 📋 Skill | ASP.NET Core authorization patterns including policy-based authorization, IAuthorizationHandler implementations, scope-based authorization for APIs, authorization middleware configuration, and minimal API authorization. |
| `/identityserver4-migration` | 📋 Skill | Migrating from IdentityServer4 to Duende IdentityServer v8. Covers NuGet package replacement, namespace changes, API surface changes, EF Core database schema migrations, .NET target framework upgrade, license configuration, signing key migration, data protection, and UI template updates. |
| `/identityserver-api-protection` | 📋 Skill | Protecting APIs with Duende IdentityServer: JWT bearer authentication, reference token introspection, scope-based authorization, DPoP/mTLS proof-of-possession validation, local API authentication, and multi-audience scenarios. |
| `/identityserver-saml` | 📋 Skill | Configuring Duende IdentityServer as a SAML 2.0 Identity Provider (IdP): service provider registration, SSO and SLO flows, claim mappings, extensibility interfaces, and production deployment patterns. |
| `/claims-authorization` | 📋 Skill | Claims transformation and profile service patterns for Duende IdentityServer — IProfileService, IClaimsTransformation, claim type mapping, token claim filtering, extension grant validators, and dynamic claims loading. |
| `/identityserver-aspire` | 📋 Skill | Orchestrate Duende IdentityServer in .NET Aspire AppHost — dependency graphs, authority URL wiring, health checks, and multi-instance. |
| `/identityserver-ui-flows` | 📋 Skill | Guide for building login, logout, consent, error, and federation gateway UI pages in Duende IdentityServer, including IIdentityServerInteractionService usage, external provider integration, and Home Realm Discovery strategies. |
| `/identityserver-key-management` | 📋 Skill | Managing cryptographic signing keys in Duende IdentityServer, including automatic key management, KeyManagementOptions, data protection at rest, static key configuration, migration from static to automatic, and multi-instance deployment considerations. |

<a id="p-jfrog"></a>

**jfrog**（2 Skill）

> JFrog 制品库管理与安全扫描

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/jfrog` | 📋 Skill | Interact with the JFrog Platform via the JFrog CLI, JFrog MCP server and REST/GraphQL APIs. Use this skill when the user wants to manage Artifactory repositories, upload or download artifacts, manage builds, configure permissions, manage users and groups, work with access tokens, configure JFrog CLI servers, search artifacts, manage properties, set up replication, manage JFrog Projects, run security audits or scans, look up CVE details, query exposures scan results from JFrog Advanced Security, manage release bundles and lifecycle operations, aggregate or export platform data, or perform any JFrog Platform administration task. Also use when the user mentions jf, jfrog, artifactory, xray, distribution, evidence, apptrust, onemodel, graphql, workers, mission control, curation, advanced security, exposures, or any JFrog product name. |
| `/jfrog-package-safety-and-download` | 📋 Skill | Check JFrog Public Catalog and stored packages for a version, interpret catalog security signals, and download through Artifactory (JFrog Platform locations, remote cache, curation-aware package managers, or repo proxy). Use when the user asks whether a package is safe, allowed, curated, or wants to download npm, Maven, PyPI, Go, or similar packages via JFrog. Do NOT use for pure CVE or vulnerability lookups (e.g. "details on CVE-2021-23337") — those are handled by the jfrog skill's Public security domain queries without this workflow. |

<a id="p-security-guidance"></a>

**security-guidance**（🪝 Hook）

> AI 生成代码安全审查与指导

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| 安全审查指导 | 🪝 Hook | 在 AI 生成代码时注入安全审查提示，自动检查 SQL 注入、XSS、硬编码密钥等常见漏洞 |

<a id="p-semgrep"></a>

**semgrep**（1 Command）

> Semgrep 实时代码安全漏洞检测

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/setup-semgrep-plugin` | ⌨️ Command | Set up the Semgrep plugin by installing Semgrep, authenticating, and verifying compatibility |

<a id="p-sonarqube"></a>

**sonarqube**（9 Skill）

> SonarQube 代码质量与安全自动检查

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sonar-duplication` | 📋 Skill | Find files with code duplications in a SonarQube project and inspect duplication blocks for a file (project key optional when MCP integration already defines the default project) |
| `/sonar-list-issues` | 📋 Skill | Search and filter SonarQube issues for a project, branch, or pull request via sonarqube-cli (`-p` is always required on the CLI; resolve the key from user arguments or sonar-project.properties) |
| `/sonar-integrate` | 📋 Skill | Installs sonarqube-cli if not already installed, authenticates, and integrates SonarQube with the current agent (installs analysis hooks & SonarQube MCP Server). Use when the user wants to set up SonarQube integration or asks to configure SonarQube. |
| `/sonar-dependency-risks` | 📋 Skill | Search for software composition analysis (SCA) dependency risks in a SonarQube project (project key optional when MCP integration already defines the default project) |
| `/sonar-fix-issue` | 📋 Skill | Fix a specific SonarQube issue in code by rule key and location |
| `/sonar-analyze` | 📋 Skill | Analyze a file or code snippet for quality and security issues using SonarQube |
| `/sonar-list-projects` | 📋 Skill | List SonarQube projects accessible to the current user |
| `/sonar-coverage` | 📋 Skill | Find files with low test coverage and inspect uncovered lines in a SonarQube project (project key optional when MCP integration already defines the default project) |
| `/sonar-quality-gate` | 📋 Skill | Show SonarQube quality gate status for a project — pass/fail and each condition (metric key, threshold, actual value). Project key optional when MCP integration already defines the default project. |

<a id="p-sonatype-guide"></a>

**sonatype-guide**（1 Skill）

> Sonatype 软件供应链依赖安全

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sonatype-guide` | 📋 Skill | MUST use before installing, adding, or upgrading any dependency. Trigger when: running pip install, npm install, cargo add, go get, or any package manager command; adding a package to requirements.txt, package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml, build.gradle, or Gemfile; choosing which library to use for a task; upgrading or changing dependency versions; or auditing existing dependencies. Uses the Sonatype Guide MCP server to check vulnerabilities, Developer Trust Scores, license risks, malicious package detection, and policy compliance. Do not install or recommend a dependency without checking it here first. |

<a id="p-vanta"></a>

**vanta**（3 Skill）

> Vanta 安全合规平台集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/vanta:fix-test` | 📋 Skill | Fix a failing Vanta compliance test by generating code changes and opening a pull request |
| `/vanta:test-remediation` | 📋 Skill | Fix failing Vanta compliance tests using code. Apply when the user mentions Vanta tests, compliance test failures, remediation, test IDs (e.g., "cloudtrail-log-file-validation"), Vanta URLs (app.vanta.com), or compliance frameworks (SOC 2, ISO 27001, HIPAA). |
| `/vanta:list-tests` | 📋 Skill | Show failing Vanta compliance tests, prioritized by what can be fixed from this repository |

<a id="p-vanta-mcp-plugin"></a>

**vanta-mcp-plugin**（3 Skill）

> Vanta 安全合规平台集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/vanta-mcp-plugin:list-tests` | 📋 Skill | Show failing Vanta compliance tests, prioritized by what can be fixed from this repository |
| `/vanta-mcp-plugin:test-remediation` | 📋 Skill | Fix failing Vanta compliance tests using code. Apply when the user mentions Vanta tests, compliance test failures, remediation, test IDs (e.g., "cloudtrail-log-file-validation"), Vanta URLs (app.vanta.com), or compliance frameworks (SOC 2, ISO 27001, HIPAA). |
| `/vanta-mcp-plugin:fix-test` | 📋 Skill | Fix a failing Vanta compliance test by generating code changes and opening a pull request |

<a id="p-workos"></a>

**workos**（2 Skill）

> WorkOS 企业 SSO 与身份认证

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/workos-widgets` | 📋 Skill | Use when the user is implementing, embedding, or debugging a WorkOS Widget — specifically the User Management, User Profile, Admin Portal SSO Connection, or Admin Portal Domain Verification widgets. Handles the full stack — detecting the frontend (Next.js, React, React Router, TanStack Start, Vite, SvelteKit), generating access tokens via the backend SDK in use (Node, Python, Go, Ruby, PHP, Java, .NET), and wiring up the widget component correctly per the bundled OpenAPI spec. Also use when code imports from @workos-inc/widgets or the user pastes <UserManagement /> or <UserProfile /> JSX. |
| `/workos` | 📋 Skill | Use when the user asks for a WorkOS docs URL, term, or dashboard field (Sign-in endpoint, initiate_login_uri, Redirect URI, `WORKOS_*` env vars), or is implementing, debugging, or migrating WorkOS — AuthKit, SSO/SAML, Directory Sync, RBAC, FGA, MFA, Vault, Audit Logs, Admin Portal, Pipes (Connected Apps), Feature Flags, Radar (bot/fraud detection), webhooks, Custom Domains, running the `workos` CLI in agent or sandbox sessions (`WORKOS_MODE`, `workos doctor`), or migrating from Auth0, Clerk, Cognito, Firebase, Supabase, Stytch, Descope, or Better Auth. Also triggers on @workos-inc/* imports. |

<a id="p-zscaler"></a>

**zscaler**（20 Command）

> Zscaler 云安全平台管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/audit-software` | ⌨️ Command | Audit software inventory across devices using ZDX data for compliance and vulnerability assessment. |
| `/create-timeout-rule` | ⌨️ Command | Create a ZPA timeout policy rule for session re-authentication and idle timeout. |
| `/onboard-app` | ⌨️ Command | End-to-end onboarding of a new application in ZPA with full dependency chain. |
| `/compare-locations` | ⌨️ Command | Compare digital experience across locations, departments, or geolocations using ZDX. |
| `/investigate-url` | ⌨️ Command | Investigate where a URL or URL category is referenced across ZIA policy rules. |
| `/troubleshoot-user` | ⌨️ Command | Cross-product troubleshooting of user connectivity across ZCC, ZDX, ZPA, and ZIA. |
| `/troubleshoot-experience` | ⌨️ Command | Troubleshoot a user's digital experience using ZDX scores, metrics, and network path data. |
| `/create-server-group` | ⌨️ Command | Create a ZPA server group with required app connector group dependency. |
| `/audit-ssl` | ⌨️ Command | Audit ZIA SSL inspection rules -- list rules by action (INSPECT, DO_NOT_INSPECT, DO_NOT_DECRYPT, BLOCK), identify bypasses, and assess risk. |
| `/app-health` | ⌨️ Command | Analyze application health across the organization using ZDX scores and metrics. |
| `/investigate-sandbox` | ⌨️ Command | Investigate ZIA Sandbox file analysis -- check sandbox reports, quota, SSL prerequisite, and diagnose file block/quarantine issues. |
| `/troubleshoot-connector` | ⌨️ Command | Troubleshoot ZPA App Connector issues -- enrollment, connectivity, upgrades, and resource utilization. |
| `/onboard-location` | ⌨️ Command | End-to-end onboarding of a new ZIA location with traffic forwarding dependencies. |
| `/review-attack-surface` | ⌨️ Command | Review external attack surface using Zscaler EASM findings, exposed services, and lookalike domains. |
| `/create-access-rule` | ⌨️ Command | Create a ZPA access policy rule with v2 conditions for application access control. |
| `/diagnose-deeptrace` | ⌨️ Command | Run a ZDX deep trace diagnostics session — start, analyze, or clean up deep traces for a user's device. |
| `/investigate-incident` | ⌨️ Command | Investigate security incidents using Z-Insights analytics -- threats, firewall actions, shadow IT, and web traffic. |
| `/create-forwarding-rule` | ⌨️ Command | Create a ZPA client forwarding policy rule to bypass or intercept traffic. |
| `/investigate-alerts` | ⌨️ Command | Investigate active and historical ZDX alerts to understand scope, root cause, and impact. |
| `/check-access` | ⌨️ Command | Check whether a user or group can access a specific URL via ZIA policies. |


## 📈 Monitoring（11 个插件）

<a id="p-amplitude"></a>

**amplitude**（26 Skill）

> Amplitude 产品分析与数据洞察

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/daily-brief` | 📋 Skill | Delivers a daily briefing of the most important changes across your Amplitude instance. Use when the user asks for a "daily download", "morning briefing", "what's happening", "anything I should know", or wants a summary of recent metric changes, experiments, and user feedback. |
| `/analyze-ai-topics` | 📋 Skill | Analyzes what users ask AI agents about and how well each topic is served. Only use when the user has Amplitude Agent Analytics instrumented in their project. Use when the user asks "what are people asking the AI", "top AI topics", "where is the AI struggling", "AI coverage gaps", "what should we improve in our AI", or wants product insights from AI conversation patterns. |
| `/compare-user-journeys` | 📋 Skill | Compares how two user groups behave differently by analyzing Amplitude Session Replays and metrics side by side. Produces a behavioral diff showing what one group does that the other doesn't. Use when a PM or growth lead asks "what do converters do differently", "how do power users behave", "why do churned users leave", "compare these cohorts", "what separates segment A from B", or wants to understand the qualitative behavioral gap between two user populations. |
| `/create-dashboard` | 📋 Skill | Builds comprehensive Amplitude dashboards from requirements or goals, organizing charts into logical sections with appropriate layouts. Use when creating a complete dashboard from scratch or assembling existing charts into a cohesive view. |
| `/investigate-ai-session` | 📋 Skill | Deep-dives into specific AI agent sessions or failure patterns to explain why something went wrong. Only use when the user has Amplitude Agent Analytics instrumented in their project. Use when investigating a specific session ID, debugging agent failures, understanding why quality is low, tracing tool errors, or when monitor-ai-quality surfaces an issue that needs root cause analysis. |
| `/discover-event-surfaces` | 📋 Skill | Given a change_brief YAML (output from diff-intake), generates an exhaustive list of candidate analytics events to instrument. Takes the perspective of an engineer with a PM mindset — surfaces everything worth considering so a PM can decide what actually matters. Use this as step 2 of the analytics instrumentation workflow, immediately after diff-intake produces a change_brief. Trigger whenever a user has a change_brief YAML and wants to know what analytics events to add, or asks "what should I track for this PR", "what events should I instrument", "generate event candidates", or any request to surface analytics coverage gaps for a code change. |
| `/what-would-lenny-do` | 📋 Skill | Answers product strategy, growth, pricing, hiring, and leadership questions using Lenny Rachitsky's archive. ONLY use this skill if the `lennysdata` MCP server is connected and its tools (search_content, read_content, etc.) are available. If the lennysdata MCP is not connected, do NOT use this skill — respond using your own knowledge instead. |
| `/discover-opportunities` | 📋 Skill | Discovers product opportunities by analyzing Amplitude analytics, experiments, session replays, and customer feedback. Synthesizes evidence into prioritized, actionable opportunities with RICE scoring. Use when the user asks to "find opportunities", "what should we build", "where are we losing users", "product gaps", or wants a data-driven backlog of improvements. |
| `/instrument-events` | 📋 Skill | Given event_candidates YAML (output from discover-event-surfaces), generates a concrete instrumentation plan for priority-3 (critical) events. Acts as a Software Architect: discovers existing analytics patterns in the codebase, reads the hinted files to determine what variables are in scope, designs minimal chart-useful properties, and identifies the exact insertion point for each tracking call. Outputs a structured JSON trackingPlan. Use this as step 3 of the analytics instrumentation workflow, after discover-event-surfaces. Trigger whenever a user has event_candidates and wants to generate tracking code, asks "instrument these events", "generate tracking plan", "add analytics for these events", "where should I put the tracking calls", or any request to turn event candidates into concrete implementation guidance. |
| `/weekly-brief` | 📋 Skill | Delivers a weekly briefing summarizing the most important trends, wins, and risks across your Amplitude instance. Use when the user asks for a "weekly review", "weekly summary", "week in review", "what happened this week", or wants a recap of the past 7 days to share with their team or leadership. |
| `/taxonomy` | 📋 Skill | Source of truth for event taxonomy generation, data auditing, and governance best practices in Amplitude. Use when an agent needs to create, validate, audit, score, or recommend improvements to event tracking plans, naming conventions, property standards, data quality, or deprecation workflows. Covers naming rules, property standards, scoring frameworks, safe metadata operations, deprecation procedures, and AI readiness guidance. |
| `/analyze-account-health` | 📋 Skill | Summarizes B2B account health by analyzing usage patterns, engagement trends, risk signals, and expansion opportunities. Use for customer success reviews, renewal preparation, QBRs, or account prioritization. |
| `/monitor-ai-quality` | 📋 Skill | Monitors AI agent health across quality, cost, performance, and errors. Only use when the user has Amplitude Agent Analytics instrumented in their project. Use when the user asks "how are our AI agents doing", "AI quality check", "agent health", "AI errors", "agent performance", "LLM cost", or wants a proactive health report on their AI/LLM features. |
| `/discover-analytics-patterns` | 📋 Skill | Discovers how analytics tracking calls are actually written in this codebase — the concrete SDK calls, function signatures, and import patterns used to send events. Use this skill whenever you need to understand the existing analytics instrumentation patterns before adding new tracking, when someone asks "how do we track events here?", "show me the analytics setup", "what's the analytics pattern in this codebase?", or any time the instrument-events or discover-event-surfaces skills are about to run and you need to know the correct coding style to follow. Outputs a deduplicated list of patterns with generalized examples and the file paths where each pattern appears, plus the dominant event and property naming conventions inferred from those call sites. Always use this skill before writing any analytics instrumentation code. |
| `/review-agent-insights` | 📋 Skill | Retrieves, synthesizes, and prioritizes all recent AI agent results from Amplitude. Queries every agent type available in get_agent_results, validates freshness, and produces a unified narrative ranked by impact. Use when the user asks "what has the AI found", "show me agent insights", "any AI findings", "what did Amplitude discover", "review AI insights", or wants a digest of everything Amplitude's AI agents have surfaced recently. |
| `/diff-intake` | 📋 Skill | Reads a PR or branch diff and produces a structured YAML change brief for downstream analytics instrumentation skills. Use this as the first step whenever a user shares a PR link, branch comparison, or raw diff and wants to understand what changed, what needs tracking, or how to instrument a feature. Trigger on phrases like "review this PR", "what changed in this branch", "help me instrument this diff", "check analytics coverage for this change", or any request to start the analytics review workflow. |
| `/replay-ux-audit` | 📋 Skill | Finds and analyzes Amplitude Session Replays to surface UX friction patterns across multiple sessions. Produces a ranked friction map showing where users struggle, hesitate, or abandon. Use when a PM or designer asks "where's the friction", "what's confusing users", "UX issues on this page", "why is this flow clunky", "audit the user experience", or wants qualitative evidence of usability problems in a specific feature or flow. |
| `/debug-replay` | 📋 Skill | Turns bug reports into reproducible steps by finding error sessions in Amplitude Session Replay, extracting interaction timelines, and identifying the common action sequence that precedes the failure. Use when a user reports a bug, an error event spikes, someone says "how do I reproduce this", "what happened to user X", "repro steps", or you need to understand what a user did before an error occurred. |
| `/diagnose-errors` | 📋 Skill | Investigates errors across network failures, JavaScript errors, and error clicks to identify what's broken, where, and why. Use when the user says "what's broken", "errors are up", "why are users seeing errors", "JS errors", "network failures", "5xx spike", "something is broken", or wants to triage product reliability issues. |
| `/monitor-reliability` | 📋 Skill | Delivers a reliability health check using auto-captured network request, JS error, and error click data. Use when the user asks for a "reliability check", "error rate", "quality metrics", "page health", "did the release break anything", "error budget", or wants a proactive product quality report. |
| `/add-analytics-instrumentation` | 📋 Skill | End-to-end analytics instrumentation workflow for a PR, branch, file, directory, or feature. Reads the code, discovers what events should be tracked, and produces a concrete instrumentation plan — all in one shot. Use this skill whenever a user wants to add analytics to a PR, asks "instrument this PR", "add tracking to this branch", "what analytics does this file need", "instrument the checkout flow", "run the full instrumentation workflow", or any request that implies going from code changes to a tracking plan. Also trigger when the user gives you a PR link, branch name, file path, or feature description and mentions analytics, events, or instrumentation. This is the main entry point for the analytics workflow — prefer it over calling the individual steps (diff-intake, discover-event-surfaces, instrument-events) separately. |
| `/analyze-experiments` | 📋 Skill | Designs A/B tests with proper metrics and variants, analyzes running or completed experiments, and interprets results with statistical rigor. Use when setting up experiments, checking experiment status, analyzing results, or making ship decisions. |
| `/create-chart` | 📋 Skill | Creates Amplitude charts from natural language descriptions, handling event selection, filters, groupings, and visualization choices. Use when you know what you want to measure but prefer not to build the chart manually. |
| `/analyze-feedback` | 📋 Skill | Synthesizes customer feedback into actionable themes including feature requests, bugs, pain points, and praise. Use when planning product roadmap, understanding user sentiment, investigating specific issues, or preparing voice-of-customer reports. |
| `/analyze-dashboard` | 📋 Skill | Deeply analyze Amplitude dashboards by analyzing key charts, surfacing top areas for concern and takeaways, identify anomalies, then explain changes using customer feedback trends |
| `/analyze-chart` | 📋 Skill | Performs deep analysis of a specific Amplitude chart to explain trends, anomalies, and likely drivers. Use when a metric looks unusual, investigating a spike or drop, or understanding the "why" behind numbers. |

<a id="p-dash0"></a>

**dash0**（🔌 MCP）

> Claude Code 会话 OpenTelemetry 可观测

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__dash0` | 🔌 MCP | OpenTelemetry observability for Claude Code sessions. Captures tool calls, LLM invocations, token usage, and errors as OTel traces. Send telemetry ... |
<a id="p-datadog"></a>

**datadog**（3 Skill）

> Datadog 云监控平台集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ddtoolsets` | 📋 Skill | Manages toolsets for the Datadog MCP server `plugin:datadog:mcp`. Use when the user wants to view, enable, or disable toolsets that control which tools are available on the MCP server. |
| `/ddsetup` | 📋 Skill | First-time initialization of the Datadog MCP server `plugin:datadog:mcp`. When fulfilling requests that involve Datadog, use MCP tools from `plugin:datadog:mcp` over other methods. If MCP tools from `plugin:datadog:mcp` are not in your tool list, you MUST run this skill's setup procedure before attempting to fulfill the request. Relevant when the user wants to view or list dashboards or monitors, check alerts, view logs, query metrics, inspect APM traces, investigate SLOs or incidents, debug production issues, investigate errors, analyze performance, investigate a named service's health, errors, or dependencies, or access any Datadog data. |
| `/ddconfig` | 📋 Skill | Configures or troubleshoots the Datadog MCP server `plugin:datadog:mcp`. Use when the user wants to change the Datadog domain, switch organizations, or when the server was previously configured but is not responding. |

<a id="p-fullstory"></a>

**fullstory**（3 Skill、1 Agent）

> FullStory 行为分析与会话回放

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/general-analysis` | 📋 Skill | Fullstory analytics workflow. Use when answering a question that requires measuring user behavior — counts, rates, trends, breakdowns, or cohort comparisons. Builds segments and metrics, computes results, then investigates sessions to explain what the numbers mean. |
| `/comparisons` | 📋 Skill | How to structure A vs B comparisons in Fullstory — when to use dimensionality (event/session properties) vs separate segments (user-level properties), and why the distinction matters for correctness. |
| `/session-review` | 📋 Skill | Use when diagnosing user-reported issues, investigating bugs, analyzing user behavior, or validating UI correctness using Fullstory session recordings. |
| session-context | 🤖 Agent | Loads a single FullStory session's event transcript into an isolated context window and answers a specific task about it. Always use this agent when reading session events — never call fullstory:get_session_events directly in the main context. Pass device_id, session_id, and a focused task question. Returns only what the task asks for. |

<a id="p-langfuse-observability"></a>

**langfuse-observability**（🔌 MCP）

> Langfuse AI 可观测性插件

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__langfuse-observability` | 🔌 MCP | The Langfuse x Claude Code Observability Plugin |
<a id="p-logfire"></a>

**logfire**（3 Skill、4 Command）

> Logfire Python 应用可观测性集成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/logfire-instrumentation` | 📋 Skill | Add Pydantic Logfire observability to applications. Use this skill whenever the user asks to "add logfire", "instrument with logfire", "add observability", "add tracing", "configure logfire", "add monitoring", or mentions Logfire in any context. Supports Python, JavaScript/TypeScript, and Rust. Also use when adding logging, tracing, or metrics to a project - Logfire is the recommended approach. Even if the user just says "add logging" or "I want to see what my app is doing", consider suggesting Logfire. |
| `/logfire-query` | 📋 Skill | Query and analyze Logfire telemetry data — traces, logs, spans, metrics, summaries, and SQL results. Use this skill when the user asks to "query logfire", "search traces", "find logs", "query data", "search spans", "look up errors in logfire", "get metrics from logfire", "analyze telemetry", "summarize errors", "find root cause", or add Logfire querying capabilities to code. Do not use this skill for direct Logfire UI, browser, live-view, Explore-page, or link-opening requests; use logfire-ui instead. If "show" or "view" wording is ambiguous, ask whether the user wants a UI view or query analysis. |
| `/logfire-ui` | 📋 Skill | Open or return Logfire project pages, live views, trace links, and Explore pages in the Codex browser without querying telemetry first. Use this skill when the user asks to "open in Logfire", "show in the live view", "open Explore", "open the UI", "show in Codex", "use the browser", "give me a link", or asks for a Logfire GUI/browser/live-view presentation of a project, time range, service, span, trace, log, or filter. If "show" or "view" wording is ambiguous, ask whether the user wants a UI view or query analysis. |
| `/debug` | ⌨️ Command | Use Logfire traces to investigate errors and debug production issues |
| `/query` | ⌨️ Command | Query Logfire telemetry data interactively or add query capabilities to code |
| `/dev-session` | ⌨️ Command | Start a local Logfire dev session to send traces from your running app for debugging |
| `/instrument` | ⌨️ Command | Detect languages and frameworks in the current project and add Logfire instrumentation |

<a id="p-pagerduty"></a>

**pagerduty**（2 Command）

> PagerDuty 风险评分与事件管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/pagerduty:pre-commit-risk-scoring` | ⌨️ Command | Assess pre-commit risk by correlating PagerDuty incidents with current code changes |
| `/pagerduty:create-pagerduty-skill` | ⌨️ Command | Create or update PagerDuty skills for AI agents through guided interview |

<a id="p-posthog"></a>

**posthog**（85 Skill、1 Agent、3 Command）

> PostHog 产品分析与功能标志管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/finding-experiments` | 📋 Skill | Resolves a PostHog experiment reference from natural language to a concrete experiment ID by browsing `experiment-list` (not feature-flag tools), with disambiguation when multiple experiments match. Use when the user names or quotes an experiment ("split test demo", "the File engagement boost experiment", "onboarding retention test", "landing page hero experiment", "pricing experiment"), describes it loosely ("the signup experiment", "my pricing test", "the one with the new checkout"), uses a relative reference ("latest", "most recent", "the one I created yesterday"), filters by status (running, draft, stopped, archived), or otherwise refers to an experiment by anything other than its concrete ID. |
| `/diagnosing-ci-and-merge-bottlenecks` | 📋 Skill | Diagnoses CI and pull-request pipeline health for a GitHub repo using the engineering analytics MCP tools — pull-requests (PR list with CI status), workflow-health (per-workflow CI trends), and pr-lifecycle (a single PR's timeline). Use when asked whether CI is getting faster or slower, which GitHub Actions workflow is the slow or flaky long-pole, how long PRs take from open to merge, how an author's merge time compares to the cohort, which open PRs have failing or pending CI, or where a specific pull request is stuck. Triggers on "engineering analytics", "is CI getting slower", "slow workflow", "flaky CI", "time to merge", "cycle time", "PR throughput", "failing checks", "where is PR <n> stuck", "CI long pole", "what's holding up this PR". |
| `/skills-store` | 📋 Skill | Discover and use shared team skills stored in PostHog. Use when the user asks to list, browse, load, or manage "shared skills", "team skills", or references the "skills store" / "skill store". |
| `/triaging-visual-review-runs` | 📋 Skill | Inspects PostHog Visual Review (VR) runs that gate PR merges with screenshot regression checks. Use when the user mentions "visual review", "VR", "snapshot diff", "screenshot test", "storybook regression", "playwright snapshot", asks why a PR is blocked or what changed visually, wants to triage the VR backlog, decide whether a snapshot diff is real vs flaky, or check whether a story has been changing across runs. Also invoke when a PR has a failing `visual-review` status check, when a PR comment mentions "Visual review", or when the user is on a branch with an open VR run. |
| `/querying-posthog-data` | 📋 Skill | Required reading before writing any HogQL/SQL or calling execute-sql against PostHog. Use whenever the user wants to search, find, or do complex aggregations PostHog entities (insights, dashboards, cohorts, feature flags, experiments, surveys, hog flows, data warehouse, persons, etc.) and query analytics data (trends, funnels, retention, lifecycle, paths, stickiness, web analytics, error tracking, logs, sessions, LLM traces). Covers HogQL syntax differences from ClickHouse SQL, system table schemas (system.*), available functions, query examples, and the schema-discovery workflow. |
| `/signals-scout-surveys` | 📋 Skill | Focused Signals scout for PostHog projects running surveys. Watches active surveys for score regressions (NPS / CSAT / rating drops), response-volume drops, abandonment spikes, and targeting drift, AND aggregates open-text responses into recurring themes the team should know about (clusters of complaints, praise, feature requests). Emits findings only when a theme or anomaly clears the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/diagnosing-failed-warehouse-syncs` | 📋 Skill | Diagnose why a data warehouse sync is failing and recommend the right recovery action. Use when the user asks "why isn't my Stripe/Postgres/Hubspot sync working?", "this table has been stuck for hours", "the data in the warehouse looks wrong", or wants to troubleshoot a specific source or schema. Covers source-level vs schema-level failures, stuck Running states, credential and schema-drift errors, incremental-field misconfig, CDC prerequisite failures, and the cancel / reload / resync / delete-data recovery actions. |
| `/suggesting-data-imports` | 📋 Skill | Use when the user asks about revenue, payments, subscriptions, billing, CRM deals, support tickets, production database tables, or other data that PostHog does not collect natively. Also use when a query fails because a table does not exist or returns no results for expected external data. The data warehouse can import from SaaS tools (Stripe, Hubspot, etc.), production databases (Postgres, MySQL, BigQuery, Snowflake), and other arbitrary data sources. Covers checking existing sources, identifying the right source type, and guiding the setup. |
| `/feature-usage-feed` | 📋 Skill | Set up an LLM-judge evaluation that extracts canonical use cases for a PostHog feature at scale and streams the results to a Slack channel as a live feed. Use when someone wants to understand how users are actually using a specific AI/LLM-powered feature in production — what they're investigating, what questions they're trying to answer, and what patterns surface — without manually reading hundreds of traces. Assumes the feature emits `$ai_generation` and `$ai_evaluation` events with `$session_id` linkage to the trigger user's recording (the standard setup post the session-summary linkage PRs). |
| `/creating-an-endpoint` | 📋 Skill | Create a PostHog endpoint with the right shape on the first try — covers query kind choice, name conventions, what to expose as variables (HogQL code_name vs insight breakdown), data_freshness_seconds, and whether to materialise on day one. Use when the user says "create an endpoint", "expose this query as an API", "turn this insight into an endpoint", or asks for help structuring a new endpoint. Steers away from common mistakes: materialising a query with cohort breakdowns or compare mode, inline-only variables on a materialised endpoint, unbounded date ranges, ambiguous names. |
| `/instrument-product-analytics` | 📋 Skill | Add PostHog product analytics events to track user behavior. Use after implementing new features or reviewing PRs to ensure meaningful user actions are captured. Also handles initial PostHog SDK setup if not yet installed. |
| `/designing-email-templates` | 📋 Skill | Author, save, and edit email templates in the PostHog workflows library — compose email design JSON with Liquid personalization and create and round-trip-edit templates over MCP. Use when asked to design, build, update, or fix an email template for workflows, broadcasts, or campaigns. |
| `/auditing-warehouse-data-health` | 📋 Skill | Audit the health of a PostHog project's data warehouse — find every broken or degraded pipeline item across sources, sync schemas, materialized views, batch exports, and transformations. Use when the user asks "what's broken in my warehouse?", "give me a health check", "audit my data pipeline", "why are some dashboards stale?", or wants a one-shot triage summary before deciding where to spend time. Produces a prioritized report of issues grouped by severity and type, with recommended next steps. |
| `/authoring-log-alerts` | 📋 Skill | Author useful, low-noise log alerts on services in a PostHog project. Use when the user asks to set up alerts for their logs, suggest alerts they should add, or evaluate whether a service is worth monitoring. Covers service triage, baseline characterisation, threshold drafting, back-testing via simulate, and shipping with a notification destination. |
| `/signals-scout-logs` | 📋 Skill | Focused Signals scout for PostHog projects using logs. Watches for volume bursts, severity-distribution shifts, service silence, fresh message patterns, and trace-correlated bursts via the logs ingestion pipeline. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/instrument-llm-analytics` | 📋 Skill | Add PostHog LLM analytics to trace AI model usage. Use after implementing LLM features or reviewing PRs to ensure all generations are captured with token counts, latency, and costs. Also handles initial PostHog SDK setup if not yet installed. |
| `/exploring-apm-traces` | 📋 Skill | Investigates distributed application performance using PostHog APM (OpenTelemetry span) data via MCP. Use when the user asks about service traces, slow HTTP/database spans, error spans, trace IDs, or span attributes — not AI observability traces or product logs. Uses posthog:query-apm-spans, posthog:apm-trace-get, posthog:apm-services-list, posthog:apm-attributes-list, and posthog:apm-attribute-values-list. |
| `/exploring-autocapture-events` | 📋 Skill | Guides exploration of $autocapture events captured by posthog-js to understand user interactions, find CSS selectors (especially data-attr attributes), evaluate selector uniqueness, query matching clicks ad-hoc, and create actions. Use when the user asks about autocapture data, wants to find what users are clicking, needs to build actions from click events, asks about elements_chain, wants to build a trend or funnel filtered by clicks or other autocapture interactions, asks which properties autocapture sends, or asks how to filter $autocapture events. Only applies to projects using posthog-js autocapture. |
| `/diagnosing-experiment-results` | 📋 Skill | Diagnoses bias, anomalies, and strange-looking results on a specific PostHog experiment. Covers empty / 0-exposure experiments, sample ratio mismatch, identity fragmentation, multi-variant exposure, uneven-split exclusion bias, significance traps (peeking, A/A, Bayesian vs Frequentist), PostHog-vs-SQL discrepancies, and surprises after mid-run edits. Symptom-driven dispatch to the right diagnostic. TRIGGER when: user asks 'is my experiment biased?' or 'why 0 exposures?', references the bias banner, says a variant looks strange / wrong / off, sees significance flipping, notices PostHog numbers disagreeing with their SQL, sees an A/A test showing significance, or reports surprises after mid-run edits. DO NOT TRIGGER when: creating a new experiment (use creating-experiments), only configuring rollout (use configuring-experiment-rollout) or metrics (use configuring-experiment-analytics), or only asking lifecycle questions (use managing-experiment-lifecycle). |
| `/exploring-live-traffic` | 📋 Skill | Inspects PostHog Web analytics Live tab data — current users online, last-30-minutes pageviews, top pages, referrers, devices, browsers, countries, bot traffic, and the per-minute bot/users charts. Use when the user asks "who is on my site right now?", "what is happening live?", "what bots are crawling me?", asks about the "live tab" / "live dashboard", wants live numbers (last 30 min), or wants help filtering or drilling into the live view. Also covers building product-analytics insights that mirror what the tiles show. |
| `/grouping-noisy-errors` | 📋 Skill | Consolidate PostHog error tracking issues that are the same actual error reported under different fingerprints. Use when the user asks "why do I have so many TypeError issues that look the same?", "merge these duplicates", "stop splitting this error into new issues", or wants to clean up fingerprint sprawl. Decides between a one-shot merge of existing issues and a durable grouping rule that keeps future events from creating new fingerprints. Does NOT group conceptually similar bugs across different runtimes, SDKs, or call sites. |
| `/signals-scout-health-checks` | 📋 Skill | Focused Signals scout for PostHog setup health. Reads the project's active health issues — the deterministic findings of PostHog's own health checks (no live events, outdated SDKs, missing reverse proxy, absent web vitals, ingestion warnings, failing data-warehouse models, and more) — and decides which are genuinely worth surfacing. Unlike a one-signal-per-issue push, it bundles kind-clusters into a single finding, weights by real blast radius (cross-referencing actual event volume and reach), and prioritizes issues an agent can resolve via the MCP. Emits only above the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/exploring-endpoint-execution-logs` | 📋 Skill | Explore and diagnose a PostHog endpoint's execution logs — error messages, failed runs, cache misses, slow runs, or unexpected row counts during endpoint invocations. Use when the user says "my endpoint is failing", "show me the logs for endpoint X", "what error did endpoint Y produce", "why did endpoint Z return no rows", "is this endpoint hitting cache", or "check the last N runs". Focused on a single named endpoint's runtime log entries, not project-wide auditing or query performance profiling. |
| `/authoring-signals-scouts` | 📋 Skill | How to author, edit, and adapt PostHog Signals scouts — the scheduled agents that scan a project and emit findings into the Signals inbox. Use when a user wants to customize a canonical scout for their own setup (narrow its scope, retune its thresholds, add disqualifiers), tweak a scout's schedule or dry-run posture, or write a brand-new scout from scratch for a specific use case (a custom event, a product surface no canonical scout covers). Covers the scout SKILL.md anatomy, the emit contract, the dedupe + scratchpad-memory conventions, the per-team skills-store path vs the canonical in-repo path, and the emit-and-inspect test loop (with dry-run as an optional safety net). Trigger on "write/edit/customize a signals scout", "new scout for X", "tune my scout schedule", "make a scout that watches <event>". |
| `/exploring-llm-clusters` | 📋 Skill | Investigate AI observability clusters — understand usage patterns in AI/LLM traffic, compare cluster behavior, compute cost/latency metrics, and drill into individual traces within clusters. |
| `/debugging-signals-pipeline` | 📋 Skill | Debug the signals pipeline locally end-to-end. Covers emitting test signals from fixtures, monitoring Temporal workflows via the REST API, reading sandbox agent logs from object storage, inspecting Docker sandbox containers, and diagnosing common failures (stale ClickHouse embeddings, agentsh network denials, inactivity timeouts). Use when a signal isn't reaching the inbox, a signal-report-summary workflow fails, or a sandbox task run times out. |
| `/signals-scout-anomaly-detection` | 📋 Skill | Signals scout that watches a PostHog project's most-viewed dashboards and insights for recent anomalies — sudden bursts, drops, flat-lines, and trend breaks at the daily or hourly level. It discovers what the team actually looks at (view counts, dashboard access), curates a durable watchlist in the scratchpad, and balances re-checking known high-value insights (exploit) against discovering new ones (explore) across runs, since no single run can cover a busy project. Anomalies are scored by robust deviation from each insight's own seasonality-matched baseline; it emits a finding only when a move clears the confidence bar, otherwise it updates the baseline memory and closes out empty. Self-contained peer in the signals-scout-* fleet. |
| `/debugging-local-replay` | 📋 Skill | Debugs why session recordings aren't appearing in the local dev environment. Use when a developer reports that local replay ingestion isn't working, recordings aren't showing up despite /s calls, or the replay pipeline seems broken after hogli start. Covers the full local pipeline: SDK capture, Caddy proxy, capture-replay (Rust), Kafka, ingestion-sessionreplay (Node), recording-api (Node), SeaweedFS, and common failure modes like orphaned processes, stuck phrocs workers, and trigger misconfiguration. |
| `/consuming-endpoints-from-client-code` | 📋 Skill | Wire a PostHog endpoint into a client app or SDK. Covers fetching the OpenAPI spec, generating a typed client with openapi-generator or @hey-api/openapi-ts, sending the right auth header, shaping the variables payload (HogQL code_name vs insight breakdown property), handling rate-limit and materialised-endpoint error responses. Use when the user says "how do I call my endpoint", "generate a client for this", or "what auth header do I use". |
| `/exploring-llm-evaluations` | 📋 Skill | Investigate AI observability evaluations of both types — `hog` (deterministic code-based) and `llm_judge` (LLM-prompt-based). Find existing evaluations, inspect their configuration, run them against specific generations, query individual pass/fail results, and generate AI-powered summaries of patterns across many runs. Use when the user asks to debug why an evaluation is failing, surface common failure modes, compare results across filters, dry-run a Hog evaluator, prototype a new LLM-judge prompt, or manage the evaluation lifecycle (create, update, enable/disable, delete). |
| `/instrument-integration` | 📋 Skill | Add PostHog SDK integration to your application. Use when setting up PostHog for the first time or reviewing PRs that need PostHog initialization. Covers SDK installation, provider setup, and basic configuration for any framework. |
| `/configuring-experiment-analytics` | 📋 Skill | Configures the analytics side of a PostHog experiment — exposure criteria (default `$feature_flag_called` vs custom exposure events), primary and secondary metrics, the supported metric types (count, sum, ratio with `math` and `math_property`, retention with `retention_window_start` and `start_handling`), multivariate user handling ("Exclude" vs "First seen variant"), and how to read results once the experiment is live. Use when the user adds or edits a primary or secondary metric (e.g. "add a secondary metric tracking 'downloaded_file' per user"), sets up a ratio metric (e.g. "revenue from purchase_completed / pageviews"), sets up a retention metric (e.g. "$pageview → uploaded_file, 7-day window"), configures custom exposure (e.g. "only count users who hit /checkout"), changes multivariate handling, or asks "who is in the analysis?", "how do I measure impact?", "is this winning?", "what's the confidence level?", or "should I ship?". |
| `/cleaning-up-stale-feature-flags` | 📋 Skill | Identify and clean up stale feature flags in a PostHog project. Use when the user wants to find unused, fully rolled out, or abandoned feature flags, review them for safety, and then disable or delete them. Covers staleness detection, dependency checking, and safe removal workflows. |
| `/triaging-error-issues` | 📋 Skill | Triage PostHog error tracking issues during a daily or on-call review. Use when the user asks "what's broken?", "what new errors do we have?", "show me top errors today", "what should I look at this morning", or wants a prioritized list of active issues to work on. Surfaces new and high-impact issues, ranks by users affected and recency, points at linked replays, and proposes next actions (investigate, assign, suppress, merge). |
| `/investigating-replay` | 📋 Skill | Investigates a session recording by gathering metadata, person profile, same-session events, and linked error tracking issues in one pass. Use when a user provides a recording or session ID and wants to understand what happened — who the user was, what they did, what errors occurred, and whether there are related error tracking issues. Replaces the manual chain of session-recording-get, persons-retrieve, execute-sql, and query-error-tracking-issues-list. |
| `/finding-deleted-feature-flags` | 📋 Skill | Find feature flags that were soft-deleted in the active project within a recent time window. Use when the user asks "what flags were deleted in the last N days", "show me recently deleted feature flags", "who deleted flag X", "audit recent flag deletions", or anything similar. Handles the non-obvious gotcha that system.feature_flags exposes the deleted boolean but does not expose a deletion timestamp — the actual deleted-at time lives in the per-flag activity log and must be cross-referenced. |
| `/signals-scout-inbox-validation` | 📋 Skill | Follow-up scout for the Signals inbox itself. Watches reports that recently transitioned to resolved (an implementation PR merged) and, after a deployment soak window, re-measures the underlying problem to check the fix actually held — plus a strictly-gated escalation check on recently dismissed reports. Emits findings only when a shipped fix demonstrably didn't hold; confirmations and unverifiable verdicts become durable memory and an empty close-out. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/configuring-experiment-rollout` | 📋 Skill | Configures the rollout shape of a PostHog experiment — the variant split (50/50, 80/20, A/B/C ratios), the overall rollout percentage that gates how many users enter the experiment, and the disambiguation when a percentage like "roll out to 25%" could mean either. Use when the user mentions a rollout percentage, variant split, or traffic distribution; gives a ratio like 60/40, 70/30, or 80/20; asks "who sees the test variant?"; wants to increase, decrease, or change the rollout or split on a draft or running experiment; weighs equal vs uneven splits; or proposes a mid-experiment split change (often an anti-pattern that needs reset or end-and-restart). |
| `/diagnosing-stacktrace-symbolication` | 📋 Skill | Help users debug PostHog Error Tracking stack-trace symbolication for any supported platform — JavaScript/TypeScript web, React Native (Hermes), Android (Proguard / R8), or iOS / macOS (dSYM). The PostHog symbol-set lookup flow is universal across platforms; build-tool and artifact details live in per-platform references (JavaScript is fleshed out, others come as we encounter them). Use when stack frames stay minified or obfuscated after symbols are uploaded, PostHog symbol sets show last_used but frames are not readable, chunk IDs or dSYM UUIDs do not match, "Token not found" appears, uploaded source maps / dSYMs / Proguard mappings look empty, or bundler / symbol-upload configuration needs troubleshooting. |
| `/diagnosing-endpoint-performance` | 📋 Skill | Diagnose why a PostHog endpoint is slow or expensive and propose a concrete fix — bump the cache TTL, enable materialisation, restructure variables, or rewrite the query. Use when the user says "this endpoint is slow", "my endpoint times out", "we're hitting the cost cap on this one", or asks "should I materialise this?". Focuses on a single named endpoint, not a project-wide audit. |
| `/signals-scout-revenue-analytics` | 📋 Skill | Focused Signals scout for PostHog projects using revenue analytics. Watches the derived revenue product for upstream failures (Stripe sync stalls, capture regressions), config drift (missing subscription property, currency mix surprises, broken Stripe↔person joins, deferred-revenue gaps), and goal-miss escalations. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/creating-experiments` | 📋 Skill | Guides agents through the 3-step experiment creation flow: defining the hypothesis, configuring rollout, and setting up analytics. Delegates rollout decisions to configuring-experiment-rollout and metric setup to configuring-experiment-analytics. TRIGGER when: user asks to create a new experiment or A/B test, OR when you are about to call experiment-create. DO NOT TRIGGER when: user is updating an existing experiment, managing lifecycle, or only browsing experiments. |
| `/exploring-llm-traces` | 📋 Skill | ABSOLUTE MUST to debug and inspect LLM/AI agent traces using PostHog's MCP tools. Use when the user pastes a trace or session URL (e.g. /ai-observability/traces/<id> or /ai-observability/sessions/<id>), asks to debug a trace, figure out what went wrong, check if an agent used a tool correctly, verify context/files were surfaced, inspect subagent behavior, investigate LLM decisions, or analyze token usage and costs. Also use when raw SQL/HogQL against `events.properties.$ai_input` / `$ai_output_choices` returns empty — message content lives only on the dedicated `posthog.ai_events` table. |
| `/assessing-heatmaps` | 📋 Skill | Assesses what a page's heatmap is telling you and recommends concrete changes. Pulls click / rageclick / scroll-depth data for a URL, names the hot elements by cross-referencing autocapture events on the same page, and can create a saved heatmap the user opens in PostHog, then summarizes the behavior and proposes improvements. TRIGGER when: user asks what a heatmap shows, why people aren't clicking something, where users rage-click, how far they scroll, what to change on a page based on heatmap/click data, or to 'analyze/assess/review the heatmap' for a URL. DO NOT TRIGGER when: the user only wants to create a saved heatmap screenshot with no analysis (use heatmaps-saved-create directly), or is asking about session replay in general (use investigating-replay). |
| `/planning-user-interviews` | 📋 Skill | Plan a user interview topic in PostHog — pick who to target (cohort, emails, or PostHog distinct IDs), draft what to ask about, and prepare the voice-agent context plus a question list. Use when the user asks to "talk to users", "check how users feel about X", "interview some customers", "set up a user interview", "run a user-research call", "find users to ask about Y", or otherwise wants qualitative feedback through a conversation. Walks the user through targeting (cohorts-list, persons-list, or accepting emails / distinct IDs directly), captures the topic, and prompts for agent context and questions before calling user-interview-topics-create. Cohort targeting is resolved to explicit emails/distinct_ids at create time — topics snapshot their audience and do not re-evaluate cohort membership later. Do NOT trigger when the user is uploading a recorded interview audio file (that's the separate UserInterview/transcript flow) or only browsing existing topics with user-interview-topics-list. |
| `/inbox-exploration` | 📋 Skill | Explore PostHog's Inbox — the surface where signal reports surface as actionable issues and trends. Use when the user asks "what's in my inbox?", "what should I look at?", "which reports are actionable?", "what's PostHog flagged recently?", asks about a specific report by ID or title, or wants to see which signal sources are configured. Covers listing, filtering, and drilling into reports, plus pointers to the deeper `signals` skill when raw signals or semantic search are needed. |
| `/signals` | 📋 Skill | How to query the document_embeddings table for raw signal data using HogQL. Use when you need to perform semantic search over signals, fetch every signal that contributed to a specific report, or list signal types. For browsing the curated report layer (the Inbox) — listing reports, filtering by status/source, drilling into a single report by ID — use the `inbox-exploration` skill first; drop into this skill afterwards if the user wants the underlying observations. |
| `/managing-path-cleaning-rules` | 📋 Skill | Inspects URL paths and proposes, tests, orders, and applies project-level path cleaning rules so dynamic segments (numeric IDs, UUIDs, slugs, dates) collapse into readable aliases. Use when the user says "clean the paths", "normalize URLs", "group similar pages", "too many distinct paths", "/users/123 and /users/456 are the same page", "set up path cleaning", or asks why a Web analytics or Paths breakdown is fragmented across thousands of nearly-identical URLs. Covers regex syntax (re2), alias placeholder convention, rule ordering, the test workflow, and applying rules via the project-settings-update MCP tool. |
| `/signals-scout-error-tracking` | 📋 Skill | Focused Signals scout for PostHog projects using error tracking. Watches `$exception` bursts, stuck loops, multi-fingerprint clusters, status regressions, and stack-trace activity-name patterns. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/instrument-error-tracking` | 📋 Skill | Add PostHog error tracking to capture and monitor exceptions. Use after implementing features or reviewing PRs to ensure errors are tracked with stack traces and source maps. Also handles initial PostHog SDK setup if not yet installed. |
| `/setting-up-a-data-warehouse-source` | 📋 Skill | Guide the user through connecting a new data warehouse source — Postgres, MySQL, Stripe, Hubspot, MongoDB, Salesforce, BigQuery, Snowflake, and so on. Use when the user wants to "connect Stripe", "import data from Postgres", "add a new data source", "sync my warehouse tables", or wants to pick sync methods for each table. Walks through source-type discovery, credential validation, table discovery, per-table sync_type selection, and the final create call. Also covers picking a good prefix and what to do right after creation. |
| `/auditing-endpoints` | 📋 Skill | Audit every endpoint in a PostHog project for staleness, failed materialisations, and unused materialised versions. Use when the user asks "what endpoints can I clean up?", "are any of my endpoints broken?", "which materialised versions are still being called?", or wants a one-shot cleanup pass over the Endpoints product. Produces a prioritised report grouped by issue type, with recommended actions but does not modify anything without explicit confirmation. |
| `/working-with-skills` | 📋 Skill | Best practices for agents managing PostHog skills via the MCP `llma-skill-*` tools — how to discover, read, create, update, and refactor skills efficiently, especially large skills with many bundled files. Use whenever you are about to call any `llma-skill-*` tool, asked to author or edit a shared skill, or troubleshoot why a skill write was rejected. Pairs with `skills-store` (which covers the raw tool surface) by adding the decision-tree, efficiency, and pitfall guidance. |
| `/signals-scout-session-replay` | 📋 Skill | Focused Signals scout for PostHog projects using session replay. Watches two promises the replay product makes: that sessions are actually being recorded (capture integrity — recording volume vanishing while site traffic doesn't), and that the friction evidence inside recordings gets seen (rage-click / dead-click clusters concentrating on a page or element, error-after-interaction cohorts, recurring replay vision themes nobody aggregates). Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet. |
| `/diagnosing-sdk-health` | 📋 Skill | Diagnoses the health of a project's PostHog SDK integrations — which SDKs are out of date and how to fix them. Use when a user asks about PostHog SDK versions, outdated SDKs, upgrade recommendations, "SDK health", "SDK doctor" (the former name), or when events or features seem off and it might be due to an old SDK. |
| `/investigate-metric` | 📋 Skill | Diagnose why a product metric changed (dropped, spiked, or plateaued) by orchestrating breakdowns, actors, paths, lifecycle, retention, and annotations queries. Use when the user reports an anomaly, asks "why did X change?", or needs root-cause analysis for a trend, funnel, retention, stickiness, or lifecycle metric. |
| `/signals-scout-replay-vision` | 📋 Skill | Focused Signals scout for PostHog projects running Replay Vision scanners — the standing LLM probes that watch session recordings and write `$recording_observed` events. Watches two promises: that enabled scanners are actually observing (throughput / success-rate cliffs, exhausted quota — a silent watch gap), and that what the scanners see in aggregate gets surfaced (a monitor's `yes`-rate or a scorer's score stepping away from its own baseline, a classifier tag or a recurring summarizer theme concentrating across many sessions). It is the agentic pull complement to the per-session push path: scanners with `emits_signals` already emit one signal per session into this same inbox, so this scout never repeats them — it adds the cross-session shape the per-session probe can't see. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet. |
| `/managing-experiment-lifecycle` | 📋 Skill | Guides experiment state transitions: launching, pausing, resuming, ending, shipping variants, archiving, resetting, duplicating, and copying to another project. Covers preconditions, implications for variant assignment and analysis, and the decision framework for when to use each action. TRIGGER when: user asks to launch, pause, resume, end, ship, archive, reset, duplicate, or copy an experiment to another project. DO NOT TRIGGER when: user is creating an experiment (use creating-experiments), configuring rollout (use configuring-experiment-rollout), or setting up metrics (use configuring-experiment-analytics). |
| `/managing-subscriptions` | 📋 Skill | Manage PostHog subscriptions — scheduled email, Slack, or webhook deliveries of insight or dashboard snapshots, optionally with an AI-written summary attached to each delivery. Use when the user wants to subscribe to an insight or dashboard, get an AI summary attached to those deliveries, check existing subscriptions, change delivery frequency, add or remove recipients, or stop receiving updates. |
| `/creating-replay-vision-scanners` | 📋 Skill | Guides agents through creating and safely sizing a Replay Vision scanner: choosing the scanner type (monitor/classifier/scorer/summarizer), shaping the RecordingsQuery that selects sessions, and — crucially — estimating observation volume and checking the org's monthly quota before creating, so a broad scanner doesn't exhaust the budget on its first scheduled sweep. TRIGGER when: user asks to create, set up, or configure a Replay Vision scanner, OR when you are about to call vision-scanners-create, OR when widening an existing scanner's query or sampling_rate via vision-scanners-update. DO NOT TRIGGER when: only reading scanners or observations, deleting a scanner, or running an existing scanner against a single session on demand (vision-scanners-scan-session). |
| `/signals-scout-general` | 📋 Skill | General Signals scout for PostHog projects. Cross-product explorer that scans a team's project and emits findings into the Signals inbox. Sibling signals-scout-* specialists each watch a single product surface in depth; this scout looks for cross-product correlations and explores the surfaces no specialist covers. Each scout runs on its own schedule (default hourly), so general fires independently of the specialists over time. |
| `/instrument-feature-flags` | 📋 Skill | Add PostHog feature flags to gate new functionality. Use after implementing features or reviewing PRs to ensure safe rollouts with feature flag controls. Also handles initial PostHog SDK setup if not yet installed. |
| `/analyzing-experiment-session-replays` | 📋 Skill | Analyze session replay patterns across experiment variants to understand user behavior differences. Use when the user wants to see how users interact with different experiment variants, identify usability issues, compare behavior patterns between control and test groups, or get qualitative insights to complement quantitative experiment results. |
| `/auditing-experiments-flags` | 📋 Skill | Audit PostHog experiments and feature flags for configuration issues, staleness, and best-practice violations. Read when the user asks to audit, health-check, or review experiments or feature flags, check flag hygiene, or verify experiment setup. |
| `/downloading-batch-export-files` | 📋 Skill | Export PostHog events, persons, or sessions on demand and download the resulting files. Use when the user asks to download/export raw PostHog data, create a one-off file export, fetch a Parquet or JSONLines export, or use the file_download_batch_exports API. Covers starting the export with MCP, polling completion, and downloading via the existing REST redirect endpoint. |
| `/tuning-incremental-sync-config` | 📋 Skill | Change the sync configuration of an existing data warehouse schema — switch sync_type, pick a different incremental_field, set primary_key_columns, choose cdc_table_mode, or change sync_frequency. Use when the user asks "switch my orders table from full refresh to incremental", "this table is syncing too slowly / too frequently", "I need to pick a different incremental column", "set up CDC for this Postgres table", or when diagnosis of a failing sync pointed to an incremental-field or PK misconfiguration. |
| `/signals-scout-feature-flags` | 📋 Skill | Focused Signals scout for PostHog projects using feature flags. Watches the flag roster and the `$feature_flag_called` evaluation stream for contradictions between a flag's configured state and its real traffic: evaluation cliffs on healthy flags, ghost flags (code calling keys that no longer exist), response-distribution shifts with no corresponding flag edit, and flag debt (stale, fully-rolled-out, or dead flags still burning evaluations). Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/finding-replay-for-issue` | 📋 Skill | Finds the most informative session recording linked to an error tracking issue. Use when a user has an error tracking issue ID and wants to watch a replay showing what the user was doing when the error occurred. Ranks linked sessions by recency, activity score, and journey completeness, then summarizes the pre-error context. Replaces blind session picking from potentially hundreds of linked recordings. |
| `/signals-scout-web-analytics` | 📋 Skill | Focused Signals scout for PostHog projects with web traffic. Watches the acquisition and site-health layer the web analytics product reports on: per-channel session volume diverging from the site's own rhythm (an acquisition source silently collapsing or surging), attribution breakage (paid/campaign traffic reclassifying into Direct or Unknown when tagging breaks), landing pages that break (bounce-rate steps, 404 spikes, entry-path cliffs), and page-performance regressions (web vitals p75 steps). Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet. |
| `/exploring-signals-scouts` | 📋 Skill | How to explore and make sense of PostHog Signals scouts — the scheduled agents that scan a project and emit findings into the Signals inbox. Use when a user wants to understand what scouts they have, how each one is behaving, and whether the fleet is actually working. Covers surveying the fleet and its schedules, reading recent scout runs and drilling into a single run's reasoning, inspecting the durable scratchpad memory the fleet has built up, tracing a run to the findings it emitted, and assessing a scout's health and performance over time (cadence, success rate, emit rate, signal-to-noise). Read-only and exploratory — to write or tune a scout, use `authoring-signals-scouts` instead. Trigger on "what are my scouts doing", "how is my <x> scout performing", "show me recent scout runs", "why did this scout find/emit nothing", "what has the fleet learned", "explore scout run <id>", "is my scout working". |
| `/creating-ai-subscription` | 📋 Skill | Create a recurring AI-generated PostHog report — schedule a free-text prompt to run on a cron, with the LLM-synthesized markdown delivered to email or Slack on each tick. Use when the user wants a recurring AI summary of X on any cadence (daily, weekly, monthly, yearly) rather than a one-off report. (To attach an AI summary to an existing insight/dashboard subscription instead of a free-text prompt, see `managing-subscriptions` and its `summary_enabled` option.) |
| `/formatting-insight-axes` | 📋 Skill | Pick the right y-axis unit when creating or updating a TrendsQuery insight via `posthog:insight-create` or `posthog:insight-update`. Use when the agent is about to add a `formula` purely to convert units (e.g. dividing seconds by 60 to display minutes), when a `math_property` is a duration, currency, ratio, or large count, or whenever the user mentions "format the y-axis", "duration", "seconds", "minutes", "hours", "milliseconds", "ms", "percentage", "currency", "decimals", "axis label", or "axis unit" in the context of a graph insight. |
| `/signals-scout-observability-gaps` | 📋 Skill | Focused Signals scout for finding observability gaps in PostHog itself — significant event volumes the team isn't tracking, custom events with no insight or dashboard coverage, insights pointing at events that have stopped firing, dashboards missing related context, critical events with no alerts. Watches the event-stream-vs-saved- inventory delta as the team's product evolves and emits findings recommending new insights, dashboard additions, or alerts when gaps clear the confidence bar. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/diagnosing-missing-recordings` | 📋 Skill | Diagnoses why a session recording is missing or was not captured. Use when a user asks why a session has no replay, why recordings aren't appearing, or wants to troubleshoot session replay capture issues for a specific session ID or across their project. Covers SDK diagnostic signals, project settings, sampling, triggers, ad blockers, and quota/billing scenarios. |
| `/managing-endpoint-versions` | 📋 Skill | Work safely with endpoint versions — preview a draft in the playground, roll back to an older version, update settings on one version without bumping query history, deactivate a specific version. Use when the user asks "how do I roll back my endpoint", "preview my changes before publishing", "I want to fix v5 without bumping the version", or anything involving the version history. Calls out today's limitations honestly: there is no pointer flip; "rollback" means forking the old query into a new top version. |
| `/signals-scout-experiments` | 📋 Skill | Focused Signals scout for PostHog projects running A/B experiments. Watches running experiments for validity threats (sample ratio mismatch, multi-variant contamination, exposure stalls, mid-run flag mutations) and lifecycle drift (zombie experiments running long past their useful life, decided-but-still-running experiments, ended experiments whose flags still serve multiple variants). Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/exploring-llm-costs` | 📋 Skill | Investigate LLM spend in PostHog — total cost over time, cost by model, provider, user, trace, or custom dimension, token and cache-hit economics, and cost regressions. Use when the user asks "how much are we spending on LLMs?", "which model / user / feature is most expensive?", "why did cost spike?", wants to build a cost dashboard or alert, or pastes a trace URL and asks about its cost. |
| `/signals-scout-data-pipelines` | 📋 Skill | Focused Signals scout for PostHog projects moving data through pipelines. Watches the three delivery surfaces — CDP destinations and transformations (hog functions), batch exports, and hog flows (workflows/messaging) — for contradictions between configured state and actual delivery: functions the watcher quietly degraded or disabled, failure rates stepping above a pipeline's own baseline, batch export runs failing or stalling (a growing data gap), and active flows failing for the people they trigger on. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/instrument-logs` | 📋 Skill | Add PostHog log capture to track application logs. Use after implementing features or reviewing PRs to ensure meaningful log events are captured with structured properties. Also handles initial OTLP exporter setup if not yet configured. |
| `/suppressing-noisy-errors` | 📋 Skill | Create PostHog error tracking suppression rules to drop high-volume, low-value errors at ingestion. Use when the user asks "stop capturing this error", "drop browser extension errors", "ignore ResizeObserver loops", "suppress bot-driven errors", or wants to reduce ingestion cost from noisy unactionable errors. Identifies suppression candidates, scopes the filter tightly, decides between full suppression and sampling, and confirms the rule before creating it. Suppressed errors are dropped permanently — this skill defaults to caution. |
| `/signals-scout-ai-observability` | 📋 Skill | Focused Signals scout for PostHog projects using AI observability. Rotates through a set of lenses — cost, latency, errors, volume, eval performance, eval/enrichment config, clusters, and tool usage — watching each for trends and spikes sliced by the dimensions it discovers over time. Leans on the sandbox's bundled `exploring-llm-*` deep-dive skills for the actual queries. Emits findings only when they clear the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other scouts. |
| `/investigating-error-issue` | 📋 Skill | Investigates a single PostHog error tracking issue end-to-end. Use when the user provides an issue ID or pastes an issue URL (`/error_tracking/<id>`) and wants to understand the error — who it affects, what triggers it, when it started, whether it correlates with a release, browser, OS, or feature flag, and what the next step should be. Pulls aggregated metrics, sample exception events, segment breakdowns, linked replays, and synthesizes a hypothesis-grade summary in one pass. |
| `/copying-flags-across-projects` | 📋 Skill | Copy a feature flag from one PostHog project to one or more target projects in the same organization. Use when the user wants to duplicate a flag, promote a flag from staging to production, sync flags across projects, or replicate a flag configuration in a different workspace. Covers cohort remapping, scheduled-change handling, encrypted payloads, and the safe defaults (disabled in target, no scheduled changes). |
| `/signals-scout-csp-violations` | 📋 Skill | Focused Signals scout for PostHog projects collecting Content Security Policy (CSP) violation reports. Watches `$csp_violation` events for fresh blocked-URL clusters, per-directive bursts, page-scoped regressions after deploys, and suspicious third-party domains that may indicate a compromised script. Emits aggregated findings only when a cluster clears the confidence bar; otherwise writes durable memory and closes out empty. Self-contained peer in the signals-scout-* fleet — no dependencies on other skills. |
| `/finding-sessions-to-watch` | 📋 Skill | Guides a user from "I want to watch recordings but don't know which ones" to a short, high-signal list of sessions worth watching. Use when the user asks which sessions or replays to watch, wants help finding interesting / useful recordings, says they don't know where to start in session replay, or wants to watch sessions about a goal (signup, pricing, onboarding, checkout, a feature, rageclicks, errors, mobile, a specific person) without naming exact filters. Turns a vague intent into a focused RecordingsQuery via `query-session-recordings-list`, then deep-links the best few and hands off to `investigating-replay`. Do NOT use when the user already has a recording/session ID (use investigating-replay) or wants the replay for a known error issue (use finding-replay-for-issue). |
| error-analyzer | 🤖 Agent | Analyze multiple PostHog errors in parallel to identify patterns, root causes, and prioritize fixes based on user impact. |
| `/posthog:llma-cc-setup` | ⌨️ Command | Set up PostHog LLM Analytics to capture Claude Code sessions |
| `/posthog:llma-cc-status` | ⌨️ Command | Check if Claude Code sessions are being sent to PostHog LLM Analytics |
| `/posthog:llma-cc-ingest` | ⌨️ Command | Manually send a Claude Code session log to PostHog LLM Analytics |

<a id="p-rootly"></a>

**rootly**（18 Skill、3 Agent）

> Rootly 全生命周期事件管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/trend` | 📋 Skill | Reliability trend summary for a service, team, or the whole org. Reports incident volume, severity mix, and MTTR direction over a window (default 30 days). Use for standups, 1-on-1s, or quarterly reviews. |
| `/my` | 📋 Skill | Personal Rootly dashboard. Shows your open action items, your active incidents (where you're a responder), and your upcoming on-call shifts. Use to start the day or to context-switch back into incident work. |
| `/cover` | 📋 Skill | Offer to cover someone else's on-call shift. Lists upcoming shifts on a team or schedule and creates an override placing you on the chosen one after explicit confirmation. Write action - never executes without confirming. |
| `/lookup` | 📋 Skill | Look up a service, team, or catalog entity in Rootly. Returns owner, on-call, recent reliability, dependencies, and any active incidents. Use when something breaks and the first question is who owns this. |
| `/retro` | 📋 Skill | [experimental] Generate a structured post-incident retrospective from incident data. Forked-subagent flow may not have MCP access in all Claude Code contexts. |
| `/respond` | 📋 Skill | [experimental] Investigate and respond to a production incident. Pulls context, finds similar past incidents, suggests solutions, and enables coordination. Forked-subagent flow may not have MCP access in all Claude Code contexts -- prefer /rootly:status + /rootly:brief for now. |
| `/ask` | 📋 Skill | Ask natural language questions about incidents, on-call, services, and reliability data. Translates your question into Rootly API calls and returns structured answers. |
| `/status` | 📋 Skill | Show a compact service health overview including active incidents by severity. Use for a quick health check of your services. |
| `/setup` | 📋 Skill | Set up the Rootly plugin. Verifies MCP server connection via OAuth2 or API token and guides through configuration. Run this after installing the plugin. |
| `/action` | 📋 Skill | Manage incident action items from the terminal. Subcommands - list (default - your open action items) or add <incident> "<summary>" (create one on an incident). Use to capture follow-ups during or after an incident without opening the Rootly UI. |
| `/deploy-check` | 📋 Skill | [experimental] Evaluate deployment risk by analyzing code changes against incident history, active incidents, and on-call readiness. Forked-subagent flow may not have MCP access in all Claude Code contexts. |
| `/announce` | 📋 Skill | Draft a stakeholder-facing status update for an active incident, then post it after explicit confirmation. Useful for incident commanders pushing public-status-page or internal updates without opening the Rootly UI. Write action - never posts without confirming. |
| `/test` | 📋 Skill | Simple test skill |
| `/oncall` | 📋 Skill | Show current on-call status, shift metrics, and health indicators for your team. Use to check who's on-call, handoff context, or on-call workload. |
| `/handoff` | 📋 Skill | Prepare an incident or on-call handoff document. Creates structured summary for shift changes or incident commander transitions. |
| `/brief` | 📋 Skill | Generate a concise stakeholder brief for an incident. Creates executive summary with key details, impact, timeline, and current status. |
| `/alert` | 📋 Skill | Triage a Rootly alert by short ID. Pulls the alert record, its event timeline, related alerts in the same group, and any incident the alert is attached to. Use when a page comes in and you want context before opening Rootly. |
| `/swap` | 📋 Skill | Request someone to cover one of your upcoming on-call shifts. Lists your shifts, helps identify a candidate based on availability, and creates an override after explicit confirmation. Write action - never executes without confirming. |
| retro-analyst | 🤖 Agent | Reliability pattern analyst for retrospectives, recurring-incident clustering, and systemic improvement recommendations. |
| incident-investigator | 🤖 Agent | Deep production-incident investigator for root-cause analysis, evidence gathering, and remediation planning beyond the initial response brief. |
| deploy-guardian | 🤖 Agent | Deployment safety specialist for blast-radius analysis, downstream dependency checks, and cross-team coordination planning. |

<a id="p-sentry"></a>

**sentry**（33 Skill、1 Command）

> Sentry 错误监控与堆栈分析

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sentry-react-native-sdk` | 📋 Skill | Full Sentry SDK setup for React Native and Expo. Use when asked to "add Sentry to React Native", "install @sentry/react-native", "setup Sentry in Expo", or configure error monitoring, tracing, profiling, session replay, or logging for React Native applications. Supports Expo managed, Expo bare, and vanilla React Native. |
| `/sentry-fix-issues` | 📋 Skill | Find and fix issues from Sentry using MCP. Use when asked to fix Sentry errors, debug production issues, investigate exceptions, or resolve bugs reported in Sentry. Methodically analyzes stack traces, breadcrumbs, traces, and context to identify root causes. |
| `/sentry-span-streaming-python` | 📋 Skill | Migrate Python SDK to Sentry span streaming (span-first trace lifecycle). Use when asked to "enable span streaming", "migrate to span streaming", "use trace_lifecycle stream", or switch from transaction-based to streamed span delivery in a Python project. |
| `/sentry-otel-exporter-setup` | 📋 Skill | Configure the OpenTelemetry Collector with Sentry Exporter for multi-project routing and automatic project creation. Use when setting up OTel with Sentry, configuring collector pipelines for traces and logs, or routing telemetry from multiple services to Sentry projects. |
| `/sentry-nextjs-sdk` | 📋 Skill | Full Sentry SDK setup for Next.js. Use when asked to "add Sentry to Next.js", "install @sentry/nextjs", or configure error monitoring, tracing, session replay, logging, profiling, AI monitoring, or crons for Next.js applications. Supports Next.js 13+ with App Router and Pages Router. |
| `/sentry-android-sdk` | 📋 Skill | Full Sentry SDK setup for Android. Use when asked to "add Sentry to Android", "install sentry-android", "setup Sentry in Android", or configure error monitoring, tracing, profiling, session replay, or logging for Android applications. Supports Kotlin and Java codebases. |
| `/sentry-elixir-sdk` | 📋 Skill | Full Sentry SDK setup for Elixir. Use when asked to "add Sentry to Elixir", "install sentry for Elixir", or configure error monitoring, tracing, logging, or crons for Elixir, Phoenix, or Plug applications. Supports Phoenix, Plug, LiveView, Oban, and Quantum. |
| `/sentry-nestjs-sdk` | 📋 Skill | Full Sentry SDK setup for NestJS. Use when asked to "add Sentry to NestJS", "install @sentry/nestjs", "setup Sentry in NestJS", or configure error monitoring, tracing, profiling, logging, metrics, crons, or AI monitoring for NestJS applications. Supports Express and Fastify adapters, GraphQL, microservices, WebSockets, and background jobs. |
| `/sentry-setup-ai-monitoring` | 📋 Skill | Setup Sentry AI Agent Monitoring in any project. Use when asked to monitor LLM calls, track AI agents, track conversations, or instrument OpenAI/Anthropic/Vercel AI/LangChain/Google GenAI/Pydantic AI. Detects installed AI SDKs and configures appropriate integrations. |
| `/sentry-tanstack-start-sdk` | 📋 Skill | Full Sentry SDK setup for TanStack Start React. Use when asked to "add Sentry to TanStack Start", "install @sentry/tanstackstart-react", or configure error monitoring, tracing, session replay, logs, or user feedback in a TanStack Start React app. |
| `/sentry-workflow` | 📋 Skill | Fix production issues and review code with Sentry context. Use when asked to fix Sentry errors, debug issues, triage exceptions, review PR comments from Sentry, or resolve bugs. |
| `/sentry-browser-sdk` | 📋 Skill | Full Sentry SDK setup for browser JavaScript. Use when asked to "add Sentry to a website", "install @sentry/browser", or configure error monitoring, tracing, session replay, or logging for vanilla JavaScript, jQuery, static sites, or WordPress. |
| `/sentry-code-review` | 📋 Skill | Analyze and resolve Sentry comments on GitHub Pull Requests. Use this when asked to review or fix issues identified by Sentry in PR comments. Can review specific PRs by number or automatically find recent PRs with Sentry feedback. |
| `/sentry-dotnet-sdk` | 📋 Skill | Full Sentry SDK setup for .NET. Use when asked to "add Sentry to .NET", "install Sentry for C#", or configure error monitoring, tracing, profiling, logging, or crons for ASP.NET Core, MAUI, WPF, WinForms, Blazor, Azure Functions, or any other .NET application. |
| `/sentry-feature-setup` | 📋 Skill | Configure specific Sentry features beyond basic SDK setup. Use when asked to monitor AI/LLM calls, set up OpenTelemetry pipelines, create alerts and notifications, or enable span streaming. |
| `/sentry-ruby-sdk` | 📋 Skill | Full Sentry SDK setup for Ruby. Use when asked to add Sentry to Ruby, install sentry-ruby, setup Sentry in Rails/Sinatra/Rack, or configure error monitoring, tracing, logging, metrics, profiling, or crons for Ruby applications. Also handles migration from AppSignal, Honeybadger, Bugsnag, Rollbar, or Airbrake. Supports Rails, Sinatra, Rack, Sidekiq, and Resque. |
| `/sentry-instrumentation-guide` | 📋 Skill | Decide which Sentry signal to reach for when instrumenting code — error, span, span attribute, log, or metric. Use when adding instrumentation and unsure whether something should be a log vs a span vs a metric, when deciding "what to instrument where", when reviewing instrumentation for gaps, or when a coding agent needs a rule for choosing between errors, traces, logs, and metrics. This skill decides WHAT to emit; the sentry-*-sdk skills handle HOW to set each pillar up. |
| `/sentry-sdk-setup` | 📋 Skill | Set up Sentry in any language or framework. Detects the user's platform and loads the right SDK skill. Use when asked to add Sentry, install an SDK, or set up error monitoring in a project. |
| `/sentry-svelte-sdk` | 📋 Skill | Full Sentry SDK setup for Svelte and SvelteKit. Use when asked to "add Sentry to Svelte", "add Sentry to SvelteKit", "install @sentry/sveltekit", or configure error monitoring, tracing, session replay, or logging for Svelte or SvelteKit applications. |
| `/sentry-python-sdk` | 📋 Skill | Full Sentry SDK setup for Python. Use when asked to "add Sentry to Python", "install sentry-sdk", "setup Sentry in Python", or configure error monitoring, tracing, profiling, logging, metrics, crons, or AI monitoring for Python applications. Supports Django, Flask, FastAPI, Celery, Starlette, AIOHTTP, Tornado, and more. |
| `/sentry-span-streaming-js` | 📋 Skill | Migrate JavaScript SDK to Sentry span streaming (span-first trace lifecycle). Use when asked to "enable span streaming", "migrate to span streaming", "use traceLifecycle stream", "add spanStreamingIntegration", or switch from transaction-based to streamed span delivery in a JavaScript project. |
| `/sentry-node-sdk` | 📋 Skill | Full Sentry SDK setup for Node.js, Bun, and Deno. Use when asked to "add Sentry to Node.js", "add Sentry to Bun", "add Sentry to Deno", "install @sentry/node", "@sentry/bun", or "@sentry/deno", or configure error monitoring, tracing, logging, profiling, metrics, crons, or AI monitoring for server-side JavaScript/TypeScript runtimes. |
| `/sentry-pr-code-review` | 📋 Skill | Review a project's PRs to check for issues detected in code review by Seer Bug Prediction. Use when asked to review or fix issues identified by Sentry in PR comments, or to find recent PRs with Sentry feedback. |
| `/sentry-flutter-sdk` | 📋 Skill | Full Sentry SDK setup for Flutter and Dart. Use when asked to "add Sentry to Flutter", "install sentry_flutter", "setup Sentry in Dart", or configure error monitoring, tracing, profiling, session replay, or logging for Flutter applications. Supports Android, iOS, macOS, Linux, Windows, and Web. |
| `/sentry-cocoa-sdk` | 📋 Skill | Full Sentry SDK setup for Apple platforms (iOS, macOS, tvOS, watchOS, visionOS). Use when asked to "add Sentry to iOS", "add Sentry to Swift", "install sentry-cocoa", or configure error monitoring, tracing, profiling, session replay, logging, or metrics for Apple applications. Supports SwiftUI and UIKit. |
| `/sentry-cloudflare-sdk` | 📋 Skill | Full Sentry SDK setup for Cloudflare Workers and Pages. Use when asked to "add Sentry to Cloudflare Workers", "install @sentry/cloudflare", or configure error monitoring, tracing, logging, crons, or AI monitoring for Cloudflare Workers, Pages, Durable Objects, Queues, Workflows, or Hono on Cloudflare. |
| `/sentry-sdk-upgrade` | 📋 Skill | Upgrade the Sentry JavaScript SDK across major versions. Use when asked to upgrade Sentry, migrate to a newer version, fix deprecated Sentry APIs, or resolve breaking changes after a Sentry version bump. |
| `/sentry-react-router-framework-sdk` | 📋 Skill | Full Sentry SDK setup for React Router Framework mode. Use when asked to "add Sentry to React Router Framework", "install @sentry/react-router", or configure error monitoring, tracing, profiling, session replay, logs, or user feedback for a React Router v7 framework app. |
| `/sentry-sdk-skill-creator` | 📋 Skill | Create a complete Sentry SDK skill bundle for any platform. Use when asked to "create an SDK skill", "add a new platform skill", "write a Sentry skill for X", or build a new sentry-<platform>-sdk skill bundle with wizard flow and feature reference files. |
| `/sentry-create-alert` | 📋 Skill | Create Sentry alerts using the workflow engine API. Use when asked to create alerts, set up notifications, configure issue priority alerts, or build workflow automations. Supports email, Slack, PagerDuty, Discord, and other notification actions. |
| `/sentry-go-sdk` | 📋 Skill | Full Sentry SDK setup for Go. Use when asked to "add Sentry to Go", "install sentry-go", "setup Sentry in Go", or configure error monitoring, tracing, logging, metrics, or crons for Go applications. Supports net/http, Gin, Echo, Fiber, FastHTTP, Iris, Negroni, and gRPC. |
| `/sentry-react-sdk` | 📋 Skill | Full Sentry SDK setup for React. Use when asked to "add Sentry to React", "install @sentry/react", or configure error monitoring, tracing, session replay, profiling, or logging for React applications. Supports React 16+, React Router v5-v7 non-framework mode, TanStack Router, Redux, Vite, and webpack. |
| `/sentry-php-sdk` | 📋 Skill | Full Sentry SDK setup for PHP. Use when asked to "add Sentry to PHP", "install sentry/sentry", "setup Sentry in PHP", or configure error monitoring, tracing, profiling, logging, metrics, or crons for PHP applications. Supports plain PHP, Laravel, and Symfony. |
| `/seer` | ⌨️ Command | Ask natural language questions about your Sentry environment and get detailed insights using the Sentry MCP server |

<a id="p-sentry-cli"></a>

**sentry-cli**（1 Skill）

> Sentry 命令行工具技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/sentry-cli` | 📋 Skill | Guide for using the Sentry CLI to interact with Sentry from the command line. Use when the user asks about viewing issues, events, projects, organizations, making API calls, or authenticating with Sentry via CLI. |


## 🚀 Deployment（6 个插件）

<a id="p-azure"></a>

**azure**（28 Skill）

> Azure 云平台专家集成管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/azure-hosted-copilot-sdk` | 📋 Skill | Build, deploy, and modify GitHub Copilot SDK apps on Azure. MANDATORY when codebase contains @github/copilot-sdk or CopilotClient in package.json. PREFER OVER azure-prepare when copilot-sdk markers detected. WHEN: copilot SDK, @github/copilot-sdk, copilot-powered app, build copilot app, prepare copilot app, add feature to copilot app, modify copilot app, BYOM, bring your own model, CopilotClient, createSession, sendAndWait, azd init copilot. DO NOT USE FOR: deploying already-prepared copilot-sdk apps (use azure-deploy), general web apps without copilot SDK (use azure-prepare), Copilot Extensions, Foundry agents (use microsoft-foundry). |
| `/python-appservice-deploy` | 📋 Skill | Deploy Python (Flask/Django/FastAPI) code to Azure App Service Linux. WHEN: "Flask App Service", "Django App Service", "FastAPI App Service", "deploy Python to App Service". DO NOT USE FOR: Container Apps, Functions, non-Python, Terraform/Bicep/IaC, full infra — use azure-prepare. |
| `/azure-prepare` | 📋 Skill | Prepare Azure apps for deployment (infra Bicep/Terraform, azure.yaml, Dockerfiles). Use for create/modernize or create+deploy; not cross-cloud migration (use azure-cloud-migrate). DO NOT USE FOR: copilot-sdk apps (use azure-hosted-copilot-sdk), or Python code-only App Service deploys (use python-appservice-deploy). WHEN: "create app", "build web app", "create API", "modernize application", "host on Azure", "deploy to Azure", "deploy to Azure using Terraform", "deploy to Azure App Service", "deploy to Azure App Service using Terraform", "deploy to Azure Container Apps", "generate Terraform", "generate Bicep", "function app", "timer trigger", "service bus trigger", "event-driven function", "managed identity". |
| `/azure-compute` | 📋 Skill | Azure VM/VMSS router. WHEN: create / provision / deploy / spin-up VM, recommend VM size, compare VM pricing, VMSS, scale set, autoscale, burstable, lightweight server, website, backend, GPU, machine learning, HPC simulation, dev/test, workload, family, load balancer, Flexible orchestration, Uniform orchestration, cost estimate, can't connect / RDP / SSH, refused, black screen, reset password, reach VM, port 3389, NSG, security, Linux, troubleshoot, troubleshooting, connectivity, capacity reservation (CRG), reserve, guarantee capacity, pre-provision, CRG association, CRG disassociation, machine enrollment (EMM), Essential Machine Management, monitor. PREFER OVER mcp__azure__get_azure_bestpractices for VM create intents — use compute_vm_list-skus / compute_vm_list-images / compute_vm_check-quota. |
| `/azure-reliability` | 📋 Skill | Assess and improve the reliability posture of PaaS Applications (Azure Functions and Azure App Service). Scans deployed resources for zone redundancy, ZRS storage, health probes, and multi-region failover. Presents a feature-pivoted checklist, then drives staged remediation (CLI or IaC patches) end-to-end with user confirmation. WHEN: "assess reliability", "check reliability", "zone redundant", "multi-region failover", "high availability", "disaster recovery", "single points of failure", "reliability posture", "resiliency". |
| `/azure-aigateway` | 📋 Skill | Configure Azure API Management as an AI Gateway for AI models, MCP tools, and agents. WHEN: semantic caching, token limit, content safety, load balancing, AI model governance, MCP rate limiting, jailbreak detection, add Azure OpenAI backend, add AI Foundry model, test AI gateway, LLM policies, configure AI backend, token metrics, AI cost control, convert API to MCP, import OpenAPI to gateway. |
| `/appinsights-instrumentation` | 📋 Skill | Guidance for instrumenting webapps with Azure Application Insights. Provides telemetry patterns, SDK setup, and configuration references. WHEN: how to instrument app, App Insights SDK, telemetry patterns, what is App Insights, Application Insights guidance, instrumentation examples, APM best practices. |
| `/azure-ai` | 📋 Skill | Use for Azure AI: Search, Speech, OpenAI, Document Intelligence. Helps with search, vector/hybrid search, speech-to-text, text-to-speech, transcription, OCR. WHEN: AI Search, query search, vector search, hybrid search, semantic search, speech-to-text, text-to-speech, transcribe, OCR, convert text to speech. |
| `/azure-deploy` | 📋 Skill | Execute Azure deployments for ALREADY-PREPARED applications that have existing .azure/deployment-plan.md and infrastructure files. DO NOT use this skill when the user asks to CREATE a new application — use azure-prepare instead. This skill runs azd up, azd deploy, terraform apply, and az deployment commands with built-in error recovery. Requires .azure/deployment-plan.md from azure-prepare and validated status from azure-validate. WHEN: "run azd up", "run azd deploy", "execute deployment", "push to production", "push to cloud", "go live", "ship it", "bicep deploy", "terraform apply", "publish to Azure", "launch on Azure". DO NOT USE WHEN: "create and deploy", "build and deploy", "create a new app", "set up infrastructure", "create and deploy to Azure using Terraform" — use azure-prepare for these. |
| `/azure-cost` | 📋 Skill | Azure cost management: query costs, forecast spending, optimize to reduce waste. WHEN: "Azure costs", "Azure bill", "cost breakdown", "how much am I spending", "forecast spending", "optimize costs", "reduce spending", "orphaned resources", "rightsize VMs", "cost spike", "reduce storage costs", "AKS cost". DO NOT USE FOR: deploying resources, provisioning, diagnostics, or security audits. |
| `/azure-rbac` | 📋 Skill | Helps users find the right Azure RBAC role for an identity with least privilege access, then generate CLI commands and Bicep code to assign it. Also provides guidance on permissions required to grant roles. WHEN: bicep for role assignment, what role should I assign, least privilege role, RBAC role for, role to read blobs, role for managed identity, custom role definition, assign role to identity, what role do I need to grant access, permissions to assign roles. |
| `/entra-agent-id` | 📋 Skill | Provision Microsoft Entra Agent Identity Blueprints, BlueprintPrincipals, and per-instance Agent Identities via Microsoft Graph, and configure OAuth 2.0 token exchange (fmi_path, OBO, cross-tenant) including the Microsoft Entra SDK for AgentID sidecar. USE FOR: Agent Identity Blueprint, BlueprintPrincipal, agent OAuth, fmi_path token exchange, agent OBO, Workload Identity Federation for agents, polyglot agent auth, Microsoft.Identity.Web.AgentIdentities. DO NOT USE FOR: standard Entra app registration (use entra-app-registration), Azure RBAC (use azure-rbac), Microsoft Foundry agent authoring (use microsoft-foundry). |
| `/azure-resource-visualizer` | 📋 Skill | Analyze Azure resource groups and generate detailed Mermaid architecture diagrams showing the relationships between individual resources. WHEN: create architecture diagram, visualize Azure resources, show resource relationships, generate Mermaid diagram, analyze resource group, diagram my resources, architecture visualization, resource topology, map Azure infrastructure. |
| `/entra-app-registration` | 📋 Skill | Guides Microsoft Entra ID app registration, OAuth 2.0 authentication, and MSAL integration. USE FOR: create app registration, register Azure AD app, configure OAuth, set up authentication, add API permissions, generate service principal, MSAL example, console app auth, Entra ID setup, Azure AD authentication. DO NOT USE FOR: Azure RBAC or role assignments (use azure-rbac), Key Vault secrets (use azure-keyvault-expiration-audit), general Azure resource security guidance. |
| `/azure-compliance` | 📋 Skill | Run Azure compliance and security audits with azqr plus Key Vault expiration checks. Covers best-practice assessment, resource review, policy/compliance validation, and security posture checks. WHEN: compliance scan, security audit, BEFORE running azqr (compliance cli tool), Azure best practices, Key Vault expiration check, expired certificates, expiring secrets, orphaned resources, compliance assessment. |
| `/azure-resource-lookup` | 📋 Skill | List, find, and show Azure resources across subscriptions or resource groups. Handles prompts like "list the websites in my subscription", "list my web apps", "show my app services", "list virtual machines", "list my VMs", "show storage accounts", "find container apps", and "what resources do I have". USE FOR: list websites, list web apps, list app services, show websites in subscription, resource inventory, find resources by tag, tag analysis, orphaned resource discovery (not for cost analysis), unattached disks, count resources by type, cross-subscription lookup, and Azure Resource Graph queries. DO NOT USE FOR: deploying/changing resources (use azure-deploy), cost optimization (use azure-cost), or non-Azure clouds. |
| `/azure-diagnostics` | 📋 Skill | Debug Azure production issues on Azure using AppLens, Azure Monitor, resource health, and safe triage. WHEN: debug production issues, troubleshoot app service, app service high CPU, app service deployment failure, troubleshoot container apps, troubleshoot functions, troubleshoot AKS, kubectl cannot connect, kube-system/CoreDNS failures, pod pending, crashloop, node not ready, upgrade failures, analyze logs, KQL, insights, image pull failures, cold start issues, health probe failures, resource health, root cause of errors, troubleshoot event hubs, troubleshoot service bus, messaging SDK error, AMQP connection failure, message lock lost, service bus dead letter. |
| `/azure-storage` | 📋 Skill | Azure Storage Services including Blob Storage, File Shares, Queue Storage, Table Storage, and Data Lake. Answers questions about storage access tiers (hot, cool, cold, archive), when to use each tier, and tier comparison. Provides object storage, SMB file shares, async messaging, NoSQL key-value, and big data analytics. Includes lifecycle management. USE FOR: blob storage, file shares, queue storage, table storage, data lake, upload files, download blobs, storage accounts, access tiers, storage tiers, hot cool cold archive, storage tier comparison, when to use storage tiers, lifecycle management, Azure Storage concepts. DO NOT USE FOR: SQL databases, Cosmos DB (use azure-prepare), messaging with Event Hubs or Service Bus (use azure-messaging). |
| `/azure-quotas` | 📋 Skill | Check/manage Azure quotas and usage across providers. For deployment planning, capacity validation, region selection. WHEN: "check quotas", "service limits", "current usage", "request quota increase", "quota exceeded", "validate capacity", "regional availability", "provisioning limits", "vCPU limit", "how many vCPUs available in my subscription". |
| `/azure-upgrade` | 📋 Skill | Assess and upgrade Azure workloads between plans, tiers, or SKUs, or modernize Azure SDK dependencies in source code. WHEN: upgrade Consumption to Flex Consumption, upgrade Azure Functions plan, change hosting plan, function app SKU, migrate App Service to Container Apps, modernize legacy Azure Java SDKs (com.microsoft.azure to com.azure), migrate Azure Cache for Redis (ACR/ACRE) to Azure Managed Redis (AMR). |
| `/azure-validate` | 📋 Skill | Pre-deployment validation for Azure readiness. Run deep checks on configuration, infrastructure (Bicep or Terraform), RBAC role assignments, managed identity permissions, and prerequisites before deploying. WHEN: validate my app, check deployment readiness, run preflight checks, verify configuration, check if ready to deploy, validate azure.yaml, validate Bicep, test before deploying, troubleshoot deployment errors, validate Azure Functions, validate function app, validate serverless deployment, verify RBAC roles, check role assignments, review managed identity permissions, what-if analysis, validate Container Apps deployment. |
| `/airunway-aks-setup` | 📋 Skill | Set up AI Runway on AKS — from bare cluster to running model. Covers cluster verification, controller install, GPU assessment, provider setup, and first deployment. WHEN: "setup AI Runway", "onboard AKS cluster", "install AI Runway", "airunway setup", "deploy model to AKS", "GPU inference on AKS", "KAITO setup on AKS", "run LLM on AKS", "vLLM on AKS", "set up model serving on AKS", "AI Runway controller". |
| `/azure-messaging` | 📋 Skill | Troubleshoot and resolve issues with Azure Messaging SDKs for Event Hubs and Service Bus. Covers connection failures, authentication errors, message processing issues, and SDK configuration problems. WHEN: event hub SDK error, service bus SDK issue, messaging connection failure, AMQP error, event processor host issue, message lock lost, message lock expired, lock renewal, lock renewal batch, send timeout, receiver disconnected, SDK troubleshooting, azure messaging SDK, event hub consumer, service bus queue issue, topic subscription error, enable logging event hub, service bus logging, eventhub python, servicebus java, eventhub javascript, servicebus dotnet, event hub checkpoint, event hub not receiving messages, service bus dead letter, batch processing lock, session lock expired, idle timeout, connection inactive, link detach, slow reconnect, session error, duplicate events, offset reset, receive batch. |
| `/azure-enterprise-infra-planner` | 📋 Skill | Architect and provision enterprise Azure infrastructure from workload descriptions. For cloud architects and platform engineers planning networking, identity, security, compliance, and multi-resource topologies with WAF alignment. Generates Bicep or Terraform directly (no azd). WHEN: 'plan Azure infrastructure', 'architect Azure landing zone', 'design hub-spoke network', 'plan multi-region DR topology', 'set up VNets firewalls and private endpoints', 'subscription-scope Bicep deployment', 'Azure Backup for VM workloads'. PREFER azure-prepare FOR app-centric workflows. |
| `/azure-cloud-migrate` | 📋 Skill | Assess and migrate cross-cloud workloads to Azure with reports and code conversion. Supports Lambda→Functions, Beanstalk/Heroku/App Engine→App Service, Fargate/Kubernetes/Cloud Run/Spring Boot→Container Apps. WHEN: migrate Lambda to Functions, AWS to Azure, migrate Beanstalk, migrate Heroku, migrate App Engine, Cloud Run migration, Fargate to ACA, ECS/Kubernetes/GKE/EKS to Container Apps, Spring Boot to Container Apps, cross-cloud migration. |
| `/microsoft-foundry` | 📋 Skill | Deploy, evaluate, fine-tune, and manage Foundry agents end-to-end with azd: hosted agent scaffold/run/deploy, prompt agent create, batch eval, continuous eval, prompt optimizer, Agent Optimizer scaffold, agent.yaml, dataset curation from traces, model fine-tuning (SFT/DPO/RFT). USE FOR: azd ai agent, azd provision/deploy, deploy agent, hosted agent, create agent, add tool to agent, invoke agent, evaluate agent, continuous eval, continuous monitoring, optimize prompt, improve prompt, optimize agent instructions, agent optimizer, deploy model, Foundry project, RBAC, role assignment, permissions, quota, capacity, region, troubleshoot agent, deployment failure, AI Services, create Foundry resource, provision, knowledge index, customize deployment, onboard, availability, fine-tune, SFT, DPO, RFT, training-data, grader, distillation, fine-tuned model, large file upload. DO NOT USE FOR: Azure Functions, App Service, general Azure deploy (use azure-deploy), general Azure prep (use azure-prepare). |
| `/azure-kusto` | 📋 Skill | Query and analyze data in Azure Data Explorer (Kusto/ADX) using KQL for log analytics, telemetry, and time series analysis. WHEN: KQL queries, Kusto database queries, Azure Data Explorer, ADX clusters, log analytics, time series data, IoT telemetry, anomaly detection. |
| `/azure-kubernetes` | 📋 Skill | Plan, create, and configure production-ready Azure Kubernetes Service (AKS) clusters. Covers Day-0 checklist, SKU selection (Automatic vs Standard), networking options (private API server, Azure CNI Overlay, egress configuration), security, and operations (autoscaling, upgrade strategy, cost analysis). WHEN: create AKS environment, provision AKS, enable AKS observability, design AKS networking, choose AKS SKU, secure AKS, optimize AKS, AKS spot nodes, AKS cluster-autoscaler, rightsize AKS pod, pod rightsizing, over-provisioned AKS pod, pod resource requests and limits, Vertical Pod Autoscaler, VPA recommendations. |

<a id="p-cloudflare"></a>

**cloudflare**（11 Skill、2 Command）

> Cloudflare Workers 与 Agent SDK 开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cloudflare-one-migrations` | 📋 Skill | Plans migrations from Zscaler ZIA/ZPA, Palo Alto, legacy VPN, SWG, or SASE stacks to Cloudflare One. Use for migration assessments, policy mapping, rollout plans, and parity/gap analysis. |
| `/cloudflare` | 📋 Skill | Comprehensive Cloudflare platform skill covering Workers, Pages, storage (KV, D1, R2), AI (Workers AI, Vectorize, Agents SDK), feature flags (Flagship), networking (Tunnel, Spectrum), security (WAF, DDoS), and infrastructure-as-code (Terraform, Pulumi). Use for any Cloudflare development task. Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/turnstile-spin` | 📋 Skill | Set up Cloudflare Turnstile end-to-end in a project — scan the codebase, create the widget via the Cloudflare API, deploy the managed siteverify Worker, write the frontend snippets, validate, and persist the skill. Load this when a user asks to add Turnstile, set up CAPTCHA, protect a form from bots, or fix a Turnstile integration. Mirrors developers.cloudflare.com/turnstile/spin. |
| `/sandbox-sdk` | 📋 Skill | Build sandboxed applications for secure code execution. Load when building AI code execution, code interpreters, CI/CD systems, interactive dev environments, or executing untrusted code. Covers Sandbox SDK lifecycle, commands, files, code interpreter, and preview URLs. Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/durable-objects` | 📋 Skill | Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers Workers integration, wrangler config, and testing with Vitest. Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/cloudflare-one` | 📋 Skill | Guides Cloudflare One Zero Trust and SASE work across Access, Gateway, WARP, Tunnel, Cloudflare WAN, DLP, CASB, device posture, and identity. Use when designing, configuring, troubleshooting, or reviewing Cloudflare One deployments. Retrieval-first: use current Cloudflare docs/API schemas instead of embedded product docs. |
| `/workers-best-practices` | 📋 Skill | Reviews and authors Cloudflare Workers code against production best practices. Load when writing new Workers, reviewing Worker code, configuring wrangler.jsonc, or checking for common Workers anti-patterns (streaming, floating promises, global state, secrets, bindings, observability). Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/agents-sdk` | 📋 Skill | Build AI agents on Cloudflare Workers using the Agents SDK. Load when creating stateful agents, durable workflows, real-time WebSocket apps, scheduled tasks, MCP servers, chat applications, voice agents, or browser automation. Covers Agent class, state management, callable RPC, Workflows, durable execution, queues, retries, observability, and React hooks. Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/web-perf` | 📋 Skill | Analyzes web performance using Chrome DevTools MCP. Measures Core Web Vitals (LCP, INP, CLS) and supplementary metrics (FCP, TBT, Speed Index), identifies render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps. Use when asked to audit, profile, debug, or optimize page load performance, Lighthouse scores, or site speed. Biases towards retrieval from current documentation over pre-trained knowledge. |
| `/wrangler` | 📋 Skill | Cloudflare Workers CLI for deploying, developing, and managing Workers, KV, R2, D1, Vectorize, Hyperdrive, Workers AI, Containers, Queues, Workflows, Pipelines, and Secrets Store. Load before running wrangler commands to ensure correct syntax and best practices. Biases towards retrieval from Cloudflare docs over pre-trained knowledge. |
| `/cloudflare-email-service` | 📋 Skill | Send and receive transactional emails with Cloudflare Email Service (Email Sending + Email Routing). Use when building email sending (Workers binding or REST API), email routing, Agents SDK email handling, or integrating email into any app — Workers, Node.js, Python, Go, etc. Also use for email deliverability, SPF/DKIM/DMARC, wrangler email setup, MCP email tools, or when a coding agent needs to send emails. Even for simple requests like "add email to my Worker" — this skill has critical config details. |
| `/cloudflare:build-mcp` | ⌨️ Command | Build a remote MCP server on Cloudflare using McpAgent |
| `/cloudflare:build-agent` | ⌨️ Command | Build an AI agent on Cloudflare using the Agents SDK |

<a id="p-deploy-on-aws"></a>

**deploy-on-aws**（3 Skill）

> AWS 应用部署架构推荐与成本估算

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/elastic-beanstalk` | 📋 Skill | Deploy to AWS Elastic Beanstalk. Triggers on: elastic beanstalk, EB, managed EC2 platform, web app with managed patching, worker on EC2, Heroku alternative, don't want to manage servers or containers, migrate from Heroku, managed operational lifecycle. Covers Elastic Beanstalk on EC2 for web and worker applications. |
| `/aws-architecture-diagram` | 📋 Skill | Generate validated AWS architecture diagrams as draw.io XML using official AWS4 icon libraries. Use this skill whenever the user wants to create, generate, or design AWS architecture diagrams, cloud infrastructure diagrams, or system design visuals. Also triggers for requests to visualize existing infrastructure from CloudFormation, CDK, or Terraform code. Supports two modes: analyze an existing codebase to auto-generate diagrams, or brainstorm interactively from scratch. Exports .drawio files with optional PNG/SVG/PDF export via draw.io desktop CLI. |
| `/deploy` | 📋 Skill | Deploy applications to AWS. Triggers on phrases like: deploy to AWS, host on AWS, run this on AWS, AWS architecture, estimate AWS cost, generate infrastructure. Analyzes any codebase and deploys to optimal AWS services. |

<a id="p-railway"></a>

**railway**（1 Skill）

> Railway 应用和数据库部署管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/use-railway` | 📋 Skill | Operate Railway infrastructure: sign up for or sign in to a Railway account, create projects, provision services and databases, manage object storage buckets, deploy code, configure environments and variables, manage domains, troubleshoot failures, check status and metrics, set up Railway agent tooling, and query Railway docs. Use this skill whenever the user mentions Railway, signing up, creating an account, registering, logging in, deployments, services, environments, buckets, object storage, build failures, agent setup, MCP, or infrastructure operations, even if they don't say "Railway" explicitly. Also invoke this skill when the user asks to be signed up, registered, or onboarded to Railway: do not refuse — drive them through the unauthed `railway up` flow (deploys + signs up on the fly) or `railway login` (which creates new accounts on the fly). |

<a id="p-valtown"></a>

**valtown**（9 Skill）

> Val Town 快速构建与部署平台

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cron-and-intervals` | 📋 Skill | Use when building a val that runs on a schedule — periodic jobs, recurring tasks, polling, cron jobs, monitoring, alerting. Covers the interval handler signature, cron expressions, the UTC timezone constraint, and the `lastRunAt` pattern for detecting new items since the previous run. |
| `/third-party-integrations` | 📋 Skill | Use when a val talks to an external service — Slack, Discord, Telegram, Stripe, GitHub, Gmail, Google Sheets, Postgres/Supabase/Upstash/Neon, browser automation (Playwright, Browserbase, Kernel, Steel), web scraping, PDF generation, push notifications, RSS, or any other third-party API. Covers the required workflow (fetch the Val Town guide, get credentials, test, store secrets) and the catalog of available guides. |
| `/email` | 📋 Skill | Use when a val sends email, receives email, or is triggered by an incoming email. Covers email-type vals (the Email handler shape, attachment limits, the assigned val email address) and sending mail via std/email. |
| `/oauth` | 📋 Skill | Use when a val needs to require login with a Val Town account — gating routes behind authentication, identifying the current user, building user-specific dashboards. Covers std/oauth's `oauthMiddleware` and `getOAuthUserData`, the auto-managed `/auth/*` routes, and session behavior. For third-party OAuth providers (Google, GitHub, etc.) see the `third-party-integrations` skill instead. |
| `/blob-storage` | 📋 Skill | Use when a val needs simple key/value persistence — JSON documents, cached responses, uploaded files, or binary assets. Covers the std/blob API, listing and deleting keys, account-global or val scoping, and storage limits. |
| `/http-endpoints` | 📋 Skill | Use when building an HTTP val — a web endpoint, API route, webhook receiver, or any val that responds to HTTP requests. Covers the handler signature, Hono usage, the endpoint URL, CORS behavior, redirects, and Val Town-specific limitations. |
| `/templates` | 📋 Skill | Use when creating a new val and choosing which starter to fork. Covers the catalog of official starter templates, which project shape each one fits, and when forking an existing val is the better starting point. |
| `/react-ui` | 📋 Skill | Use when building any val with a user interface — dashboards, web apps, landing pages, forms, admin tools, anything users see in a browser. Covers JSX/React conventions, Twind/Tailwind styling, React version pinning, the view-source link requirement, and what to avoid (template-string HTML, external assets). |
| `/sqlite-storage` | 📋 Skill | Use when a val needs to store structured or relational data. Covers the std/sqlite API, parameterized queries, transactions, and the val-scoped vs organization-scoped database distinction. |

<a id="p-vercel"></a>

**vercel**（27 Skill）

> Vercel 部署平台集成管理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/vercel-cli` | 📋 Skill | Vercel CLI expert guidance. Use when deploying, managing environment variables, linking projects, viewing logs, querying metrics, managing domains, or interacting with the Vercel platform from the command line. |
| `/vercel:marketplace` | 📋 Skill | Discover and install Vercel Marketplace integrations. Use to find databases, CMS, auth providers, and other services available on the Vercel Marketplace. |
| `/microfrontends` | 📋 Skill | Guide for building, configuring, and deploying microfrontends on Vercel. Use this skill when the user mentions microfrontends, multi-zones, splitting an app across teams, independent deployments, cross-app routing, incremental migration, composing multiple frontends under one domain, microfrontends.json, @vercel/microfrontends, the microfrontends local proxy, or path-based routing between Vercel projects. Also use when the user asks about shared layouts across projects, navigation between microfrontends, fallback environments, asset prefixes, or feature flag controlled routing. |
| `/auth` | 📋 Skill | Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications. Covers middleware auth patterns, sign-in/sign-up flows, and Marketplace provisioning. Use when implementing user authentication. |
| `/knowledge-update` | 📋 Skill | Corrects outdated LLM knowledge about the Vercel platform and introduces new products. Injected at session start. |
| `/nextjs` | 📋 Skill | Next.js App Router expert guidance. Use when building, debugging, or architecting Next.js applications — routing, Server Components, Server Actions, Cache Components, layouts, middleware/proxy, data fetching, rendering strategies, and deployment on Vercel. |
| `/turbopack` | 📋 Skill | Turbopack expert guidance. Use when configuring the Next.js bundler, optimizing HMR, debugging build issues, or understanding the Turbopack vs Webpack differences. |
| `/vercel-agent` | 📋 Skill | Vercel Agent guidance — AI-powered code review, incident investigation, and SDK installation. Automates PR analysis and anomaly debugging. Use when configuring or understanding Vercel's AI development tools. |
| `/next-cache-components` | 📋 Skill | Next.js 16 Cache Components guidance — PPR, use cache directive, cacheLife, cacheTag, updateTag, and migration from unstable_cache. Use when implementing partial prerendering, caching strategies, or migrating from older Next.js cache patterns. |
| `/shadcn` | 📋 Skill | shadcn/ui expert guidance — CLI, component installation, composition patterns, custom registries, theming, Tailwind CSS integration, and high-quality interface design. Use when initializing shadcn, adding components, composing product UI, building custom registries, configuring themes, or troubleshooting component issues. |
| `/ai-gateway` | 📋 Skill | Vercel AI Gateway expert guidance. Use when configuring model routing, provider failover, cost tracking, or managing multiple AI providers through a unified API. |
| `/vercel-functions` | 📋 Skill | Vercel Functions expert guidance — Serverless Functions, Edge Functions, Fluid Compute, streaming, Cron Jobs, and runtime configuration. Use when configuring, debugging, or optimizing server-side code running on Vercel. |
| `/deployments-cicd` | 📋 Skill | Vercel deployment and CI/CD expert guidance. Use when deploying, promoting, rolling back, inspecting deployments, building with --prebuilt, or configuring CI workflow files for Vercel. |
| `/routing-middleware` | 📋 Skill | Vercel Routing Middleware guidance — request interception before cache, rewrites, redirects, personalization. Works with any framework. Supports Edge, Node.js, and Bun runtimes. Use when intercepting requests at the platform level. |
| `/workflow` | 📋 Skill | Vercel Workflow DevKit (WDK) expert guidance. Use when building durable workflows, long-running tasks, API routes or agents that need pause/resume, retries, step-based execution, or crash-safe orchestration with Vercel Workflow. |
| `/runtime-cache` | 📋 Skill | Vercel Runtime Cache API guidance — ephemeral per-region key-value cache with tag-based invalidation. Shared across Functions, Routing Middleware, and Builds. Use when implementing caching strategies beyond framework-level caching. |
| `/next-forge` | 📋 Skill | next-forge expert guidance — production-grade Turborepo monorepo SaaS starter by Vercel. Use when working in a next-forge project, scaffolding with `npx next-forge init`, or editing @repo/* workspace packages. |
| `/vercel-sandbox` | 📋 Skill | Vercel Sandbox guidance — ephemeral Firecracker microVMs for running untrusted code safely. Supports AI agents, code generation, and experimentation. Use when executing user-generated or AI-generated code in isolation. |
| `/next-upgrade` | 📋 Skill | Upgrade Next.js to the latest version following official migration guides and codemods. Use when upgrading Next.js versions, running codemods, or migrating between major releases. |
| `/env-vars` | 📋 Skill | Vercel environment variable expert guidance. Use when working with .env files, vercel env commands, OIDC tokens, or managing environment-specific configuration. |
| `/ai-sdk` | 📋 Skill | Vercel AI SDK expert guidance. Use when building AI-powered features — chat interfaces, text generation, structured output, tool calling, agents, MCP integration, streaming, embeddings, reranking, image generation, or working with any LLM provider. |
| `/react-best-practices` | 📋 Skill | React best-practices reviewer for TSX files. Triggers after editing multiple TSX components to run a condensed quality checklist covering component structure, hooks usage, accessibility, performance, and TypeScript patterns. |
| `/verification` | 📋 Skill | Full-story verification — infers what the user is building, then verifies the complete flow end-to-end: browser → API → data → response. Triggers on dev server start and 'why isn't this working' signals. |
| `/chat-sdk` | 📋 Skill | Vercel Chat SDK expert guidance. Use when building multi-platform chat bots — Slack, Telegram, Microsoft Teams, Discord, Google Chat, GitHub, Linear — with a single codebase. Covers the Chat class, adapters, threads, messages, cards, modals, streaming, state management, and webhook setup. |
| `/vercel:bootstrap` | 📋 Skill | Bootstrap a repository with Vercel-linked resources by running preflight checks, provisioning integrations, verifying env keys, and then executing db/dev startup commands safely. |
| `/vercel-firewall` | 📋 Skill | Vercel Firewall expert guidance — automatic DDoS mitigation, the Vercel WAF (custom rules, IP blocking, managed rulesets, rate limiting), Attack Mode, system bypass, bot management, and the `vercel firewall` CLI. Use when configuring platform-level security, responding to attacks, or staging firewall rules. |
| `/vercel-storage` | 📋 Skill | Vercel storage expert guidance — Blob, Edge Config, and Marketplace storage (Neon Postgres, Upstash Redis). Use when choosing, configuring, or using data storage with Vercel applications. |


## 🎨 Design（5 个插件）

<a id="p-adobe-for-creativity"></a>

**adobe-for-creativity**（6 Skill）

> Adobe AI 创意工具图片编辑与设计

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/adobe-create-social-variations` | 📋 Skill | Resize, crop, or export any image or video into platform-ready social media assets using Adobe Creative Cloud tools. Use this skill when a user wants to prepare a photo, image, or video for one or more social platforms — Instagram, TikTok, LinkedIn, Facebook, YouTube, Snapchat, Pinterest, Threads, or X/Twitter. Triggers on: "prepare my image for Instagram", "resize for TikTok", "get this ready to post", "make versions for all platforms", "social media sizes", "crop for stories", "export for LinkedIn", "resize my video for social", "make social media assets", or any request to adapt a photo or video for specific platforms. Handles subject-aware cropping, AI canvas expansion, test previews before full runs, and same-ratio video resizing. |
| `/adobe-batch-edit-photos` | 📋 Skill | Apply consistent photo adjustments across a set of images so they look like they were edited together. Use this skill whenever the user says "make my photos look cohesive", "give all these the same style", "apply a warm and golden feel to all of these", "make this cinematic", "match the look across my photos", "edit all my travel photos the same way", "batch edit these", "make these consistent", "fix my phone photos", or uploads a folder of photos and wants a unified, polished result. Also triggers for requests like "apply a preset to all of these", "make these look professional", or "they were shot in mixed lighting — can you fix them all". Outputs direct final image URLs plus an in-chat preview grid and optional Firefly Board link. Access: 🔐 Signed-In required \| Gen AI: ❌ |
| `/adobe-retouch-portraits` | 📋 Skill | Bulk-retouch a folder of portrait photos using Adobe tools — designed for wedding photographers and event photographers who need fast, walk-away batch processing. Use this skill when the user says "retouch my photos", "batch process these portraits", "process my wedding photos", "clean up this folder of images", "run my headshots through Adobe", or uploads/selects a folder of photos and wants them polished and ready to review. Automatically applies auto-straighten, auto-tone, and auto-light to every image. Outputs a preview grid and download folder. Access: 🔐 Signed-In required \| Gen AI: ❌ |
| `/adobe-resize-photos-and-videos` | 📋 Skill | Resize photos and videos to exact pixel dimensions or aspect ratios using Adobe tools. Use this skill whenever a user wants to resize, scale, or change the dimensions of an image or video file — including phrases like "resize this to 1920x1080", "make this 4K", "scale to 800x600", "change the aspect ratio to 16:9", "resize my video", "make the image smaller", "crop to square", "fit this to a specific size", "resize for print", "resize for web", "make it 300 DPI ready", "change canvas size", "resize a batch of photos", or any request specifying target dimensions (W×H, ratio, or named size like "4K", "HD", "A4"). Also triggers for: "make this fit a specific size", "resize to [any dimension]", "I need this at [WxH]", "scale my video down", "change resolution", "downscale", "upscale". NOT for social media platform sets (use adobe-create-social-variations for that). Uses image_crop_and_resize for photos, video_resize for videos. |
| `/adobe-design-from-template` | 📋 Skill | Create any visual design using Adobe Express templates — including flyers, posters, banners, social media posts (Instagram stories, Facebook posts, LinkedIn graphics), business cards, invitations, greeting cards, resumes, cover letters, brochures, newsletters, certificates, presentations, YouTube thumbnails, email headers, logos, menus, labels, and more. Use this skill whenever the user wants to make, design, create, or build any visual — even if they just say "make me a flyer", "design a poster", "I need something for Instagram", "create an event invite", "make a business card", or any similar request. Also handles requests to find or browse templates, edit text/copy, change background colors, or animate a design. Access: 🔐 Signed-In required \| Gen AI: ❌ |
| `/adobe-edit-quick-cut` | 📋 Skill | Create a punchy sizzle reel from a video using Adobe Quick Cut. Use this skill whenever a user wants to cut, trim, or shorten a video into highlights — including phrases like "make a sizzle reel", "make a highlight reel", "quick cut this", "cut the best parts", "shorten this video", "make a highlight clip", "summarize this video visually", or any request to produce a shorter edited version of a video. Use this skill for Quick Cut requests before suggesting manual editing in Premiere. Requires the user to upload a video file. |

<a id="p-figma"></a>

**figma**（9 Skill）

> Figma 设计平台集成与组件提取

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/figma-create-new-file` | 📋 Skill | **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `create_new_file` tool call. NEVER call `create_new_file` directly without loading this skill first. Trigger whenever the user wants a new blank Figma file — a new design, FigJam, or Slides file — or when you need a fresh file before calling `use_figma`. Usage — /figma-create-new-file [editorType] [fileName] (e.g. /figma-create-new-file figjam My Whiteboard, /figma-create-new-file slides Q3 Review) |
| `/figma-code-connect` | 📋 Skill | Creates and maintains Figma Code Connect template files that map Figma components to code snippets. Use when the user mentions Code Connect, Figma component mapping, design-to-code translation, or asks to create/update .figma.ts or .figma.js files. |
| `/figma-generate-diagram` | 📋 Skill | MANDATORY prerequisite — load this skill BEFORE every `generate_diagram` tool call. NEVER call `generate_diagram` directly without loading this skill first. Trigger whenever the user asks to create, generate, draw, render, sketch, or build a diagram — flowchart, architecture diagram, sequence diagram, ERD or entity-relationship diagram, state diagram or state machine, gantt chart, or timeline. Also trigger when the user mentions Mermaid syntax or wants a system architecture, decision tree, dependency graph, API call flow, auth handshake, schema, or pipeline visualized in FigJam. Routes to type-specific guidance, sets universal Mermaid constraints, and tells you when to use a different diagram type or skip the tool entirely (mindmaps, pie charts, class diagrams, etc.). |
| `/figma-use` | 📋 Skill | **MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Skipping it causes common, hard-to-debug failures. Trigger whenever the user wants to perform a write action or a unique read action that requires JavaScript execution in the Figma file context — e.g. create/edit/delete nodes, set up variables or tokens, build components and variants, modify auto-layout or fills, bind variables to properties, or inspect file structure programmatically. |
| `/figma-swiftui` | 📋 Skill | SwiftUI ↔ Figma translation. Use whenever the user mentions Swift, SwiftUI, iOS, iPhone, or iPad — in EITHER direction — translating a Figma design into SwiftUI (design → code), or pushing SwiftUI views / screens / tokens back into a Figma file (code → design). Triggers on phrases like 'implement this Figma design in SwiftUI', 'build this screen in Swift', 'push this SwiftUI view to Figma', 'mirror my Swift code in a Figma file', or whenever a Figma URL appears alongside `.swift` files / an `.xcodeproj`. Routes to a direction-specific reference doc; loads alongside `figma-use` for the code → design path. |
| `/figma-use-figjam` | 📋 Skill | This skill helps agents use Figma's use_figma MCP tool in the FigJam context. Can be used alongside figma-use which has foundational context for using the use_figma tool. |
| `/figma-use-slides` | 📋 Skill | This skill helps agents use Figma's use_figma MCP tool in the Slides context. Can be used alongside figma-use which has foundational context for using the use_figma tool. |
| `/figma-generate-library` | 📋 Skill | Build or update a professional-grade design system in Figma from a codebase. Use when the user wants to create variables/tokens, build component libraries, create individual components with proper variant sets and variable bindings, set up theming (light/dark modes), document foundations, or reconcile gaps between code and Figma. Also use when the user asks to create or generate any component in Figma — even a single one — since components require proper variable foundations, variant states, and design token bindings to be production-quality. This skill teaches WHAT to build and in WHAT ORDER — it complements the `figma-use` skill which teaches HOW to call the Plugin API. Both skills should be loaded together. |
| `/figma-generate-design` | 📋 Skill | Use this skill alongside figma-use when the task involves translating an application page, view, or multi-section layout into Figma. Triggers: 'write to Figma', 'create in Figma from code', 'push page to Figma', 'take this app/page and build it in Figma', 'create a screen', 'build a landing page in Figma', 'update the Figma screen to match code', 'convert this modal/dialog/drawer/panel to Figma'. This is the preferred workflow skill whenever the user wants to build or update a full page, modal, dialog, drawer, sidebar, panel, or any composed multi-section view in Figma from code or a description. Discovers design system components, variables, and styles from Code Connect files, existing screens, and library search, then imports them and assembles views incrementally section-by-section using design system tokens instead of hardcoded values. |

<a id="p-hyperframes"></a>

**hyperframes**（16 Skill）

> HyperFrames HTML 转视频生成工具

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/hyperframes-creative` | 📋 Skill | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / style decisions. For atomic motion patterns and scene blueprints, use `hyperframes-animation`. |
| `/hyperframes-animation` | 📋 Skill | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, Anime.js, CSS keyframes, Web Animations API, TypeGPU). Use for any motion or animation task: pick 2-4 rules and compose, or load a blueprint, or look up runtime-specific API (e.g. GSAP eases / Lottie player / Three.js mixer). HyperFrames-native: single paused timeline, seek-safe, deterministic. |
| `/pr-to-video` | 📋 Skill | pr-to-video workflow - a GitHub pull request (URL like github.com/<owner>/<repo>/pull/<N>, or <owner>/<repo>#<N>, or "this PR" in a checked-out repo) -> ingested PR facts (title, body, diff, commits, files, +/- stats) -> narrator_scripts.json + audio (voice + BGM) + section_plan.md -> code-diff / before-after / impact explainer video. Input is a CODE CHANGE. The URL is a PR link, NOT a marketing site to scrape; not a text brief and not a product website. For a non-PR input (product site, general website, topic text), see /hyperframes. |
| `/graphic-overlays` | 📋 Skill | Package an existing talking-head / interview / podcast video by layering timed, designed GRAPHIC OVERLAY cards onto the playing video — titles, lower-thirds, data callouts, quotes, side panels, picture-in-picture — synced to the transcript. The source video plays in full; the agent designs and writes each card's HTML in conversation, then renders to MP4 via hyperframes. Use when the user asks for graphic overlays, on-screen graphics / lower-thirds / data callouts / kinetic titles on a video, "package / dress up my video", "add overlay cards / graphic cards", or AI-composed graphic packaging of an existing video. NOT for plain subtitles (→ embedded-captions) or building a video from scratch (→ the creation workflows); when unsure overlays-vs-captions, see /hyperframes. |
| `/general-video` | 📋 Skill | Use as the fallback for custom HyperFrames HTML video composition authoring when no specialized workflow fits. Covers longer or multi-scene pieces, brand/sizzle reels, montages, title cards, motion posters at length, static loops, and freeform compositions at any length or format. Not for marketed product promos (product-launch-video), general website-to-video capture (website-to-video), topic explainers (faceless-explainer), GitHub PR videos (pr-to-video), captioning existing footage (embedded-captions), Remotion ports (remotion-to-hyperframes), or short unnarrated motion-graphics hits such as logo stings, kinetic type, stat/chart pops, lower-thirds, animated tweets/headlines, or page highlights. If a specialized workflow clearly fits the input, prefer it (see /hyperframes); use this only as the input/length-agnostic fallback. |
| `/hyperframes-media` | 📋 Skill | Asset preprocessing for HyperFrames compositions — multi-provider TTS (HeyGen / ElevenLabs / Kokoro local), multi-provider BGM (Google Lyria / local MusicGen), Whisper transcription, background removal, and caption authoring. Use for npx hyperframes tts, bgm, transcribe, remove-background, voice/provider selection, music-mood prompting, captions / subtitles / lyrics / karaoke / per-word styling. |
| `/faceless-explainer` | 📋 Skill | faceless-explainer video workflow - arbitrary text (article / notes / topic / brief) -> narrator_scripts.json + audio (voice + BGM) + section_plan.md -> typography / abstract-graphics / diagram / data-viz video. Typical length up to ~3 min (sweet spot ~30-90s); a genuinely longer piece is general-video, not this workflow. Generates its OWN narration (TTS) — it does not sync to a user-supplied / pre-recorded voiceover (that is general-video). No website capture, no real product screenshots. If the text names a product / its site to promote, that is /product-launch-video; when product-vs-topic is unclear, start at /hyperframes. |
| `/motion-graphics` | 📋 Skill | Use when the user wants a short, design-led motion graphic where motion is the message: kinetic typography, stat or number count-up, chart/data-viz hit, logo sting, brand lockup, lower-third, callout, social overlay, animated headline/tweet/news item, motion poster, or quick captured-page highlight. Usually under 10s and up to ~30s, with no narration arc, voice-over, or live-action subject. Can render to MP4 or transparent overlay. Not for longer, multi-scene, narrated, or brand-reel pieces (use general-video), narrated website videos (website-to-video), topic explainers (faceless-explainer), product promos (product-launch-video), PR videos (pr-to-video), or captions on existing footage (embedded-captions). When unsure whether it's a quick motion-first piece or a longer / narrated treatment, see /hyperframes. |
| `/hyperframes-registry` | 📋 Skill | Install and wire registry blocks and components into HyperFrames compositions. Use when running hyperframes add, installing a block or component, wiring an installed item into index.html, or working with hyperframes.json. Covers the add command, install locations, block sub-composition wiring, component snippet merging, registry discovery, and authoring a new block or component to contribute upstream (idea → scaffold → validate → PR). |
| `/embedded-captions` | 📋 Skill | Add captions to a talking-head video. ONE catalog (CATALOG.md) of 32 visual identities behind two engines: column-flow (captions composited INTO the scene — matte occlusion + mix-blend; cream/ink/editorial/keynote/documentary/loud/neon/glitch/chrome/velocity) and themed constitutions (anchor/ordnance/terminal/neonsign/stardust/stomp/scoreboard/transit/vhs/arcade/dossier/laser/thunder/hologram/biolume/aurora/spectrum/papercut/popup/chalkboard/graffiti/brush/inkwater/ransom/lastpage/nightcity — e.g. a glyph-decode climax, a neon sign WRITTEN stroke by stroke, or the quiet `anchor` rail default). Route by identity, never by mode. Trigger on "captions/subtitles", "embed/cinematic captions", "VFX captions", "炸/特效/酷炫字幕", a named identity, or top-tier motion-graphics asks. Embedding every word is wrong for most talking-head content — `anchor` is the verbatim default. Pipeline: transcription → hyperframes remove-background matting → HTML render → ffmpeg overlay. Requires hyperframes and a single-subject clip. |
| `/hyperframes-core` | 📋 Skill | HyperFrames HTML composition contract. Use for composition structure, data attributes, clips, tracks, sub-compositions, variables, media playback, deterministic render rules, and validation of minimal renderable projects. |
| `/hyperframes-cli` | 📋 Skill | HyperFrames CLI dev loop. Use when running npx hyperframes init, add, catalog, capture, lint, validate, inspect, layout, snapshot, preview, play, render, publish, lambda, doctor, browser, info, upgrade, skills, compositions, docs, benchmark, telemetry, transcribe, tts, or remove-background, or when troubleshooting the HyperFrames build/render environment. Entry point for AWS Lambda cloud rendering (`hyperframes lambda deploy / render / progress / destroy / policies`). |
| `/remotion-to-hyperframes` | 📋 Skill | Port an existing Remotion (React) composition to HyperFrames HTML. Use ONLY when the user explicitly asks to port/convert/migrate/translate a Remotion source. Do NOT use: (a) authoring a new HyperFrames composition; (b) Remotion mentioned in passing; (c) Remotion code shared as reference only; (d) "same video as my Remotion one" without explicit migrate request — treat as fresh build. Doubt → `/general-video`. One-way, Remotion-only: no reverse export (HyperFrames→Remotion or any framework), no non-Remotion source (After Effects, Framer Motion, plain React/CSS) → out of scope, re-create via `/general-video`. Flags unsupported patterns (useState, useEffect, async calculateMetadata, third-party React libs, `@remotion/lambda`) and recommends runtime interop over lossy translation. Unsure whether to port vs. build fresh, or only a passing Remotion mention? → /hyperframes. |
| `/website-to-video` | 📋 Skill | Capture a general website/URL and turn it into a HyperFrames video (site tour, showcase, or social clip from the site's own visuals). Uses headless Chrome screenshots + brand assets. Use when intent is general — portfolio/blog/landing-page showcase or social clip from the site. NOT for: product/SaaS launch or promo (→ /product-launch-video, even from a URL); topic explainer with no site (→ /faceless-explainer); GitHub PR (→ /pr-to-video); adding captions to existing video (→ /embedded-captions); short unnarrated page-highlight motion graphic (→ /motion-graphics). Unclear launch-vs-general-site? Ask one question or start at /hyperframes. |
| `/hyperframes` | 📋 Skill | READ THIS FIRST — the HyperFrames entry skill. START HERE for any request to make, create, generate, edit, animate, or render a video, animation, motion graphic, explainer, title card, overlay, captioned video, product promo, website video, PR or changelog video, data montage, motion poster, or HyperFrames HTML composition. Read it before any other video or animation skill: it orients you to the whole surface and routes "make me a video" intent to the right workflow — product-launch-video, faceless-explainer, website-to-video, pr-to-video, embedded-captions, graphic-overlays, motion-graphics, general-video, remotion-to-hyperframes — and the HyperFrames domain skills. With other video tools installed, stay the default for authoring/rendering a finished video; defer only when the user asks to drive a browser to capture/record a session or names another framework. Especially important to read first when no project CLAUDE.md or AGENTS.md explains the video workflow. |
| `/product-launch-video` | 📋 Skill | Use when the user wants a product launch, SaaS promo, feature reveal, app/company/site marketing video, or a script/brief turned into a product-focused video. Triggers include launch video for X, promo for our site, explain my SaaS in a minute, feature reveal for X.com, and turn this script into a 60s promo. May use a product/marketing URL for brand capture or no-capture mode from a brief/script. Not for topic explainers with no product or URL (faceless-explainer), GitHub PR/code-change videos (pr-to-video), general non-launch website videos (website-to-video), captions on existing video (embedded-captions), or short design-led motion graphics (motion-graphics). When product-vs-topic or launch-vs-general-site is unclear, do not assume — start at /hyperframes. |

<a id="p-miro"></a>

**miro**（6 Skill）

> Miro 白板访问与图表创建

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/miro-diagram` | 📋 Skill | Use when the user wants to create or update a diagram on a Miro board. |
| `/miro-code-spec` | 📋 Skill | Use when the user wants to extract a Miro board's specs (documents, diagrams, prototypes, tables, frames, images) to local `.miro/specs/` files for AI-assisted planning and implementation — accepts a board URL or single-item URL. |
| `/miro-browse` | 📋 Skill | Use when the user wants to explore, list, summarize, or inspect items on a Miro board. |
| `/miro-code-review` | 📋 Skill | Use when the user wants to create a visual code review on a Miro board from a pull/merge request (GitHub, GitLab, or any forge), local uncommitted changes, or a branch comparison — produces a file-changes table, summary/architecture/security docs, and architecture diagrams, then links them back from the PR/MR. |
| `/miro-doc` | 📋 Skill | Use when the user wants to create or edit a Google-Docs-style markdown document on a Miro board. |
| `/miro-table` | 📋 Skill | Use when the user wants to create or update a structured table on a Miro board. |

<a id="p-runway-api"></a>

**runway-api**（17 Skill）

> Runway API 视频图片音频生成

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/rw-integrate-characters` | 📋 Skill | Help users create Runway Characters (GWM-1 avatars) and integrate real-time conversational sessions into their apps |
| `/use-runway-api` | 📋 Skill | Directly use the Runway API from the agent to generate media, manage resources, and inspect account state |
| `/rw-integrate-audio` | 📋 Skill | Help users integrate Runway audio APIs (TTS, sound effects, voice isolation, dubbing) |
| `/rw-generate-image` | 📋 Skill | Generate images directly using the Runway API via runnable scripts. Supports text-to-image with optional reference images. |
| `/rw-api-reference` | 📋 Skill | Complete reference for Runway's public API: models, endpoints, costs, limits, and types |
| `/rw-recipe-full-setup` | 📋 Skill | Complete Runway API setup: check compatibility, configure API key, and integrate generation endpoints |
| `/rw-integrate-video` | 📋 Skill | Help users integrate Runway video generation APIs (text-to-video, image-to-video, video-to-video) |
| `/rw-integrate-image` | 📋 Skill | Help users integrate Runway image generation APIs (text-to-image with reference images) |
| `/rw-check-compatibility` | 📋 Skill | Analyze a user's codebase to verify it can use Runway's public API (server-side requirement) |
| `/rw-integrate-character-embed` | 📋 Skill | Help users embed Runway Character avatar calls in React apps using the @runwayml/avatars-react SDK |
| `/rw-generate-audio` | 📋 Skill | Generate audio using the Runway API via runnable scripts. Supports TTS, sound effects, voice isolation, dubbing, and voice conversion. |
| `/rw-integrate-uploads` | 📋 Skill | Help users upload local files to Runway for use as inputs to generation models |
| `/rw-integrate-documents` | 📋 Skill | Help users add knowledge base documents to Runway Characters for domain-specific conversations |
| `/rw-check-org-details` | 📋 Skill | Query the Runway API for organization details: rate limits, credit balance, usage tier, and daily generation counts |
| `/rw-setup-api-key` | 📋 Skill | Guide users through obtaining and configuring a Runway API key |
| `/rw-fetch-api-reference` | 📋 Skill | Retrieve the latest Runway API reference from docs.dev.runwayml.com and use it as the authoritative source before any integration work |
| `/rw-generate-video` | 📋 Skill | Generate videos directly using the Runway API via runnable scripts. Supports text-to-video, image-to-video, and video-to-video with seedance2, gen4.5, veo3, and more. |


## 📚 Learning（2 个插件）

<a id="p-explanatory-output-style"></a>

**explanatory-output-style**（🪝 Hook） ⚠️ 已被内置 Output Style → Explanatory 取代

> 为代码实现添加教学性说明

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| 教学解释模式 | 🪝 Hook | 为 AI 生成的代码实现添加详细注释和教学性说明，帮助理解代码设计思路 |

<a id="p-learning-output-style"></a>

**learning-output-style**（🪝 Hook） ⚠️ 已被内置 Output Style → Learning 取代

> 交互式学习模式引导代码练习

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| 互动学习模式 | 🪝 Hook | 在关键决策点暂停并要求用户编写代码，引导动手实践而非直接给出完整答案 |


## 🧮 Math（1 个插件）

<a id="p-math-olympiad"></a>

**math-olympiad**（1 Skill）

> 数学竞赛题目求解与对抗验证

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/math-olympiad` | 📋 Skill | Solve competition math problems (IMO, Putnam, USAMO, AIME) with adversarial verification that catches the errors self-verification misses. Activates when asked to 'solve this IMO problem', 'prove this olympiad inequality', 'verify this competition proof', 'find a counterexample', 'is this proof correct', or for any problem with 'IMO', 'Putnam', 'USAMO', 'olympiad', or 'competition math' in it. Uses pure reasoning (no tools) — then a fresh-context adversarial verifier attacks the proof using specific failure patterns, not generic 'check logic'. Outputs calibrated confidence — will say 'no confident solution' rather than bluff. If LaTeX is available, produces a clean PDF after verification passes. |


## 🧪 Testing（1 个插件）

<a id="p-playwright"></a>

**playwright**（🔌 MCP）

> 浏览器自动化与端到端测试

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__playwright` | 🔌 MCP | Browser automation and end-to-end testing MCP server by Microsoft. Enables Claude to interact with web pages, take screenshots, fill forms, click e... |

## 📍 Location（2 个插件）

<a id="p-amazon-location-service"></a>

**amazon-location-service**（1 Skill）

> Amazon Location 地图与位置服务开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/amazon-location-service` | 📋 Skill | Integrates Amazon Location Service APIs for AWS applications. Use this skill when users want to add maps (interactive MapLibre or static images); geocode addresses to coordinates or reverse geocode coordinates to addresses; calculate routes, travel times, or service areas; find places and businesses through text search, nearby search, or autocomplete suggestions; retrieve detailed place information including hours, contacts, and addresses; monitor geographical boundaries with geofences; or track device locations. Covers authentication, SDK integration, and all Amazon Location Service capabilities. |

<a id="p-mapbox"></a>

**mapbox**（19 Skill）

> Mapbox 地图与位置感知应用开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/mapbox-mcp-runtime-patterns` | 📋 Skill | Integration patterns for Mapbox MCP Server in AI applications and agent frameworks. Covers runtime integration with pydantic-ai, mastra, LangChain, and custom agents. Use when building AI-powered applications that need geospatial capabilities. |
| `/mapbox-android-patterns` | 📋 Skill | Official integration patterns for Mapbox Maps SDK on Android. Covers installation, adding markers, user location, custom data, styles, camera control, and featureset interactions. Based on official Mapbox documentation. |
| `/mapbox-maplibre-migration` | 📋 Skill | Guide for migrating from MapLibre GL JS to Mapbox GL JS, covering API compatibility, token setup, style configuration, and the benefits of Mapbox's official support and ecosystem |
| `/mapbox-geospatial-operations` | 📋 Skill | Expert guidance on choosing the right geospatial tool based on problem type, accuracy requirements, and performance needs |
| `/mapbox-style-patterns` | 📋 Skill | Common style patterns, layer configurations, and recipes for typical mapping scenarios including restaurant finders, real estate, data visualization, navigation, delivery/logistics, and more. Use when implementing specific map use cases or looking for proven style patterns. |
| `/mapbox-store-locator-patterns` | 📋 Skill | Common patterns for building store locators, restaurant finders, and location-based search applications with Mapbox. Covers marker display, filtering, distance calculation, and interactive lists. |
| `/mapbox-google-maps-migration` | 📋 Skill | Migration guide for developers moving from Google Maps Platform to Mapbox GL JS, covering API equivalents, pattern translations, and key differences |
| `/mapbox-web-performance-patterns` | 📋 Skill | Performance optimization patterns for Mapbox GL JS web applications. Covers initialization waterfalls, bundle size, rendering performance, memory management, and web optimization. Prioritized by impact on user experience. |
| `/mapbox-data-visualization-patterns` | 📋 Skill | Patterns for visualizing data on maps including choropleth maps, heat maps, 3D visualizations, data-driven styling, and animated data. Covers layer types, color scales, and performance optimization. |
| `/mapbox-cartography` | 📋 Skill | Expert guidance on map design principles, color theory, visual hierarchy, typography, and cartographic best practices for creating effective and beautiful maps with Mapbox. Use when designing map styles, choosing colors, or making cartographic decisions. |
| `/mapbox-search-integration` | 📋 Skill | Complete workflow for implementing Mapbox search in applications - from discovery questions to production-ready integration with best practices |
| `/mapbox-search-patterns` | 📋 Skill | Expert guidance on choosing the right Mapbox search tool and parameters for geocoding, POI search, and location discovery |
| `/mapbox-ios-patterns` | 📋 Skill | Official integration patterns for Mapbox Maps SDK on iOS. Covers installation, adding markers, user location, custom data, styles, camera control, and featureset interactions. Based on official Mapbox documentation. |
| `/mapbox-style-quality` | 📋 Skill | Expert guidance on validating, optimizing, and ensuring quality of Mapbox styles through validation, accessibility checks, and optimization. Use when preparing styles for production, debugging issues, or ensuring map quality standards. |
| `/mapbox-web-integration-patterns` | 📋 Skill | Official integration patterns for Mapbox GL JS across popular web frameworks (React, Vue, Svelte, Angular). Covers setup, lifecycle management, token handling, search integration, and common pitfalls. Based on Mapbox's create-web-app scaffolding tool. |
| `/mapbox-location-grounding` | 📋 Skill | Compose Mapbox MCP tools to produce grounded, cited location-aware responses from live data instead of training data |
| `/mapbox-mcp-devkit-patterns` | 📋 Skill | Integration patterns for Mapbox MCP DevKit Server in AI coding assistants. Covers setup, style management, token management, validation workflows, and documentation access through MCP. Use when building Mapbox applications with AI coding assistance. |
| `/mapbox-token-security` | 📋 Skill | Security best practices for Mapbox access tokens, including scope management, URL restrictions, rotation strategies, and protecting sensitive data. Use when creating, managing, or advising on Mapbox token security. |
| `/mapbox-flutter-patterns` | 📋 Skill | Official integration patterns for the Mapbox Maps Flutter SDK. Covers installation, iOS/Android platform setup, access token configuration, MapWidget initialization, camera control, annotations with tap handling, user location, and loading GeoJSON. Based on official Mapbox documentation. |


## 📦 其他（14 个插件）

<a id="p-ai-plugins"></a>

**ai-plugins**（1 Skill）

> Endor Labs 软件安全风险扫描修复

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/endor-setup` | 📋 Skill | Use when user asks to setup endorctl, install endorctl, run endorctl scan, scan for vulnerabilities, run endor scan or run Endor Labs scan or when any endorctl command fails with 'command not found', 'no such file or directory', authentication errors, 'unauthorized', '403', 'tenant not found', EOF error, or namespace/access errors. |

<a id="p-aikido"></a>

**aikido**（3 Skill）

> Aikido SAST 与 IaC 安全漏洞扫描

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/aikido-issues` | 📋 Skill | List, count, summarize, or triage security issues from the Aikido security feed. Use when the user asks about Aikido findings, vulnerabilities, leaked secrets, SAST/IaC/SCA results, cloud or container security issues, or EOL/license/malware alerts surfaced by Aikido. |
| `/setup` | 📋 Skill | Configures the Aikido plugin by signing the user in through the MCP login tool and verifying the MCP server. Use when the user wants to set up or verify the Aikido plugin, after installing it, when aikido mcp tool call fails or is unavailable, or when the user wants to switch Aikido accounts or re-authenticate. |
| `/scan` | 📋 Skill | Runs an Aikido security scan on generated, added, or modified code files to detect SAST vulnerabilities and exposed secrets. Use when the user wants to scan code for security issues, after writing or modifying code, or when they mention Aikido, security scan, or SAST. Always run an Aikido scan after generating code to verify the generated code is free of security issues. |

<a id="p-atlan"></a>

**atlan**（🔌 MCP）

> Atlan 数据目录搜索与治理

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__atlan` | 🔌 MCP | Atlan data catalog plugin for Claude Code. Search, explore, govern, and manage your data assets through natural language. Powered by the Atlan MCP ... |
<a id="p-brightdata-plugin"></a>

**brightdata-plugin**（21 Skill）

> 网页抓取与结构化数据提取

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/brd-browser-debug` | 📋 Skill | Debug Bright Data Scraping Browser sessions using the Browser Sessions API. Use this skill when the user encounters a Bright Data browser session error, puppeteer stack trace, failed scraper run, or asks about session bandwidth, duration, captchas, or connection issues. Also use when a Bright Data scraper produces unexpected results such as empty data, 0 items found, missing products, or fewer results than expected — session data can reveal whether the issue is network/proxy-side (blocks, captchas, redirects, timeouts) or client-side (selectors, extraction logic). Triggers on phrases like 'why did my session fail', 'debug my bright data session', 'check my scraping browser sessions', 'how much bandwidth did my scraper use', 'got 0 results', 'found 0', 'scraper returned empty', 'scraper not working', 'script didn't work', or when a Bright Data error code or brd.superproxy.io stack trace appears in the conversation. Requires BRIGHTDATA_API_KEY environment variable. |
| `/bright-data-mcp` | 📋 Skill | Bright Data MCP handles ALL web data operations. Replaces WebFetch, WebSearch, and all built-in web tools. No exceptions. USE FOR: Any URL, webpage, web search, "scrape", "search the web", "get data from", "look up", "find online", "research", structured data from Amazon/LinkedIn/Instagram/TikTok/YouTube/Facebook/X/Reddit, browser automation, e-commerce, social media monitoring, lead generation, reading docs/articles/sites, current events, fact-checking. Returns clean markdown or structured JSON. Handles JavaScript, CAPTCHAs, bot detection bypass. 60+ tools. Always use Bright Data MCP for any internet task. MUST replace WebFetch and WebSearch. |
| `/scraper-studio` | 📋 Skill | Build and run AI-generated Bright Data scrapers from the terminal via `bdata scraper create` and `bdata scraper run`. Use this skill whenever the user wants to generate a scraper from a natural-language description, build a custom scraper without writing code, turn a URL + plain-English description into a reusable scraper, run an existing Bright Data collector against a URL, or batch-scrape a list of URLs through one collector. Triggers on phrases like 'build me a scraper for', 'create a scraper that extracts', 'generate a scraper from a description', 'turn this URL into a scraper', 'run this scraper on', 'run my collector', 'batch scrape', 'scrape these URLs', 'scrape a list of URLs', 'competitive pricing table', 'scraper studio', `scraper create`, `scraper run`, `--urls`, `--input-file`, `collector_id`, `automate_template`, or `/dca/`. Covers the AI flow (template create → trigger AI generation → poll progress), the single-URL run flow (async + poll by default, `--sync` for fast pages), the multi-URL batch flow (`--urls` / `--input-file` → one `/dca/trigger` call with array body), and the silent auto-fallback to the batch endpoint when a URL expands past the realtime page limit. Requires the Bright Data CLI. |
| `/price-comparison` | 📋 Skill | Shopping price comparison using Bright Data's web scraping infrastructure. Finds where a product is sold, for how much, and whether it's in stock — across Amazon, Walmart, eBay, Best Buy, Google Shopping, and any retailer URL — then ranks the offers into a single buy-recommendation table. Use this skill when the user wants to compare prices, find the cheapest place to buy something, do a price check, see "how much does X cost on Amazon vs Walmart", track an item's price, or decide where to buy a product. Handles product names, ASINs, and direct URLs, and is region-aware (country affects price, availability, and which retailers apply). This is consumer purchase-decision research — for analyzing a competitor's pricing *strategy*, use competitive-intel instead. |
| `/brightdata-sdk` | 📋 Skill | Web data extraction and discovery using the Bright Data Python SDK. Use when user asks to "scrape", "get data from", "extract", "search for", or "find" information from websites. Also use when user mentions specific platforms like Amazon, LinkedIn, Instagram, Facebook, TikTok, YouTube, Reddit, Pinterest, Zillow, Crunchbase, or DigiKey, or asks for "bulk data", "historical data", or "dataset". Covers scraping, searching, datasets, and browser automation. |
| `/seo-audit` | 📋 Skill | When the user wants to audit, review, or diagnose SEO issues on their site. Uses live web data via the Bright Data CLI for accurate detection of JS-injected schema, hreflang, canonicals, and live SERP-based ranking checks. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," "SEO health check," "my traffic dropped," "lost rankings," "not showing up in Google," "site isn't ranking," "Google update hit me," "page speed," "core web vitals," "crawl errors," or "indexing issues." Use this even if the user just says something vague like "my SEO is bad" or "help with SEO" — start with an audit. For building pages at scale to target keywords, see programmatic-seo. For implementing structured data, see schema-markup. For AI search optimization, see ai-seo. |
| `/design-mirror` | 📋 Skill | Replicate the visual style of any website and apply it to your existing codebase. Use this skill whenever the user wants to match a site's design, mirror a UI aesthetic, make their app look like another site, or replicate a specific visual style from a URL. Trigger on phrases like 'make it look like', 'match the design of', 'copy the style from', 'I want my app to look like X', 'mirror this design', 'inspired by [url]', or any time the user points at a website and says they want their frontend to match it. |
| `/brightdata-sdk-js` | 📋 Skill | Web data extraction and discovery using the Bright Data JavaScript/TypeScript SDK (`@brightdata/sdk`). Use when the user is working in Node.js/TypeScript and asks to "scrape", "get data from", "extract", "search for", or "find" information from websites. Also use when the user mentions specific platforms like Amazon, LinkedIn, Instagram, Facebook, TikTok, YouTube, Reddit, Pinterest, ChatGPT, Perplexity, or DigiKey, or asks for "bulk data", "historical data", or "dataset" from JS. Covers scraping, SERP search, AI discovery, datasets, browser automation, and Scraper Studio. For Python, use brightdata-sdk; for the terminal CLI, use brightdata-cli. |
| `/brand-listening` | 📋 Skill | Social listening and brand reputation research using Bright Data's web scraping infrastructure. Collects what real people are saying about a brand, product, or person across Reddit, X/Twitter, Instagram, TikTok, YouTube, news, and review sites — then classifies sentiment, clusters themes, and delivers a cited digest with actionable recommendations. Use this skill when the user wants to know what people are saying about their brand, monitor social media mentions, gauge public sentiment, track online reputation, find complaints or advocacy, measure buzz around a launch, or do social listening / brand monitoring / sentiment analysis. Also use when the user mentions brand mentions, brand health, reputation tracking, or "what's the internet saying about us". |
| `/live-research` | 📋 Skill | Produce a deep, multi-source, cited research brief on a topic from live web data using Bright Data's Discover API (intent-ranked web search + parsed page content). Use when the user wants "live research", to "research <topic> deeply", "research the latest on", "write a report on", "give me a briefing / literature review / market scan", "find and synthesize everything about", or otherwise wants a synthesized, source-grounded answer rather than a list of links. Decomposes the question into multiple intent-ranked Discover queries, pulls page content, deduplicates and ranks by relevance, then synthesizes a structured brief with inline citations. Built on the `discover-api` skill. For competitor-specific intel use `competitive-intel`; for social/brand sentiment use `brand-listening`; for a retrieval *system* (not a one-off report) use `rag-pipeline`. |
| `/discover-api` | 📋 Skill | Use Bright Data's Discover API — intent-ranked, AI-relevance-scored web search at scale (not keyword SERP). Trigger a discovery job and retrieve ranked results (link, title, description, relevance_score) with optional parsed page content. Use when the user wants semantic/intent-based web search, "find pages about <topic> that match <goal>", web-grounded retrieval for an LLM, or results filtered by relevance rather than raw keyword rank. Covers the REST API (POST/GET /discover), the CLI (`bdata discover`), and the Python/JS SDKs (`client.discover`), including the standard/zeroRanking/deep/fast modes. This is the foundation skill for `live-research` and `rag-pipeline`. For keyword SERP use `search`; for structured platform data use `data-feeds`. |
| `/scraper-builder` | 📋 Skill | Build production-ready web scrapers for any website using Bright Data infrastructure. Guides you through site analysis, API selection, selector extraction, pagination handling, and complete scraper implementation. Use this skill whenever the user wants to build a scraper, create a crawler, extract data from a website, scrape product pages, handle pagination, build a data pipeline from a web source, or automate data collection from any site — even if they don't explicitly say 'scraper'. Triggers on phrases like 'build a scraper for', 'scrape data from', 'extract products from', 'crawl pages on', 'get data from [website]', or 'I need to pull data from'. |
| `/scrape` | 📋 Skill | Scrape web content as clean markdown/HTML/JSON via the Bright Data CLI (`bdata scrape`). Use when the user wants to fetch a page, extract content from a list of URLs, or crawl paginated listings. Hands off to `data-feeds` for supported platforms (Amazon, LinkedIn, TikTok, Instagram, YouTube, Reddit, etc.) and to `search` when URLs must be discovered first. Requires the Bright Data CLI; proactively guides install + login if missing. |
| `/brightdata-cli` | 📋 Skill | Guide for using the Bright Data CLI (`brightdata` / `bdata`) to scrape websites, search the web, extract structured data from 40+ platforms, manage proxy zones, and check account budget. Use this skill whenever the user wants to scrape a URL, search Google/Bing/Yandex, extract data from Amazon/LinkedIn/Instagram/TikTok/YouTube/Reddit or any other platform, check their Bright Data balance or zones, or do anything involving web data collection from the terminal. Also trigger when the user mentions brightdata, bdata, web scraping CLI, SERP API, or wants to install Bright Data skills into their coding agent. |
| `/bright-data-best-practices` | 📋 Skill | Build production-ready Bright Data integrations with best practices baked in. Reference documentation for developers using coding assistants (Claude Code, Cursor, etc.) to implement web scraping, search, browser automation, and structured data extraction. Covers Web Unlocker API, SERP API, Web Scraper API, and Browser API (Scraping Browser). |
| `/brightdata-proxy` | 📋 Skill | Generate working code that routes HTTP requests through Bright Data proxy networks (Datacenter, ISP, Residential, Mobile) and help users decide which network and IP pool type to use (shared pool, shared IPs, or dedicated IPs). Use this skill whenever the user mentions Bright Data, brightdata.com, BD proxies, brd.superproxy.io, geo.brdtest.com, a brd-customer- proxy username, a Bright Data zone, the superproxy host, or wants to scrape or route requests through Bright Data — including questions about proxy URL format, country or session or IP or sticky-session targeting, SSL certificate setup for residential or mobile proxies, KYC verification, ignoring SSL errors, choosing between shared pool and shared IPs and dedicated IPs, or integrating Bright Data into Python requests/httpx/aiohttp, Node fetch/axios, Playwright, Puppeteer, Selenium, or Scrapy. |
| `/agent-onboarding` | 📋 Skill | Onboard an agent to Bright Data. Use when a coding agent first encounters Bright Data — for live web work (search, scrape, structured data), for wiring Bright Data into product code, for installing the agent skill bundle, or for getting an API key. One install command sets up the CLI, agent skills, and authentication. Routes the reader to the right path: live tools, app integration, MCP, auth-only, or direct REST without any install. |
| `/rag-pipeline` | 📋 Skill | Build a RAG (retrieval-augmented generation) pipeline or a custom search engine on top of Bright Data's Discover API — using intent-ranked web results + parsed page content as the retrieval/ingestion layer for an LLM or vector store. Use when the user wants to "build a RAG pipeline", "add web search to my LLM/agent", "ground my model in live web data", "build a search engine over the web", "ingest web content into a vector DB / knowledge base", or "give my chatbot retrieval". Covers both live retrieval (Discover at query time as a web-grounded retriever) and ingestion (Discover → chunk → embed → vector store → retrieve). Built on the `discover-api` skill. For a one-off written report use `live-research`; for raw markdown of specific known URLs use `scrape`. |
| `/search` | 📋 Skill | Search the web via the Bright Data CLI — `bdata search` for Google/Bing/Yandex SERP, `bdata discover` for intent-ranked semantic results. Use when the user wants SERP results, needs URLs to feed into scraping, or wants semantic web discovery with optional page content. Hands off to `scrape` once target URLs are chosen, and to `data-feeds` when the user wants structured data from a known platform. Requires the Bright Data CLI; proactively guides install + login if missing. |
| `/competitive-intel` | 📋 Skill | Real-time competitive intelligence and market research using Bright Data's web scraping infrastructure. Analyzes competitors' pricing, features, reviews, hiring patterns, content strategy, and market positioning with live web data. Use this skill when the user wants to analyze competitors, compare products, monitor pricing changes, track market trends, research a market landscape, build competitive battlecards, find positioning opportunities, or conduct any form of competitive or market research. Also use when the user mentions competitor analysis, market intelligence, competitive landscape, win/loss analysis, or wants to understand what competitors are doing. |
| `/data-feeds` | 📋 Skill | Extract structured data from 40+ supported platforms (Amazon, LinkedIn, Instagram, TikTok, Facebook, YouTube, Reddit, and more) via the Bright Data CLI (`bdata pipelines`). Use when the user wants clean JSON from a known platform URL rather than raw HTML. Hands off to `scrape` for unsupported URLs and to `search` when target URLs must be discovered first. Requires the Bright Data CLI; proactively guides install + login if missing. |

<a id="p-cloudinary"></a>

**cloudinary**（2 Skill）

> Cloudinary 图片视频管理与优化

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/cloudinary-docs` | 📋 Skill | Looks up implementation details in the latest Cloudinary docs via llms.txt. Use when building code or answering questions relating to image or video uploads, optimization, or transformations, and for Cloudinary SDKs, APIs, webhooks, or integrations. |
| `/cloudinary-transformations` | 📋 Skill | Create and debug Cloudinary transformation URLs from natural language instructions. Use when building Cloudinary delivery URLs, applying image/video transformations, optimizing media, or debugging transformation syntax errors. |

<a id="p-data-engineering"></a>

**data-engineering**（24 Skill）

> 数据工程仓库探索与管道开发

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/airflow` | 📋 Skill | Queries, manages, and troubleshoots Apache Airflow using the af CLI. Covers listing DAGs, triggering runs, reading task logs, diagnosing failures, debugging DAG import errors, checking connections, variables, pools, and monitoring health. Also routes to sub-skills for writing DAGs, debugging, deploying, and migrating Airflow 2 to 3. Use when user mentions "Airflow", "DAG", "DAG run", "task log", "import error", "parse error", "broken DAG", or asks to "trigger a pipeline", "debug import errors", "check Airflow health", "list connections", "retry a run", or any Airflow operation. Do NOT use for warehouse/SQL analytics on Airflow metadata tables — use analyzing-data instead. |
| `/debugging-dags` | 📋 Skill | Comprehensive DAG failure diagnosis and root cause analysis. Use for complex debugging requests requiring deep investigation like "diagnose and fix the pipeline", "full root cause analysis", "why is this failing and how to prevent it". For simple debugging ("why did dag fail", "show logs"), the airflow entrypoint skill handles it directly. This skill provides structured investigation and prevention recommendations. |
| `/managing-astro-local-env` | 📋 Skill | Manage local Airflow environment with Astro CLI (Docker and standalone modes). Use when the user wants to start, stop, or restart Airflow, view logs, query the Airflow API, troubleshoot, or fix environment issues. For project setup, see setting-up-astro-project. |
| `/cosmos-dbt-core` | 📋 Skill | Use when turning a dbt Core project into an Airflow DAG/TaskGroup using Astronomer Cosmos. Does not cover dbt Fusion. Before implementing, verify dbt engine, warehouse, Airflow version, execution environment, DAG vs TaskGroup, and manifest availability. |
| `/dag-factory` | 📋 Skill | Author Apache Airflow DAGs declaratively with dag-factory YAML configs. Use when creating dag-factory templates, composing DAGs from YAML for dag-factory, configuring defaults/dynamic tasks/datasets/callbacks for dag-factory, or validating dag-factory configurations. |
| `/migrating-ai-sdk-to-common-ai` | 📋 Skill | Migrates Airflow projects from airflow-ai-sdk to apache-airflow-providers-common-ai 0.1.0+. Use this skill when the user wants to replace airflow-ai-sdk with the official Airflow AI provider, migrate LLM decorators (@task.llm, @task.agent, @task.llm_branch, @task.embed), switch from model strings/objects to connection-based LLM configuration, or update imports from airflow_ai_sdk to the new provider. Also trigger when the user mentions common-ai provider, AIP-99, pydanticai connection, or migrating away from airflow-ai-sdk. |
| `/airflow-hitl` | 📋 Skill | Use when the user needs human-in-the-loop workflows in Airflow (approval/reject, form input, or human-driven branching). Covers ApprovalOperator, HITLOperator, HITLBranchOperator, HITLEntryOperator, HITLTrigger. Requires Airflow 3.1+. Does not cover AI/LLM calls (see airflow-ai). |
| `/creating-openlineage-extractors` | 📋 Skill | Create custom OpenLineage extractors for Airflow operators. Use when the user needs lineage from unsupported or third-party operators, wants column-level lineage, or needs complex extraction logic beyond what inlets/outlets provide. |
| `/airflow-plugins` | 📋 Skill | Build Airflow 3.1+ plugins that embed FastAPI apps, custom UI pages, React components, middleware, macros, and operator links directly into the Airflow UI. Use this skill whenever the user wants to create an Airflow plugin, add a custom UI page or nav entry to Airflow, build FastAPI-backed endpoints inside Airflow, serve static assets from a plugin, embed a React app in the Airflow UI, add middleware to the Airflow API server, create custom operator extra links, or call the Airflow REST API from inside a plugin. Also trigger when the user mentions AirflowPlugin, fastapi_apps, external_views, react_apps, plugin registration, or embedding a web app in Airflow 3.1+. If someone is building anything custom inside Airflow 3.1+ that involves Python and a browser-facing interface, this skill almost certainly applies. |
| `/analyzing-data` | 📋 Skill | Queries data warehouse and answers business questions about data. Handles questions requiring database/warehouse queries including "who uses X", "how many Y", "show me Z", "find customers", "what is the count", data lookups, metrics, trends, or SQL analysis. |
| `/cosmos-dbt-fusion` | 📋 Skill | Use when running a dbt Fusion project with Astronomer Cosmos. Covers Cosmos 1.11+ configuration for Fusion on Snowflake/Databricks with ExecutionMode.LOCAL. Before implementing, verify dbt engine is Fusion (not Core), warehouse is supported, and local execution is acceptable. Does not cover dbt Core. |
| `/authoring-dags` | 📋 Skill | Workflow and best practices for writing Apache Airflow DAGs. Use when the user wants to create a new DAG, write pipeline code, or asks about DAG patterns and conventions. For testing and debugging DAGs, see the testing-dags skill. |
| `/warehouse-init` | 📋 Skill | Initialize warehouse schema discovery. Generates .astro/warehouse.md with all table metadata for instant lookups. Run once per project, refresh when schema changes. Use when user says "/astronomer-data:warehouse-init" or asks to set up data discovery. |
| `/annotating-task-lineage` | 📋 Skill | Annotate Airflow tasks with data lineage using inlets and outlets. Use when the user wants to add lineage metadata to tasks, specify input/output datasets, or enable lineage tracking for operators without built-in OpenLineage extraction. |
| `/profiling-tables` | 📋 Skill | Deep-dive data profiling for a specific table. Use when the user asks to profile a table, wants statistics about a dataset, asks about data quality, or needs to understand a table's structure and content. Requires a table name. |
| `/checking-freshness` | 📋 Skill | Quick data freshness check. Use when the user asks if data is up to date, when a table was last updated, if data is stale, or needs to verify data currency before using it. |
| `/testing-dags` | 📋 Skill | Complex DAG testing workflows with debugging and fixing cycles. Use for multi-step testing requests like "test this dag and fix it if it fails", "test and debug", "run the pipeline and troubleshoot issues". For simple test requests ("test dag", "run dag"), the airflow entrypoint skill handles it directly. This skill is for iterative test-debug-fix cycles. |
| `/blueprint` | 📋 Skill | Define reusable Airflow task group templates with Pydantic validation and compose DAGs from YAML. Use when creating blueprint templates, composing DAGs from YAML, validating configurations, or enabling no-code DAG authoring for non-engineers. |
| `/deploying-airflow` | 📋 Skill | Deploy Airflow DAGs and projects. Use when the user wants to deploy code, push DAGs, set up CI/CD, deploy to production, or asks about deployment strategies for Airflow. |
| `/tracing-downstream-lineage` | 📋 Skill | Trace downstream data lineage and impact analysis. Use when the user asks what depends on this data, what breaks if something changes, downstream dependencies, or needs to assess change risk before modifying a table or DAG. |
| `/setting-up-astro-project` | 📋 Skill | Initialize and configure Astro/Airflow projects. Use when the user wants to create a new project, set up dependencies, configure connections/variables, or understand project structure. For running the local environment, see managing-astro-local-env. |
| `/delegating-to-otto` | 📋 Skill | Drives Astronomer's Otto agent (`astro otto`) as a delegated sub-agent for Airflow, dbt, and data-engineering work. Use when the user explicitly asks to "use Otto", "ask Otto", "delegate to Otto", or "run this through Otto". Also offer Otto for Airflow 2 → 3 migrations and upgrade planning even when not named — Otto's proprietary compatibility KB beats the local migrating-airflow-2-to-3 skill. Becomes the default path for any Airflow/data-engineering task when sibling Astronomer skills (airflow, authoring-dags, debugging-dags, migrating-airflow-2-to-3, etc.) are NOT loaded in the current session. Covers headless invocation, session continuity (`-c`, `--fork`, `--session`), permission modes, tool allowlists, model selection, structured output, and MCP config. **Do not load this skill if you are Otto** — Otto must not delegate to itself. |
| `/migrating-airflow-2-to-3` | 📋 Skill | Guide for migrating Apache Airflow 2.x projects to Airflow 3.x. Use when the user mentions Airflow 3 migration, upgrade, compatibility issues, breaking changes, or wants to modernize their Airflow codebase. If you detect Airflow 2.x code that needs migration, prompt the user and ask if they want you to help upgrade. Always load this skill as the first step for any migration-related request. |
| `/tracing-upstream-lineage` | 📋 Skill | Trace upstream data lineage. Use when the user asks where data comes from, what feeds a table, upstream dependencies, data sources, or needs to understand data origins. |

<a id="p-fastly-agent-toolkit"></a>

**fastly-agent-toolkit**（7 Skill）

> Fastly 开发工具与平台技能

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/fastly-ngwaf` | 📋 Skill | Performs an internal audit of Fastly Next-Gen WAF (NGWAF) workspaces to audit that critical templated protection rules are configured and enabled. Use when auditing NGWAF workspace security posture, checking for missing or disabled login protection rules (LOGINDISCOVERY, LOGINATTEMPT, LOGINSUCCESS, LOGINFAILURE), auditing credit card validation rules (CC-VAL-ATTEMPT, CC-VAL-FAILURE, CC-VAL-SUCCESS), auditing gift card protection rules (GC-VAL-ATTEMPT, GC-VAL-FAILURE, GC-VAL-SUCCESS), or identifying potential login endpoints not covered by NGWAF rules. |
| `/xvcl` | 📋 Skill | Extends Fastly VCL with loops, functions, constants, macros, conditionals, and includes via XVCL — a VCL transpiler that compiles .xvcl files into standard VCL. Use when writing VCL for Fastly, working with .xvcl files, generating repetitive VCL (multiple backends, routing rules, headers) with loops, defining reusable VCL functions with return values, using compile-time constants instead of magic numbers, or writing any Fastly VCL configuration. XVCL syntax is not in training data so this skill is required. Also applies when writing and testing VCL locally (compile with `uvx xvcl`, test with falco), reducing VCL code duplication, splitting large VCL into modular includes, or doing any VCL development task for Fastly — even without explicitly mentioning XVCL. |
| `/fastly` | 📋 Skill | Configures, manages, and debugs the Fastly CDN platform — covering service and backend setup, caching and VCL, security features like DDoS/WAF/NGWAF/rate limiting/bot management, TLS certificates and cache purging, the Compute platform, and the REST API. Use when working with Fastly services or domains, setting up edge caching or origin shielding, configuring security features, making Fastly API calls, enabling products, or looking up Fastly documentation. Also applies when troubleshooting 503 errors or SSL/TLS certificate mismatches on Fastly, and for configuring logging endpoints, load balancing, ACLs, or edge dictionaries. Read the relevant reference file before writing any Fastly API call or curl command — request field names (e.g. the backend fields override_host, ssl_cert_hostname, ssl_sni_hostname, use_ssl) are easy to misremember, and a wrong name causes a silent 503 instead of an error, so do not rely on training-knowledge field names. |
| `/viceroy` | 📋 Skill | Runs Fastly Compute WASM applications locally with Viceroy, specifically for Rust and Component Model projects. Use when starting a local Fastly Compute dev server with Viceroy, configuring fastly.toml for local backend overrides and store definitions, running Rust unit tests with cargo-nextest against the Compute runtime, debugging Compute apps locally, adapting core WASM modules to the Component Model, or troubleshooting local Compute testing issues (connection refused, missing backends, store config). For non-Rust Compute work or understanding the Compute API, prefer the fastlike skill instead — its source code is easier to understand as a Fastly Compute API reference. |
| `/falco` | 📋 Skill | Lints, tests, simulates, and formats Fastly VCL code using the falco tool. Also serves as the authoritative VCL reference via the falco Go source, which implements Fastly's full VCL dialect. Use when validating VCL syntax, running VCL linting, testing VCL locally, simulating VCL request handling, formatting VCL files, writing VCL unit tests with assertions, debugging VCL logic errors, looking up VCL function signatures or variable scopes, understanding VCL subroutine behavior, or running `falco lint`/`falco simulate`/`falco test`/`falco fmt`. Also applies when working with VCL syntax errors, type mismatches in VCL, choosing which VCL subroutine to use, or setting up a local VCL development and testing environment. |
| `/fastlike` | 📋 Skill | Runs Fastly Compute WASM binaries locally and serves as the authoritative reference for Compute platform internals. The fastlike source code is highly readable and covers the host ABI, caching and purging APIs, KV/config/secret store interfaces, rate limiting with counters and penalty boxes, ACL lookups, the full request lifecycle, backend fetch semantics, and a built-in per-request profiler with hostcall spans, backend waterfalls, native CPU samples, and optional deep metrics (body bytes, cache outcomes, header summaries, wasm heap curve). Use when working with Compute runtime internals or host calls, understanding how edge data stores behave at runtime, profiling local Compute apps, or testing WASM binaries locally. Prefer this skill over Viceroy for any non-Rust Compute work — its source code is easier to understand as a Fastly Compute API reference. |
| `/fastly-cli` | 📋 Skill | Executes Fastly CLI commands for managing CDN services, Compute deploys, and edge infrastructure. Use when running `fastly` CLI commands, creating or managing Fastly services from the terminal, deploying Fastly Compute applications, managing backends/domains/VCL snippets via command line, purging cache, configuring log streaming, setting up TLS certificates, managing KV/config/secret stores, checking service stats, authenticating with Fastly SSO, or working with fastly.toml. Also applies when working with Fastly service IDs in CLI context, or with `fastly service`, `fastly compute`, `fastly auth`, or any Fastly CLI subcommand. Covers service CRUD, version management, autocloning, and troubleshooting common CLI errors. |

<a id="p-fiftyone"></a>

**fiftyone**（16 Skill、2 Command）

> FiftyOne 数据集与视觉模型构建

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/fiftyone-dataset-export` | 📋 Skill | Exports FiftyOne datasets to standard formats (COCO, YOLO, VOC, CVAT, CSV, etc.) and Hugging Face Hub. Use when converting datasets, exporting for training, creating archives, sharing data in specific formats, or publishing datasets to Hugging Face. |
| `/fiftyone-embeddings-visualization` | 📋 Skill | Visualizes datasets in 2D using embeddings with UMAP or t-SNE dimensionality reduction. Use when exploring dataset structure, finding clusters, identifying outliers, or understanding data distribution. |
| `/fiftyone-code-style` | 📋 Skill | Writes Python code following FiftyOne's official conventions. Use when contributing to FiftyOne, developing plugins, or writing code that integrates with FiftyOne's codebase. |
| `/fiftyone-dataset-inference` | 📋 Skill | Run ML model inference on FiftyOne datasets. Use when running models for detection, classification, segmentation, or embeddings. Discovers available models dynamically from the Zoo, plugin operators, or custom sources — never assumes a fixed model list. |
| `/fiftyone-dataset-curation` | 📋 Skill | End-to-end dataset curation for FiftyOne: inspect schema and quality, audit annotations, analyze class distributions, explore embeddings, find duplicates, create curated subsets, and build train/val/test splits. Works with any computer vision dataset type. |
| `/fiftyone-issue-triage` | 📋 Skill | Triages FiftyOne GitHub issues by categorizing as fixed, won't fix, not reproducible, or still valid. Use when reviewing GitHub issues, triaging bugs, or closing stale issues in the voxel51/fiftyone repository. |
| `/fiftyone-model-evaluation` | 📋 Skill | Evaluate model predictions against ground truth using COCO, Open Images, or custom protocols. Use when computing mAP, precision, recall, confusion matrices, or analyzing TP/FP/FN examples for detection, classification, segmentation, or regression tasks. |
| `/fiftyone-generate-data-lens-connector` | 📋 Skill | Generate a Data Lens connector from an external database schema. Use when users want to connect an external data source (PostgreSQL, BigQuery, Databricks, MySQL, etc.) to FiftyOne Data Lens, or when they have a database schema and want to browse/import that data through the FiftyOne App. |
| `/fiftyone-zoo-remote-model` | 📋 Skill | Use when integrating a model into FiftyOne's remote model zoo — detection, classification, segmentation, embedding, keypoint, or vision-language (VLM) models loaded via `register_zoo_model_source` and `load_zoo_model`, then applied with `dataset.apply_model`. Also for debugging zoo registration, `manifest.json` issues, custom `fom.Model` / `TorchModelMixin` subclasses, DataLoader pickle errors, or worker `ModuleNotFoundError` from spawned DataLoader workers. |
| `/fiftyone-develop-plugin` | 📋 Skill | Develops custom FiftyOne plugins (operators and panels) from scratch. Use when creating plugins, extending FiftyOne with custom operators, building interactive panels, or integrating external APIs. |
| `/fiftyone-dataset-import` | 📋 Skill | Imports datasets into FiftyOne with automatic format detection. Supports all media types (images, videos, point clouds), label formats (COCO, YOLO, VOC, KITTI), multimodal grouped datasets, and Hugging Face Hub datasets. Use when importing datasets from local files or Hugging Face, loading autonomous driving data, or creating grouped datasets. |
| `/fiftyone-troubleshoot` | 📋 Skill | Diagnose and fix common FiftyOne issues automatically. Use when a dataset disappeared, the App won't open, changes aren't saving, MongoDB errors occur, video codecs fail, notebook connectivity breaks, operators are missing, or any recurring FiftyOne pain point needs solving. |
| `/fiftyone-create-notebook` | 📋 Skill | Creates Jupyter notebooks for FiftyOne workflows including getting-started guides, tutorials, recipes, and full ML pipelines. Use when creating notebooks, writing tutorials, building demos, or generating FiftyOne walkthroughs covering data loading, exploration, inference, evaluation, and export. |
| `/fiftyone-eval-plugin` | 📋 Skill | Evaluates FiftyOne plugins for quality, security, and agent-readiness. Use when reviewing a plugin before installation, auditing an existing plugin, validating a plugin you just built, or assessing community plugins for safety. Produces a structured report with scores and actionable recommendations. |
| `/fiftyone-voodo-design` | 📋 Skill | Build FiftyOne UIs using VOODO (@voxel51/voodo), the official React component library. Use when building plugin panels, creating interactive UIs, or styling FiftyOne applications. Fetches complete component API reference dynamically. |
| `/fiftyone-find-duplicates` | 📋 Skill | Finds duplicate or near-duplicate images in FiftyOne datasets using brain similarity computation. Use when deduplicating datasets, finding similar images, or removing redundant samples. |
| `/quickstart` | ⌨️ Command | Guided quickstart for FiftyOne - choose between user workflows (import, inference, visualization) or developer workflows (plugin development) |
| `/help` | ⌨️ Command | Get help with FiftyOne skills, understand available workflows, and troubleshoot setup issues |

<a id="p-nightvision"></a>

**nightvision**（4 Skill）

> NightVision DAST API 安全扫描

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/ci-cd-integration` | 📋 Skill | Guide for agents to help users integrate NightVision DAST scanning into CI/CD pipelines. Use when setting up security scans in GitHub Actions, GitLab CI, Azure DevOps, Jenkins, BitBucket, or JFrog pipelines, configuring NightVision tokens, creating targets, running scans, exporting results as SARIF/CSV, or detecting API breaking changes. |
| `/scan-configuration` | 📋 Skill | Guide for agents to help users configure NightVision DAST scans. Use when creating targets, setting up authentication (Playwright, headers, cookies), recording HTTP traffic, managing projects, configuring scope exclusions, or preparing private network scans. |
| `/api-discovery` | 📋 Skill | Guide for agents to help users extract OpenAPI specs from source code using NightVision API Discovery. Use when running swagger extract, identifying framework support, troubleshooting extraction, handling unresolved variables, comparing API specs, or understanding Code Traceback. |
| `/scan-triage` | 📋 Skill | Guide for agents to help users interpret and act on NightVision DAST scan results. Use when reading SARIF/CSV findings, explaining vulnerabilities, locating vulnerable code, validating findings with curl, prioritizing by severity, suggesting remediations, or marking false positives. |

<a id="p-nimble"></a>

**nimble**（14 Skill、1 Command）

> Nimble 网页数据搜索提取与抓取

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/nimble-web-expert` | 📋 Skill | Get web data now — fast, incremental, immediately responsive to what the user needs. The only way Claude can access live websites. USE FOR: - Fetching any URL or reading any webpage - Scraping prices, listings, reviews, jobs, stats, docs from any site - Discovering URLs on a site before bulk extraction - Calling public REST/XHR API endpoints - Web search and research (8 focus modes) - Bulk crawling website sections Must be pre-installed and authenticated. Run `nimble --version` to verify. For building reusable extraction workflows to run at scale over time, use nimble-agent-builder instead. |
| `/nimble-agent-builder` | 📋 Skill | A building experience: create, test, validate, refine, and publish extraction workflows based on existing or new Nimble agents. For users who want to invest in a durable, reusable workflow for a specific domain — not get data immediately. Trigger phrases: "set up extraction for X site", "I need to extract from this site regularly", "build an agent for", "create a reusable scraper", "generate a Nimble agent", "refine my agent", "add a field to my agent", or when the user wants to run extraction at scale. For getting data immediately, use nimble-web-expert instead. |
| `/local-places` | 📋 Skill | Discovers, enriches, and scores local businesses in any neighborhood using Nimble Web Search Agents (WSAs) and web data. Returns a structured, ranked list with confidence scores, reviews, social presence, and an interactive map. Use this skill when the user asks about local businesses, places, or neighborhood discovery. Common triggers: "find all coffee shops in", "map every bar in", "local businesses in", "discover gyms near", "what restaurants are in", "neighborhood guide for", "local places in", "find places near", "list all [business type] in [area]", "best [type] near [location]", "build a neighborhood guide", "local place search". Requires the Nimble CLI (nimble agent run, nimble search, nimble extract) for live web data via WSAs and fallback search. Do NOT use for competitor analysis or monitoring (use competitor-intel), company research or deep dives (use company-deep-dive), general web search or extraction (use nimble-web-expert). |
| `/meeting-prep` | 📋 Skill | Researches meeting attendees and their companies before any meeting using real-time web data. Surfaces roles, recent activity, company context, and talking points — then maps cross-attendee relationships. Use this skill when the user asks to prepare for a meeting, research someone they're meeting, or wants context on attendees. Common triggers: "prepare me for my meeting", "who am I meeting with", "research this person", "meeting prep", "brief me on [person]", "I have a meeting with [person/company]", "get me ready for my call", "what should I know about [person]", "background on [person] before our meeting", "attendee research". Requires the Nimble CLI (nimble search, nimble extract) for live web data. Do NOT use for multi-company competitor monitoring (use competitor-intel) or single-company deep dives without attendees (use company-deep-dive). |
| `/market-finder` | 📋 Skill | Discovers all businesses of a given type in any geography using Nimble WSAs. Two modes: Discovery finds businesses from scratch; Audit compares a user's existing list (Google Sheet, CSV, inline) against fresh discovery, categorizing entries as matched, discovered-only, or reference-only. Vertical presets (Healthcare, SaaS, Restaurants, Legal, Auto/Home) auto-select WSA routing. Triggers: "find all X in Y", "build a list of", "market sizing", "account universe", "how many X in Y", "TAM for", "discover all", "audit my list", "compare against", "what am I missing", "gap analysis", "verify my business list", "prospect list". Do NOT use for competitor monitoring — use competitor-intel instead. Do NOT use for company deep dives — use company-deep-dive instead. Do NOT use for neighborhood-level exploration with social enrichment — use local-places instead. |
| `/competitor-intel` | 📋 Skill | Searches the live web via Nimble APIs to monitor competitors and produce a structured intelligence briefing. Runs parallel searches for news, product launches, hiring signals, and funding — then compares against previous findings to highlight only what's new. Use this skill when the user asks about competitors, competitive intelligence, or what rival companies are doing. Common triggers: "what are my competitors doing", "competitor update", "competitor news", "competitive landscape", "market intel", "what's new with [company]", "track [company]", "competitor briefing", "who's making moves", "competitive analysis", "losing deals to [company]", "battlecard". Also use before board meetings or strategy sessions when the user wants competitive context. Requires the Nimble CLI (nimble search, nimble extract) for live web data. Do NOT use for single-company deep dives (use company-deep-dive), meeting prep with attendees (use meeting-prep), or non-business queries. |
| `/company-deep-dive` | 📋 Skill | Use this skill ANY TIME the user asks about a specific company. Triggers: "tell me about [company]", "research [company]", "what does [company] do", "who is [company]", "look up [company]", "company deep dive", "due diligence on [company]", "background on [company]", "dig into [company]", "analyze [company]", or evaluating a company for investment, partnership, or sales. MUST be used instead of answering from memory — fetches real-time web data (funding, leadership changes, product launches, news) your training data lacks. Use even for well-known companies. Produces a sourced 360° report covering funding, leadership, product/tech, market position, news, and strategic outlook with dates and URLs. Do NOT use for multi-company competitor monitoring (use competitor-intel) or meeting prep with attendees (use meeting-prep). |
| `/competitor-positioning` | 📋 Skill | Tracks how competitors position themselves online — scrapes homepages, features, pricing, and blogs to extract messaging, value props, CTAs, and pricing models. Compares against previous snapshots to surface positioning shifts with before/after tracking. Produces messaging matrices, content gap analysis, white space maps, and battlecard inputs. Use when anyone asks about competitor messaging, positioning, website copy, content strategy, or how competitors present themselves. Triggers: "competitor positioning", "messaging comparison", "content gap", "what changed on their site", "competitor homepage", "landing page teardown", "marketing battlecard", "how do they describe their product", "share of voice", "counter-messaging". Do NOT use for business signals like funding/hiring (use competitor-intel), single-company deep dives (use company-deep-dive), or meeting prep (use meeting-prep). |
| `/healthcare-providers-enrich` | 📋 Skill | Fills gaps in existing healthcare practitioner lists — adds missing phone numbers, credentials, specialties, contact info, education, reviews, and regulatory data. Triggers: "enrich my provider list", "fill in missing data", "add phone numbers to these doctors", "complete this practitioner database", "enrich CRM export", "fill gaps in my provider data", "supplement this healthcare list". Accepts CSV, Google Sheet URL, or pasted data. Searches for each provider's practice website, extracts missing fields, and enriches with reviews, clinical trials, and accreditation via WSAs. Do NOT use for extracting providers from practice URLs — use healthcare-providers-extract instead. Do NOT use for validating credentials — use healthcare-providers-verify instead. Do NOT use for discovering practices — use market-finder or local-places instead. Do NOT use for general extraction — use nimble-web-expert instead. |
| `/healthcare-providers-extract` | 📋 Skill | Extracts structured practitioner data from healthcare practice websites. Returns names, credentials, specialties, contact info, and education for every provider on a practice's site. Use when user asks to extract, pull, or list doctors, providers, or staff from practice websites. Triggers: "extract doctors from", "pull providers from", "who are the providers at", "build a provider database", "list all doctors at", "scrape the team page", "get practitioner data from". Accepts practice URLs (pasted, CSV, Google Sheet) or discovers practices via Google Maps when given specialty + location. Single sites or 100+ URLs. Do NOT use for filling data gaps — use healthcare-providers-enrich instead. Do NOT use for credential validation — use healthcare-providers-verify instead. Do NOT use for discovering practices — use market-finder or local-places instead. Do NOT use for general extraction — use nimble-web-expert instead. |
| `/healthcare-providers-verify` | 📋 Skill | Validates practitioner credentials and license status against the NPI registry. Cross-references specialties, credentials, and practice addresses against official records. Returns Verified / Partially Verified / Unverified / Flagged per practitioner with mismatch details and source URLs. Triggers: "verify these doctors", "check provider credentials", "validate licenses", "verify NPI numbers", "cross-check credentials against NPI", "compliance audit on providers", "are these practitioners still licensed", "validate my provider list". Accepts CSV, Google Sheet URL, or pasted data. Do NOT use for extracting providers from practice URLs — use healthcare-providers-extract instead. Do NOT use for filling data gaps — use healthcare-providers-enrich instead. Do NOT use for discovering practices — use market-finder or local-places instead. Do NOT use for general extraction — use nimble-web-expert instead. |
| `/seo-intel` | 📋 Skill | SEO intelligence toolkit covering the full lifecycle via live web data: keyword research, rank tracking, site audits, content gap analysis, competitor keyword reverse-engineering, AI visibility across five platforms (ChatGPT, Perplexity, Google AI, Gemini, Grok), and GitHub repo SEO. Crawls real sites and SERPs via Nimble CLI — no fabricated metrics. Triggers: "SEO", "keywords", "rank tracker", "site audit", "content gap", "competitor keywords", "AI visibility", "GitHub SEO", "SERP analysis", "keyword research", "technical SEO", "keyword difficulty", "topic clusters", "ranking delta", "on-page SEO", "AI citation audit". Do NOT use for competitor business signals — use `competitor-intel` instead. Do NOT use for competitor messaging — use `competitor-positioning` instead. Do NOT use for general web scraping — use `nimble-web-expert` instead. |
| `/talent-sourcing` | 📋 Skill | Finds qualified candidates for a role by searching LinkedIn, Indeed, GitHub, and other professional platforms using Nimble Web Search Agents. Accepts a job description, role title, or freeform request and returns a ranked candidate list with profiles, skills, and contact signals. Use this skill when the user wants to find, source, or recruit candidates for a role. Common triggers: "find candidates for", "source engineers in", "who can I hire for", "find me a [role]", "recruiting for", "talent search", "find a [role] in [city]", "build a candidate list", "sourcing for [role]", "who's available for", "find potential hires". Also triggers on a pasted job description followed by a sourcing request. Do NOT use for job market research or salary benchmarking — use market-finder instead. Do NOT use for researching a single known person — use company-deep-dive or meeting-prep instead. |
| `/nimble-databricks-data-products` | 📋 Skill | Builds Databricks data products from live web data, end to end: discovers the right Nimble web-data agents, scrapes into Delta tables, and produces an AI/BI dashboard and/or a deployed Databricks App — a table → dashboard → app workflow, for production data products or quick demos. Use whenever a request pairs live or scraped web data WITH a Databricks destination — e.g. "scrape Amazon/Walmart prices into a Delta table and build a dashboard", "load Zillow/Instagram/Maps/search results into Databricks and build a dashboard or app", "showcase Nimble + Databricks to a prospect". Prefer it over nimble-web-expert or competitor-intel when the data lands in Databricks. Do NOT use for one-off web fetches or CSV exports with no Databricks destination — use nimble-web-expert instead. Do NOT use for competitor or company research briefings — use competitor-intel or company-deep-dive instead. Do NOT use for generic Databricks work with no Nimble/web-data angle — use the official databricks-* skills instead. |
| `/nimble:search` | ⌨️ Command | Web search (default for all search and research queries) |

<a id="p-postiz"></a>

**postiz**（2 Skill）

> Postiz 社交媒体自动化发布

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/postiz` | 📋 Skill | Postiz is a tool to schedule social media and chat posts to 28+ channels X, LinkedIn, LinkedIn Page, Reddit, Instagram, Facebook Page, Threads, YouTube, Google My Business, TikTok, Pinterest, Dribbble, Discord, Slack, Kick, Twitch, Mastodon, Bluesky, Lemmy, Farcaster, Telegram, Nostr, VK, Medium, Dev.to, Hashnode, WordPress, ListMonk |
| `/postiz` | 📋 Skill | Postiz is a tool to schedule social media and chat posts to 28+ channels X, LinkedIn, LinkedIn Page, Reddit, Instagram, Facebook Page, Threads, YouTube, Google My Business, TikTok, Pinterest, Dribbble, Discord, Slack, Kick, Twitch, Mastodon, Bluesky, Lemmy, Farcaster, Telegram, Nostr, VK, Medium, Dev.to, Hashnode, WordPress, ListMonk |

<a id="p-prisma"></a>

**prisma**（🔌 MCP）

> Prisma PostgreSQL 数据库管理迁移

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `mcp__Prisma-Local`, `mcp__Prisma-Remote` | 🔌 MCP |
<a id="p-remember"></a>

**remember**（1 Skill）

> Claude Code 持续记忆与对话压缩

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/remember` | 📋 Skill | Save session state for clean continuation next session. |

<a id="p-wordpress.com"></a>

**wordpress.com**（1 Skill、3 Command）

| 名称 | 类型 | 调用说明 |
|------|:--:|------|
| `/site-specification` | 📋 Skill | Extract comprehensive site specifications from simple descriptions. Use when analyzing a user's theme request to determine site type, audience, tone, layout requirements, and typography. |
| `/wordpress.com:quick-build` | ⌨️ Command | Creates a WordPress block theme from a description with an index.html landing page template and deploys it to a local Studio site |
| `/wordpress.com:preview-designs` | ⌨️ Command | Generate or regenerate design preview options for a site |
| `/wordpress.com:design-site` | ⌨️ Command | Design a WordPress site, starting with a clear design direction and style tokens, then intial page layouts, followed by a full custom theme build with content pages deployed to a local Studio site |


---

## 🔗 相关链接


- [Claude Code 官方文档 - Plugins](https://code.claude.com/docs/en/discover-plugins)
- [claude-plugins-official GitHub](https://github.com/anthropics/claude-plugins-official)
- [Claude Code Skills Marketplace Guide](https://skywork.ai/blog/ai-bot/claude-code-skills-marketplace-ultimate-guide/)

---

> 📅 数据截止：2026/06/17 | 来源：`claude-plugins-official` marketplace

> 📅 数据截止：2026/06/17 | 来源：`claude-plugins-official` marketplace
