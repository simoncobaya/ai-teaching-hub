# ⌨️ Claude Code 内置命令完整指南

> 来源：[Claude Code 官方 Commands 文档](https://code.claude.com/docs/en/commands) · v2.1.181。可用命令因平台、计划和环境而异，输入 `/` 查看当前环境实际列表。

---

## 🟢 会话管理

| 命令 | 用途 |
|------|------|
| `/clear [名称]` | 清空对话，旧对话可在 `/resume` 中恢复（别名 `/reset`、`/new`） |
| `/compact [指令]` | 压缩上下文，释放 token 空间 |
| `/resume [会话]` | 恢复之前的会话（别名 `/continue`） |
| `/rename [名称]` | 重命名当前会话 |
| `/branch [名称]` | 从当前对话分叉出新分支，探索不同方向 |
| `/fork <指令>` | 派生子 Agent 在后台工作，完成后返回结果（v2.1.161+） |
| `/rewind` | 回退到之前的检查点（别名 `/checkpoint`、`/undo`） |
| `/export [文件名]` | 导出对话到文件或剪贴板 |
| `/copy [N]` | 复制回复到剪贴板，`/copy 2` 复制倒数第二次 |
| `/context [all]` | 查看上下文用量（彩色网格图） |
| `/recap` | 生成一句话会话摘要 |
| `/btw <问题>` | 临时问题，回答不留在对话历史里 |
| `/background [指令]` | 将当前会话转入后台运行（别名 `/bg`） |
| `/stop` | 停止后台会话。仅在附加到后台会话时可用，普通会话中不显示 |
| `/cd <路径>` | 切换工作目录，保留 prompt 缓存（v2.1.169+） |
| `/diff` | 交互式查看代码变更 |

---

## 🔵 模型与思考

| 命令 | 用途 |
|------|------|
| `/model [模型]` | 切换模型（sonnet/opus/haiku/fable），保存为新默认 |
| `/effort [级别\|auto]` | 思考深度：`low`/`medium`/`high`/`xhigh`/`max`/`ultracode` |
| `/fast [on\|off]` | 切换快速模式（仅 Anthropic API/订阅 + Opus 模型 + 开启 usage credits 时可用。Bedrock/Vertex/Foundry/第三方 API 不可用。v2.1.36+） |
| `/plan [描述]` | 进入规划模式——只探索和设计，不写代码 |
| `/goal [条件\|clear]` | 设定完成目标，Claude 跨轮次持续推进 |
| `/advisor [model\|off]` | 启用顾问工具——第二个模型在关键决策点提供建议（v2.1.98+）。仅 Anthropic API 可用，Bedrock/Vertex/Foundry/第三方 API 代理不可用。主模型需 Opus 4.6+ / Sonnet 4.6+ / Haiku 4.5+ / Fable 5（v2.1.170+） |

---

## 🟡 项目与配置

| 命令 | 用途 |
|------|------|
| `/init` | 为项目创建 `CLAUDE.md` |
| `/memory` | 编辑 CLAUDE.md 记忆文件，管理 auto-memory |
| `/config [key=value]` | 打开设置面板，或直接设值如 `/config theme=dark`（v2.1.181+） |
| `/permissions` | 管理工具权限规则（别名 `/allowed-tools`） |
| `/add-dir <路径>` | 添加工作目录 |
| `/theme` | 换主题（含色盲友好主题和自定义主题） |
| `/color [颜色\|default]` | 换提示栏颜色（red/blue/green/yellow/purple/orange/pink/cyan） |
| `/status` | 查看版本、模型、账户信息 |
| `/keybindings` | 编辑键盘快捷键 |
| `/statusline` | 配置状态栏 |
| `/sandbox` | 切换沙盒模式。仅在支持的平台上可用 |
| `/terminal-setup` | 配置终端快捷键。仅在需要配置的终端中可见（如 VS Code、Cursor、Alacritty、Zed 等） |
| `/tui [default\|fullscreen]` | 切换终端 UI 渲染器 |
| `/focus` | 切换专注视图。仅在[全屏渲染模式](/en/fullscreen)下可用 |
| `/scroll-speed` | 调整鼠标滚轮速度。仅在[全屏渲染模式](/en/fullscreen)下可用 |

---

## 🟠 代码审查与质量

| 命令 | 用途 |
|------|------|
| `/code-review [级别] [--fix] [--comment]` | 审查代码质量（内置技能），`--fix` 自动修复，`ultra` 云端深度审查 |
| `/review [PR]` | 在本地会话中审查 PR |
| `/code-review ultra` | 云端多 Agent 深度审查（需要 Pro/Max 计划的 [usage credits](https://support.claude.com/en/articles/12429409)，含 3 次免费） |
| `/ultrareview [PR]` | `/code-review ultra` 的别名 |
| `/ultraplan <指令>` | 在云端起草计划，浏览器中审阅，然后远程执行或发回终端 |
| `/security-review` | 扫描安全漏洞 |
| `/simplify [目标]` | 清理代码，自动应用修复（v2.1.154+） |
| `/run` | 启动项目应用验证改动（内置技能，v2.1.145+） |
| `/verify` | 确认代码改动达到预期效果（内置技能，v2.1.145+） |
| `/run-skill-generator` | 教 `/run` 和 `/verify` 如何启动你的项目（内置技能，v2.1.145+） |

---

## 🟣 系统与诊断

| 命令 | 用途 |
|------|------|
| `/help` | 列出所有可用命令 |
| `/doctor` | 诊断安装和配置 |
| `/usage` | 查看用量仪表盘（别名 `/cost`、`/stats`） |
| `/debug [描述]` | 启用调试日志并分析（内置技能） |
| `/feedback [报告]` | 提交反馈或 Bug 报告（别名 `/bug`、`/share`） |
| `/release-notes` | 交互式查看更新日志 |
| `/insights` | 生成使用模式分析报告 |
| `/heapdump` | 导出内存快照用于诊断 |
| `/login` / `/logout` | 登录/登出 |

---

## 🟤 扩展管理

| 命令 | 用途 |
|------|------|
| `/plugin [子命令]` | 管理插件（list/install/enable/disable） |
| `/skills` | 查看已安装的 Skill 列表 |
| `/agents` | 管理子 Agent 配置 |
| `/mcp [操作]` | 管理 MCP 服务器连接 |
| `/hooks` | 查看和管理 Hook 配置 |
| `/reload-skills` | 重新扫描 Skill 目录（v2.1.152+） |
| `/reload-plugins [--force]` | 重新加载插件 |

---

## ⚫ 后台与自动化

| 命令 | 用途 |
|------|------|
| `/tasks` | 查看后台任务 |
| `/loop [间隔] [指令]` | 定时重复执行（内置技能，别名 `/proactive`） |
| `/schedule [描述]` | 创建云端定时任务（别名 `/routines`） |
| `/batch <指令>` | 大规模并行重构（内置技能）。需要 git 仓库 |
| `/workflows` | 查看运行中的工作流 |
| `/autofix-pr [指令]` | 派云端会话监控 PR，CI 失败时自动推送修复。需要 `gh` CLI 和 Claude Code Web 访问权限 |
| `/deep-research <问题>` | 多源网络调研，生成带引用报告（内置工作流） |
| `/claude-api` | 加载 Claude API 参考文档（内置技能） |
| `/fewer-permission-prompts` | 扫描历史，自动添加权限白名单（内置技能） |

---

## 🌐 跨设备

| 命令 | 用途 |
|------|------|
| `/teleport` | 将 Web 会话拉到终端（别名 `/tp`）。需要 claude.ai 订阅 |
| `/remote-control` | 开启远程控制，从 claude.ai 控制此会话（别名 `/rc`） |
| `/desktop` | 切换到桌面 App（别名 `/app`）。需要 macOS 或 Windows + Claude 订阅，不满足条件时不显示 |
| `/mobile` | 显示 Claude 手机 App 下载二维码（别名 `/ios`、`/android`） |
| `/web-setup` | 连接 GitHub 账户到 Claude Code Web |
| `/remote-env` | 选择云端 Agent 的默认环境 |

---

## 💳 订阅相关

| 命令 | 用途 |
|------|------|
| `/upgrade` | 打开升级页面。仅 Pro 和 Max 计划可见 |
| `/privacy-settings` | 隐私设置。仅 Pro 和 Max 计划 |
| `/usage-credits` | 配置额外用量积分 |
| `/passes` | 分享免费体验周。仅符合条件的账户可见 |
| `/stickers` | 订购 Claude Code 贴纸 |
| `/radio` | 打开 Claude FM lo-fi 电台。Bedrock、Vertex、Foundry 不可用 |

---

## ☁️ 云平台专用

| 命令 | 用途 |
|------|------|
| `/setup-bedrock` | 配置 Amazon Bedrock。仅 `CLAUDE_CODE_USE_BEDROCK=1` 时可见 |
| `/setup-vertex` | 配置 Google Vertex AI。仅 `CLAUDE_CODE_USE_VERTEX=1` 时可见 |

---

## 🔧 其他

| 命令 | 用途 |
|------|------|
| `/powerup` | 通过互动教程发现功能 |
| `/team-onboarding` | 生成团队上手指南 |
| `/install-github-app` | 配置 Claude GitHub Actions |
| `/install-slack-app` | 安装 Claude Slack App |
| `/voice [hold\|tap\|off]` | 切换语音输入。需要 claude.ai 账户 |
| `/exit` | 退出 CLI（别名 `/quit`） |

---

## ❌ 已移除

| 命令 | 状态 |
|------|------|
| `/vim` | v2.1.92 移除 → 用 `/config` → Editor mode |
| `/pr-comments` | v2.1.91 移除 → 直接让 Claude 查看 PR 评论 |

---

> 💡 输入 `/` 可查看当前环境所有可用命令，输入 `/` 后继续输入字母可筛选。不同平台、不同计划看到的命令可能不同。
