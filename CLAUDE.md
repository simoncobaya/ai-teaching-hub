# AI Teaching Hub - 项目指南

## 🎯 项目定位

AI 教学中心：帮助 4-6 年级学生（9-12 岁）学会用 AI 工具编程的教育项目。

## 👥 目标用户

- **主要用户**：4-6 年级学生（9-12 岁），编程初学者
- **次要用户**：AI 竞赛选手、教学老师/教练
- **用户特点**：没有编程基础，中文母语，需要简单易懂的指导

## ✍️ 写作规范

### 语言风格
- **中文为主**，技术术语保留英文原文（如 API Key、CLI、IDE）
- **语气友好、鼓励式**，像大哥哥大姐姐在教弟弟妹妹
- 大量使用 emoji 让内容更生动（🎮 🐛 🎨 💡 等）
- 避免"显然"、"简单来说"等可能让学生感到挫败的表达

### 内容要求
- **步骤化**：所有操作都拆成 Step 1、Step 2、Step 3
- **可复制**：命令和代码都要能直接复制粘贴运行
- **有示例**：每个概念配一个具体例子（如"帮我写一个猜数字游戏 🎮"）
- **避免假设**：不假设学生已经知道任何编程概念，从零开始解释
- **费用透明**：明确标注哪些免费、哪些需要付费
- **跨平台兼容**：学生使用的电脑可能是 Windows、macOS 或 Linux。文档中出现与操作系统相关的命令行时，需要分别标注 Windows（PowerShell 和 CMD）、macOS、Linux，或使用三个系统通用的命令

### 格式规范
- 使用 Markdown 格式
- 表格对比不同选项
- 代码块标注语言类型（bash、python、toml 等）
- 用 `> 💡` 标注小贴士和注意事项

## 📁 项目结构

```
skills/          → CodeBuddy Skill 定义（agentmaker、wrong-answer-book）
docs/            → 教学文档
  ai-coding-tools/ → AI 编程工具全家桶教程（11+ 工具）
  agentmaker/      → AI 智能体制造者教程
  wrong-answer-book/ → 魔法错题本教程
  teacher/         → 教师教学材料
app/             → Flask Web 应用（错题本）
artifacts/       → 测试材料（试卷等）
```

## 🔧 技术栈

- **AI 编程工具**：Claude Code、Cursor、Codex CLI、OpenCode、TRAE、CodeBuddy、Qoder 等
- **AI 模型**：DeepSeek、智谱 GLM、OpenAI、Claude
- **配置管理**：CC Switch
- **Web 应用**：Python Flask
- **Skill 平台**：CodeBuddy

## 📌 重要提醒

- 内容面向儿童，**安全第一**：不展示真实 API Key、密码等敏感信息
- 所有外部链接要确保可访问
- 国内用户优先考虑网络可达性（标注国内/国际版入口）
- 费用说明要清晰，避免学生产生意外消费
