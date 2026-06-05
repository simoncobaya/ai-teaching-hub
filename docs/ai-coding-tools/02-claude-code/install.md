# 📥 安装 Claude Code

> 在你的电脑上安装 Claude Code，准备开始 AI 编程之旅！

---

## 🎯 目标

完成这一步后，你将拥有：
- ✅ 安装好的 Claude Code

---

## 📋 前置条件

安装 Claude Code 之前，你需要先安装 **Node.js**（版本 18 或更高）。

👉 **[安装 Node.js 教程](../00-introduction/install-nodejs.md)** — 如果你还没安装 Node.js，先去看这个教程！

---

## 🚀 安装 Claude Code

### Windows 系统

#### Step 1：打开终端

按 `Win + R`，输入 `cmd`，按回车。

或者搜索"PowerShell"打开。

#### Step 2：安装 Claude Code

在终端中输入以下命令：

```bash
npm install -g @anthropic-ai/claude-code
```

> 💡 `npm` 是 Node.js 的包管理器，就像应用商店一样。这个命令是从"应用商店"下载安装 Claude Code。

#### Step 3：验证安装

```bash
claude --version
```

如果显示版本号，说明安装成功！🎉

---

### macOS 系统

#### Step 1：打开终端

按 `Command + 空格`，搜索"Terminal"，打开。

#### Step 2：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

#### Step 3：验证安装

```bash
claude --version
```

---

### Linux 系统

#### Step 1：打开终端

用快捷键 `Ctrl + Alt + T` 打开终端。

#### Step 2：安装 Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

#### Step 3：验证安装

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

## 🔑 登录（可选）

安装完成后，你有 **两种方式** 开始使用 Claude Code：

### 路径 A：用 DeepSeek 模型（⭐ 推荐给学生！）

> 💡 **没有 Claude 订阅？完全没问题！**
>
> 大多数同学不需要购买 Claude 订阅。直接配置 **DeepSeek** 模型，便宜又好用！
>
> 👉 **[配置 DeepSeek 教程](../03-deepseek-claudecode/README.md)** — 这是我们推荐的路径！

### 路径 B：登录 Claude 账号（适合已有订阅的同学）

如果你已经有 Claude 订阅，可以登录使用：

1. 在终端中输入 `claude` 启动
2. Claude Code 会自动打开浏览器，让你登录 Claude 账号
3. 登录成功后就可以使用了！🎉

登录需要以下 **任意一种** Claude 订阅：

| 订阅 | 费用 | 说明 |
|------|------|------|
| 🌟 Claude Pro | $20/月 | 最适合个人使用 |
| 🚀 Claude Max | $100/月 | 无限制使用 |
| 👥 Claude Team | 团队版 | 适合团队 |
| 🏢 Claude Enterprise | 企业版 | 适合企业 |

---

## ⚠️ 遇到问题？

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

### 问题 4：登录时浏览器没有打开

**解决**：
1. 在 Claude Code 里输入 `/login` 重新触发登录
2. 如果还是不行，检查终端里显示的链接，手动复制到浏览器打开

---

## 📌 下一步

Claude Code 安装好了！接下来最重要的一步：

👉 **[⭐ 配置 Claude Code + DeepSeek](../03-deepseek-claudecode/README.md)** — 让 Claude Code 使用便宜的 DeepSeek 模型

配置完成后，再回来学习怎么使用：

👉 **[Claude Code 基础用法](./basics.md)** — 学会和 Claude Code 对话
