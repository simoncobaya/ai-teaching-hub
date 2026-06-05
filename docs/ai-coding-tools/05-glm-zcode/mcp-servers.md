# 📦 智谱专属 MCP 服务器

> 智谱 Coding Plan 用户可以使用独家 MCP 服务器，给 AI 工具加上"超能力"！

---

## 🤔 MCP 服务器有什么用？

MCP（Model Context Protocol）让 AI 工具能连接外部服务。智谱 Coding Plan 提供了 **4 个专属 MCP**：

---

## 🌟 四大专属 MCP

### 1. 👁️ 视觉理解 MCP

让 AI 能 **看懂图片**！

| 能力 | 说明 |
|------|------|
| 看 UI 设计图 | 分析设计稿并生成对应代码 |
| 看流程图 | 理解架构图和逻辑图 |
| 看截图 | 从截图中提取信息和错误 |
| OCR 识别 | 从图片中提取文字 |

> 🧠 底层使用 **GLM-4.6V** 视觉推理模型，看图能力很强！

**使用场景举例**：
```
[上传一张 UI 设计截图]
请根据这个设计图，帮我用 HTML + CSS 写出对应的网页代码。
```

---

### 2. 🔍 网络搜索 MCP

让 AI 能 **搜索互联网**！

| 能力 | 说明 |
|------|------|
| 搜索技术文档 | 查找最新的 API 文档 |
| 搜索解决方案 | 查找编程问题的答案 |
| 获取实时信息 | 查询最新的技术动态 |

**使用场景举例**：
```
搜索一下 Python 3.12 有什么新特性
```

---

### 3. 🌐 网页读取 MCP

让 AI 能 **读取网页内容**！

| 能力 | 说明 |
|------|------|
| 读取网页 | 获取任意网页的完整内容 |
| 提取信息 | 提取标题、正文、链接等 |
| 解析结构 | 分析网页的结构和布局 |

**使用场景举例**：
```
读取这个网页的内容：https://docs.python.org/3/tutorial/
然后帮我总结 Python 入门教程的要点。
```

---

### 4. 📂 开源仓库 MCP

让 AI 能 **访问 GitHub 仓库**！

| 能力 | 说明 |
|------|------|
| 查看目录结构 | 快速了解项目布局 |
| 读取文件内容 | 查看 GitHub 上的代码 |
| 搜索代码 | 在仓库中搜索关键词 |

**使用场景举例**：
```
看一下这个 GitHub 仓库的结构：
https://github.com/python/cpython
告诉我 Python 源码是怎么组织的。
```

---

## 🚀 如何启用 MCP

### 方式一：用 Coding Tool Helper（推荐）

```bash
npx @z_ai/coding-helper
```

运行后选择"配置 MCP 服务器"，自动完成配置。

### 方式二：在 CC Switch 中启用

1. 打开 CC Switch
2. 进入 MCP 管理页面
3. 找到智谱专属 MCP
4. 启用你需要的 MCP

### 方式三：手动配置

在 `~/.claude/settings.json` 中添加 MCP 配置：

```json
{
  "mcpServers": {
    "glm-vision": {
      "command": "npx",
      "args": ["-y", "@z_ai/mcp-vision"],
      "env": {
        "ZHIPU_API_KEY": "你的智谱API-Key"
      }
    },
    "glm-search": {
      "command": "npx",
      "args": ["-y", "@z_ai/mcp-search"],
      "env": {
        "ZHIPU_API_KEY": "你的智谱API-Key"
      }
    }
  }
}
```

> ⚠️ 具体的 MCP 包名和参数请参考智谱官方文档：https://docs.bigmodel.cn/cn/coding-plan/quick-start

---

## 💡 使用建议

| MCP | 什么时候用 |
|-----|-----------|
| 👁️ 视觉理解 | 需要 AI 看图时（设计稿、截图、流程图） |
| 🔍 网络搜索 | 需要查找最新信息时 |
| 🌐 网页读取 | 需要读取在线文档或网页内容时 |
| 📂 开源仓库 | 需要参考 GitHub 上的开源代码时 |

> 💡 **建议**：全部启用！这些 MCP 不额外收费，而且能让你的 AI 编程工具更强大。

---

## 📌 下一步

👉 **[ZCode 编程工具简介](./zcode-intro.md)**

👉 **[Cursor IDE 教程](../06-cursor/README.md)**
