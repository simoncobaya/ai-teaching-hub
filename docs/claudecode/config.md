# ⚙️ /config 命令与设置详解

> 基于 Claude Code v2.1.181 `/config` 实际输出 · 31 个设置全部通过实际切换后 grep 验证生效范围
>
> 输入 `/config` 打开交互式设置面板，`↑/↓` 或 `j/k` 上下移动，`←/→` 切换选项。

### 生效范围

| 标注 | 含义 |
|:--:|------|
| 🌐 用户 | 写入 `~/.claude/settings.json`，所有项目生效 |
| 📁 本地 | 写入 `.claude/settings.local.json`，仅当前项目生效 |
| 💻 会话 | 纯 UI/内存开关，不写入任何文件，仅当前会话有效 |

---

## 📋 全部 31 个设置一览

### 会话行为

| 设置 | 默认值 | 范围 | JSON 键 | 说明 |
|------|------|:--:|------|------|
| **Auto-compact** | true | 🌐 | `autoCompactEnabled` | 对话上下文快用完时自动触发 `/compact` 压缩。关闭后上下文满了会直接报错，需手动 `/compact` |
| **Switch models when flagged** | true | 🌐 | `switchModelsOnFlag` | Claude 回复被内容审核标记时，自动切换到其他模型重试 |
| **Show tips** | true | 📁 | `spinnerTipsEnabled` | 加载等待时显示操作提示文字（如"正在读取文件..."） |
| **Reduce motion** | false | 📁 | `prefersReducedMotion` | 减少或禁用 UI 动画——旋转、闪烁、渐变效果等，无障碍支持 |
| **Thinking mode** | true | 🌐 | `alwaysThinkingEnabled` | 默认启用 extended thinking（扩展思考），Claude 在复杂任务上花更多时间推理。可通过 `MAX_THINKING_TOKENS=0` 强制关闭（Fable 5 除外） |
| **Session recap** | true | 🌐 | `awaySummaryEnabled` | 离开终端几分钟后回来时，自动显示一句话会话摘要 |
| **Rewind code (checkpoints)** | true | 🌐 | `fileCheckpointingEnabled` | 每次编辑文件前自动创建快照，使 `/rewind` 可回退代码。关闭后 `/rewind` 无法恢复文件 |
| **Dynamic workflows** | true | 🌐 | `enableWorkflows` | 启用动态工作流——Claude 可将大型任务拆解后并行分派给多个子 Agent |
| **Ultracode keyword trigger** | true | 🌐 | `workflowKeywordTriggerEnabled` | 输入中包含 `ultracode` 关键词时自动触发多 Agent 工作流编排 |
| **Verbose output** | false | 🌐 | `verbose` | 显示详细逐轮执行过程（含每次工具调用的完整输入输出），调试时用 |
| **Terminal progress bar** | true | 🌐 | `terminalProgressBarEnabled` | 显示终端进度条，可视化当前操作进度 |
| **Show turn duration** | true | 🌐 | `showTurnDuration` | 每轮对话结束后显示耗时 |

---

### 权限与模式

| 设置 | 默认值 | 范围 | JSON 键 | 说明 |
|------|------|:--:|------|------|
| **Default permission mode** | Default | 🌐 | `defaultMode` | 新会话默认权限模式。可选：Default（需确认）/ Plan Mode（只读规划）/ Accept edits（自动接受编辑）/ Auto mode（自行判断）/ Don't Ask（直接执行）。`Shift+Tab` 可临时切换 |
| **Worktree base ref** | fresh | 🌐 | `worktree.baseRef` | 创建 git worktree 的基准分支：`fresh` = 从 `origin/<默认分支>`，`head` = 从当前 HEAD |
| **Use auto mode during plan** | true | 🌐 | `useAutoModeDuringPlan` | Plan 模式下也启用 auto mode 的自动批准逻辑 |

---

### 界面与显示

