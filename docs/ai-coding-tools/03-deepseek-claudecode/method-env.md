# 📝 方式二：手动配置（settings.json 或环境变量）

> 手动编辑配置文件或设置环境变量来配置 Claude Code + DeepSeek。适合喜欢自己动手的同学 ✏️

---

## 🎯 目标

通过编辑 settings.json 或设置环境变量，让 Claude Code 使用 DeepSeek 的 API。

> 📖 **参考文档**：[DeepSeek 官方 - 接入 Claude Code](https://api-docs.deepseek.com/zh-cn/quick_start/agent_integrations/claude_code)

---

## 📋 你需要准备

- [ ] ✅ DeepSeek API Key（在 [DeepSeek Platform](https://platform.deepseek.com/) 获取）
- [ ] ✅ Claude Code 已安装
- [ ] ✅ 知道怎么打开和编辑文件

---

## 🔍 需要设置的环境变量

在开始之前，先了解一下每个环境变量的作用 👇

| 环境变量 | 作用 | 填什么 |
|---------|------|--------|
| `ANTHROPIC_AUTH_TOKEN` | 你的 API Key 🔑 | 你的 DeepSeek API Key |
| `ANTHROPIC_BASE_URL` | API 地址 🌐 | `https://api.deepseek.com/anthropic` |
| `ANTHROPIC_MODEL` | 主力模型 🧠 | `deepseek-v4-pro[1m]` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | Opus 级别模型 | `deepseek-v4-pro[1m]` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME` | Opus 模型显示名 | `deepseek-v4-pro` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Sonnet 级别模型 | `deepseek-v4-pro[1m]` |
| `ANTHROPIC_DEFAULT_SONNET_MODEL_NAME` | Sonnet 模型显示名 | `deepseek-v4-pro` |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | Haiku 级别模型（轻量）⚡ | `deepseek-v4-flash` |
| `CLAUDE_CODE_EFFORT_LEVEL` | 努力程度 💪 | `max`（全力以赴！） |

> 💡 **小贴士**：
> - `deepseek-v4-pro[1m]` 是 DeepSeek 最强大的模型，`[1m]` 表示支持 **100 万** Token 的超长上下文窗口，用来处理复杂的编程任务
> - `deepseek-v4-flash` 是更轻快、更便宜的模型，用来处理简单的小任务

---

## 🚀 配置步骤

### 📁 找到配置文件

不管你用什么系统，首先找到 Claude Code 的配置文件：

| 系统 | 路径 |
|------|------|
| **Windows** | `C:\Users\你的用户名\.claude\settings.json` |
| **macOS** | `~/.claude/settings.json` |
| **Linux** | `~/.claude/settings.json` |

> 💡 `~` 代表你的用户主目录。比如在 macOS 上就是 `/Users/你的用户名/`，在 Linux 上是 `/home/你的用户名/`。

---

### macOS / Linux 系统

#### 方法 A：编辑 settings.json（⭐ 推荐）

**Step 1：打开配置文件**

用你喜欢的文本编辑器打开 `~/.claude/settings.json`：

```bash
# 用 VS Code 打开（推荐）
code ~/.claude/settings.json

# 或者用 nano 打开
nano ~/.claude/settings.json
```

> ⚠️ 如果文件不存在，就新建一个。如果文件夹 `.claude` 也不存在，先创建它：`mkdir -p ~/.claude`

**Step 2：写入配置**

如果文件是空的或新建的，把下面的内容**完整复制**进去：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的DeepSeek-API-Key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

如果文件里已经有内容，找到或添加 `"env"` 字段，把上面的环境变量加进去。

**Step 3：替换 API Key**

把 `sk-你的DeepSeek-API-Key` 替换成你的**真实 API Key**。

**Step 4：保存文件**

按 `Ctrl + S`（或 `Command + S`）保存文件。

> 💡 这种方式设置后会**永久生效**，而且只对 Claude Code 有效，不会影响其他程序。

---

#### 方法 B：在终端中临时设置

打开终端，逐行粘贴执行：

```bash
export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
export ANTHROPIC_AUTH_TOKEN="sk-你的DeepSeek-API-Key"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL_NAME="deepseek-v4-pro"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL="max"
```

> ⚠️ **注意**：这种设置只在**当前终端窗口**有效，关闭窗口后就失效了。

---

#### 方法 C：写入 Shell 配置文件（永久生效）

如果你希望每次打开终端都自动设置好，可以把环境变量写到 Shell 配置文件里。

**Zsh 用户**（macOS 默认）：编辑 `~/.zshrc`

```bash
echo 'export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"' >> ~/.zshrc
echo 'export ANTHROPIC_AUTH_TOKEN="sk-你的DeepSeek-API-Key"' >> ~/.zshrc
echo 'export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"' >> ~/.zshrc
echo 'export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"' >> ~/.zshrc
echo 'export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME="deepseek-v4-pro"' >> ~/.zshrc
echo 'export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"' >> ~/.zshrc
echo 'export ANTHROPIC_DEFAULT_SONNET_MODEL_NAME="deepseek-v4-pro"' >> ~/.zshrc
echo 'export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"' >> ~/.zshrc
echo 'export CLAUDE_CODE_EFFORT_LEVEL="max"' >> ~/.zshrc
source ~/.zshrc
```

**Bash 用户**（部分 Linux 默认）：编辑 `~/.bashrc`

```bash
echo 'export ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"' >> ~/.bashrc
echo 'export ANTHROPIC_AUTH_TOKEN="sk-你的DeepSeek-API-Key"' >> ~/.bashrc
echo 'export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"' >> ~/.bashrc
echo 'export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"' >> ~/.bashrc
echo 'export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME="deepseek-v4-pro"' >> ~/.bashrc
echo 'export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"' >> ~/.bashrc
echo 'export ANTHROPIC_DEFAULT_SONNET_MODEL_NAME="deepseek-v4-pro"' >> ~/.bashrc
echo 'export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"' >> ~/.bashrc
echo 'export CLAUDE_CODE_EFFORT_LEVEL="max"' >> ~/.bashrc
source ~/.bashrc
```

> ⚠️ **注意**：这种方式会把 API Key 写在文件里，请确保电脑只有你一个人使用！

---

### Windows 系统

#### 方法 A：编辑 settings.json（⭐ 推荐）

**Step 1：打开配置文件**

配置文件在 `C:\Users\你的用户名\.claude\settings.json`。

用你喜欢的编辑器打开：
- 📝 **记事本**（Windows 自带）
- 📝 **VS Code**（推荐，免费好用）

> ⚠️ `.claude` 可能是隐藏文件夹。你可以在文件管理器的地址栏直接输入路径，或者在 PowerShell 中执行：`code $env:USERPROFILE\.claude\settings.json`

**Step 2：写入配置**

如果文件是空的或新建的，把下面的内容**完整复制**进去：

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-你的DeepSeek-API-Key",
    "ANTHROPIC_BASE_URL": "https://api.deepseek.com/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "deepseek-v4-flash",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_OPUS_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "deepseek-v4-pro[1m]",
    "ANTHROPIC_DEFAULT_SONNET_MODEL_NAME": "deepseek-v4-pro",
    "ANTHROPIC_MODEL": "deepseek-v4-pro[1m]",
    "CLAUDE_CODE_EFFORT_LEVEL": "max"
  }
}
```

如果文件里已经有内容，找到或添加 `"env"` 字段，把上面的环境变量加进去。

**Step 3：替换 API Key**

把 `sk-你的DeepSeek-API-Key` 替换成你的**真实 API Key**。

**Step 4：保存文件**

按 `Ctrl + S` 保存文件。

> 💡 这种方式设置后会**永久生效**，而且只对 Claude Code 有效。

---

#### 方法 B：在 PowerShell 中临时设置

打开 PowerShell，逐行粘贴执行：

```powershell
$env:ANTHROPIC_BASE_URL = "https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN = "sk-你的DeepSeek-API-Key"
$env:ANTHROPIC_MODEL = "deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL = "deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL_NAME = "deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL = "deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL_NAME = "deepseek-v4-pro"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL = "deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL = "max"
```

> ⚠️ **注意**：这种设置只在**当前 PowerShell 窗口**有效，关闭窗口后就失效了。

---

#### 方法 C：在 CMD（命令提示符）中临时设置

打开 CMD，逐行粘贴执行：

```cmd
set ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
set ANTHROPIC_AUTH_TOKEN=sk-你的DeepSeek-API-Key
set ANTHROPIC_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_OPUS_MODEL_NAME=deepseek-v4-pro
set ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro[1m]
set ANTHROPIC_DEFAULT_SONNET_MODEL_NAME=deepseek-v4-pro
set ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash
set CLAUDE_CODE_EFFORT_LEVEL=max
```

> ⚠️ **注意**：同样只在**当前 CMD 窗口**有效。

---

## 📊 方法对比

| 方法 | 生效范围 | 持久性 | 安全性 |
|------|---------|--------|--------|
| settings.json 的 env | Claude Code | 永久 ✅ | ⭐⭐⭐ 较安全 |
| 终端临时设置 | 当前终端 | 关闭即失效 | ⭐⭐⭐⭐ 最安全 |
| Shell 配置文件 | 所有终端 | 永久 ✅ | ⭐⭐ API Key 在文件里 |

> 💡 **推荐**：使用 **settings.json 的 env 方式**，既持久又比较安全！

---

## ✅ 验证

设置完成后，进入你的项目目录，启动 Claude Code：

```bash
cd /path/to/my-project
claude
```

> 📝 把 `/path/to/my-project` 替换成你自己的项目路径哦！

然后发送一条消息测试：

```
你好，请告诉我你现在用的是哪个模型
```

如果一切正常，Claude Code 会通过 DeepSeek 的 API 回复你！🎉

---

## ❓ 常见问题

### Q：settings.json 的 JSON 格式报错？

检查以下几点：
- 每个键值对后面有没有多余的逗号 `,`
- 有没有缺少引号 `"`
- 最后一个元素后面**不能有逗号**

> 💡 可以用 JSON 验证工具检查：https://jsonlint.com/

### Q：找不到 .claude 文件夹？

- **macOS / Linux**：在终端执行 `mkdir -p ~/.claude`
- **Windows**：`.claude` 可能是隐藏文件夹。你可以在文件管理器的地址栏直接输入路径，或者在 PowerShell 中执行 `New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude"`

### Q：环境变量设置后不生效？

1. **关闭终端，重新打开** 再试一次
2. 检查是否拼写正确（注意大小写，变量名全是**大写字母**）
3. 确认 API Key 没有多余的空格或引号
4. 如果用的是 settings.json，检查 JSON 格式是否正确（逗号、括号别漏了）

### Q：想切换回 Claude 怎么办？

**临时方法**：删除环境变量

```bash
# macOS / Linux
unset ANTHROPIC_BASE_URL
unset ANTHROPIC_AUTH_TOKEN
unset ANTHROPIC_MODEL
unset ANTHROPIC_DEFAULT_OPUS_MODEL
unset ANTHROPIC_DEFAULT_OPUS_MODEL_NAME
unset ANTHROPIC_DEFAULT_SONNET_MODEL
unset ANTHROPIC_DEFAULT_SONNET_MODEL_NAME
unset ANTHROPIC_DEFAULT_HAIKU_MODEL
unset CLAUDE_CODE_EFFORT_LEVEL
```

```powershell
# Windows PowerShell
Remove-Item Env:ANTHROPIC_BASE_URL
Remove-Item Env:ANTHROPIC_AUTH_TOKEN
Remove-Item Env:ANTHROPIC_MODEL
Remove-Item Env:ANTHROPIC_DEFAULT_OPUS_MODEL
Remove-Item Env:ANTHROPIC_DEFAULT_OPUS_MODEL_NAME
Remove-Item Env:ANTHROPIC_DEFAULT_SONNET_MODEL
Remove-Item Env:ANTHROPIC_DEFAULT_SONNET_MODEL_NAME
Remove-Item Env:ANTHROPIC_DEFAULT_HAIKU_MODEL
Remove-Item Env:CLAUDE_CODE_EFFORT_LEVEL
```

```cmd
# Windows CMD
set ANTHROPIC_BASE_URL=
set ANTHROPIC_AUTH_TOKEN=
set ANTHROPIC_MODEL=
set ANTHROPIC_DEFAULT_OPUS_MODEL=
set ANTHROPIC_DEFAULT_OPUS_MODEL_NAME=
set ANTHROPIC_DEFAULT_SONNET_MODEL=
set ANTHROPIC_DEFAULT_SONNET_MODEL_NAME=
set ANTHROPIC_DEFAULT_HAIKU_MODEL=
set CLAUDE_CODE_EFFORT_LEVEL=
```

**永久方法**：从 settings.json 或 shell 配置文件中删除对应行。

### Q：可以同时用多种配置方式吗？

不建议。选择 **一种** 方式即可，多种方式可能会冲突。

### Q：`ANTHROPIC_BASE_URL` 末尾的 `/anthropic` 可以省略吗？

❌ **不可以！** 这个 `/anthropic` 是 DeepSeek 的 Anthropic 兼容接口路径，少了它 Claude Code 就找不到 API 了。

---

## 📌 下一步

👉 **[验证配置是否成功](./verify.md)**

👉 **[实践：让 AI 帮你写个猜数字游戏 🎮](./first-project.md)**
