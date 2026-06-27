# ⚙️ /config 命令与设置详解

> 基于 Claude Code v2.1.181 `/config` 实际输出 · 31 个设置全部通过实际切换后 grep 验证生效范围 · 默认值来源：官网明确记录 或 来自用户环境（标注 *）

输入 `/config` 打开交互式设置面板，`↑/↓` 或 `j/k` 上下移动，`←/→` 切换选项。

### 生效范围

| 标注 | 含义 |
|:--:|------|
| 🌐 用户 | 写入 `~/.claude/settings.json`，所有项目生效 |
| 📁 本地 | 写入 `.claude/settings.local.json`，仅当前项目生效 |
| 💻 会话 | 纯 UI/内存开关，不写入任何文件，仅当前会话有效 |

---

## 会话行为

### Auto-compact
| 项目 | 内容 |
|------|------|
| 默认值 | true ✅ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `autoCompactEnabled` |

当对话上下文快用完时，Claude 自动触发 `/compact` 压缩。关闭后上下文满了会直接报错，需要手动 `/compact`。

---

### Switch models when a message is flagged
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `switchModelsOnFlag` |

当 Claude 的回复被内容审核标记时，自动切换到其他模型重试。关闭则收到标记后不自动切换。

---

### Show tips
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 📁 本地 |
| JSON 键 | `spinnerTipsEnabled` |

加载等待时显示操作提示文字（如"正在读取文件..."）。关闭后只显示加载动画。

---

### Reduce motion
| 项目 | 内容 |
|------|------|
| 默认值 | false ⚠️ |
| 生效范围 | 📁 本地 |
| JSON 键 | `prefersReducedMotion` |

减少或禁用 UI 动画——旋转、闪烁、渐变效果等。为对动画敏感的用户提供无障碍支持。

---

### Thinking mode
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `alwaysThinkingEnabled` |

默认启用 extended thinking（扩展思考）。开启后 Claude 在复杂任务上会花更多时间推理。可通过环境变量 `MAX_THINKING_TOKENS=0` 强制关闭（Fable 5 除外）。

---

### Session recap
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `awaySummaryEnabled` |

离开终端几分钟后回来时，自动显示一句话会话摘要，帮你快速回忆上下文。

---

### Rewind code (checkpoints)
| 项目 | 内容 |
|------|------|
| 默认值 | true ✅ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `fileCheckpointingEnabled` |

每次编辑文件前自动创建快照，使得 `/rewind` 可以回退代码修改。关闭后 `/rewind` 无法恢复文件，只能回退对话。

---

### Dynamic workflows
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `enableWorkflows` |

启用动态工作流——Claude 可以将大型任务拆解后并行分派给多个子 Agent 执行。关闭后工作流功能不可用。

---

### Ultracode keyword trigger
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `workflowKeywordTriggerEnabled` |

当用户输入中包含 `ultracode` 关键词时，自动触发多 Agent 工作流编排。

---

### Verbose output
| 项目 | 内容 |
|------|------|
| 默认值 | false ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `verbose` |

显示详细的逐轮执行过程，包括每次工具调用的完整输入输出。调试时有用，日常使用建议关闭。

---

### Terminal progress bar
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `terminalProgressBarEnabled` |

显示终端进度条，可视化当前操作的进度。

---

### Show turn duration
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `showTurnDuration` |

每轮对话结束后显示耗时。

---

## 权限与模式

### Default permission mode
| 项目 | 内容 |
|------|------|
| 默认值 | Default ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `defaultMode` |

新会话默认的权限模式。可选值：
- **Default**：工具调用需确认
- **Plan Mode**：只读规划模式，不执行操作
- **Accept edits**：自动接受编辑，其他仍需确认
- **Auto mode**：自动模式，Claude 自行判断
- **Don't Ask**：不询问，直接执行

可用 `Shift+Tab` 在当前会话中临时切换。

---

### Worktree base ref
| 项目 | 内容 |
|------|------|
| 默认值 | fresh ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `worktree.baseRef` |

创建 git worktree 时的基准分支。`fresh` = 从 `origin/<默认分支>` 创建，`head` = 从当前 HEAD 创建。

---

### Use auto mode during plan
| 项目 | 内容 |
|------|------|
| 默认值 | true ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `useAutoModeDuringPlan` |

Plan 模式下也启用 auto mode 的自动批准逻辑。

---

## 界面与显示

### Theme
| 项目 | 内容 |
|------|------|
| 默认值 | Dark mode ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `theme` |

终端主题配色。包含 light/dark/auto 主题、色盲友好主题、ANSI 主题（跟随终端配色）、自定义主题。也可用 `/theme` 命令切换。

---

### Respect .gitignore in file picker
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

`@` 文件选择器是否遵循 `.gitignore` 规则。开启时，被 `.gitignore` 忽略的文件不出现在建议列表中。