| 设置 | 默认值 | 范围 | JSON 键 | 说明 |
|------|------|:--:|------|------|
| **Theme** | Dark mode | 🌐 | `theme` | 终端主题配色。含 light/dark/auto、色盲友好、ANSI（跟随终端配色）、自定义主题。也可用 `/theme` 切换 |
| **Respect .gitignore** | false | 💻 | — | `@` 文件选择器是否遵循 `.gitignore` 规则，开启后被忽略的文件不出现在建议列表中 |
| **Skip the /copy picker** | false | 💻 | — | 使用 `/copy` 时跳过内容选择器，直接复制全部内容 |
| **Open agents view by default** | false | 💻 | — | 启动时默认打开 Agent 管理视图 |
| **← opens agents** | true | 💻 | — | 按 `←`（左箭头键）打开 Agent 管理视图 |
| **Show last response in editor** | false | 💻 | — | 在外部编辑器（如 VS Code）中显示最后一次回复 |
| **Show PR status footer** | false | 💻 | — | 底部状态栏显示当前 PR 的状态信息 |
| **Auto-install IDE extension** | true | 💻 | — | 自动安装 Claude Code 的 IDE 扩展（如 VS Code 插件） |
| **Claude in Chrome by default** | false | 💻 | — | 新会话默认启用 Chrome 浏览器集成（让 Claude 可控制浏览器） |

---

### 模型与输出

| 设置 | 默认值 | 范围 | JSON 键 | 说明 |
|------|------|:--:|------|------|
| **Model** | 当前模型 | 🌐 | `model` | 默认 AI 模型。可选 sonnet（均衡）/ opus（最强）/ haiku（最快）/ fable（最新）。也可用 `/model` 切换 |
| **Output style** | default | 📁 | `outputStyle` | 输出风格——**直接修改 system prompt**，影响最大的设置。详见下方章节。可选 Default / Proactive / Explanatory / Learning / 自定义。切换后需 `/clear` 或重启 |
| **Language** | Default (English) | 🌐 | `language` | Claude 默认回复语言。设 `"chinese"` 则默认中文回复，也影响语音输入语言和会话标题 |
| **Diff tool** | auto | 💻 | — | 查看代码差异时使用的对比工具，auto = 自动选择 |

---

### 通知与更新

| 设置 | 默认值 | 范围 | JSON 键 | 说明 |
|------|------|:--:|------|------|
| **Local notifications** | Auto | 🌐 | `preferredNotifChannel` | 任务完成和权限提示的通知方式。可选 Auto / terminal_bell / iterm2 / kitty / ghostty / notifications_disabled |
| **Auto-update channel** | 取决于环境 | 🌐 | `autoUpdatesChannel` | 自动更新通道：`"latest"` = 最新版，`"stable"` = 稳定版（滞后约一周）。被 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 禁用则显示 `disabled` |
| **Editor mode** | normal | 🌐 | `editorMode` | 输入提示符键位模式：`"normal"` = 常规编辑，`"vim"` = Vim 风格 |

---

### 汇总

| 生效范围 | 数量 | 包含 |
|:--:|:--:|------|
| 🌐 用户 | **19** | 大部分行为、模式、通知类设置 |
| 📁 本地 | **3** | Show tips, Reduce motion, Output style |
| 💻 会话 | **9** | 界面显示偏好，重启后恢复默认 |

---

## 🎨 Output Style（输出风格）

> 写入 `.claude/settings.local.json`（📁 本地），直接修改 system prompt。切换后需 `/clear` 或重启生效。

| 风格 | 作用 |
|------|------|
| **Default** | 标准软件工程助手——默认 system prompt |
| **Proactive** | 自主执行——合理假设、偏好行动而非反复确认 |
| **Explanatory** | 教学解释——在代码任务间插入"Insights"说明设计思路 |
| **Learning** | 互动学习——留 `TODO(human)` 让你亲手写关键代码段 |

自定义风格：创建 `.claude/output-styles/<名称>.md`，设 `keep-coding-instructions: true` 保留默认工程指令，`false` 则为纯自定义角色。

---

## 🚀 学生常用速查

| 想做什么 | 怎么设 |
|------|------|
| 互动教学模式 | `/config` → Output style → **Explanatory** |
| 切换模型 | `/model haiku` |
| 换主题 | `/theme` |
| Claude 用中文回复 | `/config` → **Language** |
| 手动控制上下文压缩 | `/config` → 关闭 **Auto-compact** |
| 允许 git 命令自动执行 | `/permissions` → 添加 `Bash(git *):*` |
