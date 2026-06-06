# 🤖 认识 + 安装 Claude Code

> Claude Code 是一个住在终端里的 AI 编程小伙伴。你跟它说话，它就帮你写代码、改代码、运行程序！

---

## 🤔 Claude Code 是什么？

Claude Code 是 **Anthropic 公司**（就是做 Claude AI 的公司）开发的 **终端编程工具**。

简单理解：
- 📟 它运行在一个 **黑色的终端窗口** 里
- 💬 你用 **自然语言**（普通的话）和它对话
- 💻 它帮你 **写代码、改代码、运行程序**
- 📁 它能 **理解整个项目**，不只是单个文件

### 🌟 Claude Code 的超能力

- 📖 **读懂整个项目** — 知道哪些文件互相依赖，理解项目结构
- 🔧 **直接操作文件** — 创建、修改、删除文件和文件夹
- ▶️ **运行命令** — 运行程序、安装依赖、查找文件
- 🔄 **支持多种 AI 模型** — 不只能用 Claude，还能用 DeepSeek、GLM 等

> ⭐ **这就是为什么我们要配置 Claude Code + DeepSeek** — 用最好的工具搭配最便宜的模型！

---

## 💰 费用说明

> 💰 **重要说明**：
> - Claude Code 工具本身是 **免费** 的
> - 但默认情况下需要 **Claude 账号**（付费订阅）
> - ⭐ **好消息**：配置 DeepSeek 后，**不需要 Claude 账号**，而且费用超便宜！

---

## 📥 安装 Claude Code

### 📋 前置条件

安装 Claude Code 之前，你需要先安装 **Node.js**（版本 18 或更高）。

👉 如果你还没安装 Node.js，请先看上一页的教程！

### 🚀 安装步骤

#### Windows 系统

**Step 1：打开终端**

按 `Win + R`，输入 `cmd`，按回车。或者搜索"PowerShell"打开。

**Step 2：安装 Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

> 💡 `npm` 是 Node.js 的包管理器，就像应用商店一样。这个命令是从"应用商店"下载安装 Claude Code。

**Step 3：验证安装**

```bash
claude --version
```

如果显示版本号，说明安装成功！🎉

---

#### macOS 系统

**Step 1：打开终端**

按 `Command + 空格`，搜索"Terminal"，打开。

**Step 2：安装 Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

**Step 3：验证安装**

```bash
claude --version
```

---

#### Linux 系统

**Step 1：打开终端**

用快捷键 `Ctrl + Alt + T` 打开终端。

**Step 2：安装 Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

**Step 3：验证安装**

```bash
claude --version
```

---

<details>
<summary>🌐 备选安装方式（适合海外用户）</summary>

如果你在海外或有代理，也可以用 **官方安装脚本**（不需要 Node.js）：

**macOS / Linux：**

```bash
curl -fsSL https://claude.ai/install.sh | sh
```

**Windows PowerShell：**

```powershell
irm https://claude.ai/install.ps1 | iex
```

**macOS Homebrew：**

```bash
brew install --cask claude-code
```

> ⚠️ 国内用户注意：Anthropic 不向国内提供服务，这些官方链接在国内可能无法使用。推荐使用上面的 npm 方式。

</details>

---

## ✅ 验证安装

安装完成后，试着运行一下：

```bash
claude
```

你会看到一个欢迎界面，可能会提示你登录：

```
Welcome to Claude Code! 🤖

Please log in to continue...
```

> ⚠️ **看到登录提示是正常的！不用慌！**
>
> 你 **不需要** 注册 Claude 账号，也 **不需要** 在这里登录。
>
> 👉 下一步我们会配置 DeepSeek，配置完成后就可以直接使用了！

按 `Ctrl + C` 退出即可。

---

## ⚠️ 安装遇到问题？

### 问题 1："'npm' 不是内部或外部命令"

**原因**：Node.js 没有安装成功。

**解决**：
1. 重新下载 Node.js：https://nodejs.org/
2. 安装时确保勾选了"Add to PATH"
3. 安装完 **重新打开** 终端

### 问题 2：安装很慢或报错

**原因**：可能是网络问题。

**解决**：试试使用国内镜像源：

```bash
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

### 问题 3："'claude' 不是内部或外部命令"

**原因**：npm 全局安装路径没有加入 PATH。

**解决**：
1. 关闭终端，重新打开
2. 如果还不行，重启电脑
3. 还不行的话，检查 npm 全局路径：

```bash
npm config get prefix
```

把这个路径加到系统的 PATH 环境变量中。

---

[⬅️ 上一页：安装 Node.js](./02-nodejs.md) | [➡️ 下一页：配置 DeepSeek](./04-config.md)
