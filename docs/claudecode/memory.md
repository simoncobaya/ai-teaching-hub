# 🧠 Claude Code 的上下文与记忆系统

> 本文结合 [Claude Code 官方文档](https://code.claude.com/docs/en/memory) 和一份真实的 API 请求，解释 Claude Code 如何在每次请求中组装上下文、如何跨会话保留记忆、以及 Prompt Caching 如何降低延迟和费用。

---

## 1. 两种"记忆"

Claude Code 的每次对话都从一个**空的上下文窗口**开始。跨会话保留信息依赖两种机制：

| | CLAUDE.md | Auto Memory |
|---|---|---|
| **谁写** | 你 | Claude |
| **内容** | 指令、规范、约定 | 学到的经验、模式、偏好 |
| **作用域** | 项目 / 用户 / 组织 | 每个 git 仓库独立 |
| **加载方式** | 会话开始时全文加载 | 会话开始时加载 MEMORY.md 的前 200 行或 25KB |
| **用途** | 编码规范、架构约定、工作流 | 构建命令、调试经验、Claude 发现的偏好 |

> 💡 两者都是**上下文（Context）而非强制执行（Enforcement）**。如果需要阻断某个操作（无论 Claude 做什么决定），应使用 Hook 而非 CLAUDE.md。

---

## 2. 上下文组装顺序

每次会话启动时，Claude Code 客户端按下述顺序将信息拼装进 API 请求。以下是官方 [Context Window Explorer](https://code.claude.com/docs/en/context-window) 所列的加载次序：

```
启动过程（自动加载，你不可见）
┌────────────────────────────────────────────────────────────────┐
│ ① System prompt          ~4,200 tokens   核心指令：行为、工具、格式  │
│ ② Auto memory MEMORY.md  ~680 tokens     Claude 的跨会话笔记       │
│ ③ Environment info       ~280 tokens     工作目录、平台、Shell      │
│ ④ MCP tools (deferred)   ~120 tokens     MCP 工具名称列表          │
│ ⑤ Skill descriptions     ~450 tokens     可用 Skill 的一行描述     │
│ ⑥ ~/.claude/CLAUDE.md    ~320 tokens     用户全局偏好             │
│ ⑦ Project CLAUDE.md      ~1,800 tokens   项目约定、构建命令        │
├────────────────────────────────────────────────────────────────┤
│ ⑧ Your prompt            ~45 tokens      你输入的内容             │
├────────────────────────────────────────────────────────────────┤
│ 动态增长（可见或半可见）                                          │
├────────────────────────────────────────────────────────────────┤
│ ⑨ File reads             每次 ~1,000-2,500 tokens                 │
│ ⑩ Path-scoped rules      匹配文件时自动触发                        │
│ ⑪ Tool calls + results   每次往返追加到 messages 数组              │
│ ⑫ Skill full content      仅在你手动触发或 Claude 调用时才加载      │
└────────────────────────────────────────────────────────────────┘
```

> ⚠️ ⑤ Skill descriptions **不会**在 `/compact` 后重新注入。只有你实际调用过的 Skill 会被保留。

---

## 3. 一份真实 API 请求的结构

以下是用户实际发送的一次 Claude Code API 请求（stripped 版本）。本节标注了每部分对应上述组装阶段的哪一环。

### 3.1 HTTP 层

```json
{
  "method": "POST",
  "path": "/v1/messages?beta=true",
  "headers": {
    "User-Agent": "claude-cli/2.1.181 (external, cli)",
    "X-Claude-Code-Session-Id": "38221a45-70e3-42c7-9dac-8aa1a678df7b",
    "anthropic-beta": "claude-code-20250219,context-1m-2025-08-07,..."
  }
}
```

| Header | 说明 |
|--------|------|
| `User-Agent` | 客户端身份：`claude-cli/2.1.181`，标记为外部 API（非 Anthropic 官方） |
| `X-Claude-Code-Session-Id` | 会话 UUID，用于关联多轮往返 |
| `anthropic-beta` | 启用的 beta 功能：1M 上下文窗口、interleaved thinking、prompt caching scope 等 |

### 3.2 `system` 数组 —— 对应 ① ② ③

API 请求的 `system` 字段是一个**数组**，包含 3 个 content block：

```json
"system": [
  {
    "type": "text",
    "text": "x-anthropic-billing-header: cc_version=2.1.181.df1; cc_entrypoint=cli;"
  },
  {
    "type": "text",
    "text": "You are Claude Code, Anthropic's official CLI for Claude.",
    "cache_control": { "type": "ephemeral" }
  },
  {
    "type": "text",
    "text": "\nYou are an interactive agent that helps users with software engineering tasks...\ngitStatus: ...\nRecent commits: ...",
    "cache_control": { "type": "ephemeral" }
  }
]
```

| Block | 对应阶段 | 内容 | 缓存 |
|-------|----------|------|------|
| `system[0]` | — | 计费路由信息（不是给 AI 看的指令） | ❌ |
| `system[1]` | ① 的一部分 | 核心身份锚定：`"You are Claude Code..."` | ✅ ephemeral |
| `system[2]` | ① ③ | Harness 全文：行为规则、工具使用约定、Memory 系统定义、**Environment**、**gitStatus**、**Recent commits** | ✅ ephemeral |

**关键事实：**

- **gitStatus** 和 **Recent commits** 在 `system[2]` 的最末尾，是 Harness 指令的一部分，不是独立的 system message。
- 这意味着 git 状态变化 → `system[2]` 的内容变化 → 缓存断点 2 失效。
- ① System prompt（~4,200 tokens）、② Auto memory（~680 tokens）、③ Environment info 在官方文档中是分开描述的，但在实际 API 请求中，② Auto memory MEMORY.md 并不在 `system` 数组里——它通过 `system-reminder` 注入到 `messages` 中。

### 3.3 `messages` 数组 —— 对应 ② ⑥ ⑦ + 动态内容

```json
"messages": [
  {
    "role": "user",
    "content": [
      { "type": "text", "text": "<system-reminder>\n# claudeMd\n
        Contents of /aidev/ai-teaching-hub/CLAUDE.md:\n
        # AI Teaching Hub - 项目指南\n...\n
        # currentDate\n
        Today's date is 2026/06/26.\n
      </system-reminder>" },
      { "type": "text", "text": "<command-message>review</command-message>\n
        <command-name>/review</command-name>\n
        <command-args>git staged changes, 写commit message</command-args>" },
      { "type": "text", "text": "\nYou are an expert code reviewer. Follow these steps:\n..." }
    ]
  },
  {
    "role": "system",
    "content": "SessionStart hook additional context: <EXTREMELY_IMPORTANT>\n
      You have superpowers.\n\n
      **Below is the full content of your 'superpowers:using-superpowers' skill:**\n
      ...\n
      Available agent types for the Agent tool:\n
      - claude: ...\n
      - claude-code-guide: ...\n
      ...\n
      Available skills:\n
      - deep-research: ...\n
      ...
    "
  },
  {
    "role": "assistant",
    "content": [
      { "type": "thinking", "thinking": "The user wants me to review...", "signature": "ffc0906f-..." },
      { "type": "text", "text": "I'll review your staged changes and help write a commit message." },
      { "type": "tool_use", "id": "call_00_ESp2f...", "name": "Bash", "input": { "command": "git diff --cached --stat" } },
      { "type": "tool_use", "id": "call_01_yTpq...", "name": "Bash", "input": { "command": "git diff --cached" } }
    ]
  },
  {
    "role": "user",
    "content": [
      { "tool_use_id": "call_00_ESp2f...", "type": "tool_result", "content": " docs/ai-coding-tools/... | 35 +\n ..." },
      { "tool_use_id": "call_01_yTpq...", "type": "tool_result", "content": "<persisted-output>\nOutput too large (755.3KB). Full output saved to: ..." }
    ]
  },
  // ... 后续轮次的 assistant tool_use + user tool_result ...
  {
    "role": "system",
    "content": "The task tools haven't been used recently. If you're working on tasks that would benefit from tracking progress, consider using TaskCreate..."
  }
]
```

**每条 message 的来源：**

| Message | 角色 | 对应阶段 | 来源 |
|----------|------|----------|------|
| `<system-reminder> CLAUDE.md + currentDate` | user | ⑥ ⑦ | 客户端读取 CLAUDE.md 文件，包裹在 system-reminder 标签中，放在第一条 user message 的开头 |
| `<command-message> /review` | user | ⑧ | 用户输入的 slash command |
| `You are an expert code reviewer...` | user | ⑧ | `/review` Skill 的指令文本，由客户端直接拼接在用户输入后面 |
| `SessionStart hook additional context` | **system** | — | **SessionStart Hook 注入**：superpowers 插件在会话开始时注入其核心技能内容 + Agent 类型列表 + Skills 列表 |
| `assistant` (thinking + text + tool_use) | assistant | — | AI 的回复（思考过程 + 文字 + 工具调用） |
| `user` (tool_result) | user | — | 工具执行后的返回值 |
| `The task tools haven't been used...` | system | — | 客户端注入的**温和提醒**，建议使用 Task 工具 |

> 💡 `"role": "system"` 的消息在对话中间也可以出现——这被称为 **mid-conversation system messages**（仅 Opus 4.8+ 的 Anthropic API 支持）。它的关键优势是：放在 messages 数组的中间（缓存前缀之后），因此**添加/修改它不会使前面的缓存失效**。Claude Code 正是利用这一点来注入 SessionStart Hook 内容和温和提醒——如果这些内容放在顶层 `system` 字段里，任何改动都会导致整个缓存前缀失效。

### 3.4 `tools` 数组 —— 对应 ④

```json
"tools": [
  { "name": "Agent", "description": "Launch a new agent...", "input_schema": { ... } },
  { "name": "Bash", "description": "Executes a bash command...", "input_schema": { ... } },
  { "name": "Read", "description": "Reads a file from the local filesystem...", "input_schema": { ... } },
  // ... 共 28 个工具
  { "name": "mcp__ide__executeCode", ... },
  { "name": "mcp__ide__getDiagnostics", ... }
]
```

`tools` 数组不在 `messages` 里，是 API 请求的独立字段。但根据 Anthropic 官方文档：

> *"Prompt caching references the entire prompt — **tools, system, and messages (in that order)** up to and including the block designated with cache_control."* [3]

这意味着 `system[2]` 上的缓存断点实际上覆盖了 **tools 数组 + 全部 system 块**——它们作为同一个前缀被哈希和缓存。

---

## 4. Hook 如何注入上下文

### 4.1 SessionStart Hook

SessionStart 在每次会话启动时触发。从真实请求中可以看到它注入了一条独立的 `"role": "system"` 消息：

```
SessionStart hook additional context:
  ├── Superpowers 插件的 using-superpowers 技能全文（约 60 tokens 的摘要）
  ├── Available agent types 列表（6 种 Agent 的定义）
  └── Available skills 列表（42+ 个 Skill 的名称和一句话描述）
```

注入方式有两种：
- **`additionalContext`**（JSON 输出）：包裹在 `<system-reminder>` 中，插入到对话流中对应位置
- **stdout**（纯文本输出）：SessionStart 的 stdout 直接作为附加上下文

### 4.2 其他 Hook 注入点

| 事件 | 注入时机 | 上下文插入位置 |
|------|----------|---------------|
| `SessionStart` | 会话启动 | 对话最开头，第一条用户消息之前 |
| `UserPromptSubmit` | 用户提交 prompt 后 | 和用户 prompt 一起 |
| `PreToolUse` | 工具执行前 | 可阻断工具调用或修改参数 |
| `PostToolUse` | 工具执行后 | 紧邻工具返回值 |
| `Stop` | AI 完成回复后 | 轮次末尾 |

---

## 5. Prompt Caching：缓存如何工作

### 5.1 基本机制

Anthropic 的 Prompt Caching 是一种**前缀字符串匹配**的 KV-cache 复用机制。工作方式：

1. 在 API 请求中，你在某个 content block 上标记 `cache_control: { "type": "ephemeral" }`
2. API 计算到该断点为止的所有 token 序列的 KV-cache，并存储起来
3. 下一次请求如果前缀**逐字节完全一致**，API 直接从缓存读取，跳过重复计算

```
请求 A（写入缓存）:
┌────────系统──────────┬──────────────── messages ────────────────────┐
│ system[0]+[1]+[2]   │ msg[0] ... msg[N-1] │ 最后一条 tool_result   │
│ ← 断点2 覆盖        │ ← 正常计算          │ ← 断点3 覆盖（滑动窗口）│
└────────────────────┴────────────────────┴─────────────────────────┘

请求 B（新的一轮）:
┌────────系统──────────┬──────────────── messages ──────────────────────┐
│ system[0]+[1]+[2]   │ 和请求A相同的部分 │ 新增的一对 tool_use+result │
│ ✅ 前缀未变 → 命中    │ ✅ 也命中（断点3）  │ ❌ 新的 → 触发新的缓存写    │
└────────────────────┴──────────────────┴─────────────────────────────┘
```

### 5.2 定价

| 操作 | 5 分钟 TTL | 1 小时 TTL |
|------|-----------|-----------|
| **写入缓存** | 1.25× 基础输入价格 | 2.0× 基础输入价格 |
| **读取缓存** | **0.1×** 基础输入价格 | **0.1×** 基础输入价格 |

> 缓存读取相当于**打一折**。这就是为什么 `cache_read_input_tokens` 占比越高越省钱。

### 5.3 真实请求中的缓存布局

从 `request.json` 可以看到 **3 个缓存断点**：

```
断点 1：system[1]  "You are Claude Code..." + cache_control
断点 2：system[2]  Harness 全文 + cache_control
断点 3：messages 中最后一条 tool_result + cache_control  ← 滑动窗口！
```

这三者共同构成缓存前缀。对应的缓存语义：

```
前缀序列（缓存视角）:
┌─system[0]──┬─system[1]──┬────────system[2]────────┬───── messages（部分）─────┐
│ 计费信息    │ 核心身份    │  Harness 全文             │  对话历史（含最后一轮结果）│
│ 无缓存标记  │ 断点1 ✅    │  断点2 ✅                 │  断点3 ✅（滑动窗口）     │
│            │ ~50 tokens │  ~20,000 tokens           │                          │
└────────────┴────────────┴─────────────────────────┴──────────────────────────┘

断点3 的特殊之处：它不在 system 数组中，而在 messages 数组的最后一条 tool_result 上。
这是 Claude Code 的 kVY() 函数实现的滑动窗口策略——每次都把最远的缓存边界推到
最后一轮工具返回的位置。随着对话增长，断点 3 的绝对位置不断向前滑动。
```

**实际效果**（来自该请求的 `usage` 字段）：

```json
"usage": {
  "input_tokens": 2437,           // 新 tokens，全价计费
  "cache_read_input_tokens": 29824, // 从缓存命中的 tokens，一折计费
  "output_tokens": 1300
}
```

约 30K tokens 走缓存（占输入 93%），只有 2.4K 按全价。这三个断点协同工作，省了大量费用。

### 5.4 什么会破坏缓存

> 📖 本节前半部分来自 [Anthropic 官方文档](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 的缓存失效规则表，后半部分补充 Claude Code 特有的触发场景。

**核心规则：缓存遵循 tools → system → messages 的层级。某一层发生变化，该层及之后的所有层都失效。**

```
tools 层变化 → tools ✘, system ✘, messages ✘  (全部失效)
system 层变化 → tools ✓, system ✘, messages ✘
messages 层变化 → tools ✓, system ✓, messages ✘
```

#### API 层面的失效规则

| 什么变了 | tools 缓存 | system 缓存 | messages 缓存 | 影响 |
|----------|:----------:|:-----------:|:-------------:|------|
| 修改工具定义（名称、描述、参数） | ✘ | ✘ | ✘ | 整个缓存失效 |
| 开启/关闭 Web Search | ✓ | ✘ | ✘ | 修改了 system prompt |
| 开启/关闭 Citations | ✓ | ✘ | ✘ | 修改了 system prompt |
| 切换 Speed 模式（fast ↔ 标准） | ✓ | ✘ | ✘ | system 和 messages 缓存失效 |
| 修改 `tool_choice` 参数 | ✓ | ✓ | ✘ | 仅影响 message blocks |
| 增删图片 | ✓ | ✓ | ✘ | 影响 message blocks |
| 修改 Thinking 参数（开关/budget） | ✓ | ✓ | ✘ | 影响 message blocks |

> 💡 **新增一轮对话不会破坏缓存**——这正是断点 3（滑动窗口）的作用：`cache_control` 始终放在最后一条 tool_result 上，每次新轮次自动向前滑动，保证之前的内容仍然命中。

#### Claude Code 特有的触发场景

将上述 API 规则映射到 Claude Code 的实际使用：

| 用户操作 | 对应的 API 层变化 | 失效范围 |
|----------|-------------------|----------|
| MCP 服务器重连（工具定义可能重排） | tools 层 | **全部缓存失效** |
| 提交代码 / 切换分支 | system 层（gitStatus 变化） | system + messages |
| 编辑 CLAUDE.md | messages 层（system-reminder 变化） | messages |
| 安装/卸载插件 | messages 层（SessionStart hook 注入的 Agent/Skill 列表变化） | messages |
| `/fast on` / `/fast off` | system 层 | system + messages |
| `/effort` 修改 | Thinking 参数变化 → messages 层 | messages |
| 超过 5 分钟 TTL | — | **全部缓存失效** |

> 💡 **为什么 Claude Code 用 mid-conversation system messages 来放 Hook 输出？** 如果这些内容放在顶层 `system` 字段，Hook 输出的任何变化都会从最开头改变前缀哈希，整个缓存失效。放在 messages 中间（缓存断点之后），前面的 system prompt 缓存不受影响。这是 Claude Code 选择在 messages 数组中使用 `"role": "system"` 而非修改顶层 `system` 数组的原因。详见 [Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages)。

### 5.5 参数约束

| 参数 | 限制 |
|------|------|
| 每请求最大断点数 | 4 |
| 每个断点的回溯窗口 | 20 个 content block |
| 最小可缓存 token 数 | 1024（Opus 4.8 / Sonnet 4.6）/ 512（Fable 5） |
| 缓存前缀计算顺序 | tools → system → messages | [3] |
| `ephemeral` TTL | 5 分钟（默认），可选 1 小时 |

---

## 6. CLAUDE.md 文件的加载逻辑

### 6.1 文件位置与优先级

CLAUDE.md 可以放在多个位置，按**从宽到窄**的顺序加载（后面的在上下文中位置更靠后，因此 AI 更优先关注）：

| 作用域 | 位置 | 用途 |
|--------|------|------|
| **组织策略** | `/etc/claude-code/CLAUDE.md` (Linux) | IT/DevOps 统一管理的公司级规范 |
| **用户全局** | `~/.claude/CLAUDE.md` | 个人偏好，所有项目生效 |
| **项目级** | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 团队共享的项目约定（版本控制） |
| **本地** | `./CLAUDE.local.md` | 个人项目偏好（加入 .gitignore） |

### 6.2 子目录与规则的按需加载

- **父目录**的 CLAUDE.md：启动时按目录树向上搜索并全部加载
- **子目录**的 CLAUDE.md：**按需加载**——当 Claude 读取该子目录的文件时才触发
- **`.claude/rules/`**：可按文件路径 scope（`paths:` frontmatter），匹配的文件被读取时自动加载对应规则

### 6.3 从真实请求验证

在 `messages[0]` 的 system-reminder 中：

```
Contents of /aidev/ai-teaching-hub/CLAUDE.md (project instructions, checked into the codebase):
```

这证实了：客户端读取 CLAUDE.md 文件 → 把**全文内容**包裹在 `<system-reminder>` 标签中 → 作为第一条 user message 的开头部分注入。

---

## 7. Auto Memory：Claude 自己写的笔记

### 7.1 存储结构

```
~/.claude/projects/<project>/memory/
├── MEMORY.md           ← 索引文件，会话启动时加载（前 200 行或 25KB）
├── debugging.md        ← Claude 写的调试经验
├── api-conventions.md  ← Claude 记录的 API 约定
└── ...                 ← 其他按需创建的主题文件
```

### 7.2 加载机制

- **MEMORY.md**：会话启动时自动加载（前 200 行或 25KB，取较小者）。这是所有加载内容中**唯一有长度限制**的。
- **Topic 文件**（如 `debugging.md`）：**不自动加载**。Claude 需要时通过 Read 工具读取。
- Claude 在会话中读写 memory 文件，更新 MEMORY.md 索引。

### 7.3 与 CLAUDE.md 的区别

```
CLAUDE.md:     你写的 → 告诉 Claude "你要这样做"
Auto memory:   Claude 写的 → Claude 告诉自己 "上次我学到了这个"
```

Auto memory 通常在以下场景触发：
- 你纠正了 Claude 的错误 → Claude 记录正确的做法
- 你重复了同样的要求 → Claude 记录这个偏好
- Claude 发现了一个不显而易见的构建命令 → Claude 记下来

---

## 8. Context Management：上下文管理

### 8.1 Compaction（压缩）

当对话历史接近模型的 context window 上限时，客户端自动触发压缩：

```
压缩前:
  [轮次 1] [轮次 2] [轮次 3] ... [轮次 N-1] [轮次 N]

压缩后:
  [轮次 1~N-1 的 AI 生成摘要] [轮次 N 的完整内容] [继续追加的新对话]
```

### 8.2 什么在 compact 后保留？什么会丢失？

| 内容 | compact 后 | 说明 |
|------|-----------|------|
| Project CLAUDE.md | ✅ 保留 | 客户端重新从磁盘读取并注入 |
| 子目录 CLAUDE.md | ⚠️ 延迟恢复 | 等到下次读取该子目录文件时重新加载 |
| Auto memory MEMORY.md | ✅ 保留 | 同样重新从磁盘读取 |
| Skill descriptions 列表 | ❌ 不保留 | 只有你实际调用过的 Skill 会保留 |
| 对话中口头告诉 Claude 的指令 | ❌ 丢失 | 如果重要，写入 CLAUDE.md |
| 已读取的文件内容 | ❌ 丢失 | 需要时 Claude 重新读取 |

> 💡 使用 `/context` 命令可以查看当前上下文用量（彩色网格图）。

---

## 9. 一份请求的完整数据流

```
用户打开终端，输入 claude
│
├─ 客户端读取 settings.json（含 Hook 配置、权限等）
├─ 客户端执行 SessionStart Hooks → 收集注入内容
├─ 客户端扫描 CLAUDE.md（向上搜索目录树 + 向下发现子目录）
├─ 客户端读取 MEMORY.md 索引
└─ 客户端组装 System Prompt（计费信息 + 身份 + Harness + Environment + gitStatus）

用户输入 "/review git staged changes, 写commit message"
│
├─ 客户端识别 /review → 加载 review skill 的指令文本
├─ 客户端包裹 system-reminder（CLAUDE.md 全文 + currentDate）
├─ 客户端拼接完整 messages 数组：
│   ├─ [0] user: system-reminder + 命令 + skill 指令
│   ├─ [1] system: SessionStart hook 注入
│   ├─ [2] assistant: 上轮 AI 回复
│   ├─ [3] user: 上轮工具返回值
│   └─ ... 继续追加
└─ 发送 HTTPS POST /v1/messages?beta=true

API 侧处理:
├─ 检查 tools 前缀是否命中缓存
├─ 检查 system 前缀是否命中缓存
├─ 跳过缓存命中的部分（直接读 KV cache）
└─ 计算未命中部分 → 流式返回

客户端收到响应:
├─ 解析 thinking → 可能展示思考过程
├─ 解析 text → 渲染为 Markdown 显示
├─ 解析 tool_use → 执行工具调用
└─ 把工具返回值作为新 user message 发回去 → 循环
```

---

## 10. `/context` 命令的实际输出

在你的环境中运行 `/context` 得到：

| 类别 | Tokens | 占比 | 说明 |
|------|--------|------|------|
| System prompt | 1.7k | 0.2% | Harness 核心指令 |
| System tools | 15.3k | 1.5% | 28 个工具的 JSON Schema 定义 |
| Memory files | 771 | 0.1% | CLAUDE.md（本请求中无 auto memory） |
| Skills | 2.4k | 0.2% | 所有已安装 Skill 的一行描述 |
| Messages | 62.1k | 6.2% | 对话历史：system-reminder + 多轮 assistant/user + 工具结果 |
| **Total** | **82.1k** | **8%** | 1M 窗口还剩 91.8% 可用 |

这和上文的分析完全吻合：
- System prompt 1.7k → `system[1]` + `system[2]` 的部分内容
- System tools 15.3k → 28 个工具定义
- Memory files 771 → CLAUDE.md 内容（通过 system-reminder 在 messages 中，但在 `/context` 中被归类到 Memory）
- Skills 2.4k → Skill descriptions 列表（部分来自 SessionStart hook 的 system message）
- Messages 62.1k → 对话历史（system-reminder + hook 注入 + assistant 回复 + tool 结果 + 温和提醒）

---

## 11. 总结：三种"视角"

理解 Claude Code 的记忆/上下文系统，有三个不同的视角：

| 视角 | 关心的问题 | 管用工具 |
|------|-----------|----------|
| **逻辑视角** | "AI 看到了哪些信息？从哪来的？" | 本文第 2、3、6、7 节 |
| **缓存视角** | "哪些 token 不需要重复计算？" | 本文第 5 节 |
| **用户视角** | "我如何控制 AI 知道什么？" | CLAUDE.md、`/memory`、`/context`、`/compact` |

这三个视角**互不隶属**：逻辑分层不等同于缓存边界，缓存命中不关心语义分组。但三者协同工作，共同构成了 Claude Code 的"记忆"。

---

> 📚 **参考来源：**
> - [Claude Code — How Claude remembers your project](https://code.claude.com/docs/en/memory) — CLAUDE.md 和 Auto Memory 的官方文档
> - [Claude Code — Explore the context window](https://code.claude.com/docs/en/context-window) — 上下文组装顺序的交互式模拟
> - [Claude Code — Hooks Guide](https://code.claude.com/docs/en/hooks) — Hook 生命周期、注入方式、配置格式
> - [3] [Anthropic — Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) — 官方文档原文：*"Prompt caching references the entire prompt — tools, system, and messages (in that order) up to and including the block designated with cache_control."*（已通过代理直接验证）
> - [1] [DeepWiki — Claude Code Cache Invalidation](https://deepwiki.com/cablate/claude-code-research/5.2-cache-invalidation:-root-causes-and-verification) — 对 Claude Code 内部函数 `vuK()`、`Z57()`、`yVY()`、`kVY()` 的逆向分析，从代码层面验证了相同行为
> - [2] [GitHub: opencode PR #14743](https://github.com/anomalyco/opencode/pull/14743) — 基于相同 byte order 修复 Anthropic 缓存命中率的开源 PR
> - 本文所有 API 请求片段来自用户提供的真实请求数据（Claude Code v2.1.181 + DeepSeek v4 Pro）
