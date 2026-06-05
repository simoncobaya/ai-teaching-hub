# ⚡ 切换模型与供应商

> 学会用 CC Switch 在不同 AI 供应商和模型之间快速切换！

---

## 🎯 目标

学会在 CC Switch 中切换供应商，以及在 Claude Code 中切换模型层级。

---

## 🔄 两种切换有什么区别？

| 操作 | 在哪操作 | 说明 |
|------|---------|------|
| **切换供应商** | CC Switch | 在 DeepSeek、Claude、GLM 等之间切换 |
| **切换模型层级** | Claude Code `/model` | 在 sonnet、opus、haiku 之间切换 |

> 💡 `/model` 命令**不能**在供应商之间切换（比如从 DeepSeek 切到 Claude）。供应商切换只能在 CC Switch 中完成。

---

## 🚀 切换供应商（在 CC Switch 中）

1. 打开 CC Switch
2. 在左侧导航栏，点击你想使用的工具（如 **Claude Code**）
3. 在该工具的页面中，找到你想启用的供应商卡片（如 DeepSeek 或 Claude Official）
4. 点击供应商卡片上的 **「启用」** 按钮
5. CC Switch 会通过本地代理自动将请求路由到新供应商

> ✅ 不需要手动编辑任何配置文件！CC Switch 的本地代理会帮你处理切换，**也不需要重启工具**。

---

## 🚀 切换模型层级（在 Claude Code 中）

在 Claude Code 对话中，你可以用 `/model` 命令切换模型层级：

```
/model             ← 查看可用的模型层级
/model sonnet      ← 切换到 Sonnet（日常使用，推荐）
/model opus        ← 切换到 Opus（最强，适合难题）
/model haiku       ← 切换到 Haiku（最快，适合简单任务）
```

---

## 📊 常用场景

### 场景 1：日常编程 → DeepSeek + Sonnet

在 CC Switch 中启用 DeepSeek，然后在 Claude Code 中用 `/model sonnet`。

便宜又好，适合大部分编程任务。

### 场景 2：遇到难题 → DeepSeek + Opus

在 Claude Code 中输入：

```
/model opus
```

Opus 会花更多时间思考，给出更好的答案。

### 场景 3：需要最强能力 → 切换到 Claude

在 CC Switch 中启用 **Claude Official** 供应商，然后在 Claude Code 中用 `/model sonnet` 或 `/model opus`。

Claude 的推理能力最强，但价格较高。

### 场景 4：中文特别好的模型 → GLM

在 CC Switch 中启用 **ZhipuAI/GLM** 供应商。

---

## 💡 切换技巧

### 技巧 1：根据任务选择

| 任务类型 | 推荐方案 |
|---------|---------|
| 写新功能 | DeepSeek + Sonnet |
| 找 Bug | DeepSeek + Opus |
| 复杂重构 | Claude + Opus |
| 中文文档 | DeepSeek + Sonnet |
| 学习理解 | DeepSeek + Sonnet |

### 技巧 2：先试便宜的

遇到问题时，按照这个顺序尝试：

```
1. 先用 DeepSeek + Sonnet（最便宜）
2. 解决不了 → /model opus（稍贵但更强）
3. 还是不行 → 在 CC Switch 切到 Claude（最强但最贵）
```

### 技巧 3：让 AI 帮你判断

你可以问 AI：

```
这个问题你自己能解决吗？如果觉得需要更强的模型，请告诉我。
```

---

## 📌 下一步

👉 **[管理多个工具](./manage-tools.md)** — 用 CC Switch 同时管理 Claude Code、Codex、OpenCode 等

👉 **[MCP 服务器管理](./mcp-management.md)** — 给 AI 工具添加额外能力