---

### Skip the /copy picker
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

使用 `/copy` 时跳过内容选择器，直接复制全部内容。

---

### Open agents view by default
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

启动时默认打开 Agent 管理视图。

---

### ← opens agents
| 项目 | 内容 |
|------|------|
| 默认值 | true |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

按 `←`（左箭头键）打开 Agent 管理视图。

---

### Show last response in external editor
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

在外部编辑器（如 VS Code）中显示最后一次回复。

---

### Show PR status footer
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

底部状态栏显示当前 PR 的状态信息。

---

### Auto-install IDE extension
| 项目 | 内容 |
|------|------|
| 默认值 | true |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

自动安装 Claude Code 的 IDE 扩展（如 VS Code 插件）。

---

### Claude in Chrome enabled by default
| 项目 | 内容 |
|------|------|
| 默认值 | false |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

新会话默认启用 Chrome 浏览器集成（让 Claude 可以控制浏览器）。

---

## 模型与输出

### Model
| 项目 | 内容 |
|------|------|
| 默认值 | 当前模型 ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `model` |

Claude Code 使用的默认 AI 模型。可选 sonnet（均衡）、opus（最强）、haiku（最快）、fable（最新）。也可用 `/model` 命令切换，切换后的选择自动保存为此设置。

---

### Output style
| 项目 | 内容 |
|------|------|
| 默认值 | default ⚠️ |
| 生效范围 | 📁 本地 |
| JSON 键 | `outputStyle` |

输出风格——**直接修改 system prompt**，是对 Claude 行为影响最大的设置。详见下方专门章节。可选 Default / Proactive / Explanatory / Learning / 自定义风格。切换后需 `/clear` 或重启生效。

---

### Language
| 项目 | 内容 |
|------|------|
| 默认值 | Default (English) ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `language` |

Claude 的默认回复语言。设为 `"chinese"` 则 Claude 默认用中文回复。同时也影响语音输入的语言和自动生成的会话标题（v2.1.176+）。不设置时，会话标题跟随对话语言自动匹配。

---

### Diff tool
| 项目 | 内容 |
|------|------|
| 默认值 | auto |
| 生效范围 | 💻 会话 |
| JSON 键 | — |

查看代码差异时使用的对比工具。auto = 自动选择可用的工具。

---

## 通知与更新

### Local notifications
| 项目 | 内容 |
|------|------|
| 默认值 | Auto ✅ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `preferredNotifChannel` |

任务完成和权限提示时的通知方式。可选 Auto、terminal_bell（终端响铃）、iterm2、kitty、ghostty、notifications_disabled。

---

### Auto-update channel
| 项目 | 内容 |
|------|------|
| 默认值 | 取决于环境 ⚠️ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `autoUpdatesChannel` |

自动更新通道。`"latest"` = 最新版，`"stable"` = 稳定版（滞后约一周，跳过重大回归）。如果被环境变量 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 禁用则显示 `disabled (set by env)`。

---

### Editor mode
| 项目 | 内容 |
|------|------|
| 默认值 | normal ✅ |
| 生效范围 | 🌐 用户 |
| JSON 键 | `editorMode` |

输入提示符的键位模式。`"normal"` = 常规编辑，`"vim"` = Vim 风格键位。

---

## 汇总

| 生效范围 | 数量 | 设置 |
|:--:|:--:|------|
| 🌐 用户 | **19** | 大部分行为、模式、通知类设置 |
| 📁 本地 | **3** | Show tips, Reduce motion, Output style |
| 💻 会话 | **9** | 界面显示偏好，重启后恢复默认 |

---

## 🎨 Output Style（输出风格）

> 写入 `.claude/settings.local.json`（📁 本地），直接修改 system prompt。

| 风格 | 作用 |
|------|------|
| **Default** | 标准软件工程助手——默认 system prompt |
| **Proactive** | 自主执行——合理假设、偏好行动而非反复确认 |
| **Explanatory** | 教学解释——在代码任务间插入"Insights"说明设计思路 |
| **Learning** | 互动学习——留 `TODO(human)` 让你亲手写关键代码段 |

切换后需 `/clear` 或重启生效。

自定义风格：创建 `.claude/output-styles/<名称>.md`，设 `keep-coding-instructions: true` 保留默认工程指令，`false` 则为纯自定义角色。

---

## 🚀 学生常用速查

| 想做什么 | 怎么设 |
|------|------|
| 互动教学模式 | `/config` → Output style → **Learning** |
| 切换模型 | `/model haiku` |
| 换主题 | `/theme` |
| Claude 用中文回复 | `/config` → **Language** |
| 手动控制上下文压缩 | `/config` → 关闭 **Auto-compact** |
| 允许 git 命令自动执行 | `/permissions` → 添加 `Bash(git *):*` |
