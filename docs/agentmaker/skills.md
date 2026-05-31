# AI 智能体制造者 Skill

> 面向「全国青少年人工智能创新挑战赛 · AI 智能体开发专项赛」的参赛教练——从选题到交付，带学生 7 步完成一个获奖级 AI 智能体。

---

## 安装

将 Skill 复制到 CodeBuddy 的 skills 目录（已安装可跳过）：

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

在 CodeBuddy 对话框中确认 Skill 已加载。

> 💡 **懒得自己敲命令？** 把下面这句话复制到 CodeBuddy 对话框，让 AI 帮你搞定：

```
帮我安装当前项目的 agentmaker skill：把 skills/agentmaker 复制到项目的 .codebuddy/skills/ 目录。
```

---

## 使用

在 CodeBuddy 对话框中，用 `/agentmaker` 命令或直接说「我要参赛」「帮我设计一个智能体」即可触发。

Skill 会按 7 个阶段引导学生完成参赛作品：

| 阶段 | 名称 | 你得到的 |
|:---:|------|----------|
| 0 | **组别确认** | 确认所在学段，了解节点数硬性要求（小学 ≥5，初高中 ≥10） |
| 1 | **选题引导** | 多轮启发式对话 → 一票否决过滤 → 5 维度 13 项可行性评估 |
| 2 | **工作流设计** | 输出方案设计文档 v1.0，Subflow 三原则拆解，含判断节点设计 |
| 3 | **Skill 验证** | 在 CodeBuddy 中秒级测试工作流逻辑，快速迭代 |
| 4 | **Coze 搭建** | 逐节点配置文档，学生"拿文档就能操作" |
| 5 | **评分优化** | 13 项指标逐项检查，给出快速加分建议 |
| 6 | **交付件生成** | 一次性输出全部参赛材料 |

### 核心策略：Skill 先行、Coze 后置

先在 CodeBuddy 中用文本快速验证工作流逻辑（分钟级反馈），确认无误后再去 Coze 平台"照图纸施工"可视化搭建——省去 1-2 小时的盲目试错。

### 触发方式

```
/agentmaker                  → 启动参赛辅导
我要参加AI智能体比赛          → 同上
帮我设计一个智能体             → 同上
```

进入某个阶段后，直接自然对话即可，无需再输命令。

---

## 交付件

阶段 6 一次性输出 7 项参赛材料：

| 序号 | 交付件 | 说明 |
|:---:|--------|------|
| 1 | **方案设计文档** | 四章完整文档：需求分析 → 系统设计 → 关键技术 → 开发计划 |
| 2 | **Coze 搭建指南** | 逐节点配置表（输入/输出/模型/提示词/条件/代码），照做就行 |
| 3 | **SKILL.md** | 工作流"代码"，结构化执行步骤 |
| 4 | **附件 1** | 项目基本信息表（含选手信息、原创性声明） |
| 5 | **PPT 大纲** | 16 页答辩结构，含设计建议 |
| 6 | **视频脚本** | 5 分钟分镜脚本 + 拍摄 Checklist |
| 7 | **过程记录** | 开发日志 / 关键决策 / 版本迭代 / 测试记录 |

---

## 文件说明

```
skills/agentmaker/
├── SKILL.md                         ← 核心流程（7 阶段 + 门控规则）
├── scripts/                         ← 脚本目录（预留）
├── assets/                          ← 交付件模板（填空式）
│   ├── design-doc-template.md       ← 方案设计文档模板
│   ├── skill-template.md            ← SKILL.md 生成模板
│   ├── coze-node-config-template.md ← Coze 逐节点配置模板
│   ├── appendix1-template.md        ← 附件 1：项目基本信息表
│   ├── ppt-outline-template.md      ← PPT 大纲模板（16 页）
│   ├── video-script-template.md     ← 视频脚本模板（5 分钟）
│   └── process-log-template.md      ← 过程记录模板
└── references/                      ← 参考资料
    ├── competition-rules.md         ← 竞赛规则速查手册
    ├── official-competition-rules.md← 官方规则原文（兜底参考）
    ├── scoring-checklist.md         ← 13 项评分指标详解 + 优化清单
    ├── topic-ideas.md               ← 选题灵感库（4 组别 × 10 主题）
    ├── workflow-patterns.md         ← 工作流设计模式参考
    └── coze-build-guide.md          ← Coze 平台搭建通用 SOP
```

---

## 示例

### 从零开始参赛

```
用户：/agentmaker

Skill：
  欢迎来到 AI 智能体制造者！👋

  我是你的参赛教练，会带你一步步完成一个能获奖的 AI 智能体。

  首先，告诉我你所在的学段：
  - 小学低年级组（1-3 年级）
  - 小学高年级组（4-6 年级）
  - 初中组
  - 高中组

用户：小学高年级组

Skill：
  好的，小学高年级组的要求是：
  - 工作流节点数 ≥ 5
  - 作品需解决一个真实问题

  那我们开始想选题吧。你平时在学习或生活中，
  有没有觉得"要是能有个工具帮我……"的事情？

  （引导式对话，不低于 3 轮自主探索）
```

### 选题评估

```
用户：（经过多轮探讨，提出：校园失物招领智能助手）

Skill：
  这个选题不错，我来帮你分析一下：

  ✅ 扣题性：解决校园真实问题，符合"应用性"要求
  ✅ 创新性：失物招领 + AI 描述匹配，有差异化
  ✅ 可行性：5-7 个节点可实现，技术上不需要复杂模型
  ✅ 完整性：涉及用户输入 → AI 分析 → 数据库匹配 → 通知反馈
  ⚠️ 挑战点：数据来源需要事先整理失物库

  综合评分：88/100，建议推进 👉
```

### 输出交付件

```
用户：可以生成材料了

Skill：
  正在生成全部 7 项交付件……

  ✅ 方案设计文档 — design-doc-v1.3.md
  ✅ Coze 搭建指南 — coze-build-guide.md
  ✅ SKILL.md — skill-校园失物招领助手.md
  ✅ 附件 1 — 附录一-项目基本信息表.md
  ✅ PPT 大纲 — ppt-outline-v1.0.md
  ✅ 视频脚本 — video-script-v1.0.md
  ✅ 过程记录 — process-log.md

  所有文件已保存到项目目录，根据文件中的 [TODO] 提示补全即可提交！
```

---

## 常见问题

**Q: 这个 Skill 需要 API 密钥吗？**
A: 不需要。Skill 本身不调用外部 API，仅在阶段 4 引导你到 Coze 平台搭建时需要 Coze 账号。

**Q: 适合零基础的学生吗？**
A: 适合。Skill 以"教练对话"方式引导，选题、设计、搭建每一步都有模板和参考，学生主要工作是思考和决策。

**Q: 不同学段有什么区别？**
A: 小学组节点数要求 ≥5，不强制 Subflow；初高中组要求 ≥10，建议使用 Subflow 和多智能体协同。Skill 会根据你选的组别自动调整引导策略。

**Q: 选题有什么红线？**
A: 三种情况直接淘汰：① AI 代写方案/报告；② 纯代码编程（未体现工作流和大模型决策）；③ 人文艺术类（小故事、音乐、美术等）。

**Q: 在 Coze 搭建遇到问题怎么办？**
A: 说「Coze 搭建遇到问题」即可，Skill 会检索最新 Coze 平台信息，按"从底层到顶层"顺序逐步指导。
