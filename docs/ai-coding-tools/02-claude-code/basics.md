# 📖 Claude Code 基础用法

> 学会和 Claude Code 对话，让它帮你写代码！

---

> ⚠️ **重要提示**：你需要 **先完成 DeepSeek 配置**，才能实际操作下面的练习！
>
> 如果还没配置，请先去 👉 **[配置 Claude Code + DeepSeek](../03-deepseek-claudecode/README.md)**
>
> 配置完成后，再回来学习使用方法。

---

## 🎯 目标

学完这一节，你将知道：
- ✅ 如何启动和退出 Claude Code
- ✅ 如何和 Claude Code 对话
- ✅ 常用的命令

---

## 🚀 启动 Claude Code

### Step 1：创建一个项目文件夹

首先，创建一个文件夹来放你的代码：

**macOS / Linux（终端）：**

```bash
mkdir my-first-project
cd my-first-project
```

**Windows（PowerShell 或 CMD）：**

```powershell
mkdir my-first-project
cd my-first-project
```

> 💡 这几个系统的命令其实是一样的！都可以直接复制粘贴。

### Step 2：启动 Claude Code

```bash
claude
```

你会看到 Claude Code 的欢迎界面！🎉

### Step 3：信任项目文件夹（首次使用时）

第一次在一个新文件夹里使用 Claude Code 时，它会问你一个问题：

```
Accessing workspace: /你的项目文件夹路径

Quick safety check: Is this a project you created or one you trust?

❯ 1. Yes, I trust this folder
   2. No, exit
```

- 如果你**自己创建**了这个文件夹 → 选 **1. Yes, I trust this folder**（按回车）
- 如果你**不确定**这个文件夹里有什么 → 选 **2. No, exit**，先看看再说

> 💡 这是 Claude Code 的安全保护，确保它不会在你不知道的文件夹里乱改文件。
> 下次再打开同一个文件夹，就不会再问这个问题了。

> 💡 **快捷用法**：如果你只想让 AI 做一件事，不用进入对话模式，直接写：
> ```bash
> claude "帮我写一个 Hello World 程序"
> ```
> 这样 Claude Code 会直接帮你完成任务，做完就退出！

---

## 💬 和 Claude Code 对话

启动后，你就可以直接 **打字和 Claude Code 对话** 了！

### 试试这些对话

#### 对话 1：让 AI 写代码

```
你：帮我用 Python 写一个打印"Hello World"的程序
```

Claude Code 会帮你创建一个 Python 文件并写入代码。

#### 对话 2：让 AI 解释代码

```
你：请解释一下这个项目里的代码都在做什么
```

Claude Code 会读取你的项目文件，然后用简单的语言解释。

#### 对话 3：让 AI 修改代码

```
你：请把猜数字游戏的范围改成 1-1000
```

Claude Code 会找到相关文件并修改代码。

#### 对话 4：让 AI 运行程序

```
你：运行猜数字游戏
```

Claude Code 会帮你执行程序。

---

## ⌨️ 常用命令

在 Claude Code 里，以 `/` 开头的是特殊命令：

| 命令 | 作用 | 例子 |
|------|------|------|
| `/help` | 查看帮助 | 显示所有可用命令 |
| `/model` | 切换 AI 模型层级 | `/model sonnet` |
| `/login` | 登录账号 | 重新登录或切换账号 |
| `/config` | 打开设置 | 查看/修改配置 |
| `/clear` | 清空对话 | 开始新的对话 |
| `/compact` | 压缩上下文 | 对话太长时使用 |
| `/quit` | 退出 Claude Code | 结束会话 |

### 最常用的命令

```
/model             ← 查看可用的模型列表
/model sonnet      ← 切换到 Sonnet（日常使用）
/model opus        ← 切换到 Opus（最强，适合难题）
/model haiku       ← 切换到 Haiku（最快，适合简单任务）
```

> 💡 `/model` 只能在 opus、sonnet、haiku 之间切换。如果你用 CC Switch 配置了 DeepSeek，这些模型实际调用的就是 DeepSeek。要在不同供应商（DeepSeek ↔ Claude）之间切换，请在 **CC Switch** 中操作。

---

## 📂 Claude Code 如何操作文件

Claude Code 会 **自动** 帮你操作文件，但每次操作前都会 **问你确认**：

| 操作 | 你会看到 | 你要做的 |
|------|---------|---------|
| 创建文件 | 📝 "创建文件 xxx" | 按 `y` 确认 |
| 修改文件 | ✏️ "修改 xxx 第 10 行" | 按 `y` 确认 |
| 运行命令 | ▶️ "运行命令 xxx" | 按 `y` 确认 |

> 💡 **安全提示**：Claude Code 每次操作都会问你，不会偷偷改你的文件。如果你不确定，可以按 `n` 拒绝。

---

## 🎮 实战练习

让我们用 Claude Code 写一个简单的程序！

### 练习 1：Hello World

1. 启动 Claude Code
2. 输入：
   ```
   帮我用 Python 写一个 Hello World 程序
   ```
3. 按 `y` 确认创建文件
4. 输入：
   ```
   运行这个程序
   ```
5. 按 `y` 确认运行

### 练习 2：让 AI 做网页

试试这些有趣的对话：

```
帮我用 HTML 写一个显示"我喜欢 AI 🤖"的网页，要有好看的背景和字体
```

```
帮我用 HTML + JavaScript 写一个九九乘法表网页
```

---

## 🔄 退出 Claude Code

对话结束后，你可以用以下方式退出：

- 输入 `/quit`
- 或按 `Ctrl + C` 两次

---

## ❓ 常见问题

### Q：Claude Code 需要联网吗？
**是的！** Claude Code 需要联网才能和 AI 模型对话。

### Q：第一次打开 Claude Code 会怎样？

- **已配置 DeepSeek**：直接就能用，不需要登录 Claude 账号
- **未配置 DeepSeek**：Claude Code 会让你登录 Claude 账号（需要 Claude 订阅）。如果你没有订阅，请先去 [配置 DeepSeek](../03-deepseek-claudecode/README.md)

### Q：Claude Code 会自动保存吗？
**是的！** Claude Code 创建和修改的文件会直接保存到你的项目文件夹里。

### Q：我可以拒绝 Claude Code 的操作吗？
**当然可以！** 每次操作都会问你，按 `n` 就可以拒绝。

---

## 📌 下一步

你已经学会 Claude Code 的基本用法了！

👉 **[实用小技巧](./tips.md)** — 学会让 AI 更听话的秘诀

👉 **[⭐ 配置 Claude Code + DeepSeek](../03-deepseek-claudecode/README.md)** — 这是最核心的一步！
