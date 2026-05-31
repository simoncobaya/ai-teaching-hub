# AI Teaching Hub

> 面向 AI 教育的 CodeBuddy Skill 集合——把 AI 工具变成孩子的学习伙伴。

---

## Skills

### 🤖 AI 智能体制造者

面向「全国青少年人工智能创新挑战赛 · AI 智能体开发专项赛」的参赛教练——从选题到交付，带学生 7 步完成一个获奖级 AI 智能体。

| 文档 | 说明 |
|------|------|
| [使用说明](docs/agentmaker/skills.md) | 安装、使用、交付件一览（含对话示例） |

安装：

```bash
# Linux / macOS
cp -r skills/agentmaker .codebuddy/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Path "skills/agentmaker" -Destination ".codebuddy\skills\"
```

```cmd
REM Windows CMD
xcopy /E /I "skills\agentmaker" ".codebuddy\skills\agentmaker"
```

> 💡 或直接对 CodeBuddy 说：「帮我安装当前项目的 agentmaker skill」

---

### 📝 魔法错题本

拍照上传试卷 → 自动识别批改 → 生成错题库 → 随时查漏补缺。支持 Skill 对话、CLI 命令行和 Web 界面三种使用方式。

| 文档 | 说明 |
|------|------|
| [使用说明](docs/wrong-answer-book/skills.md) | 安装、配置、使用指南（含对话示例） |
| [CLI 说明](docs/wrong-answer-book/cli.md) | 命令行版操作参考 |
| [Web 版说明](docs/wrong-answer-book/web.md) | Flask Web 界面使用说明 |

安装：

```bash
# Linux / macOS
cp -r skills/wrong-answer-book .codebuddy/skills/
```

```powershell
# Windows PowerShell
Copy-Item -Recurse -Path "skills/wrong-answer-book" -Destination ".codebuddy\skills\"
```

```cmd
REM Windows CMD
xcopy /E /I "skills\wrong-answer-book" ".codebuddy\skills\wrong-answer-book"
```

> 💡 或直接对 CodeBuddy 说：「帮我安装当前项目的 wrong-answer-book skill」

启动 Web 界面：

> 💡 对 CodeBuddy 说这句，自动装依赖、启动服务、打开浏览器：

```
帮我启动魔法错题本的 Web 界面：进入 app/wrong-answer-book 目录，安装依赖，然后用 python web_app.py 启动服务，启动后帮我打开浏览器。
```

---

## 项目结构

```
ai-teaching-hub/
├── skills/                          ← Skill 定义
│   ├── agentmaker/                  ← AI 智能体制造者
│   └── wrong-answer-book/           ← 魔法错题本
├── app/wrong-answer-book/           ← 错题本独立应用（Flask）
├── docs/                            ← 文档
│   ├── agentmaker/                  ← 智能体制造者使用说明
│   └── wrong-answer-book/           ← 错题本使用说明
└── artifacts/                       ← 测试素材
    └── wrong-answer-book/           ← 试卷图片（10 张）
```

---

## 快速开始

1. 打开 CodeBuddy，克隆本项目
2. 安装你需要的 Skill（见上方各 Skill 安装命令）
3. 在对话框中用对应的命令或自然语言触发

**AI 智能体制造者** 无需额外配置，安装后直接使用。

**魔法错题本** 需要配置腾讯云 OCR API 密钥，详见 [使用说明 - 配置 API 密钥](docs/wrong-answer-book/skills.md#配置-api-密钥)。
