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

## 📖 Claude Code 的诞生故事

你可能会好奇：**为什么 Claude Code 这么厉害？它是怎么被发明出来的？**

这是一个超酷的真实故事 👇

### 🔬 一个大胆的实验

2024 年 9 月，一位叫 **Boris Cherny** 的工程师加入了 Anthropic 公司。他做了一个大胆的实验：**让 AI 直接看到你的代码文件**。

在此之前，AI 编程助手的工作方式是这样的：

```
你：    "我有一段代码出了 bug..."
AI：    "把代码贴给我看看？"
你：    （复制粘贴代码）
AI：    "试试改成这样..."
你：    （复制粘贴回去）→ 运行 → 还是报错 → 再问 AI → 再改...
```

Boris 想：**如果 AI 能直接看到我的代码，自己运行、自己看报错、自己修改呢？**

于是他给 AI 加了一个"超能力"——**直接访问你的电脑文件和终端**。

### 🤯 意想不到的结果

结果让所有人都惊呆了！

AI 不只是"回答问题更好了"——它开始 **主动探索** 你的项目：
- 📖 自己打开文件，看看项目里有什么
- 🔍 追踪代码之间的依赖关系
- 🧠 理解整个项目的结构
- 🔄 自己运行代码，看到报错就自己修改

**没有人专门教它这样做！** 这个能力是 AI 自己"冒出来"的。

### 🚀 内部爆火

2024 年 11 月，Claude Code 在 Anthropic 公司内部发布。结果：

| 时间 | 使用比例 |
|------|---------|
| 第一天 | **20%** 的工程师在用 |
| 第五天 | **50%** 的工程师在用 |
| 2025 年 5 月（正式发布） | **80%+** 的工程师每天在用 |

工程师们平均每天提交 **5 个代码改动**（一般公司只有 1-2 个），效率提升了 **3-5 倍**！

### 🤖 最酷的事实

Boris Cherny 公开说过：**Claude Code 自身的代码，100% 是由 Claude Code 自己写的！**

没错，Claude Code 是用 Claude Code 写的 —— 这就像一个机器人自己造了自己 🤯

> 🌱 阿基米德说过：**"给我一个支点，我能撬起整个地球。"** Claude Code 就是 Boris 找到的那个支点——它给了 AI "手和脚"，让 AI 从只会聊天变成了能真正动手编程的工具。你现在要学的，就是如何使用这个支点！

---

## 💡 为什么用命令行而不是网页聊天？

你可能会问：**我直接在 DeepSeek 网页上聊天不就好了吗？为什么要用命令行工具？**

这是个好问题！来看看区别：

| | 🌐 网页聊天 | 📟 命令行工具（CLI） |
|--|-----------|-------------------|
| AI 能看到你的代码？ | ❌ 你要自己复制粘贴 | ✅ AI 直接读取你的文件 |
| AI 能运行代码？ | ❌ 只能给你建议 | ✅ AI 自己运行、看报错、修改 |
| 修改代码 | ❌ 你要手动复制粘贴回去 | ✅ AI 直接帮你改文件 |
| 理解整个项目 | ❌ 每次对话从零开始 | ✅ AI 理解整个项目结构 |
| 速度 | 🐢 问→答→复制→粘贴→运行→报错→再问... | ⚡ 说一句话，AI 自动完成所有步骤 |

简单来说：

> 🌐 **网页聊天** = AI 是一个"电话里的顾问"（看不到你的屏幕）
>
> 📟 **命令行工具** = AI 是一个"坐在你旁边的小伙伴"（能看到你的代码、帮你操作）

这就是为什么我们推荐用 **Claude Code** —— 它让 AI 从"只能聊天"变成了"真正能帮你编程"！

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

**Step 1：打开终端（重要！）**

> ⚠️ **先用 CMD（命令提示符），不要用 PowerShell！**
>
> PowerShell 可能会报 "禁止运行脚本" 的错误，需要额外配置。
> 用 CMD 最简单，不会遇到权限问题。

按 `Win + R`，输入 `cmd`，按回车。

![Windows 运行 CMD 截图]

**Step 2：安装 Claude Code**

```bash
npm install -g @anthropic-ai/claude-code
```

> 💡 `npm` 是 Node.js 的包管理器，就像应用商店一样。这个命令是从"应用商店"下载安装 Claude Code。
>
> ⚠️ 如果你不小心用了 PowerShell 并且看到 **"禁止运行脚本"** 的错误，不用慌！关掉 PowerShell，用 CMD 重新安装就行。如果坚持要用 PowerShell，请看下方的问题排查章节。

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

