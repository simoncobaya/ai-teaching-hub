# 🤖 Claude Code 是什么？

> Claude Code 是一个住在终端里的 AI 编程小伙伴。你跟它说话，它就帮你写代码、改代码、运行程序！

---

## 🤔 Claude Code 是什么？

Claude Code 是 **Anthropic 公司**（就是做 Claude AI 的公司）开发的 **终端编程工具**。

简单理解：
- 📟 它运行在一个 **黑色的终端窗口** 里
- 💬 你用 **自然语言**（普通的话）和它对话
- 💻 它帮你 **写代码、改代码、运行程序**
- 📁 它能 **理解整个项目**，不只是单个文件

---

## 🌟 Claude Code 的超能力

### 1. 📖 读懂整个项目

Claude Code 不只是看一个文件，它能理解你的 **整个项目**：
- 知道哪些文件互相依赖
- 理解项目的结构
- 修改一个地方时，知道其他地方要怎么改

### 2. 🔧 直接操作文件

Claude Code 可以：
- ✏️ 创建新文件
- 📝 修改已有文件
- 🗑️ 删除文件
- 📂 创建文件夹

### 3. ▶️ 运行命令

Claude Code 可以帮你：
- 🏃 运行程序
- 📦 安装依赖包
- 🧪 运行测试
- 🔍 查找文件

### 4. 🔄 支持多种 AI 模型

Claude Code 不只能用 Claude，还可以用：
- 🐋 DeepSeek（便宜又好！）
- 🧠 GLM（智谱的模型）
- 📝 其他 OpenAI 兼容的模型

> ⭐ **这就是为什么我们要配置 Claude Code + DeepSeek** — 用最好的工具搭配最便宜的模型！

---

## 📺 Claude Code 长什么样？

Claude Code 运行在终端（也叫命令行、Terminal）里：

```
╭──────────────────────────────────────────────╮
│  🤖 Claude Code                               │
│                                                │
│  > 帮我写一个猜数字游戏                        │
│                                                │
│  好的！我来帮你写一个猜数字游戏。              │
│                                                │
│  📝 创建文件：guess_number.py                  │
│  ```python                                     │
│  import random                                 │
│                                                │
│  target = random.randint(1, 100)               │
│  ...                                           │
│  ```                                           │
│                                                │
│  ✅ 文件已创建！你可以运行 python guess_number.py│
╰──────────────────────────────────────────────╯
```

---

## 🖥️ Claude Code 的多种使用方式

Claude Code 不只是终端工具！现在有很多方式可以使用它：

| 使用方式 | 说明 | 适合谁 |
|---------|------|--------|
| 📟 终端（CLI） | 在命令行里输入 `claude` 使用 | 喜欢命令行的同学（本教程重点！） |
| 🖥️ 桌面应用 | 有图形界面的 Claude Code 应用 | 喜欢图形界面的同学 |
| 🔌 VS Code 扩展 | 在 VS Code 编辑器里使用 | 已经在用 VS Code 的同学 |
| 🔌 JetBrains 扩展 | 在 JetBrains IDE 里使用 | 用 JetBrains 的同学 |

> 💡 **本教程主要教终端版（CLI）**，因为它最灵活、最强大！
> 其他使用方式可以在 Claude Code 官网了解更多。

---

## 🆚 Claude Code vs 其他工具

| 特点 | Claude Code | CodeBuddy | Cursor | TRAE |
|------|-------------|-----------|--------|------|
| 类型 | 终端工具 | CLI + IDE | IDE 编辑器 | IDE 编辑器 |
| 界面 | 命令行 | 都有 | 图形界面 | 图形界面 |
| 适合 | 喜欢命令行的同学 | 想用国内工具的同学 | 喜欢图形界面的同学 | 想免费用的同学 |
| AI 模型 | 可切换 | 内置多种 | 可切换 | 内置免费 |
| 价格 | 工具免费，需 Claude 订阅或 API | 个人版限时免费 | 有免费版，有付费版 | 个人版免费，企业版收费 |

> 💰 **Claude Code 费用说明**：
> - Claude Code 工具本身是 **免费** 的
> - 但使用它需要 **Claude 订阅**（Pro $20/月 或 Max $100/月）
> - 或者用 **API 按量付费**（用多少付多少）
> - ⭐ **省钱秘诀**：配置 DeepSeek 模型后，费用会便宜很多！

> 💡 **选择建议**：如果你喜欢图形界面，用 Cursor 或 TRAE；如果你想学更高级的操作，用 Claude Code！

---

## 🔗 相关链接

| 名称 | 链接 |
|------|------|
| Claude Code 官网 | https://code.claude.com/ |
| Claude Code 文档 | https://code.claude.com/docs/ |
| Claude Code GitHub | https://github.com/anthropics/claude-code |

---

## 📌 下一步

了解 Claude Code 之后，让我们安装它！

👉 **[安装 Claude Code](./install.md)** — 在你的电脑上安装 Claude Code
