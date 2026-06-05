# 📖 Codex CLI 基础用法

---

## 🚀 启动

在项目目录中运行：

```bash
codex
```

看到交互界面就说明启动成功了！🎉

---

## 💬 三种使用方式

### 方式一：交互模式（最常用 ✅）

启动后直接跟 Codex 对话，就像跟一个编程高手聊天：

```bash
codex
# 进入交互界面后，直接输入你想让它做的事：
> 帮我检查这个项目有没有 bug 🐛
> 帮我写一个猜数字游戏 🎮
> 解释一下 main.py 的代码在做什么
```

### 方式二：直接给任务

一行命令直接告诉 Codex 做什么：

```bash
codex "帮我创建一个 Python 的 hello world 程序"
```

### 方式三：自动模式（让 Codex 自己跑）

用 `codex exec` 让 Codex 自动完成任务，不需要你盯着：

```bash
# 让 Codex 自己总结项目结构
codex exec "总结这个项目的结构"

# 让 Codex 帮你修 bug
codex exec "运行测试，找出失败的用例并修复"
```

> 💡 自动模式适合让 Codex 在后台帮你做事，比如自动修 bug、生成报告等。

---

## 🔒 安全模式

Codex 会保护你的电脑，你可以选择它有多"自由"：

| 模式 | 说明 | 比喻 |
|------|------|------|
| **Read Only（只读）** 👀 | 只能看，不能改 | 像在图书馆看书 |
| **Auto（自动）** ✅ | 可以改文件和运行命令 | 像让你写作业（推荐！） |
| **Workspace Write** 📝 | 可以改工作区的文件 | 像给你一个专属作业本 |

### 切换安全模式

在交互模式中输入：

```
/permissions
# 然后从弹出菜单选择你想要的模式
```

> 💡 沙箱保护：Codex 在沙箱里运行，就像在一个"安全围栏"里面做事，不会随便改你电脑上其他文件。

---

## ⌨️ 常用命令

在交互模式中输入 `/` 可以打开命令菜单。这里列出最常用的：

### 📌 最常用的命令

| 命令 | 说明 | 怎么记 |
|------|------|--------|
| `/model` | 换一个 AI 模型 | model = 模型 |
| `/permissions` | 切换安全模式 | permissions = 权限 |
| `/diff` | 看看你改了什么 | diff = 差异 |
| `/compact` | 总结对话，省空间 | compact = 压缩 |
| `/clear` | 清屏，重新开始 | clear = 清空 |
| `/quit` | 退出 Codex | quit = 退出 |

### 🔄 会话管理

| 命令 | 说明 |
|------|------|
| `/new` | 开始一个新对话 |
| `/resume` | 回到之前的对话 |
| `/fork` | 分叉对话（试试不同方案） |

> 💡 **小技巧**：正在执行任务时，输入命令后按 `Tab`，可以排队等任务完成后自动执行。

---

## 🎯 常见用法

| 你想做什么 | 命令 |
|------------|------|
| 🆕 写新文件 | `codex "创建一个工具文件 utils.py"` |
| ✏️ 修改代码 | `codex "把 main.py 里的 print 改成 logging"` |
| 🐛 找 bug | `codex "帮我找出代码里的错误"` |
| 🧪 运行测试 | `codex "运行测试并告诉我结果"` |
| 📝 生成文档 | `codex "帮每个函数写上注释说明"` |
| 👀 代码审查 | `codex "审查我刚才的改动，找找问题"` |

---

<details>
<summary>🔧 进阶内容（适合高年级和老师）</summary>

### ⚙️ 配置文件

Codex 使用 TOML 格式的配置文件：

| 文件位置 | 说明 |
|----------|------|
| `~/.codex/config.toml` | 用户全局配置 |
| `.codex/config.toml` | 项目级配置 |

### 常用配置项

```toml
# 默认模型
model = "o4-mini"

# 权限策略（on-request = 需要时询问）
approval_policy = "on-request"

# 沙箱模式
sandbox_mode = "workspace-write"

# 推理强度
model_reasoning_effort = "high"

# 回复风格
personality = "friendly"

# 网页搜索
web_search = "cached"
```

### 更多高级命令

| 命令 | 说明 |
|------|------|
| `/status` | 查看当前模型、权限、token 用量 |
| `/fast` | 切换快速模式 |
| `/plan` | 先规划再执行 |
| `/review` | 审查当前改动 |
| `/skills` | 浏览技能 |
| `/mcp` | 查看 MCP 工具 |
| `/init` | 生成 AGENTS.md 配置文件 |
| `/memories` | 管理记忆功能 |
| `/personality` | 选择回复风格 |
| `/vim` | 切换 Vim 编辑模式 |
| `/theme` | 选择语法高亮主题 |

### 非交互模式高级用法

```bash
# JSON 输出（给其他程序用）
codex exec --json "分析代码风险"

# 管道输入（把命令结果交给 Codex）
npm test 2>&1 | codex exec "总结失败的测试"

# 把结果保存到文件
codex exec "生成 Release Notes" | tee release-notes.md
```

### 🔗 官方文档链接

| 名称 | 链接 |
|------|------|
| CLI 命令参考 | https://developers.openai.com/codex/cli/command-line-options |
| Slash 命令大全 | https://developers.openai.com/codex/cli/slash-commands |
| 配置基础 | https://developers.openai.com/codex/config-basic |
| 非交互模式 | https://developers.openai.com/codex/noninteractive |
| 安全与沙箱 | https://developers.openai.com/codex/security |

</details>

---

## 📌 下一步

👉 **[Codex 桌面版](./desktop.md)** — 了解桌面版的功能

👉 **[OpenCode](../08-opencode/README.md)** — 免费开源的替代方案

👉 **[CC Switch](../04-cc-switch/README.md)** — 用 CC Switch 管理 Codex