> ⚠️ 如果看到 `EACCES: permission denied` 错误，说明权限不够。在命令前面加 `sudo` 即可：
>
> ```bash
> sudo npm install -g @anthropic-ai/claude-code
> ```
>
> 系统会提示你输入电脑密码（输入时不会显示，这是正常的），输完按回车就行。

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

> ⚠️ 如果看到权限错误，加 `sudo`：
>
> ```bash
> sudo npm install -g @anthropic-ai/claude-code
> ```

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

### Windows 问题

<details>
<summary>❓ PowerShell 提示"禁止运行脚本"</summary>

**错误信息**：
```
无法加载文件 xxx.ps1，因为在此系统上禁止运行脚本。
```

**原因**：Windows PowerShell 为了安全，默认不允许运行来自网络的脚本。

**解决方法（二选一）**：

**方法一（推荐⭐）：改用 CMD**
1. 按 `Win + R`，输入 `cmd`，回车
2. 在 CMD 中重新运行安装命令
3. CMD 不会有执行策略的问题！

**方法二：修改 PowerShell 执行策略**
1. 右键开始菜单 → **「Windows PowerShell（管理员）」** 或 **「终端（管理员）」**
2. 输入以下命令：
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. 输入 `Y` 确认
4. 关闭管理员窗口，重新打开普通 PowerShell
5. 再次运行安装命令

![Windows PowerShell 执行策略错误截图]（待补充）

</details>

<details>
<summary>❓ CMD 提示 "没有权限"</summary>

**解决方法**：右键开始菜单 → 选择 **「命令提示符（管理员）」** 或 **「终端（管理员）」**，在管理员窗口中重新运行安装命令。

</details>

---

### macOS 问题

<details>
<summary>❓ 提示 "EACCES: permission denied"</summary>

**错误信息**：
```
EACCES: permission denied, access '/usr/local/lib/node_modules'
```

**原因**：macOS 系统保护 `/usr/local` 目录，普通用户不能直接写入。

**解决方法（二选一）**：

**方法一（推荐⭐）：使用 sudo**
```bash
sudo npm install -g @anthropic-ai/claude-code
```
系统会提示输入你的电脑密码（**输入时不会显示任何字符，这是正常的！**），输完按回车就行。

**方法二：修复 npm 权限（一劳永逸）**

如果不想每次都输入 `sudo`，可以修改 npm 的全局安装目录到你的用户目录：

```bash
# 1. 创建用户级的全局安装目录
mkdir ~/.npm-global

# 2. 配置 npm 使用新目录
npm config set prefix '~/.npm-global'

# 3. 把新目录加入 PATH（添加到 ~/.zshrc 或 ~/.bash_profile）
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# 4. 现在可以不用 sudo 了！
npm install -g @anthropic-ai/claude-code
```

> 💡 方法二操作稍多，但以后装其他包也不需要 sudo。建议有时间的时候做。

![macOS EACCES 权限错误截图]（待补充）

</details>

---

### Linux 问题

<details>
<summary>❓ 提示权限不足</summary>

**解决方法**：
```bash
sudo npm install -g @anthropic-ai/claude-code
```
输入你的用户密码（不会显示），按回车即可。

</details>

---

### 通用问题

<details>
<summary>❓ "npm 不是内部或外部命令"</summary>

**原因**：Node.js 没有安装成功。

**解决**：
1. 重新下载 Node.js：https://nodejs.org/
2. 安装时确保勾选了 **"Add to PATH"**（一般默认勾选）
3. 安装完 **重新打开** 终端再试

</details>

<details>
<summary>❓ 安装很慢或报网络错误</summary>

**原因**：国内访问 npm 官方源可能比较慢。

**解决**：使用国内镜像源：
```bash
npm install -g @anthropic-ai/claude-code --registry=https://registry.npmmirror.com
```

</details>

<details>
<summary>❓ "claude 不是内部或外部命令"</summary>

**原因**：npm 全局安装路径没有加入 PATH。

**解决**：
1. **关闭终端，重新打开** 再试（很多时候这就解决了！）
2. 如果还不行，重启电脑
3. 检查 npm 全局路径：
   ```bash
   npm config get prefix
   ```
4. 把输出的路径加到系统的 PATH 环境变量中

</details>

---

[⬅️ 上一页：安装 Node.js](./02-nodejs.md) | [➡️ 下一页：配置 DeepSeek](./04-config.md)
